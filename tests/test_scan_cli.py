import hashlib
import json
import struct
import subprocess
import sys
import zlib

from PIL import Image


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "image_evidence_scanner", *map(str, args)],
        check=False,
        capture_output=True,
        text=True,
    )


def make_image(path, image_format="PNG"):
    Image.new("RGB", (2, 3), "red").save(path, format=image_format)
    return path


def oversized_pixel_png(path):
    width, height = 10_000, 5_001
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)

    def chunk(kind, data):
        return (
            struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))
        )

    path.write_bytes(
        b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", b"") + chunk(b"IEND", b"")
    )
    return path


def scan_json(*args):
    output = args[0]
    result = run_cli("--json-output", output, *args[1:])
    return result, json.loads(output.read_text())


def test_cli_scans_jpeg_and_png_and_reports_original_hash_and_facts(tmp_path):
    png = make_image(tmp_path / "photo.png")
    jpeg = make_image(tmp_path / "photo.jpg", "JPEG")
    report = tmp_path / "report.json"

    result, data = scan_json(report, png, jpeg)

    assert result.returncode == 0
    assert len(data["images"]) == 2
    first, second = data["images"]
    assert first["processing_status"] == second["processing_status"] == "processed"
    assert first["sha256"] == hashlib.sha256(png.read_bytes()).hexdigest()
    assert first["detected_format"] == "PNG"
    assert first["generation"]["decision"] == "inconclusive"
    assert first["editing"]["decision"] == "inconclusive"
    assert first["advisory"] == "inconclusive"
    assert first["image_facts"] == {
        "width": 2,
        "height": 3,
        "aspect_ratio": 2 / 3,
        "mode": "RGB",
        "color_space": None,
        "bit_depth_per_channel": 8,
        "frame_count": 1,
    }
    assert first["file_structure"]["container"] == "PNG"
    assert first["file_structure"]["chunk_types"] == {
        "IHDR": 1,
        "IDAT": 1,
        "IEND": 1,
    }
    assert second["detected_format"] == "JPEG"
    assert first["verdict"] == "inconclusive"
    assert "Verdict: inconclusive" in result.stdout
    assert "Generation: inconclusive (score not_available)" in result.stdout
    assert "Model/data profile: not configured" in result.stdout
    assert "Limitations:" in result.stdout
    assert "Advisory: inconclusive" in result.stdout
    assert result.stdout.index("Verdict:") < result.stdout.index("Generation:")
    assert result.stdout.index("Generation:") < result.stdout.index("Evidence:")
    assert result.stdout.index("Evidence:") < result.stdout.index("Model/data profile:")
    assert result.stdout.index("Model/data profile:") < result.stdout.index("Advisory:")
    assert result.stdout.index("Advisory:") < result.stdout.index("Limitations:")


def test_cli_reports_global_channel_distribution_without_localization(tmp_path):
    image = tmp_path / "pixels.png"
    pixels = Image.new("RGB", (2, 1))
    pixels.putdata([(0, 0, 0), (255, 128, 64)])
    pixels.save(image)
    result, data = scan_json(tmp_path / "report.json", image)
    signals = data["images"][0]["pixel_signals"]

    assert result.returncode == 0
    channels = signals["result"]["channels"]
    assert [channel["mean"] for channel in channels] == [127.5, 64.0, 32.0]
    assert [channel["maximum"] for channel in channels] == [255, 128, 64]
    assert all(sum(channel["histogram"]) == 2 for channel in channels)
    assert signals["result"]["jpeg"] is None
    assert signals["prerequisites"]
    assert signals["reference_data"] is None
    assert "localization" not in signals


def test_cli_reports_jpeg_quantization_and_subsampling(tmp_path):
    jpeg = make_image(tmp_path / "photo.jpg", "JPEG")
    result, data = scan_json(tmp_path / "report.json", jpeg)
    image = data["images"][0]
    signals = image["pixel_signals"]
    jpeg_signals = signals["result"]["jpeg"]

    assert result.returncode == 0
    assert jpeg_signals["quantization_tables"]
    assert jpeg_signals["subsampling"] in {"4:4:4", "4:2:2", "4:2:0", "unknown"}
    assert image["file_structure"]["container"] == "JPEG"
    assert image["file_structure"]["quantization_table_count"] == len(
        jpeg_signals["quantization_tables"]
    )


def test_cli_bounds_png_chunk_structure_scan(tmp_path):
    image = make_image(tmp_path / "many-chunks.png")
    png = bytearray(image.read_bytes())
    iend_offset = png.rfind(b"IEND") - 4
    chunk_type = b"vpAg"
    empty_chunk = struct.pack(">I", 0) + chunk_type + struct.pack(">I", zlib.crc32(chunk_type))
    png[iend_offset:iend_offset] = empty_chunk * 100_001
    image.write_bytes(png)

    result, data = scan_json(tmp_path / "report.json", image)
    structure = data["images"][0]["file_structure"]

    assert result.returncode == 0
    assert structure["chunk_count"] == 100_000
    assert structure["chunk_types"] == {"IHDR": 1, "IDAT": 1}
    assert structure["other_chunk_count"] == 99_998
    assert structure["truncated"] is True


def test_cli_accepts_five_inputs(tmp_path):
    image = make_image(tmp_path / "photo.png")

    result, data = scan_json(tmp_path / "report.json", *([image] * 5))

    assert result.returncode == 0
    assert len(data["images"]) == 5
    assert data["batch_status"] == "complete"


def test_invalid_input_does_not_suppress_successful_result(tmp_path):
    good = make_image(tmp_path / "good.png")
    missing = tmp_path / "missing.png"
    report = tmp_path / "report.json"

    result, data = scan_json(report, good, missing)

    assert result.returncode != 0
    assert [image["processing_status"] for image in data["images"]] == ["processed", "failed"]
    assert data["batch_status"] == "partial"
    assert data["images"][1]["error"]


def test_cli_rejects_invalid_batch_sizes_before_creating_report(tmp_path):
    image = make_image(tmp_path / "one.png")

    for paths in [[], [image] * 6]:
        report = tmp_path / f"report-{len(paths)}.json"
        result = run_cli("--json-output", report, *paths)
        assert result.returncode != 0
        assert "one to five" in result.stderr
        assert not report.exists()


def test_cli_rejects_directories_and_urls(tmp_path):
    result = run_cli(tmp_path)
    assert result.returncode != 0
    assert "director" in result.stdout.lower() or "director" in result.stderr.lower()

    result = run_cli("https://example.invalid/image.png")
    assert result.returncode != 0
    assert "url" in result.stdout.lower() or "url" in result.stderr.lower()


def test_cli_rejects_oversized_input_before_decoding(tmp_path):
    oversized = tmp_path / "oversized.png"
    with oversized.open("wb") as file:
        file.truncate(100 * 1024 * 1024 + 1)

    result, data = scan_json(tmp_path / "report.json", oversized)

    assert result.returncode != 0
    assert data["images"][0]["processing_status"] == "failed"
    assert "100 MiB" in data["images"][0]["error"]
    assert data["images"][0]["sha256_status"] == "not_computed"
    assert data["images"][0]["sha256_error"]


def test_cli_rejects_images_over_pixel_limit_before_decoding(tmp_path):
    path = oversized_pixel_png(tmp_path / "large.png")

    result, data = scan_json(tmp_path / "report.json", path)

    assert result.returncode != 0
    assert "50,000,000" in data["images"][0]["error"]


def test_cli_rejects_malformed_unsupported_and_multiframe_images(tmp_path):
    malformed = tmp_path / "malformed.png"
    malformed.write_bytes(b"not an image")
    unsupported = tmp_path / "unsupported.gif"
    Image.new("RGB", (1, 1), "red").save(unsupported, format="GIF")
    multiframe = tmp_path / "animated.png"
    frames = [Image.new("RGB", (1, 1), color) for color in ("red", "blue")]
    frames[0].save(multiframe, format="PNG", save_all=True, append_images=frames[1:])
    report = tmp_path / "report.json"

    result, data = scan_json(report, malformed, unsupported, multiframe)

    assert result.returncode != 0
    assert all(image["processing_status"] == "failed" for image in data["images"])
    assert "malformed" in data["images"][0]["error"]
    assert "unsupported" in data["images"][1]["error"]
    assert "multi-frame" in data["images"][2]["error"]


def test_cli_refuses_output_that_is_an_input_or_symlink(tmp_path):
    image = make_image(tmp_path / "photo.png")
    result = run_cli("--json-output", image, image)
    assert result.returncode != 0
    assert Image.open(image).format == "PNG"

    target = tmp_path / "target.json"
    destination = tmp_path / "symlink.json"
    destination.symlink_to(target)
    result = run_cli("--json-output", destination, image)
    assert result.returncode != 0
    assert not target.exists()


def test_cli_prints_results_when_json_destination_cannot_be_written(tmp_path):
    image = make_image(tmp_path / "photo.png")

    result = run_cli("--json-output", tmp_path / "missing" / "report.json", image)

    assert result.returncode != 0
    assert "Verdict: inconclusive" in result.stdout
    assert "Unable to write JSON report" in result.stderr


def test_cli_leaves_input_bytes_unchanged(tmp_path):
    image = make_image(tmp_path / "photo.png")
    original = image.read_bytes()

    result = run_cli(image)

    assert result.returncode == 0
    assert image.read_bytes() == original


def test_cli_escapes_control_characters_in_terminal_paths(tmp_path):
    image = make_image(tmp_path / "line\nbreak.png")

    result = run_cli(image)

    assert result.returncode == 0
    assert 'Image: "' in result.stdout
    assert "\\nbreak.png" in result.stdout
