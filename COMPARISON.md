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

- Revision 5.82, English schema-v1, 2026-10-23; authority REPORT c91218583b467e9a.
- Editorial delivery commit (local source attribution): `dc28b3bd0cffc5649aaa97899a632dcb870bea40`.
- Approved JSON SHA256: `6a76759a09ed96de5ea6d11e003781e38746e42ab60fdb62fb5e93d154c12df9` (1869931 bytes).
- Sealed editorial receipt SHA256: `525d59596fca01b59718e4ee746ec41e8a9b9f04fd1fbadc854f3def1782d3d7` (3163 bytes).
- Exact baseline 5.73 SHA256: `4a5a7d3b9a26367ecc037c28d0147c839e6e3e2e3ce7717ae3b7e2ea6dbd01d7`.
- Verified signing fingerprint: `BDF794EB7E1CBDE115BDC13B29F9A1FA8EA34B8A`.

`comparison/data.json` is the sole active verdict source and is retained byte-identically.
The snapshot has 60 criteria, 26 stacks, 1560 cells: 778 Yes, 680 No and 102 Pending.
Research remains in progress; qualifications and unpublished-reference labels
are part of each decision, not optional presentation details.

This snapshot retires exactly F25/F35 and their 52 cells from the active grid.
Seven surviving cell records and two profiles change; no surviving criteria,
IDs, marks or logos are added/changed. C06-PN/PI and E05-I2/NS move Pending→Yes,
C06-NS Pending→No, and F32-PN/PI No→Yes. All qualifications remain unchanged
from the sealed snapshot, including successor-specific C06 scope and the
author-declared F32 negotiated capacities/QoS to rendezvous.
All previous URLs remain; C08/F25/F35 are never recycled and K02 is absent.
The importer freezes exact prior criterion/cell records in
`comparison/archive/F25-5.73.json` and `F35-5.73.json`, attributed to the verified
baseline hash. Existing `C08-4.72.json` is unchanged. These historical records
are not active verdict sources. The renderer rebuilds all 78 old cell URLs with
prominent archived previous-definition notices and matching criterion archive
links, never redirects to a new definition. Routine imports preserve records.
Exhaustive retirement, changed IDs and existing-cell transitions are retained in
`scripts/comparison-approved.json`. Matrix mark metadata and logos are unchanged.
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
`--retirement-r582` option is required; ordinary import still rejects grid changes.
E05-BA Yes is dated Freifunk Stuttgart evidence, not certification of Linux 6.12
or all optional settings. G02 PRP uses prepared paths. The new documentary
judgments do not accept HS2, REFERENCE or ROUTE-001 integration/security gates.

## Auxiliary inventories and Protocol Atlas

`comparison/wake-traffic.json` remains exact (66701 bytes, SHA256
`1860d68f3680c20b6df256eb5c90457edfe3512838ae4295ba68330d0a151f23`).
Website-owned `comparison/wake.py` renders the static summary and complete
inventory/conditions/source text. There are 26 historical accounts, 19 conditional
totals and seven incomplete accounts. No sorting/ranking across unlike scopes;
the former cutoff is retired, not a current measurement or universal budget.
Research labels link only to public archived F25 cells, never private files.
Matrix and archived F25 pages link to this auxiliary page.

`protocol-atlas/` contains only the approved English v2 poster, public metadata
and website wrapper. Seven signed input objects, exact sizes/hashes, including
poster SVG/PNG/PDF and metadata, are recorded in the approved receipt and the
`comparison-582` publication evidence. `scripts/render-atlas.py` verifies poster
hashes and regenerates the wrapper from exact `poster-content.json`, retaining
description, alt, credits, technical limits and source snapshot date verbatim.
SVG safety was checked before import; never silently sanitize signed bytes.
Responsive preview, full-size SVG/PNG links and exact downloads are available
under a shared Protocol Atlas navigation entry. No editorial renderer, private
research, sources.json or scripts are imported. RRL/AOP, successor sequence and
historical-wire distinctions remain as approved; no security acceptance follows.

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
python3 scripts/render-atlas.py
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
   `--retirement-r582` admits only the exact 5.73/5.82 digests and removal of
   F25/F35 plus 52 cells. Historical records are generated from the pinned local
   baseline. Prior C08 records stay intact; routine imports reject recycling of
   all three retired IDs. No generic deletion or retirement switch is provided.
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
