import json
import os
import shutil
import subprocess
import sys

from PIL import Image


def run_cli(*args, env=None):
    return subprocess.run(
        [sys.executable, "-m", "image_evidence_scanner", *map(str, args)],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )


def image_with_description(path, description):
    exif = Image.Exif()
    exif[0x010E] = description
    Image.new("RGB", (2, 3), "red").save(path, format="JPEG", exif=exif)
    return path


def test_metadata_is_reported_but_sensitive_values_are_not_printed(tmp_path):
    secret = "private-location-description"
    image = image_with_description(tmp_path / "photo.jpg", secret)
    report = tmp_path / "report.json"

    result = run_cli("--json-output", report, image)
    data = json.loads(report.read_text())

    assert result.returncode == 0
    assert data["images"][0]["metadata_status"] == "complete"
    assert data["images"][0]["metadata"]["IFD0:ImageDescription"] == secret
    assert data["images"][0]["parser_coverage"][0]["version"]
    assert secret not in result.stdout
    assert data["images"][0]["metadata_unverified"] is True


def test_exiftool_extracts_xmp_and_iptc_values(tmp_path):
    image = image_with_description(tmp_path / "photo.jpg", "camera description")
    subprocess.run(
        [
            shutil.which("exiftool"),
            "-overwrite_original",
            "-XMP-dc:Description=private-xmp-value",
            "-IPTC:Caption-Abstract=private-iptc-value",
            str(image),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    report = tmp_path / "report.json"

    result = run_cli("--json-output", report, image)
    data = json.loads(report.read_text())
    metadata = data["images"][0]["metadata"]

    assert result.returncode == 0
    assert metadata["XMP-dc:Description"] == "private-xmp-value"
    assert metadata["IPTC:Caption-Abstract"] == "private-iptc-value"
    assert result.stdout.find("private-xmp-value") == -1
    assert result.stdout.find("private-iptc-value") == -1


def test_c2pa_absence_is_neutral_and_revocation_limitation_is_reported(tmp_path):
    image = tmp_path / "plain.png"
    Image.new("RGB", (1, 1), "red").save(image)
    report = tmp_path / "report.json"

    result = run_cli("--json-output", report, image)
    data = json.loads(report.read_text())
    provenance = data["images"][0]["provenance"]

    assert result.returncode == 0
    assert provenance["status"] == "absent"
    assert provenance["revocation_status"] == "not_checked_offline"
    assert provenance["network_policy"] == {
        "remote_manifest_fetch": False,
        "ocsp_fetch": False,
    }


def test_missing_exiftool_is_explicit_and_preserves_image_facts(tmp_path):
    image = tmp_path / "plain.png"
    Image.new("RGB", (1, 1), "red").save(image)
    report = tmp_path / "report.json"
    env = os.environ.copy()
    env["PATH"] = str(tmp_path)

    result = run_cli("--json-output", report, image, env=env)
    data = json.loads(report.read_text())

    assert result.returncode != 0
    assert data["images"][0]["image_facts"]["width"] == 1
    assert data["images"][0]["metadata_status"] == "unavailable"
    assert data["images"][0]["parser_coverage"][0]["status"] == "unavailable"


def test_exiftool_timeout_is_reported_instead_of_hanging(tmp_path):
    image = tmp_path / "plain.png"
    Image.new("RGB", (1, 1), "red").save(image)
    executable_dir = tmp_path / "bin"
    executable_dir.mkdir()
    exiftool = executable_dir / "exiftool"
    exiftool.write_text(f"#!{sys.executable}\nimport time\ntime.sleep(30)\n")
    exiftool.chmod(0o755)
    env = os.environ.copy()
    env["PATH"] = str(executable_dir)
    report = tmp_path / "report.json"

    result = run_cli("--json-output", report, image, env=env)
    data = json.loads(report.read_text())

    assert result.returncode != 0
    assert data["images"][0]["parser_coverage"][0]["status"] == "error"
    assert "timed out" in data["images"][0]["parser_coverage"][0]["errors"][0]


def test_exiftool_output_limit_is_enforced(tmp_path):
    image = tmp_path / "plain.png"
    Image.new("RGB", (1, 1), "red").save(image)
    executable_dir = tmp_path / "bin"
    executable_dir.mkdir()
    exiftool = executable_dir / "exiftool"
    exiftool.write_text(
        f"#!{sys.executable}\nimport sys\nsys.stdout.write('x' * (17 * 1024 * 1024))\n"
    )
    exiftool.chmod(0o755)
    env = os.environ.copy()
    env["PATH"] = str(executable_dir)
    report = tmp_path / "report.json"

    result = run_cli("--json-output", report, image, env=env)
    data = json.loads(report.read_text())

    assert result.returncode != 0
    assert data["images"][0]["parser_coverage"][0]["status"] == "error"
    assert "16 MiB" in data["images"][0]["parser_coverage"][0]["errors"][0]
