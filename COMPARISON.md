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

- Revision 1.97, English, 2026-10-15; authority REPORT e146065a177b6923.
- Editorial delivery commit: `c6d2f21ad6947189099c8312f4e9557ab01d8689`.
- Package SHA256: `e53a0204b791b6010baca2fa8fc21d48d407e5cb78b1acd5695a321cc9ff47a5` (749182 bytes).
- Original manifest SHA256: `e3ed4df85c7256843a41575c17ddbeb6f9c2ce729117a5d319da3230fdb83bc9`.
- Approved data SHA256: `0a53746ef35fb705de23a2e5acde20c3ecbfeb37baf565e15408b9febaa6436a` (777710 bytes).
- Verified signing fingerprint: `BDF794EB7E1CBDE115BDC13B29F9A1FA8EA34B8A`.

`comparison/data.json` is the sole verdict source and is retained byte-identically.
The snapshot has 38 criteria, 21 stacks, 798 cells and 62 Pending decisions.
Research remains in progress; qualifications and unpublished-reference labels
are part of each decision, not optional presentation details.

Revision 1.97 changes 31 records from 1.92: F04-LT; F05-PN; F05-PI; F05-BP;
F05-LP; F05-TO; F05-I2; F05-YG; F05-CJ; F05-SC; F05-RT; F05-MT; F05-GN;
F05-BL; F09-CG; F09-LT; F10-CG; F10-LT; F13-IP; F13-NS; F13-MT; F21-CG;
F21-LT; C01-CG; C01-LT; S02-LT; S03-LT; G02-CG; G02-LT; G04-CG; G04-LT.
Exactly ten verdicts change Pending → Yes: F04-LT, F10-CG, F10-LT, F21-CG,
F21-LT, C01-CG, C01-LT, S02-LT, G02-CG, G02-LT. F05/F13 wording and CG/LT
profiles follow the approved snapshot; documentary evidence does not imply
full-stack runtime certification. Upstream renderer is byte-identical to the
1.92 export, so the reviewed website presentation adaptations remain unchanged.

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
The baseline receipt predates JSON-only delivery and identifies the verified
historical package; it is not a fabricated standalone JSON seal. Temporary
rename/escaping and invalid-input fixtures never enter production content.
Imports stage coherent files locally; only a reviewed Git commit and the
managed publisher provide atomic public delivery. Roll back any interrupted
local import before committing; never publish a partially prepared worktree.

## Rollback

Identify the last approved, publicly verified commit. Create a new forward commit
restoring that complete comparison snapshot and matching navigation integration;
do not reset or force-push history. Repeat rebuild, validation and managed deploy,
then verify public bytes and report the rollback. Do not mix old data with new
cell pages. Prior snapshots remain recoverable through Git history.
