#!/usr/bin/env python3
"""Erzeugt das App-Icon (Nacht-Horizont, Kompassnadel, roter Stern) in mehreren Größen."""
from PIL import Image, ImageDraw, ImageFilter
import math, os

S = 1024          # Arbeitsgröße (Supersampling)
OUT = os.path.dirname(os.path.abspath(__file__))

img = Image.new('RGBA', (S, S), (4, 7, 15, 255))
px = img.load()

# Hintergrund: Radialverlauf tiefblau -> fast schwarz, unten warmes Horizontglühen
cx, cy = S*0.5, S*0.42
for y in range(S):
    for x in range(0, S, 2):
        d = math.hypot(x-cx, y-cy) / (S*0.78)
        t = min(1.0, d)
        r = int(10*(1-t) + 4*t)
        g = int(23*(1-t) + 7*t)
        b = int(48*(1-t) + 15*t)
        # Horizontglut
        hz = max(0.0, 1.0 - abs(y - S*0.86) / (S*0.30))
        hz = hz**2.2
        r += int(46*hz); g += int(26*hz); b += int(10*hz)
        for xx in (x, x+1):
            if xx < S:
                px[xx, y] = (min(255, r), min(255, g), min(255, b), 255)

d = ImageDraw.Draw(img, 'RGBA')

# Sternenstaub
import random
random.seed(7)
for _ in range(190):
    x, y = random.uniform(0, S), random.uniform(0, S*0.86)
    a = random.randint(40, 150)
    rr = random.choice([1, 1, 1, 2])
    d.ellipse([x-rr, y-rr, x+rr, y+rr], fill=(200, 226, 255, a))

# Kompassring
R = S*0.30
ring = Image.new('RGBA', (S, S), (0,0,0,0))
rd = ImageDraw.Draw(ring, 'RGBA')
rd.ellipse([cx-R, cy-R, cx+R, cy+R], outline=(127, 227, 255, 78), width=int(S*0.009))
for i in range(24):
    a = math.radians(i*15)
    r1, r2 = R*0.90, R*1.0
    w = int(S*0.014) if i % 6 == 0 else int(S*0.008)
    col = (127, 227, 255, 150) if i % 6 == 0 else (127, 227, 255, 60)
    rd.line([cx+math.sin(a)*r1, cy-math.cos(a)*r1, cx+math.sin(a)*r2, cy-math.cos(a)*r2], fill=col, width=w)
ring = ring.filter(ImageFilter.GaussianBlur(S*0.004))
img.alpha_composite(ring)

# Nadel: zeigt nach oben, cyan mit Glow
ang = math.radians(18)           # leicht nach rechts geneigt
L = R*0.80
tipx, tipy = cx + math.sin(ang)*L, cy - math.cos(ang)*L
basew = S*0.055
bx, by = cx + math.sin(ang+math.pi)*L*0.42, cy - math.cos(ang+math.pi)*L*0.42
left  = (cx + math.sin(ang+math.pi/2)*basew, cy - math.cos(ang+math.pi/2)*basew)
right = (cx + math.sin(ang-math.pi/2)*basew, cy - math.cos(ang-math.pi/2)*basew)

glow = Image.new('RGBA', (S, S), (0,0,0,0))
gd = ImageDraw.Draw(glow, 'RGBA')
gd.polygon([(tipx, tipy), left, (bx, by), right], fill=(160, 240, 255, 255))
glow = glow.filter(ImageFilter.GaussianBlur(S*0.022))
img.alpha_composite(glow)
d.polygon([(tipx, tipy), left, (bx, by), right], fill=(238, 252, 255, 255))

# Zielstern (Betelgeuse): roter Punkt mit Glow und Funkeln
sx, sy = cx + math.sin(ang)*L*1.12, cy - math.cos(ang)*L*1.12
sg = Image.new('RGBA', (S, S), (0,0,0,0))
sd = ImageDraw.Draw(sg, 'RGBA')
for rr, aa in ((S*0.062, 55), (S*0.038, 105), (S*0.021, 195)):
    sd.ellipse([sx-rr, sy-rr, sx+rr, sy+rr], fill=(255, 90, 77, aa))
sg = sg.filter(ImageFilter.GaussianBlur(S*0.012))
img.alpha_composite(sg)
d.ellipse([sx-S*0.015, sy-S*0.015, sx+S*0.015, sy+S*0.015], fill=(255, 150, 140, 255))
for k in (0.052, 0.024):
    d.line([sx-S*k, sy, sx+S*k, sy], fill=(255, 190, 180, 190), width=int(S*0.006))
    d.line([sx, sy-S*k, sx, sy+S*k], fill=(255, 190, 180, 190), width=int(S*0.006))

# Sanfte Vignette
vig = Image.new('RGBA', (S, S), (0,0,0,0))
vd = ImageDraw.Draw(vig)
for i in range(60):
    t = i/60
    vd.ellipse([-S*0.2*t, -S*0.2*t, S*(1+0.2*t), S*(1+0.2*t)], outline=(0,0,0,int(4+10*t)), width=int(S*0.02))
img.alpha_composite(vig.filter(ImageFilter.GaussianBlur(S*0.02)))

for size in (512, 180, 32, 16):
    img.resize((size, size), Image.LANCZOS).save(os.path.join(OUT, f'icon-{size}.png'))
img.resize((256, 256), Image.LANCZOS).save(os.path.join(OUT, 'icon.png'))
print('ok')
