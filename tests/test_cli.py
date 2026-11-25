import subprocess
import sys


def test_module_cli_help_describes_image_paths():
    result = subprocess.run(
        [sys.executable, "-m", "image_evidence_scanner", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "usage:" in result.stdout
    assert "IMAGE" in result.stdout
    assert "one to five" in result.stdout


def test_module_cli_reports_unreadable_input():
    result = subprocess.run(
        [sys.executable, "-m", "image_evidence_scanner", "example.jpg"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "Status: failed" in result.stdout
    assert "unable to read input file" in result.stdout
