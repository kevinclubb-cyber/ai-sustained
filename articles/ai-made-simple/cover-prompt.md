# Hero-image prompts — Issue 013 · AI Made Simple

The shipped `cover.png` is a clean vector hero (an empty AI prompt box with a blinking acid cursor and an acid send button, on a deep forest ground, headline "AI, Made Simple." with "Simple." as the Fraunces-italic acid accent). If you'd rather a photoreal / painterly hero from Gemini or another image model, use the prompts below.

Square 1:1. Brand palette: deep forest green `#1B4332`, neon acid-yellow `#E8FF3A`, warm cream `#F2ECD9`, soft mint `#D8F3DC`, coral `#FF8C61`. Keep the upper third clear for a headline overlay.

---

## PRIMARY PROMPT (the empty box)

> A bold, minimal editorial conceptual cover, perfect 1:1 square, about ordinary people freezing in front of an AI chatbot. Centre of frame: a single large, empty text-input box rendered as a clean rounded rectangle with a thin glowing acid-yellow (#E8FF3A) outline, floating on a deep forest-green (#1B4332) void. Inside the box, one lonely blinking acid cursor and nothing else, capturing the "what do I even type" moment. Faint cream (#F2ECD9) placeholder shimmer. A soft volumetric glow pools under the box. Lots of calm negative space above for a headline. High contrast, cinematic, premium tech-magazine aesthetic, flat-meets-3D hybrid illustration, subtle film grain. Mood: quietly intimidating but solvable. No words, no letters, no logos, no readable UI labels. Square aspect ratio 1:1.

---

## ALT A — "the on-ramp" (one boring job)

> A striking 1:1 square editorial illustration about starting small with AI. A single dull grey office object (a stack of paper, a spreadsheet grid, an unread email envelope) rendered in muted cream (#F2ECD9), being lifted and transformed into a clean stream of acid-yellow (#E8FF3A) light as it passes through a simple glowing portal on a deep forest-green (#1B4332) background. Minimal, high-contrast, cinematic, generous dark negative space at the top for a headline. No text, no letters, no logos. Square 1:1.

---

## ALT B — "draft, then iterate"

> A minimal, powerful 1:1 square editorial cover about refining AI output. Three stacked horizontal cards on a deep forest-green (#1B4332) field, the lowest dim cream (#F2ECD9), the middle brighter, the top glowing full acid-yellow (#E8FF3A), suggesting a rough draft improving through iteration. Thin coral (#FF8C61) arrows loop from the top card back down, implying "argue with it and go again". Clean, restrained, premium poster design, negative space up top. No text, no letters, no logos. Square 1:1.

---

## NEGATIVE PROMPT

> text, words, letters, numbers, captions, watermark, logo, brand marks, low resolution, blurry, cluttered, busy, cartoonish, childish, stock-photo people, faces, hands, distorted geometry, oversaturated rainbow colours, neon pink, purple, blue dominance, robots, glowing brains, humanoid AI clichés

---

## Tips

- **Add the headline after.** Generate clean, then overlay "AI made simple." in Space Grotesk with an acid-yellow Fraunces-italic accent on "Simple.", upper-third negative space.
- **Palette lock:** if colours drift, append *"strictly limited colour palette: forest green, acid yellow, cream, coral only."*
- **Note on the shipped file:** the current `cover.png` was drawn as a vector in the sandbox using Poppins/Lora as stand-ins for Space Grotesk/Fraunces (the brand fonts and the headless renderer weren't available). For a final version, re-render with the real brand fonts or generate from a prompt above.
