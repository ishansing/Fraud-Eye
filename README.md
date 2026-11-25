# Image Evidence Scanner

Offline-first local CLI for examining evidence about possible AI-generated and AI-edited images.
The scanner processes one to five explicit local JPEG or PNG files. It reports file identity,
basic image facts, global pixel signals, metadata coverage, and offline C2PA status. Advanced
forensic signals and model-backed assessment are not implemented yet.

## Development

Use Python 3.11 or newer:

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
python -m image_evidence_scanner --help
python -m pytest -q
ruff check .
ruff format --check .
```

ExifTool must also be installed separately and available as `exiftool` on `PATH` for metadata
extraction. Use the [official installation instructions](https://exiftool.org/install.html);
the scanner does not download it at scan time. If it is missing, image facts are still reported,
but the run is marked partial and returns nonzero.

## Current CLI

Show help:

```sh
python -m image_evidence_scanner --help
```

Scan files and optionally write a JSON report:

```sh
python -m image_evidence_scanner photo.jpg screenshot.png
python -m image_evidence_scanner --json-output report.json photo.jpg
```

Scans accept one to five explicit files, reject directories and URLs, and currently support
single-frame JPEG and PNG. Files over 100 MiB and images over 50,000,000 decoded pixels are
rejected. Each result includes the original-byte SHA-256 when bytes are read, basic image facts,
available ExifTool metadata, and an `inconclusive` verdict until validated model profiles are
implemented. Global channel histograms/statistics and JPEG quantization/subsampling are
measurements, not proof of origin or localized editing. Files rejected before being read
(including oversized files) have no digest; the
JSON report states why the digest was not computed.

Generation and editing assessments are separate. Until a validated local model/profile is
selected and passes the release gates, both task results and the overall verdict remain
`inconclusive`; no score or “no configured signal” advisory is emitted.

JSON output is local and includes parseable metadata by default. Metadata may contain sensitive
GPS, device, creator, or prompt values. Treat report paths as private. Terminal output avoids
printing full metadata values. C2PA validation disables remote-manifest and OCSP fetching;
fresh online revocation status is not checked.
