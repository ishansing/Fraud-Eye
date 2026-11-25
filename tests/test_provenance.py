import json

from image_evidence_scanner import c2pa_worker


def test_active_manifest_validation_uses_offline_settings(monkeypatch):
    calls = []

    class FakeContext:
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    class FakeReader:
        def __init__(self, *args, **kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def json(self):
            return json.dumps(
                {
                    "active_manifest": "active",
                    "manifests": {
                        "active": {
                            "signature_info": {"valid": True, "trusted": False},
                            "assertions": [],
                            "claim": {},
                        }
                    },
                    "validation_status": [],
                }
            )

    def offline_context(settings):
        calls.append(settings)
        return FakeContext()

    monkeypatch.setattr(c2pa_worker.Context, "from_dict", offline_context)
    monkeypatch.setattr(c2pa_worker, "Reader", FakeReader)

    result = c2pa_worker.validate(b"local-image-bytes", "PNG")

    assert result["status"] == "valid_but_untrusted"
    assert calls == [{"verify": {"remote_manifest_fetch": False, "ocsp_fetch": False}}]
