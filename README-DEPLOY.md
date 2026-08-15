# ai-sustained.com — consent deploy, rev B, 15 August 2026

**35 HTML files. Editorial site only.** Nothing here touches the consulting site.

> **This supersedes the consent files in the earlier combined package.** That version had
> two bugs, found after you deployed it. Deploy this over the top.

---

## 1. What rev B fixes

Both bugs were in the reopen path, so they only bit people who clicked **Cookie choices** after already making a decision.

**Bug 1 — the panel lied.** Reopening always rendered the toggles at their defaults, all off, regardless of what the visitor had actually chosen. Someone who accepted everything and came back to check would see four switches off and reasonably conclude nothing had been accepted.

**Bug 2 — reopening silently revoked consent.** The reopen handler cleared the stored decision before rebuilding the banner. Look at your settings, close the tab without choosing again, and you were back to fully denied having never asked to be. A consent tool that revokes consent because you glanced at it is worse than not having one.

Now:

- The panel reflects the visitor's actual saved state
- Reopening jumps straight to the detail view, so current choices are visible immediately
- Nothing is ever revoked except by an explicit choice

**The underlying consent signals were correct throughout** — Accept all really did grant everything, and it was stored properly. Only the UI and the reopen path were wrong. No visitor was ever tracked without consent.

---

## 2. What is in the package

All 35 tagged pages, each carrying: consent block → GA4 `G-L3WZNV09BB` → GTM `GTM-K3HFQT6S`, in that order.

Includes the **updated privacy notice** at `privacy/index.html`. The old text claimed *"no advertising or cross-site tracking cookies are used"* and never mentioned Microsoft Clarity — inaccurate from the moment session recording went live. Rewritten to cover consent-first behaviour, Clarity, the pixel position and legal basis.

Not included, deliberately: `article-score-cta-snippet.html` and `privacy-learn-section.html` (HTML fragments with no `<head>`), and the three LinkedIn image-source files in `articles/openai-hugging-face-hack/`.

---

## 3. Upload

1. `ai-sustained` repo → **Add file → Upload files**
2. Drag the whole `editorial-deploy` **folder** in — dragging a directory preserves paths, so all 35 land correctly in one commit
3. Commit message: `Consent banner rev B, updated privacy notice`
4. Commit to `main`

**Check the commit says 35 files changed.** Fewer means the folder drag half-took — the same failure that left your consulting root pages behind last time. Fallback: upload the one root file first, then go into each of the 12 folders individually.

---

## 4. Purge Cloudflare

Caching → Configuration → **Purge Everything**.

---

## 5. Then GTM — still outstanding on this container

Consent Mode blocks Google's own tags automatically. It does **not** block Microsoft Clarity, which is a third-party template.

1. tagmanager.google.com → **GTM-K3HFQT6S**
2. **Tags** → **Microsoft Clarity**
3. **Advanced Settings** → **Consent Settings**
4. **Require additional consent for tag to fire**
5. Consent type: `functionality_storage`
6. **Save** → **Submit** → `Clarity behind consent` → **Publish**

Until this is published, session recording runs on visitors who declined it while the privacy notice promises otherwise.

---

## 6. Verify

Private window, every time.

1. `https://ai-sustained.com/` — banner appears
2. Footer shows **· Privacy · Cookie choices**
3. DevTools → Network → filter `clarity`
4. **Reject all** → no request to `clarity.ms`, ever
5. Fresh private window → **Accept all** → `clarity.ms` appears
6. Click footer **Cookie choices** → panel opens with **all four toggles on**. This is the rev B fix. If they show off, the old file is still cached — purge again.

---

## 7. Verification already done on this build

Rendered in headless Chromium across eight pages covering all four of your footer templates (`footer-left`, `brand-footer`, the bare `<span>` footer on `/learn/score/`, and the article variant):

| Check | Result |
|---|---|
| Banner appears | Pass, 8/8 |
| Consent default reaches dataLayer before `gtm.start` | Pass, 8/8 |
| Footer links inject on every footer variant | Pass, 8/8 |
| Privacy link suppressed on `/privacy/` | Pass |
| Accept all → reopen shows all four toggles on | Pass |
| Storage preserved across reopen | Pass |
| Old revoke-on-reopen code present anywhere | None — 0 files |
| All 35 carry GA4 and GTM exactly once | Pass |
| HTML parses cleanly | Pass |
| JavaScript errors introduced | None |
