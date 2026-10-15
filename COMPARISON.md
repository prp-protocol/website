# Approved comparison publication

Public route: `/comparison/`. Stable evidence URLs use criterion and stack IDs,
for example `/comparison/cells/F01-PN.html`, never review-round numbers.
Selected stack descriptions have their own stable pages, for example
`/comparison/stacks/PN.html`, reached through the circled information icon beside
each project title (accessible name: “Selected stack: [project]”). Its touch area
is at least 44 × 44 px. Mobile headers use smaller logos and a narrower sticky
criterion column. Project titles retain their official external links. Legacy
`#profile-ID` anchors point to those links; full profiles are not repeated below
the matrix. Profiles are generated unchanged from the same approved JSON.

## Current approved source

- Revision 2.69, English schema-v1, 2026-10-15; authority REPORT 3436707b2335a963.
- Editorial delivery commit: `4b98e32128c12ae84c10d4742a5bb7e60f9ffa93`.
- Approved JSON SHA256: `67d189343b908c17b055952f9d7a13d15e71e19fbee4ef521c0aade520373e51` (1312317 bytes).
- Sealed editorial receipt SHA256: `77706c68f6d74860a5a950a2b1d9ed8428df319562e499a3fc3d0105a8d53278` (11343 bytes).
- Exact baseline 2.14 SHA256: `7c5876e4b797d4094dd9198facca00047e5d36f0bd37976d413679e70c164835`.
- Verified signing fingerprint: `BDF794EB7E1CBDE115BDC13B29F9A1FA8EA34B8A`.

`comparison/data.json` is the sole verdict source and is retained byte-identically.
The snapshot has 53 criteria, 24 stacks, 1272 cells: 617 Yes, 370 No and 285 Pending.
Research remains in progress; qualifications and unpublished-reference labels
are part of each decision, not optional presentation details.

This coordinated expansion adds F24, F25, S04 and D04, and columns RI (IPv6
IoT/RPL), HP (HIPv2/ESP), CX (CCNx 1.0): 243 new cells. K02 is absent; no old
IDs are retired or renumbered. The receipt lists 5 changed criterion records,
5 changed column records and 295 changed cells including additions. Exhaustive
IDs and new asset credits are in `scripts/comparison-approved.json`.
G04-HP/G04-CX Yes concerns distributed work without a mandatory single
coordinator, not proven global capacity. F23-CX remains Pending, including the
unresolved consumer retry/attachment mechanism. Increased Pending includes new
rows/columns, not 83 regressions. No runtime/security/interoperability/global-scale
certification is implied. Website presentation and all old logos are retained.
Only approved JSON and three explicitly coordinated neutral SVG labels are
imported; historical sealed packages remain unchanged.

New independently signed assets (exact bytes, safe static typography):

- `logos/hipv2.svg`, 328 bytes: `d836317b845bf765811c594420841ae5c1d4e480bc20c5d07b2774917e66174e`.
- `logos/ccnx.svg`, 327 bytes: `b6fe33cda3f2bf2162015577d7a97d7b77d2940b7d2d9c6a5373e8f0c8b3c644`.
- `logos/iot-rpl.svg`, 330 bytes: `fff20dd148fd75e85bddfe45c8766dadc94afa56040ed4c7dac5ef2837548bae`.

## Rebuild and validate

```sh
python3 scripts/sync-navigation.py
python3 comparison/render.py --out comparison
python3 scripts/sync-navigation.py --check
python3 scripts/check-comparison.py
```

The renderer uses only Python's standard library. Its data, logos, navigation
template and navigation stylesheet are all within `comparison/`; the comparison
can be copied elsewhere and rebuilt with the same command without this repository
or editorial modules. The first command above is only needed to propagate a site
menu/style change into the local template. Render again after changing that template.
Generated HTML is committed because hosting is static and build-free.

Website adaptations cover the shared header, scoped mark styling, a main
landmark, scroll focus outline, compact mobile headers, accessible information
icons and separate stack profile pages. Regeneration preserves
them. The deployed `comparison/manifest.json` records all adapted file hashes;
it is distinct from the original editorial manifest above. Do not edit generated
HTML or `data.json` to change decisions. No runtime JavaScript is needed.

## Approved updates

Workflow adopted under REPORT 39b2c21af7898ea3 on 2026-10-15. The editorial
contract is `pesquisa/prp-estado-da-arte-v1/PUBLICATION.md` in the read-only
editorial repository. This adoption does not publish any new research revision.

Editorial owns criteria titles, definitions, methods and research actions;
column labels, profiles and official links; verdicts, rationales, sources,
qualifications and existing mark-reference/credit metadata. Website owns the
renderer, validation, navigation, HTML/CSS and logo binaries. All labels come
from JSON. Criterion labels currently appear in matrix rows/definitions; cell
pages identify criteria by stable IDs, not copied titles. Profiles use column
labels. Renaming F13 must not change F13, F13-PN, anchors or URLs. Substantive
criteria changes require affected-decision review; genuinely new criteria need
new stable IDs. Never recycle or renumber identifiers.

1. Receive ONE explicitly approved, sealed schema-v1 `data.json` via editorial →
   orchestrator → website, plus detached signature and coordination receipt:
   revision/date, bytes/SHA256, all status counts and changed criterion, column
   and cell IDs (empty arrays explicitly mean unchanged). Recover equivalent work.
   Editorial's `--data-only` export has full-export JSON byte parity; do not rerun
   or synchronize private editorial sources here.
2. Independently verify catalog custody, digest, size and expected signer. Save
   that evidence and its reference in the receipt. The importer requires detached
   GPG verification against `BDF794EB7E1CBDE115BDC13B29F9A1FA8EA34B8A`, checks
   exact bytes, schema, unique/stable IDs, complete grid, statuses, safe source
   URLs, private-path exclusion and existing logo references/hashes. Catalog
   evidence is a separately checked prerequisite, not inferred from a filename
   or the receipt's prose. Cryptographic validity does not establish external
   web-of-trust identity.
3. Routine import NEVER imports HTML/CSS/renderers or logo binaries. Full exports
   are review/initial-provisioning artifacts only. New schema, new/retired IDs or
   new/changed binary assets require a separately identified coordination; the
   routine importer rejects them. Preserve old sealed packages and Git history.
   Snapshot-specific exceptions `--expansion-r214` and `--expansion-r269` are
   pinned to their exact source/baseline digests, additions and no removals.
   For 2.69, `--asset-objects` supplies only the three exact hashes above, after
   all five catalog objects/signatures and SVG safety have been independently
   verified. Assets are staged with JSON before regeneration; existing assets
   cannot be overwritten. Neither exception enables arbitrary later expansion.
4. Stage the exact JSON with website-owned files, regenerate twice and verify
   deterministic output and ownership before applying. Update this source receipt
   with the approved delivery; `--apply` records its machine-readable receipt in
   `scripts/comparison-approved.json`. Run all checks below. Check desktop/mobile
   scrolling, keyboard access, collapsed definitions, representative evidence,
   external title links, local logos and credits in a browser.
5. Commit the complete snapshot once and publish through the managed website
   publisher. Internal synchronization is independent under the owner's current
   policy. No direct push, unattended private-draft sync, private review pages,
   lab outputs or research index publication is authorized.
6. Verify successful Pages deployment, downloaded data/manifest and generated
   file hashes, HTTP/MIME and public browser behavior. Return the exact commit,
   deployment receipt/time, changed IDs and evidence to the orchestrator.

Example receipt (values must come from the authorized handoff, not this example):

```json
{
  "authority": "REPORT <approved update>",
  "catalog_receipt": "<path/reference to independently checked broker evidence>",
  "revision": "<approved revision>", "date": "YYYY-MM-DD",
  "bytes": 0, "sha256": "<sealed JSON digest>",
  "status_counts": {"Y": 0, "N": 0, "?": 0},
  "changed_ids": {"criteria": [], "columns": [], "cells": []}
}
```

```sh
# Dry-run verifies signature, receipt, schema and two temporary rebuilds.
python3 scripts/import-comparison.py /sealed/object --signature /sealed/signature.asc --receipt /working/approved-receipt.json
# Only after review; repository writes, NOT deployment:
python3 scripts/import-comparison.py /sealed/object --signature /sealed/signature.asc --receipt /working/approved-receipt.json --apply
python3 scripts/test-comparison-import.py
python3 scripts/check-comparison.py
python3 scripts/sync-navigation.py --check
git diff --check
```

Use `--gnupghome` only for an explicitly provisioned public verification key
store; do not hunt credentials or import an unverified replacement signer.
The historical 1.97 receipt predates JSON-only delivery and identifies its verified
package; 2.14 is a separately signed JSON and receipt delivery. Temporary
rename/escaping and invalid-input fixtures never enter production content.
Imports stage coherent files locally; only a reviewed Git commit and the
managed publisher provide atomic public delivery. Roll back any interrupted
local import before committing; never publish a partially prepared worktree.

## Rollback

Identify the last approved, publicly verified commit. Create a new forward commit
restoring that complete comparison snapshot, approved receipt, matching grid
checks and navigation integration;
do not reset or force-push history. Repeat rebuild, validation and managed deploy,
then verify public bytes and report the rollback. Do not mix old data with new
cell pages. Prior snapshots remain recoverable through Git history.
