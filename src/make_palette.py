#!/usr/bin/env python3
"""Draw docs/palette.svg: one row per poster with its palette and type specimens. Needs rsvg-convert.

The source SVG names the fonts; rsvg-convert writes the final SVG with the glyphs as outlines, so it looks
the same on GitHub where those fonts are not installed.
"""
import subprocess
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
W, H = 960, 880
INK, MUTED = "#1c1c1c", "#6b6b6b"

rows = [
    dict(name="Modern", note="Rounded cards, tinted panels, one sans family", display="Inter Display", dw=800, ui="Inter", r=10,
         swatches=[("KU red", "#901a1e"), ("Teal", "#0f6b73"), ("Gold", "#e0a526"), ("Soft", "#f4efe9"), ("Ink", "#1c1c1c"), ("Grey", "#444444"), ("Paper", "#ffffff")],
         specimens=[("Hire a physicist.", dict(family="Inter Display", weight=900, size=44, fill=INK), "Inter Display Black"),
                    ("Better moderators make better neutron beams", dict(family="Inter Display", weight=800, size=26, fill="#901a1e"), "Inter Display ExtraBold"),
                    ("Liquid hydrogen needs continuous ortho–para conversion. Thymol (C₁₀H₁₄O) is abundant.", dict(family="Inter", weight=400, size=18, fill=INK), "Inter Regular")]),
    dict(name="Classic", note="White page, hairline rules, serif voice", display="Garamontio", dw=700, ui="Arimo Nerd Font", r=0,
         swatches=[("KU red", "#901a1e"), ("Gold", "#e0a526"), ("Ink", "#1c1c1c"), ("Grey", "#555555"), ("Rule", "#cfc8bf"), ("Paper", "#ffffff")],
         specimens=[("Hire a physicist.", dict(family="Garamontio", weight=700, size=48, fill=INK), "Garamontio Bold"),
                    ("Better moderators make better neutron beams", dict(family="Garamontio", weight=700, size=28, fill="#901a1e"), "Garamontio Bold"),
                    ("Liquid hydrogen needs continuous ortho–para conversion. Thymol (C₁₀H₁₄O) is abundant.", dict(family="Garamontio", weight=400, size=21, fill=INK), "Garamontio Regular"),
                    ("Thymol, 300 K. AFGA (A = 0.946) against a fitted sigmoidal curve.", dict(family="Arimo Nerd Font", weight=400, size=15, fill="#555555"), "Arimo Regular")]),
]


def t(x, y, s, family, size, fill, weight=400, anchor="start", style="normal"):
    return f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" font-style="{style}" fill="{fill}" text-anchor="{anchor}">{s}</text>'


out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">', f'<rect width="{W}" height="{H}" fill="#fff"/>']
oy = 0
for i, row in enumerate(rows):
    if i:
        out.append(f'<rect x="32" y="{oy}" width="{W - 64}" height="1" fill="#e2ddd6"/>')
    out.append(t(32, oy + 56, row["name"], row["display"], 34, "#901a1e", row["dw"]))
    out.append(t(32, oy + 80, row["note"], row["ui"], 14, MUTED))
    for k, (name, hexv) in enumerate(row["swatches"]):
        x = 32 + k * 128
        out.append(f'<rect x="{x}" y="{oy + 100}" width="116" height="64" rx="{row["r"]}" fill="{hexv}" stroke="#d9d4cc" stroke-width="1"/>')
        out.append(t(x, oy + 186, name, row["ui"], 14, INK, 700))
        out.append(t(x, oy + 204, hexv, row["ui"], 13, MUTED))
    y = oy + 264
    for text, f, tag in row["specimens"]:
        out.append(t(32, y, text, f["family"], f["size"], f["fill"], f["weight"]))
        out.append(t(W - 32, y, tag, row["ui"], 12, MUTED, anchor="end"))
        y += f["size"] + 26
    oy += 430
out.append("</svg>")
src = DOCS / "_palette_src.svg"
src.write_text("\n".join(out))
subprocess.run(["rsvg-convert", "-f", "svg", "-o", str(DOCS / "palette.svg"), str(src)], check=True)
src.unlink()
print("wrote docs/palette.svg")
