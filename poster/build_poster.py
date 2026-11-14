#!/usr/bin/env python3
"""Generate the DesignCraft script for poster and run it. Coordinates are mm, type is pt."""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
A = HERE / "assets"
OUT = HERE / "build"  # intermediates (bleed PDF, script, log, preview), overwritten each run, never deleted
OUT.mkdir(exist_ok=True)
SRC = HERE / "source"  # editable files
SRC.mkdir(exist_ok=True)
L = []


def cmd(_id, **kw):
    L.append(f"{_id} {json.dumps(kw, ensure_ascii=False)}")


M = 72 / 25.4  # layout is written in mm; the document unit is points
PT = 1


def style(name, font, size, fill, align="left", lead=None, track=0, after=0):
    chars = {"fontFamily": "Inter" if font == "Regular" else "Inter Display", "fontStyle": font, "size": round(size * PT, 3), "fill": fill}
    if lead:
        chars["leading"] = {"kind": "points", "value": round(lead * PT, 3)}
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
cmd("file.new", width=2383.94, height=3370.08, units="points", margins=0, bleed=round(3 * M, 3), title="ESS DMSC School 2026 poster")
for n, c in [("KU red", "#901a1e"), ("Teal", "#0f6b73"), ("Gold", "#e0a526"), ("Soft", "#f4efe9"), ("Ink", "#1c1c1c"), ("Grey", "#444444")]:
    cmd("swatch.create", name=n, color=c)
W = "[Paper]"
style("H1", "Black", 92, W, lead=92)
style("H2", "ExtraBold", 56, "KU red", lead=58)
style("H3", "ExtraBold", 44, "KU red", lead=46)
style("Kick", "Bold", 24, "Teal", track=140)
style("Body", "Regular", 34, "Ink", lead=44)
style("Bullet", "Regular", 32, "Ink", lead=40, after=6)
style("Cap", "Regular", 24, "Grey", lead=30)
style("Auth", "Bold", 32, W, lead=38)
style("Affil", "Regular", 22, W, lead=27)
style("CardQ", "SemiBold", 32, W, lead=38)
style("CardN", "Black", 54, "Gold", lead=54)
style("StepH", "Bold", 32, "Ink", lead=34)
style("StepP", "Regular", 28, "Ink", lead=34)
style("StepN", "Black", 30, W, align="center", lead=30)
style("Big", "Black", 72, "KU red", lead=72)
style("BigS", "Regular", 26, "Ink", lead=31)
style("Pill", "Black", 14, "Ink", align="center", track=80)
style("FootBig", "Bold", 56, W, lead=60)
style("FootSm", "Regular", 30, W, lead=36)
style("Refs", "Regular", 16, W, lead=21)

# ---- header
rect(-3, -3, 844, 222, "KU red")
img(A / "nbi_logo.pdf", 28, 8, 28 + 150, 8 + 150 * 186 / 262)
rect(688, 16, 813, 86, W, r=6)
img(A / "isis.png", 698, 24, 803, 78)
text(28, 117, 813, 186, "Can a simple model predict how neutrons cross new moderator materials?", "H1")
text(28, 191, 813, 202, "Mark B.H. Sørensen¹, M. Krzystyniak², G. Škoro², S. Rudić², H.N. Bordallo¹", "Auth")
text(28, 203, 813, 220, "¹ Niels Bohr Institute, University of Copenhagen · ² ISIS Neutron and Muon Source, Rutherford Appleton Laboratory, UK", "Affil")

# ---- why
text(28, 238, 400, 249, "WHY IT MATTERS", "Kick")
text(28, 251, 400, 294, "Better moderators make better neutron beams", "H2")
text(28, 298, 400, 452,
     "Liquid hydrogen needs continuous ortho–para conversion. Solid methane breaks down under radiation, limiting its lifetime to about 60 days. "
     "Aromatic hydrocarbons are more radiation-stable and are candidate cryogenic moderators.\n"
     "Thymol (C₁₀H₁₄O) and p-cymene (C₁₀H₁₄) are abundant, low-toxicity candidates. We measured how strongly each scatters neutrons.", "Body")
rect(416, 235, 813, 452, "Soft", r=8)
rect(424, 243, 805, 420, W, r=3)
img(A / "vesuvio.png", 428, 247, 801, 416)
text(424, 423, 805, 449, "Measured on VESUVIO at ISIS (UK). Image credit: STFC. a) incident monitor, b) transmitted monitor, c–d) detectors, e) gold foils.", "Cap")

# ---- research questions
qs = ["How accurately can VESUVIO transmission measure the cross section?",
      "How well does the AFGA model predict it?",
      "What explains the differences between thymol and p-cymene?",
      "Are they suitable cold or thermal moderators?"]
cw = (785 - 3 * 10) / 4
for i, q in enumerate(qs):
    x = 28 + i * (cw + 10)
    rect(x, 464, x + cw, 562, "KU red", r=8)
    text(x + 9, 470, x + 40, 492, str(i + 1), "CardN")
    text(x + 9, 494, x + cw - 9, 560, q, "CardQ")

# ---- pipeline
text(28, 574, 400, 584, "HOW WE GOT FROM RAW COUNTS TO PHYSICS", "Kick")
text(28, 586, 813, 606, "Four steps, from beam monitors to barns", "H2")
steps = [("Count neutrons", "Two beam monitors count neutrons before and after the sample, by arrival time.", "monitor.png", "Monitor data"),
         ("Compare the beams", "Dividing “after” by “before” gives the fraction that survives the sample.", "transmission.png", "Transmission"),
         ("Turn it into a cross section", "Fewer neutrons through means a bigger target. The log of transmission gives the cross section.", "xsec.png", "Total cross section"),
         ("Anchor it in barns", "At high energy neutrons see free atoms. Matching that known limit gives absolute values.", None, None)]
sw = (785 - 3 * 7) / 4
for i, (h, p, im, c) in enumerate(steps):
    x = 28 + i * (sw + 7)
    y = 618
    rect(x, y, x + sw, y + 228, "Soft", r=8)
    rect(x + 8, y - 7, x + 25, y + 10, "Teal", shape="ellipse")
    text(x + 8, y - 4, x + 25, y + 8, str(i + 1), "StepN")
    text(x + 8, y + 14, x + sw - 8, y + 42, h, "StepH")
    text(x + 8, y + 44, x + sw - 8, y + 84, p, "StepP")
    if im:
        rect(x + 8, y + 88, x + sw - 8, y + 200, W, r=3)
        img(A / im, x + 10, y + 90, x + sw - 10, y + 198)
        text(x + 8, y + 204, x + sw - 8, y + 224, c, "Cap")
    else:
        text(x + 8, y + 92, x + sw - 8, y + 122, "328 b", "Big")
        text(x + 8, y + 124, x + sw - 8, y + 142, "thymol free-atom limit", "BigS")
        text(x + 8, y + 150, x + sw - 8, y + 180, "323 b", "Big")
        text(x + 8, y + 182, x + sw - 8, y + 200, "p-cymene free-atom limit", "BigS")
text(28, 850, 600, 860, "Data reduction performed with the Mantid framework [4].", "Cap")

# ---- results
text(28, 870, 330, 880, "PRELIMINARY RESULTS", "Kick")
rect(150, 868, 236, 882, "Gold", r=7)
text(150, 871, 236, 881, "WORK IN PROGRESS", "Pill")
text(28, 884, 230, 902, "AFGA vs. measurement", "H3")
img(A / "afga_fit.png", 28, 906, 228, 1068)
text(28, 1070, 228, 1094, "Thymol, 300 K. AFGA (A = 0.946) against a fitted sigmoidal curve.", "Cap")
rect(240, 884, 610, 1094, "Soft", r=8)
text(252, 892, 600, 903, "TAKE-HOME", "Kick")
bul = ["AFGA overpredicts the cross section by about 4–6 % (13–17 b), almost independent of energy.",
       "Above about 1 eV, thymol and p-cymene are neutronically equivalent.",
       "Below about 25 meV, solid thymol and liquid p-cymene (300 K) differ. Statistics are limited there.",
       "The choice between them rests on engineering: phase, radiolytic stability, handling.",
       "Next: benchmark AFGA against full lattice dynamics (DFT)."]
text(252, 906, 600, 1090, "\n".join(bul), "Bullet")
text(623, 884, 813, 902, "Thymol vs. p-cymene", "H3")
img(A / "pairwise.png", 623, 906, 813, 1068)
text(623, 1070, 813, 1094, "Pair-wise comparison at 10 K and 300 K.", "Cap")

# ---- footer
rect(-3, 1100, 844, 1192, "KU red")
img(A / "me.png", 28, 1106, 106, 1184, mode="fillProportionally", shape="ellipse")
cmd("object.stroke", swatch="Gold", weight=6)
text(122, 1116, 570, 1138, "Talk to me, or help me find a PhD scholarship", "FootBig")
text(122, 1141, 570, 1160, "mark.sorensen@nbi.ku.dk · Bordallo Group, Niels Bohr Institute", "FootSm")
text(580, 1110, 813, 1180,
     "[1] Romanelli et al., Meas. Sci. Technol. 28, 095501 (2017)\n[2] Romanelli et al., J. Phys.: Condens. Matter 33, 285901 (2021)\n"
     "[3] Krzystyniak et al., Phys. Scr. 98, 025707 (2023)\n[4] Arnold et al., Nucl. Instrum. Methods A 764, 156 (2014)", "Refs")

# p-cymene: the locant p is always italic
for ps, fam, st in [("Body", "Inter", "Italic"), ("Bullet", "Inter", "Italic"), ("BigS", "Inter", "Italic"),
                    ("CardQ", "Inter Display", "SemiBold Italic"), ("H3", "Inter Display", "ExtraBold Italic")]:
    cmd("find.change", find="p(?=-cymene)", grep=True, caseSensitive=True, scope="document", findFormat={"paraStyle": ps},
        change="", attrs={"fontFamily": fam, "fontStyle": st})

cmd("file.save", path=str(SRC / "poster"))
cmd("file.exportIdml", path=str(SRC / "poster.idml"))
cmd("file.exportPdf", path=str(OUT / "poster_trim.pdf"))
cmd("file.exportPdf", path=str(OUT / "poster_bleed.pdf"), bleed=True)
cmd("document.inspect")
cmd("font.list")

script = OUT / "build.txt"
script.write_text("\n".join(L) + "\n")
r = subprocess.run(["designcraft-cli", "script", str(script), "--export", str(OUT / "preview.png")], capture_output=True, text=True)
(OUT / "run.log").write_text(r.stdout + r.stderr)
dc_rc = r.returncode
print(dc_rc, len(L), "commands")

# ---- print copy with trim marks (HP poster printer; marks widen the page by 36 pt a side, trim box stays A0)
PRINT = HERE  # print PDF sits next to the poster
src, dst = OUT / "poster_bleed.pdf", PRINT / "poster_print.pdf"
dst.unlink(missing_ok=True)
steps = [{"tool": "doc_open", "args": {"path": str(src)}},
         {"tool": "doc_printer_marks", "args": {"doc": 1, "trim": True, "bleed": True, "registration": False, "color_bars": False,
                                                 "page_info": True, "make_room": 36, "line_weight": 0.5, "label": "ESS DMSC poster, A0 trim and bleed marks"}},
         {"tool": "doc_save", "args": {"doc": 1, "path": str(dst), "full": True}}]
(OUT / "steps.json").write_text(json.dumps(steps))
r = subprocess.run(["pdfcraft-cli", "run", "--script", str(OUT / "steps.json"), "--root", str(HERE)], capture_output=True, text=True)
print("print copy:", dst, "rc", r.returncode, r.stderr[-300:])

# the deliverable: the NBI poster at poster/poster.pdf (A0, no marks)
shutil.copy(OUT / "poster_trim.pdf", HERE / "poster.pdf")
log = (OUT / "run.log").read_text()
if dc_rc or r.returncode or '"overset": true' in log:
    print("CHECK THE BUILD: overset text or errors; intermediates kept in", OUT); sys.exit(1)
