# GTM rollout — ai-sustained.com (editorial site)

**Container:** GTM-K3HFQT6S (account: AI Sustained)
**Date prepared:** 15 August 2026
**Files changed:** 35 HTML files
**Source:** `ai-sustained-main (1).zip`, downloaded 15 Aug 2026 — current as of today

> **This supersedes the earlier package.** The first version was built from a 13 August download and was missing two articles. Delete `ai-sustained-gtm-deploy-2026-08-15.zip` and use this one.

---

## 1. What was done

Standard two-part GTM snippet on every real page:

- **Head part** — immediately after `<meta charset>`, as high in `<head>` as it can legally go
- **Noscript part** — immediately after the opening `<body>` tag

Nothing else touched. Verified by diffing every file against the untouched original: the only added lines are the GTM blocks (plus the GA4 block on the four pages noted in §2).

### Included — the two articles missing from the first attempt

- `articles/claude-text-watermark-debate/` — Issue 017, "Claude now watermarks everything it writes"
- `articles/ai-models-v-public-detector-dilemma/`

Both already carried GA4 and now carry GTM too. The Issue 017 card on the home page is intact — confirmed present in the packaged `index.html`.

### Pages tagged (35)

Root: `index.html`, `advertise/`, `ledger/`, `privacy/`

`learn/`: index, programme, score, terms

`case-studies/`: index, charles-virtual-agent, ifg-data-platform, screenshot-paste-build, shadow-ai-ask-the-workforce, single-source-of-truth, teach-it-once

`articles/`: 009_siri_but_make_it_gemini, A-British-Prompt, AI-Space-Race, ai-competency-pyramid (index + pilot-competency-pyramid-index), ai-curious, ai-made-simple, **ai-models-v-public-detector-dilemma**, ai-vs-industrial-revolution, claude-chats-google, **claude-text-watermark-debate**, fable-5-mythos-5-suspended, four-labs-seven-days, future-delivery-squad, gpt-56-sol-vs-fable-5, kimi-k3-open-vs-frontier, openai-hugging-face-hack (index + openai_hugging_face_hack.html), slop-or-supper, vibe-coding-capability

### Not tagged (5) — deliberate

| File | Why |
|---|---|
| `article-score-cta-snippet.html` | HTML fragment, no `<head>` or `<body>` |
| `privacy-learn-section.html` | HTML fragment, no `<head>` or `<body>` |
| `articles/openai-hugging-face-hack/cover-source.html` | Image-generation source |
| `articles/openai-hugging-face-hack/openai_hugging_face_hack_cover.html` | 1080x1080 LinkedIn cover source |
| `articles/openai-hugging-face-hack/openai_hugging_face_hack_feed.html` | 1080x1080 LinkedIn feed source |

---

## 2. Four pages had no analytics at all

Carrying **no GA4 tag whatsoever** — invisible in your reporting since publication:

- `articles/AI-Space-Race/index.html` — Issue 007, The Silicon Space Race
- `articles/ai-made-simple/index.html`
- `articles/openai-hugging-face-hack/index.html`
- `articles/openai-hugging-face-hack/openai_hugging_face_hack.html`

All four now carry the standard `G-L3WZNV09BB` gtag block plus GTM.

**Separate issue to look at:** `openai_hugging_face_hack.html` sits alongside `index.html` in the same folder and appears to be a leftover duplicate of the same article, with no canonical tag. If it's reachable it competes with the real article in search. Consider deleting it or adding `<link rel="canonical" href="https://ai-sustained.com/articles/openai-hugging-face-hack/">`.

---

## 3. The hard rule

**Do not add a GA4 tag inside GTM-K3HFQT6S.** GA4 `G-L3WZNV09BB` is hardcoded on every page; a GA4 tag in the container double-counts every pageview.

Container is for Meta pixel, TikTok pixel, Microsoft Clarity, consent management.

---

## 4. Verification already done

| Check | Result |
|---|---|
| Head snippet count per page | Exactly 1 on all 35 |
| Noscript count per page | Exactly 1 on all 35 |
| GA4 present per page | Exactly 1 on all 35 |
| HTML parses cleanly | All 35 |
| Diff vs original | Only GTM/GA4 lines added, nothing else changed |
| Headless Chromium render (8 pages) | `gtm.js?id=GTM-K3HFQT6S` and `gtag/js?id=G-L3WZNV09BB` both load, `dataLayer` = 3 entries, no new JS errors |

---

## 5. Deploy (GitHub web UI)

1. `ai-sustained` repo on GitHub → **Add file → Upload files**
2. Drag the whole unzipped `gtm-deploy` **folder** onto the upload area — dragging a directory preserves folder paths, so all 35 files land correctly in one commit
3. Commit message: `Add GTM-K3HFQT6S to all pages`, commit to `main`
4. Wait for Pages to deploy (Actions tab), 1–2 minutes

Fallback if the folder drag doesn't take: upload the root file first, then navigate into each subfolder and upload individually. 13 folders, tedious — try the drag first.

---

## 6. Then publish the container

Empty and never published. Until it has a version, the snippet loads and does nothing.

1. tagmanager.google.com → **GTM-K3HFQT6S**
2. **Submit** → version name `Initial publish` → **Publish**
3. Add Microsoft Clarity via **Tags → New → Community Template Gallery → Microsoft Clarity**, All Pages trigger
   - Use a **second Clarity project** for this site. Reusing the consulting project ID blends two different audiences into one dataset.
4. **Preview** → `https://ai-sustained.com/` → confirm the tag fires

---

## 7. Pre-existing issue, not caused by this change

`articles/AI-Space-Race/index.html` throws `Chart is not defined`. Present in the untouched original too — verified by rendering both. It loads Chart.js and Plotly from CDNs which are blocked in my sandbox, so it may be fine live. Worth a glance in your browser console; nothing to do with GTM.

---

## 8. Rollback

Purely additive. Revert the commit in GitHub, or re-upload from a clean repo ZIP.
