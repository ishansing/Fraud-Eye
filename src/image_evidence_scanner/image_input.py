import hashlib
import io
import os
import stat
import warnings
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image, ImageStat, JpegImagePlugin, UnidentifiedImageError

MAX_FILE_BYTES = 100 * 1024 * 1024
MAX_PIXELS = 50_000_000
MAX_PNG_CHUNKS = 100_000


def inspect_image(input_path: str) -> tuple[dict, bytes | None]:
    result = {
        "input_path": input_path,
        "processing_status": "failed",
        "sha256": None,
        "sha256_status": "not_computed",
        "detected_format": None,
        "file_size": None,
        "image_facts": None,
        "verdict": "inconclusive",
        "error": None,
    }

    if urlparse(input_path).scheme:
        result["error"] = "URLs are not supported; provide a local file path"
        return result, None

    path = Path(input_path)
    if path.is_dir():
        result["error"] = "directories are not supported; provide image file paths"
        return result, None
    try:
        descriptor = os.open(input_path, os.O_RDONLY | getattr(os, "O_NONBLOCK", 0))
        with os.fdopen(descriptor, "rb") as source:
            file_stat = os.fstat(source.fileno())
            if not stat.S_ISREG(file_stat.st_mode):
                result["error"] = "input is not a regular image file"
                return result, None
            result["file_size"] = file_stat.st_size
            if file_stat.st_size > MAX_FILE_BYTES:
                result["error"] = "input exceeds the 100 MiB file-size limit"
                result["sha256_error"] = "not computed because the input exceeds the read limit"
                return result, None
            image_bytes = source.read(MAX_FILE_BYTES + 1)
    except OSError:
        result["error"] = "unable to read input file"
        return result, None

    if len(image_bytes) > MAX_FILE_BYTES:
        result["error"] = "input exceeds the 100 MiB file-size limit"
        result["sha256_error"] = "not computed because the input exceeds the read limit"
        return result, None

    result["file_size"] = len(image_bytes)
    result["sha256"] = hashlib.sha256(image_bytes).hexdigest()
    result["sha256_status"] = "computed"

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(io.BytesIO(image_bytes)) as image:
                result["detected_format"] = image.format
                if image.format not in {"JPEG", "PNG"}:
                    result["error"] = "unsupported format; only JPEG and PNG are supported"
                    return result, image_bytes
                frame_count = getattr(image, "n_frames", 1)
                if frame_count != 1:
                    result["error"] = "multi-frame images are not supported"
                    return result, image_bytes
                width, height = image.size
                if width * height > MAX_PIXELS:
                    result["error"] = "image exceeds the 50,000,000 decoded-pixel limit"
                    return result, image_bytes
                image.load()
                result["image_facts"] = {
                    "width": width,
                    "height": height,
                    "aspect_ratio": width / height,
                    "mode": image.mode,
                    "bit_depth_per_channel": _bit_depth_per_channel(image),
                    "frame_count": frame_count,
                }
                result["pixel_signals"] = _pixel_signals(image)
                result["file_structure"] = _file_structure(image, image_bytes)
    except (Image.DecompressionBombError, Image.DecompressionBombWarning):
        result["error"] = "image exceeds the decoder pixel-safety limit"
        return result, image_bytes
    except (UnidentifiedImageError, OSError, SyntaxError, ValueError):
        result["error"] = "image is malformed or could not be decoded"
        return result, image_bytes

    result["processing_status"] = "processed"
    return result, image_bytes


def _pixel_signals(image: Image.Image) -> dict:
    bands = image.getbands()
    statistics = ImageStat.Stat(image)
    histogram = image.histogram()
    bins_per_band = len(histogram) // len(bands)
    channels = []
    for index, band in enumerate(bands):
        start = index * bins_per_band
        channels.append(
            {
                "channel": band,
                "minimum": statistics.extrema[index][0],
                "maximum": statistics.extrema[index][1],
                "mean": statistics.mean[index],
                "standard_deviation": statistics.stddev[index],
                "histogram": histogram[start : start + bins_per_band],
            }
        )

    jpeg = None
    if image.format == "JPEG":
        sampling = JpegImagePlugin.get_sampling(image)
        jpeg = {
            "quantization_tables": {
                str(index): table for index, table in sorted((image.quantization or {}).items())
            },
            "subsampling": {0: "4:4:4", 1: "4:2:2", 2: "4:2:0"}.get(sampling, "unknown"),
        }

    return {
        "method": "Pillow channel histograms and population statistics",
        "channels": channels,
        "jpeg": jpeg,
        "limitations": ["Global image statistics do not localize edits or prove image origin."],
    }


def _bit_depth_per_channel(image: Image.Image) -> int | None:
    for key in ("bitdepth", "bits"):
        value = image.info.get(key)
        if isinstance(value, int):
            return value
    if image.mode.startswith("I;16"):
        return 16
    return {
        "1": 1,
        "L": 8,
        "P": 8,
        "RGB": 8,
        "RGBA": 8,
        "LA": 8,
        "CMYK": 8,
        "I": 32,
        "F": 32,
    }.get(image.mode)


def _file_structure(image: Image.Image, image_bytes: bytes) -> dict:
    if image.format == "JPEG":
        sampling = JpegImagePlugin.get_sampling(image)
        return {
            "container": "JPEG",
            "quantization_table_count": len(image.quantization or {}),
            "chroma_subsampling": {0: "4:4:4", 1: "4:2:2", 2: "4:2:0"}.get(sampling, "unknown"),
        }

    known_chunks = {
        "IHDR",
        "PLTE",
        "IDAT",
        "IEND",
        "tRNS",
        "iCCP",
        "sRGB",
        "gAMA",
        "cHRM",
        "eXIf",
        "tEXt",
        "zTXt",
        "iTXt",
    }
    chunk_types = {}
    other_chunk_count = 0
    chunk_count = 0
    offset = 8
    truncated = False
    while offset + 12 <= len(image_bytes) and chunk_count < MAX_PNG_CHUNKS:
        chunk_length = int.from_bytes(image_bytes[offset : offset + 4], "big")
        end = offset + 12 + chunk_length
        if end > len(image_bytes):
            truncated = True
            break
        chunk_type = image_bytes[offset + 4 : offset + 8].decode("ascii", "replace")
        chunk_count += 1
        if chunk_type in known_chunks:
            chunk_types[chunk_type] = chunk_types.get(chunk_type, 0) + 1
        else:
            other_chunk_count += 1
        offset = end
        if chunk_type == "IEND":
            break
    else:
        truncated = offset < len(image_bytes)

    return {
        "container": "PNG",
        "chunk_count": chunk_count,
        "chunk_types": chunk_types,
        "other_chunk_count": other_chunk_count,
        "truncated": truncated,
    }
