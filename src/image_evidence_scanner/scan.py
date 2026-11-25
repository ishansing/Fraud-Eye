from datetime import datetime, timezone
from importlib.metadata import version

from image_evidence_scanner.image_input import inspect_image
from image_evidence_scanner.assessment import assess
from image_evidence_scanner.metadata import extract_metadata
from image_evidence_scanner.provenance import validate_provenance


def scan_batch(paths: list[str]) -> dict:
    images = []
    for path in paths:
        try:
            image, image_bytes = inspect_image(path)
            image.update(assess())
            if image_bytes is not None and image["processing_status"] == "processed":
                try:
                    metadata = extract_metadata(image_bytes)
                except Exception:
                    metadata = {
                        "status": "error",
                        "metadata": {},
                        "coverage": {
                            "name": "ExifTool",
                            "version": None,
                            "status": "error",
                            "groups": [],
                            "errors": ["metadata extraction failed unexpectedly"],
                            "unknown_tags_requested": True,
                            "limitations": [
                                "Unrecognized binary blocks may remain opaque to the parser."
                            ],
                        },
                    }
                image["metadata"] = metadata["metadata"]
                image["metadata_status"] = metadata["status"]
                image["parser_coverage"] = [
                    metadata["coverage"],
                    {
                        "name": "Pillow",
                        "version": version("Pillow"),
                        "status": "complete",
                        "groups": ["format", "dimensions", "mode", "frames"],
                        "errors": [],
                    },
                ]
                image["metadata_unverified"] = True
                try:
                    image["provenance"] = validate_provenance(image_bytes, image["detected_format"])
                except Exception:
                    image["provenance"] = {
                        "status": "validator_error",
                        "error": "C2PA validation failed unexpectedly",
                        "revocation_status": "not_checked_offline",
                    }
                image["analysis_status"] = (
                    "complete"
                    if metadata["status"] == "complete"
                    and image["provenance"]["status"] not in {"unsupported", "validator_error"}
                    else "partial"
                )
            else:
                image["analysis_status"] = "failed"
            images.append(image)
        except Exception:
            images.append(
                {
                    "input_path": path,
                    "processing_status": "failed",
                    "sha256": None,
                    "sha256_status": "not_computed",
                    "detected_format": None,
                    "file_size": None,
                    "image_facts": None,
                    "verdict": "inconclusive",
                    "error": "analysis failed unexpectedly",
                    "sha256_error": "analysis failed before a digest was available",
                    "analysis_status": "failed",
                    **assess(),
                }
            )
    failures = sum(image["analysis_status"] != "complete" for image in images)
    if failures == 0:
        batch_status = "complete"
    elif failures == len(images):
        batch_status = "failed"
    else:
        batch_status = "partial"

    return {
        "schema_version": "1.0",
        "scan_timestamp": datetime.now(timezone.utc).isoformat(),
        "tool_version": version("image-evidence-scanner"),
        "batch_status": batch_status,
        "images": images,
    }
