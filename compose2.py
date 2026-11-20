#!/usr/bin/env python3
"""Build the make.fun news-image-20261120 entry v2: a dense newspaper front
page summing up Friday 20 November 2026. Rebuilt from scratch after v1
ranked #765 of 11,657: Cyclone Akvan's landfall is now LEAD 2 (v1 missed it
entirely), COP31's final-day deadlock and BepiColombo's arrival at Mercury
are numbered cards, and every scene is a richer, labelled, high-contrast
illustration -- the Akvan lead uses a REAL satellite photo (JTWC/NASA,
public domain, via Wikimedia Commons); all other scenes are drawn in code
modelled on real reference imagery. All text set with real fonts.
Writes entry.png (1024x1024) next to this script."""

import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (251, 250, 245)
INK = (17, 17, 17)
RED = (178, 0, 0)
GREY = (110, 110, 110)
LIGHT = (225, 222, 214)
MAPDOT = (96, 116, 148)

LF = "/usr/share/fonts/truetype/liberation/"
SERIF_B = os.path.join(LF, "LiberationSerif-Bold.ttf")
SANS = os.path.join(LF, "LiberationSans-Regular.ttf")
SANS_B = os.path.join(LF, "LiberationSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if fnt.getlength(t) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_lines(d, x, y, lines, fnt, fill=INK, lh=None):
    if lh is None:
        lh = int(fnt.size * 1.25)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def rule(d, x0, x1, y, fill=INK, wdt=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=wdt)


def chip(d, x, y, text, fnt, fg=(255, 255, 255), bg=(17, 17, 17), pad=4):
    """Small dark label chip with white bold text; returns its right edge."""
    tw = int(fnt.getlength(text)) + 2 * pad
    th = fnt.size + 2 * pad
    d.rectangle([x, y, x + tw, y + th], fill=bg)
    d.text((x + pad, y + pad - 1), text, font=fnt, fill=fg)
    return x + tw


# ---------------------------------------------------------------- world map
NA = [(-168, 66), (-150, 70), (-135, 69), (-125, 71), (-115, 68), (-100, 69),
      (-90, 68), (-85, 66), (-80, 73), (-70, 62), (-60, 55), (-55, 47),
      (-60, 45), (-65, 44), (-70, 42), (-74, 39), (-76, 35), (-80, 32),
      (-81, 26), (-84, 30), (-89, 29), (-90, 21), (-95, 16), (-92, 15),
      (-97, 16), (-105, 20), (-110, 23), (-114, 28), (-120, 34), (-124, 40),
      (-124, 48), (-130, 54), (-140, 60), (-150, 59), (-158, 58), (-165, 60)]
GREENLAND = [(-58, 64), (-52, 60), (-43, 60), (-32, 68), (-22, 70), (-25, 76),
             (-40, 76), (-55, 76), (-60, 74)]
SA = [(-79, 9), (-77, 8), (-72, 11), (-64, 10), (-59, 8), (-52, 5), (-50, 0),
      (-44, -3), (-35, -8), (-38, -15), (-40, -22), (-48, -27), (-53, -33),
      (-58, -38), (-62, -41), (-65, -45), (-68, -50), (-70, -54), (-73, -50),
      (-73, -44), (-73, -37), (-71, -30), (-70, -20), (-75, -15), (-79, -8),
      (-81, -4), (-80, 1)]
AFRICA = [(-17, 15), (-16, 20), (-11, 27), (-6, 34), (-10, 37), (-5, 36),
          (0, 36), (8, 37), (11, 34), (15, 32), (20, 32), (25, 32), (30, 31),
          (34, 28), (35, 28), (39, 21), (43, 12), (48, 11), (51, 12), (51, 2),
          (48, -2), (42, -8), (40, -15), (36, -22), (33, -26), (31, -29),
          (28, -33), (20, -35), (17, -32), (14, -27), (12, -18), (12, -12),
          (13, -10), (12, -6), (9, -1), (9, 4), (4, 6), (-3, 5), (-8, 5),
          (-13, 8), (-15, 11)]
EURASIA = [(-10, 36), (-9, 38), (-9, 43), (-4, 44), (-2, 47), (-1, 46), (0, 48),
           (2, 51), (4, 53), (7, 54), (8, 57), (10, 57), (12, 55), (18, 56),
           (21, 55), (21, 59), (24, 59), (24, 61), (28, 60), (30, 62),
           (30, 66), (32, 70), (40, 68), (44, 68), (50, 69), (55, 69),
           (60, 69), (68, 70), (72, 72), (78, 72), (85, 74), (95, 76),
           (105, 77), (113, 74), (120, 73), (128, 71), (135, 72), (142, 72),
           (150, 70), (158, 70), (162, 66), (170, 66), (178, 65), (178, 62),
           (170, 60), (162, 60), (158, 56), (156, 52), (150, 59), (142, 55),
           (141, 50), (140, 45), (140, 39), (137, 35), (135, 34), (132, 33),
           (130, 33), (127, 35), (126, 38), (124, 40), (122, 38), (120, 32),
           (118, 25), (112, 22), (110, 20), (108, 18), (106, 10), (105, 9),
           (103, 7), (100, 7), (99, 10), (98, 14), (97, 16), (94, 17),
           (92, 21), (91, 22), (89, 22), (88, 22), (86, 20), (84, 19),
           (81, 16), (80, 13), (79, 9), (77, 8), (76, 10), (74, 15),
           (73, 19), (72, 21), (70, 22), (68, 24), (66, 25), (64, 25),
           (61, 25), (58, 26), (56, 27), (54, 27), (52, 28), (50, 29),
           (49, 30), (47, 30), (44, 29), (42, 30), (40, 32), (38, 34),
           (36, 36), (34, 36), (32, 36), (30, 36), (28, 37), (26, 38),
           (23, 36), (22, 37), (20, 40), (19, 42), (16, 44), (14, 44),
           (12, 44), (10, 44), (8, 44), (6, 43), (4, 43), (2, 42), (0, 40),
           (-1, 38), (-3, 37), (-6, 36), (-9, 37)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-4, 58), (-2, 57), (0, 54), (1, 52),
      (1, 51), (-2, 50), (-4, 50)]
JAPAN = [(130, 31), (131, 33), (133, 34), (135, 34), (137, 35), (139, 35),
         (140, 37), (141, 39), (141, 41), (142, 44), (144, 44), (145, 43),
         (143, 42), (141, 40), (140, 36), (139, 35), (137, 34), (134, 33),
         (131, 32)]
AUSTRALIA = [(113, -22), (114, -28), (115, -33), (118, -35), (124, -33),
             (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
             (144, -38), (146, -39), (149, -37), (150, -37), (153, -32),
             (153, -27), (151, -24), (149, -20), (146, -19), (143, -15),
             (142, -11), (140, -13), (137, -12), (136, -15), (135, -12),
             (132, -11), (130, -13), (127, -14), (125, -15), (122, -17),
             (119, -19), (116, -21), (114, -22)]
INDONESIA = [(95, 5), (98, 3), (100, 0), (103, -3), (106, -6), (110, -7),
             (114, -8), (118, -9), (120, -10), (122, -10), (125, -9),
             (128, -7), (131, -3), (134, -4), (137, -2), (138, -2), (140, -8),
             (138, -8), (135, -7), (132, -4), (130, -2), (128, 0), (126, 1),
             (124, 1), (122, 0), (120, 1), (118, 1), (116, -1), (114, -3),
             (112, -7), (110, -7), (108, -7), (106, -6), (104, -4), (102, -1),
             (100, 1), (97, 4)]
NZ = [(167, -45), (168, -46), (170, -44), (172, -43), (174, -41), (175, -40),
      (176, -38), (178, -38), (177, -37), (176, -38), (174, -36), (173, -35),
      (174, -37), (175, -40), (173, -42), (171, -43), (169, -44)]
LAND = [NA, GREENLAND, SA, AFRICA, EURASIA, UK, JAPAN, AUSTRALIA, INDONESIA, NZ]


def inside_poly(lon, lat, poly):
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > lat) != (yj > lat):
            xin = (xj - xi) * (lat - yi) / (yj - yi) + xi
            if lon < xin:
                inside = not inside
        j = i
    return inside


def on_land(lon, lat):
    return any(inside_poly(lon, lat, p) for p in LAND)


# ---------------------------------------------------------------- scenes
def scene(d, x, y, w, h, kind, img=None, base=None):
    """Flat illustration inside box (x, y, w, h). Labelled, high contrast.
    kind 'akvan' pastes the real satellite photo (img = the PIL photo);
    base = the page image the scene is pasted onto."""
    x1, y1 = x + w, y + h
    f_lab = font(SANS_B, 9)
    if kind == "akvan":
        # real satellite photo of Cyclone Akvan (JTWC/NASA, public domain),
        # cropped to the storm's spiral core, pasted to fill the panel.
        ph = img.crop((350, 700, 1150, 985)).resize((w, h), Image.LANCZOS)
        base.paste(ph, (x, y))
        d.rectangle([x, y, x1, y1], outline=(17, 17, 17), width=2)
        # photo credit strip, bottom of the photo
        d.rectangle([x, y1 - 14, x1, y1], fill=(17, 17, 17))
        d.text((x + 5, y1 - 12), "SATELLITE PHOTO: JTWC/NASA",
               font=font(SANS_B, 7), fill=(255, 255, 255))
        d.text((x1 - 5, y1 - 12), "GOPALPUR, ODISHA", font=font(SANS_B, 7),
               fill=(255, 210, 90), anchor="ra")
        return
    if kind == "kyiv":
        # night over Kyiv: stars, burning blocks, smoke, a Dnipro bridge
        # with a cracked span across the bottom
        d.rectangle([x, y, x1, y1], fill=(14, 20, 48))
        for sx, sy in [(0.12, 0.10), (0.30, 0.06), (0.48, 0.14), (0.66, 0.07),
                       (0.82, 0.12), (0.94, 0.06), (0.22, 0.22), (0.58, 0.20)]:
            d.ellipse([x + w * sx - 1, y + h * sy - 1, x + w * sx + 1,
                       y + h * sy + 1], fill=(255, 255, 255))
        # fire glow behind the blocks
        d.ellipse([x + w * 0.55, y + h * 0.18, x + w * 0.95, y + h * 0.72],
                  fill=(255, 110, 20))
        d.ellipse([x + w * 0.62, y + h * 0.30, x + w * 0.88, y + h * 0.68],
                  fill=(255, 180, 60))
        # smoke columns
        for cx, cy, cw, ch in [(0.60, 0.04, 0.09, 0.30), (0.72, 0.02, 0.07, 0.26),
                               (0.28, 0.08, 0.08, 0.30)]:
            d.ellipse([x + w * cx, y + h * cy, x + w * (cx + cw),
                       y + h * (cy + ch)], fill=(105, 105, 118))
        # buildings: left intact, middle damaged (broken roof), right burning
        d.rectangle([x + w * 0.04, y + h * 0.52, x + w * 0.24, y1],
                    fill=(8, 10, 26))
        d.polygon([(x + w * 0.28, y + h * 0.62), (x + w * 0.34, y + h * 0.44),
                   (x + w * 0.38, y + h * 0.56), (x + w * 0.44, y + h * 0.46),
                   (x + w * 0.48, y + h * 0.62)], fill=(8, 10, 26))
        d.rectangle([x + w * 0.28, y + h * 0.62, x + w * 0.48, y1],
                    fill=(10, 12, 30))
        d.rectangle([x + w * 0.52, y + h * 0.48, x + w * 0.96, y1],
                    fill=(8, 10, 26))
        for wx in range(5):
            d.rectangle([x + w * 0.06 + wx * w * 0.035, y + h * 0.58,
                         x + w * 0.06 + wx * w * 0.035 + 5, y + h * 0.66],
                        fill=(255, 200, 90))
        for wx in range(4):
            d.rectangle([x + w * 0.56 + wx * w * 0.09, y + h * 0.54,
                         x + w * 0.56 + wx * w * 0.09 + 6, y + h * 0.62],
                        fill=(255, 160, 60))
        # bridge across the bottom, cracked span in the middle
        d.rectangle([x, y1 - 12, x1, y1 - 8], fill=(200, 200, 210))
        d.polygon([(x + w * 0.46, y1 - 12), (x + w * 0.50, y1 - 26),
                   (x + w * 0.54, y1 - 12)], fill=(200, 200, 210))
        d.line([(x + w * 0.50, y1 - 26), (x + w * 0.50, y1 - 8)],
               fill=(255, 60, 40), width=2)
        chip(d, x + 5, y + 5, "KYIV, OVERNIGHT", f_lab, bg=(178, 0, 0))
        return
    if kind == "markets":
        # trading floor at the close: candlesticks falling, big red line
        d.rectangle([x, y, x1, y1], fill=(18, 20, 32))
        n = 8
        vals = [0.80, 0.72, 0.76, 0.58, 0.64, 0.46, 0.34, 0.22]
        bw = w / (n * 1.7)
        for i, v in enumerate(vals):
            bx = x + 10 + i * (w - 20) / n
            bh = v * (h - 24)
            col = (70, 170, 90) if i < 2 else (215, 55, 45)
            d.rectangle([bx, y1 - 8 - bh, bx + bw, y1 - 8], fill=col)
            d.line([(bx + bw / 2, y1 - 8 - bh - 6), (bx + bw / 2, y1 - 8)],
                   fill=col, width=1)
        pts = [(x + 10 + i * (w - 20) / (n - 1), y + 14 + (0.10 + 0.10 * i) * h)
               for i in range(n)]
        d.line(pts, fill=(255, 70, 55), width=3)
        for px, py in pts:
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 255, 255))
        d.polygon([(x + w - 26, y + h * 0.62), (x + w - 12, y + h * 0.62),
                   (x + w - 19, y + h * 0.78)], fill=(255, 70, 55))
        chip(d, x + 5, y + 5, "AI SELL-OFF", f_lab, bg=(178, 0, 0))
        d.text((x1 - 6, y + 6), "-4.8%", font=font(SANS_B, 16),
               fill=(255, 90, 70), anchor="ra")
        return
    if kind == "cop31":
        # conference hall on the final day: flags, podium, clock
        d.rectangle([x, y, x1, y1], fill=(238, 228, 205))
        d.rectangle([x, y, x1, y + h * 0.30], fill=(30, 60, 110))
        flagcols = [(200, 16, 46), (255, 255, 255), (0, 120, 80),
                    (255, 200, 0), (20, 60, 160), (220, 90, 40),
                    (0, 90, 140), (255, 255, 255)]
        for i, fc in enumerate(flagcols):
            fx = x + 8 + i * (w - 16) / len(flagcols)
            d.line([(fx + 5, y + 6), (fx + 5, y + h * 0.28)], fill=(90, 70, 40),
                   width=1)
            d.rectangle([fx, y + 6, fx + 12, y + 14], fill=fc,
                        outline=(17, 17, 17), width=1)
        # clock: final day
        cx, cy, r = x + w * 0.82, y + h * 0.58, 13
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255),
                  outline=(17, 17, 17), width=2)
        d.line([(cx, cy), (cx, cy - r + 4)], fill=(17, 17, 17), width=2)
        d.line([(cx, cy), (cx + r - 6, cy + 3)], fill=(178, 0, 0), width=2)
        # podium with papers
        d.rectangle([x + w * 0.30, y + h * 0.62, x + w * 0.58, y1 - 4],
                    fill=(120, 90, 50))
        d.rectangle([x + w * 0.32, y + h * 0.56, x + w * 0.56, y + h * 0.62],
                    fill=(255, 255, 255))
        d.line([(x + w * 0.36, y + h * 0.58), (x + w * 0.52, y + h * 0.58)],
               fill=(17, 17, 17), width=1)
        chip(d, x + 5, y + h - 18, "FINAL DAY", f_lab, bg=(178, 0, 0))
        return
    if kind == "bepi":
        # Mercury's cratered limb, BepiColombo above it (modelled on ESA's
        # flyby renders: boxy white body, two long dark solar arrays).
        # Drawn on a layer of exactly the scene size so the planet disc
        # (which extends past the box) is clipped to the scene.
        layer = Image.new("RGB", (w, h), (5, 5, 12))
        dl = ImageDraw.Draw(layer)
        for sx, sy in [(0.08, 0.12), (0.25, 0.06), (0.45, 0.16), (0.70, 0.08),
                       (0.88, 0.14), (0.95, 0.05), (0.55, 0.05)]:
            dl.ellipse([w * sx - 1, h * sy - 1, w * sx + 1, h * sy + 1],
                       fill=(255, 255, 255))
        # Mercury disc rising from the bottom
        mx, my, mr = w * 0.50, h * 1.55, w * 0.72
        dl.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(168, 158, 142))
        for cx, cy, cr in [(0.30, 0.62, 0.05), (0.55, 0.70, 0.07),
                           (0.72, 0.60, 0.04), (0.42, 0.80, 0.06),
                           (0.62, 0.84, 0.05), (0.20, 0.78, 0.04)]:
            dl.ellipse([w * cx - cr * w, h * cy - cr * w,
                        w * cx + cr * w, h * cy + cr * w],
                       fill=(140, 130, 114))
        # orbit ellipse
        dl.arc([w * 0.10, -h * 0.55, w * 0.90, h * 0.55],
               start=200, end=340, fill=(255, 255, 255), width=1)
        # spacecraft: body + two solar arrays
        bx, by = w * 0.50, h * 0.30
        dl.rectangle([bx - 9, by - 6, bx + 9, by + 6], fill=(235, 235, 235),
                     outline=(17, 17, 17), width=1)
        dl.rectangle([bx - 34, by - 3, bx - 10, by + 3], fill=(30, 30, 50),
                     outline=(120, 120, 140), width=1)
        dl.rectangle([bx + 10, by - 3, bx + 34, by + 3], fill=(30, 30, 50),
                     outline=(120, 120, 140), width=1)
        dl.ellipse([bx - 3, by - 9, bx + 3, by - 3], fill=(255, 210, 90))
        chip(dl, 5, 5, "8 YEARS", f_lab, bg=(17, 17, 17))
        base.paste(layer, (x, y))
        return
    if kind == "estonia":
        # snowy border crossing, barrier down, CLOSED sign, watchtower
        d.rectangle([x, y, x1, y1], fill=(198, 220, 238))
        d.rectangle([x, y + h * 0.68, x1, y1], fill=(240, 244, 248))
        for tx in (0.10, 0.88):
            cx = x + w * tx
            d.polygon([(cx, y + h * 0.30), (cx - w * 0.07, y + h * 0.68),
                       (cx + w * 0.07, y + h * 0.68)], fill=(24, 80, 50))
            d.rectangle([cx - 2, y + h * 0.68, cx + 2, y + h * 0.78],
                        fill=(90, 60, 30))
        # watchtower
        d.rectangle([x + w * 0.78, y + h * 0.34, x + w * 0.94, y + h * 0.80],
                    fill=(120, 90, 60))
        d.polygon([(x + w * 0.76, y + h * 0.34), (x + w * 0.86, y + h * 0.22),
                   (x + w * 0.96, y + h * 0.34)], fill=(140, 40, 40))
        d.rectangle([x + w * 0.82, y + h * 0.42, x + w * 0.90, y + h * 0.50],
                    fill=(255, 220, 140))
        # barrier: red-white striped arm across the road
        d.rectangle([x + w * 0.16, y + h * 0.58, x + w * 0.72, y + h * 0.66],
                    fill=(255, 255, 255), outline=(17, 17, 17), width=1)
        for i in range(4):
            bx = x + w * (0.16 + i * 0.14)
            d.rectangle([bx, y + h * 0.58, bx + w * 0.07, y + h * 0.66],
                        fill=(200, 30, 30))
        for bx in range(4):
            d.rectangle([x + w * 0.18 + bx * w * 0.14, y + h * 0.58,
                         x + w * 0.22 + bx * w * 0.14, y + h * 0.66],
                        fill=(60, 60, 60))
        chip(d, x + 5, y + 5, "CLOSED 1 DEC", f_lab, bg=(178, 0, 0))
        return
    if kind == "gta6":
        # neon Vice City night: moon, palms, lit towers, low car
        d.rectangle([x, y, x1, y1], fill=(18, 8, 44))
        d.ellipse([x + w * 0.76, y + 4, x + w * 0.92, y + h * 0.34],
                  fill=(255, 210, 90))
        for sx, sy in [(0.08, 0.08), (0.30, 0.05), (0.55, 0.10), (0.68, 0.04)]:
            d.ellipse([x + w * sx - 1, y + h * sy - 1, x + w * sx + 1,
                       y + h * sy + 1], fill=(255, 255, 255))
        heights = [0.42, 0.62, 0.50, 0.72, 0.56, 0.66, 0.40]
        cols = [(255, 80, 180), (60, 220, 230), (255, 200, 60),
                (140, 100, 255), (255, 80, 180), (60, 220, 230),
                (255, 200, 60)]
        bw = w / len(heights)
        for i, hh in enumerate(heights):
            bx = x + i * bw
            d.rectangle([bx + 2, y1 - hh * h, bx + bw - 2, y1],
                        fill=(30, 22, 60))
            for wy in range(3):
                d.rectangle([bx + 4, y1 - hh * h + 5 + wy * 11,
                             bx + bw - 4, y1 - hh * h + 10 + wy * 11],
                            fill=cols[i])
        # palm silhouettes
        for px, py in [(0.06, 0.86), (0.93, 0.88)]:
            d.line([(x + w * px, y + h * py), (x + w * px, y + h * (py - 0.16))],
                   fill=(8, 30, 12), width=3)
            for a in (-0.5, -0.2, 0.1, 0.4):
                d.line([(x + w * px, y + h * (py - 0.16)),
                        (x + w * (px + a * 0.10), y + h * (py - 0.10))],
                       fill=(8, 30, 12), width=2)
        # low car with headlights
        d.rectangle([x + w * 0.34, y1 - 12, x + w * 0.62, y1 - 6],
                    fill=(255, 80, 180))
        d.polygon([(x + w * 0.38, y1 - 12), (x + w * 0.42, y1 - 18),
                   (x + w * 0.54, y1 - 18), (x + w * 0.58, y1 - 12)],
                  fill=(255, 80, 180))
        d.ellipse([x + w * 0.36, y1 - 6, x + w * 0.40, y1 - 2], fill=(17, 17, 17))
        d.ellipse([x + w * 0.56, y1 - 6, x + w * 0.60, y1 - 2], fill=(17, 17, 17))
        d.rectangle([x, y1 - 3, x1, y1], fill=(255, 80, 180))
        return
    if kind == "euaid":
        # EU shield in gold on blue, drone above it
        d.rectangle([x, y, x1, y1], fill=(18, 55, 115))
        cx, cy = x + w * 0.5, y + h * 0.52
        d.polygon([(cx, y + h * 0.10), (cx + w * 0.30, y + h * 0.24),
                   (cx + w * 0.30, y + h * 0.52), (cx, y + h * 0.86),
                   (cx - w * 0.30, y + h * 0.52), (cx - w * 0.30, y + h * 0.24)],
                  outline=(255, 204, 0), width=3)
        for k in range(12):
            a = 2 * math.pi * k / 12 - math.pi / 2
            sx = cx + math.cos(a) * w * 0.16
            sy = cy + math.sin(a) * h * 0.20
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 204, 0))
        d.ellipse([cx - 11, cy - 4, cx + 11, cy + 4], fill=(255, 255, 255))
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(178, 0, 0))
        # small drone top-right
        dx, dy = x + w * 0.80, y + h * 0.16
        d.rectangle([dx - 8, dy - 2, dx + 8, dy + 2], fill=(220, 220, 220))
        d.ellipse([dx - 13, dy - 5, dx - 7, dy + 1], fill=(220, 220, 220))
        d.ellipse([dx + 7, dy - 5, dx + 13, dy + 1], fill=(220, 220, 220))
        d.text((x + 6, y + 4), "\u20ac1bn", font=font(SANS_B, 15),
               fill=(255, 204, 0))
        return
    if kind == "euuk":
        # summit table in Brussels: EU + UK flags, papers, microphones
        d.rectangle([x, y, x1, y1], fill=(233, 226, 210))
        d.rectangle([x, y, x1, y + h * 0.52], fill=(40, 70, 130))
        # EU flag
        fx, fy, fw, fh = x + w * 0.08, y + h * 0.08, w * 0.34, h * 0.36
        d.rectangle([fx, fy, fx + fw, fy + fh], fill=(0, 51, 153))
        for k in range(12):
            a = 2 * math.pi * k / 12 - math.pi / 2
            sx = fx + fw / 2 + math.cos(a) * fw * 0.28
            sy = fy + fh / 2 + math.sin(a) * fh * 0.28
            d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 204, 0))
        # UK flag
        ux, uy, uw, uh = x + w * 0.58, y + h * 0.08, w * 0.34, h * 0.36
        d.rectangle([ux, uy, ux + uw, uy + uh], fill=(1, 33, 105))
        d.polygon([(ux, uy), (ux + uw * 0.18, uy), (ux + uw, uy + uh),
                   (ux + uw * 0.82, uy + uh)], fill=(255, 255, 255))
        d.polygon([(ux + uw, uy), (ux + uw, uy + uh * 0.18), (ux, uy + uh),
                   (ux, uy + uh * 0.82)], fill=(255, 255, 255))
        d.rectangle([ux + uw * 0.42, uy, ux + uw * 0.58, uy + uh],
                    fill=(255, 255, 255))
        d.rectangle([ux, uy + uh * 0.4, ux + uw, uy + uh * 0.6],
                    fill=(255, 255, 255))
        d.rectangle([ux + uw * 0.46, uy, ux + uw * 0.54, uy + uh],
                    fill=(200, 16, 46))
        d.rectangle([ux, uy + uh * 0.44, ux + uw, uy + uh * 0.56],
                    fill=(200, 16, 46))
        # long table with papers + microphones
        d.rectangle([x + w * 0.06, y + h * 0.62, x + w * 0.94, y + h * 0.70],
                    fill=(110, 80, 45))
        d.rectangle([x + w * 0.06, y + h * 0.70, x + w * 0.94, y1 - 4],
                    fill=(90, 64, 36))
        for px in (0.14, 0.42, 0.70):
            d.rectangle([x + w * px, y + h * 0.56, x + w * (px + 0.12),
                         y + h * 0.62], fill=(255, 255, 255))
            d.line([(x + w * (px + 0.06), y + h * 0.56),
                    (x + w * (px + 0.06), y + h * 0.48)], fill=(17, 17, 17),
                   width=1)
            d.ellipse([x + w * (px + 0.06) - 2, y + h * 0.46,
                       x + w * (px + 0.06) + 2, y + h * 0.50],
                      fill=(17, 17, 17))
        chip(d, x + 5, y + h - 16, "BRUSSELS", f_lab, bg=(17, 17, 17))
        return
    if kind == "poland":
        # radar screen: sweep, three red blips crossing in
        d.rectangle([x, y, x1, y1], fill=(8, 30, 14))
        cx, cy, r = x + w * 0.5, y + h * 0.52, min(w, h) * 0.42
        for rr in (0.4, 0.7, 1.0):
            d.ellipse([cx - r * rr, cy - r * rr, cx + r * rr, cy + r * rr],
                      outline=(40, 140, 70), width=1)
        d.line([(cx, cy - r), (cx, cy + r)], fill=(40, 140, 70), width=1)
        d.line([(cx - r, cy), (cx + r, cy)], fill=(40, 140, 70), width=1)
        d.polygon([(cx, cy), (cx + r * 0.7, cy - r * 0.7),
                   (cx + r * 0.85, cy - r * 0.45)], fill=(60, 200, 100))
        for bx, by in [(0.30, 0.30), (0.62, 0.22), (0.76, 0.44)]:
            d.ellipse([x + w * bx - 4, y + h * by - 4, x + w * bx + 4,
                       y + h * by + 4], fill=(255, 60, 40),
                      outline=(255, 255, 255), width=1)
        chip(d, x + 5, y + 5, "3 OBJECTS", f_lab, bg=(178, 0, 0))
        return
    if kind == "unicef":
        # schoolhouse under a hot sun, Ukrainian flag on a pole
        d.rectangle([x, y, x1, y1], fill=(245, 222, 160))
        d.ellipse([x + w * 0.76, y + 4, x + w * 0.92, y + h * 0.30],
                  fill=(255, 190, 60))
        d.rectangle([x + w * 0.10, y + h * 0.44, x + w * 0.60, y1 - 4],
                    fill=(30, 90, 160))
        d.polygon([(x + w * 0.06, y + h * 0.44), (x + w * 0.35, y + h * 0.20),
                   (x + w * 0.64, y + h * 0.44)], fill=(178, 0, 0))
        for wx in range(3):
            d.rectangle([x + w * 0.14 + wx * w * 0.14, y + h * 0.54,
                         x + w * 0.20 + wx * w * 0.14, y + h * 0.66],
                        fill=(255, 255, 255))
        d.rectangle([x + w * 0.31, y + h * 0.74, x + w * 0.39, y1 - 4],
                    fill=(255, 255, 255))
        # Ukrainian flag
        d.line([(x + w * 0.70, y + h * 0.30), (x + w * 0.70, y + h * 0.86)],
               fill=(60, 60, 60), width=2)
        d.rectangle([x + w * 0.70, y + h * 0.30, x + w * 0.86, y + h * 0.38],
                    fill=(0, 90, 180))
        d.rectangle([x + w * 0.70, y + h * 0.38, x + w * 0.86, y + h * 0.46],
                    fill=(255, 210, 0))
        for px, py in [(0.74, 0.88), (0.84, 0.90), (0.92, 0.88)]:
            d.ellipse([x + w * px - 3, y + h * py - 3, x + w * px + 3,
                       y + h * py + 3], fill=(178, 0, 0))
        return
    if kind == "haiti":
        # bright Port-au-Prince street, colourful houses, flag, shield
        d.rectangle([x, y, x1, y1], fill=(255, 214, 140))
        d.ellipse([x + w * 0.80, y + 4, x + w * 0.94, y + h * 0.26],
                  fill=(255, 240, 160))
        d.rectangle([x + w * 0.05, y + h * 0.46, x + w * 0.30, y1 - 4],
                    fill=(0, 120, 90))
        d.rectangle([x + w * 0.34, y + h * 0.30, x + w * 0.58, y1 - 4],
                    fill=(220, 90, 40))
        d.rectangle([x + w * 0.62, y + h * 0.52, x + w * 0.95, y1 - 4],
                    fill=(30, 90, 160))
        for bx, bw2 in [(0.05, 0.30), (0.34, 0.58), (0.62, 0.95)]:
            for wy in range(2):
                d.rectangle([x + w * (bx + 0.04), y + h * (0.56 + wy * 0.18),
                             x + w * (bx + 0.10), y + h * (0.66 + wy * 0.18)],
                            fill=(255, 255, 255))
        # Haitian flag on a pole
        d.line([(x + w * 0.47, y + h * 0.08), (x + w * 0.47, y + h * 0.32)],
               fill=(60, 60, 60), width=2)
        d.rectangle([x + w * 0.47, y + h * 0.08, x + w * 0.63, y + h * 0.14],
                    fill=(0, 60, 160))
        d.rectangle([x + w * 0.47, y + h * 0.14, x + w * 0.63, y + h * 0.20],
                    fill=(200, 30, 40))
        return
    if kind == "sudan":
        # desert gold mine at dusk, drone overhead, dust cloud
        d.rectangle([x, y, x1, y1], fill=(250, 225, 170))
        d.ellipse([x + w * 0.68, y + 4, x + w * 0.88, y + h * 0.32],
                  fill=(255, 170, 40))
        d.polygon([(x, y1), (x + w * 0.35, y + h * 0.55), (x + w * 0.7, y1)],
                  fill=(220, 170, 90))
        d.polygon([(x + w * 0.55, y1), (x + w * 0.85, y + h * 0.62),
                   (x + w, y1)], fill=(205, 150, 70))
        # mine building + headframe
        d.rectangle([x + w * 0.10, y + h * 0.56, x + w * 0.34, y + h * 0.86],
                    fill=(120, 85, 50))
        d.polygon([(x + w * 0.08, y + h * 0.56), (x + w * 0.22, y + h * 0.42),
                   (x + w * 0.36, y + h * 0.56)], fill=(90, 60, 35))
        d.line([(x + w * 0.40, y + h * 0.86), (x + w * 0.40, y + h * 0.44)],
               fill=(60, 40, 25), width=2)
        d.line([(x + w * 0.40, y + h * 0.44), (x + w * 0.48, y + h * 0.60)],
               fill=(60, 40, 25), width=2)
        d.line([(x + w * 0.40, y + h * 0.44), (x + w * 0.32, y + h * 0.60)],
               fill=(60, 40, 25), width=2)
        # drone in the sky
        dx, dy = x + w * 0.52, y + h * 0.20
        d.rectangle([dx - 9, dy - 2, dx + 9, dy + 2], fill=(40, 40, 40))
        d.ellipse([dx - 15, dy - 6, dx - 8, dy, ], fill=(40, 40, 40))
        d.ellipse([dx + 8, dy - 6, dx + 15, dy, ], fill=(40, 40, 40))
        # dust cloud over the mine
        for cx, cy, cr in [(0.20, 0.52, 0.05), (0.28, 0.48, 0.06),
                           (0.36, 0.52, 0.05)]:
            d.ellipse([x + w * (cx - cr), y + h * (cy - cr),
                       x + w * (cx + cr), y + h * (cy + cr)],
                      fill=(235, 210, 160))
        chip(d, x + 5, y + 5, "BAJOUN MINE", f_lab, bg=(17, 17, 17))
        return
    d.rectangle([x, y, x1, y1], fill=(220, 220, 220))


# ---------------------------------------------------------------- content
LEADS = [
    dict(num=1, tag="UKRAINE", src="BBC \u00b7 REUTERS", kind="kyiv",
         ver="CONFIRMED",
         head="Russia's overnight barrage batters Kyiv",
         text="110+ missiles and 400+ drones; three Dnipro bridges hit; "
              "at least 8 killed, 28 hurt."),
    dict(num=2, tag="WEATHER \u00b7 INDIA", src="IMD \u00b7 REUTERS",
         kind="akvan", ver="CONFIRMED",
         head="Cyclone Akvan hits India's east coast",
         text="Landfall at Gopalpur, 07:30 IST; winds 70\u201380, gusts 90; "
              "300,000+ sheltered, no deaths reported."),
    dict(num=3, tag="MARKETS", src="CNBC \u00b7 AL JAZEERA", kind="markets",
         ver="CONFIRMED",
         head="Stocks slide worldwide",
         text="Nikkei down 4.8%, S&P 500 down 2% as AI doubts spread; "
              "SoftBank falls 16%."),
]

GRID = [
    dict(num=4, tag="CLIMATE \u00b7 ANTALYA", kind="cop31", ver="REPORTED",
         head="COP31 enters final day with no deal in sight",
         line="Draft drops fossil fuels, $120bn aid; Panama vows to block."),
    dict(num=5, tag="SPACE \u00b7 ESA/JAXA", kind="bepi", ver="CONFIRMED",
         head="BepiColombo reaches Mercury after eight years",
         line="ESA\u2013JAXA probe reaches Mercury; thrusters fire Saturday."),
    dict(num=6, tag="ESTONIA \u00b7 REUTERS", kind="estonia", ver="CONFIRMED",
         head="Estonia to shut Russia border from 1 Dec",
         line="Crossings shut for six months; Moscow cries \u2018new Iron "
              "Curtain\u2019."),
    dict(num=7, tag="CULTURE \u00b7 BBC", kind="gta6", ver="REPORTED",
         head="GTA 6 tops $2.3bn in day one",
         line="Day-one sales above $2.3bn, a record for entertainment."),
    dict(num=8, tag="EUROPE \u00b7 EU COUNCIL", kind="euaid", ver="CONFIRMED",
         head="EU approves \u20ac1bn arms aid for Ukraine",
         line="Drones, air defence and ammunition, delivered by end 2027."),
    dict(num=9, tag="EUROPE \u00b7 BBC", kind="euuk", ver="CONFIRMED",
         head="EU and UK seal post-Brexit reset deal",
         line="Trade checks eased, emissions linked; youth mobility opens."),
    dict(num=10, tag="UKRAINE \u00b7 UNICEF", kind="unicef", ver="CONFIRMED",
         head="1,144 children killed or hurt in 2026",
         line="UNICEF: toll near 2022 levels as Russian strikes intensify."),
    dict(num=11, tag="AMERICAS \u00b7 AL JAZEERA", kind="haiti",
         ver="REPORTED",
         head="Haiti forces kill 34 in gang raid",
         line="Police say 34 suspected gang members died in the raid."),
    dict(num=12, tag="AFRICA \u00b7 ALLAFRICA", kind="sudan", ver="REPORTED",
         head="Drone strike kills 10 at Sudan gold mine",
         line="Ten die in a drone strike on the Bajoun mine in S. Kordofan."),
    dict(num=13, tag="EUROPE \u00b7 REUTERS", kind="poland", ver="REPORTED",
         head="Russian missiles breach Polish airspace",
         line="Warsaw: three objects crossed \u2014 two missiles and a drone."),
]

NUMBERS = [
    ("-4.8%", "NIKKEI, FRIDAY"),
    ("-2%", "S&P 500, THURSDAY"),
    ("$2.3bn+", "GTA 6 DAY-ONE SALES (EST.)"),
    ("\u20ac1bn", "EU ARMS AID FOR UKRAINE"),
    ("300,000+", "MOVED FROM AKVAN'S PATH"),
    ("1,144", "UKRAINE CHILD CASUALTIES, 2026"),
]

TIMELINE = [
    ("OVERNIGHT", "Russia's barrage hits Kyiv"),
    ("02:00 UTC", "Akvan landfall at Gopalpur"),
    ("ASIA MORNING", "Nikkei falls 4.8%"),
    ("MIDDAY", "EU\u2013UK summit seals reset deal"),
    ("15:50 CET", "EU approves \u20ac1bn arms aid"),
    ("EVENING", "Trump: \u201cvery good talks\u201d with Putin"),
]

# ALSO ON: (number, region, text) -- 22 items, 14-35, one line each
ALSO_A = [
    (14, "EUROPE", "UK admits cyber attacks on Russia, China, Iran, N. Korea"),
    (15, "EUROPE", "EU disburses record \u20ac7.9bn to Ukraine"),
    (16, "EUROPE", "Georgia declares 22 Nov mourning for Tbilisi victims"),
    (17, "EUROPE", "Youth in 25+ countries strike over costs, rearmament"),
    (18, "ASIA & PACIFIC", "S. Korea ruling party moves to impeach top judge"),
    (19, "ASIA & PACIFIC", "Mongolia bids farewell to President Kh\u00fcrels\u00fckh"),
    (20, "ASIA & PACIFIC", "Cyclone Xavier downgraded to category 4, Cook Is."),
    (21, "ASIA & PACIFIC", "Pakistan says 22 militants killed in NW raids"),
    (22, "ASIA & PACIFIC", "Japan inflation at year's high as subsidies end"),
    (23, "AFRICA", "Dozens missing after migrant boat capsizes off Senegal"),
    (24, "AFRICA", "Somalia expels UAE ambassador"),
    (25, "AFRICA", "Strikes reported near Badme, Ethiopia\u2013Eritrea border"),
]
ALSO_B = [
    (26, "MIDDLE EAST", "IEA: Iran war scars energy; Brent $90.05"),
    (27, "MIDDLE EAST", "Mosque set on fire in northern Israel"),
    (28, "MIDDLE EAST", "S. Africa: ICJ Myanmar ruling bolsters Gaza case"),
    (29, "MIDDLE EAST", "Iraq moves on Iran-backed militia base, Jurf al-Sakhar"),
    (30, "AMERICAS", "Thousands protest Colombia's tax plans"),
    (31, "AMERICAS", "Bukele registers for a third term in El Salvador"),
    (32, "AMERICAS", "Trump: \u201cvery good talks\u201d with Putin on Ukraine"),
    (33, "AMERICAS", "Brazil central bank sells $1bn as the real slides"),
    (34, "AMERICAS", "White House fires cyber chief after outages"),
    (35, "GLOBAL", "IMF: global public debt nearing 100% of GDP"),
]

DATECHECK_LEFT = [
    "Shenzhen summit: Trump, Xi and Putin met Thursday 19 Nov",
    "ICJ Myanmar ruling: Thursday 19 Nov (9\u20136, genocide)",
    "Anthropic's Nasdaq debut: Thursday 19 Nov (+17% close)",
    "COP31 draft dropping fossil-fuel phase-out: Thursday 19 Nov",
    "Kerch Bridge hit a third time: overnight 18\u201319 Nov",
    "Houthi strike on Riyadh's PIF tower: early Thursday 19 Nov",
]
DATECHECK_RIGHT = [
    "Pete Rose pardon: Thursday 19 Nov",
    "Kenya's last Ebola patient went home: 11 Nov",
    "Fiona the hippo died: Thursday 19 Nov",
    "Tbilisi gas blast that killed six: Thursday 19 Nov",
    "NOT YET: EU\u2013UK youth scheme \u2014 in force only if the UK cuts EU "
    "student fees in six months",
]

# (number, lon, lat, dx, dy) -- pins match the numbered pictured stories
PINS = [
    (1, -74.0, 40.7, 10, -10),
    (2, 30.5, 50.45, 0, 0),
    (3, 84.9, 19.3, 0, 0),
    (4, 30.7, 36.9, 0, 0),
    (5, 8.65, 49.87, 0, 0),
    (6, 24.75, 59.44, 0, 0),
    (7, -3.19, 55.95, 0, 0),
    (8, 4.35, 50.85, 0, 0),
    (9, 4.35, 50.85, 12, -10),
    (10, 30.5, 50.45, -12, 10),
    (11, -72.34, 18.54, 0, 0),
    (12, 30.0, 11.5, 0, 0),
    (13, 21.01, 52.23, 0, 0),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 14
    X0, X1 = M, W - M
    CW = X1 - X0
    PHOTO = Image.open(os.path.join(HERE, "photos",
                                    "akvan-2026-11-18.jpg")).convert("RGB")

    f_name = font(SERIF_B, 19)
    f_date = font(SERIF_B, 48)
    f_count = font(SANS_B, 16)
    f_num_fig = font(SANS_B, 20)
    f_num_lab = font(SANS_B, 9)
    f_tl_head = font(SANS_B, 11)
    f_tl_time = font(SANS_B, 10)
    f_tl_txt = font(SANS, 10)
    f_lead_tag = font(SANS_B, 12)
    f_lead_head = font(SERIF_B, 21)
    f_lead_line = font(SANS, 12)
    f_lead_src = font(SANS, 10)
    f_grid_tag = font(SANS_B, 9)
    f_grid_head = font(SANS_B, 13)
    f_grid_line = font(SANS, 10)
    f_sec = font(SANS_B, 13)
    f_also_head = font(SANS_B, 9)
    f_also = font(SANS, 8)
    f_dc_head = font(SANS_B, 11)
    f_dc = font(SANS, 9)

    # ---- masthead
    d.text((W // 2, 8), "THE WORLD IN ONE PAGE", font=f_name, fill=INK,
           anchor="ma")
    d.text((W // 2, 28), "FRIDAY 20 NOVEMBER 2026", font=f_date, fill=INK,
           anchor="ma")
    d.text((W // 2, 82), "35 STORIES \u00b7 7 REGIONS \u00b7 ALL FROM THIS FRIDAY",
           font=f_count, fill=RED, anchor="ma")
    rule(d, X0, X1, 104, wdt=2)
    rule(d, X0, X1, 108, wdt=1)

    # ---- numbers strip
    y0 = 114
    bw = (CW - 5 * 6) // 6
    for i, (fig, lab) in enumerate(NUMBERS):
        bx = X0 + i * (bw + 6)
        d.rectangle([bx, y0, bx + bw, y0 + 36], outline=(180, 176, 168), width=1)
        d.text((bx + bw // 2, y0 + 3), fig, font=f_num_fig, fill=RED, anchor="ma")
        d.text((bx + bw // 2, y0 + 24), lab, font=f_num_lab, fill=INK, anchor="ma")

    # ---- timeline
    y = 158
    d.text((X0, y), "THE DAY IN TIME", font=f_tl_head, fill=INK)
    d.text((X1, y), "ALL TIMES UTC UNLESS MARKED", font=f_tl_head, fill=GREY,
           anchor="ra")
    ty = 184
    rule(d, X0, X1, ty, fill=(150, 146, 138), wdt=2)
    seg = CW / len(TIMELINE)
    for i, (t, txt) in enumerate(TIMELINE):
        cx = int(X0 + seg * i + seg / 2)
        d.ellipse([cx - 5, ty - 5, cx + 5, ty + 5], fill=RED)
        d.text((cx, ty - 16), t, font=f_tl_time, fill=RED, anchor="ma")
        lines = wrap(txt, f_tl_txt, int(seg - 8))
        yy = ty + 10
        for ln in lines[:2]:
            d.text((cx, yy), ln, font=f_tl_txt, fill=INK, anchor="ma")
            yy += 12

    # ---- leads
    ly = 222
    colw = (CW - 2 * 10) // 3
    for i, s in enumerate(LEADS):
        lx = X0 + i * (colw + 10)
        scene(d, lx, ly, colw, 112, s["kind"], img=PHOTO, base=img)
        ty2 = ly + 118
        d.text((lx, ty2), s["tag"], font=f_lead_tag, fill=RED)
        d.text((lx + colw, ty2), s["ver"], font=f_lead_tag, fill=GREY,
               anchor="ra")
        hy = ty2 + 17
        lines = wrap(s["head"], f_lead_head, colw)
        hy = text_lines(d, lx, hy, lines[:2], f_lead_head, lh=24)
        sy = hy + 2
        slines = wrap(s["text"], f_lead_line, colw)
        sy = text_lines(d, lx, sy, slines[:2], f_lead_line, lh=15)
        d.text((lx, sy + 2), "Source: " + s["src"], font=f_lead_src, fill=GREY)
        if i < 2:
            d.line([(lx + colw + 5, ly), (lx + colw + 5, ly + 224)],
                   fill=LIGHT, width=1)
    rule(d, X0, X1, 452, fill=INK, wdt=1)

    # ---- pictured grid, 2 rows x 5
    gy = 460
    gw = (CW - 4 * 9) // 5
    gh = 128
    for r in range(2):
        for c in range(5):
            s = GRID[r * 5 + c]
            gx = X0 + c * (gw + 9)
            gy2 = gy + r * gh
            scene(d, gx, gy2, gw, 48, s["kind"], img=PHOTO, base=img)
            ty3 = gy2 + 52
            d.text((gx, ty3), s["tag"], font=f_grid_tag, fill=RED)
            d.text((gx + gw, ty3), s["ver"], font=f_grid_tag, fill=GREY,
                   anchor="ra")
            hy = ty3 + 12
            lines = wrap(s["head"], f_grid_head, gw)
            hy = text_lines(d, gx, hy, lines[:2], f_grid_head, lh=15)
            ln = wrap(s["line"], f_grid_line, gw)
            text_lines(d, gx, hy + 1, ln[:2], f_grid_line, lh=12)
    rule(d, X0, X1, 718, fill=INK, wdt=1)

    # ---- bottom third
    by = 726
    d.text((X0, by), "WHERE IT HAPPENED", font=f_sec, fill=INK)
    d.text((X0 + 358, by), "ALSO ON \u2014 22 MORE STORIES (14\u201335)",
           font=f_sec, fill=INK)
    rule(d, X0, X1, by + 18, fill=INK, wdt=1)

    # dotted world map
    mx, my, mw, mh = X0, by + 22, 342, 132
    d.rectangle([mx, my, mx + mw, my + mh], outline=(180, 176, 168), width=1)
    lon0, lon1, lat0, lat1 = -170, 190, 78, -58
    step = 6
    gx = mx + 4
    while gx < mx + mw - 2:
        gy3 = my + 4
        while gy3 < my + mh - 2:
            lon = lon0 + (gx - mx) / mw * (lon1 - lon0)
            lat = lat0 - (gy3 - my) / mh * (lat0 - lat1)
            if on_land(lon, lat):
                d.ellipse([gx - 1, gy3 - 1, gx + 1, gy3 + 1], fill=MAPDOT)
            gy3 += step
        gx += step
    f_pin = font(SANS_B, 9)
    for num, lon, lat, dx, dy in PINS:
        px = mx + (lon - lon0) / (lon1 - lon0) * mw + dx
        py = my + (lat0 - lat) / (lat0 - lat1) * mh + dy
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((px, py - 6), str(num), font=f_pin, fill=(255, 255, 255),
               anchor="ma")
    d.text((X0, my + mh + 4), "Pins match the numbered stories above.",
           font=f_also, fill=GREY)

    # ALSO ON columns, numbered, one line each (warn if any wraps)
    ax = X0 + 358
    colw2 = (X1 - ax - 12) // 2

    def also_col(x, items, ytop):
        yy = ytop
        cur_region = None
        for num, region, txt in items:
            if region != cur_region:
                cur_region = region
                d.text((x, yy), region, font=f_also_head, fill=RED)
                yy += 11
            line = f"{num}. {txt}"
            if f_also.getlength(line) > colw2 - 8:
                print(f"WARNING: ALSO item too wide: {line!r} "
                      f"({f_also.getlength(line):.0f} > {colw2 - 8})")
            d.text((x, yy), line, font=f_also, fill=INK)
            yy += 10
        return yy

    also_col(ax, ALSO_A, by + 22)
    also_col(ax + colw2 + 12, ALSO_B, by + 22)

    # ---- DATE CHECK box
    dy = 908
    d.rectangle([X0, dy, X1, dy + 90], outline=RED, width=2)
    d.text((X0 + 8, dy + 6),
           "DATE CHECK \u2014 NOT TODAY'S NEWS: THESE BIG STORIES HAPPENED "
           "BEFORE FRIDAY",
           font=f_dc_head, fill=RED)
    yy = dy + 26
    for t in DATECHECK_LEFT:
        d.text((X0 + 8, yy), "\u2022 " + t, font=f_dc, fill=INK)
        yy += 11
    yy = dy + 26
    for t in DATECHECK_RIGHT:
        lines = wrap("\u2022 " + t, f_dc, 480)
        for ln in lines:
            d.text((X0 + 500, yy), ln, font=f_dc, fill=INK)
            yy += 11

    # ---- footer (one line, shrink until it fits)
    foot = ("Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 BBC \u00b7 Al Jazeera "
            "\u00b7 CNBC \u00b7 EU Council \u00b7 UNICEF \u00b7 SCMP \u00b7 "
            "Carbon Brief \u00b7 UN News \u00b7 IMD \u2014 Akvan photo: "
            "JTWC/NASA. Every event happened, or was first reported, on "
            "Friday 20 November 2026.")
    for fsize in (8, 7):
        f_foot = font(SANS, fsize)
        if f_foot.getlength(foot) <= CW:
            break
    d.text((W // 2, 1004), foot, font=f_foot, fill=GREY, anchor="ma")

    img.save(OUT, "PNG")
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
