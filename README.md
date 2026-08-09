# Percept-V — project page

Static project page for **The Percept-V Challenge: Can Multimodal LLMs Crack Simple Perception Problems?** (COLM 2026).

This branch (`gh-pages`) contains only the website. No build step, no dependencies — plain HTML, CSS and JS.

```
index.html                  the whole page
static/css/style.css        styles (light + dark, follows the OS theme, with a manual toggle)
static/js/data.js           all paper data: domains, prompts, every results table
static/js/main.js           rendering + interaction
static/images/teaser/       Figure 1 examples
static/images/domains/      one sample image per domain (problem size 9)
static/images/figures/      Figures 2–8 from the paper
.nojekyll                   tells GitHub Pages to serve dotfiles/underscore paths as-is
```

## Hosting on GitHub Pages

Repo → **Settings → Pages** → *Source*: **Deploy from a branch** → branch `gh-pages`, folder `/ (root)` → **Save**.

The site will be published at `https://dair-iitd.github.io/Percept-V/`.

Note: GitHub Pages serves a **public** site even from a private repo only on GitHub Enterprise Cloud. On the
free/Pro plans the repo must be public for Pages to be reachable.

## Local preview

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

## Things to fill in before release

| What | Where |
| --- | --- |
| BibTeX | `index.html`, `<pre id="bib">` — currently the arXiv entry; update once the official COLM entry exists. Note the arXiv author list omits Goswami and Mausam. |
| Social preview image | `index.html`, `og:image` currently points at the radar chart. |

Any hero button left on `href="#"` with a `data-link` attribute renders as a greyed "soon" chip instead of a
live link, so links can be removed and restored without touching the CSS.

## Updating the numbers

Everything numeric lives in `static/js/data.js` — `RESULTS_SKILL`, `RESULTS_DOMAIN`, `FINETUNE`, `HUMAN_STUDY`,
`ONE_SHOT`, `RESOLUTION`, `THREE_D`, `PROMPT_STYLE`, `FORMAT_ERRORS`. Column order matches the `MODELS` array.
Edit there and the tables, heat-map shading and per-domain accuracy bars all update.

## Credits

Layout conventions from the [Academic Project Page Template](https://github.com/eliahuhorwitz/Academic-project-page-template),
released under [CC BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/).
