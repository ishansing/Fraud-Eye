# Implementation review

**Range:** `a22a883...619b084`  
**Verdict:** Changes requested  
**Scope:** ISSUE-001 through ISSUE-005 implementation checkpoint. ISSUE-006 is outside this
range and remains gated on model, dataset, licensing, and hardware decisions.

## Standards

No findings. The changes follow documented project rules; Ruff-enforced issues are excluded.

## Spec and acceptance coverage

### Findings

1. **[Medium] Image structure and color-space signals are incomplete.** `SPEC.md` REQ-9 and
   ISSUE-004 require mode/color space and relevant file structure. `image_input.py:79–87`
   reports mode but no color space; `image_input.py:99–132` reports global statistics and
   JPEG tables/subsampling, but no general file-structure indicators (including PNG chunk
   structure).

2. **[Medium] Nested metadata bounds are not explicit.** `SPEC.md` REQ-4 and ISSUE-003 require
   a stable bound on metadata nesting/structure. `metadata.py:45–52` passes parser output
   directly to `json.loads`; the byte/time limits exist, but no configured depth limit or
   nesting-bound test documents the effective limit. The caller isolates parse failures.

3. **[Medium] The C2PA output cap is applied after output materialization.** In
   `c2pa_worker.py:18–30`, `Reader.json()` creates the complete manifest JSON string before
   its 8 MiB check. A large embedded manifest can therefore consume memory beyond the stated
   output cap before the worker returns an error. The 10-second parent timeout limits time,
   not peak memory.

4. **[Medium] Offline CI coverage does not cover all network paths.** `.github/workflows/ci.yml:24–27`
   blocks and counts IPv4 `iptables` OUTPUT traffic only; there is no IPv6 rule. The current
   C2PA integration fixture checks an image with no manifest, so it does not exercise an
   active-manifest validation path under denied networking. This falls short of ISSUE-003’s
   network-denial merge gate on environments where IPv6 egress is available.

5. **[Low] User documentation omits general verdict/advisory meanings.** ISSUE-005’s documentation
   impact calls for verdict categories, score semantics, and advisory meanings. `README.md:51–53`
   explains the current unconfigured/inconclusive case but does not explain the meanings and
   scope of the other contract values.

### Coverage notes

- Generation and editing tasks are separate and explicitly unconfigured; no unsupported model
  verdict is emitted.
- Metadata sensitivity and offline revocation limitations are documented.
- The offline adversarial review found no demonstrated compromise path for hostile local
  images. Its coverage did not include native-library fuzzing or OS-level observation of
  C2PA network behavior.
- The CI workflow’s IPv4 packet counter is intended to catch denied IPv4 attempts; the
  uncovered issue is IPv6 and the lack of an active-manifest fixture.

## Recommended next

Return to implementation for findings 1–4. Finding 5 can be addressed with concise README
definitions. Then rerun affected tests and return for review.
