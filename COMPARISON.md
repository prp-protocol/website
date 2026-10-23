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

- Revision 5.73, English schema-v1, 2026-10-23; authority REPORT 68adefcaadf6682d.
- Editorial delivery commit (local source attribution): `8aeddf1aac1143a5f4f49be497c17e7b0f39cdd9`.
- Approved JSON SHA256: `4a5a7d3b9a26367ecc037c28d0147c839e6e3e2e3ce7717ae3b7e2ea6dbd01d7` (1963227 bytes).
- Sealed editorial receipt SHA256: `22ff62adb5d0e02c2a703b9cb6544194e2c23f759150f8330fd6a3c59fef168a` (16994 bytes).
- Exact baseline 4.72 SHA256: `06894e8efb1bb1157c9ad9a6644465e52a7600834f47b76556d96170bf8493fa`.
- Verified signing fingerprint: `BDF794EB7E1CBDE115BDC13B29F9A1FA8EA34B8A`.

`comparison/data.json` is the sole active verdict source and is retained byte-identically.
The snapshot has 62 criteria, 26 stacks, 1612 cells: 816 Yes, 681 No and 115 Pending.
Research remains in progress; qualifications and unpublished-reference labels
are part of each decision, not optional presentation details.

This snapshot retires exactly C08 and its 26 cells from the active grid.
Six criterion records and 225 surviving cell records change, with 144 verdict
transitions (not all Pending resolutions). No columns, marks or assets change.
All previous URLs remain; C08 is never recycled and K02 is absent.
The importer freezes the exact prior criterion and cell records in
`comparison/archive/C08-4.72.json`, attributed to the verified baseline hash.
This historical data is not an active verdict source. The renderer rebuilds
all 26 original C08 URLs with a prominent archived previous-definition notice
and links to `/comparison/archive/C08.html`, not to a missing active row or a
replacement definition. Archive records remain immutable on routine imports.
Exhaustive retirement, changed IDs and existing-cell transitions are retained in
`scripts/comparison-approved.json`. Mark metadata and all assets are unchanged.
Website presentation, prior cell/profile URLs and historical CCNx SVG remain.
Preserve CPU versus network exhaustion and negotiated receive-window scope.
ALIAS/digest-object witnesses are selected constructions, not registry allocation.
F31 PRP custody covers E2E/multicast channels and authorized consumers, not public
CDN storage; ALIAS knowledge grants no access. Normative custody and the author's
reuse clarification retain separate attribution. No blanket certification follows.
LP/LI G05 No applies only to the selected IPv4 compositions, not universal
libp2p/LISP impossibility. NET/ROM and batman-adv bounds remain source/architecture
inferences, not executed world-scale benchmarks. Evidence dates, licensing scope
and conditional PQ witnesses remain qualified. Pending is not absence proof.
G05 now assesses architectural plausibility under the common infrastructure and
workload assumptions. Historical numerical targets are sizing references, not
jointly certified pass/fail thresholds. The website-owned methodology summary
is aligned with that definition; the sealed JSON remains unchanged. G05-CG/LT
No applies to the selected private-ipn singleton compositions, not a family-wide
DTN/CGR/LTP incapacity; G05-BP remains Pending. Documentary plausibility, bounded
historical interoperability, selected profiles and measured results retain their
distinct qualifications. No runtime, security, postquantum, interoperability or
global-capacity certification is implied. The exact snapshot-bound
`--retirement-r573` option is required; ordinary import still rejects grid changes.
E05-BA Yes is dated Freifunk Stuttgart evidence, not certification of Linux 6.12
or all optional settings. E05-NS remains Pending because the located extension
is excluded. G02 PRP uses prepared paths; F32 No concerns the selected planning
composition; C06 remains Pending. Publication does not accept HS2 or ROUTE-001.

`comparison/groups.json` contains the four label/first-criterion pairs from the
signed receipt. Website-owned full-width rowgroup bands use a nested sticky
label, bounded by the scroll container width, without JavaScript or copied
verdicts. Print disables clipping and sticky positioning; wide-table PDF checks
do not certify readable A4 output. Actual Chromium viewport widths of 390 and
1440 pixels are tested at horizontal start/middle/end, not physical devices.

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
   `--asset-r321` similarly pins the exact 2.69/3.21 hashes and CCNx JPEG bytes,
   permits only that active logo/credit substitution and no grid change. Verify
   all three sealed signatures/custody before using `--asset-objects` with it.
   `--expansion-r390` admits only the exact 3.21/3.90 hashes, LI/IL and their
   106 cells, with no new assets or mark changes. Unapproved expansions remain
   rejected by the ordinary path. Grid checks and receipt travel with rollback.
   `--expansion-r472` admits only the exact 4.39/4.72 hashes and F26–F35 with
   their 260 cells, no removed IDs, new columns or changed marks/assets. It is
   mutually exclusive with historical exceptions. Wrong baseline/output hashes,
   extra additions, removals and the ordinary path remain rejected.
   `--retirement-r573` admits only exact 4.72/5.73 digests and removal of C08
   with its 26 cells. It creates historical records from the verified baseline,
   never from a private editorial export, and regenerates the old URLs with
   archival notices. Other deletion, renumbering, addition, wrong snapshots and
   mixed exceptions remain rejected. Routine imports cannot recycle C08.
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
