# AI Sustained — Article Anatomy

**Reference article:** Issue 014 · `openai-hugging-face-hack` · "OpenAI's AI escaped, hacked Hugging Face and stole the answers" · published 23 Jul 2026
**Skin:** Forest & Acid (Brand v2.0, dark) — the current standard
**Last updated:** 24 Jul 2026

> A component-by-component map of a standard article, header to footer. Use it as a build checklist and a consistency reference. Plain Markdown — portable to GitHub, wiki, Cloudflare, Notion or Google Docs.

---

## 0. Page shell & tech baseline
| Item | Detail |
|------|--------|
| File | `articles/<slug>/index.html` — one self-contained hand-written HTML file |
| Framework | None. No build step, no external JS. Static, served as-is by Cloudflare Pages |
| Container | `<article class="page">`, `max-width: 860px`, centred |
| Top signal | 3px acid (`#E8FF3A`) bar across the very top of `<body>` — the instant brand tell |
| Responsive | Single breakpoint at 720px (stacks takeaway grid, shrinks hero) |
| Print | `@media print` → A3 page, avoids breaking stat boxes / quotes / takeaway |

---

## 1. `<head>` — analytics, SEO, fonts

### 1.1 Analytics
Google Analytics (gtag.js), measurement ID **`G-L3WZNV09BB`**. Loaded first in `<head>`. Same ID across the site.

### 1.2 Meta / SEO stack (all present on 014)
- `charset`, `viewport`
- `title`, `meta description`, `meta keywords`, `meta author`
- **Open Graph:** `og:title`, `og:description`, `og:type=article`, `og:image`
- **Twitter Card:** `twitter:card=summary_large_image`, `twitter:title`, `twitter:description`, `twitter:image`
- **JSON-LD** `schema.org/Article`: headline, author (Person "Kevin Clubb"), datePublished, description, keywords, image, publisher (Organization "AI Sustained")

> Note: 014's OG/Twitter/JSON-LD `image` values are **relative** (`openai_hugging_face_hack_Article_Cover.png`). The homepage uses absolute URLs. For reliable social previews, prefer absolute `https://ai-sustained.com/articles/<slug>/<image>`.
> Note: 014 has **no** `rel=canonical` in the article (the homepage does). Worth adding per article for SEO hygiene.

### 1.3 Fonts (Google Fonts)
| Role | Family |
|------|--------|
| Headlines, decks, pull-quotes, takeaway accents | **Fraunces** (serif; italic for accents) |
| Section headings h2/h3, strong body | **Space Grotesk** |
| Body copy | **Inter** |
| Metadata, stats, kickers, masthead, tags | **JetBrains Mono** (uppercase, tracked) |

### 1.4 Colour tokens (`:root`, Forest & Acid)
`--forest #1B4332` (ground) · `--ink #0A0F0C` (takeaway panel) · `--paper #F2ECD9` (text) · `--acid #E8FF3A` (accent) · `--coral #FF5A3C` (risk only) · `--moss #2D6A4F` · `--sage #74C69D` · `--mint #D8F3DC` · `--muted #8FA398`. Accent used sparingly — a line, a word, a numeral.

---

## 2. Body components, in order

### 2.1 Masthead — `header.masthead`
Two rows of mono uppercase metadata. Left: `AI Sustained.` wordmark (acid) + issue number. Right: date (e.g. `23 JUL 2026`) + category (e.g. `AI Made Simple · Cybersecurity`). Bottom rule.

### 2.2 Hero — `section.hero` (centred)
- **Kicker** — mono acid label with a short leading rule (category/series).
- **H1** — Fraunces, large `clamp(42px…74px)`, one italic **acid accent** phrase via `<span class="accent">`.
- **Deck** — Fraunces italic, `--paper-2`, one sentence; may include an acid accent word.

### 2.3 Hero figure — `figure.hero-figure` *(optional)*
Full-width image, acid top-border, rounded. Mono `figcaption`. **Alt text is detailed and descriptive** (accessibility + SEO). 014's image: `ai_escaping_hero.png`.

### 2.4 Stat grid — `section.stat-grid`
2–4 `.stat-box` cards (auto-fit, min 170px). Each: mono sage **label**, big mono **acid value** with optional `.unit`, small **note**. Acid bottom border. 014 uses four: 17,000+ actions / 10,000+ flaws / 271 Firefox fixes / 4 chained bugs.

### 2.5 Table of contents — `nav.toc` *(long reads)*
Panel with mono acid label "In this issue"; ordered list of anchor links (`#section-id`) with mono acid numbers. Anchors map to `id`s on the `h2`s below.

### 2.6 Content — `section.content`
Main reading column, `max-width: 680px`. Supported inline/block elements:
- `p`, with `strong` (Space Grotesk) and `em` (Fraunces italic, acid)
- `a` — acid, underlined (external source links open inline)
- `h2` (Space Grotesk 32px, carries anchor `id`) and `h3` (19px)
- `ul` / `ol` with acid list markers
- `span.inline-highlight` — acid emphasis on a key phrase/number
- **`blockquote.pull-quote`** — centred Fraunces italic, acid top/bottom rules, big acid quote mark. Used 2× in 014 as mid-article emphasis beats.

### 2.7 Tactical Takeaway — `section.takeaway` **(signature, mandatory)**
Ink-black panel (`--ink`), the one surface darker than the ground, with a faint acid ring motif. Mono acid label "Tactical takeaway"; Fraunces italic H2 thesis; **three points**, each a mono acid number-label (`01 · CAPABILITY`) + a Fraunces italic sentence with a Space Grotesk `strong` phrase. This is the "what to do about it" close.

### 2.8 Subscribe / Substack slab — `section.cta-slab`
Full acid-fill slab (inverse of the page), ink text, faint ink ring. Marked in source as `<!-- SLOT: subscribe / substack slab -->`.
- Mono kicker "Read more · Subscribe"
- Space Grotesk H2 with Fraunces italic accent
- Intro paragraph
- **Two buttons** (`.cta-row`):
  - `Read on Substack` → the specific Substack post URL (with `utm_campaign`/`utm_medium` and `showWelcomeOnShare` params), `target="_blank" rel="noopener"`, `↗` glyph.
  - `Subscribe` (`.primary`) → **`/#subscribe`** — the site's single live HubSpot newsletter form on the homepage. `→` glyph. (Comment in source confirms: one central form, not per-article.)

### 2.9 Footer — `footer.footer`
- **`footer-cta`** — a Fraunces italic parting question with an acid `strong` phrase (e.g. "which room could it not get out of?").
- **`sources`** — mono, muted, a `·`-separated list of **outbound source links** (sage), one per cited claim. 014 links OpenAI, Hugging Face, Anthropic Glasswing, Anthropic Fable redeployment, AP.

### 2.10 Tags — `div.hashtags`
Mono label "Tags" + a line of sage `#Hashtags` (7 on 014). Feed LinkedIn/social reuse.

### 2.11 Colophon — `div.colophon`
Acid top rule; mono uppercase. Left: `AI Sustained.` wordmark + "By Kevin Clubb". Right: year.

---

## 3. Links & outbound map (what points where)
| From | To | Purpose |
|------|----|---------|
| TOC anchors | in-page `#section-id` | jump navigation |
| Inline `content a` | primary sources (OpenAI, HF, Anthropic, AP…) | evidence |
| Footer `sources` | same primary sources, consolidated | citation block |
| CTA "Read on Substack" | `open.substack.com/pub/aisustained/p/<post>` + UTM | deeper version / funnel |
| CTA "Subscribe" | `/#subscribe` (homepage HubSpot form) | list capture |
| Masthead/colophon wordmark | (text only on 014, not linked) | brand |

**Funnel logic:** article (free, SEO) → Substack (depth + subscribe) → HubSpot list (`/#subscribe`). Substack links carry UTMs; the internal Score CTA (seen on older articles) carries `utm_source=editorial`.

---

## 4. Add-on features seen across articles
- **AI Survival Score CTA** — ink/acid block linking `ai-sustained.com/learn/score/` with UTM tags. Present on several older articles' footers (competency-pyramid, ai-curious, etc.). *Not* on 014 — 014 uses the Substack slab instead. Decide whether both should co-exist.
- **AI Slider** — optional adaptive-depth control (see AI Slider spec). Not yet on any live article.
- **Hero figure** — optional; 014 has one, 001 does not.

---

## 5. Consistency watch-list (for the skill review)
1. **Two skins live:** 001 = Clinical Green (light), 014 = Forest & Acid (dark). Decide: migrate legacy or leave.
2. **Social image paths:** relative on 014, absolute elsewhere — standardise on absolute.
3. **`rel=canonical`:** on homepage, missing on 014 article — add per article.
4. **Closing CTA:** some articles close on the Survival Score, 014 closes on Substack — pick a default order (or allow both: Substack slab → Score).
5. **TOC presence:** long reads have it, short ones don't — fine, but make it a documented rule.
