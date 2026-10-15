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

- Revision 1.92, English, 2026-10-15; authority REPORT 056c6c851af67984.
- Editorial contract commit: `5942bc983ed24b3200b88fbf75a98206c4c639f1`.
- Package SHA256: `999bd441a83a402154472e9cf01dc2b31cc836e0ad8cd5b7871f7a100195800c` (754614 bytes).
- Original manifest SHA256: `08d9c6d045d73db376010a563331d643cd06af1f5a7a819da3fcaadfcdbcfc0a`.
- Approved data SHA256: `4e929778ac52927f2dcbe506f83ea36c1887757cb17407d2dfbd300306619b03`.
- Verified signing fingerprint: `BDF794EB7E1CBDE115BDC13B29F9A1FA8EA34B8A`.

`comparison/data.json` is the sole verdict source and is retained byte-identically.
The snapshot has 38 criteria, 21 stacks, 798 cells and 72 Pending decisions.
Research remains in progress; qualifications and unpublished-reference labels
are part of each decision, not optional presentation details.

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

Website adaptations are limited to the shared header, scoped mark styling, a
main landmark and a focus outline on the scroll region. Regeneration preserves
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
