# Participant Relationship Protocol website

Static public website for the PRP project. This repository is the canonical
working copy for both the internal Gitea mirror and the public GitHub Pages
site.

The site is intentionally build-free: the files in the repository root are the
files served in production.

The public roadmap summary lives in `index.html`; `ROADMAP.md` is its detailed,
versioned source. Update both in the same commit whenever a milestone changes.

Sponsor logos live in `assets/sponsors/`. Keep organization names as text in
the sponsor cards so recognition does not depend on images and remains
accessible to assistive technologies. Describe ecosystem participants by their
current capabilities rather than by tiers; the participant rail is designed to
accept additional cards as the ecosystem grows.

## Local preview

The introductory Meet PRP player lives on `index.html`. The remaining conceptual
films live in `videos.html`; its old Meet PRP anchor links to the home player.
Technical model, layer diagrams and design principles live in `architecture.html`;
legacy home-page anchors remain linked entry points. Keep roadmap and sponsor
content on the home page, with their existing status and disclaimers.
The technical episode catalog lives in `technical-series.html`: add one numbered
article per episode, with its title, summary, duration and links to its EN/PT
episode pages. Keep technical players on those individual pages so the catalog
can grow without loading every video. Approved MP4 files live under
`assets/videos/`; preserve their bytes and existing episode URLs.
Keep the home page as an entry point to the collection. The legacy technical
anchors in `videos.html` remain as visible links to the technical catalog.
Use `.episode-card` for catalog entries and `.intro-card` for the standalone
introduction: they use normal block flow, not the three-row player subgrid.

Open `index.html` in a browser, or serve the directory with any static server:

```sh
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

## Repository and publication flow

- `origin` is the internal Gitea repository. Commit completed changes to
  `main`; the Agentmux publisher sends those commits to Gitea.
- The public destination is `prp-protocol/website`. Use the granted
  `github-prp-website` managed publisher from a clean `main`, with a verified
  commit-specific bundle and its SHA-256. Check remote state before publishing.
  Do not use the legacy direct-push script or obtain credentials.
- As authorized by the owner on 2026-10-11, public publication does not wait
  for internal Gitea synchronization. Internal synchronization remains managed
  independently; this does not authorize a direct internal push.
- The managed publisher updates GitHub's `main` and `gh-pages` together.
  Verify the Pages deployment and publicly served content separately: a Git
  publication receipt alone is not evidence of public delivery.

Do not edit `gh-pages` directly. Every published GitHub revision must exist as
a regular commit on `main`.

## Access analytics

The production page includes the Cloudflare Web Analytics beacon immediately
before the closing `body` tag in `index.html`. Its token belongs to
`prp-protocol.org` and is intentionally different from the token used by the
[PRP Journal](https://journal.prp-protocol.org/), so the two properties retain
separate access statistics.

## Source material

Content is derived from:

- `../specifications/prp-architecture-v1-rc1.md`
- `../specifications/README.md`

The public publication repository intentionally contains only documents linked
from this site and its roadmap. Editorial drafts, conformance vectors,
registries under development, and review records remain in the canonical
`prp-spec` working project.
