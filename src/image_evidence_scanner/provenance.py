import json
import subprocess
import sys
from importlib.metadata import version

MAX_PROVENANCE_BYTES = 8 * 1024 * 1024
VALIDATOR_TIMEOUT_SECONDS = 10


def validate_provenance(image_bytes: bytes, image_format: str) -> dict:
    if image_format not in {"JPEG", "PNG"}:
        return _result("unsupported", "unsupported image format")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "image_evidence_scanner.c2pa_worker", image_format],
            input=image_bytes,
            capture_output=True,
            timeout=VALIDATOR_TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return _result("validator_error", "C2PA validation timed out")
    except OSError:
        return _result("validator_error", "C2PA validator could not be started")

    if len(result.stdout) > MAX_PROVENANCE_BYTES + 64 * 1024:
        return _result("validator_error", "C2PA output exceeded the 8 MiB limit")
    try:
        report = json.loads(result.stdout)
    except json.JSONDecodeError:
        return _result("validator_error", "C2PA validator returned invalid JSON")
    if result.returncode != 0 or not isinstance(report, dict):
        return _result("validator_error", "C2PA validator failed")

    report["validator"] = {"name": "c2pa-python", "version": version("c2pa-python")}
    report["revocation_status"] = "not_checked_offline"
    report["network_policy"] = {"remote_manifest_fetch": False, "ocsp_fetch": False}
    return report


def _result(status: str, error: str | None) -> dict:
    return {
        "status": status,
        "signer": None,
        "actions": [],
        "binding": None,
        "validation_details": None,
        "manifest": None,
        "revocation_status": "not_checked_offline",
        "validator": {"name": "c2pa-python", "version": version("c2pa-python")},
        "network_policy": {"remote_manifest_fetch": False, "ocsp_fetch": False},
        "error": error,
    }
