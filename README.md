# Sternenkarte

Mobile Sternkarte für das iPhone: hältst du das Telefon vor dich, zeigt die App per Pfeil, wohin du dich drehen musst, um **Betelgeuse**, Planeten, die ISS oder Sternbilder zu finden. Alles live über deinem echten Horizont.

Eine einzige HTML-Datei (`index.html`), keine Server-Abhängigkeit — alle Bibliotheken und Sterndaten sind eingebettet.

## Funktionen

- **Peilung**: Kompass + Gyro + GPS → Azimut/Höhe in Echtzeit, Pfeil mit Grad-Angabe und Höhen-Hinweis, „GEFUNDEN"-Zustand
- **Betelgeuse** hervorgehoben (roter Puls-Halo, Fakten-Karte, Distanz 548 Lj)
- **Planeten** Sonne, Mond, Merkur … Pluto — toggelbar, mit aktueller Position, Mondphase
- **ISS** live (wheretheiss.at) mit Bahnspur
- **Sternbilder** (88, Stellarium-Linien) und 2.620 Sterne bis 5,4 mag (HYG v3)
- **Zeitregler** ±12 h, Rotlichtmodus, optionale Kamera-Durchsicht, Namens-Toggles
- Rechnet mit astronomy-engine: Präzession, Aberration, Refraktion, wahre Sternörter

## Technik

| Baustein | Details |
|---|---|
| Rechenkern | astronomy-engine 2.1.19 (MIT) |
| 3D | three.js r169 (MIT) |
| Sterndaten | HYG-Database v3.7 (CC BY-SA 4.0), Sternbildlinien: Stellarium (GPL) |
| Sensoren | `DeviceOrientationEvent.requestPermission()` (iOS 13+), `webkitCompassHeading`, `watchPosition` |
| HTTPS | Pflicht für Sensoren & Standort — deshalb über GitHub Pages |

## Bauen

```bash
python3 build.py      # src/app.html + build/* → index.html (Platzhalter ersetzen)
```

Quellen liegen in `src/app.html` (App-Code) und `build/` (Bibliotheken, `stars.json`).
`build_data.py` erzeugt `build/stars.json` aus HYG-CSV + Stellarium-`index.json`.

## Bedienung

1. Seite über HTTPS öffnen, „Karte starten" tippen, Standort + Bewegung erlauben.
2. Ziel unten wählen (Betelgeuse ist vorbelegt).
3. Dem Pfeil folgen, bis „GEFUNDEN" erscheint.

Ohne Sensoren: „Ohne Sensoren" wählen und mit dem Finger ziehen.

## Hinweise

- Betelgeuse ist ein Roter Überriese in ~548 Lichtjahren; die Supernova in ~100.000 Jahren wäre tagelang heller als der Vollmond — „kurz vor der Explosion" sind astronomisch also noch ein paar Jahrtausende.
- Kompass-Genauigkeit hängt von der Umgebung ab (Metall, Magnete). Bei Abweichung: Handy in Acht bewegen.
