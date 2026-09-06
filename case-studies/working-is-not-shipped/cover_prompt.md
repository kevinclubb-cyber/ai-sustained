# Cover art prompt · Case Study 006 · `working-is-not-shipped`

Output: a 1920x1080 source image. Run the prompt in Gemini, Midjourney or your usual tool. No stock, no clip art.

**Save the source anywhere, then hand Claude the path.** The house convention is not a raw `cover.png` in the repo — three derived files are generated from the one source and the HTML already points at them:

| File | Used by | Recipe |
|---|---|---|
| `cover.webp` | the page `<img>` | `cwebp -q 82` |
| `cover.jpg` | `og:image`, `twitter:image`, JSON-LD | `sips -Z 1200 -s format jpeg -s formatOptions 82` |
| `tile.webp` | the homepage carousel card | copy of `cover.webp` |

WebP for the page because it is 10-30x smaller; JPEG for social because scrapers handle WebP unreliably; 1200px on the social image because that is ample for every scraper.

## Prompt

Editorial photograph, cinematic and quiet. A dark desk at night lit by a single warm desk lamp. In the centre, a thick stack of printed source code, a few hundred pages, slightly fanned, held with a black bulldog clip. Beside it an open deep forest-green ring binder with the word REVIEW embossed on the spine in small capitals. One printed page has been pulled out and laid on top of the stack; a single line on it is marked with a thick acid-yellow highlighter stroke, the only bright colour in the frame. A capped fountain pen rests across the binder. Laptop closed in the background, screen dark, its edge catching the lamp light. Shallow depth of field, focus on the highlighted line. Colour palette: deep forest green #1B4332 shadows, warm cream #F2ECD9 paper, one acid-lime #E8FF3A accent. Matte textures, film grain, slightly desaturated except the highlighter. Composition leaves the upper third calm and dark for a headline overlay. Photorealistic, 35mm, f/2.

## Negative prompt

no people, no hands, no faces, no screens with visible code or UI, no glowing neon, no circuit boards, no robots, no holograms, no blue light, no purple, no gradients, no text other than the single word REVIEW, no watermark, no logos, no clip art, no 3D render look.

## Alt text (already in the HTML)

A single desk lamp lighting a stack of printed code, a green ring binder marked Review open beside it, one page pulled out and marked in acid-yellow highlighter.

## Card

The `/case-studies/` index card uses `cover.webp` directly, and the homepage carousel uses `tile.webp`. No separate crop and no added text — the existing tiles use the cover art as-is.
