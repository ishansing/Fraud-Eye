import json


def render_text(report: dict) -> str:
    lines = []
    for image in report["images"]:
        lines.extend(
            [
                f"Image: {json.dumps(image['input_path'], ensure_ascii=True)}",
                f"Verdict: {image['verdict']}",
                f"Generation: {image['generation']['decision']} (score {image['generation']['score_semantics']})",
                f"Editing: {image['editing']['decision']} (score {image['editing']['score_semantics']})",
                f"Interpretation: {image['interpretation']}",
                f"Advisory: {image['advisory']}",
                f"Status: {image['processing_status']}",
            ]
        )
        if image["sha256"]:
            lines.append(f"SHA-256: {image['sha256']}")
        if image["error"]:
            lines.append(f"Reason: {image['error']}")
        if "metadata_status" in image:
            lines.append(f"Metadata coverage: {image['metadata_status']}")
            lines.append(f"Provenance: {image['provenance']['status']}")
        if image.get("pixel_signals"):
            lines.append("Evidence: global channel statistics (not localized)")
    failed = sum(image.get("analysis_status") != "complete" for image in report["images"])
    lines.append(
        f"Batch: {report['batch_status']} ({len(report['images']) - failed}/{len(report['images'])} processed)"
    )
    return "\n".join(lines)
