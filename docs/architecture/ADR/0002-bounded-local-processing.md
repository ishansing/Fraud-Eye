# ADR 0002: Bounded local processing

- **Status:** Accepted
- **Date:** 2026-11-24

## Context

The CLI processes attacker-controlled image bytes and metadata, while reports can contain sensitive metadata. Parsing and inference must remain local, bounded, reproducible, and isolated per image.

## Decision

Process images sequentially. Read each input through one bounded per-image processing path, compute its original-byte digest before analysis, and apply byte, decoded-pixel, metadata, and wall-clock limits before expensive work. Keep image decoding and orchestration in the Python process; evaluate Pillow with decoder safeguards retained and explicitly restrict accepted formats and frame count.

Evaluate ExifTool as a metadata subprocess using fixed arguments, no shell interpolation, a bounded timeout and captured output, and explicit parser/version/error reporting. Run integration tests with outbound networking denied. Treat this process separation as fault containment, not a security sandbox.

Output writes use a same-directory temporary file and atomic replacement, and reject symlink destinations and destinations resolving to any input. Terminal output remains concise and excludes full sensitive metadata; local JSON includes all parseable metadata as specified.

## Consequences

- Sequential per-image processing avoids retaining a batch of decoded images at once.
- Exact memory/time budgets and packaging requirements remain open pending feasibility tests.
- C2PA SDK integration and network-denial behavior require a prototype/test before selection.
- The output path implementation must defend against symlink and input-overwrite races, not only perform a string comparison.

## Evidence

- `SPEC.md` REQ-3–REQ-9 and REQ-18–REQ-19 define processing, privacy, and output safety.
- `docs/product/research.md` §§Bounded JPEG/PNG decode, Broad metadata, and Network-free execution identify candidate libraries and evidence gaps.
