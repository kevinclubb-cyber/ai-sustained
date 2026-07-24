# Depth Slider — Build / Deploy / Backfill Runbook

_For future-me. Vanilla JS, no dependencies, fits the static Cloudflare Pages setup._

## What it is
A "Reading depth" control at the top of an article. Reader picks **Explain like I'm 5 / Curious / Practitioner / Expert** and the main reading column swaps to a version written at that depth. Choice is saved to `localStorage`, so the site remembers it across articles.

The masthead, hero, stat grid and Tactical Takeaway stay **fixed** — only the `#reading` column changes.

## How it's wired (per article)
1. A CSS block for `.depth`, `.tick`, `#reading` (Clinical Green — already in the pilot `<style>`).
2. A `.depth` control + an empty `<div id="reading"></div>` where the swappable content used to be.
3. A `<script>` at the bottom holding a `DEPTHS` array — four objects, each with `name`, `meta` and `html`. That's the only part that changes article-to-article.

## Deploy (per article)
1. Preview the file locally first (double-click → opens in browser). Test all 4 tiers + refresh (should remember last tier).
2. In GitHub web UI: open `articles/<slug>/index.html` → edit → paste the new version → commit to `main`.
3. Cloudflare Pages rebuilds in ~60s. Hard-refresh the live URL to check.
4. No sitemap change needed (same URL). No new infra.

## Backfill (manual-assisted — the agreed method)
Per article, one at a time:
1. I take the article's current HTML and generate the 4-tier `DEPTHS` block.
2. **You fact-check the AI-drafted tiers** — especially the Expert tier and any stat. The published prose is the source of truth; ELI5/Expert are re-expressions of it.
3. You paste + commit. Cloudflare deploys. Move to next article.

Order suggestion: do the evergreen/explainer pieces first (highest payoff), editorials after.

## Watch-outs
- **Voice on editorials.** The ELI5 and Expert tiers can flatten a strongly-voiced piece. Read them as Kevin, not as a machine, before committing.
- **Stats must survive the rewrite.** Every tier must keep the same numbers (95% at L0–3, 20.6m, etc.). Don't let a depth variant invent a figure.
- **SEO.** Google indexes the default (Curious) tier that renders on load. Keep the canonical argument in that tier.
- **Analytics.** Optional: fire a `gtag('event','depth_change',{level})` inside `render()` to measure whether readers actually use it before rolling out wider.

## Next step to industrialise (optional, later)
If manual gets tedious across the whole archive, graduate to a Python script that reads every `articles/*/index.html`, calls an LLM API to draft the 4 tiers, injects the block, and writes files back for you to review + commit. Needs an API key and a review pass. Not needed for the pilot.
