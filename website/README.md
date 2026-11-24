# Paddlr Website

Static landing page for Paddlr, deployed to GitHub Pages at <https://thanhdt942.github.io/paddlr/>.

Plain HTML, CSS, and JavaScript. No build step, no dependencies. Supports English (`en`) and Vietnamese (`vi`).

```text
website/
├── index.html
└── assets/
    ├── css/styles.css
    ├── js/i18n.js        # STRINGS (en/vi) and AGENTS install data
    ├── js/main.js        # i18n runtime, installer tabs, clipboard copy, theme toggle
    └── images/favicon.svg
```

## Local preview

```bash
python -m http.server 8000 --directory website
# open http://localhost:8000/
# or test Vietnamese directly: http://localhost:8000/?lang=vi
```

All asset paths are relative (`./assets/...`), so the page works both at a domain root and under the `/paddlr/` repository subpath.

## Adding or changing an agent

Edit the `AGENTS` array in `assets/js/i18n.js`. Shared invariant fields (`id`, `name`, `fullName`, `status`, command strings, and `docs.href`) are defined once. User-facing text fields (`prerequisites`, `methods[].label`, `methods[].note`, `verify.text`, and `docs.label`) provide both `en` and `vi` values. The tabs and panel render from this data; no HTML changes are needed.

Only add commands that have been verified against the agent's CLI.

## Updating translations

Edit `STRINGS.en` and `STRINGS.vi` in `assets/js/i18n.js`. Keep exact key parity between both locales. Plain-text elements in `index.html` bind via `data-i18n`, inline HTML elements containing trusted `<code>` or `<a>` tags bind via `data-i18n-html`, and ARIA labels bind via `data-i18n-aria-label`.

## Deployment

`.github/workflows/deploy-pages.yml` uploads `website/` and deploys it with the official GitHub Pages actions on pushes that touch `website/**` (branches `dev` and `release`) or on manual `workflow_dispatch`.

One-time repository setting: **Settings -> Pages -> Build and deployment -> Source: GitHub Actions**. The `github-pages` environment must allow the deploying branch.
