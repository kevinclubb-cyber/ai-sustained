#!/usr/bin/env python3
"""AI Sustained Issue 002 hero — 'the paste moment'.
A cream document, half-fed into a glowing acid slot on a dark desk;
a messy stack waits its turn. Forest & Acid locked palette, one light source.
Rendered SVG -> PNG via cairosvg, film grain + vignette via PIL.
"""
import cairosvg, math, random
from PIL import Image, ImageDraw

W, H = 1920, 1080
FOREST, INK = "#1B4332", "#0A0F0C"
CREAM, CREAM2 = "#F2ECD9", "#E4DCC4"
ACID, ACID_HI = "#E8FF3A", "#F7FF9E"

def textlines(x, y, w, n, rot, lh=26, color="#0A0F0C", op=0.35, seed=1):
    """Abstract text bars on a sheet (no real glyphs)."""
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        lw = w * rnd.uniform(0.55, 0.96)
        out.append(f'<rect x="{x}" y="{y + i*lh}" width="{lw:.0f}" height="9" rx="4.5" '
                   f'fill="{color}" opacity="{op}" transform="{rot}"/>')
    return "\n".join(out)

S = []
S.append(f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">')
S.append('''<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#06100b"/>
  <stop offset="0.55" stop-color="#0f231a"/>
  <stop offset="1" stop-color="#1B4332"/>
</linearGradient>
<linearGradient id="desk" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#0d1811"/>
  <stop offset="0.08" stop-color="#0A0F0C"/>
  <stop offset="1" stop-color="#050805"/>
</linearGradient>
<radialGradient id="glowBig" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="#E8FF3A" stop-opacity="0.32"/>
  <stop offset="0.35" stop-color="#E8FF3A" stop-opacity="0.13"/>
  <stop offset="1" stop-color="#E8FF3A" stop-opacity="0"/>
</radialGradient>
<radialGradient id="glowMid" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="#F7FF9E" stop-opacity="0.55"/>
  <stop offset="0.4" stop-color="#E8FF3A" stop-opacity="0.22"/>
  <stop offset="1" stop-color="#E8FF3A" stop-opacity="0"/>
</radialGradient>
<linearGradient id="slotCore" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#E8FF3A" stop-opacity="0"/>
  <stop offset="0.12" stop-color="#E8FF3A" stop-opacity="0.9"/>
  <stop offset="0.5" stop-color="#F7FF9E"/>
  <stop offset="0.88" stop-color="#E8FF3A" stop-opacity="0.9"/>
  <stop offset="1" stop-color="#E8FF3A" stop-opacity="0"/>
</linearGradient>
<linearGradient id="sheet" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#F2ECD9"/>
  <stop offset="0.75" stop-color="#EBE3CC"/>
  <stop offset="1" stop-color="#F7F3E4"/>
</linearGradient>
<linearGradient id="sheetLit" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#F2ECD9" stop-opacity="0"/>
  <stop offset="0.72" stop-color="#EFFF9C" stop-opacity="0.15"/>
  <stop offset="1" stop-color="#E8FF3A" stop-opacity="0.55"/>
</linearGradient>
<linearGradient id="deviceFace" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#15291e"/>
  <stop offset="0.5" stop-color="#0c1710"/>
  <stop offset="1" stop-color="#070c09"/>
</linearGradient>
<linearGradient id="deviceTop" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#22402f"/>
  <stop offset="1" stop-color="#132419"/>
</linearGradient>
<radialGradient id="vign" cx="0.5" cy="0.46" r="0.75">
  <stop offset="0" stop-color="#000000" stop-opacity="0"/>
  <stop offset="0.62" stop-color="#000000" stop-opacity="0"/>
  <stop offset="1" stop-color="#000000" stop-opacity="0.55"/>
</radialGradient>
<radialGradient id="deskPool" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="#E8FF3A" stop-opacity="0.20"/>
  <stop offset="0.5" stop-color="#E8FF3A" stop-opacity="0.07"/>
  <stop offset="1" stop-color="#E8FF3A" stop-opacity="0"/>
</radialGradient>
</defs>''')

# ---- background & desk ----
S.append(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')
DESK_Y = 700
S.append(f'<rect x="0" y="{DESK_Y}" width="{W}" height="{H-DESK_Y}" fill="url(#desk)"/>')
# faint horizon line of desk edge
S.append(f'<rect x="0" y="{DESK_Y-2}" width="{W}" height="3" fill="#2a4a38" opacity="0.55"/>')

# ---- ambient glow behind device (single light source) ----
S.append(f'<ellipse cx="1210" cy="655" rx="640" ry="420" fill="url(#glowBig)"/>')
# light pool on desk
S.append(f'<ellipse cx="1195" cy="742" rx="480" ry="95" fill="url(#deskPool)"/>')

# ---- waiting stack, left, in half-shadow ----
stack = [
    (300, 728, 320, 216, -7,  "#c9c2ab", 0.92),
    (322, 716, 316, 212, 4,   "#d6cfb6", 0.95),
    (295, 702, 330, 220, -3,  "#e0d9c0", 0.97),
    (318, 688, 322, 214, 2,   "#EBE4CC", 1.0),
]
for i,(x,y,w,h,ang,col,op) in enumerate(stack):
    rot = f'rotate({ang} {x+w/2} {y+h/2})'
    S.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{col}" opacity="{op}" transform="{rot}"/>')
    if i == len(stack)-1:
        S.append(textlines(x+26, y+30, w-60, 6, rot, lh=27, op=0.28, seed=7))
# soft shadow under the stack
S.append(f'<ellipse cx="470" cy="905" rx="270" ry="26" fill="#000000" opacity="0.4"/>')
# paperclips (cream strokes) near stack — scale cue
for (cx,cy,ang) in [(690,880,18),(722,904,-31)]:
    S.append(f'<g transform="translate({cx} {cy}) rotate({ang})" opacity="0.8">'
             f'<rect x="-3" y="-26" width="6" height="52" rx="3" fill="none" stroke="#d6cfb6" stroke-width="4"/>'
             f'<rect x="-3" y="-16" width="6" height="32" rx="3" fill="none" stroke="#d6cfb6" stroke-width="3" opacity="0.7"/></g>')

# ---- the device: low slab with a glowing intake slot ----
DX, DW = 880, 660           # device left x, width
DTOP, DH = 596, 150         # top face y, face height
# top face (slightly lit)
S.append(f'<path d="M {DX+22} {DTOP} L {DX+DW-22} {DTOP} L {DX+DW} {DTOP+34} L {DX} {DTOP+34} Z" fill="url(#deviceTop)"/>')
# front face
S.append(f'<rect x="{DX}" y="{DTOP+34}" width="{DW}" height="{DH}" rx="10" fill="url(#deviceFace)"/>')
# acid edge along the top-front rim
S.append(f'<rect x="{DX}" y="{DTOP+32}" width="{DW}" height="3" fill="{ACID}" opacity="0.35"/>')
# slot aperture on the top face
SLX, SLW, SLY = DX+70, DW-140, DTOP+15
S.append(f'<rect x="{SLX-6}" y="{SLY-4}" width="{SLW+12}" height="22" rx="11" fill="#03130b"/>')
# slot glow layers
S.append(f'<ellipse cx="{SLX+SLW/2}" cy="{SLY+7}" rx="{SLW*0.72}" ry="60" fill="url(#glowMid)"/>')
S.append(f'<rect x="{SLX}" y="{SLY}" width="{SLW}" height="12" rx="6" fill="url(#slotCore)"/>')
S.append(f'<rect x="{SLX+SLW*0.18}" y="{SLY+3}" width="{SLW*0.64}" height="5" rx="2.5" fill="{ACID_HI}"/>')
# tiny status dot on front face
S.append(f'<circle cx="{DX+DW-46}" cy="{DTOP+34+DH-38}" r="7" fill="{ACID}" opacity="0.9"/>')
S.append(f'<circle cx="{DX+DW-46}" cy="{DTOP+34+DH-38}" r="16" fill="url(#glowMid)" opacity="0.5"/>')
# device shadow on desk
S.append(f'<ellipse cx="{DX+DW/2}" cy="{DTOP+34+DH+16}" rx="{DW*0.55}" ry="22" fill="#000000" opacity="0.5"/>')

# ---- the document, half-fed into the slot ----
# group rotated about insertion point
ix, iy = SLX+SLW*0.52, SLY+8          # insertion point on slot
ang = -24
S.append(f'<g transform="rotate({ang} {ix} {iy})">')
shw, shh = 380, 500                    # sheet size
sx, sy = ix - shw*0.52, iy - shh       # sheet above slot
# sheet shadow cast back
S.append(f'<rect x="{sx+14}" y="{sy+18}" width="{shw}" height="{shh}" rx="6" fill="#000000" opacity="0.25"/>')
S.append(f'<rect x="{sx}" y="{sy}" width="{shw}" height="{shh}" rx="6" fill="url(#sheet)"/>')
# acid light licking up the sheet from the slot
S.append(f'<rect x="{sx}" y="{sy}" width="{shw}" height="{shh}" rx="6" fill="url(#sheetLit)"/>')
# folded corner, top-right
S.append(f'<path d="M {sx+shw-64} {sy} L {sx+shw} {sy} L {sx+shw} {sy+64} Z" fill="#d9d1b8"/>')
S.append(f'<path d="M {sx+shw-64} {sy} L {sx+shw} {sy+64} L {sx+shw-64} {sy+64} Z" fill="#c4bca2" opacity="0.6"/>')
# abstract text on sheet
S.append(textlines(sx+40, sy+64, shw-84, 9, "", lh=34, op=0.4, seed=3))
# one acid-highlight line (the interesting bit being read)
S.append(f'<rect x="{sx+40}" y="{sy+64+5*34-3}" width="{(shw-84)*0.78:.0f}" height="15" rx="6" fill="{ACID}" opacity="0.5"/>')
S.append('</g>')
# occlude everything below the slot line: redraw front-of-slot top face + front face OVER the sheet
S.append(f'<path d="M {DX+10} {SLY+16} L {DX+DW-10} {SLY+16} L {DX+DW} {DTOP+34} L {DX} {DTOP+34} Z" fill="url(#deviceTop)"/>')
S.append(f'<rect x="{DX}" y="{DTOP+34}" width="{DW}" height="{DH}" rx="10" fill="url(#deviceFace)"/>')
S.append(f'<rect x="{DX}" y="{DTOP+32}" width="{DW}" height="3" fill="{ACID}" opacity="0.35"/>')
S.append(f'<circle cx="{DX+DW-46}" cy="{DTOP+34+DH-38}" r="7" fill="{ACID}" opacity="0.9"/>')
S.append(f'<circle cx="{DX+DW-46}" cy="{DTOP+34+DH-38}" r="16" fill="url(#glowMid)" opacity="0.5"/>')
# slot re-lit over the inserted paper edge
S.append(f'<rect x="{SLX+SLW*0.1}" y="{SLY+9}" width="{SLW*0.8}" height="4" rx="2" fill="{ACID}" opacity="0.9"/>')

# ---- mug, right foreground (scale cue), acid rim light ----
MX, MY = 1705, 800         # mug top-centre
MRX, MH = 92, 190          # radius-x, height
S.append(f'<ellipse cx="{MX}" cy="{MY+MH+8}" rx="{MRX+46}" ry="20" fill="#000000" opacity="0.45"/>')
S.append(f'<path d="M {MX-MRX} {MY} L {MX-MRX+10} {MY+MH} Q {MX} {MY+MH+26} {MX+MRX-10} {MY+MH} L {MX+MRX} {MY} Z" fill="#080d09"/>')
S.append(f'<path d="M {MX+MRX-4} {MY+34} q 74 -10 78 52 q 4 62 -66 64" fill="none" stroke="#080d09" stroke-width="24"/>')
S.append(f'<ellipse cx="{MX}" cy="{MY}" rx="{MRX}" ry="26" fill="#0f1811"/>')
S.append(f'<ellipse cx="{MX}" cy="{MY}" rx="{MRX}" ry="26" fill="none" stroke="#1c2b20" stroke-width="5"/>')
S.append(f'<path d="M {MX-MRX} {MY} A {MRX} 26 0 0 1 {MX-MRX*0.1} {MY-26}" fill="none" stroke="{ACID}" stroke-width="4" opacity="0.55"/>')
S.append(f'<path d="M {MX-MRX} {MY+4} L {MX-MRX+9} {MY+MH*0.72}" stroke="{ACID}" stroke-width="3" opacity="0.22"/>')

# ---- floating motes in the light beam (dust) ----
rnd = random.Random(11)
for _ in range(26):
    mx = rnd.uniform(940, 1480); my = rnd.uniform(300, 640)
    r = rnd.uniform(1.2, 3.4); o = rnd.uniform(0.12, 0.5)
    S.append(f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="{r:.1f}" fill="{ACID_HI}" opacity="{o:.2f}"/>')

# ---- vignette ----
S.append(f'<rect width="{W}" height="{H}" fill="url(#vign)"/>')
S.append('</svg>')

svg = "\n".join(S)
open("ai-curious_hero.svg","w").write(svg)
cairosvg.svg2png(bytestring=svg.encode(), write_to="_hero_raw.png",
                 output_width=W, output_height=H)

# ---- post: film grain + slight extra vignette via PIL ----
img = Image.open("_hero_raw.png").convert("RGB")
rnd = random.Random(42)
grain = Image.effect_noise((W, H), 26).convert("L")
img = Image.composite(
    Image.blend(img, Image.new("RGB", (W,H), (255,255,255)), 0.05),
    Image.blend(img, Image.new("RGB", (W,H), (0,0,0)), 0.05),
    grain)
img.save("ai-curious_hero.png", optimize=True)
# derived index card — straight downscale
img.resize((1200, 675), Image.LANCZOS).save("ai-curious_card.png", optimize=True)
print("done:", img.size)
