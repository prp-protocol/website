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

1. Receive a coherent, explicitly approved editorial snapshot via editorial →
   orchestrator → website, with revision/date, package and manifest hashes,
   signature, and changed cell IDs (or an explicit no-decision-change statement).
2. Recover equivalent delivery first. Verify catalog custody, signer, exact bytes,
   safe regular archive paths and every individual manifest hash before importing.
3. Compare IDs and verdict changes with the handoff. Replace the coherent data,
   renderer and assets together; reapply/review the website-only wrapper adaptation.
   Retain the source JSON byte-for-byte. Remove obsolete generated outputs only
   when explicitly identified by the new snapshot; preserve stable IDs/history.
4. Update this source receipt, rerender and validate. Update expected counts in
   the checker only when the approved snapshot changes them. Check desktop/mobile
   scrolling, keyboard access, collapsed definitions, representative evidence,
   external title links, local logos and credits in a browser.
5. Commit the complete snapshot once and publish through the managed website
   publisher. Internal synchronization is independent under the owner's current
   policy. No direct push, unattended private-draft sync, private review pages,
   lab outputs or research index publication is authorized.
6. Verify successful Pages deployment, downloaded data/manifest and generated
   file hashes, HTTP/MIME and public browser behavior. Return the exact commit,
   deployment receipt/time, changed IDs and evidence to the orchestrator.

## Rollback

Identify the last approved, publicly verified commit. Create a new forward commit
restoring that complete comparison snapshot and matching navigation integration;
do not reset or force-push history. Repeat rebuild, validation and managed deploy,
then verify public bytes and report the rollback. Do not mix old data with new
cell pages. Prior snapshots remain recoverable through Git history.
