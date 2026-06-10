# -*- coding: utf-8 -*-
"""
Export AutoCAD (DXF R2010) des plans de principe électricité.
- Fond de plan architecte : image raster référencée à l'échelle 1:1 (mm).
- Symboles électriques : blocs natifs sur calques séparés (modifiables).
Sorties : autocad/plan_principe_elec_RDC.dxf, autocad/plan_principe_elec_R1.dxf
"""
import os
import math
import fitz
import ezdxf
from ezdxf.enums import TextEntityAlignment as TA

from generate_plans_principe import (
    ECL_RDC, PC_RDC, ECL_R1, PC_R1, LEG_ECL, LEG_PC)

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "0210_SITE CENTRE DE DREPANOCYTOSE LQ 3.pdf")
OUTDIR = os.path.join(HERE, "autocad")
os.makedirs(OUTDIR, exist_ok=True)

# Page A3 (1190.76 x 841.8 pt) à l'échelle 1:300 -> coordonnées réelles en mm
W_PT, H_PT = 1190.76, 841.8
F = 25.4 / 72.0 * 300.0          # pt -> mm réels
W_MM, H_MM = W_PT * F, H_PT * F  # ~126 030 x 89 105 mm

LAYERS = [
    ("FOND-ARCHI", 8), ("ELEC-ECL-LUM", 2), ("ELEC-ECL-SECU", 3),
    ("ELEC-ECL-CMD", 4), ("ELEC-PC-NORMAL", 7), ("ELEC-PC-SECOURU", 1),
    ("ELEC-PC-IT-ONDULE", 3), ("ELEC-TD", 6), ("ELEC-TEXTE", 7),
    ("ELEC-LEGENDE", 7), ("ELEC-CARTOUCHE", 7),
]
LAYER_PAR_SYMBOLE = {
    "pave": "ELEC-ECL-LUM", "downlight": "ELEC-ECL-LUM", "reglette": "ELEC-ECL-LUM",
    "etanche": "ELEC-ECL-LUM", "hublot": "ELEC-ECL-LUM", "suspension": "ELEC-ECL-LUM",
    "projecteur": "ELEC-ECL-LUM", "candelabre": "ELEC-ECL-LUM", "tl": "ELEC-ECL-LUM",
    "baes": "ELEC-ECL-SECU", "baeh": "ELEC-ECL-SECU", "sc": "ELEC-ECL-SECU",
    "dp": "ELEC-ECL-CMD",
    "pc": "ELEC-PC-NORMAL", "pce": "ELEC-PC-NORMAL", "pc20": "ELEC-PC-NORMAL",
    "pct": "ELEC-PC-NORMAL", "sca": "ELEC-PC-NORMAL",
    "pcs": "ELEC-PC-SECOURU",
    "pco": "ELEC-PC-IT-ONDULE", "gtl": "ELEC-PC-IT-ONDULE", "tri": "ELEC-PC-IT-ONDULE",
    "cpi": "ELEC-PC-IT-ONDULE", "les": "ELEC-PC-IT-ONDULE",
    "td": "ELEC-TD",
}
NOM_BLOC = {k: "ELEC_" + k.upper() for k in LAYER_PAR_SYMBOLE}


def fond_png(nom, page_idx):
    out = os.path.join(OUTDIR, f"fond_{nom}.png")
    if not os.path.exists(out):
        d = fitz.open(SRC)
        d[page_idx].get_pixmap(matrix=fitz.Matrix(3, 3)).save(out)
        d.close()
    return out


# ---------------------------------------------------------------------------
# Définition des blocs symboles (géométrie en mm réels, calque 0 -> ByBlock)
# ---------------------------------------------------------------------------
def _txt(blk, t, pos, h=220, valign=TA.MIDDLE_CENTER):
    blk.add_text(t, dxfattribs={"height": h, "style": "Standard"}
                 ).set_placement(pos, align=valign)


def _demi_disque(blk, r):
    pts = [(r * math.cos(math.radians(a)), r * math.sin(math.radians(a)))
           for a in range(0, 181, 15)]
    h = blk.add_hatch()
    h.paths.add_polyline_path(pts + [(-r, 0)], is_closed=True)


def definir_blocs(doc):
    B = {}

    def bloc(nom):
        blk = doc.blocks.new(name=nom)
        return blk

    blk = bloc("ELEC_PAVE")
    blk.add_lwpolyline([(-300, -300), (300, -300), (300, 300), (-300, 300)], close=True)
    blk.add_line((-300, -300), (300, 300)); blk.add_line((-300, 300), (300, -300))

    blk = bloc("ELEC_DOWNLIGHT")
    blk.add_circle((0, 0), 180)
    d = 180 * math.cos(math.pi / 4)
    blk.add_line((-d, -d), (d, d)); blk.add_line((-d, d), (d, -d))

    blk = bloc("ELEC_REGLETTE")
    blk.add_lwpolyline([(-600, -90), (600, -90), (600, 90), (-600, 90)], close=True)
    blk.add_line((-600, 0), (600, 0))

    blk = bloc("ELEC_ETANCHE")
    blk.add_lwpolyline([(-600, -90), (600, -90), (600, 90), (-600, 90)], close=True)
    blk.add_line((-600, 0), (600, 0)); _txt(blk, "IP65", (0, 220), 160)

    blk = bloc("ELEC_HUBLOT")
    blk.add_circle((0, 0), 180); blk.add_circle((0, 0), 90)

    blk = bloc("ELEC_SUSPENSION")
    blk.add_circle((0, 0), 150); blk.add_line((0, 150), (0, 330))

    blk = bloc("ELEC_PROJECTEUR")
    blk.add_lwpolyline([(-200, -140), (160, -140), (160, 140), (-200, 140)], close=True)
    blk.add_line((160, 0), (420, 0))
    blk.add_line((330, 80), (420, 0)); blk.add_line((330, -80), (420, 0))

    blk = bloc("ELEC_CANDELABRE")
    blk.add_circle((180, 0), 150)
    blk.add_line((30, 0), (-240, 0)); blk.add_line((-240, -190), (-240, 190))

    blk = bloc("ELEC_TL")
    blk.add_lwpolyline([(-750, -180), (750, -180), (750, 180), (-750, 180)], close=True)
    for i in (-375, 0, 375):
        blk.add_line((i, -180), (i, 180))
    _txt(blk, "TL", (0, 0), 170)

    blk = bloc("ELEC_GTL")
    blk.add_lwpolyline([(-900, -200), (900, -200), (900, 200), (-900, 200)], close=True)
    for i in (-450, 0, 450):
        blk.add_line((i, -200), (i, 200))
    _txt(blk, "GTL", (0, 0), 180)

    blk = bloc("ELEC_BAES")
    blk.add_lwpolyline([(-240, -150), (240, -150), (240, 150), (-240, 150)], close=True)
    _txt(blk, "S", (0, 0), 170)

    blk = bloc("ELEC_BAEH")
    blk.add_lwpolyline([(-280, -150), (280, -150), (280, 150), (-280, 150)], close=True)
    _txt(blk, "S+H", (0, 0), 140)

    blk = bloc("ELEC_SC")
    blk.add_solid([(0, 200), (-210, -160), (210, -160)])

    blk = bloc("ELEC_DP")
    pts = [(210 * math.cos(math.radians(a)), 210 * math.sin(math.radians(a)))
           for a in range(0, 181, 15)]
    blk.add_lwpolyline(pts)
    blk.add_line((-210, 0), (210, 0)); _txt(blk, "DP", (0, 90), 120)

    def prise(nom, fill=False, marque=None, antennes=1):
        blk = bloc(nom)
        pts = [(200 * math.cos(math.radians(a)), 200 * math.sin(math.radians(a)))
               for a in range(0, 181, 10)]
        blk.add_lwpolyline(pts)
        blk.add_line((-200, 0), (200, 0))
        if antennes == 1:
            blk.add_line((0, 200), (0, 420))
        else:
            for dx in (-100, 0, 100):
                blk.add_line((dx, 170 if dx else 200), (dx, 400))
        if fill:
            _demi_disque(blk, 200)
        if marque:
            _txt(blk, marque, (0, -320), 150)
        return blk

    prise("ELEC_PC")
    prise("ELEC_PCS", fill=True)
    prise("ELEC_PCO", marque=None); _txt(doc.blocks.get("ELEC_PCO"), "O", (330, 160), 160)
    prise("ELEC_PCE", marque="IP55")
    prise("ELEC_PC20", marque="20A")
    prise("ELEC_PCT", antennes=3)

    blk = bloc("ELEC_SCA")
    blk.add_line((-260, 0), (40, 0))
    h = blk.add_hatch(); h.paths.add_polyline_path(
        [(140 + 90 * math.cos(math.radians(a)), 90 * math.sin(math.radians(a)))
         for a in range(0, 360, 20)], is_closed=True)
    blk.add_circle((140, 0), 90)

    blk = bloc("ELEC_TD")
    blk.add_solid([(-450, -220), (450, -220), (-450, 220), (450, 220)])
    blk.add_lwpolyline([(-450, -220), (450, -220), (450, 220), (-450, 220)], close=True)

    blk = bloc("ELEC_TRI")
    blk.add_lwpolyline([(-340, -190), (340, -190), (340, 190), (-340, 190)], close=True)
    blk.add_circle((-100, 0), 100); blk.add_circle((100, 0), 100)

    blk = bloc("ELEC_CPI")
    blk.add_lwpolyline([(-260, -160), (260, -160), (260, 160), (-260, 160)], close=True)
    _txt(blk, "CPI", (0, 0), 150)

    blk = bloc("ELEC_LES")
    blk.add_line((0, 220), (0, 0))
    blk.add_line((-180, 0), (180, 0))
    blk.add_line((-120, -90), (120, -90))
    blk.add_line((-60, -180), (60, -180))
    return B


def XY(fx, fy):
    return fx * W_MM, (1.0 - fy) * H_MM


def construire_dxf(nom, page_idx, items, zones, titre):
    doc = ezdxf.new("R2010", setup=True)
    doc.header["$INSUNITS"] = 4      # millimètres
    doc.header["$MEASUREMENT"] = 1
    msp = doc.modelspace()
    for layer, col in LAYERS:
        doc.layers.add(layer, color=col)
    definir_blocs(doc)

    # --- fond de plan raster référencé, à l'échelle réelle ---
    png = fond_png(nom, page_idx)
    img = fitz.Pixmap(png)
    image_def = doc.add_image_def(filename=os.path.basename(png),
                                  size_in_pixel=(img.width, img.height))
    msp.add_image(image_def=image_def, insert=(0, 0), size_in_units=(W_MM, H_MM),
                  rotation=0, dxfattribs={"layer": "FOND-ARCHI"})

    # --- symboles ---
    for fx, fy, kind, lab in items:
        x, y = XY(fx, fy)
        msp.add_blockref(NOM_BLOC[kind], (x, y),
                         dxfattribs={"layer": LAYER_PAR_SYMBOLE[kind]})
        if lab:
            msp.add_text(lab, dxfattribs={"layer": "ELEC-TEXTE", "height": 550}
                         ).set_placement((x + 650, y - 750), align=TA.LEFT)
    for fx, fy, t in zones:
        x, y = XY(fx, fy)
        msp.add_text(t, dxfattribs={"layer": "ELEC-TEXTE", "height": 900}
                     ).set_placement((x, y), align=TA.LEFT)

    # --- légende ---
    lx, ly = W_MM + 3000, H_MM - 4000
    msp.add_text("LÉGENDE", dxfattribs={"layer": "ELEC-LEGENDE", "height": 1600}
                 ).set_placement((lx, ly), align=TA.LEFT)
    ly -= 3200
    for titre_sec, entrees in (("ÉCLAIRAGE", LEG_ECL), ("PRISES DE COURANT / FORCES", LEG_PC)):
        msp.add_text(titre_sec, dxfattribs={"layer": "ELEC-LEGENDE", "height": 1100}
                     ).set_placement((lx, ly), align=TA.LEFT)
        ly -= 2400
        for kind, texte in entrees:
            msp.add_blockref(NOM_BLOC[kind], (lx + 1200, ly + 250),
                             dxfattribs={"layer": LAYER_PAR_SYMBOLE[kind]})
            msp.add_text(texte, dxfattribs={"layer": "ELEC-LEGENDE", "height": 650}
                         ).set_placement((lx + 3200, ly), align=TA.LEFT)
            ly -= 2100
        ly -= 1200

    # --- cartouche ---
    cx, cy = W_MM + 3000, 9000
    for i, t in enumerate([
            "CENTRE DE DRÉPANOCYTOSE - COTONOU (BÉNIN)",
            titre,
            "Lot électricité - plan de principe APS - juin 2026 - ind. A",
            "Unités : mm (1:1) - vérif. échelle : entraxe des files = 8000 mm",
            "Calques ELEC-ECL-* / ELEC-PC-* activables séparément",
            "Réf. NF C 15-100, NF C 15-211 / CEI 60364-7-710, NF EN 12464-1, NF EN 1838"]):
        msp.add_text(t, dxfattribs={"layer": "ELEC-CARTOUCHE",
                                    "height": 1100 if i == 0 else 750}
                     ).set_placement((cx, cy - i * 1700), align=TA.LEFT)

    chemin = os.path.join(OUTDIR, f"plan_principe_elec_{nom.upper()}.dxf")
    doc.saveas(chemin)
    print("OK :", chemin)
    return chemin


def main():
    zones_rdc = [(0.555, 0.245, "ZONE URGENCES - GROUPE 2 - IT MÉDICAL"),
                 (0.16, 0.105, "LOCAUX TECHNIQUES : TGBT - GE - TRANSFO")]
    zones_r1 = [(0.52, 0.745, "LABORATOIRES DE RECHERCHE")]
    construire_dxf("rdc", 1, ECL_RDC + PC_RDC, zones_rdc,
                   "RDC - éclairage + prises (planches E-01/E-02)")
    construire_dxf("r1", 2, ECL_R1 + PC_R1, zones_r1,
                   "1er étage - éclairage + prises (planches E-03/E-04)")


if __name__ == "__main__":
    main()
