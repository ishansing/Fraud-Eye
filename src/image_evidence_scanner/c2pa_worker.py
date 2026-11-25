import io
import json
import sys

from c2pa import C2paError, Context, Reader

MAX_MANIFEST_BYTES = 8 * 1024 * 1024
MAX_FILE_BYTES = 100 * 1024 * 1024


def validate(image_bytes: bytes, image_format: str) -> dict:
    content_type = {"JPEG": "image/jpeg", "PNG": "image/png"}[image_format]
    try:
        context = Context.from_dict(
            {"verify": {"remote_manifest_fetch": False, "ocsp_fetch": False}}
        )
        with context:
            with Reader(content_type, io.BytesIO(image_bytes), context=context) as reader:
                manifest_json = reader.json()
    except C2paError.ManifestNotFound:
        return _result("absent")
    except C2paError.NotSupported:
        return _result("unsupported", error="C2PA validation is unsupported for this asset")
    except (C2paError.Signature, C2paError.Verify):
        return _result("present_but_invalid")
    except Exception:
        return _result("validator_error", error="C2PA validator failed")

    if len(manifest_json.encode("utf-8")) > MAX_MANIFEST_BYTES:
        return _result("validator_error", error="C2PA report exceeded the 8 MiB limit")
    try:
        manifest_store = json.loads(manifest_json)
    except json.JSONDecodeError:
        return _result("validator_error", error="C2PA validator returned invalid JSON")
    if not isinstance(manifest_store, dict):
        return _result("validator_error", error="C2PA validator returned an unexpected report")

    active_key = manifest_store.get("active_manifest")
    active_manifest = manifest_store.get("manifests", {}).get(active_key, {})
    validation = manifest_store.get("validation_status", [])
    if not isinstance(active_manifest, dict) or not isinstance(validation, list):
        return _result("validator_error", error="C2PA validator returned an unexpected report")
    signature_info = active_manifest.get("signature_info") or {}
    if not isinstance(signature_info, dict):
        signature_info = {}
    invalid = any(
        isinstance(item, dict)
        and str(item.get("status", item.get("severity", ""))).lower()
        in {"invalid", "error", "failure"}
        for item in validation
    )
    if invalid or signature_info.get("valid") is False:
        status = "present_but_invalid"
    elif signature_info.get("trusted") is True:
        status = "trusted_valid"
    else:
        status = "valid_but_untrusted"

    return {
        "status": status,
        "signer": signature_info,
        "actions": active_manifest.get("assertions", []),
        "binding": active_manifest.get("claim", {}),
        "validation_details": validation,
        "manifest": active_manifest,
        "error": None,
    }


def _result(status: str, error: str | None = None) -> dict:
    return {
        "status": status,
        "signer": None,
        "actions": [],
        "binding": None,
        "validation_details": None,
        "manifest": None,
        "error": error,
    }


if __name__ == "__main__":
    content_type = sys.argv[1]
    image_bytes = sys.stdin.buffer.read(MAX_FILE_BYTES + 1)
    if len(image_bytes) > MAX_FILE_BYTES:
        result = _result("validator_error", "image exceeded the C2PA input bound")
    else:
        result = validate(image_bytes, content_type)
    output = json.dumps(result, ensure_ascii=True)
    if len(output.encode("utf-8")) > MAX_MANIFEST_BYTES + 64 * 1024:
        output = json.dumps(
            _result("validator_error", error="C2PA output exceeded the 8 MiB limit")
        )
    print(output)
