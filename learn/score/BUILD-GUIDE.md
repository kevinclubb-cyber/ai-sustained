# Quiz League Rank — Build Guide

Goal: after someone finishes the quiz on ai-sustained.com/learn, show
"You scored higher than X% of participants — rank N of M."

How it works: a GitHub Action pulls all scores from HubSpot every 6 hours,
publishes an anonymous `scores.json` to your GitHub Pages site, and the quiz
page computes the percentile in the browser. No backend, no exposed secrets.

---

## Step 1 — HubSpot private app (one-off, ~5 min)

1. HubSpot > Settings (cog) > Integrations > **Private Apps** > Create private app
2. Name it `quiz-scores-reader`
3. Scopes tab: tick **crm.objects.contacts.read** only (least privilege)
4. Create app > copy the access token (starts `pat-...`). You won't see it again.

## Step 2 — Confirm the score property internal name

1. HubSpot > Settings > Properties > search "AI Survival Score"
2. Note the **internal name** (likely `ai_survival_score`, but confirm)
3. If different, edit line 7 of `fetch-scores.mjs` (`SCORE_PROPERTY`)

## Step 3 — Add the token to GitHub

1. GitHub repo > Settings > Secrets and variables > Actions > **New repository secret**
2. Name: `HUBSPOT_TOKEN`, value: the token from Step 1

## Step 4 — Add the files to the repo

- `update-scores.yml` → `.github/workflows/update-scores.yml`
- `fetch-scores.mjs` → `scripts/fetch-scores.mjs`

Commit and push.

## Step 5 — Test the Action

1. Repo > Actions tab > "Update AI Survival Scores" > **Run workflow**
2. Green run = a `scores.json` appears at the repo root
3. Once Pages redeploys, check `https://ai-sustained.com/scores.json` loads
   (if your site publishes from a subfolder e.g. `/docs`, move the output path
   in `fetch-scores.mjs` accordingly — ask me)

## Step 6 — Wire up the quiz page

1. Add `<div id="rank-result"></div>` to the results section
2. Add `percentile-snippet.js` (inline or as a file)
3. Call `showRank(userScore)` at the point where the score is displayed

## Step 7 — Verify

- Take the quiz yourself, check the rank line appears and looks sane
- Sanity-check: `scores.json` count should roughly match your HubSpot submissions

---

## Notes

- `scores.json` is public but contains **numbers only** — no emails, no PII
- Snippet hides itself below 10 total scores and if scores.json fails — it can never break the results page
- Rank is up to 6 hours stale; the just-submitted score is counted as the "+1" in "of M"
- HubSpot search API caps at 10,000 results — a problem you'd be happy to have; flag it to me if you get near
- Cron is UTC; timing precision doesn't matter here
