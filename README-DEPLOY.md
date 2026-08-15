# ai-sustained.com — rev E, 15 August 2026

## What changed in this revision

**Facebook and TikTok removed from the landing page footer.** The social row now shows **LinkedIn and Substack** only. Both buttons were removed cleanly, icon and SVG included, leaving no gap in the markup.

They appeared only on `index.html` — no other page carries the social row — so this is a one-file change on top of everything below.

Worth a thought before you deploy: TikTok and Facebook are your two main traffic sources into the editorial. Removing the outbound links doesn't affect inbound traffic at all, but it does remove the route for a reader who wants to follow you after reading. If the intent was to stop leaking attention outward, this is right. If it was to tidy the footer, keeping TikTok might be worth it. Your call — it's one line to put back.

---

**35 HTML files. Editorial site only.** Complete and self-contained — upload all 35 and the site is correct regardless of what landed before.

---

## 1. Footer: links line one, text line two

Same treatment as the consulting site. Verified at 1280px and 390px.

Your home page footer read:

```
BUILT BY HAND · HOSTED ON CLOUDFLARE PAGES · SOURCE ON GITHUB ↗
                                    · PRIVACY · COOKIE CHOICES
```

It now reads:

```
SOURCE ON GITHUB ↗ · PRIVACY · COOKIE CHOICES
BUILT BY HAND · HOSTED ON CLOUDFLARE PAGES
```

**This needed six different edits, not one.** Your editorial footers come in six shapes:

| Shape | Pages | What happened |
|---|---|---|
| `footer-right` | index | The `<p>` split into a links line and a text line |
| `.sources` | 23 articles and the ledger | No links at all previously — a links row added above the sources note |
| bare `<span>` | advertise, learn/programme, learn/score, learn/terms | Links and text were mixed in one span; separated into two |
| `.wrap` | learn | Same mixing, same fix |
| `brand-footer` | case-studies ×2, privacy, ifg-data-platform | Text and links were side by side in a flex row. Reordered links-first and given `flex-basis:100%` so they stack |
| article closing section | AI-Space-Race, 009_siri | `<footer>` is article content on these, so a discrete links row was appended rather than restructuring the section |

---

## 2. Two things caught in testing

**Duplicate Privacy links.** `/learn/` and `/advertise/` already had a Privacy link in the footer, so adding another produced `Privacy · Privacy`. The links row now de-duplicates by label, keeping the first.

**A lost separator.** Pulling the anchors out of the mixed spans also stripped the middot between the remaining text fragments, so the home page briefly read `BUILT BY HAND HOSTED ON CLOUDFLARE PAGES`. Restored on the two pages affected.

Both were caught by rendering the pages and reading the output, not by inspecting the code — worth knowing if you ever redo this by hand.

---

## 3. Mobile

The links row wraps, with `white-space:nowrap` on each link so labels break *between* links rather than mid-phrase. At 390px the home footer stacks: social icons, wordmark, links row, text row. No label is split in half.

---

## 4. Also carried in this package

Complete replacement, so everything from the earlier revisions is here:

- GTM `GTM-K3HFQT6S` and GA4 `G-L3WZNV09BB`, consent block ordered before both
- Consent banner **rev B** fixes — the panel reflects your actual saved choice, and reopening never silently revokes consent
- The **updated privacy notice** at `privacy/index.html`, covering Clarity and the consent-first position

---

## 5. Upload

1. `ai-sustained` repo → **Add file → Upload files**
2. Drag the whole `editorial-deploy` **folder** in
3. Commit: `Footer layout, consent rev D`
4. **Confirm the commit says 35 files changed**
5. Cloudflare → Caching → Configuration → **Purge Everything**

---

## 6. A permanent fix for the cache problem

Your footer confirmed the site runs on **Cloudflare Pages**, which means the `_headers` file in your repo root is live and is the right place to solve this properly instead of purging by hand every deploy.

Add this **above** the existing rule:

```
/*.html
  Cache-Control: public, max-age=0, must-revalidate

/
  Cache-Control: public, max-age=0, must-revalidate
```

Keep your existing block underneath:

```
/case-studies/index.json
       Access-Control-Allow-Origin: *
       Cache-Control: public, max-age=300
```

HTML then revalidates on every request while images, CSS and fonts keep their long cache lifetimes. Deploys go live immediately and you stop chasing ghosts.

I have **not** put this in the package — it changes caching behaviour site-wide and you should make that call deliberately rather than find it in a drop. Two lines, whenever you want it.

---

## 7. Verification already done

| Check | Result |
|---|---|
| All 35 carry the consent block exactly once, ordered before `gtm.js` | Pass |
| All 35 carry GA4 `G-L3WZNV09BB` exactly once | Pass |
| Footer reopen link present in markup on all 35 | Pass |
| No duplicate injected footer block | Pass — 0 across 9 sampled pages |
| Links line stacked above text line | Pass, desktop and mobile, all footer shapes |
| Duplicate Privacy links | None remaining |
| HTML parses cleanly | Pass |
| JavaScript errors introduced | None |

---

## 8. Still outstanding

**The Clarity consent setting in GTM-K3HFQT6S.** Tags → Microsoft Clarity → Advanced Settings → Consent Settings → require `functionality_storage` → Submit → Publish. Nothing in this package changes it, and until it is published session recording runs on visitors who declined it.
