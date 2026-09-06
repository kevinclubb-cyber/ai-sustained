# Issue 019 image prompts (Gemini)

Four images. One hero for the site article, three for the Substack edition. All 16:9. Paste each prompt as written; Gemini takes the "Avoid" line as part of the prompt rather than a separate negative field. If a render drifts teal or adds lettering, re-run with "Strictly no text anywhere in the image" appended.

House rules baked into every prompt: forest green and near-black carry the frame, cream for light surfaces, exactly one acid-lime charge, no text, no robots, no glowing brains, negative space in the upper third.

---

## 1. Hero (site article and index card)

File: `fable-5-1-vs-gpt-6-astra_hero.png`, 1920x1080. Then derive `cover.png` at 1200x675.

Idea: the signed page and the hand that wants to drive. A sheet of paper with a mouse resting on it as a paperweight; the acid light leaks from under the mouse into the paper's grain like ink that should not be there.

```
Cinematic editorial photograph, 16:9. A single sheet of cream paper lying on a long dark wooden desk in a quiet office at night. A wired computer mouse rests on the paper like a paperweight, its cable trailing off the edge of the desk. A thin electric acid-lime glow leaks from beneath the mouse and soaks into the fibres of the paper, as if the paper itself is faintly lit from within around the mouse. Behind the desk an empty office chair is pushed back at an angle. Venetian blinds half drawn, the room otherwise dark. Shallow depth of field focused on the mouse and paper, physically plausible lighting with the glow under the mouse as the single dominant light source, fine film grain, muted contrast in the shadows, composed and still, generous empty space in the upper third of the frame. Colour palette locked to deep forest green (#1B4332) and near-black (#0A0F0C) as the dominant tones, warm cream (#F2ECD9) for the paper, and exactly one accent of electric acid-lime (#E8FF3A) for the glow. No teal, cyan, magenta, purple or orange anywhere. Avoid: any writing or lettering on the paper, visible screen content, robots, robot hands, human hands, circuit boards, glowing brains, holographic interfaces, lens flare, teal-and-orange grading, logos, watermarks, clutter.
```

Alt text (already in the HTML): A single sheet of cream paper on a dark desk at night with a wired computer mouse resting on it like a paperweight, acid-green light bleeding from under the mouse into the grain of the paper, an empty chair pushed back behind.

---

## 2. Substack image A: the mark

Place after the section "The mark: how it works and where it fails". 1456x816 or any 16:9.

Idea: the signature you cannot see. A fountain pen nib lifted a centimetre off cream paper, and instead of ink, a faint acid stain spreading through the fibres where it touched.

```
Cinematic editorial macro photograph, 16:9. A fountain pen nib held a centimetre above a sheet of heavy cream paper on a dark desk, photographed from low and close. Where the nib last touched, a faint electric acid-lime stain is spreading outward through the fibres of the paper like ink in blotting paper, glowing very softly, the only light in the frame. The rest of the desk falls away into deep forest-green darkness. Extremely shallow depth of field, the paper grain and the stain in sharp focus, the pen barrel softening into the dark. Film grain, muted shadow contrast, composed and still, empty space in the upper third. Colour palette locked to deep forest green (#1B4332) and near-black (#0A0F0C) dominant, warm cream (#F2ECD9) for the paper, exactly one accent of electric acid-lime (#E8FF3A) for the stain. No teal, cyan, magenta, purple or orange. Avoid: any writing, letters, signatures or symbols on the paper, hands, robots, circuit boards, glowing brains, holographic effects, lens flare, logos, watermarks, clutter.
```

Suggested caption: The mark is in the words, not around them. You cannot see it, and you are not on the list of people who can.

---

## 3. Substack image B: the meter

Place after the section "The plan: who actually gets the best model". 16:9.

Idea: credit that runs out before you have started. A vintage coin-slot electricity meter on a dark wall, its needle resting on empty, a single acid light in its small glass window.

```
Cinematic editorial photograph, 16:9. An old British coin-operated electricity meter, cast iron and black enamel, mounted on a wall painted deep forest green, photographed straight on at eye level in a dim hallway. Its round analogue dial shows the needle resting all the way at the empty end. The only light in the frame is a small electric acid-lime glow behind the meter's little glass inspection window, catching the edge of the coin slot. Everything else falls into near-black shadow. Shallow depth of field, physically plausible lighting, film grain, muted shadow contrast, composed and still, empty wall space in the upper third. Colour palette locked to deep forest green (#1B4332) and near-black (#0A0F0C) dominant, warm cream (#F2ECD9) for the dial face, exactly one accent of electric acid-lime (#E8FF3A) for the window glow. No teal, cyan, magenta, purple or orange. Avoid: any numbers, letters or brand names on the dial or casing, coins, hands, robots, circuit boards, glowing brains, holographic effects, lens flare, logos, watermarks, clutter.
```

Suggested caption: On the menu is not the same as on the table. Ten prompts at High, five hours of credit, gone in three minutes.

---

## 4. Substack image C: hidden reasoning

Place after the section "The part that should worry you, with the mechanism". 16:9.

Idea: reasoning that loops where you cannot follow. A spiral staircase seen from directly above, turning down into darkness, one acid light on the lowest landing that the eye cannot quite reach.

```
Cinematic editorial photograph, 16:9. A stone spiral staircase in an old building, photographed from directly above looking straight down the central well. The steps turn round and round into darkness. Far below, on the lowest landing, a single small electric acid-lime light glows, partly hidden by the curve of the stairs so you cannot see what it is lighting. The upper steps are lit only faintly by that glow from beneath. Cream-painted iron handrail catching a little of the light. Deep shadows, physically plausible lighting with the light below as the single source, film grain, muted shadow contrast, composed and still, the widest and darkest part of the spiral in the upper third of the frame. Colour palette locked to deep forest green (#1B4332) and near-black (#0A0F0C) dominant, warm cream (#F2ECD9) for the handrail and worn step edges, exactly one accent of electric acid-lime (#E8FF3A) for the light at the bottom. No teal, cyan, magenta, purple or orange. Avoid: people, hands, robots, circuit boards, glowing brains, holographic effects, text, signage, lens flare, logos, watermarks, clutter.
```

Suggested caption: Part of Astra's reasoning now runs in loops that leave no readable trace. The fewer steps you can see, the more of the answer you check.

---

## After generation

- Hero: save as `articles/fable-5-1-vs-gpt-6-astra/fable-5-1-vs-gpt-6-astra_hero.png`, run `derive_card.py`, rename the output to `cover.png`. pngquant at `--quality=82-98` roughly halves the file with no visible loss on this palette.
- Substack images: upload through the Substack editor at the section breaks above. Substack renders 1456px wide; anything larger is downscaled.
- Check each render for stray lettering before use. Gemini likes to put numbers on dials and words on paper even when told not to.
