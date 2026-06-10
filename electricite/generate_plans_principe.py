# -*- coding: utf-8 -*-
"""
Plans de principe annotés ÉLECTRICITÉ (éclairage / prises de courant)
Centre de Drépanocytose - Cotonou. 4 planches A3 paysage sur fonds architecte.
Sortie : plans_principe_electricite_annotes.pdf
"""
import os
import fitz
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas as rcanvas

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "0210_SITE CENTRE DE DREPANOCYTOSE LQ 3.pdf")
OUT = os.path.join(HERE, "plans_principe_electricite_annotes.pdf")

VERT = colors.HexColor("#6aa84f")
GRIS = colors.HexColor("#444444")
ROUGE = colors.HexColor("#cc0000")
VERTF = colors.HexColor("#1b7a33")
BLEU = colors.HexColor("#0d47a1")
NOIR = colors.black

PAGE = landscape(A3)  # 420 x 297 mm
IW = 346 * mm
IH = IW * 841.8 / 1190.76
OX = 4 * mm
OY = (PAGE[1] - IH) / 2.0
LX = OX + IW + 4 * mm          # colonne légende
LW = PAGE[0] - LX - 4 * mm


def extraire(nom, page_idx):
    out = os.path.join(HERE, f"fond_{nom}.png")
    if not os.path.exists(out):
        d = fitz.open(SRC)
        d[page_idx].get_pixmap(matrix=fitz.Matrix(3, 3)).save(out)
        d.close()
    return out


# ---------------------------------------------------------------------------
# Symboles (dessin direct sur canvas)
# ---------------------------------------------------------------------------
def sym(c, k, x, y, s=1.0, halo=True):
    u = s * mm
    if halo:
        c.saveState()
        c.setFillColor(colors.white)
        c.setFillAlpha(0.72)
        c.setStrokeAlpha(0)
        c.circle(x, y, 3.2 * u, stroke=0, fill=1)
        c.restoreState()
    c.saveState()
    c.setLineWidth(0.9)
    c.setStrokeColor(NOIR)
    c.setFillColor(colors.white)

    def txt(t, dy=-0.9 * u, size=3.2 * s, col=NOIR):
        c.setFont("Helvetica-Bold", size)
        c.setFillColor(col)
        c.drawCentredString(x, y + dy, t)

    if k == "pave":          # L1 pavé LED
        c.setStrokeColor(BLEU)
        c.rect(x - 2.2 * u, y - 1.5 * u, 4.4 * u, 3 * u)
        c.line(x - 2.2 * u, y - 1.5 * u, x + 2.2 * u, y + 1.5 * u)
        c.line(x - 2.2 * u, y + 1.5 * u, x + 2.2 * u, y - 1.5 * u)
    elif k == "downlight":   # L2
        c.setStrokeColor(BLEU)
        c.circle(x, y, 1.6 * u)
        c.line(x - 1.1 * u, y - 1.1 * u, x + 1.1 * u, y + 1.1 * u)
        c.line(x - 1.1 * u, y + 1.1 * u, x + 1.1 * u, y - 1.1 * u)
    elif k == "reglette":    # L3
        c.setStrokeColor(BLEU)
        c.rect(x - 3 * u, y - 0.7 * u, 6 * u, 1.4 * u)
        c.line(x - 3 * u, y, x + 3 * u, y)
    elif k == "etanche":     # L4
        c.setStrokeColor(BLEU)
        c.rect(x - 3 * u, y - 0.7 * u, 6 * u, 1.4 * u)
        c.line(x - 3 * u, y, x + 3 * u, y)
        c.setFillColor(BLEU)
        c.setFont("Helvetica-Bold", 2.4 * s)
        c.drawCentredString(x, y + 1.1 * u, "IP65")
    elif k == "hublot":      # L5
        c.setStrokeColor(BLEU)
        c.circle(x, y, 1.6 * u)
        c.circle(x, y, 0.8 * u)
    elif k == "suspension":  # L7
        c.setStrokeColor(BLEU)
        c.circle(x, y, 1.4 * u)
        c.line(x, y + 1.4 * u, x, y + 2.6 * u)
    elif k == "projecteur":  # L8
        c.setStrokeColor(BLEU)
        c.rect(x - 1.8 * u, y - 1.2 * u, 3.2 * u, 2.4 * u)
        c.line(x + 1.4 * u, y, x + 3.4 * u, y)
        c.line(x + 2.6 * u, y + 0.7 * u, x + 3.4 * u, y)
        c.line(x + 2.6 * u, y - 0.7 * u, x + 3.4 * u, y)
    elif k == "candelabre":  # L9
        c.setStrokeColor(BLEU)
        c.circle(x + 1.6 * u, y, 1.3 * u)
        c.line(x + 0.3 * u, y, x - 2 * u, y)
        c.line(x - 2 * u, y - 1.6 * u, x - 2 * u, y + 1.6 * u)
    elif k == "tl":          # bandeau tête de lit
        c.setStrokeColor(BLEU)
        c.rect(x - 3.2 * u, y - 1.1 * u, 6.4 * u, 2.2 * u)
        for i in (1, 2, 3):
            c.line(x - 3.2 * u + i * 1.6 * u, y - 1.1 * u, x - 3.2 * u + i * 1.6 * u, y + 1.1 * u)
        txt("TL", dy=-0.95 * u, col=BLEU)
    elif k == "baes":
        c.setStrokeColor(VERTF)
        c.rect(x - 2 * u, y - 1.3 * u, 4 * u, 2.6 * u)
        txt("S", col=VERTF)
    elif k == "baeh":        # combiné BAES+BAEH
        c.setStrokeColor(VERTF)
        c.rect(x - 2.4 * u, y - 1.3 * u, 4.8 * u, 2.6 * u)
        txt("S+H", size=2.4 * s, col=VERTF)
    elif k == "sc":          # luminaire sur ASI / source centrale
        c.setFillColor(VERTF)
        c.setStrokeColor(VERTF)
        pth = c.beginPath()
        pth.moveTo(x, y + 1.7 * u)
        pth.lineTo(x - 1.8 * u, y - 1.3 * u)
        pth.lineTo(x + 1.8 * u, y - 1.3 * u)
        pth.close()
        c.drawPath(pth, stroke=1, fill=1)
    elif k == "dp":
        c.setStrokeColor(BLEU)
        c.arc(x - 1.8 * u, y - 1.8 * u, x + 1.8 * u, y + 1.8 * u, 0, 180)
        c.line(x - 1.8 * u, y, x + 1.8 * u, y)
        txt("DP", dy=0.4 * u, size=2.4 * s, col=BLEU)
    elif k in ("pc", "pcs", "pco", "pce"):
        col = {"pc": NOIR, "pcs": ROUGE, "pco": VERTF, "pce": NOIR}[k]
        c.setStrokeColor(col)
        c.arc(x - 1.7 * u, y - 1.7 * u, x + 1.7 * u, y + 1.7 * u, 0, 180)
        c.line(x, y + 1.7 * u, x, y + 3 * u)
        c.line(x - 1.7 * u, y, x + 1.7 * u, y)
        if k == "pcs":
            c.setFillColor(ROUGE)
            pth = c.beginPath()
            pth.moveTo(x - 1.7 * u, y)
            pth.arcTo(x - 1.7 * u, y - 1.7 * u, x + 1.7 * u, y + 1.7 * u, 0, 180)
            pth.close()
            c.drawPath(pth, stroke=1, fill=1)
        if k == "pco":
            c.setFont("Helvetica-Bold", 2.6 * s)
            c.setFillColor(VERTF)
            c.drawCentredString(x + 2.6 * u, y + 1.2 * u, "O")
        if k == "pce":
            c.setFont("Helvetica-Bold", 2.2 * s)
            c.setFillColor(NOIR)
            c.drawCentredString(x, y - 2.6 * u, "IP55")
    elif k == "pc20":
        c.arc(x - 1.7 * u, y - 1.7 * u, x + 1.7 * u, y + 1.7 * u, 0, 180)
        c.line(x, y + 1.7 * u, x, y + 3 * u)
        c.line(x - 1.7 * u, y, x + 1.7 * u, y)
        txt("20A", dy=-2.8 * u, size=2.2 * s)
    elif k == "pct":
        c.arc(x - 1.7 * u, y - 1.7 * u, x + 1.7 * u, y + 1.7 * u, 0, 180)
        for dx in (-0.8 * u, 0, 0.8 * u):
            c.line(x + dx, y + (1.7 * u if dx == 0 else 1.45 * u), x + dx, y + 2.9 * u)
        c.line(x - 1.7 * u, y, x + 1.7 * u, y)
    elif k == "sca":
        c.line(x - 2.2 * u, y, x + 0.4 * u, y)
        c.setFillColor(NOIR)
        c.circle(x + 1.2 * u, y, 0.8 * u, stroke=1, fill=1)
    elif k == "gtl":         # gaine tête de lit IT médical
        c.setStrokeColor(VERTF)
        c.rect(x - 3.6 * u, y - 1.2 * u, 7.2 * u, 2.4 * u)
        for i in (1, 2, 3):
            c.line(x - 3.6 * u + i * 1.8 * u, y - 1.2 * u, x - 3.6 * u + i * 1.8 * u, y + 1.2 * u)
        txt("GTL", dy=-0.9 * u, size=2.6 * s, col=VERTF)
    elif k == "td":
        c.setFillColor(NOIR)
        c.rect(x - 2.6 * u, y - 1.3 * u, 5.2 * u, 2.6 * u, stroke=1, fill=1)
    elif k == "tri":
        c.setStrokeColor(VERTF)
        c.rect(x - 3 * u, y - 1.6 * u, 6 * u, 3.2 * u)
        c.circle(x - 0.9 * u, y, 0.9 * u)
        c.circle(x + 0.9 * u, y, 0.9 * u)
    elif k == "cpi":
        c.setStrokeColor(VERTF)
        c.rect(x - 2.4 * u, y - 1.4 * u, 4.8 * u, 2.8 * u)
        txt("CPI", size=2.6 * s, col=VERTF)
    elif k == "les":
        c.setStrokeColor(VERTF)
        c.line(x, y + 1.9 * u, x, y)
        c.line(x - 1.6 * u, y, x + 1.6 * u, y)
        c.line(x - 1.05 * u, y - 0.75 * u, x + 1.05 * u, y - 0.75 * u)
        c.line(x - 0.5 * u, y - 1.5 * u, x + 0.5 * u, y - 1.5 * u)
    c.restoreState()


def label(c, x, y, t, col=GRIS, dx=3.2, dy=0, size=3.4, halo=True):
    c.saveState()
    c.setFont("Helvetica-Bold", size)
    w = c.stringWidth(t, "Helvetica-Bold", size)
    px, py = x + dx * mm, y + dy * mm
    if halo:
        c.setFillColor(colors.white)
        c.setFillAlpha(0.72)
        c.rect(px - 0.4 * mm, py - 0.5 * mm, w + 0.8 * mm, size + 0.6, stroke=0, fill=1)
        c.setFillAlpha(1)
    c.setFillColor(col)
    c.drawString(px, py, t)
    c.restoreState()


def XY(fx, fy):
    return OX + fx * IW, OY + (1 - fy) * IH


# ---------------------------------------------------------------------------
# Habillage de planche : cadre, légende, cartouche
# ---------------------------------------------------------------------------
def habillage(c, fond, titre, sstitre, entrees_legende, notes):
    c.drawImage(fond, OX, OY, IW, IH)
    c.setStrokeColor(GRIS)
    c.setLineWidth(0.6)
    c.rect(OX, OY, IW, IH)
    # bandeau titre sur le plan (recouvre le cartouche DCE du fond)
    c.setFillColor(VERT)
    c.rect(OX, OY + IH - 13 * mm, 112 * mm, 13 * mm, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 9.5)
    c.drawString(OX + 3 * mm, OY + IH - 6 * mm, titre)
    c.setFont("Helvetica", 7)
    c.drawString(OX + 3 * mm, OY + IH - 10.8 * mm, sstitre)
    # panneau légende
    c.setFillColor(colors.white)
    c.setStrokeColor(GRIS)
    c.rect(LX, OY, LW, IH, stroke=1, fill=1)
    c.setFillColor(VERT)
    c.rect(LX, OY + IH - 8 * mm, LW, 8 * mm, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(LX + 2.5 * mm, OY + IH - 5.5 * mm, "LÉGENDE")
    yy = OY + IH - 15 * mm
    for kind, txt_ in entrees_legende:
        sym(c, kind, LX + 6.5 * mm, yy, s=0.95, halo=False)
        c.setFillColor(GRIS)
        c.setFont("Helvetica", 5.6)
        lignes = []
        mot = ""
        for w in txt_.split():
            if c.stringWidth(mot + " " + w, "Helvetica", 5.6) > LW - 16 * mm:
                lignes.append(mot)
                mot = w
            else:
                mot = (mot + " " + w).strip()
        lignes.append(mot)
        ty = yy + (len(lignes) - 1) * 1.1 * mm
        for ln in lignes:
            c.drawString(LX + 13 * mm, ty - 0.8 * mm, ln)
            ty -= 2.4 * mm
        yy -= max(7.2 * mm, (len(lignes) * 2.4 + 3.4) * mm)
    # notes + cartouche
    c.setFont("Helvetica-Oblique", 5.2)
    c.setFillColor(GRIS)
    ty = OY + 26 * mm
    for n in notes:
        c.drawString(LX + 2 * mm, ty, n)
        ty -= 2.6 * mm
    c.setStrokeColor(GRIS)
    c.line(LX, OY + 17 * mm, LX + LW, OY + 17 * mm)
    c.setFont("Helvetica-Bold", 6.2)
    c.setFillColor(NOIR)
    c.drawString(LX + 2 * mm, OY + 13 * mm, "CENTRE DE DRÉPANOCYTOSE")
    c.drawString(LX + 2 * mm, OY + 10 * mm, "COTONOU - BÉNIN")
    c.setFont("Helvetica", 5.4)
    c.drawString(LX + 2 * mm, OY + 6.5 * mm, "Lot électricité - plan de principe APS")
    c.drawString(LX + 2 * mm, OY + 3.5 * mm, "Juin 2026 - ind. A - éch. ≈ 1:300 (A3)")


# ---------------------------------------------------------------------------
# Données d'implantation (fractions du fond de plan ; x→droite, y→bas)
# ---------------------------------------------------------------------------
def chambres_rdc():
    """(fx, fy, nom) têtes de lit RDC."""
    return [
        (0.405, 0.290, "Hospi jour 2 lits"),
        (0.458, 0.290, "Soins int. Ad. 2 lits"),
        (0.410, 0.372, "Hospi enfants 2 lits"),
        (0.465, 0.372, "Soins int. Enf. 2 lits"),
    ]


ECL_RDC = (
    # corridors / circulations : downlights
    [(x, 0.342, "downlight", "") for x in (0.315, 0.36, 0.405, 0.45, 0.495)]
    + [(x, 0.690, "downlight", "") for x in (0.40, 0.44, 0.48, 0.52)]
    + [(0.350, 0.678, "downlight", ""), (0.272, 0.43, "downlight", ""),
       (0.272, 0.49, "downlight", ""), (0.585, 0.315, "downlight", ""),
       (0.605, 0.345, "downlight", "")]
    # locaux
    + [(0.355, 0.295, "pave", "L1 - échographie"),
       (0.505, 0.285, "pave", "L1 - surv. soins"),
       (0.340, 0.645, "pave", "L1 - réunion"),
       (0.345, 0.725, "pave", "L1 - bureaux"),
       (0.420, 0.640, "pave", "L1 - pharmacie"),
       (0.470, 0.735, "pave", "L1 - postes consult. (x5)"),
       (0.560, 0.690, "suspension", "L7 - accueil"),
       (0.575, 0.715, "downlight", "")]
    # têtes de lit + secours
    + [(fx, fy, "tl", "") for fx, fy, _ in chambres_rdc()]
    + [(0.530, 0.300, "tl", "déchocage 1"), (0.530, 0.362, "tl", "déchocage 2"),
       (0.556, 0.330, "tl", "box examen")]
    + [(0.476, 0.300, "sc", ""), (0.483, 0.382, "sc", ""),
       (0.546, 0.310, "sc", ""), (0.546, 0.372, "sc", "ASI groupe 2")]
    # services / techniques
    + [(0.275, 0.310, "etanche", "L4 - cuisine"),
       (0.205, 0.150, "etanche", ""), (0.255, 0.150, "etanche", ""),
       (0.300, 0.150, "etanche", "L4 - locaux techniques"),
       (0.270, 0.690, "hublot", "L5 - vestiaires"),
       (0.256, 0.445, "hublot", ""), (0.276, 0.527, "hublot", "L5 - ESC 2"),
       (0.612, 0.527, "hublot", "L5 - ESC 1"),
       (0.716, 0.152, "hublot", "L5 - guérite")]
    + [(0.262, 0.452, "dp", ""), (0.282, 0.535, "dp", ""), (0.268, 0.698, "dp", "")]
    # sécurité
    + [(0.335, 0.335, "baeh", ""), (0.475, 0.335, "baeh", "BAES+BAEH (sommeil)"),
       (0.452, 0.695, "baes", ""), (0.530, 0.695, "baes", ""),
       (0.355, 0.682, "baes", ""), (0.272, 0.46, "baes", ""),
       (0.592, 0.298, "baes", ""), (0.645, 0.330, "baes", "sortie urgences"),
       (0.645, 0.624, "baes", "sortie consult."),
       (0.278, 0.545, "baes", ""), (0.610, 0.545, "baes", ""),
       (0.560, 0.700, "baes", "anti-panique attente")]
    # extérieur
    + [(0.300, 0.095, "candelabre", ""), (0.435, 0.095, "candelabre", "L9 - parking nord"),
       (0.570, 0.095, "candelabre", ""),
       (0.745, 0.300, "candelabre", ""), (0.745, 0.455, "candelabre", "L9 - parking est"),
       (0.748, 0.640, "candelabre", ""), (0.160, 0.790, "candelabre", ""),
       (0.410, 0.870, "candelabre", "L9 - parvis sud"),
       (0.660, 0.330, "projecteur", "L8 - entrée urgences"),
       (0.660, 0.622, "projecteur", "L8 - entrée consult."),
       (0.628, 0.252, "projecteur", "L8 - SAS ambulance")]
)

PC_RDC = (
    # urgences / soins intensifs : IT médical
    [(0.530, 0.296, "gtl", ""), (0.530, 0.366, "gtl", "GTL déchocage IT méd."),
     (0.458, 0.286, "gtl", "GTL soins int. adultes"),
     (0.465, 0.376, "gtl", "GTL soins int. enfants"),
     (0.556, 0.326, "pcs", "box examen"),
     (0.512, 0.262, "tri", ""), (0.512, 0.292, "cpi", "2 x TRI 8 kVA + CPI"),
     (0.545, 0.300, "les", ""), (0.548, 0.370, "les", ""),
     (0.470, 0.300, "les", ""), (0.477, 0.388, "les", "LES groupe 2"),
     (0.585, 0.310, "pc", ""), (0.598, 0.322, "pco", "accueil urgences"),
     (0.628, 0.296, "pc", "SAS")]
    # chambres (têtes de lit secourues)
    + [(0.405, 0.286, "pcs", ""), (0.410, 0.368, "pcs", "PC rouges têtes de lit"),
       (0.405, 0.318, "pc", ""), (0.410, 0.398, "pc", "")]
    + [(0.505, 0.290, "pc", ""), (0.512, 0.302, "pco", "surv. soins")]
    # nord / services
    + [(0.355, 0.290, "pcs", ""), (0.362, 0.305, "pco", "échographie"),
       (0.275, 0.305, "pce", ""), (0.282, 0.320, "pct", "cuisine"),
       (0.205, 0.146, "pce", ""), (0.300, 0.146, "pce", "locaux techn."),
       (0.190, 0.160, "sca", "surpresseur"),
       (0.716, 0.158, "pc", "guérite")]
    # sud
    + [(0.408, 0.636, "pco", ""), (0.420, 0.650, "pc", ""),
       (0.436, 0.628, "pc20", "CF pharmacie (secouru)"),
       (0.398, 0.706, "pc", "bur. pharmacien"),
       (0.318, 0.726, "pco", ""), (0.348, 0.726, "pco", ""), (0.378, 0.726, "pco", "bureaux : 3 PC + PCO/poste"),
       (0.335, 0.648, "pc", ""), (0.345, 0.660, "pco", "réunion"),
       (0.270, 0.685, "pc", "vestiaires")]
    + [(x, 0.735, "pcs", "") for x in (0.415, 0.455, 0.495, 0.535)]
    + [(x, 0.752, "pco", "") for x in (0.425, 0.465, 0.505)]
    + [(0.545, 0.752, "pco", "consult. : 6 PC dont 2 PCS + 2 PCO"),
       (0.560, 0.685, "pco", "affichage"), (0.548, 0.662, "pc", ""),
       (0.582, 0.700, "pc", "")]
    # circulations / TD
    + [(0.36, 0.342, "pc", ""), (0.46, 0.342, "pc", "PC entretien circul."),
       (0.44, 0.690, "pc", ""), (0.272, 0.47, "pc", "")]
    + [(0.286, 0.152, "td", "TGBT+GE"), (0.328, 0.152, "td", "TR 630 kVA"),
       (0.262, 0.552, "td", "TD RDC"), (0.514, 0.318, "td", "TD URG (secouru)"),
       (0.600, 0.660, "td", "TD CONS")]
)


def chambres_r1():
    nord = [(x, 0.292) for x in (0.310, 0.357, 0.404, 0.464, 0.512, 0.562, 0.607)]
    sud = [(x, 0.660) for x in (0.282, 0.337, 0.392, 0.447, 0.497)]
    return nord, sud


N_R1, S_R1 = chambres_r1()

ECL_R1 = (
    [(fx, fy, "tl", "") for fx, fy in N_R1]
    + [(fx, fy, "tl", "") for fx, fy in S_R1]
    + [(N_R1[3][0], N_R1[3][1] - 0.0, "tl", "")]  # repère
    # circulations
    + [(x, 0.357, "downlight", "") for x in (0.32, 0.37, 0.42, 0.47, 0.52, 0.57)]
    + [(x, 0.585, "downlight", "") for x in (0.30, 0.35, 0.40, 0.45, 0.50)]
    + [(0.300, 0.45, "downlight", ""), (0.594, 0.45, "downlight", ""),
       (0.600, 0.555, "downlight", "accueil étage")]
    # laboratoires
    + [(0.540, 0.625, "pave", ""), (0.540, 0.672, "pave", ""),
       (0.600, 0.625, "pave", ""), (0.600, 0.672, "pave", "L1 - laboratoires IP54")]
    + [(0.276, 0.292, "reglette", "L3 - serv. distribution"),
       (0.432, 0.292, "reglette", "L3 - local entretien"),
       (0.330, 0.228, "hublot", "L5 - balcons"),
       (0.278, 0.50, "hublot", ""), (0.612, 0.50, "hublot", "L5 - escaliers")]
    + [(0.283, 0.508, "dp", ""), (0.607, 0.508, "dp", "")]
    # sécurité (étage à sommeil : BAES+BAEH)
    + [(0.335, 0.350, "baeh", ""), (0.435, 0.350, "baeh", ""),
       (0.535, 0.350, "baeh", "BAES+BAEH circulations"),
       (0.325, 0.592, "baeh", ""), (0.425, 0.592, "baeh", ""),
       (0.520, 0.592, "baeh", ""),
       (0.300, 0.47, "baes", ""), (0.594, 0.47, "baes", ""),
       (0.282, 0.522, "baes", "ESC 2"), (0.610, 0.522, "baes", "ESC 1"),
       (0.560, 0.648, "baes", "")]
)

PC_R1 = (
    # chambres : 2 PCS tête de lit + PC
    [(fx, fy - 0.006, "pcs", "") for fx, fy in N_R1]
    + [(fx, fy + 0.028, "pc", "") for fx, fy in N_R1]
    + [(fx, fy - 0.028, "pc", "") for fx, fy in S_R1]
    + [(fx, fy + 0.006, "pcs", "") for fx, fy in S_R1]
    + [(0.628, 0.30, "pcs", "PC rouges têtes de lit (x2/lit)")]
    # laboratoires
    + [(0.532, 0.618, "pcs", ""), (0.548, 0.618, "pc", "bandeaux paillasses (4 PC/ml)"),
       (0.532, 0.664, "pc", ""), (0.548, 0.664, "pcs", ""),
       (0.592, 0.618, "pco", "acquisition"),
       (0.556, 0.692, "pc20", "congél. -80 °C (secouru + alarme)"),
       (0.604, 0.692, "pct", "autoclave 3P+N+T"),
       (0.522, 0.605, "les", "LES groupe 1")]
    # supports / accueil
    + [(0.276, 0.286, "pc", ""), (0.283, 0.300, "pco", "serv. distribution"),
       (0.432, 0.286, "pc", "entretien"),
       (0.596, 0.560, "pc", ""), (0.606, 0.572, "pco", "accueil étage")]
    # circulations + TD
    + [(0.36, 0.357, "pc", ""), (0.50, 0.357, "pc", "PC entretien (1/10-15 m)"),
       (0.34, 0.585, "pc", ""), (0.47, 0.585, "pc", "")]
    + [(0.268, 0.470, "td", "TD R+1"), (0.522, 0.630, "td", "TD LABO (secouru)")]
)

LEG_ECL = [
    ("pave", "L1 - pavé LED 600x600 UGR<19 (IP54 zones de soins / labos)"),
    ("downlight", "L2 - downlight LED - circulations, accueils"),
    ("reglette", "L3 - réglette LED - locaux supports / stockage"),
    ("etanche", "L4 - réglette LED étanche IP65 - cuisine, locaux techniques"),
    ("hublot", "L5 - hublot LED IP44 - sanitaires, escaliers, balcons"),
    ("suspension", "L7 - suspension décorative - accueil"),
    ("projecteur", "L8 - projecteur LED ext. IP66 - entrées, SAS ambulance"),
    ("candelabre", "L9 - candélabre LED 4-5 m IP66 (amb. saline) - parkings, parvis"),
    ("tl", "TL - bandeau tête de lit : général + lecture + examen + veille"),
    ("sc", "SC - luminaire repris sur ASI (locaux groupe 2)"),
    ("baes", "BAES évacuation 45 lm SATI"),
    ("baeh", "BAES+BAEH combiné (zones à sommeil) 8 lm / 5 h"),
    ("dp", "DP - détecteur de présence"),
]
LEG_PC = [
    ("pc", "PC 2P+T 16 A - réseau NORMAL (blanc), h=0,30 m sauf soins 0,90-1,20 m"),
    ("pcs", "PCS 2P+T 16 A - réseau SECOURU GE (rouge)"),
    ("pco", "PCO 2P+T 16 A - réseau ONDULÉ ASI / détrompé (vert)"),
    ("pce", "PCE 2P+T 16 A étanche IP55"),
    ("pc20", "Circuit spécialisé 20 A (congél. -80 °C, chambre froide CF)"),
    ("pct", "Prise 3P+N+T 16/32 A (NF EN 60309)"),
    ("sca", "Sortie de câble / attente force (CVC, équipt fixe)"),
    ("gtl", "Gaine tête de lit groupe 2 : 8-12 PC sur 2 circuits IT médical"),
    ("tri", "Transformateur d'isolement médical 230/230 V"),
    ("cpi", "CPI - contrôleur permanent d'isolement, report poste de soins"),
    ("les", "LES - liaison équipotentielle supplémentaire"),
    ("td", "Tableau électrique (TGBT / divisionnaire), réserve 30 %"),
]
NOTES = [
    "Implantations indicatives de principe (APS) - calepinage et",
    "quantités définitifs en phase PRO (calculs DiaLux / Caneco).",
    "Réf. : NF C 15-100, NF C 15-211 / CEI 60364-7-710,",
    "NF EN 12464-1, NF EN 1838 - fond : Koffi & Diabaté 09/2025.",
]


def planche(c, fond, titre, sstitre, items, leg, extra_labels=()):
    habillage(c, fond, titre, sstitre, leg, NOTES)
    for fx, fy, kind, lab in items:
        x, y = XY(fx, fy)
        sym(c, kind, x, y, s=0.78)
        if lab:
            label(c, x, y, lab)
    for fx, fy, t, col in extra_labels:
        x, y = XY(fx, fy)
        label(c, x, y, t, col=col, dx=0, size=4.2)
    c.showPage()


def main():
    fond_rdc = extraire("rdc", 1)
    fond_r1 = extraire("r1", 2)
    c = rcanvas.Canvas(OUT, pagesize=PAGE)
    c.setTitle("Plans de principe électricité annotés - Centre de Drépanocytose Cotonou")
    zones_rdc = [(0.575, 0.255, "ZONE URGENCES / GROUPE 2 - IT MÉDICAL", ROUGE),
                 (0.17, 0.115, "LOCAUX TECHNIQUES : TGBT - GE - TRANSFO", GRIS)]
    planche(c, fond_rdc, "PLAN DE PRINCIPE ÉCLAIRAGE - RDC",
            "éclairage normal, sécurité et extérieur - planche E-01", ECL_RDC, LEG_ECL, zones_rdc)
    planche(c, fond_rdc, "PLAN DE PRINCIPE PRISES DE COURANT - RDC",
            "réseaux normal / secouru / ondulé-IT médical - planche E-02", PC_RDC, LEG_PC, zones_rdc)
    planche(c, fond_r1, "PLAN DE PRINCIPE ÉCLAIRAGE - 1ER ÉTAGE",
            "hospitalisation et laboratoires - planche E-03", ECL_R1, LEG_ECL,
            [(0.55, 0.74, "LABORATOIRES DE RECHERCHE", colors.HexColor("#7b4fa0"))])
    planche(c, fond_r1, "PLAN DE PRINCIPE PRISES DE COURANT - 1ER ÉTAGE",
            "hospitalisation et laboratoires - planche E-04", PC_R1, LEG_PC,
            [(0.55, 0.74, "LABORATOIRES DE RECHERCHE", colors.HexColor("#7b4fa0"))])
    c.save()
    print("OK :", OUT)


if __name__ == "__main__":
    main()
