#!/usr/bin/env python3
"""Build the make.fun news-image-20261120 entry: a dense newspaper front page
summing up Friday 20 November 2026. Flat illustrations drawn in code, all
text set with real fonts. Writes entry.png (1024x1024) next to this script."""

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

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = os.path.join(FD, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FD, "DejaVuSans.ttf")
SANS_B = os.path.join(FD, "DejaVuSans-Bold.ttf")


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


# ---------------------------------------------------------------- scenes
def scene(d, x, y, w, h, kind):
    """Flat illustration inside box (x, y, w, h). No text inside."""
    x1, y1 = x + w, y + h
    if kind == "markets":
        d.rectangle([x, y, x1, y1], fill=(24, 28, 40))
        n = 7
        bw = w / (n * 1.6)
        vals = [0.85, 0.7, 0.78, 0.55, 0.62, 0.4, 0.28]
        for i, v in enumerate(vals):
            bx = x + 8 + i * (w - 16) / n
            bh = v * (h - 18)
            col = (200, 60, 50) if i >= 3 else (70, 130, 90)
            d.rectangle([bx, y1 - 6 - bh, bx + bw, y1 - 6], fill=col)
        pts = [(x + 8 + i * (w - 16) / (n - 1), y + 10 + (0.15 + 0.11 * i) * h)
               for i in range(n)]
        d.line(pts, fill=(230, 90, 70), width=3)
        for px, py in pts:
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 255, 255))
    elif kind == "kyiv":
        d.rectangle([x, y, x1, y1], fill=(18, 24, 52))
        for sx, sy in [(x + w * 0.2, y + 12), (x + w * 0.55, y + 8), (x + w * 0.8, y + 16)]:
            d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
        d.ellipse([x + w * 0.62, y + h * 0.42, x + w * 0.82, y + h * 0.75],
                  fill=(255, 140, 40))
        d.ellipse([x + w * 0.66, y + h * 0.5, x + w * 0.78, y + h * 0.72],
                  fill=(255, 190, 80))
        d.rectangle([x, y + h * 0.62, x + w * 0.22, y1], fill=(10, 12, 28))
        d.rectangle([x + w * 0.26, y + h * 0.5, x + w * 0.46, y1], fill=(12, 14, 32))
        d.rectangle([x + w * 0.5, y + h * 0.55, x + w * 0.98, y1], fill=(10, 12, 28))
        for wx in range(6):
            d.rectangle([x + w * 0.28 + wx * 8, y + h * 0.56,
                         x + w * 0.28 + wx * 8 + 4, y + h * 0.62],
                        fill=(255, 200, 90))
        # smoke rising from the fire
        for cx, cy, cw, ch in [(0.64, 0.10, 0.07, 0.28), (0.72, 0.04, 0.06, 0.24),
                               (0.30, 0.12, 0.08, 0.30)]:
            d.ellipse([x + w * cx, y + h * cy, x + w * (cx + cw), y + h * (cy + ch)],
                      fill=(120, 120, 130))
    elif kind == "euuk":
        d.rectangle([x, y, x1, y1], fill=(232, 228, 218))
        fx, fy, fw, fh = x + w * 0.06, y + h * 0.18, w * 0.40, h * 0.64
        d.rectangle([fx, fy, fx + fw, fy + fh], fill=(0, 51, 153))
        for k in range(12):
            a = 2 * math.pi * k / 12 - math.pi / 2
            sx = fx + fw / 2 + math.cos(a) * fw * 0.30
            sy = fy + fh / 2 + math.sin(a) * fh * 0.30
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 204, 0))
        ux, uy, uw, uh = x + w * 0.54, y + h * 0.18, w * 0.40, h * 0.64
        d.rectangle([ux, uy, ux + uw, uy + uh], fill=(1, 33, 105))
        d.polygon([(ux, uy), (ux + uw * 0.18, uy), (ux + uw, uy + uh),
                   (ux + uw * 0.82, uy + uh)], fill=(255, 255, 255))
        d.polygon([(ux + uw, uy), (ux + uw, uy + uh * 0.18), (ux, uy + uh),
                   (ux, uy + uh * 0.82)], fill=(255, 255, 255))
        d.rectangle([ux + uw * 0.42, uy, ux + uw * 0.58, uy + uh], fill=(255, 255, 255))
        d.rectangle([ux, uy + uh * 0.4, ux + uw, uy + uh * 0.6], fill=(255, 255, 255))
        d.rectangle([ux + uw * 0.46, uy, ux + uw * 0.54, uy + uh], fill=(200, 16, 46))
        d.rectangle([ux, uy + uh * 0.44, ux + uw, uy + uh * 0.56], fill=(200, 16, 46))
        d.rectangle([x, y1 - 6, x1, y1], fill=(120, 110, 95))
    elif kind == "estonia":
        d.rectangle([x, y, x1, y1], fill=(214, 228, 240))
        d.polygon([(x, y1), (x + w * 0.3, y + h * 0.55), (x + w * 0.6, y1)],
                  fill=(235, 240, 246))
        d.polygon([(x + w * 0.55, y1), (x + w * 0.8, y + h * 0.5),
                   (x + w, y1)], fill=(228, 236, 244))
        for tx in (0.14, 0.86):
            cx = x + w * tx
            d.polygon([(cx, y + h * 0.42), (cx - w * 0.05, y + h * 0.72),
                       (cx + w * 0.05, y + h * 0.72)], fill=(34, 90, 60))
            d.rectangle([cx - 2, y + h * 0.72, cx + 2, y + h * 0.82], fill=(90, 60, 30))
        d.rectangle([x + w * 0.30, y + h * 0.62, x + w * 0.70, y + h * 0.66],
                    fill=(200, 40, 40))
        d.rectangle([x + w * 0.30, y + h * 0.72, x + w * 0.70, y + h * 0.76],
                    fill=(240, 240, 240))
        for bx in range(4):
            d.rectangle([x + w * 0.32 + bx * w * 0.10, y + h * 0.62,
                         x + w * 0.36 + bx * w * 0.10, y + h * 0.76],
                        fill=(60, 60, 60))
        d.rectangle([x + w * 0.74, y + h * 0.60, x + w * 0.92, y + h * 0.82],
                    fill=(150, 160, 175))
        d.polygon([(x + w * 0.72, y + h * 0.60), (x + w * 0.83, y + h * 0.48),
                   (x + w * 0.94, y + h * 0.60)], fill=(120, 40, 40))
    elif kind == "gta6":
        d.rectangle([x, y, x1, y1], fill=(16, 10, 34))
        for sx, sy in [(x + w * 0.1, y + 8), (x + w * 0.4, y + 14), (x + w * 0.7, y + 6),
                       (x + w * 0.9, y + 18)]:
            d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
        d.ellipse([x + w * 0.78, y + 6, x + w * 0.92, y + h * 0.28], fill=(255, 210, 90))
        heights = [0.45, 0.65, 0.5, 0.75, 0.58, 0.68, 0.42]
        cols = [(255, 80, 180), (60, 220, 230), (255, 200, 60), (120, 90, 255),
                (255, 80, 180), (60, 220, 230), (255, 200, 60)]
        bw = w / len(heights)
        for i, hh in enumerate(heights):
            bx = x + i * bw
            d.rectangle([bx + 2, y1 - hh * h, bx + bw - 2, y1], fill=(28, 20, 55))
            for wy in range(3):
                d.rectangle([bx + 4, y1 - hh * h + 6 + wy * 12,
                             bx + bw - 4, y1 - hh * h + 12 + wy * 12],
                            fill=cols[i])
        d.rectangle([x, y1 - 4, x1, y1], fill=(255, 80, 180))
    elif kind == "euaid":
        d.rectangle([x, y, x1, y1], fill=(20, 60, 120))
        d.polygon([(x + w * 0.5, y + h * 0.12), (x + w * 0.82, y + h * 0.28),
                   (x + w * 0.82, y + h * 0.55), (x + w * 0.5, y + h * 0.88),
                   (x + w * 0.18, y + h * 0.55), (x + w * 0.18, y + h * 0.28)],
                  outline=(255, 204, 0), width=3)
        cx, cy = x + w * 0.5, y + h * 0.48
        d.ellipse([cx - 14, cy - 5, cx + 14, cy + 5], fill=(255, 255, 255))
        for dx, dy in [(-18, -10), (18, -10), (-18, 10), (18, 10)]:
            d.line([(cx + dx, cy + dy), (cx + dx * 0.5, cy + dy * 0.5)],
                   fill=(255, 255, 255), width=2)
            d.ellipse([cx + dx - 6, cy + dy - 2, cx + dx + 6, cy + dy + 2],
                      fill=(255, 204, 0))
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(178, 0, 0))
    elif kind == "poland":
        d.rectangle([x, y, x1, y1], fill=(170, 205, 235))
        for rx in range(3):
            d.arc([x + w * 0.1 + rx * 8, y + h * 0.15 + rx * 8,
                   x + w * 0.9 - rx * 8, y + h * 0.95 - rx * 8],
                  start=200, end=340, fill=(255, 255, 255), width=2)
        cx, cy = x + w * 0.55, y + h * 0.45
        d.polygon([(cx - 26, cy), (cx + 26, cy), (cx + 10, cy - 6), (cx - 10, cy - 6)],
                  fill=(60, 60, 60))
        d.polygon([(cx + 26, cy), (cx + 38, cy - 10), (cx + 26, cy - 4)],
                  fill=(60, 60, 60))
        d.rectangle([x + w * 0.06, y + h * 0.78, x + w * 0.30, y + h * 0.88],
                    fill=(255, 255, 255))
        d.rectangle([x + w * 0.06, y + h * 0.88, x + w * 0.30, y + h * 0.98],
                    fill=(220, 40, 60))
        d.polygon([(x + w * 0.30, y + h * 0.78), (x + w * 0.30, y + h * 0.98),
                   (x + w * 0.34, y + h * 0.88)], fill=(120, 120, 120))
    elif kind == "unicef":
        d.rectangle([x, y, x1, y1], fill=(245, 222, 160))
        d.ellipse([x + w * 0.74, y + 6, x + w * 0.90, y + h * 0.30], fill=(255, 190, 60))
        d.rectangle([x + w * 0.08, y + h * 0.42, x + w * 0.60, y1 - 4], fill=(30, 90, 160))
        d.polygon([(x + w * 0.04, y + h * 0.42), (x + w * 0.34, y + h * 0.18),
                   (x + w * 0.64, y + h * 0.42)], fill=(178, 0, 0))
        for wx in range(3):
            d.rectangle([x + w * 0.13 + wx * w * 0.14, y + h * 0.52,
                         x + w * 0.19 + wx * w * 0.14, y + h * 0.64],
                        fill=(255, 255, 255))
        d.rectangle([x + w * 0.30, y + h * 0.72, x + w * 0.38, y1 - 4],
                    fill=(255, 255, 255))
        for px, py in [(0.70, 0.82), (0.80, 0.86), (0.90, 0.82)]:
            d.ellipse([x + w * px - 4, y + h * py - 4, x + w * px + 4, y + h * py + 4],
                      fill=(178, 0, 0))
            d.rectangle([x + w * px - 2, y + h * py + 4, x + w * px + 2,
                         y + h * py + 12], fill=(178, 0, 0))
    elif kind == "haiti":
        d.rectangle([x, y, x1, y1], fill=(255, 214, 140))
        d.rectangle([x + w * 0.05, y + h * 0.45, x + w * 0.30, y1 - 4], fill=(0, 120, 90))
        d.rectangle([x + w * 0.34, y + h * 0.30, x + w * 0.58, y1 - 4], fill=(220, 90, 40))
        d.rectangle([x + w * 0.62, y + h * 0.50, x + w * 0.95, y1 - 4], fill=(30, 90, 160))
        for bx, bw2 in [(0.05, 0.30), (0.34, 0.58), (0.62, 0.95)]:
            for wy in range(2):
                d.rectangle([x + w * (bx + 0.04), y + h * (0.55 + wy * 0.18),
                             x + w * (bx + 0.10), y + h * (0.65 + wy * 0.18)],
                            fill=(255, 255, 255))
        d.rectangle([x + w * 0.46, y + h * 0.08, x + w * 0.47, y + h * 0.30],
                    fill=(60, 60, 60))
        d.polygon([(x + w * 0.47, y + h * 0.08), (x + w * 0.62, y + h * 0.13),
                   (x + w * 0.47, y + h * 0.18)], fill=(0, 60, 160))
    elif kind == "sudan":
        d.rectangle([x, y, x1, y1], fill=(250, 225, 170))
        d.ellipse([x + w * 0.68, y + 4, x + w * 0.88, y + h * 0.32], fill=(255, 170, 40))
        d.polygon([(x, y1), (x + w * 0.35, y + h * 0.55), (x + w * 0.7, y1)],
                  fill=(220, 170, 90))
        d.polygon([(x + w * 0.55, y1), (x + w * 0.85, y + h * 0.62), (x + w, y1)],
                  fill=(205, 150, 70))
        d.rectangle([x + w * 0.10, y + h * 0.55, x + w * 0.34, y + h * 0.85],
                    fill=(120, 85, 50))
        d.polygon([(x + w * 0.08, y + h * 0.55), (x + w * 0.22, y + h * 0.42),
                   (x + w * 0.36, y + h * 0.55)], fill=(90, 60, 35))
        d.rectangle([x + w * 0.16, y + h * 0.64, x + w * 0.28, y + h * 0.85],
                    fill=(60, 40, 25))
    elif kind == "iraq":
        d.rectangle([x, y, x1, y1], fill=(235, 220, 190))
        d.rectangle([x + w * 0.08, y + h * 0.40, x + w * 0.42, y1 - 4], fill=(200, 180, 140))
        d.rectangle([x + w * 0.46, y + h * 0.55, x + w * 0.92, y1 - 4], fill=(180, 160, 120))
        d.polygon([(x + w * 0.08, y + h * 0.40), (x + w * 0.25, y + h * 0.25),
                   (x + w * 0.42, y + h * 0.40)], fill=(140, 60, 50))
        d.rectangle([x + w * 0.60, y + h * 0.12, x + w * 0.62, y + h * 0.55],
                    fill=(60, 60, 60))
        d.rectangle([x + w * 0.62, y + h * 0.12, x + w * 0.82, y + h * 0.20],
                    fill=(200, 30, 40))
        d.rectangle([x + w * 0.62, y + h * 0.20, x + w * 0.82, y + h * 0.28],
                    fill=(255, 255, 255))
        d.rectangle([x + w * 0.62, y + h * 0.28, x + w * 0.82, y + h * 0.36],
                    fill=(20, 20, 20))
        d.ellipse([x + w * 0.70, y + h * 0.70, x + w * 0.78, y + h * 0.82],
                  fill=(255, 200, 60))
    elif kind == "cyber":
        d.rectangle([x, y, x1, y1], fill=(16, 22, 38))
        for i in range(4):
            yy = y + 10 + i * (h - 20) / 3
            d.line([(x + 6, yy), (x + w - 6, yy)], fill=(40, 90, 140), width=1)
            d.ellipse([x + w * 0.25, yy - 3, x + w * 0.25 + 6, yy + 3],
                      fill=(80, 200, 255))
            d.ellipse([x + w * 0.70, yy - 3, x + w * 0.70 + 6, yy + 3],
                      fill=(255, 90, 90))
        d.rectangle([x + w * 0.40, y + h * 0.30, x + w * 0.60, y + h * 0.72],
                    fill=(255, 204, 0))
        d.rectangle([x + w * 0.44, y + h * 0.18, x + w * 0.56, y + h * 0.32],
                    outline=(255, 204, 0), width=3)
        d.ellipse([x + w * 0.48, y + h * 0.44, x + w * 0.52, y + h * 0.50],
                  fill=(16, 22, 38))
    elif kind == "japan":
        d.rectangle([x, y, x1, y1], fill=(245, 240, 230))
        d.ellipse([x + w * 0.08, y + h * 0.22, x + w * 0.34, y + h * 0.78],
                  fill=(255, 210, 60), outline=(200, 150, 0), width=2)
        d.rectangle([x + w * 0.13, y + h * 0.46, x + w * 0.29, y + h * 0.52],
                    fill=(120, 90, 0))
        d.rectangle([x + w * 0.20, y + h * 0.32, x + w * 0.22, y + h * 0.68],
                    fill=(120, 90, 0))
        pts = [(x + w * 0.40, y + h * 0.72), (x + w * 0.55, y + h * 0.55),
               (x + w * 0.68, y + h * 0.62), (x + w * 0.85, y + h * 0.28)]
        d.line(pts, fill=(178, 0, 0), width=3)
        d.polygon([(x + w * 0.85, y + h * 0.28), (x + w * 0.78, y + h * 0.28),
                   (x + w * 0.85, y + h * 0.38)], fill=(178, 0, 0))
        for px, py in pts:
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(178, 0, 0))


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


# ---------------------------------------------------------------- content
LEADS = [
    dict(num=1, tag="MARKETS", src="CNBC \u00b7 AL JAZEERA", kind="markets",
         ver="CONFIRMED",
         head="Stocks slide worldwide",
         text="Nikkei down 4.8%, S&P 500 down 2% as AI doubts spread; SoftBank falls 16%."),
    dict(num=2, tag="UKRAINE", src="BBC", kind="kyiv", ver="CONFIRMED",
         head="Russia's overnight barrage batters Kyiv",
         text="Bridges, power and rail hit; embassies and a cathedral damaged; Kyiv says 8 killed."),
    dict(num=3, tag="EUROPE", src="BBC \u00b7 AL JAZEERA", kind="euuk", ver="CONFIRMED",
         head="EU and UK seal post-Brexit reset deal",
         text="Trade checks eased and emissions schemes linked; youth mobility for 100,000 under-30s a year."),
]

GRID = [
    dict(num=4, tag="ESTONIA \u00b7 REUTERS", kind="estonia", ver="CONFIRMED",
         head="Estonia to shut Russia border from 1 Dec",
         line="Crossings close for six months; Moscow cries \u2018new Iron Curtain\u2019."),
    dict(num=5, tag="CULTURE \u00b7 BBC", kind="gta6", ver="REPORTED",
         head="GTA 6 tops $2.3bn in day one",
         line="Estimates put day-one sales above $2.3bn, a record for entertainment."),
    dict(num=6, tag="EUROPE \u00b7 EU COUNCIL", kind="euaid", ver="CONFIRMED",
         head="EU approves \u20ac1bn arms aid for Ukraine",
         line="Drones, air defence and ammunition, delivered by end of 2027."),
    dict(num=7, tag="EUROPE \u00b7 REUTERS", kind="poland", ver="REPORTED",
         head="Russian missiles breach Polish airspace",
         line="Warsaw says three objects crossed overnight: two missiles and a drone."),
    dict(num=8, tag="UKRAINE \u00b7 UNICEF", kind="unicef", ver="CONFIRMED",
         head="1,144 children killed or hurt in 2026",
         line="UNICEF says the toll is near 2022 levels as Russian strikes intensify."),
    dict(num=9, tag="AMERICAS \u00b7 AL JAZEERA", kind="haiti", ver="REPORTED",
         head="Haiti forces kill 34 in gang raid",
         line="Police say 34 suspected gang members died in the raid."),
    dict(num=10, tag="AFRICA \u00b7 ALLAFRICA", kind="sudan", ver="REPORTED",
         head="Drone strike kills 10 at Sudan gold mine",
         line="Ten die in a drone strike on the Bajoun mining site in South Kordofan."),
    dict(num=11, tag="MIDDLE EAST \u00b7 REUTERS", kind="iraq", ver="CONFIRMED",
         head="Iraq moves on Iran-backed militia base",
         line="Forces deploy in Jurf al-Sakhar as PM orders Kataib Hezbollah out."),
    dict(num=12, tag="TECH \u00b7 SCMP", kind="cyber", ver="CONFIRMED",
         head="White House fires cyber chief after outages",
         line="Sean Cairncross out after air-travel and email chaos; Davies named."),
    dict(num=13, tag="ECONOMY \u00b7 JAPAN TIMES", kind="japan", ver="CONFIRMED",
         head="Japan inflation at year's high",
         line="Core prices peak as subsidies end; a Bank of Japan rate rise stays on track."),
]

NUMBERS = [
    ("-4.8%", "NIKKEI, FRIDAY"),
    ("-2%", "S&P 500, THURSDAY"),
    ("$2.3bn+", "GTA 6 DAY-ONE SALES (EST.)"),
    ("\u20ac1bn", "EU ARMS AID FOR UKRAINE"),
    ("100,000", "YOUTH MOBILITY / YEAR"),
    ("1,144", "UKRAINE CHILD CASUALTIES, 2026"),
]

TIMELINE = [
    ("OVERNIGHT", "Russia's barrage hits Kyiv"),
    ("ASIA MORNING", "Nikkei falls 4.8%"),
    ("MORNING", "Poland reports airspace breach"),
    ("MIDDAY", "EU\u2013UK summit seals reset deal"),
    ("15:50 CET", "EU approves \u20ac1bn arms aid"),
    ("EVENING", "Trump: \u201cvery good talks\u201d with Putin"),
]

# ALSO ON: (region, text) — 22 items, each kept short to fit one line
ALSO_A = [
    ("EUROPE", "UK admits cyber attacks on Russia, China, Iran, N. Korea"),
    ("EUROPE", "EU disburses record \u20ac7.9bn to Ukraine"),
    ("EUROPE", "Georgia declares 22 Nov mourning for Tbilisi blast victims"),
    ("EUROPE", "Youth in 25+ countries strike over living costs, rearmament"),
    ("EUROPE", "UK: four men guilty over woman drugged by her husband"),
    ("ASIA & PACIFIC", "S. Korea ruling party moves to impeach top judge"),
    ("ASIA & PACIFIC", "Mongolia bids farewell to President Kh\u00fcrels\u00fckh"),
    ("ASIA & PACIFIC", "Cyclone Xavier downgraded to category 4 near Cook Islands"),
    ("ASIA & PACIFIC", "Pakistan says 22 militants killed in northwest raids"),
    ("AFRICA", "Dozens missing after migrant boat capsizes off Senegal"),
    ("AFRICA", "Somalia expels UAE ambassador"),
]
ALSO_B = [
    ("AFRICA", "Zimbabwe destroys its 250,000th landmine"),
    ("AFRICA", "Strikes reported near Badme on Ethiopia\u2013Eritrea border"),
    ("MIDDLE EAST", "IEA: Iran war leaves lasting marks on energy; Brent $90.05"),
    ("MIDDLE EAST", "Mosque set on fire in northern Israel"),
    ("MIDDLE EAST", "S. Africa: ICJ Myanmar ruling bolsters its Gaza case"),
    ("AMERICAS", "Thousands protest Colombia's tax plans"),
    ("AMERICAS", "Bukele registers for a third term in El Salvador"),
    ("AMERICAS", "Trump: \u201cvery good talks\u201d with Putin on Ukraine"),
    ("AMERICAS", "El Ni\u00f1o storm threatens Los Angeles with flooding"),
    ("AMERICAS", "Brazil central bank sells $1bn as the real slides"),
    ("GLOBAL", "IMF: global public debt nearing 100% of GDP"),
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
    "NOT YET: EU\u2013UK youth scheme \u2014 in force only if the UK cuts EU student fees in six months",
]

# (number, lon, lat, dx, dy) — pins match the numbered pictured stories
PINS = [
    (1, -74.0, 40.7, 10, -10),
    (2, 30.5, 50.45, 0, 0),
    (3, 4.35, 50.85, 0, 0),
    (4, 24.75, 59.44, 0, 0),
    (5, -3.19, 55.95, 0, 0),
    (6, 4.35, 50.85, 12, -10),
    (7, 21.01, 52.23, 0, 0),
    (8, 30.5, 50.45, -12, 10),
    (9, -72.34, 18.54, 0, 0),
    (10, 30.0, 11.5, 0, 0),
    (11, 44.2, 32.9, 0, 0),
    (12, -77.04, 38.9, -10, 8),
    (13, 139.69, 35.68, 0, 0),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 14
    X0, X1 = M, W - M
    CW = X1 - X0

    f_name = font(SERIF_B, 20)
    f_date = font(SERIF_B, 52)
    f_count = font(SANS_B, 17)
    f_num_fig = font(SANS_B, 21)
    f_num_lab = font(SANS_B, 9)
    f_tl_head = font(SANS_B, 11)
    f_tl_time = font(SANS_B, 10)
    f_tl_txt = font(SANS, 10)
    f_lead_tag = font(SANS_B, 12)
    f_lead_head = font(SERIF_B, 20)
    f_lead_line = font(SANS, 12)
    f_lead_src = font(SANS, 10)
    f_grid_tag = font(SANS_B, 9)
    f_grid_head = font(SANS_B, 12)
    f_grid_line = font(SANS, 10)
    f_sec = font(SANS_B, 13)
    f_also_head = font(SANS_B, 10)
    f_also = font(SANS, 10)
    f_dc_head = font(SANS_B, 11)
    f_dc = font(SANS, 9)
    f_foot = font(SANS, 8)

    # ---- masthead
    d.text((W // 2, 8), "THE WORLD IN ONE PAGE", font=f_name, fill=INK,
           anchor="ma")
    d.text((W // 2, 30), "FRIDAY 20 NOVEMBER 2026", font=f_date, fill=INK,
           anchor="ma")
    d.text((W // 2, 90), "35 STORIES \u00b7 7 REGIONS \u00b7 ALL FROM THIS FRIDAY",
           font=f_count, fill=RED, anchor="ma")
    rule(d, X0, X1, 112, wdt=2)
    rule(d, X0, X1, 116, wdt=1)

    # ---- numbers strip
    y0 = 124
    bw = (CW - 5 * 6) // 6
    for i, (fig, lab) in enumerate(NUMBERS):
        bx = X0 + i * (bw + 6)
        d.rectangle([bx, y0, bx + bw, y0 + 38], outline=(180, 176, 168), width=1)
        d.text((bx + bw // 2, y0 + 3), fig, font=f_num_fig, fill=RED, anchor="ma")
        d.text((bx + bw // 2, y0 + 25), lab, font=f_num_lab, fill=INK, anchor="ma")

    # ---- timeline
    y = 170
    d.text((X0, y), "THE DAY IN TIME", font=f_tl_head, fill=INK)
    d.text((X1, y), "ALL TIMES UTC UNLESS MARKED", font=f_tl_head, fill=GREY,
           anchor="ra")
    ty = 202
    rule(d, X0, X1, ty, fill=(150, 146, 138), wdt=2)
    seg = CW / len(TIMELINE)
    for i, (t, txt) in enumerate(TIMELINE):
        cx = int(X0 + seg * i + seg / 2)
        d.ellipse([cx - 5, ty - 5, cx + 5, ty + 5], fill=RED)
        d.text((cx, ty - 18), t, font=f_tl_time, fill=RED, anchor="ma")
        lines = wrap(txt, f_tl_txt, int(seg - 8))
        yy = ty + 10
        for ln in lines[:2]:
            d.text((cx, yy), ln, font=f_tl_txt, fill=INK, anchor="ma")
            yy += 12

    # ---- leads
    ly = 244
    colw = (CW - 2 * 10) // 3
    for i, s in enumerate(LEADS):
        lx = X0 + i * (colw + 10)
        scene(d, lx, ly, colw, 108, s["kind"])
        ty2 = ly + 114
        d.text((lx, ty2), s["tag"], font=f_lead_tag, fill=RED)
        d.text((lx + colw, ty2), s["ver"], font=f_lead_tag, fill=GREY,
               anchor="ra")
        hy = ty2 + 17
        lines = wrap(s["head"], f_lead_head, colw)
        hy = text_lines(d, lx, hy, lines[:2], f_lead_head, lh=23)
        sy = hy + 3
        slines = wrap(s["text"], f_lead_line, colw)
        sy = text_lines(d, lx, sy, slines[:2], f_lead_line, lh=15)
        d.text((lx, sy + 2), "Source: " + s["src"], font=f_lead_src, fill=GREY)
        if i < 2:
            d.line([(lx + colw + 5, ly), (lx + colw + 5, ly + 222)],
                   fill=LIGHT, width=1)
    rule(d, X0, X1, ly + 228, fill=INK, wdt=1)

    # ---- pictured grid, 2 rows x 5
    gy = 480
    gw = (CW - 4 * 9) // 5
    gh = 112
    for r in range(2):
        for c in range(5):
            s = GRID[r * 5 + c]
            gx = X0 + c * (gw + 9)
            gy2 = gy + r * (gh + 8)
            scene(d, gx, gy2, gw, 44, s["kind"])
            ty3 = gy2 + 47
            d.text((gx, ty3), s["tag"], font=f_grid_tag, fill=RED)
            d.text((gx + gw, ty3), s["ver"], font=f_grid_tag, fill=GREY,
                   anchor="ra")
            hy = ty3 + 12
            lines = wrap(s["head"], f_grid_head, gw)
            hy = text_lines(d, gx, hy, lines[:2], f_grid_head, lh=14)
            ln = wrap(s["line"], f_grid_line, gw)
            text_lines(d, gx, hy + 1, ln[:2], f_grid_line, lh=12)
    rule(d, X0, X1, gy + 2 * gh + 8 + 4, fill=INK, wdt=1)

    # ---- bottom third
    by = 714
    d.text((X0, by), "WHERE IT HAPPENED", font=f_sec, fill=INK)
    d.text((X0 + 358, by), "ALSO ON \u2026", font=f_sec, fill=INK)
    rule(d, X0, X1, by + 18, fill=INK, wdt=1)

    # dotted world map
    mx, my, mw, mh = X0, by + 26, 342, 160
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

    # ALSO ON columns
    ax = X0 + 358
    colw2 = (X1 - ax - 12) // 2

    def also_col(x, items, ytop):
        yy = ytop
        cur_region = None
        for region, txt in items:
            if region != cur_region:
                cur_region = region
                d.text((x, yy), region, font=f_also_head, fill=RED)
                yy += 12
            lines = wrap(txt, f_also, colw2 - 8)
            for ln in lines[:2]:
                d.text((x, yy), ln, font=f_also, fill=INK)
                yy += 11
        return yy

    also_col(ax, ALSO_A, by + 26)
    also_col(ax + colw2 + 12, ALSO_B, by + 26)

    # ---- DATE CHECK box
    dy = 914
    d.rectangle([X0, dy, X1, dy + 94], outline=RED, width=2)
    d.text((X0 + 8, dy + 6),
           "DATE CHECK \u2014 NOT TODAY'S NEWS: THESE BIG STORIES HAPPENED BEFORE FRIDAY",
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

    # ---- footer (one line)
    d.text((W // 2, 1012),
           "Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 BBC \u00b7 Al Jazeera \u00b7 CNBC \u00b7 EU Council \u00b7 UNICEF \u00b7 SCMP \u00b7 France 24 \u00b7 AllAfrica \u00b7 RNZ \u00b7 Montsame \u00b7 Ukrinform \u2014 every event happened, or was first reported, on Friday 20 November 2026.",
           font=f_foot, fill=GREY, anchor="ma")

    img.save(OUT, "PNG")
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
