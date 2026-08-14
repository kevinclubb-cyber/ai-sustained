# Issue 017a — publish checklist

**Slug:** `ai-models-v-public-detector-dilemma`
**Date:** 14 Aug 2026 · **Category:** Policy · **Text by:** Google Gemini, unedited

## 1. Drop in

```
articles/ai-models-v-public-detector-dilemma/index.html
articles/ai-models-v-public-detector-dilemma/ai-models-v-public-detector-dilemma_hero.png   1920x1080
articles/ai-models-v-public-detector-dilemma/cover.png                                      1200x675
```

Both images are already the live filenames the repo expects, so no rename is needed. Both were built as the same frame (hero rendered natively at 1920x1080, card downscaled from it) and both are pngquant'd at `--quality=82-98`. Hero is 1.6MB, card 547KB.

## 2. `index.html` — add to `#editorial-grid`, immediately after the Issue 017 card

```html
<a class="card" data-topic="strategy" data-type="news" href="/articles/ai-models-v-public-detector-dilemma/">
  <div class="card-image">
    <img src="/articles/ai-models-v-public-detector-dilemma/cover.png" alt="The Engine Under the Bonnet: AI Models v Public Detector Dilemma. Cover image: rows of identical hexagonal bolt heads across a dark engine block, six lit acid green from inside their sockets, a knurled socket key resting over the row." />
  </div>
  <div class="card-body">
    <div class="card-meta">
      <span>Issue 017a</span>
      <span class="dot"></span>
      <span>Policy</span>
      <span class="dot"></span>
      <span class="muted">5 min read &middot; 14 Aug 2026</span>
    </div>
    <h3 class="card-title">The Engine Under the Bonnet: AI Models v Public Detector Dilemma</h3>
    <p class="card-deck">Exploring AI's version of prohibition, the mechanics of cryptographic keys, and how everyday users can avoid the AI proofreading trap.</p>
    <span class="card-cta">Read</span>
  </div>
</a>
```

## 3. `search-index.json` — add to `pages`, after the 017 entry

Tags are **space separated** in this file, which is not what the skill's `_search-entry.json` emits. The converted version is below, use this one.

```json
{
  "type": "Editorial",
  "ref": "Issue 017a",
  "title": "The Engine Under the Bonnet: AI Models v Public Detector Dilemma",
  "url": "/articles/ai-models-v-public-detector-dilemma/",
  "date": "2026-08-14",
  "summary": "A second model's read on watermarking: how the green list works, what a cryptographic key is, and why publishing the detector breaks it.",
  "tags": "watermark greenlist cryptographic key detector euaiact spoofing proofreading gemini"
}
```

## 4. `sitemap.xml`

```xml
<url>
  <loc>https://ai-sustained.com/articles/ai-models-v-public-detector-dilemma/</loc>
  <lastmod>2026-08-14</lastmod>
  <changefreq>monthly</changefreq>
  <priority>0.7</priority>
</url>
```

## 5. `llms.txt` — Editorial (selected)

```
- [Issue 017a: The Engine Under the Bonnet, AI Models v Public Detector Dilemma](https://ai-sustained.com/articles/ai-models-v-public-detector-dilemma/): how text watermarking actually works, the green list, the cryptographic key, and why handing the detector out defeats it. Written by Google Gemini, published unedited as a follow up to Issue 017.
```

## 6. Nothing on Substack

017a has **no Substack edition** and no Substack link anywhere on the page. The closing slab points back to Issue 017 instead. Nothing to post, no slug to match.

## Verification already run

- `check_article.py`: 20 pass, 0 warnings. The only remaining failure is the missing Substack markdown, which is deliberate.
- Served over `python3 -m http.server` and rendered in headless Chromium. Card reports natural size 1200x675, hero reports 1920x1080, both `complete: true`, no 404s on either page.
- Grepped for em and en dashes: none in reader-facing text. Two remain in HTML comments, identical to Issue 017.

## When you replace the hero with the Gemini frame

The prompt is in `ai-models-v-public-detector-dilemma_cover_prompt.md`. When you swap the file in, update two things or the page starts lying: the `alt` text on `.hero-figure img`, and the `figcaption`, which currently reads "Built in house". Regenerate `cover.png` as a straight 1200x675 downscale of the new hero so the two stay the same frame.
