# Paddlr Website

Static landing page for Paddlr, deployed to GitHub Pages at <https://thanhdt942.github.io/paddlr/>.

Plain HTML, CSS, and JavaScript. No build step, no dependencies.

```text
website/
├── index.html
└── assets/
    ├── css/styles.css
    ├── js/main.js        # AGENTS data (install instructions) + UI logic
    └── images/favicon.svg
```

## Local preview

```bash
python -m http.server 8000 --directory website
# open http://localhost:8000/
```

All asset paths are relative (`./assets/...`), so the page works both at a domain root and under the `/paddlr/` repository subpath.

## Adding or changing an agent

Edit the `AGENTS` array at the top of `assets/js/main.js`. Each entry defines `id`, `name`, `status` (`supported` | `experimental` | `planned`), `prerequisites`, `methods[].steps[]` (one entry per command that must be run separately), `verify`, and `docs`. The tabs and panel render from this data; no HTML changes are needed.

Only add commands that have been verified against the agent's CLI.

## Deployment

`.github/workflows/deploy-pages.yml` uploads `website/` and deploys it with the official GitHub Pages actions on pushes that touch `website/**` (branches `dev` and `release`) or on manual `workflow_dispatch`.

One-time repository setting: **Settings → Pages → Build and deployment → Source: GitHub Actions**. The `github-pages` environment must allow the deploying branch.
