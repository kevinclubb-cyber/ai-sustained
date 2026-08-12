# Issue 016 — publish package

**Article:** The Victorians out-spent us. That is not the comfort it sounds like.
**Slug:** `ai-vs-industrial-revolution` · 12 Aug 2026 · AI Made Simple · History
**Live URL when deployed:** https://ai-sustained.com/articles/ai-vs-industrial-revolution/

## What goes in the repo

Copy `articles/ai-vs-industrial-revolution/` into the repo root, preserving the path. Three files, nothing else:

| File | Purpose |
|---|---|
| `index.html` | The article. Self-contained, no build step, no external JS |
| `ai-vs-industrial-revolution_hero.png` | 1920x1080 in-article hero and social preview image |
| `ai-vs-industrial-revolution_card.png` | 1200x675 thumbnail for the article catalogue |

## What does NOT go in the repo

Everything in `_not-for-deploy/` is a working file:

- `..._substack.md` — the extended edition, paste into Substack
- `..._search-entry.json` — merge this object into the `pages` array of the root `search-index.json`
- `..._cover_prompt.md` — record of the cover-art brief, for regenerating the hero later

## Publish checklist

1. Copy the article folder in, path intact.
2. Merge the search entry into `search-index.json`. Without it the article is invisible to site search.
3. Add the article to `sitemap.xml`.
4. Add the article card to the catalogue page, using `ai-vs-industrial-revolution_card.png`.
5. Check `llms.txt` if it carries an article list.
6. Post the extended edition to Substack. The CTA in the article already points at
   `open.substack.com/pub/aisustained/p/when-centuries-become-years-ai-and`.
7. Update the Deployment Log in `AI-Slider-Spec.md` — this issue ships all four depths.

## Notes

- The AI Slider ships with all four tiers authored. The Curious tier is the canonical
  version captured from the page at init, so crawlers and no-JS readers get the full article.
- All four tiers carry identical figures. An error in one is an error in four.
- Every stat is sourced and every source is linked inline and in the footer.
