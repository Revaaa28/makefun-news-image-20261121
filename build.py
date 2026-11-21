#!/usr/bin/env python3
"""Build script for the news-image-20261121 entry.

Renders entry.png (1024x1024) with Pillow. This script is a local build
tool only -- the grader runs main.py, which ships the rendered PNG.
Written fresh for the 21 November 2026 edition.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 36
CW = W - 2 * MARGIN  # content width = 952

CREAM = (246, 241, 229)
PANEL = (238, 231, 214)
INK = (22, 22, 22)
RED = (176, 35, 24)
NAVY = (31, 58, 95)
GREY = (90, 83, 72)
RULE = (22, 22, 22)
DOT = (140, 152, 175)
GOLD = (217, 154, 43)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


def F_SANS(size):
    return font("DejaVuSans.ttf", size)


def F_BOLD(size):
    return font("DejaVuSans-Bold.ttf", size)


def F_SERIF(size):
    return font("DejaVuSerif.ttf", size)


def F_SERIF_B(size):
    return font("DejaVuSerif-Bold.ttf", size)


def text_w(d, s, f):
    return d.textlength(s, font=f)


def wrap(d, s, f, maxw):
    """Greedy word wrap; returns list of lines."""
    words = s.split()
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if text_w(d, trial, f) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, lines, x, y, f, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


# ----------------------------------------------------------------------------
# Dotted world map. Hand-authored landmask: 19 rows x 136 cols, '#' = land.
# Columns run lon -180..+180, rows run lat ~78N..~-57S.
# ----------------------------------------------------------------------------
LANDMASK = [
    "                                                                                                                                        ",
    "        ####   ##############                                                                                                           ",
    "       ###### #################################            ##  ########                                                                 ",
    "        ####  ###############################  ##           #################  ###############################################          ",
    "              #############################                 ################ ##################################################       ",
    "               ##########################                    ##############  #################################################          ",
    "                ########################                      ########    #############################################             ",
    "                 #####################                         ######      ##########################################               ",
    "                  ##################                            ####        ################  ##################                    ",
    "                   ################                              ##          ##############      ################                       ",
    "                    #############                                                            ##########    ##########                     ",
    "                     ##########                                                              ########      ########                       ",
    "                      ########                                                                ######                                    ",
    "                      ########                                                                 ####            ##########               ",
    "                      #######                                                                                  ############             ",
    "                      ######                                                                                    ########              ",
    "                       #####                                                                                      ######                ",
    "                       ####                                                                                                            ",
    "                        ##                                                                                                             ",
]

# pin positions: (lon, lat, story number)
PINS = [
    (19.0, 52.0, 1),      # Poland
    (114.1, 22.5, 2),     # Shenzhen
    (-74.0, 40.7, 3),     # New York
    (28.0, 13.0, 4),      # West Kordofan, Sudan
    (101.7, 3.1, 5),      # Kuala Lumpur
    (174.8, -41.3, 6),    # Wellington
]


def draw_map(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=PANEL, outline=RULE, width=2)
    rows = len(LANDMASK)
    cols = max(len(r) for r in LANDMASK)
    cell_w = w / cols
    cell_h = h / rows
    r = max(1.6, min(cell_w, cell_h) * 0.34)
    for ri, row in enumerate(LANDMASK):
        for ci, ch in enumerate(row):
            if ch == "#":
                cx = x0 + (ci + 0.5) * cell_w
                cy = y0 + (ri + 0.5) * cell_h
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=DOT)
    # pins on top
    for lon, lat, num in PINS:
        px = x0 + (lon + 180.0) / 360.0 * w
        py = y0 + (78.0 - lat) / 140.0 * h
        pr = 12
        d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=RED, outline=(255, 255, 255), width=2)
        label = str(num)
        f = F_BOLD(15)
        tw = text_w(d, label, f)
        d.text((px - tw / 2, py - 9), label, font=f, fill=(255, 255, 255))


# ----------------------------------------------------------------------------
# Vignettes. Each returns a PIL Image of exactly (w, h). Flat shapes only,
# no text inside any vignette.
# ----------------------------------------------------------------------------
def _img(w, h, color):
    return Image.new("RGB", (w, h), color)


def vig_poland(w, h):
    """Missiles descending on a village skyline; burst stars at impact."""
    im = _img(w, h, (46, 74, 107))
    d = ImageDraw.Draw(im)
    ground_y = int(h * 0.78)
    d.rectangle([0, ground_y, w, h], fill=(96, 110, 78))
    # houses along the horizon
    houses = [(0.04, 0.30), (0.20, 0.22), (0.38, 0.34), (0.60, 0.24), (0.80, 0.30)]
    for fx, fw in houses:
        hx = int(w * fx)
        hw = int(w * fw * 0.55)
        hh = int(h * 0.16)
        hy = ground_y - hh
        d.rectangle([hx, hy, hx + hw, ground_y], fill=(214, 203, 178))
        d.polygon([(hx - 4, hy), (hx + hw // 2, hy - int(h * 0.10)), (hx + hw + 4, hy)], fill=(120, 52, 40))
        d.rectangle([hx + hw // 2 - 4, ground_y - 14, hx + hw // 2 + 4, ground_y], fill=(70, 52, 40))
    # missiles: two diagonal bodies with smoke trails
    for (sx, sy, ex, ey) in [(0.30, 0.02, 0.52, 0.52), (0.62, 0.0, 0.80, 0.46)]:
        x1, y1, x2, y2 = int(w * sx), int(h * sy), int(w * ex), int(h * ey)
        # smoke trail: soft circles stepping back along the path
        for t in [i / 9 for i in range(1, 10)]:
            cx = x2 + (x1 - x2) * t
            cy = y2 + (y1 - y2) * t
            rr = 3 + t * 7
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(168, 175, 182))
        # body: elongated diamond pointing down-right
        import math
        ang = math.atan2(y2 - y1, x2 - x1)
        L, B = 44, 7
        px_, py_ = math.cos(ang), math.sin(ang)
        qx, qy = -py_, px_
        tip = (x2, y2)
        tail = (x2 - px_ * L, y2 - py_ * L)
        left = (tail[0] + qx * B, tail[1] + qy * B)
        right = (tail[0] - qx * B, tail[1] - qy * B)
        d.polygon([tip, left, tail, right], fill=(226, 228, 230))
        d.polygon([tip, (tip[0] - px_ * 12 + qx * 4.5, tip[1] - py_ * 12 + qy * 4.5),
                   (tip[0] - px_ * 12 - qx * 4.5, tip[1] - py_ * 12 - qy * 4.5)], fill=RED)
        # fins
        d.polygon([tail, (tail[0] - px_ * 10 + qx * 13, tail[1] - py_ * 10 + qy * 13),
                   (tail[0] + qx * 5, tail[1] + qy * 5)], fill=(150, 40, 32))
        d.polygon([tail, (tail[0] - px_ * 10 - qx * 13, tail[1] - py_ * 10 - qy * 13),
                   (tail[0] - qx * 5, tail[1] - qy * 5)], fill=(150, 40, 32))
    # burst stars at impact points
    import math
    for fx, fy, R in [(0.55, 0.72, 20), (0.83, 0.70, 15)]:
        cx, cy = int(w * fx), int(h * fy)
        pts = []
        for i in range(16):
            ang = i * math.pi / 8
            rr = R if i % 2 == 0 else R * 0.42
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        d.polygon(pts, fill=GOLD)
        pts2 = [(cx + (p[0] - cx) * 0.55, cy + (p[1] - cy) * 0.55) for p in pts]
        d.polygon(pts2, fill=(240, 120, 40))
    return im


def vig_shenzhen(w, h):
    """Skyline, three flags, and a summit table with three figures."""
    im = _img(w, h, (206, 220, 232))
    d = ImageDraw.Draw(im)
    # skyline silhouette
    base = int(h * 0.62)
    towers = [(0.0, 0.30), (0.10, 0.44), (0.22, 0.24), (0.33, 0.52), (0.47, 0.34),
              (0.60, 0.46), (0.73, 0.28), (0.84, 0.40), (0.94, 0.30)]
    for fx, fh in towers:
        tw_ = int(w * 0.09)
        tx = int(w * fx)
        d.rectangle([tx, base - int(h * fh), tx + tw_, base], fill=NAVY)
    d.rectangle([0, base, w, h], fill=(58, 84, 66))
    # flags on poles above a long table
    table_y = int(h * 0.84)
    flag_cols = [(0.20, (58, 92, 160)), (0.50, (196, 40, 34)), (0.80, (232, 232, 232))]
    for fx, col in flag_cols:
        cx = int(w * fx)
        d.line([cx, table_y - int(h * 0.42), cx, table_y], fill=(40, 40, 40), width=3)
        fw_, fh_ = int(w * 0.16), int(h * 0.20)
        d.rectangle([cx, table_y - int(h * 0.42), cx + fw_, table_y - int(h * 0.42) + fh_], fill=col)
    # table + three seated figures
    d.polygon([(w * 0.08, table_y), (w * 0.92, table_y), (w * 0.86, h * 0.99), (w * 0.14, h * 0.99)], fill=(110, 74, 44))
    for fx in (0.26, 0.50, 0.74):
        cx = int(w * fx)
        hy = table_y - int(h * 0.15)
        d.ellipse([cx - 12, hy - 12, cx + 12, hy + 12], fill=(52, 42, 36))
        d.polygon([(cx - 21, table_y), (cx + 21, table_y), (cx + 13, hy + 8), (cx - 13, hy + 8)], fill=(38, 44, 58))
    return im


def vig_wallst(w, h):
    """Night skyline with a plunging red market line."""
    im = _img(w, h, (18, 26, 44))
    d = ImageDraw.Draw(im)
    # building silhouettes with a few lit windows
    towers = [(0.0, 0.55, 0.16), (0.14, 0.78, 0.15), (0.30, 0.42, 0.13), (0.44, 0.66, 0.16),
              (0.60, 0.50, 0.14), (0.74, 0.84, 0.13), (0.88, 0.58, 0.12)]
    for fx, fh, fw in towers:
        x0 = int(w * fx)
        x1 = x0 + int(w * fw)
        y0 = int(h * (1 - fh))
        d.rectangle([x0, y0, x1, h], fill=(36, 50, 78))
        for wy in range(y0 + 8, h - 8, 15):
            for wx in range(x0 + 6, x1 - 6, 13):
                if (wx * 7 + wy * 13) % 5 == 0:
                    d.rectangle([wx, wy, wx + 4, wy + 6], fill=(250, 214, 110))
    # plunging chart line
    pts = [(w * 0.03, h * 0.14), (w * 0.24, h * 0.20), (w * 0.42, h * 0.16),
           (w * 0.58, h * 0.38), (w * 0.72, h * 0.34), (w * 0.97, h * 0.80)]
    d.line(pts, fill=RED, width=max(4, h // 22), joint="curve")
    # arrowhead at the end
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - w * 0.075, ey - h * 0.015), (ex - w * 0.02, ey - h * 0.10)], fill=RED)
    return im


def vig_sudan(w, h):
    """Desert scene: sun, dunes, acacia, a small convoy, distant smoke."""
    im = _img(w, h, (238, 205, 138))
    d = ImageDraw.Draw(im)
    d.ellipse([w * 0.80, h * 0.05, w * 0.92, h * 0.34], fill=(246, 166, 50))
    # distant smoke column
    for i in range(5):
        cx = w * 0.13 + i * 2
        cy = h * (0.42 - i * 0.07)
        rr = 4 + i * 2.5
        d.ellipse([cx - rr, cy - rr * 0.7, cx + rr, cy + rr * 0.7], fill=(172, 160, 144))
    # dunes
    d.polygon([(0, h * 0.66), (w * 0.35, h * 0.52), (w * 0.72, h * 0.68), (w, h * 0.58), (w, h), (0, h)], fill=(222, 178, 100))
    d.polygon([(0, h * 0.82), (w * 0.45, h * 0.68), (w, h * 0.84), (w, h), (0, h)], fill=(203, 156, 80))
    # acacia tree
    tx, ty = int(w * 0.66), int(h * 0.66)
    d.line([tx, ty, tx - 6, ty - int(h * 0.22)], fill=(92, 66, 40), width=5)
    d.line([tx - 4, ty - int(h * 0.12), tx - int(w * 0.07), ty - int(h * 0.24)], fill=(92, 66, 40), width=4)
    d.line([tx - 4, ty - int(h * 0.12), tx + int(w * 0.06), ty - int(h * 0.25)], fill=(92, 66, 40), width=4)
    d.ellipse([tx - int(w * 0.13), ty - int(h * 0.33), tx + int(w * 0.12), ty - int(h * 0.21)], fill=(86, 110, 52))
    # convoy: three small vehicles
    for i, fx in enumerate((0.24, 0.36, 0.48)):
        vx, vy = int(w * fx), int(h * (0.86 + (i % 2) * 0.02))
        vw_, vh_ = int(w * 0.085), int(h * 0.10)
        d.rectangle([vx, vy - vh_, vx + vw_, vy], fill=(70, 74, 66))
        d.rectangle([vx + vw_ - 12, vy - vh_ - 7, vx + vw_ - 2, vy - vh_], fill=(70, 74, 66))
        d.ellipse([vx + 4, vy - 5, vx + 13, vy + 4], fill=(30, 30, 30))
        d.ellipse([vx + vw_ - 13, vy - 5, vx + vw_ - 4, vy + 4], fill=(30, 30, 30))
    return im


def vig_boat(w, h):
    """A boat of passengers crossing toward a palm-lined shore."""
    im = _img(w, h, (198, 224, 233))
    d = ImageDraw.Draw(im)
    d.ellipse([w * 0.05, h * 0.06, w * 0.16, h * 0.30], fill=(245, 205, 90))
    sea_y = int(h * 0.52)
    d.rectangle([0, sea_y, w, h], fill=(43, 102, 134))
    # distant shore with palms
    d.polygon([(w * 0.70, sea_y), (w, sea_y - int(h * 0.06)), (w, sea_y + 4), (w * 0.70, sea_y + 4)], fill=(84, 116, 70))
    for fx in (0.82, 0.93):
        px_, py_ = int(w * fx), sea_y - int(h * 0.05)
        d.line([px_, py_, px_ + 3, py_ - int(h * 0.20)], fill=(96, 72, 44), width=4)
        for ang in (-0.9, -0.45, 0.0, 0.45, 0.9):
            import math
            ex = px_ + 3 + int(w * 0.07 * math.cos(ang - 1.57))
            ey = py_ - int(h * 0.20) + int(h * 0.10 * math.sin(ang - 1.57)) + 6
            d.line([px_ + 3, py_ - int(h * 0.20), ex, ey], fill=(60, 110, 56), width=3)
    # boat hull + passengers
    bx, by = int(w * 0.16), int(h * 0.66)
    bw_, bh_ = int(w * 0.46), int(h * 0.16)
    d.polygon([(bx, by), (bx + bw_, by), (bx + bw_ - int(w * 0.07), by + bh_), (bx + int(w * 0.05), by + bh_)], fill=(122, 80, 46))
    d.rectangle([bx - 2, by - 5, bx + bw_ + 2, by + 2], fill=(94, 60, 34))
    for i in range(5):
        cx = bx + int(bw_ * (0.14 + i * 0.18))
        d.ellipse([cx - 8, by - 30, cx + 8, by - 14], fill=(52, 42, 36))
        d.polygon([(cx - 11, by - 4), (cx + 11, by - 4), (cx + 7, by - 16), (cx - 7, by - 16)], fill=(70, 84, 110) if i % 2 else (140, 70, 54))
    # gentle wave strokes
    for i, (fx, fy) in enumerate([(0.08, 0.86), (0.30, 0.92), (0.55, 0.87), (0.78, 0.93), (0.90, 0.84)]):
        x0, y0 = int(w * fx), int(h * fy)
        d.arc([x0, y0, x0 + 34, y0 + 12], start=180, end=360, fill=(170, 205, 222), width=3)
    return im


def vig_cricket(w, h):
    """Cricket: pitch strip, stumps, batsman pictogram, red ball."""
    im = _img(w, h, (74, 138, 66))
    d = ImageDraw.Draw(im)
    # outfield shading bands
    for i in range(6):
        if i % 2 == 0:
            d.rectangle([0, int(h * i / 6), w, int(h * (i + 1) / 6)], fill=(80, 146, 70))
    # pitch
    px0, px1 = int(w * 0.40), int(w * 0.60)
    d.rectangle([px0, int(h * 0.06), px1, int(h * 0.96)], fill=(216, 196, 150))
    # stumps at the far end
    sx = int(w * 0.50)
    for k in (-1, 0, 1):
        d.line([sx + k * 7, int(h * 0.10), sx + k * 7, int(h * 0.24)], fill=(240, 220, 130), width=3)
    d.line([sx - 8, int(h * 0.10), sx + 8, int(h * 0.10)], fill=(240, 220, 130), width=3)
    # batsman pictogram (blocky, side-on, mid swing)
    hx, hy = int(w * 0.47), int(h * 0.52)   # hip point
    d.ellipse([hx - 10, hy - 64, hx + 10, hy - 44], fill=(30, 34, 44))            # head/helmet
    d.line([hx, hy - 44, hx + 4, hy], fill=(30, 34, 44), width=11)                # torso
    d.line([hx + 4, hy, hx - 14, hy + 34], fill=(30, 34, 44), width=9)            # front leg
    d.line([hx + 4, hy, hx + 20, hy + 30], fill=(30, 34, 44), width=9)            # back leg
    d.line([hx + 2, hy - 38, hx + 26, hy - 22], fill=(30, 34, 44), width=8)       # arms to bat
    d.line([hx + 26, hy - 22, hx + 44, hy + 8], fill=(196, 164, 104), width=7)    # bat
    # pads hint
    d.line([hx - 14, hy + 34, hx - 16, hy + 44], fill=(238, 238, 238), width=9)
    d.line([hx + 20, hy + 30, hx + 24, hy + 40], fill=(238, 238, 238), width=9)
    # ball with motion dashes
    bx, by = int(w * 0.80), int(h * 0.30)
    for i in range(3):
        d.line([bx - 34 - i * 16, by + 10 + i * 7, bx - 16 - i * 16, by + 10 + i * 7], fill=(220, 230, 220), width=3)
    d.ellipse([bx - 10, by - 10, bx + 10, by + 10], fill=(178, 34, 30))
    d.arc([bx - 6, by - 8, bx + 6, by + 8], start=300, end=120, fill=(240, 220, 210), width=2)
    return im


# ----------------------------------------------------------------------------
# Page assembly
# ----------------------------------------------------------------------------
def centered(d, s, f, y, fill):
    d.text(((W - text_w(d, s, f)) / 2, y), s, font=f, fill=fill)


def story_text(d, x, y, w, label, headline, summary,
               label_size=21, head_size=30, sum_size=20,
               head_leading=35, sum_leading=24, head_lines=2):
    f_label = F_BOLD(label_size)
    d.text((x, y), label, font=f_label, fill=RED)
    y += label_size + 6
    f_head = F_BOLD(head_size)
    for ln in wrap(d, headline, f_head, w)[:head_lines]:
        d.text((x, y), ln, font=f_head, fill=INK)
        y += head_leading
    y += 3
    f_sum = F_SANS(sum_size)
    for ln in wrap(d, summary, f_sum, w):
        d.text((x, y), ln, font=f_sum, fill=INK)
        y += sum_leading
    return y


def main():
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)

    # ---- masthead ----
    centered(d, "THE WORLD IN ONE DAY", F_BOLD(25), 24, RED)
    centered(d, "SATURDAY, 21 NOVEMBER 2026", F_SERIF_B(54), 54, INK)
    centered(d, "Six stories that sum up the day — from Warsaw to Shenzhen to Wellington",
             F_SERIF(20), 120, GREY)
    d.line([MARGIN, 148, W - MARGIN, 148], fill=RULE, width=3)
    d.line([MARGIN, 154, W - MARGIN, 154], fill=RULE, width=1)

    # ---- dotted world map ----
    draw_map(d, MARGIN, 166, CW, 112)

    # ---- hero: story 1, Poland ----
    hero_y = 292
    im.paste(vig_poland(412, 220), (MARGIN, hero_y))
    hx = MARGIN + 412 + 24
    hw = W - MARGIN - hx
    d.text((hx, hero_y + 2), "1 — WARSAW, POLAND", font=F_BOLD(22), fill=RED)
    f_hh = F_BOLD(47)
    yy = hero_y + 34
    for ln in wrap(d, "RUSSIAN MISSILES FALL IN POLAND", f_hh, hw):
        d.text((hx, yy), ln, font=f_hh, fill=INK)
        yy += 54
    yy += 6
    f_hs = F_SANS(23)
    for ln in wrap(d, "Poland says two Russian missiles and a drone came down on its "
                      "territory. NATO calls it a grave violation of allied airspace.",
                   f_hs, hw):
        d.text((hx, yy), ln, font=f_hs, fill=INK)
        yy += 29

    d.line([MARGIN, 540, W - MARGIN, 540], fill=RULE, width=1)

    # ---- row 2: stories 2 and 3 ----
    r2_y = 554
    col_w = 458
    col2_x = MARGIN + col_w + 36
    im.paste(vig_shenzhen(col_w, 92), (MARGIN, r2_y))
    story_text(d, MARGIN, r2_y + 100, col_w,
               "2 — SHENZHEN, CHINA",
               "TRUMP, XI, PUTIN END FIRST SUMMIT",
               "They closed with a four-point declaration; analysts say symbolism beat substance.")
    im.paste(vig_wallst(col_w, 92), (col2_x, r2_y))
    story_text(d, col2_x, r2_y + 100, col_w,
               "3 — NEW YORK, USA",
               "AI SELL-OFF TIPS WALL ST INTO CORRECTION",
               "The S&P 500 fell 3.7% on Friday as chip shares plunged; Tokyo's Nikkei lost 5.1%.")

    d.line([MARGIN, 806, W - MARGIN, 806], fill=RULE, width=1)

    # ---- row 3: stories 4, 5, 6 (vignette left, label+headline right, summary below) ----
    r3_y = 820
    c3_w = 301
    cards = [
        (vig_sudan(88, 88), "4 — WEST KORDOFAN", "ARMY SAYS RSF BASES BROKEN",
         "Sudan's army says it dismantled RSF strongholds in 10 areas."),
        (vig_boat(88, 88), "5 — KUALA LUMPUR", "10,000 ROHINGYA FOR TÜRKIYE",
         "Malaysia's deal follows the World Court's genocide ruling."),
        (vig_cricket(88, 88), "6 — WELLINGTON", "RECORD OPENING STAND",
         "Jaiswal and Rahul post a record stand for India in NZ."),
    ]
    for i, (vig, label, headline, summary) in enumerate(cards):
        cx = MARGIN + i * (c3_w + 24)
        im.paste(vig, (cx, r3_y))
        tx = cx + 88 + 10
        tw = cx + c3_w - tx
        d.text((tx, r3_y), label, font=F_BOLD(17), fill=RED)
        f3 = F_BOLD(22)
        yy = r3_y + 24
        for ln in wrap(d, headline, f3, tw)[:3]:
            d.text((tx, yy), ln, font=f3, fill=INK)
            yy += 26
        f3s = F_SANS(18)
        yy = r3_y + 108
        for ln in wrap(d, summary, f3s, c3_w)[:2]:
            d.text((cx, yy), ln, font=f3s, fill=INK)
            yy += 23

    # ---- ALSO TODAY ticker ----
    d.rectangle([0, 980, W, H], fill=(18, 18, 18))
    items = "EU adds €1bn Ukraine aid   ·   Nigeria barge: search for survivors   ·   Cancer pill breakthrough hailed"
    f_label = F_BOLD(18)
    label_w = text_w(d, "ALSO TODAY   ", f_label)
    size = 16
    while size > 11 and label_w + text_w(d, items, F_BOLD(size)) > W - 16:
        size -= 1
    f_tick = F_BOLD(size)
    total = label_w + text_w(d, items, f_tick)
    x = (W - total) / 2
    d.text((x, 992), "ALSO TODAY", font=f_label, fill=GOLD)
    d.text((x + label_w, 993), items, font=f_tick, fill=(240, 238, 230))

    im.save("entry.png", optimize=True)
    print("saved entry.png", im.size)


if __name__ == "__main__":
    main()
