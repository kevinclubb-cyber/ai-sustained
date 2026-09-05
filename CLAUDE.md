# ai-sustained.com — editorial

Static, hand-written HTML/CSS. No framework, no build step, no bundler. Files in this repo are served as-is.

- **Live at** https://ai-sustained.com
- **Host** Cloudflare Pages, auto-deploys on push to `main`, live in ~60s
- **Sibling repo** `ai-sustained-consulting` → consulting.ai-sustained.com (local: `../AIS_C`)

## Every push publishes

There is no staging environment and no review gate. A push to `main` is a publish. Get it right before pushing rather than fixing forward, and say so in chat when a push has just put something live.

## Pull before you commit

`.github/workflows/update-scores.yml` runs **every 6 hours** and commits `scores.json` straight to `main` as `scores-bot`. Always `git pull --rebase` before committing or you'll hit a non-fast-forward rejection. Those `chore: update scores.json` commits in the log are the bot, not lost work.

## Design system — "Forest & Acid"

Read the palette from the CSS custom properties in `index.html`; don't hardcode hexes from memory.

| Token | Hex | Role |
|---|---|---|
| `--forest` | `#1B4332` | ground |
| `--paper` | `#F2ECD9` | text / cream |
| `--acid` | `#E8FF3A` | accent |
| `--ink` | `#0A0F0C` | deepest |
| `--coral` | `#FF8C61` | secondary accent |
| `--mint` | `#D8F3DC` | soft fill |

Acid has a ramp: `--acid-hi` `#F4FF7A`, `--acid-mid` `#CFE62E`, `--acid-deep` `#9DB324`, `--acid-shadow` `#6E7F14`.

Type: **Fraunces** headlines · **Space Grotesk** section headings · **Inter** body · **JetBrains Mono** data/kickers.

> `README.md` still describes an older "Clinical Green" system (`#F7FCF9` base, Playfair Display, Plus Jakarta Sans). That is **stale** — the site moved to Forest & Acid. Trust the CSS, not the README.

## Images — the rule that matters

Covers are AI-generated photographic art. **Never commit multi-MB PNGs.** In Aug 2026, 25 covers went from 57.9MB to 2.5MB with no visible quality loss.

For each cover:

```bash
cwebp -q 82 cover-source.png -o cover.webp                                  # for <img>
sips -s format jpeg -s formatOptions 82 cover-source.png --out cover.jpg    # for og:image
```

- `<img src>` → the **`.webp`**
- `og:image` / `twitter:image` → the **`.jpg`** (social scrapers handle WebP unreliably)
- If the image is *only* ever an `og:image`, skip the WebP entirely.

Do **not** use Git LFS. Cloudflare Pages does not fetch LFS objects at build time, so every tracked image would be served as a ~130-byte text pointer.

## Verifying before you push

Cloudflare returns **HTTP 200 with an HTML page** for missing files. Status codes prove nothing — check `content_type` or magic bytes:

```bash
curl -s -o /dev/null -w "%{content_type}\n" https://ai-sustained.com/path/to/cover.webp
```

To render locally: `python3 -m http.server 8787` from the repo root. Force `loading="lazy"` images to load before counting broken ones, or you'll get false positives on the case-study tiles.

## Layout

```
index.html          landing page          articles/<slug>/index.html + cover.webp/.jpg
case-studies/       case studies          cover-set/       reusable cover art
learn/              learning hub          ledger/          receipts.json
advertise/          partners page         scripts/         fetch-scores.mjs (CI)
resource/ docs/ privacy/                  _headers         Cloudflare headers
llms.txt  robots.txt  sitemap.xml
```

Adding an article: create `articles/<slug>/`, add `index.html` + optimised cover, add a card to `index.html`, add the URL to `sitemap.xml`. `README.md` tells you to do this through the GitHub web UI — **ignore that**, it predates the local clone. Work locally and push.

## Known pre-existing breakage

Not regressions; don't "fix" them by accident, and don't count them as new:

- **`case-studies/ifg-data-platform/`** is a **draft scaffold**, not a finished page — `[bracketed]` placeholder copy and a visible coral DRAFT banner — and it references a `cover.png` that has never existed, with no source art anywhere in the repo. It carries `noindex, nofollow` so search engines leave it alone, but it is **still publicly reachable at its URL**. Finishing it needs new artwork and real copy; unpublishing it is Kevin's editorial call, not a fix to make unprompted. Its `<head>` also has a duplicated `<meta charset>`.
- **`README.md`** contains `/articles/<slug>/cover.webp` as a template placeholder. A link checker will flag it; it isn't a real reference.

## Case study numbering — two systems, don't "fix" them

The homepage carousel numbers cards **by display order** (001–005). Each case study's own page carries a different internal number, and they don't line up — `shadow-ai-ask-the-workforce` is carousel 001 but its own page says 004, and both `shadow-ai-ask-the-workforce` and `teach-it-once` claim 004 internally. Leave the carousel numbering alone; it is the sequence a reader sees.

Current carousel order: `shadow-ai-ask-the-workforce` · `single-source-of-truth` · `charles-virtual-agent` · `teach-it-once` · `screenshot-paste-build`. `ifg-data-platform` is deliberately absent (draft). When you add a case study, it needs a card in `index.html`, a card in `case-studies/index.html`, **and** a `sitemap.xml` entry — `screenshot-paste-build` was live and listed on `/case-studies/` but missing from both the homepage and the sitemap for some time.

### Fixed 21 Aug 2026 — don't re-report these

`slop-or-supper`, `A-British-Prompt` and `vibe-coding-capability` had covers referencing a `cover.png` that never existed; their orphaned `cover-v2.png` art is now wired up as `cover.jpg` (+ `cover.webp` for slop-or-supper, the only one with an `<img>` hero). `/learn/og-learn.jpg` generated from the unused `hero-learn.png`. `009_siri_but_make_it_gemini` had its canonical, `og:url` and social images pointing at `/articles/siri-gemini-takeover/`, a slug that doesn't exist — a canonical resolving to a 404 risks de-indexing — now repointed at the real URL. JSON-LD `publisher.logo` in two articles pointed at a missing `/logo.png`, now `ai_sustained_logo.png`.

## Site plumbing (added 5 Sep 2026)

- **`404.html`** at the repo root. Cloudflare Pages serves it with a genuine 404 status; before it existed, unknown paths returned the homepage with a 200. Don't delete it.
- **`og-card.png`** (1200x630) is the social card for the homepage, `/ledger/` and `/advertise/`. Built from `learn/wordmark_white.png` + `learn/logo_mark_white.png`. Note both of those assets carry a semi-opaque backing plate at alpha 1-31 across the whole canvas — strip anything under alpha 40 or you get a faint box. `ai_sustained_wordmark.png` is the **dark** version and disappears on forest.
- **`sitemap.xml` is hand-maintained** — 33 entries, `changefreq`/`priority`, no `lastmod`. Add new articles and case studies when you publish them. `case-studies/ifg-data-platform/` is deliberately excluded: it is a DRAFT scaffold carrying `noindex, nofollow`.
- **Never inline images as base64.** Two pages did and were 563KB and 372KB, ~90% of which was one data URI. They are now 55KB and 53KB with WebP files alongside.

## The footer utility link row (`.ais-fl`)

The `ai-sustained.com · Privacy · Cookie choices` row is a `<div class="ais-fl">`. **It carries no colour or size of its own in the base stylesheet** — the only `.ais-fl` rule outside a `@media(max-width:640px)` block sets `display` and `white-space`. On the homepage it inherits from `.footer-right a`; on article and case-study pages it sits in `.footer`, which has no descendant `a` rule, so it fell through to browser defaults (`#0000EE`, 16px, underlined) on 23 of 34 pages until 21 Aug 2026.

Every page that has the row now carries this, injected before the last `</style>` in `<head>`:

```css
.ais-fl{font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:0.02em;color:var(--muted,#8FA398)}
.ais-fl a{color:var(--acid,#E8FF3A);text-decoration:none;border-bottom:1px solid transparent}
.ais-fl a:hover,.ais-fl a:focus-visible{border-bottom-color:var(--acid,#E8FF3A)}
```

Two traps when touching this:

- **The obvious anchor is inside a media query.** `.ais-fl{line-height:2.1}` lives inside `@media(max-width:640px)`. Patch there and your rule silently applies on mobile only.
- **`articles/A-British-Prompt/` and `articles/vibe-coding-capability/` define no CSS custom properties at all.** `var(--acid)` is invalid on them and the declaration is dropped. Always give `var()` a literal fallback on these pages — and expect any other token-based rule to fail there too.

`privacy/`, `case-studies/`, `case-studies/ifg-data-platform/` and `articles/009_siri_but_make_it_gemini/` were already correct at 11px mono **mint** and were left alone, so the site runs two footer-link colours (28 acid, 4 mint). Unify only if asked. `articles/AI-Space-Race/` and `articles/future-delivery-squad/` use different footer markup entirely — no `.ais-fl` — and render correctly at 10px mono; the `.ais-fl` string in those two files is inside an instructional HTML comment, not live markup.

### Sizing social images

`og:image` / `twitter:image` are capped at **1200 px** (`sips -Z 1200`), which is ample for every scraper and keeps them roughly 100–500 KB. The earlier bulk conversion left ~14 og JPEGs at full source resolution (up to 2752 px, ~1 MB); they work, but new ones should follow the 1200 px cap.

## Identity

Commits here use `Kevin Clubb <269910415+kevinclubb-cyber@users.noreply.github.com>`, set per-repo. Global git config is a work email and must not appear in this repo — if you add a new clone, set the local identity.
