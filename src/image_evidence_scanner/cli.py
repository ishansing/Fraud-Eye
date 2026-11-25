import argparse
import sys

from image_evidence_scanner.output import write_json_report
from image_evidence_scanner.report import render_text
from image_evidence_scanner.scan import scan_batch


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="image-evidence-scanner",
        description="Offline-first local assessment of image-origin evidence.",
    )
    parser.add_argument(
        "--json-output",
        metavar="PATH",
        help="write a detailed JSON report to this local path",
    )
    parser.add_argument(
        "images",
        nargs="*",
        metavar="IMAGE",
        help="one to five local JPEG or PNG image paths",
    )
    args = parser.parse_args(argv)
    if not 1 <= len(args.images) <= 5:
        parser.error("provide one to five explicit image paths")

    report = scan_batch(args.images)
    print(render_text(report))

    if args.json_output:
        try:
            write_json_report(args.json_output, report, args.images)
        except (OSError, ValueError, RuntimeError):
            print(
                "Unable to write JSON report; check the destination and permissions.",
                file=sys.stderr,
            )
            return 1

    return int(report["batch_status"] != "complete")
