# AI Slider — Functional & Technical Specification

**Feature:** Adaptive reading-depth slider ("AI Slider")
**Product:** ai-sustained.com editorial / learn
**Owner:** Kevin Clubb
**Status:** Pilot built, not yet live
**Last updated:** 24 Jul 2026

> Keep this file current. Every time the slider is applied to (or removed from) an article, update the **Deployment Log** at the bottom. Plain Markdown — drops cleanly into GitHub, a wiki, Cloudflare, Notion or Google Docs.

---

## 1. Functional breakdown

### 1.1 What it is
A control pinned to the top of an article that lets the reader choose how deep they want the writing to go. Moving the control rewrites the article's main reading column into a version written at that depth. The page furniture (masthead, hero, stats, Tactical Takeaway) stays fixed.

### 1.2 The four depths
| # | Tier | Audience | Rough length |
|---|------|----------|--------------|
| 0 | Explain like I'm 5 | Total newcomer | ~200 words |
| 1 | Curious | General reader (the published default) | ~600 words |
| 2 | Practitioner | Works in the field | ~1,000 words |
| 3 | Expert | Assumes fluency | ~900 words, denser |

Tier 1 (Curious) is the default that loads on first visit and the version search engines index.

### 1.3 Why it exists
- One article can serve a newcomer and a practitioner without writing four separate posts.
- It is self-demonstrating: an AI editorial using AI-shaped content depth on the page.
- It is rare, so it reads as a signature feature rather than a blog gimmick.

### 1.4 User-visible behaviour
- Four labelled buttons + a range slider; both stay in sync.
- Changing depth fades the reading column out and back in (~190 ms).
- A small metadata line shows the current tier name and approximate length/read-time.
- The reader's last choice is remembered across articles (persists via `localStorage`).

### 1.5 Explicit non-goals
- No live AI call in the reader's browser. Variants are pre-written and cached in the page.
- Does not restyle or re-flow the hero, stat grid, or Tactical Takeaway.
- Not a translation or tone toggle — it is depth only.

---

## 2. Technical specification

### 2.1 Architecture
Pure client-side, zero dependencies. Fits the site's static, no-build, no-framework model (hand-written HTML/CSS on Cloudflare Pages).

Three parts inside the article's `index.html`:

1. **CSS block** — styles for `.depth` (control), `.tick` (buttons), `.reading-meta`, and `#reading` (the swap target). Uses the article's own colour variables so it inherits whichever skin the article uses.
2. **Markup** — the `.depth` control plus an empty `<div id="reading"></div>` where the swappable content sits. Fixed sections (takeaway, footer) live outside `#reading`.
3. **Script** — a `DEPTHS` array of four objects (`name`, `meta`, `html`) and ~20 lines of vanilla JS that paints the chosen tier, toggles the active button, and reads/writes `localStorage`.

Only the `DEPTHS` array changes from article to article. The CSS and JS are boilerplate.

### 2.2 The data shape
```js
const DEPTHS = [
  { name: "Explain like I'm 5", meta: "≈200 words · 1 min", html: `...` },
  { name: "Curious",           meta: "≈600 words · 4 min", html: `...` },
  { name: "Practitioner",      meta: "≈1,000 words · 7 min", html: `...` },
  { name: "Expert",            meta: "≈900 words · 6 min",  html: `...` }
];
```
`html` holds the article body markup for that tier (`.content` sections, tier bands, pull-quotes — whatever that article uses).

### 2.3 Persistence
`localStorage` key `aisustained_reading_depth` stores the integer 0–3. On load, the script restores it; default is `1` (Curious) if unset. No cookies, no tracking, no server.

### 2.4 Performance & SEO
- All four variants ship in the initial HTML, so there is no network wait on depth change.
- The default (Curious) tier renders on load and is what crawlers see — keep the canonical argument and key facts in that tier.
- Adds one small inline `<script>`; no external JS. Consistent with the site's zero-JS philosophy (this is the one deliberate exception).

### 2.5 Optional analytics hook
To measure real usage before wider rollout, add inside the `render()` function:
```js
if (window.gtag) gtag('event', 'depth_change', { level: d.name });
```
The site already loads gtag (`G-L3WZNV09BB`), so this needs no extra setup.

### 2.6 Two skins (important)
The site runs two design systems. The slider must match the host article:

| Skin | Used by | Ground | Text | Accent | Headlines |
|------|---------|--------|------|--------|-----------|
| Clinical Green (light) | Older articles (e.g. 001 competency-pyramid) | `#F7FCF9` | `#081C15` | `#1B4332` | Playfair Display |
| Forest & Acid (dark, v2.0) | Newer articles (e.g. 014) + newsletter skill | `#1B4332` | `#F2ECD9` | `#E8FF3A` | Fraunces |

Because the slider CSS references each article's own variables, dropping it into a Forest & Acid article inherits the dark skin automatically, provided the class names match that article's stylesheet.

---

## 3. Integration & deployment

### 3.1 Per-article process
1. Take the article's current body markup.
2. Generate the four `DEPTHS` variants from it (manual-assisted: draft → **Kevin fact-checks** → paste).
3. Wrap the fixed sections (Tactical Takeaway, footer) outside `#reading`.
4. Paste the CSS + control + script into the article's `index.html`, replacing the old single-version body.
5. Commit **directly to `main`** → Cloudflare rebuilds in ~60s.
6. Hard-refresh (Cmd/Ctrl+Shift+R) to confirm.
7. Update the Deployment Log below.

### 3.2 Common failure
Uploading the slider as a *new* file (e.g. `pilot-...-index.html`) does not change the live article — the live URL serves `index.html`. To go live you must overwrite `index.html` itself, keeping that exact filename (it preserves the URL, sitemap entry, and backlinks).

### 3.3 Quality gates before commit
- Every tier keeps the same headline facts and figures — a depth variant must never invent a number.
- Read the ELI5 and Expert tiers in Kevin's voice; on strongly-voiced editorials they can flatten tone.
- Confirm the default (Curious) tier still reads as the canonical piece for SEO.

---

## 4. Deployment Log

_Update this table on every change. Status values: `planned` · `pilot (staged)` · `live` · `removed`._

| Issue | Slug | Skin | Status | Depths authored | Live URL | Notes | Updated |
|------:|------|------|--------|-----------------|----------|-------|---------|
| 001 | ai-competency-pyramid | Clinical Green | pilot (staged) | 0–3 ✔ | staged as `pilot-competency-pyramid-index.html` | Not yet merged into `index.html`. Preview only. | 24 Jul 2026 |
| 014 | openai-hugging-face-hack | Forest & Acid | planned | — | — | Candidate for first Forest & Acid rollout. | 24 Jul 2026 |

### Rollout backlog (agreed scope: all articles, editorials included)
Suggested order — evergreen/explainer pieces first, then editorials:
1. `ai-made-simple` (013)
2. `ai-curious`
3. `ai-competency-pyramid` (001) — finish the staged pilot
4. Remaining editorials as time allows.
