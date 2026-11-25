import json
import shutil
import subprocess
import threading

MAX_METADATA_BYTES = 16 * 1024 * 1024
MAX_METADATA_NESTING = 64
PARSER_TIMEOUT_SECONDS = 5


def extract_metadata(image_bytes: bytes) -> dict:
    executable = shutil.which("exiftool")
    coverage = {
        "name": "ExifTool",
        "version": None,
        "status": "unavailable",
        "groups": [],
        "errors": [],
        "unknown_tags_requested": True,
        "limitations": ["Unrecognized binary blocks may remain opaque to the parser."],
    }
    if executable is None:
        coverage["errors"].append("ExifTool is not installed or not on PATH")
        return {"status": "unavailable", "metadata": {}, "coverage": coverage}

    try:
        return_code, output = _run_exiftool(executable, image_bytes)
    except subprocess.TimeoutExpired:
        coverage["status"] = "error"
        coverage["errors"].append("ExifTool timed out")
        return {"status": "error", "metadata": {}, "coverage": coverage}
    except OSError:
        coverage["status"] = "error"
        coverage["errors"].append("ExifTool could not be started")
        return {"status": "error", "metadata": {}, "coverage": coverage}

    if output is None:
        coverage["status"] = "error"
        coverage["errors"].append("ExifTool output exceeded the 16 MiB metadata limit")
        return {"status": "error", "metadata": {}, "coverage": coverage}
    if return_code != 0:
        coverage["status"] = "error"
        coverage["errors"].append("ExifTool reported an extraction failure")
        return {"status": "error", "metadata": {}, "coverage": coverage}

    if _exceeds_json_nesting(output):
        coverage["status"] = "error"
        coverage["errors"].append(
            f"ExifTool JSON exceeded the {MAX_METADATA_NESTING}-level nesting limit"
        )
        return {"status": "error", "metadata": {}, "coverage": coverage}

    try:
        parsed = json.loads(output)
        if not isinstance(parsed, list) or len(parsed) != 1 or not isinstance(parsed[0], dict):
            raise ValueError("unexpected JSON shape")
    except (json.JSONDecodeError, ValueError):
        coverage["status"] = "error"
        coverage["errors"].append("ExifTool returned invalid JSON")
        return {"status": "error", "metadata": {}, "coverage": coverage}

    metadata = {key: value for key, value in parsed[0].items() if key != "SourceFile"}
    coverage["version"] = str(metadata.get("ExifTool:ExifToolVersion", "unknown"))
    coverage["groups"] = sorted({key.split(":", 1)[0] for key in metadata if ":" in key})
    coverage["status"] = "complete"
    return {"status": "complete", "metadata": metadata, "coverage": coverage}


def _exceeds_json_nesting(output: bytes) -> bool:
    depth = 0
    in_string = False
    escaped = False
    for byte in output:
        if in_string:
            if escaped:
                escaped = False
            elif byte == ord("\\"):
                escaped = True
            elif byte == ord('"'):
                in_string = False
        elif byte == ord('"'):
            in_string = True
        elif byte in (ord("["), ord("{")):
            depth += 1
            if depth > MAX_METADATA_NESTING:
                return True
        elif byte in (ord("]"), ord("}")):
            depth -= 1
    return False


def _run_exiftool(executable: str, image_bytes: bytes) -> tuple[int, bytes | None]:
    process = subprocess.Popen(
        [executable, "-json", "-G1", "-a", "-u", "-U", "--", "-"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    output = bytearray()
    overflow = threading.Event()

    def read_output() -> None:
        while chunk := process.stdout.read(64 * 1024):
            if len(output) + len(chunk) > MAX_METADATA_BYTES:
                overflow.set()
                process.kill()
                return
            output.extend(chunk)

    def write_input() -> None:
        try:
            process.stdin.write(image_bytes)
            process.stdin.close()
        except OSError:
            pass

    reader = threading.Thread(target=read_output)
    writer = threading.Thread(target=write_input)
    reader.start()
    writer.start()
    try:
        process.wait(timeout=PARSER_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
        raise
    finally:
        reader.join()
        writer.join()
        process.stdout.close()
        process.stdin.close()

    return process.returncode, None if overflow.is_set() else bytes(output)
