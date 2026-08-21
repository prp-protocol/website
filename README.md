# Participant Relationship Protocol website

Static public website for the PRP project. This repository is the canonical
working copy for both the internal Gitea mirror and the public GitHub Pages
site.

The site is intentionally build-free: the files in the repository root are the
files served in production.

## Local preview

Open `index.html` in a browser, or serve the directory with any static server:

```sh
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

## Repository and publication flow

- `origin` is the internal Gitea repository. Commit completed changes to
  `main`; the Agentmux publisher sends those commits to Gitea.
- `github` is the public `prp-protocol/website` repository. After the Gitea
  publication is complete, run `./scripts/publish-github.sh` from a clean
  `main` branch.
- The publication script sends the same commit to GitHub's `main` and
  `gh-pages` branches. This keeps the public source and the GitHub Pages source
  identical.

Do not edit `gh-pages` directly. Every published GitHub revision must first
exist as a regular commit on `main`.

## Source material

Content is derived from:

- `../specifications/prp-architecture-v1-rc1.md`
- `../specifications/README.md`
