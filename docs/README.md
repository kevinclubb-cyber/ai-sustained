# AI Sustained — Documentation

Internal docs for the ai-sustained.com editorial site. Plain Markdown; GitHub renders this folder automatically.

**Last updated:** 24 Jul 2026 · **Maintainer:** Kevin Clubb

---

## Contents

| Doc | What it covers | Update when… |
|-----|----------------|--------------|
| [AI-Slider-Spec.md](./AI-Slider-Spec.md) | The "AI Slider" adaptive reading-depth feature — functional breakdown, technical spec, per-article integration, and the **Deployment Log** | You apply, change or remove the slider on any article |
| [Article-Anatomy.md](./Article-Anatomy.md) | Component-by-component map of a standard article (reference: Issue 014), header to footer — SEO, fonts, colours, every section, links & funnel | The article template changes, or a new standard component is added |
| [newsletter-skill-slider-addition.md](./newsletter-skill-slider-addition.md) | The slider option to add to the `ai-sustained-newsletter` skill, with the recommendation on when to use it | You revise the skill or the slider recommendation |

---

## How the site works (one-paragraph orientation)

Hand-written static HTML/CSS, no framework and no build step, hosted on Cloudflare Pages. Each article is a single `articles/<slug>/index.html`. Every commit to `main` auto-deploys in ~60 seconds. There are currently **two design skins** live — Clinical Green (light, older articles) and Forest & Acid (dark, current standard, v2.0). See [Article-Anatomy.md](./Article-Anatomy.md) for the full breakdown.

## Keeping these docs current

- **Slider Deployment Log** is the one table that must never go stale — update it in the same commit that ships a slider change. It's at the bottom of [AI-Slider-Spec.md](./AI-Slider-Spec.md).
- Bump the **Last updated** date at the top of any doc you edit.
- Keep everything in plain Markdown (no raw HTML) so it stays portable to a wiki, Notion or Google Docs.

## Open items / consistency watch-list

Tracked in full at the end of [Article-Anatomy.md](./Article-Anatomy.md). Headlines:

1. Two brand skins live — decide whether to migrate legacy Clinical Green articles to Forest & Acid.
2. Standardise social-image paths (absolute vs relative) and add `rel=canonical` per article.
3. Pick a default closing CTA order (Substack slab vs AI Survival Score, or both).
4. Review the `ai-sustained-newsletter` skill for consistency with the current live template.
