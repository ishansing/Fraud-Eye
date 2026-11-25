import json
import os
import tempfile
from pathlib import Path


def write_json_report(output_path: str, report: dict, input_paths: list[str]) -> None:
    destination = Path(output_path)
    if destination.is_symlink():
        raise ValueError("JSON destination must not be a symlink")

    resolved_destination = destination.resolve()
    for input_path in input_paths:
        input_file = Path(input_path)
        if resolved_destination == input_file.resolve():
            raise ValueError("JSON destination must not resolve to an input file")
        if (
            destination.exists()
            and input_file.exists()
            and os.path.samefile(destination, input_file)
        ):
            raise ValueError("JSON destination must not be an input file")

    descriptor, temporary_path = tempfile.mkstemp(
        prefix=f".{destination.name}.",
        suffix=".tmp",
        dir=destination.parent,
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as output:
            json.dump(report, output, ensure_ascii=True, indent=2)
            output.write("\n")
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary_path, destination)
    finally:
        if os.path.exists(temporary_path):
            os.unlink(temporary_path)
