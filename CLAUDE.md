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

- `slop-or-supper`, `A-British-Prompt`, `vibe-coding-capability` reference a `cover.png` that has never existed. Their `cover-v2.png` art is present but unwired.
- `/learn/og-learn.png` missing → broken social preview on `/learn/`, `/learn/programme/`, `/learn/terms/`.
- `009_siri_but_make_it_gemini/index.html` points at `/articles/siri-gemini-takeover/` (slug mismatch).
- `/logo.png` and `case-studies/ifg-data-platform/cover.png` referenced, neither exists.
- `pilot-competency-pyramid-index.html` uses a relative `og:image`; scrapers need absolute.

## Identity

Commits here use `Kevin Clubb <269910415+kevinclubb-cyber@users.noreply.github.com>`, set per-repo. Global git config is a work email and must not appear in this repo — if you add a new clone, set the local identity.
