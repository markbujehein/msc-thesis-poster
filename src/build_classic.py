#!/usr/bin/env python3
"""Classic poster: white page, Garamond voice, free-flowing blocks with no column grid. Coordinates are mm, type is pt.

Close to the KU poster template (white page, KU red, serif wordmark voice, columns) with the
rules bent where it helps: a full-bleed red masthead with a gold line, one oversized number.
"""
import json, subprocess, sys
from pathlib import Path

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
A = SRC / "assets"
OUT = ROOT / "build"
OUT.mkdir(exist_ok=True)
L = []


def cmd(_id, **kw):
    L.append(f"{_id} {json.dumps(kw, ensure_ascii=False)}")


M = 72 / 25.4  # layout is written in mm; the document unit is points
SERIF, SANS = "Garamontio", "Arimo Nerd Font"


def style(name, fam, sty, size, fill, align="left", lead=None, track=0, after=0):
    chars = {"fontFamily": fam, "fontStyle": sty, "size": size, "fill": fill}
    if lead:
        chars["leading"] = {"kind": "points", "value": lead}
    if track:
        chars["tracking"] = track
    cmd("style.paragraph.create", name=name, chars=chars, para={"align": align, "hyphenate": False, "spaceAfter": round(after * M, 2)})


def rect(x0, y0, x1, y1, fill, r=None, shape="rectangle"):
    cmd("frame.create", rect=[x0 * M, y0 * M, x1 * M, y1 * M], shape=shape, content="unassigned")
    cmd("object.fill", swatch=fill)
    cmd("object.stroke", swatch="[None]")
    if r:
        cmd("object.cornerOptions", shape="rounded", size=round(r * M, 2))


def text(x0, y0, x1, y1, txt, st):
    cmd("frame.create", rect=[x0 * M, y0 * M, x1 * M, y1 * M], content="text", text=txt, caret=True)
    cmd("edit.selectAll")
    cmd("style.paragraph.apply", name=st)


def img(path, x0, y0, x1, y1, mode="fitProportionally", shape="rectangle"):
    cmd("frame.create", rect=[x0 * M, y0 * M, x1 * M, y1 * M], shape=shape, content="graphic")
    cmd("file.place", path=str(path))
    cmd("object.fit", mode=mode)


# ---- document, swatches, styles
cmd("file.new", width=2383.94, height=3370.08, units="points", margins=0, bleed=round(3 * M, 3), title="ESS DMSC School 2026 poster (classic)")
for n, c in [("KU red", "#901a1e"), ("Gold", "#e0a526"), ("Ink", "#1c1c1c"), ("Grey", "#555555"), ("Rule", "#cfc8bf")]:
    cmd("swatch.create", name=n, color=c)
W = "[Paper]"
style("H1", SERIF, "Bold", 100, W, lead=100)
style("Auth", SERIF, "Italic", 36, W, lead=40)
style("Affil", SANS, "Regular", 22, W, lead=27)
style("H2", SERIF, "Bold", 50, "KU red", lead=54)
style("H3", SERIF, "Bold", 38, "Ink", lead=42)
style("Body", SERIF, "Regular", 36, "Ink", lead=47, after=4)
style("Q", SERIF, "Regular", 36, "Ink", lead=45, after=5)
style("StepH", SERIF, "Bold", 34, "Ink", lead=36)
style("Lead", SERIF, "Bold", 60, "KU red", lead=62)
style("StepP", SERIF, "Regular", 30, "Ink", lead=37)
style("Num", SERIF, "Bold Italic", 44, "KU red", lead=40)
style("Cap", SANS, "Regular", 21, "Grey", lead=26)
style("Bullet", SERIF, "Regular", 32, "Ink", lead=40, after=8)
style("Big", SERIF, "Italic", 150, "KU red", lead=140)
style("BigS", SERIF, "Regular", 30, "Ink", lead=37)
style("BigN", SERIF, "Bold Italic", 56, "KU red", lead=56)
style("BigL", SERIF, "Regular", 30, "Ink", lead=37)
style("Pill", SANS, "Bold", 14, "Ink", align="center", track=80)
style("FootBig", SERIF, "Bold", 96, W, lead=96)
style("FootSm", SANS, "Regular", 30, W, lead=36)
style("Refs", SANS, "Regular", 15, W, lead=19)
style("FootCap", SANS, "Regular", 22, W, align="right", lead=28, after=3)

# ---- masthead: full-bleed red, a gold line under it
rect(-3, -3, 844, 226, "KU red")
rect(-3, 226, 844, 229, "Gold")
img(A / "nbi_logo.pdf", 36, 16, 36 + 120, 16 + 120 * 186 / 262)
rect(680, 16, 805, 86, W, r=6)
img(A / "isis.png", 690, 24, 795, 78)
text(36, 104, 805, 186, "Can a simple model predict how neutrons cross new moderator materials?", "H1")
text(36, 190, 805, 204, "Mark B.H. Sørensen¹, M. Krzystyniak², G. Škoro², S. Rudić², H.N. Bordallo¹", "Auth")
text(36, 206, 805, 221, "¹ Niels Bohr Institute, University of Copenhagen · ² ISIS Neutron and Muon Source, Rutherford Appleton Laboratory, UK", "Affil")

# ---- introduction: statement and text on the left, the instrument breaks out on the right
text(36, 250, 400, 318, "Better moderators make better neutron beams", "Lead")
text(36, 322, 400, 462,
     "Liquid hydrogen needs continuous ortho–para conversion. Solid methane breaks down under radiation, limiting its lifetime to about 60 days. "
     "Aromatic hydrocarbons are more radiation-stable and are candidate cryogenic moderators.\n"
     "Thymol (C₁₀H₁₄O) and p-cymene (C₁₀H₁₄) are abundant, low-toxicity candidates. We measured how strongly each scatters neutrons.", "Body")
img(A / "vesuvio.png", 430, 250, 805, 250 + 375 * 720 / 959)
text(430, 535, 805, 558, "Measured on VESUVIO at ISIS (UK). Image credit: STFC. a) incident monitor, b) transmitted monitor, c–d) detectors, e) gold foils.", "Cap")
rect(36, 474, 37.4, 562, "KU red")
qs = ["How accurately can VESUVIO transmission measure the cross section?",
      "How well does the AFGA model predict it?",
      "What explains the differences between thymol and p-cymene?",
      "Are they suitable cold or thermal moderators?"]
text(46, 474, 400, 564, "\n".join(qs), "Q")

# ---- method: a tinted full-bleed band, the steps run left to right
rect(36, 580, 805, 581.2, "KU red")
text(36, 590, 600, 610, "From raw counts to a cross section", "H2")
steps = [("Count neutrons", "Two beam monitors count neutrons before and after the sample, by arrival time.", "monitor.png", "Monitor data"),
         ("Compare the beams", "Dividing “after” by “before” gives the fraction that survives the sample.", "transmission.png", "Transmission"),
         ("Turn it into a cross section", "Fewer neutrons through means a bigger target. The log of transmission gives the cross section.", "xsec.png", "Total cross section"),
         ("Anchor it in barns", "At high energy neutrons see free atoms. Matching that known limit gives absolute values.", None, None)]
bw = (769 - 3 * 18) / 4
for i, (h, p, im, c) in enumerate(steps):
    x, y = 36 + i * (bw + 18), 622
    text(x, y, x + 14, y + 18, str(i + 1), "Num")
    text(x + 15, y + 1, x + bw, y + 15, h, "StepH")
    text(x, y + 17, x + bw, y + 59, p, "StepP")
    if im:
        img(A / im, x, y + 62, x + bw, y + 182)
        text(x, y + 184, x + bw, y + 196, c, "Cap")
    else:
        text(x, y + 66, x + bw, y + 87, "328 b", "BigN")
        text(x, y + 88, x + bw, y + 100, "thymol free-atom limit", "BigL")
        text(x, y + 112, x + bw, y + 133, "323 b", "BigN")
        text(x, y + 134, x + bw, y + 146, "p-cymene free-atom limit", "BigL")
        text(x, y + 184, x + bw, y + 205, "Data reduction performed with the Mantid framework [4].", "Cap")

# ---- results: figures left, the number and the conclusions right, no grid
rect(36, 846, 805, 847.2, "KU red")
text(36, 852, 200, 872, "Results", "H2")
rect(112, 857, 198, 871, "Gold")
text(112, 861.14, 198, 871.14, "WORK IN PROGRESS", "Pill")
text(36, 878, 260, 893, "AFGA vs. measurement", "H3")
img(A / "afga_fit.png", 36, 896, 36 + 178 * 4939 / 4390, 1074)
text(36, 1076, 270, 1096, "Thymol, 300 K. AFGA (A = 0.946) against a fitted sigmoidal curve.", "Cap")
text(276, 878, 470, 893, "Thymol vs. p-cymene", "H3")
img(A / "pairwise.png", 276, 896, 276 + 178 * 2909 / 3013, 1074)
text(276, 1076, 470, 1096, "Pair-wise comparison at 10 K and 300 K.", "Cap")
text(500, 852, 805, 914, "4–6 %", "Big")
text(500, 916, 805, 944, "AFGA overpredicts the cross section (13–17 b), almost independent of energy.", "BigS")
rect(500, 950, 805, 950.4, "Rule")
text(500, 956, 805, 1096,
     "Above about 1 eV, thymol and p-cymene are neutronically equivalent.\n"
     "Below about 25 meV, solid thymol and liquid p-cymene (300 K) differ. Statistics are limited there.\n"
     "The choice between them rests on engineering: phase, radiolytic stability, handling.\n"
     "Next: benchmark AFGA against full lattice dynamics (DFT).", "Bullet")

# ---- footer: call to action, references, QR code to the academic page
rect(-3, 1100, 844, 1192, "KU red")
img(A / "me.png", 36, 1106, 114, 1184, mode="fillProportionally", shape="ellipse")
cmd("object.stroke", swatch="Gold", weight=6)
text(130, 1105, 565, 1141, "Hire a physicist.", "FootBig")
text(130, 1148, 565, 1162, "PhD position wanted. Modelling, experiments, fitting, Bayesian analysis.", "FootSm")
text(130, 1166, 345, 1188, "[1] Romanelli et al., Meas. Sci. Technol. 28, 095501 (2017)\n[2] Romanelli et al., J. Phys.: Condens. Matter 33, 285901 (2021)", "Refs")
text(350, 1166, 565, 1188, "[3] Krzystyniak et al., Phys. Scr. 98, 025707 (2023)\n[4] Arnold et al., Nucl. Instrum. Methods A 764, 156 (2014)", "Refs")
text(570, 1126, 716, 1172, "Scan to see my work and contact me\nmark.sorensen@nbi.ku.dk\nmarkbujehein.github.io", "FootCap")
rect(725, 1106, 805, 1186, W, r=6)
img(A / "qr_classic.pdf", 725, 1106, 805, 1186)

# p-cymene: the locant p is always italic
for ps, fam, st in [("Body", SERIF, "Italic"), ("Q", SERIF, "Italic"), ("Bullet", SERIF, "Italic"), ("BigL", SERIF, "Italic"), ("H3", SERIF, "Bold Italic")]:
    cmd("find.change", find="p(?=-cymene)", grep=True, caseSensitive=True, scope="document", findFormat={"paraStyle": ps},
        change="", attrs={"fontFamily": fam, "fontStyle": st})

cmd("file.save", path=str(SRC / "classic"))
cmd("file.exportIdml", path=str(SRC / "classic.idml"))
cmd("file.exportPdf", path=str(OUT / "classic_trim.pdf"))
cmd("file.exportPdf", path=str(OUT / "classic_bleed.pdf"), bleed=True)
cmd("document.inspect")
cmd("font.list")

script = OUT / "classic_build.txt"
script.write_text("\n".join(L) + "\n")
r = subprocess.run(["designcraft-cli", "script", str(script), "--export", str(OUT / "classic_preview.png")], capture_output=True, text=True)
(OUT / "classic_run.log").write_text(r.stdout + r.stderr)
dc_rc = r.returncode
from PIL import Image  # the preview is only for the README: shrink it
im = Image.open(OUT / "classic_preview.png"); im.thumbnail((1400, 2000)); im.save(OUT / "classic_preview.png", optimize=True)
print(dc_rc, len(L), "commands")

# ---- print PDF: the bleed PDF plus trim marks (marks widen the page by 36 pt a side, trim box stays A0)
src, dst = OUT / "classic_bleed.pdf", OUT / "classic_print.pdf"
dst.unlink(missing_ok=True)
steps = [{"tool": "doc_open", "args": {"path": str(src)}},
         {"tool": "doc_printer_marks", "args": {"doc": 1, "trim": True, "bleed": True, "registration": False, "color_bars": False,
                                                 "page_info": True, "make_room": 36, "line_weight": 0.5, "label": "ESS DMSC poster (classic), A0 trim and bleed marks"}},
         {"tool": "doc_save", "args": {"doc": 1, "path": str(dst), "full": True}}]
(OUT / "classic_steps.json").write_text(json.dumps(steps))
r = subprocess.run(["pdfcraft-cli", "run", "--script", str(OUT / "classic_steps.json"), "--root", str(ROOT)], capture_output=True, text=True)
print("print copy:", dst, "rc", r.returncode, r.stderr[-300:])
src.unlink(missing_ok=True)  # the bleed PDF only feeds the print PDF; export it on request

log = (OUT / "classic_run.log").read_text()
if dc_rc or r.returncode or '"overset": true' in log:
    print("CHECK THE BUILD: overset text or errors; intermediates kept in", OUT); sys.exit(1)
