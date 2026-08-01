#!/usr/bin/env python3
"""AI Sustained Issue 003 hero — 'the photo finish'.
Four motion streaks on a dark night track hit the finish tape level;
only the nose-ahead leader carries the single acid charge. Forest & Acid
locked palette. SVG -> PNG via cairosvg, grain + vignette via PIL.
"""
import cairosvg, random
from PIL import Image

W, H = 1920, 1080
ACID, ACID_HI = "#E8FF3A", "#F7FF9E"

S = []
S.append(f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">')
S.append('''<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#050a07"/>
  <stop offset="0.6" stop-color="#0d2018"/>
  <stop offset="1" stop-color="#1B4332"/>
</linearGradient>
<linearGradient id="track" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#101d15"/>
  <stop offset="0.12" stop-color="#0A0F0C"/>
  <stop offset="1" stop-color="#040705"/>
</linearGradient>
<radialGradient id="glowBig" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="#E8FF3A" stop-opacity="0.30"/>
  <stop offset="0.4" stop-color="#E8FF3A" stop-opacity="0.11"/>
  <stop offset="1" stop-color="#E8FF3A" stop-opacity="0"/>
</radialGradient>
<radialGradient id="glowHead" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="#F7FF9E" stop-opacity="0.75"/>
  <stop offset="0.45" stop-color="#E8FF3A" stop-opacity="0.28"/>
  <stop offset="1" stop-color="#E8FF3A" stop-opacity="0"/>
</radialGradient>
<linearGradient id="tailAcid" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#E8FF3A" stop-opacity="0"/>
  <stop offset="0.55" stop-color="#E8FF3A" stop-opacity="0.35"/>
  <stop offset="0.9" stop-color="#F0FF6E" stop-opacity="0.9"/>
  <stop offset="1" stop-color="#F7FF9E"/>
</linearGradient>
<linearGradient id="tailCream1" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#F2ECD9" stop-opacity="0"/>
  <stop offset="0.55" stop-color="#F2ECD9" stop-opacity="0.16"/>
  <stop offset="0.9" stop-color="#F2ECD9" stop-opacity="0.55"/>
  <stop offset="1" stop-color="#F2ECD9" stop-opacity="0.8"/>
</linearGradient>
<linearGradient id="tailCream2" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#d9d2ba" stop-opacity="0"/>
  <stop offset="0.55" stop-color="#d9d2ba" stop-opacity="0.13"/>
  <stop offset="0.9" stop-color="#d9d2ba" stop-opacity="0.45"/>
  <stop offset="1" stop-color="#e4ddc6" stop-opacity="0.7"/>
</linearGradient>
<linearGradient id="tailSage" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#9DB8A8" stop-opacity="0"/>
  <stop offset="0.55" stop-color="#9DB8A8" stop-opacity="0.12"/>
  <stop offset="0.9" stop-color="#9DB8A8" stop-opacity="0.4"/>
  <stop offset="1" stop-color="#b9cfc0" stop-opacity="0.65"/>
</linearGradient>
<radialGradient id="vign" cx="0.5" cy="0.46" r="0.78">
  <stop offset="0" stop-color="#000000" stop-opacity="0"/>
  <stop offset="0.6" stop-color="#000000" stop-opacity="0"/>
  <stop offset="1" stop-color="#000000" stop-opacity="0.58"/>
</radialGradient>
<radialGradient id="poolAcid" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="#E8FF3A" stop-opacity="0.16"/>
  <stop offset="1" stop-color="#E8FF3A" stop-opacity="0"/>
</radialGradient>
</defs>''')

# ---- sky & track ----
S.append(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')
TRACK_Y = 560
S.append(f'<rect x="0" y="{TRACK_Y}" width="{W}" height="{H-TRACK_Y}" fill="url(#track)"/>')
S.append(f'<rect x="0" y="{TRACK_Y-2}" width="{W}" height="3" fill="#2a4a38" opacity="0.5"/>')

# lane dividers (5 lines -> 4 lanes), perspective-ish spacing widening toward viewer
lane_ys = [600, 700, 810, 930, 1060]
for y in lane_ys:
    S.append(f'<rect x="0" y="{y}" width="{W}" height="2" fill="#F2ECD9" opacity="0.10"/>')
    # dashed centre hint
# lane centres
lanes = [(lane_ys[i]+lane_ys[i+1])//2 for i in range(4)]

# ---- finish post + tape ----
FX = 1560
# ambient glow at the finish
S.append(f'<ellipse cx="{FX}" cy="760" rx="560" ry="430" fill="url(#glowBig)"/>')
# posts (near + far for depth)
S.append(f'<rect x="{FX+16}" y="470" width="14" height="130" rx="4" fill="#0d130e"/>')
S.append(f'<rect x="{FX+16}" y="470" width="14" height="130" rx="4" fill="none" stroke="#22402f" stroke-width="2"/>')
S.append(f'<rect x="{FX-2}" y="540" width="22" height="{H-540}" rx="6" fill="#0a0f0c"/>')
S.append(f'<rect x="{FX-2}" y="540" width="4" height="{H-540}" fill="{ACID}" opacity="0.5"/>')
# the tape: bows forward at the acid lane (lane index 1)
tape_top, tape_bow_y = 585, lanes[1]
S.append(f'<path d="M {FX+8} {tape_top} L {FX+8} {tape_bow_y-40} Q {FX-70} {tape_bow_y} {FX+8} {tape_bow_y+40} L {FX+8} {H}" '
         f'fill="none" stroke="#F2ECD9" stroke-width="7" opacity="0.85"/>')
S.append(f'<path d="M {FX+8} {tape_top} L {FX+8} {tape_bow_y-40} Q {FX-70} {tape_bow_y} {FX+8} {tape_bow_y+40} L {FX+8} {H}" '
         f'fill="none" stroke="#ffffff" stroke-width="2" opacity="0.35"/>')

# ---- the four streaks: heads nearly level; only lane 2 is acid ----
def streak(cy, head_x, h, tail, grad, head_fill, head_stroke_op, blur_ticks, seed):
    out = []
    rnd = random.Random(seed)
    # tail
    out.append(f'<rect x="{head_x-tail}" y="{cy-h/2}" width="{tail}" height="{h}" rx="{h/2}" fill="url(#{grad})"/>')
    # speed ticks behind
    for _ in range(blur_ticks):
        tx = head_x - tail*rnd.uniform(0.15, 0.95)
        ty = cy + rnd.uniform(-h*0.9, h*0.9)
        tw = rnd.uniform(30, 120)
        out.append(f'<rect x="{tx-tw}" y="{ty}" width="{tw:.0f}" height="3" rx="1.5" fill="{head_fill}" opacity="{rnd.uniform(0.06,0.2):.2f}"/>')
    # head capsule
    out.append(f'<ellipse cx="{head_x}" cy="{cy}" rx="{h*0.62}" ry="{h*0.52}" fill="{head_fill}" opacity="{head_stroke_op}"/>')
    return "\n".join(out)

# dim rivals (cream, cream2, sage) — level within a nose
S.append(streak(lanes[0], FX-34, 34, 640, "tailCream1", "#F2ECD9", 0.85, 7, 21))
S.append(streak(lanes[2], FX-52, 38, 700, "tailCream2", "#e4ddc6", 0.75, 7, 22))
S.append(streak(lanes[3], FX-44, 42, 620, "tailSage",  "#b9cfc0", 0.7, 7, 23))
# the acid leader — nose past the others, breaking the tape
S.append(f'<ellipse cx="{FX-10}" cy="{lanes[1]}" rx="330" ry="120" fill="url(#glowHead)"/>')
S.append(streak(lanes[1], FX+6, 44, 860, "tailAcid", ACID, 1.0, 10, 24))
S.append(f'<ellipse cx="{FX+6}" cy="{lanes[1]}" rx="20" ry="17" fill="{ACID_HI}"/>')
# light pool under the leader
S.append(f'<ellipse cx="{FX-160}" cy="{lanes[1]+64}" rx="420" ry="60" fill="url(#poolAcid)"/>')

# ---- dust motes in the finish glow ----
rnd = random.Random(9)
for _ in range(24):
    mx = rnd.uniform(1150, 1780); my = rnd.uniform(340, 900)
    r = rnd.uniform(1.2, 3.2); o = rnd.uniform(0.1, 0.45)
    S.append(f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="{r:.1f}" fill="{ACID_HI}" opacity="{o:.2f}"/>')

# ---- vignette ----
S.append(f'<rect width="{W}" height="{H}" fill="url(#vign)"/>')
S.append('</svg>')

svg = "\n".join(S)
open("four-labs-seven-days_hero.svg","w").write(svg)
cairosvg.svg2png(bytestring=svg.encode(), write_to="hero_raw.png", output_width=W, output_height=H)

img = Image.open("hero_raw.png").convert("RGB")
grain = Image.effect_noise((W, H), 26).convert("L")
img = Image.composite(
    Image.blend(img, Image.new("RGB", (W,H), (255,255,255)), 0.05),
    Image.blend(img, Image.new("RGB", (W,H), (0,0,0)), 0.05),
    grain)
img.save("four-labs-seven-days_hero.png", optimize=True)
img.resize((1200, 675), Image.LANCZOS).save("four-labs-seven-days_card.png", optimize=True)
print("done", img.size)
