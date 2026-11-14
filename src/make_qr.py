#!/usr/bin/env python3
"""Footer QR code: a thymol molecule with neutrons in the centre, recoloured per poster. Needs rsvg-convert and zbarimg.

assets/qr_base.svg is the finished design: QR version 6, error level H, round ink modules, rounded corner marks,
a ball-and-stick thymol (2-isopropyl-5-methylphenol) crossed by a neutron beam. This script restyles it and writes
assets/qr_modern.{svg,pdf} and assets/qr_classic.{svg,pdf} with a transparent background, then asserts they decode.

Hard limits found by testing (keep them if the base is ever redrawn):
- The centre knock-out is 44 % of the code width. 46 % no longer decodes. Do not enlarge it.
- Stay at QR version 6 or lower: version 7 has an alignment pattern at the exact centre.
- Keep the mark bold. Hairlines vanish at poster distance.
- Standard chemistry colours (carbon grey, oxygen red, hydrogen white). No gold oxygen.
"""
import math, re, subprocess, sys
from pathlib import Path

URL = "https://markbujehein.github.io/"
A = Path(__file__).resolve().parent / "assets"
FRAME = "halo"  # none | disc | bare | halo | glow: what surrounds the molecule
TEAL, GOLD, SOFT = "#0f6b73", "#e0a526", "#f4efe9"
C, R = 24.5, 9.02  # centre and knock-out radius, in modules

DISC = re.compile(r'<circle cx="24.5" cy="24.5" r="9.02" fill="#f4efe9" stroke="#901a1e" stroke-width="0.32"/>')
MOD = re.compile(r'<circle cx="([\d.]+)" cy="([\d.]+)" r="\.47" fill="#1c1c1c"/>')
GLOW = f'<circle cx="{C}" cy="{C}" r="11.5" fill="url(#gG)"/>'
GLOW_DEF = f'<radialGradient id="gG"><stop offset=".55" stop-color="{SOFT}"/><stop offset="1" stop-color="{SOFT}" stop-opacity="0"/></radialGradient></defs>'


def dot(m, grow=4.0):
    """Modules shrink towards the molecule: the code fades into it instead of being cut off by a ring."""
    x, y = float(m[1]), float(m[2])
    t = min(1.0, max(0.0, (math.hypot(x - C, y - C) - R) / grow))
    return f'<circle cx="{m[1]}" cy="{m[2]}" r="{.47 * (.4 + .6 * t):.3f}" fill="#1c1c1c"/>'


def variant(poster, frame=FRAME):
    s = (A / "qr_base.svg").read_text().replace('<rect width="49" height="49" fill="#ffffff"/>', "", 1)  # the poster draws the white tile
    assert DISC.search(s) and MOD.search(s), "qr_base.svg changed shape"
    if frame in ("bare", "halo", "glow", "none"):
        s = DISC.sub(GLOW if frame == "glow" else "", s)
    if frame == "glow":
        s = s.replace("</defs>", GLOW_DEF, 1)
    if frame == "halo":
        s = MOD.sub(dot, s)
    if poster == "classic":  # no teal or beige in the classic palette, and the page stays pure white
        s = s.replace(TEAL, GOLD).replace(SOFT, "#ffffff").replace('opacity=".55"', 'opacity=".9"')
    return s


def decodes(svg_path, width):
    png = svg_path.with_name(f"_check_{width}.png")
    subprocess.run(["rsvg-convert", "-w", str(width), "-b", "white", "-o", str(png), str(svg_path)], check=True)
    out = subprocess.run(["zbarimg", "--raw", "-q", str(png)], capture_output=True, text=True).stdout.strip()
    png.unlink()
    return out == URL


if __name__ == "__main__":
    frame = sys.argv[1] if len(sys.argv) > 1 else FRAME
    for poster in ("modern", "classic"):
        svg = A / f"qr_{poster}.svg"
        svg.write_text(variant(poster, frame))
        subprocess.run(["rsvg-convert", "-f", "pdf", "-o", str(A / f"qr_{poster}.pdf"), str(svg)], check=True)
        for width in (800, 250):
            assert decodes(svg, width), f"{poster}/{frame}: QR does not decode at {width}px"
        print(f"qr_{poster}: frame={frame}, decodes")
