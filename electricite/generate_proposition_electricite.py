# -*- coding: utf-8 -*-
"""
Génération de la proposition de principe ÉLECTRICITÉ
Centre de Drépanocytose - Cotonou (Bénin)
Sortie : proposition_principe_electricite.pdf
"""
import os
import fitz  # PyMuPDF : extraction des plans du dossier architecte

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
    TableStyle, PageBreak, Image, Flowable, NextPageTemplate, KeepTogether,
)

HERE = os.path.dirname(os.path.abspath(__file__))
SRC_PDF = os.path.join(HERE, "..", "0210_SITE CENTRE DE DREPANOCYTOSE LQ 3.pdf")
OUT_PDF = os.path.join(HERE, "proposition_principe_electricite.pdf")

VERT = colors.HexColor("#6aa84f")
GRIS = colors.HexColor("#444444")
ROUGE = colors.HexColor("#cc0000")
VERT_F = colors.HexColor("#2e7d32")
ORANGE = colors.HexColor("#e69138")
BLEU = colors.HexColor("#1f5c99")
FOND = colors.HexColor("#eef3ea")

styles = getSampleStyleSheet()
S = {}
S["titre"] = ParagraphStyle("titre", parent=styles["Title"], fontName="Helvetica-Bold",
                            fontSize=24, leading=30, textColor=GRIS)
S["soustitre"] = ParagraphStyle("soustitre", parent=styles["Title"], fontName="Helvetica",
                                fontSize=14, leading=20, textColor=VERT)
S["h1"] = ParagraphStyle("h1", parent=styles["Heading1"], fontName="Helvetica-Bold",
                         fontSize=14, leading=18, textColor=VERT, spaceBefore=14, spaceAfter=6)
S["h2"] = ParagraphStyle("h2", parent=styles["Heading2"], fontName="Helvetica-Bold",
                         fontSize=11.5, leading=15, textColor=GRIS, spaceBefore=10, spaceAfter=4)
S["corps"] = ParagraphStyle("corps", parent=styles["Normal"], fontName="Helvetica",
                            fontSize=9.5, leading=13.5, alignment=TA_JUSTIFY, spaceAfter=5)
S["puce"] = ParagraphStyle("puce", parent=S["corps"], leftIndent=10, bulletIndent=2, spaceAfter=2.5)
S["cell"] = ParagraphStyle("cell", parent=styles["Normal"], fontName="Helvetica",
                           fontSize=8.2, leading=10.5)
S["cellb"] = ParagraphStyle("cellb", parent=S["cell"], fontName="Helvetica-Bold")
S["cellc"] = ParagraphStyle("cellc", parent=S["cell"], alignment=TA_CENTER)
S["note"] = ParagraphStyle("note", parent=S["corps"], fontSize=8, leading=11,
                           textColor=colors.HexColor("#666666"))
S["legende_fig"] = ParagraphStyle("legende_fig", parent=S["note"], alignment=TA_CENTER, spaceBefore=2)


def p(texte, style="corps"):
    return Paragraph(texte, S[style])


def puce(texte):
    return Paragraph(texte, S["puce"], bulletText="–")


def entete_pied(canv, doc):
    canv.saveState()
    w, h = doc.pagesize
    canv.setStrokeColor(VERT)
    canv.setLineWidth(0.8)
    canv.line(15 * mm, h - 12 * mm, w - 15 * mm, h - 12 * mm)
    canv.setFont("Helvetica", 7)
    canv.setFillColor(GRIS)
    canv.drawString(15 * mm, h - 10 * mm,
                    "CENTRE DE DRÉPANOCYTOSE - COTONOU (BÉNIN)")
    canv.drawRightString(w - 15 * mm, h - 10 * mm,
                         "LOT ÉLECTRICITÉ - PROPOSITION DE PRINCIPE - PHASE APS")
    canv.line(15 * mm, 12 * mm, w - 15 * mm, 12 * mm)
    canv.drawString(15 * mm, 8.5 * mm, "Juin 2026 - indice A - document de principe, à valider en phase PRO/EXE")
    canv.drawRightString(w - 15 * mm, 8.5 * mm, "Page %d" % canv.getPageNumber())
    canv.restoreState()


# ----------------------------------------------------------------------------
# Symboles de légende (dessins vectoriels simplifiés, inspirés NF C 03 / CEI 60617)
# ----------------------------------------------------------------------------
class Symbole(Flowable):
    def __init__(self, kind, w=18 * mm, h=9 * mm):
        super().__init__()
        self.kind, self.width, self.height = kind, w, h

    def wrap(self, aw, ah):
        return self.width, self.height

    def draw(self):
        c = self.canv
        cx, cy = self.width / 2.0, self.height / 2.0
        c.setLineWidth(1)
        c.setStrokeColor(colors.black)
        c.setFillColor(colors.white)
        k = self.kind

        def cercle(r, fill=0):
            c.circle(cx, cy, r, stroke=1, fill=fill)

        def texte(t, dy=-2.6, size=5.5, col=colors.black):
            c.setFont("Helvetica-Bold", size)
            c.setFillColor(col)
            c.drawCentredString(cx, cy + dy, t)
            c.setFillColor(colors.white)

        if k == "pave600":
            c.rect(cx - 5 * mm, cy - 5 * mm * 0.6, 10 * mm, 6 * mm)
            c.line(cx - 5 * mm, cy - 3 * mm, cx + 5 * mm, cy + 3 * mm)
            c.line(cx - 5 * mm, cy + 3 * mm, cx + 5 * mm, cy - 3 * mm)
        elif k == "downlight":
            cercle(3 * mm)
            c.line(cx - 2.1 * mm, cy - 2.1 * mm, cx + 2.1 * mm, cy + 2.1 * mm)
            c.line(cx - 2.1 * mm, cy + 2.1 * mm, cx + 2.1 * mm, cy - 2.1 * mm)
        elif k == "reglette":
            c.rect(cx - 7 * mm, cy - 1.4 * mm, 14 * mm, 2.8 * mm)
            c.line(cx - 7 * mm, cy, cx + 7 * mm, cy)
        elif k == "etanche":
            c.rect(cx - 7 * mm, cy - 1.4 * mm, 14 * mm, 2.8 * mm)
            c.line(cx - 7 * mm, cy, cx + 7 * mm, cy)
            c.setFont("Helvetica-Bold", 5)
            c.setFillColor(colors.black)
            c.drawCentredString(cx, cy + 2.2 * mm, "IP65")
            c.setFillColor(colors.white)
        elif k == "hublot":
            cercle(3 * mm)
            cercle(1.6 * mm)
        elif k == "applique":
            c.rect(cx - 4 * mm, cy - 1.2 * mm, 8 * mm, 2.4 * mm, fill=0)
            c.line(cx - 4 * mm, cy - 2.6 * mm, cx + 4 * mm, cy - 2.6 * mm)
        elif k == "bandeau_lit":
            c.rect(cx - 8 * mm, cy - 2 * mm, 16 * mm, 4 * mm)
            for i in range(1, 4):
                x = cx - 8 * mm + i * 4 * mm
                c.line(x, cy - 2 * mm, x, cy + 2 * mm)
            texte("TL", dy=-1.8, size=5)
        elif k == "suspension":
            cercle(2.6 * mm)
            c.line(cx, cy + 2.6 * mm, cx, cy + 4.5 * mm)
        elif k == "projecteur":
            c.rect(cx - 3 * mm, cy - 2 * mm, 6 * mm, 4 * mm)
            c.line(cx + 3 * mm, cy, cx + 6.5 * mm, cy)
            c.line(cx + 5 * mm, cy + 1.2 * mm, cx + 6.5 * mm, cy)
            c.line(cx + 5 * mm, cy - 1.2 * mm, cx + 6.5 * mm, cy)
        elif k == "candelabre":
            cercle(2.2 * mm)
            c.line(cx - 2.2 * mm, cy, cx - 6 * mm, cy)
            c.line(cx - 6 * mm, cy - 3 * mm, cx - 6 * mm, cy + 3 * mm)
        elif k == "baes":
            c.rect(cx - 4.5 * mm, cy - 2.6 * mm, 9 * mm, 5.2 * mm)
            texte("S", dy=-2.0, size=6)
        elif k == "baeh":
            c.rect(cx - 4.5 * mm, cy - 2.6 * mm, 9 * mm, 5.2 * mm)
            texte("H", dy=-2.0, size=6)
        elif k == "secours_sc":
            c.setFillColor(colors.black)
            pth = c.beginPath()
            pth.moveTo(cx, cy + 3 * mm)
            pth.lineTo(cx - 3.2 * mm, cy - 2.4 * mm)
            pth.lineTo(cx + 3.2 * mm, cy - 2.4 * mm)
            pth.close()
            c.drawPath(pth, stroke=1, fill=1)
            c.setFillColor(colors.white)
        elif k == "inter_sa":
            cercle(1.8 * mm, fill=1)
            c.line(cx + 1.2 * mm, cy + 1.2 * mm, cx + 4 * mm, cy + 4 * mm)
            c.line(cx + 4 * mm, cy + 4 * mm, cx + 5.6 * mm, cy + 3.2 * mm)
        elif k == "inter_vv":
            cercle(1.8 * mm, fill=1)
            for dx in (0, 1.8 * mm):
                c.line(cx + 1.2 * mm + dx * 0.4, cy + 1.2 * mm, cx + 4 * mm + dx, cy + 4 * mm)
                c.line(cx + 4 * mm + dx, cy + 4 * mm, cx + 5.4 * mm + dx, cy + 3.2 * mm)
        elif k == "bp":
            cercle(2.6 * mm)
            cercle(1.2 * mm, fill=1)
        elif k == "detecteur":
            pth = c.beginPath()
            pth.moveTo(cx - 4 * mm, cy - 2 * mm)
            pth.lineTo(cx + 4 * mm, cy - 2 * mm)
            c.drawPath(pth)
            c.arc(cx - 4 * mm, cy - 6 * mm, cx + 4 * mm, cy + 2 * mm, 0, 180)
            texte("DP", dy=0.6, size=5)
        elif k in ("pc16", "pc16_sec", "pc16_ond", "pc_etanche"):
            col = {"pc16": colors.black, "pc16_sec": ROUGE,
                   "pc16_ond": VERT_F, "pc_etanche": colors.black}[k]
            c.setStrokeColor(col)
            c.arc(cx - 3 * mm, cy - 3 * mm, cx + 3 * mm, cy + 3 * mm, 0, 180)
            c.line(cx, cy + 3 * mm, cx, cy + 5.5 * mm)
            c.line(cx - 3 * mm, cy, cx + 3 * mm, cy)
            if k == "pc16_sec":
                c.setFillColor(ROUGE)
                pth = c.beginPath()
                pth.moveTo(cx - 3 * mm, cy)
                pth.arcTo(cx - 3 * mm, cy - 3 * mm, cx + 3 * mm, cy + 3 * mm, 0, 180)
                pth.close()
                c.drawPath(pth, stroke=1, fill=1)
                c.setFillColor(colors.white)
            if k == "pc16_ond":
                c.setFont("Helvetica-Bold", 5)
                c.setFillColor(VERT_F)
                c.drawCentredString(cx + 5 * mm, cy + 2 * mm, "O")
                c.setFillColor(colors.white)
            if k == "pc_etanche":
                c.setFont("Helvetica-Bold", 4.6)
                c.setFillColor(colors.black)
                c.drawCentredString(cx, cy - 5 * mm + 0.6 * mm, "IP55")
                c.setFillColor(colors.white)
            c.setStrokeColor(colors.black)
        elif k == "pc20":
            c.arc(cx - 3 * mm, cy - 3 * mm, cx + 3 * mm, cy + 3 * mm, 0, 180)
            c.line(cx, cy + 3 * mm, cx, cy + 5.5 * mm)
            c.line(cx - 3 * mm, cy, cx + 3 * mm, cy)
            texte("20A", dy=-4.8, size=4.6)
        elif k == "pc_tri":
            c.arc(cx - 3 * mm, cy - 3 * mm, cx + 3 * mm, cy + 3 * mm, 0, 180)
            for dx in (-1.4 * mm, 0, 1.4 * mm):
                c.line(cx + dx, cy + (3 * mm if dx == 0 else 2.6 * mm), cx + dx, cy + 5.2 * mm)
            c.line(cx - 3 * mm, cy, cx + 3 * mm, cy)
        elif k == "sortie_cable":
            c.line(cx - 4 * mm, cy, cx + 1 * mm, cy)
            cercle_x = cx + 2.5 * mm
            c.circle(cercle_x, cy, 1.5 * mm, stroke=1, fill=1)
        elif k == "rj45":
            c.rect(cx - 2.6 * mm, cy - 2.6 * mm, 5.2 * mm, 5.2 * mm)
            c.line(cx - 2.6 * mm, cy + 2.6 * mm, cx, cy + 5 * mm)
            c.line(cx, cy + 5 * mm, cx + 2.6 * mm, cy + 2.6 * mm)
        elif k == "td":
            c.setFillColor(colors.black)
            c.rect(cx - 5 * mm, cy - 2.4 * mm, 10 * mm, 4.8 * mm, fill=1)
            c.setFillColor(colors.white)
            texte("TD", dy=-1.8, size=5, col=colors.white)
        elif k == "it_med":
            c.rect(cx - 6 * mm, cy - 3 * mm, 12 * mm, 6 * mm)
            c.circle(cx - 1.8 * mm, cy, 1.8 * mm)
            c.circle(cx + 1.8 * mm, cy, 1.8 * mm)
        elif k == "cpi":
            c.rect(cx - 4.5 * mm, cy - 2.6 * mm, 9 * mm, 5.2 * mm)
            texte("CPI", dy=-1.8, size=5)
        elif k == "equipot":
            c.line(cx, cy + 3.5 * mm, cx, cy)
            c.line(cx - 3 * mm, cy, cx + 3 * mm, cy)
            c.line(cx - 2 * mm, cy - 1.4 * mm, cx + 2 * mm, cy - 1.4 * mm)
            c.line(cx - 1 * mm, cy - 2.8 * mm, cx + 1 * mm, cy - 2.8 * mm)
        elif k == "chemin_cable":
            c.line(cx - 8 * mm, cy + 1.5 * mm, cx + 8 * mm, cy + 1.5 * mm)
            c.line(cx - 8 * mm, cy - 1.5 * mm, cx + 8 * mm, cy - 1.5 * mm)
            for i in range(5):
                x = cx - 7 * mm + i * 3.5 * mm
                c.line(x, cy - 1.5 * mm, x, cy + 1.5 * mm)


def ligne_legende(kind, repere, designation):
    return [Symbole(kind), Paragraph(repere, S["cellb"]), Paragraph(designation, S["cell"])]


def table_legende(titre, lignes):
    data = [[Paragraph("Symbole", S["cellb"]), Paragraph("Repère", S["cellb"]),
             Paragraph("Désignation", S["cellb"])]] + lignes
    t = Table(data, colWidths=[24 * mm, 18 * mm, 138 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), VERT),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, FOND]),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return [p(titre, "h2"), t]


# ----------------------------------------------------------------------------
# Schéma unifilaire de principe
# ----------------------------------------------------------------------------
class SchemaUnifilaire(Flowable):
    def __init__(self, w=180 * mm, h=120 * mm):
        super().__init__()
        self.width, self.height = w, h

    def wrap(self, aw, ah):
        return self.width, self.height

    def boite(self, c, x, y, w, h, lignes, fill=colors.white, border=colors.black, tcol=colors.black):
        c.setFillColor(fill)
        c.setStrokeColor(border)
        c.setLineWidth(1)
        c.rect(x, y, w, h, stroke=1, fill=1)
        c.setFillColor(tcol)
        n = len(lignes)
        for i, t in enumerate(lignes):
            c.setFont("Helvetica-Bold" if i == 0 else "Helvetica", 6.4)
            c.drawCentredString(x + w / 2, y + h - (i + 1) * (h / (n + 1)) - 2, t)

    def fleche(self, c, x1, y1, x2, y2, col=colors.black, dash=None):
        c.setStrokeColor(col)
        c.setLineWidth(1.1)
        if dash:
            c.setDash(dash, dash)
        c.line(x1, y1, x2, y2)
        c.setDash()

    def draw(self):
        c = self.canv
        W, H = self.width, self.height
        # Niveau 1 : sources
        self.boite(c, 2 * mm, H - 16 * mm, 38 * mm, 13 * mm,
                   ["RÉSEAU SBEE", "HTA 15 kV - 50 Hz", "(évolutif 20 kV)"], fill=FOND)
        self.boite(c, 46 * mm, H - 16 * mm, 40 * mm, 13 * mm,
                   ["POSTE HTA/BT", "Transfo 630 kVA", "15(20)/0,41 kV"], fill=FOND)
        self.boite(c, 132 * mm, H - 16 * mm, 40 * mm, 13 * mm,
                   ["GROUPE ÉLECTROGÈNE", "500 kVA - secours", "reprise < 15 s"],
                   fill=colors.HexColor("#fdecea"), border=ROUGE, tcol=ROUGE)
        self.fleche(c, 40 * mm, H - 9.5 * mm, 46 * mm, H - 9.5 * mm)
        # TGBT
        self.boite(c, 46 * mm, H - 40 * mm, 80 * mm, 14 * mm,
                   ["TGBT (local technique RDC - angle nord-ouest)",
                    "jeu de barres NORMAL / jeu de barres SECOURU",
                    "inverseur de sources automatique N/S - parafoudre type 1+2"])
        self.fleche(c, 66 * mm, H - 16 * mm, 66 * mm, H - 26 * mm)
        self.fleche(c, 152 * mm, H - 16 * mm, 152 * mm, H - 33 * mm, col=ROUGE)
        self.fleche(c, 152 * mm, H - 33 * mm, 126 * mm, H - 33 * mm, col=ROUGE)
        # ASI
        self.boite(c, 132 * mm, H - 62 * mm, 40 * mm, 13 * mm,
                   ["ASI (onduleur)", "2 x 40 kVA redondants", "autonomie >= 30 min"],
                   fill=colors.HexColor("#e8f5e9"), border=VERT_F, tcol=VERT_F)
        self.fleche(c, 120 * mm, H - 40 * mm, 120 * mm, H - 50 * mm, col=VERT_F)
        self.fleche(c, 120 * mm, H - 50 * mm, 132 * mm, H - 55 * mm, col=VERT_F)
        # Niveau tableaux divisionnaires
        tds = [
            (2, "TD RDC", ["consultations", "pharmacie", "bureaux"]),
            (32, "TD R+1", ["hospitalisation", "laboratoires"]),
            (62, "TD URGENCES", ["secouru", "groupe 1 / 2"]),
            (92, "TD CVC", ["centrales clim.", "édicule technique"]),
        ]
        for x, titre, det in tds:
            self.boite(c, x * mm, H - 72 * mm, 26 * mm, 14 * mm, [titre] + det)
            self.fleche(c, (x + 13) * mm, H - 40 * mm, (x + 13) * mm, H - 58 * mm)
        # IT médical
        self.boite(c, 132 * mm, H - 90 * mm, 40 * mm, 16 * mm,
                   ["TABLEAUX IT MÉDICAL", "transfo d'isolement 6,3 / 8 kVA",
                    "+ CPI + report d'alarme", "soins intensifs / déchocage"],
                   fill=colors.HexColor("#e8f5e9"), border=VERT_F, tcol=VERT_F)
        self.fleche(c, 152 * mm, H - 62 * mm, 152 * mm, H - 74 * mm, col=VERT_F)
        # Légende du schéma
        c.setFont("Helvetica-Oblique", 6.4)
        c.setFillColor(GRIS)
        c.drawString(2 * mm, H - 84 * mm, "Noir : réseau normal   -   Rouge : réseau secouru (groupe électrogène)   -   Vert : réseau ondulé / IT médical (sans coupure)")
        c.drawString(2 * mm, H - 90 * mm, "Régime de neutre général : TN-S  -  Locaux du groupe 2 : schéma IT médical (CEI 60364-7-710 / NF C 15-211)")
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(colors.black)
        c.drawString(2 * mm, H - 100 * mm, "Filiation des alimentations selon criticité :")
        c.setFont("Helvetica", 6.6)
        c.drawString(2 * mm, H - 106 * mm, "Classe 15 s (groupe électrogène) : urgences, hospitalisation, éclairage des circulations, chambres froides pharmacie, congélateurs -80 °C labos, monte-malade.")
        c.drawString(2 * mm, H - 111 * mm, "Classe 0,5 s / sans coupure (ASI) : locaux du groupe 2 (déchocage, soins intensifs), serveurs / baies informatiques, SSI, téléphonie.")


# ----------------------------------------------------------------------------
# Extraction des plans du dossier architecte
# ----------------------------------------------------------------------------
def extraire_plans():
    chemins = []
    doc = fitz.open(SRC_PDF)
    for idx, nom in [(1, "plan_rdc.png"), (2, "plan_r1.png")]:
        pg = doc[idx]
        pix = pg.get_pixmap(matrix=fitz.Matrix(2, 2))
        out = os.path.join(HERE, nom)
        pix.save(out)
        chemins.append(out)
    doc.close()
    return chemins


# ----------------------------------------------------------------------------
# Construction du document
# ----------------------------------------------------------------------------
def construire():
    doc = BaseDocTemplate(OUT_PDF, pagesize=A4,
                          leftMargin=15 * mm, rightMargin=15 * mm,
                          topMargin=18 * mm, bottomMargin=16 * mm,
                          title="Proposition de principe électricité - Centre de Drépanocytose Cotonou",
                          author="Étude de principe - lot électricité")
    fr_p = Frame(15 * mm, 16 * mm, A4[0] - 30 * mm, A4[1] - 34 * mm, id="portrait")
    fr_l = Frame(15 * mm, 16 * mm, A4[1] - 30 * mm, A4[0] - 34 * mm, id="paysage")
    doc.addPageTemplates([
        PageTemplate(id="P", frames=[fr_p], onPage=entete_pied),
        PageTemplate(id="L", frames=[fr_l], onPage=entete_pied, pagesize=landscape(A4)),
    ])

    E = []  # éléments

    # ---------------- Page de garde ----------------
    E.append(Spacer(1, 30 * mm))
    E.append(Paragraph("CENTRE DE DRÉPANOCYTOSE", S["titre"]))
    E.append(Paragraph("Cotonou - République du Bénin", S["soustitre"]))
    E.append(Spacer(1, 14 * mm))
    t = Table([[Paragraph("LOT ÉLECTRICITÉ - COURANTS FORTS<br/>PROPOSITION DE PRINCIPE",
                          ParagraphStyle("g", parent=S["titre"], fontSize=16, leading=22,
                                         alignment=TA_CENTER, textColor=colors.white))]],
              colWidths=[180 * mm], rowHeights=[24 * mm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), VERT),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    E.append(t)
    E.append(Spacer(1, 12 * mm))
    E.append(p("Principes de distribution électrique, d'éclairage et de prises de courant, "
               "avec légendes correspondantes."))
    E.append(Spacer(1, 6 * mm))
    info = Table([
        ["Projet", "Centre de prise en charge de la drépanocytose - 58 lits (54 hospitalisation + 4 hôpital de jour)"],
        ["Programme", "Urgences, consultations, hospitalisation, pharmacie, bureaux, laboratoires de recherche"],
        ["Architecte", "Koffi & Diabaté Architectes - dossier DCE de référence : septembre 2025"],
        ["Géométrie", "Bâtiment R+1 + édicule technique en toiture - trame 8,00 x 8,00 m - emprise ≈ 48 x 45 m - patio central"],
        ["Site", "Cotonou (Bénin) - climat tropical humide, ambiance saline (proximité littoral)"],
        ["Phase", "Avant-projet sommaire (APS) - document de principe"],
        ["Date / indice", "Juin 2026 - indice A"],
    ], colWidths=[32 * mm, 148 * mm])
    info.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
        ("BACKGROUND", (0, 0), (0, -1), FOND),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.2),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
    ]))
    E.append(info)
    E.append(PageBreak())

    # ---------------- 1. Objet ----------------
    E.append(p("1. OBJET DU DOCUMENT", "h1"))
    E.append(p("Le présent document constitue la proposition de principe du lot électricité courants forts "
               "du Centre de Drépanocytose de Cotonou. Il définit le référentiel normatif applicable, "
               "l'architecture générale de distribution, les principes d'éclairage (niveaux d'éclairement, "
               "appareils, commandes, éclairage de sécurité) et les principes d'appareillage prises de courant, "
               "ainsi que les légendes graphiques destinées aux plans de principe. Les puissances, sections et "
               "calibres indiqués sont des ordres de grandeur d'APS, à confirmer par les notes de calcul en phase PRO."))

    E.append(p("2. DESCRIPTION SOMMAIRE DU BÂTIMENT", "h1"))
    E.append(p("D'après le dossier architecte (DCE septembre 2025), le bâtiment se développe en R+1 autour d'un "
               "patio central, sur une trame de 8,00 m (files X01-X07 / Y00-Y08), avec un édicule technique en toiture "
               "(terrasse technique ≈ 1 935 m²) :"))
    E.append(puce("<b>RDC :</b> hall urgences avec SAS ambulance et boxes de déchocage, soins intensifs adultes (2 lits), "
                  "hospitalisation de jour (2 lits), chambres adultes, salle d'échographie, accueil consultations, "
                  "5 postes de consultation, pharmacie, salle de réunion, bureaux, cuisine, locaux techniques en "
                  "limite nord (local TGBT/transformateur, local groupe électrogène, local CO2, surpresseur)."))
    E.append(puce("<b>R+1 :</b> ailes d'hospitalisation (chambres 1 lit avec sanitaires), accueil d'étage, "
                  "laboratoires de recherche, locaux supports, deux escaliers + ascenseur monte-malade."))
    E.append(puce("<b>Surface utile estimée :</b> ≈ 2 100 m² par niveau, soit ≈ 4 200 m² hors terrasse technique."))

    # ---------------- 3. Normes ----------------
    E.append(p("3. RÉFÉRENTIEL NORMATIF ET RÉGLEMENTAIRE (VÉRIFIÉ)", "h1"))
    E.append(p("Le Bénin ne dispose pas d'un corpus normatif électrique national complet : la pratique des maîtres "
               "d'œuvre et des bailleurs (projets hospitaliers récents au Bénin) est d'appliquer le référentiel "
               "français NF / européen EN / international CEI, en cohérence avec le Code Réseau et le Règlement de "
               "service de la SBEE. Référentiel retenu :"))
    normes = [
        ["Domaine", "Référence", "Objet / points clés vérifiés"],
        ["Raccordement", "Code Réseau & Règlement de service SBEE",
         "Distribution HTA 15 kV à Cotonou (standardisation progressive à 20 kV) ; BT 230/400 V - 50 Hz, tolérance +6 % / -10 %. Le poste HTA/BT sera commandé apte 15 et 20 kV."],
        ["Poste de livraison", "NF C 13-100 / NF C 13-200",
         "Poste de livraison HTA/BT et installations HTA : comptage, cellules, protections, local poste."],
        ["Installations BT", "NF C 15-100 (et guide UTE C 15-105)",
         "Règles générales : protections, sections, chutes de tension (≤ 3 % éclairage / 5 % autres usages), DDR 30 mA type A haute immunité sur circuits prises."],
        ["Locaux médicaux", "NF C 15-211 / CEI 60364-7-710",
         "Classification des locaux en groupes 0, 1, 2 ; schéma IT médical (transformateur d'isolement + CPI) et continuité de service pour le groupe 2 ; liaisons équipotentielles supplémentaires ; temps de reprise des sources de sécurité (≤ 15 s, ≤ 0,5 s)."],
        ["Éclairage intérieur", "NF EN 12464-1",
         "Niveaux d'éclairement, UGR, uniformité et IRC par type de local (valeurs santé : chambres, salles d'examen, laboratoires...)."],
        ["Éclairage de sécurité", "NF EN 1838 / EN 60598-2-22 + règlement ERP type U (réf.)",
         "Évacuation 45 lm (BAES SATI), habitation/sommeil : BAEH + BAES, anti-panique dans les salles d'attente ; établissement avec locaux à sommeil."],
        ["Foudre / surtensions", "NF EN 62305-1 à 4 / NF C 15-100 §443 et 534",
         "Région à forte densité de foudroiement (golfe de Guinée) : analyse de risque, paratonnerre éventuel, parafoudres type 1+2 au TGBT et type 2 en divisionnaire - obligatoires pour un établissement de soins."],
        ["Groupes / ASI", "NF EN ISO 8528 / NF EN 62040",
         "Groupe électrogène de secours et alimentations sans interruption."],
        ["Appareillage", "NF EN 60309 / NF C 61-314", "Prises industrielles et prises domestiques 2P+T 16 A (standard franco-béninois type E)."],
    ]
    tn = Table([[Paragraph(x, S["cellb" if i == 0 else "cell"]) for x in ligne]
                for i, ligne in enumerate(normes)], colWidths=[26 * mm, 44 * mm, 110 * mm], repeatRows=1)
    tn.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), VERT),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, FOND]),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    E.append(tn)
    E.append(p("Conditions de site prises en compte : température ambiante élevée (déclassement des câbles et "
               "transformateur), hygrométrie forte, atmosphère saline du littoral de Cotonou (matériels IP/IK adaptés, "
               "visserie inox, traitement anticorrosion C4/C5 pour les matériels extérieurs), réseau public sujet à "
               "creux de tension et coupures (d'où groupe électrogène + ASI).", "note"))

    # ---------------- 4. Bilan de puissance ----------------
    E.append(p("4. BILAN DE PUISSANCE ESTIMATIF (APS)", "h1"))
    bilan = [
        ["Poste de charge", "Base de calcul", "P. installée", "Foisonnement", "P. foisonnée"],
        ["Éclairage interieur + extérieur", "≈ 10 W/m² (LED) x 4 200 m²", "45 kVA", "0,9", "40 kVA"],
        ["Prises de courant et petits forces", "≈ 25 VA/m²", "105 kVA", "0,4", "42 kVA"],
        ["Climatisation / ventilation (CVC)", "≈ 90 VA/m² climatisé", "330 kVA", "0,8", "264 kVA"],
        ["Équipements médicaux (urgences, soins int., imagerie légère)", "forfait", "60 kVA", "0,7", "42 kVA"],
        ["Laboratoires (paillasses, congélateurs -80 °C, étuves)", "forfait", "70 kVA", "0,6", "42 kVA"],
        ["Pharmacie (chambres froides) + cuisine", "forfait", "50 kVA", "0,7", "35 kVA"],
        ["Ascenseur monte-malade, surpresseur, divers", "forfait", "35 kVA", "0,6", "21 kVA"],
        ["TOTAL", "", "≈ 695 kVA", "", "≈ 486 kVA"],
    ]
    tb = Table([[Paragraph(x, S["cellb" if i in (0, 8) else "cell"]) for x in ligne]
                for i, ligne in enumerate(bilan)],
               colWidths=[72 * mm, 46 * mm, 22 * mm, 20 * mm, 20 * mm])
    tb.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), VERT),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#dce8d4")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
        ("ALIGN", (2, 1), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ]))
    E.append(tb)
    E.append(puce("<b>Transformateur :</b> 1 x 630 kVA - 15(20) kV / 410 V, type sec enrobé, en local poste "
                  "(emplacement prévu au plan RDC, bande technique nord), réserve de puissance ≈ 25 %."))
    E.append(puce("<b>Groupe électrogène :</b> 500 kVA (≈ 100 % des usages hors confort non prioritaire), capoté, "
                  "insonorisé, cuve 24 h, reprise automatique ≤ 15 s (exigence locaux médicaux), local GE prévu au plan."))
    E.append(puce("<b>ASI :</b> 2 x 40 kVA redondantes (N+1), autonomie ≥ 30 min, alimentant les tableaux IT médical "
                  "du groupe 2, les baies informatiques / courants faibles et l'éclairage des postes de soins critiques."))
    E.append(puce("<b>Compensation d'énergie réactive :</b> batterie de condensateurs au TGBT (cos φ ≥ 0,93 exigible "
                  "par la SBEE en tarif professionnel)."))

    # ---------------- 5. Architecture ----------------
    E.append(p("5. ARCHITECTURE DE DISTRIBUTION - SCHÉMA DE PRINCIPE", "h1"))
    E.append(puce("Régime de neutre général <b>TN-S</b> (5 conducteurs) depuis le TGBT ; "
                  "<b>IT médical</b> pour les circuits des locaux du groupe 2."))
    E.append(puce("Colonnes montantes en gaines techniques au droit des deux noyaux escaliers ; cheminements "
                  "principaux sur chemins de câbles en faux-plafond des circulations, séparation courants forts / "
                  "courants faibles ≥ 30 cm."))
    E.append(puce("Tableaux divisionnaires par niveau et par fonction (consultations, hospitalisation, urgences, "
                  "laboratoires, CVC, cuisine), avec 30 % de réserve d'équipement."))
    E.append(puce("Sélectivité totale des protections sur les départs secourus et le groupe 2 (exigence NF C 15-211)."))
    E.append(Spacer(1, 3 * mm))
    E.append(SchemaUnifilaire())
    E.append(PageBreak())

    # ---------------- 6. Classification locaux médicaux ----------------
    E.append(p("6. CLASSIFICATION DES LOCAUX À USAGE MÉDICAL (NF C 15-211 / CEI 60364-7-710)", "h1"))
    classif = [
        ["Groupe", "Définition", "Locaux du projet", "Dispositions principales"],
        ["Groupe 0", "Pas d'appareil médical électrique appliqué au patient",
         "Bureaux, accueil, salles d'attente, circulations, pharmacie (hors préparation), locaux techniques, cuisine",
         "Règles générales NF C 15-100 ; DDR 30 mA type A HI sur les prises."],
        ["Groupe 1", "Appareils appliqués de façon externe ou invasive non vitale",
         "Chambres d'hospitalisation, hôpital de jour, postes de consultation, salle d'échographie, salles de soins, laboratoires",
         "DDR 30 mA HI par circuit limité ; liaison équipotentielle supplémentaire (LES) ; ≥ 2 circuits distincts par local ; secours ≤ 15 s."],
        ["Groupe 2", "Appareils vitaux / patient en situation critique",
         "Boxes de déchocage des urgences, soins intensifs (2 lits), SAS urgences vitales",
         "Schéma IT médical : transfo d'isolement 230 V + contrôleur permanent d'isolement (CPI) avec report d'alarme au poste de soins ; ≥ 2 sources par poste patient ; LES ≤ 0,2 Ω ; secours ≤ 0,5 s (ASI) pour les fonctions vitales."],
    ]
    tc = Table([[Paragraph(x, S["cellb" if i == 0 else "cell"]) for x in ligne]
                for i, ligne in enumerate(classif)], colWidths=[16 * mm, 36 * mm, 56 * mm, 72 * mm], repeatRows=1)
    tc.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), VERT),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, FOND]),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    E.append(tc)

    # ---------------- 7. Principes éclairage ----------------
    E.append(p("7. PRINCIPES D'ÉCLAIRAGE", "h1"))
    E.append(p("7.1 Niveaux d'éclairement retenus (NF EN 12464-1 - section santé)", "h2"))
    lux = [
        ["Local", "Em (lux)", "UGR", "IRC", "Appareil type / observations"],
        ["Circulations (jour / nuit)", "200 / 50", "22", "80", "Downlights LED, abaissement nocturne par horloge"],
        ["Accueil, salles d'attente", "300", "22", "80", "Pavés LED + suspensions décoratives ; anti-panique"],
        ["Chambre : général / lecture / examen / veille", "100 / 300 / 1000 / 5", "19", "80 (90 examen)",
         "Bandeau tête de lit multifonction (indirect + lecture + examen + veille)"],
        ["Soins intensifs : général / examen / veille", "100 / 1000 / 20", "19", "90",
         "Bandeau / gaine tête de lit groupe 2, gradation DALI"],
        ["Urgences - box de déchocage", "500 / 1000 (examen)", "19", "90", "Plafonniers IP54 nettoyables + éclairage d'examen mobile"],
        ["Postes de consultation, échographie", "500 (1000 local.)", "19", "90", "Pavés LED UGR<19 + lampe d'examen ; gradation en échographie"],
        ["Laboratoires de recherche", "500", "19", "90", "Pavés LED IP54 sur paillasses, 750 lx au plan de travail"],
        ["Pharmacie (préparation / stockage)", "500 / 200", "19/22", "80", "Réglettes LED"],
        ["Bureaux, salle de réunion", "500", "19", "80", "Pavés LED 600x600, détection + gradation lumière du jour"],
        ["Sanitaires, vestiaires", "200", "25", "80", "Hublots LED IP44, détection de présence"],
        ["Cuisine", "500", "22", "80", "Réglettes LED IP65 alimentaires"],
        ["Escaliers", "150", "25", "80", "Hublots LED IP44 antivandales"],
        ["Locaux techniques, édicule", "200", "25", "80", "Réglettes LED IP65"],
        ["Extérieurs : parvis / parkings / cheminements", "50 / 20 / 10", "-", "70",
         "Candélabres LED 4-5 m et bornes, gestion crépusculaire + horloge, ULR < 3 % "],
    ]
    tl = Table(
        [[Paragraph(x, S["cellb" if i == 0 else "cell"]) for x in ligne] for i, ligne in enumerate(lux)],
        colWidths=[52 * mm, 26 * mm, 12 * mm, 16 * mm, 74 * mm], repeatRows=1)
    tl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), VERT),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (1, 1), (3, -1), "CENTER"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, FOND]),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ]))
    E.append(tl)
    E.append(p("7.2 Dispositions générales", "h2"))
    E.append(puce("Sources <b>100 % LED</b>, température de couleur 4 000 K (3 000 K dans les chambres et zones "
                  "d'attente pour le confort), flux maintenu L80B10 50 000 h, drivers DALI-2 dans les zones gradables."))
    E.append(puce("Gestion : détection de présence dans sanitaires, vestiaires, locaux techniques et escaliers ; "
                  "détection + gradation lumière du jour dans bureaux et laboratoires (apports du patio et des "
                  "façades claustra) ; commande veilleuse nocturne dans les circulations d'hospitalisation ; "
                  "horloge astronomique + cellule crépusculaire pour l'extérieur."))
    E.append(puce("Indices de protection : IP20 en locaux secs, IP44 sanitaires, IP54 nettoyables en locaux de soins "
                  "et laboratoires, IP65 cuisine / locaux techniques / extérieur ; IK08+ en circulations et extérieur ; "
                  "matériels extérieurs traités ambiance saline (C4/C5-M)."))
    E.append(puce("Chambres : commande générale en entrée + commandes lecture / examen / veille au bandeau tête de "
                  "lit, bouton d'appel relié au système appel-malade (lot courants faibles)."))
    E.append(p("7.3 Éclairage de sécurité (établissement de soins avec locaux à sommeil)", "h2"))
    E.append(puce("<b>Évacuation :</b> blocs autonomes BAES SATI 45 lm sur l'ensemble des cheminements, sorties, "
                  "obstacles et changements de direction (interdistance ≤ 15 m)."))
    E.append(puce("<b>Locaux à sommeil (hospitalisation) :</b> BAES + BAEH combinés (8 lm / 5 h) dans les circulations "
                  "des unités, conformément au référentiel ERP type U."))
    E.append(puce("<b>Anti-panique :</b> 5 lm/m² dans accueil / attentes > 50 personnes et salle de réunion."))
    E.append(puce("<b>Zones critiques (groupe 2) :</b> une partie de l'éclairage général du déchocage et des soins "
                  "intensifs est reprise sur l'ASI (continuité ≤ 0,5 s) en complément des BAES."))
    E.append(puce("Télécommande de mise au repos au TGBT et à l'accueil ; blocs adressables SATI connectés conseillés "
                  "pour la maintenance."))
    E.append(PageBreak())

    # ---------------- 8. Prises ----------------
    E.append(p("8. PRINCIPES PRISES DE COURANT ET PETITES FORCES", "h1"))
    E.append(p("8.1 Réseaux de prises et détrompage", "h2"))
    E.append(puce("<b>Réseau NORMAL</b> (appareillage <b>blanc</b>) : alimenté par le jeu de barres normal, délesté "
                  "sur coupure réseau hors zones prioritaires."))
    E.append(puce("<b>Réseau SECOURU</b> (appareillage <b>rouge</b>) : repris par le groupe électrogène ≤ 15 s "
                  "(têtes de lit, postes de soins, congélateurs -80 °C, chambres froides pharmacie, paillasses critiques)."))
    E.append(puce("<b>Réseau ONDULÉ / IT MÉDICAL</b> (appareillage <b>vert</b>, détrompage à clé en informatique) : "
                  "sans coupure via ASI ; en groupe 2, distribué en IT médical avec CPI."))
    E.append(puce("Prises 2P+T 16 A type E (standard béninois) ; circuits ≤ 8 prises en 3G2,5 mm² protégés 20 A ; "
                  "DDR 30 mA type A haute immunité (sauf circuits IT médical : surveillance par CPI, pas de "
                  "coupure au premier défaut)."))
    E.append(p("8.2 Hauteurs de pose (axe appareillage)", "h2"))
    E.append(puce("Locaux courants : 0,30 m - bureaux sur goulottes ou nourrices ; interrupteurs et commandes entre "
                  "0,90 et 1,30 m (accessibilité PMR)."))
    E.append(puce("Locaux de soins : 0,90 à 1,20 m (nettoyabilité, lits et chariots) ; au-dessus des paillasses : 1,10 m ; "
                  "cuisine et locaux humides : 1,20 m, hors volumes d'eau, appareillage IP44/IP55."))
    E.append(p("8.3 Dotations de principe par local", "h2"))
    dot = [
        ["Local", "Dotation prises de courant (principe)"],
        ["Chambre d'hospitalisation (1 lit)",
         "Tête de lit : 2 PC secourues (rouges) + 2 PC normales sur bandeau ; 2 PC normales en partie courante ; "
         "1 PC TV ; 1 PC entretien près de la porte ; sanitaire : 1 PC IP44 hors volumes (sèche-mains)."],
        ["Soins intensifs / déchocage (groupe 2)",
         "Gaine tête de lit par poste patient : 8 à 12 PC vertes réparties sur 2 circuits IT médical distincts "
         "+ 2 PC secourues hors IT ; barrette de liaison équipotentielle (≥ 6 plots) ; prises gaz médicaux et appel "
         "malade en coordination lots fluides / CFa ; alarme CPI reportée au poste de soins."],
        ["Poste de consultation / échographie",
         "6 PC dont 2 secourues au poste d'examen + 2 PC ondulées au poste informatique ; négatoscope / écran : 1 PC dédiée."],
        ["Laboratoires de recherche",
         "Bandeaux de paillasse : 1 bloc 4 PC par mètre linéaire dont 50 % secourues ; circuits dédiés 20 A : "
         "congélateurs -80 °C (secourus, 1 circuit par appareil + alarme température), étuves, centrifugeuses, "
         "autoclave (tri 3P+N+T) ; 2 PC ondulées par poste d'acquisition."],
        ["Pharmacie",
         "4 PC + 2 PC ondulées au comptoir ; circuits dédiés secourus pour chambres froides et réfrigérateurs "
         "(alarme de température reportée)."],
        ["Bureaux / salle de réunion",
         "Par poste de travail : 3 PC (dont 1 détrompée ondulée) + 2 RJ45 ; réunion : nourrice centrale 4 PC + "
         "écran 2 PC + 1 PC entretien."],
        ["Accueils / attentes", "2 PC entretien + PC TV/affichage dynamique (ondulées) + PC distributeurs."],
        ["Cuisine", "PC IP55 en bandeau 1,20 m ; attentes force : chambre froide, four (tri), lave-vaisselle ; "
         "coupure d'urgence cuisine en sortie."],
        ["Circulations / parties communes", "1 PC entretien tous les 10 à 15 m et près des ascenseurs."],
        ["Locaux techniques / terrasse", "1 PC étanche IP55 par local + attentes force CVC ; PC 3P+N+T 32 A en local maintenance."],
    ]
    td = Table([[Paragraph(x, S["cellb" if i == 0 else "cell"]) for x in ligne] for i, ligne in enumerate(dot)],
               colWidths=[48 * mm, 132 * mm], repeatRows=1)
    td.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), VERT),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, FOND]),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    E.append(td)
    E.append(PageBreak())

    # ---------------- 9. Légendes ----------------
    E.append(p("9. LÉGENDES DES PLANS DE PRINCIPE", "h1"))
    E.append(p("Symboles graphiques inspirés des normes NF C 03 / CEI 60617, destinés aux plans de principe "
               "éclairage et prises de courant."))
    for fl in table_legende("9.1 Légende ÉCLAIRAGE", [
        ligne_legende("pave600", "L1", "Pavé LED 600x600 encastré, UGR&lt;19 - bureaux, consultations, laboratoires (IP54 en zone de soins)"),
        ligne_legende("downlight", "L2", "Downlight LED encastré Ø200 - circulations, accueils"),
        ligne_legende("reglette", "L3", "Réglette LED - pharmacie, stockage, locaux supports"),
        ligne_legende("etanche", "L4", "Réglette LED étanche IP65 - cuisine, locaux techniques, édicule, parkings couverts"),
        ligne_legende("hublot", "L5", "Hublot LED IP44/IK10 - sanitaires, escaliers, SAS"),
        ligne_legende("applique", "L6", "Applique murale LED - chambres (éclairage doux), salons d'attente"),
        ligne_legende("bandeau_lit", "TL", "Bandeau / gaine tête de lit multifonction : général indirect + lecture + examen 1 000 lx + veilleuse (PC et fluides intégrés)"),
        ligne_legende("suspension", "L7", "Suspension décorative - hall d'accueil, patio couvert"),
        ligne_legende("projecteur", "L8", "Projecteur LED extérieur IP66 - façades, parvis, SAS ambulance"),
        ligne_legende("candelabre", "L9", "Candélabre LED 4-5 m / borne extérieure IP66, traitement ambiance saline - parkings, cheminements"),
        ligne_legende("baes", "BAES", "Bloc autonome d'éclairage de sécurité d'évacuation 45 lm, SATI"),
        ligne_legende("baeh", "BAEH", "Bloc autonome d'éclairage d'habitation 8 lm / 5 h - circulations des unités d'hospitalisation (combiné BAES+BAEH)"),
        ligne_legende("secours_sc", "SC", "Luminaire repris sur source centrale / ASI (zones groupe 2)"),
        ligne_legende("inter_sa", "", "Interrupteur simple allumage (h = 0,90-1,30 m)"),
        ligne_legende("inter_vv", "", "Interrupteur va-et-vient"),
        ligne_legende("bp", "", "Bouton-poussoir lumineux sur télérupteur / minuterie"),
        ligne_legende("detecteur", "DP", "Détecteur de présence / mouvement plafonnier"),
    ]):
        E.append(fl)
    E.append(PageBreak())
    for fl in table_legende("9.2 Légende PRISES DE COURANT ET FORCES", [
        ligne_legende("pc16", "PC", "Prise de courant 2P+T 16 A 250 V type E - réseau NORMAL (appareillage blanc), h = 0,30 m sauf indication"),
        ligne_legende("pc16_sec", "PCS", "Prise 2P+T 16 A - réseau SECOURU groupe électrogène (appareillage rouge)"),
        ligne_legende("pc16_ond", "PCO", "Prise 2P+T 16 A - réseau ONDULÉ ASI / IT médical (appareillage vert, détrompage)"),
        ligne_legende("pc_etanche", "PCE", "Prise 2P+T 16 A étanche IP55 - cuisine, locaux techniques, extérieur"),
        ligne_legende("pc20", "PC20", "Prise / circuit spécialisé 20 A (congélateur -80 °C, étuve, chambre froide...)"),
        ligne_legende("pc_tri", "PCT", "Prise triphasée 3P+N+T 16/32 A (NF EN 60309) - cuisine, maintenance, laboratoires"),
        ligne_legende("sortie_cable", "SCa", "Sortie de câble / attente force motrice (CVC, équipement fixe)"),
        ligne_legende("rj45", "RJ", "Prise RJ45 Cat. 6A (rappel - lot courants faibles, associée aux postes de travail)"),
        ligne_legende("bandeau_lit", "GTL", "Gaine tête de lit soins intensifs / déchocage : 8-12 PC sur 2 circuits IT médical + équipotentialité"),
        ligne_legende("td", "TD", "Tableau électrique divisionnaire (TD) - armoire IP43/IK08, réserve 30 %"),
        ligne_legende("it_med", "TRI", "Transformateur d'isolement médical 230/230 V (3,15 à 8 kVA) - locaux groupe 2"),
        ligne_legende("cpi", "CPI", "Contrôleur permanent d'isolement avec report d'alarme au poste de soins"),
        ligne_legende("equipot", "LES", "Barrette / liaison équipotentielle supplémentaire des masses et éléments conducteurs (locaux groupes 1 et 2)"),
        ligne_legende("chemin_cable", "CdC", "Chemin de câbles courants forts (dalle marine perforée, éclisses inox)"),
    ]):
        E.append(fl)
    E.append(Spacer(1, 4 * mm))
    E.append(p("Nota : les implantations précises des appareils sur les plans (calepinage des luminaires, positions "
               "des prises) seront produites en phase PRO sur les fonds de plan architecte au 1/100, en appliquant "
               "les dotations du §8.3 et les niveaux d'éclairement du §7.1 (calculs Dialux à l'appui).", "note"))

    # ---------------- 10. Annexes plans ----------------
    plans = extraire_plans()
    E.append(NextPageTemplate("L"))
    E.append(PageBreak())
    E.append(p("10. ANNEXE - FONDS DE PLAN DE RÉFÉRENCE (dossier architecte, éch. 1:300)", "h1"))
    E.append(p("Plans support des principes : RDC (urgences, consultations, soins intensifs, pharmacie, bureaux, "
               "locaux techniques nord) et R+1 (hospitalisation, laboratoires). Les zones en orange (urgences) et "
               "les soins intensifs relèvent des groupes 1-2 ; les laboratoires (violet au R+1) reçoivent les "
               "dotations paillasses du §8.3."))
    for chemin, titre in zip(plans, ["Plan RDC - dossier Koffi & Diabaté (sept. 2025)",
                                     "Plan 1er étage - dossier Koffi & Diabaté (sept. 2025)"]):
        h_img = 148 * mm
        img = Image(chemin, width=h_img * 1308.0 / 924.0, height=h_img)
        E.append(KeepTogether([img, Paragraph(titre, S["legende_fig"])]))
        E.append(Spacer(1, 4 * mm))

    doc.build(E)
    print("OK :", OUT_PDF)


if __name__ == "__main__":
    construire()
