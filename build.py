#!/usr/bin/env python3
"""Baut die Ein-Datei-App: ersetzt Platzhalter durch three.js, astronomy-engine und Sterndaten."""
import json, pathlib, re, shutil, sys

ROOT = pathlib.Path(__file__).resolve().parent
DATA = ROOT / 'build'
OUT = ROOT / 'index.html'
STAGE = ROOT / 'index.stage.html'

html = (ROOT / 'src' / 'app.html').read_text(encoding='utf-8')
three = (DATA / 'three.module.min.js').read_text(encoding='utf-8')
astro = (DATA / 'astronomy.js').read_text(encoding='utf-8')
stars = (DATA / 'stars.json').read_text(encoding='utf-8')
json.loads(stars)  # Validierung

# three.module.min.js exportiert einzelne Bindings -> Namespace-Objekt THREE bauen
i = three.rfind('export{')
j = three.index('}', i)
items = [x.strip() for x in three[i + 7:j].split(',') if x.strip()]
pairs = []
for it in items:
    if ' as ' in it:
        loc, exp = it.split(' as ')
        pairs.append(f'{exp.strip()}:{loc.strip()}')
    else:
        pairs.append(f'{it}:{it}')
three = three[:i] + 'const THREE={' + ','.join(pairs) + '}' + three[j + 1:]

for marker, payload in (('/* __THREE__ */', three), ('/* __ASTRO__ */', astro), ('/* __STARS__ */', stars)):
    if html.count(marker) != 1:
        sys.exit(f'Marker {marker} kommt {html.count(marker)}x vor')
    html = html.replace(marker, payload)

STAGE.write_text(html, encoding='utf-8')
shutil.move(str(STAGE), str(OUT))

final = OUT.read_text(encoding='utf-8')
assert final.count('__THREE__') == 2   # three.js selbst nutzt window.__THREE__ (2x in einer Zeile)
assert final.count('__ASTRO__') == 0
assert final.count('__STARS__') == 0
print(f'OK {OUT} {len(final)} bytes')
