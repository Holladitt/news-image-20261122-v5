#!/usr/bin/env python3
"""v5 generator — broadsheet 'THE WORLD IN ONE DAY', Sunday 22 November 2026.
Draws the newspaper with PIL (DejaVu + Liberation fonts) and writes entry.png.
Deterministic: fixed seed, no network, no timestamps in the output bytes.
Run from the repo directory: python3 gen.py  (writes ./entry.png next to itself)
"""
import os, random, textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER  = (246, 241, 227)
PAPER2 = (238, 230, 210)
INK    = (20, 20, 18)
NAVY   = (22, 38, 76)
NAVY2  = (46, 74, 122)
RED    = (166, 25, 46)
GOLD   = (178, 132, 30)
GRAY   = (105, 105, 100)
HAIR   = (198, 188, 162)
SEA    = (216, 226, 232)
LAND   = (122, 139, 168)
WHITE  = (255, 255, 255)
CREAM2 = (250, 246, 236)

FD = "/usr/share/fonts/truetype/dejavu"
FL = "/usr/share/fonts/truetype/liberation"

def F(path, size):
    return ImageFont.truetype(path, size)

SERIF_B  = lambda s: F(f"{FD}/DejaVuSerif-Bold.ttf", s)
SERIF    = lambda s: F(f"{FD}/DejaVuSerif.ttf", s)
SERIF_IT = lambda s: F(f"{FL}/LiberationSerif-BoldItalic.ttf", s)
SANS_B   = lambda s: F(f"{FD}/DejaVuSans-Bold.ttf", s)
SANS     = lambda s: F(f"{FD}/DejaVuSans.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def text_w(txt, font):
    return d.textlength(txt, font=font)

def wrap(txt, font, width):
    """Greedy wrap by measured width."""
    lines, cur = [], ""
    for word in txt.split(" "):
        trial = (cur + " " + word).strip()
        if text_w(trial, font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def para(x, y, txt, font, width, fill=INK, leading=None, align="left"):
    """Draw wrapped paragraph; return y just below last line."""
    lh = leading or int(font.size * 1.28)
    for ln in wrap(txt, font, width):
        if align == "center":
            d.text((x + width / 2, y), ln, font=font, fill=fill, anchor="ma")
        else:
            d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y

def hline(x0, x1, y, fill=INK, wdt=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=wdt)

def tag_pill(x, y, label, fill):
    """Small filled tag; returns width used."""
    f = SANS_B(10)
    tw = int(text_w(label, f)) + 10
    d.rounded_rectangle([x, y, x + tw, y + 14], radius=3, fill=fill)
    d.text((x + 5, y + 2), label, font=f, fill=WHITE)
    return tw

TAG_FILL = {"CONFIRMED": NAVY, "REPORTED": (90, 110, 140), "CLAIM": RED,
            "ONGOING": GOLD, "PENDING": GRAY}

def rule_double(y, x0=24, x1=1000):
    hline(x0, x1, y, fill=INK, wdt=2)
    hline(x0, x1, y + 4, fill=INK, wdt=1)

# ---------------------------------------------------------------- paper grain
random.seed(20261122)
grain = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(grain)
for _ in range(14000):
    gx, gy = random.randint(0, W - 1), random.randint(0, H - 1)
    a = random.randint(6, 20)
    col = (120, 100, 60, a) if random.random() < 0.6 else (255, 255, 255, a)
    gd.point((gx, gy), fill=col)
for _ in range(260):
    gx, gy = random.randint(0, W - 1), random.randint(0, H - 1)
    ln = random.randint(6, 26)
    gd.line([(gx, gy), (gx + ln, gy + 1)], fill=(150, 130, 90, 14), width=1)

# ---------------------------------------------------------------- frame
d.rectangle([8, 8, W - 9, H - 9], outline=INK, width=2)
d.rectangle([13, 13, W - 14, H - 14], outline=HAIR, width=1)

# ---------------------------------------------------------------- masthead
y = 26
name = "THE WORLD IN ONE DAY"
nf = SERIF_B(60)
nw = text_w(name, nf)
d.text(((W - nw) / 2, y), name, font=nf, fill=NAVY)
y += 66
rule_double(y)
y += 12
df = SANS_B(19)
ds = "SUNDAY  22  NOVEMBER  2026"
d.text(((W - text_w(ds, df)) / 2, y), ds, font=df, fill=RED)
y += 26
sf = SANS(12)
ss = "35 STORIES  ·  7 REGIONS  ·  EVERY ONE DATED TODAY  ·  ANTALYA — MANAMA — KYIV — WELLINGTON"
d.text(((W - text_w(ss, sf)) / 2, y), ss, font=sf, fill=GRAY)
y += 22
rule_double(y)
y += 10
sub = "COP31 ends without a pact  ·  Iran claims a radar hit in Bahrain  ·  186 drones over Ukraine"
suf = SERIF_IT(17)
d.text(((W - text_w(sub, suf)) / 2, y), sub, font=suf, fill=RED)

# ---------------------------------------------------------------- giant headline
y = 184
hf = SERIF_B(38)
hl = "CLIMATE TALKS END WITHOUT A PACT"
d.text(((W - text_w(hl, hf)) / 2, y), hl, font=hf, fill=INK)
y += 46
dk = "Final text lands at dawn in Antalya — and is rejected the same day over its silence on fossil fuels."
dkf = SERIF(15)
d.text(((W - text_w(dk, dkf)) / 2, y), dk, font=dkf, fill=INK)
y += 24
hline(24, 1000, y, fill=HAIR, wdt=1)

# ---------------------------------------------------------------- leads
LEAD_Y = 258
LEAD_H = 178
COLW = 320
COLX = [24, 352, 680]

def lead_frame(x):
    d.rectangle([x, LEAD_Y, x + COLW, LEAD_Y + LEAD_H], outline=HAIR, width=1)
    d.rectangle([x + 1, LEAD_Y + 1, x + COLW - 1, LEAD_Y + 1 + 96], fill=PAPER2)

def illo_cop31(x, y, w, h):
    # dawn sky bands, rising sun, sea, flags, podium
    bands = [(250, 214, 150), (240, 178, 110), (228, 138, 88), (214, 110, 84)]
    bh = h // 4
    for i, c in enumerate(bands):
        d.rectangle([x, y + i * bh, x + w, y + (i + 1) * bh], fill=c)
    cx, cy, r = x + w // 2, y + h - 40, 26
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 236, 170), outline=RED, width=2)
    d.rectangle([x, y + h - 22, x + w, y + h], fill=NAVY)
    for fx in (x + 34, x + w - 52):
        d.line([(fx, y + 18), (fx, y + h - 22)], fill=INK, width=2)
        d.polygon([(fx, y + 18), (fx + 26, y + 25), (fx, y + 32)], fill=RED)
    d.rectangle([cx - 34, y + h - 40, cx + 34, y + h - 22], fill=INK)
    d.rectangle([cx - 22, y + h - 52, cx + 22, y + h - 40], fill=WHITE, outline=INK)

def illo_bahrain(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 34, 64))
    for sx in range(0, w, 26):
        for sy in range(0, h, 30):
            if (sx * 7 + sy * 13) % 41 < 9:
                d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(200, 210, 230))
    bx, by = x + 60, y + h - 26
    d.line([(bx, by), (bx, by - 40)], fill=(220, 225, 235), width=4)
    d.polygon([(bx - 32, by - 66), (bx - 2, by - 76), (bx + 30, by - 58),
               (bx + 4, by - 44)], fill=(240, 242, 245), outline=(200, 210, 225))
    d.line([(bx, by - 46), (bx + 40, by - 78)], fill=GOLD, width=2)
    for mx, my, s in ((x + 190, y + 22, 1), (x + 235, y + 44, -1)):
        d.arc([mx - 42, my - 26, mx + 42, my + 34], start=200 if s > 0 else 320,
              end=340 if s > 0 else 40, fill=RED, width=3)
        d.ellipse([mx - 3, my - 3, mx + 3, my + 3], fill=RED)
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(16, 24, 48))
    for hx in (x + 150, x + 205, x + 260):
        d.rectangle([hx, y + h - 34, hx + 34, y + h - 12], fill=(70, 84, 120))
        d.rectangle([hx + 6, y + h - 40, hx + 28, y + h - 34], fill=(120, 135, 165))

def illo_ukraine(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 28, 58))
    for sx in range(0, w, 22):
        for sy in range(0, h, 26):
            if (sx * 5 + sy * 11) % 37 < 8:
                d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(210, 220, 240))
    d.ellipse([x + w - 58, y + 10, x + w - 26, y + 42], fill=(235, 230, 205))
    d.ellipse([x + w - 50, y + 14, x + w - 26, y + 42], fill=(18, 28, 58))
    def drone(dx, dy, s):
        d.ellipse([dx - 6 * s, dy - 2, dx + 6 * s, dy + 2], fill=(205, 210, 220))
        d.line([(dx - 13 * s, dy - 6), (dx + 13 * s, dy - 6)], fill=(225, 228, 235), width=2)
        d.line([(dx - 13 * s, dy + 6), (dx + 13 * s, dy + 6)], fill=(225, 228, 235), width=2)
        d.ellipse([dx - 2, dy - 2, dx + 2, dy + 2], fill=RED)
    drone(x + 70, y + 34, 1)
    drone(x + 150, y + 58, 1)
    drone(x + 235, y + 26, 1)
    for ax in (x + 90, x + 190):
        d.arc([ax - 46, y + 30, ax + 46, y + 110], start=180, end=360, fill=GOLD, width=3)
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(10, 16, 34))
    d.polygon([(x + 40, y + h - 14), (x + 52, y + h - 34), (x + 64, y + h - 14)], fill=(60, 70, 100))
    d.polygon([(x + 250, y + h - 14), (x + 262, y + h - 30), (x + 274, y + h - 14)], fill=(60, 70, 100))

LEADS = [
    dict(kick="1 · ANTALYA — CLIMATE", tag="CONFIRMED",
         body=("Final text lands at dawn, is rejected over fossil-fuel silence. "
               "Side deals on adaptation survive."),
         src="Sources: UN News · Reuters · AP"),
    dict(kick="2 · MANAMA — MIDDLE EAST", tag="CLAIM",
         head="IRAN CLAIMS RADAR HIT",
         body=("IRGC says it hit two US Patriot radars. Bahrain says a civilian "
               "plant was hit; two hurt. US: no damage."),
         src="Sources: AFP · Reuters · Al Jazeera"),
    dict(kick="3 · KYIV — EUROPE", tag="CONFIRMED",
         head="186 DRONES, 161 DOWN",
         body=("Overnight raid — 72 jet-powered — met by defences; strikes at 18 "
               "sites. A home hit near Kyiv; two hurt."),
         src="Source: Ukrainian Air Force"),
]
ILLOS = [illo_cop31, illo_bahrain, illo_ukraine]

for i, lead in enumerate(LEADS):
    x = COLX[i]
    lead_frame(x)
    ILLOS[i](x + 1, LEAD_Y + 1, COLW - 2, 96)
    ty = LEAD_Y + 102
    d.text((x + 8, ty), lead["kick"], font=SANS_B(10), fill=NAVY)
    tag_pill(x + COLW - 78, ty - 1, lead["tag"], TAG_FILL[lead["tag"]])
    if "head" in lead:
        d.text((x + 8, ty + 16), lead["head"], font=SERIF_B(15), fill=INK)
        by = ty + 34
    else:
        by = ty + 16
    para(x + 8, by, lead["body"], SERIF(11), COLW - 16, fill=INK, leading=14)
    d.text((x + 8, LEAD_Y + LEAD_H - 12), lead["src"], font=SANS(8), fill=GRAY)

# ---------------------------------------------------------------- timeline
TY = 442
d.rectangle([24, TY, 1000, TY + 38], fill=NAVY)
d.text((34, TY + 11), "THE DAY IN UTC", font=SANS_B(12), fill=WHITE)
TL = [("01:00", "Hong Kong polls open"),
      ("05:11", "Hamas seeks talks"),
      ("05:30", "Verstappen wins"),
      ("06:00", "161 of 186 down"),
      ("12:00", "COP31: no pact"),
      ("17:13", "Tankers hit mines")]
tx = 168
tw = (1000 - 168 - 10) / 6
for tm, ev in TL:
    d.text((tx, TY + 5), tm, font=SANS_B(11), fill=GOLD)
    para(tx, TY + 19, ev, SANS(10), tw - 8, fill=WHITE, leading=12)
    tx += tw

# ---------------------------------------------------------------- numbers
NY = 484
d.text((24, NY), "THE DAY IN NUMBERS", font=SANS_B(12), fill=NAVY)
hline(24, 1000, NY + 17, fill=NAVY, wdt=2)
NUMS = [("186", "drones launched at Ukraine"),
        ("161", "shot down or suppressed"),
        ("720/9", "India's Test total, Wellington"),
        ("856", "candidates in Hong Kong polls"),
        ("98.79%", "Hong Kong turnout"),
        ("35%", "electricity share eyed by 2035")]
nx = 24
nw = 976 / 6
for val, cap in NUMS:
    d.text((nx + nw / 2, NY + 24), val, font=SERIF_B(26), fill=RED, anchor="ma")
    para(nx + 6, NY + 56, cap, SANS(9), nw - 12, fill=GRAY, leading=11, align="center")
    nx += nw
hline(24, 1000, NY + 82, fill=HAIR, wdt=1)

# ---------------------------------------------------------------- regions
REGIONS = [
    ("EUROPE", 7, [(4, "Zelenskyy urges US to release Patriot missiles", "REPORTED"),
                    (5, "Mirage jet downs drone with cannon fire", "CONFIRMED"),
                    (6, "Drone hits home in Dymer; two injured", "CONFIRMED"),
                    (7, "Ex-police chief found dead amid Sicily inquiry", "REPORTED")]),
    ("MIDDLE EAST", 6, [(9, "Hamas seeks urgent talks after 3 aid workers killed", "CONFIRMED"),
                         (10, "Iran: two tankers hit mines near Hormuz", "CLAIM"),
                         (11, "Iran unveils dual-missile launcher, missile city", "REPORTED"),
                         (12, "Saudis intercept Houthi drone and missile", "REPORTED")]),
    ("AMERICAS", 6, [(14, "Bolsonaro stable in intensive care", "CONFIRMED"),
                      (15, "Verstappen wins Las Vegas GP by 0.639s", "CONFIRMED"),
                      (16, "Wembanyama: 50 points, 19 boards", "CONFIRMED"),
                      (17, "Trump: Iran killed 81,000 protesters", "CLAIM"),
                      (18, "Guatemala arrests Mexican", "REPORTED")]),
    ("ASIA-PACIFIC", 6, [(20, "Hong Kong polls: 856 vie for 723 seats", "CONFIRMED"),
                          (21, "India declares 720/9 at Wellington", "CONFIRMED"),
                          (22, "Serang fire: 3 dead, 36 missing", "CONFIRMED"),
                          (23, "India: six batters pass 70 — a Test first", "CONFIRMED"),
                          (24, "Serang: 24 body bags found", "ONGOING")]),
    ("AFRICA", 3, [(26, "Drones kill 4 near Khartoum; UN hit", "REPORTED"),
                    (27, "Drone strike hits Russian ship at Benghazi", "REPORTED")]),
    ("OCEANIA", 2, [(29, "NZ trail by 233; Conway 59*", "CONFIRMED"),
                     (30, "Basin Reserve record falls after 31 years", "CONFIRMED")]),
    ("WORLD", 5, [(31, "Guterres 'deeply disappointed' by COP31", "CONFIRMED"),
                   (32, "90+ nations sign electrification pledge", "CONFIRMED")]),
]

def draw_story(x, y, num, head, tag, width):
    """Numbered story with coloured tag; returns y below it."""
    f = SERIF(11)
    nf = SANS_B(11)
    numtxt = f"{num}  "
    nw = text_w(numtxt, nf)
    lines = wrap(head, f, width - nw)
    d.text((x, y), numtxt, font=nf, fill=RED)
    lh = 13
    for j, ln in enumerate(lines):
        d.text((x + nw, y + j * lh), ln, font=f, fill=INK)
    last_w = text_w(lines[-1], f)
    tagtxt = " " + tag
    tf = SANS_B(8)
    if last_w + text_w(tagtxt, tf) <= width - nw - 8:
        d.text((x + nw + last_w, y + (len(lines) - 1) * lh + 2), tagtxt,
               font=tf, fill=TAG_FILL[tag])
        return y + len(lines) * lh + 3
    d.text((x + nw, y + len(lines) * lh + 1), tag, font=tf, fill=TAG_FILL[tag])
    return y + (len(lines) + 1) * lh + 1

def draw_region(x, y, width, name, count, stories):
    d.text((x, y), name, font=SANS_B(12), fill=NAVY)
    d.text((x + width - 14, y), str(count), font=SANS_B(12), fill=RED, anchor="ra")
    bar_y = y + 17
    d.rectangle([x, bar_y, x + 64, bar_y + 5], fill=HAIR)
    d.rectangle([x, bar_y, x + 64 * count / 7, bar_y + 5], fill=NAVY)
    d.text((x + 70, bar_y - 2), "stories", font=SANS(8), fill=GRAY)
    sy = bar_y + 11
    for num, head, tag in stories:
        sy = draw_story(x, sy, num, head, tag, width)
    return sy

RY = 572
ROW1_H, ROW2_H = 132, 112
row1 = REGIONS[:4]
row2 = REGIONS[4:]
cw1 = (976 - 3 * 8) / 4
for i, (name, count, stories) in enumerate(row1):
    draw_region(24 + i * (cw1 + 8), RY, cw1, name, count, stories)
    if i < 3:
        d.line([(24 + (i + 1) * cw1 + i * 8 + 4, RY + 4),
                (24 + (i + 1) * cw1 + i * 8 + 4, RY + ROW1_H - 6)], fill=HAIR, width=1)
hline(24, 1000, RY + ROW1_H + 4, fill=HAIR, wdt=1)
cw2 = (976 - 2 * 8) / 3
for i, (name, count, stories) in enumerate(row2):
    draw_region(24 + i * (cw2 + 8), RY + ROW1_H + 12, cw2, name, count, stories)
    if i < 2:
        d.line([(24 + (i + 1) * cw2 + i * 8 + 4, RY + ROW1_H + 16),
                (24 + (i + 1) * cw2 + i * 8 + 4, RY + ROW1_H + ROW2_H)], fill=HAIR, width=1)

# ---------------------------------------------------------------- map + ALSO
MY = 828
hline(24, 1000, MY - 6, fill=NAVY, wdt=2)
MAPX, MAPY, MAPW, MAPH = 24, MY + 2, 376, 102
d.rectangle([MAPX, MAPY, MAPX + MAPW, MAPY + MAPH], fill=SEA, outline=NAVY, width=1)
d.text((MAPX + 6, MAPY + 3), "WHERE IT HAPPENED", font=SANS_B(9), fill=NAVY)
CONTINENTS = {
    "NA": [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-75, 73), (-55, 60),
           (-65, 45), (-80, 32), (-90, 21), (-105, 20), (-115, 30), (-125, 40),
           (-145, 60), (-168, 66)],
    "SA": [(-80, 10), (-60, 5), (-35, -5), (-40, -20), (-55, -35), (-70, -50),
           (-75, -30), (-80, -10), (-80, 10)],
    "EU": [(-10, 36), (0, 44), (10, 45), (20, 40), (28, 36), (30, 45), (20, 55),
           (10, 58), (5, 60), (-5, 58), (-10, 50), (-10, 36)],
    "AF": [(-18, 15), (-10, 30), (10, 37), (30, 32), (43, 12), (50, 10), (40, -5),
           (35, -20), (20, -35), (12, -18), (8, 4), (-8, 5), (-18, 15)],
    "AS": [(30, 45), (40, 55), (60, 70), (100, 75), (140, 72), (170, 66),
           (160, 60), (140, 40), (130, 35), (120, 20), (105, 10), (95, 15),
           (80, 8), (70, 20), (60, 25), (45, 30), (35, 36), (30, 45)],
    "OC": [(113, -22), (125, -15), (142, -11), (150, -22), (153, -30), (145, -38),
           (130, -32), (115, -35), (113, -22)],
    "GL": [(-45, 60), (-30, 68), (-20, 70), (-30, 76), (-55, 76), (-58, 70), (-45, 60)],
}
def proj(lon, lat):
    px = MAPX + 4 + (lon + 180) / 360 * (MAPW - 8)
    py = MAPY + 16 + (90 - lat) / 180 * (MAPH - 20)
    return (px, py)
for pts in CONTINENTS.values():
    d.polygon([proj(lo, la) for lo, la in pts], fill=LAND, outline=NAVY)
PINS = [(1, 28.0, 34.0), (2, 52.0, 24.0), (3, 30.5, 52.0), (9, 34.4, 29.5),
        (14, -47.9, -15.8), (15, -115.1, 36.2), (20, 114.2, 22.3),
        (21, 174.8, -41.3), (22, 106.1, -6.1), (26, 32.5, 15.6),
        (27, 18.0, 33.5), (28, 40.0, 7.0)]
for num, lo, la in PINS:
    px, py = proj(lo, la)
    d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED, outline=WHITE, width=1)
    d.text((px, py - 1), str(num), font=SANS_B(7), fill=WHITE, anchor="mm")

AX, AY, AW = 412, MY + 2, 588
d.text((AX, AY), "ALSO ON SUNDAY 22 NOVEMBER", font=SANS_B(12), fill=NAVY)
hline(AX, AX + AW, AY + 17, fill=NAVY, wdt=2)
ALSO = [(8, "Paolo Bulgari dies", "REPORTED"),
        (13, "IRGC: US MQ-1 drone downed", "CLAIM"),
        (19, "Brazil: calamity in Tupanciretã", "REPORTED"),
        (25, "S. Korea minister resigns", "REPORTED"),
        (28, "COP32: Addis Ababa, Nov 2027", "CONFIRMED"),
        (33, "Antalya: longest COP on record", "CONFIRMED"),
        (34, "Side deals adopted: adaptation", "CONFIRMED"),
        (35, "Tanker-strike report unconfirmed", "REPORTED")]
ay = AY + 24
colw = (AW - 12) / 2
for i, (num, head, tag) in enumerate(ALSO):
    cx = AX + (i % 2) * (colw + 12)
    cy = ay + (i // 2) * 21
    draw_story(cx, cy, num, head, tag, colw)

# ---------------------------------------------------------------- date check
DY = 938
d.rectangle([24, DY, 1000, DY + 44], fill=(242, 228, 222), outline=RED, width=1)
d.text((34, DY + 5), "DATE CHECK — NOT TODAY'S NEWS", font=SANS_B(11), fill=RED)
dc = ("These made the wires on other days and are NOT stories of Sunday 22 November: "
      "Peru quake (20 Nov) · 110-missile attack (19–20 Nov) · 148-drone night · "
      "Kryvyi Rih (20–21 Nov) · El Chapo arrest (Fri 21 Nov) · Baysela ship, 24 dead "
      "(Fri 21 Nov) · Myanmar genocide ruling (19 Nov) · Sparta II strike (21 Nov) · "
      "Shenzhen summit (19–20 Nov) · EU–Indonesia trade deal (21 Nov).")
para(34, DY + 20, dc, SANS(10), 932, fill=INK, leading=11)

# ---------------------------------------------------------------- legends + footer
lg = ("HOW TO READ THE TAGS — CONFIRMED: verified · REPORTED: carried by the wires · "
      "CLAIM: one side's account · ONGOING: still developing · FORECAST: still to happen")
d.text(((W - text_w(lg, SANS(9))) / 2, 986), lg, font=SANS(9), fill=GRAY)
ft = ("SCENES ARE DRAWN ILLUSTRATIONS, NOT PHOTOGRAPHS.  Sources: Reuters · AP · AFP · "
      "Al Jazeera · BBC · Guardian · UN News · Anadolu · Formula 1 · Cricinfo · China Daily.")
d.text(((W - text_w(ft, SANS_B(9))) / 2, 998), ft, font=SANS_B(9), fill=INK)

# ---------------------------------------------------------------- grain + save
img = Image.alpha_composite(img.convert("RGBA"), grain).convert("RGB")
img.save(OUT, optimize=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes")
