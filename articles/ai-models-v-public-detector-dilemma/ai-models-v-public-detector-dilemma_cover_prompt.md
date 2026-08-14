# Issue 017a — hero cover prompt

**Target file:** `ai-models-v-public-detector-dilemma_hero.png`
**Size:** 1920 x 1080 (16:9). Generate at this ratio. Do not generate the card separately, downscale the hero to 1200 x 675.

## The five decisions

| Decision | Call |
|---|---|
| Subject | A cylinder head with a row of identical bolts, one of them lit from inside its socket. Not "the concept of watermarking" |
| Moment | The instant after the bonnet is lifted, before anyone touches anything |
| Scale cue | A torque wrench laid across the head, and the bonnet strut at the top edge |
| Palette | Forest and near-black carry it. One acid charge, doing structural work as the only light source |
| Must not look like | The negative list below |

## Prompt

```
A cylinder head inside a just-opened engine bay, photographed close and slightly
from above, a straight row of identical hexagonal bolt heads running across it.
One bolt in that row is seated differently to the others and acid-green light is
coming up out of its socket, the only light source in the frame. A torque wrench
lies across the head, unattended. The bonnet strut cuts the top edge of the shot.
Cinematic editorial photography, shallow depth of field, high fidelity, physically
plausible lighting, single dominant light source, film grain, muted contrast in
the shadows, 16:9, negative space in the upper third for a headline overlay.
Colour palette locked to deep forest green (#1B4332) and near-black (#0A0F0C) as
the dominant tones, with warm cream (#F2ECD9) for any light surfaces or metal
highlights, and exactly one accent of electric acid-lime (#E8FF3A) used sparingly
as the light coming out of the single socket. No teal, no cyan, no magenta, no
purple, no orange. Composed and still, not chaotic. Oil and grime present but the
frame is orderly.
```

## Negative prompt

```
No glowing blue brains, no circuit-board motifs, no humanoid robots, no binary
digit rain, no neural-network node diagrams, no floating holographic UI, no lens
flare, no teal-and-orange grade, no stock-photo handshake, no text, no watermarks,
no logos, no distorted hands or faces, no crowded composition, no neon cyberpunk
city, no honeycomb or beehive reading, no glowing hexagon grid.
```

The last two exclusions are deliberate. A field of lit hexagons drifts into honeycomb, which is the wrong story entirely.

## Alt text (already set in index.html, keep it matched to the final frame)

> A cylinder head under a just-opened bonnet, a row of identical bolt heads across it, acid-green light coming out of one socket, a torque wrench laid across the metal.

## Notes

If the generator will not give you a single bolt lit from inside, the acceptable fallbacks in order are: light spilling from the gap where one bolt is missing; a socket sitting alone beside the row with the light in it; a fault-code glow on a diagnostic screen reflected in the metal. Do not accept a version where the acid appears in more than one place.

If Gemini stamps its visible diamond watermark bottom right, leave it. Issue 017 made a point of that, and 017a is a Gemini piece, so it is consistent rather than sloppy.
