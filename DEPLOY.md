# AI Made Simple — Deployment Pack
Repo: `kevinclubb-cyber/ai-sustained` · Built 18 Jul 2026

All HTML files are **pure ASCII** — every special character is an HTML entity (or `\uXXXX` in JS), so the `â€"` corruption cannot recur no matter what editor or clipboard touches them.

## File map

| File in this pack | Commit to |
|---|---|
| `learn/index.html` | `learn/index.html` (replace) |
| `learn/score/index.html` | `learn/score/index.html` (replace) |
| `learn/programme/index.html` | `learn/programme/index.html` (replace) |
| `learn/terms/index.html` | `learn/terms/index.html` (new) |
| `advertise/index.html` | `advertise/index.html` (new) |
| `privacy/index.html` | `privacy/index.html` | Replace |

## What changed vs live

**/learn** — "Three rungs" → "Four rungs"; FAQ section + FAQPage schema; "For teams" bridge to consulting (UTM-tagged); "Not ready" band now captures subscribers instead of leaking to the editorial; hygiene footer; ChatGPT/Claude/Gemini naming in hero, pillar 3, FAQ and meta.

**/learn/score/** — GDPR-safe gate note with privacy link (old wording contradicted the weekly emails); `legalConsentOptions` recorded in HubSpot payload; weakest pillar sent as `ai_weakest_pillar`; booking link pre-filled with name+email; share URLs UTM-tagged (`survival_score_share`); `quiz_progress` GA event per question; hygiene footer; ChatGPT/Claude/Gemini named in Q8.

**/learn/programme/** — hygiene footer; small-print now names payment + links terms; "For teams" bridge; tool names woven into "why now" copy.

**New pages** — `/learn/terms/` (plain-English T&Cs incl. 14-day cooling-off) and `/advertise/` (open-to-partners page, honest early-stage framing, zero invented numbers).

**/privacy/** — full replacement: masthead now carries the logo mark + wordmark and a Learn nav link; contact email is kevin@ai-sustained.com; "The newsletter" section is now "Email subscription" covering new editorials, case studies, updates, promotions and new products; Survival Score, booking and advertising sections merged in; footer links Terms + Advertising.

## Before you push — 4 TODOs

1. **`HS_SUBSCRIPTION_TYPE_ID = 999`** in `learn/score/index.html` — replace with your real ID (HubSpot: Settings → Marketing → Email → Subscription types). Harmless if wrong: the code falls back to a core-fields submit, but consent then isn't recorded.
2. **HubSpot property** — create `ai_weakest_pillar` (single-line text, contact property). Same fallback applies until it exists.
3. **Email** — all pages now use kevin@ai-sustained.com. Make sure that mailbox exists (Cloudflare Email Routing to your real inbox does the job).
4. **Terms** = plain-English draft, not legal advice. Sanity-check the cooling-off wording (Consumer Contracts Regulations 2013) before taking payments.

## After deploy — quick smoke test

Take the quiz with a test email → check the contact lands in HubSpot with score, tier, weakest pillar and consent → click the booking button and confirm name/email pre-fill → check GA4 DebugView for `quiz_progress` events.
