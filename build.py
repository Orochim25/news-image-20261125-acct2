# news-image-20261125 akun 2 — REVISI v2 (layout baru per Sensei)
# Peta dikecilin ke pojok kiri bawah (seperti biasa) + scene hero diperjelas.
# Isi 36 cerita SAMA PERSIS seperti v1. Program gambar PIL, deterministik.
# build(path) menulis PNG 1024x1024 ke path yang diminta.
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1024, 1024
M = 22  # margin halaman

# ---------- palet (navy / merah bata / krem) ----------
NAVY = (31, 58, 95)
NAVY_D = (18, 38, 66)
BRICK = (178, 58, 42)
BRICK_D = (140, 40, 28)
CREAM = (244, 238, 222)
CREAM2 = (250, 246, 234)
PAPER = (247, 243, 232)
INK = (28, 28, 28)
GRAY = (110, 110, 105)
LINE = (31, 58, 95)
SEA = (198, 222, 232)
SEA_D = (168, 200, 216)
LAND = (214, 186, 138)
LANDB = (196, 164, 108)
GREEN = (74, 124, 72)
GREEN_D = (46, 90, 48)
GOLD = (212, 160, 60)
ORANGE = (224, 122, 40)
YELLOW = (240, 200, 80)
SKY = (178, 214, 232)
SKY_D = (140, 190, 220)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
RED = (200, 40, 32)

# ---------- font ----------
FD = "/usr/share/fonts/truetype/dejavu/"
def F(size, bold=False, serif=False):
    try:
        if serif:
            return ImageFont.truetype(FD + ("DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"), size)
        return ImageFont.truetype(FD + ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), size)
    except Exception:
        return ImageFont.load_default()

def tw(d, s, font):
    return d.textlength(s, font=font)

def fit_font(d, s, maxw, size, bold=False, serif=False, minsize=6):
    while size > minsize:
        f = F(size, bold, serif)
        if tw(d, s, f) <= maxw:
            return f
        size -= 1
    return F(minsize, bold, serif)

def wrap(d, s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(d, t, font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def para(d, x, y, s, font, maxw, fill, maxlines=99, lh=None):
    if lh is None:
        lh = font.size + 3
    out = []
    for ln in wrap(d, s, font, maxw)[:maxlines]:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
        out.append(ln)
    return y

# ---------- helper gambar ----------
def person(d, x, y, s, shirt, pants, skin=(232, 190, 150), hair=BLACK):
    # x,y = tengah kaki; s = tinggi orang
    hr = s * 0.16
    d.ellipse([x - hr, y - s, x + hr, y - s + 2 * hr], fill=skin, outline=NAVY_D)
    d.ellipse([x - hr, y - s - hr * 0.5, x + hr, y - s + hr * 0.6], fill=hair)
    d.rectangle([x - s * 0.22, y - s * 0.62, x + s * 0.22, y - s * 0.30], fill=shirt, outline=NAVY_D)
    d.line([x - s * 0.20, y - s * 0.30, x - s * 0.16, y - 1], fill=pants, width=max(2, int(s * 0.09)))
    d.line([x + s * 0.20, y - s * 0.30, x + s * 0.16, y - 1], fill=pants, width=max(2, int(s * 0.09)))
    d.line([x - s * 0.22, y - s * 0.58, x - s * 0.34, y - s * 0.38], fill=shirt, width=max(2, int(s * 0.07)))
    d.line([x + s * 0.22, y - s * 0.58, x + s * 0.34, y - s * 0.38], fill=shirt, width=max(2, int(s * 0.07)))

def building(d, x, y, w, h, color, win=WHITE):
    d.rectangle([x, y, x + w, y + h], fill=color, outline=NAVY_D, width=1)
    cols = max(1, int(w // 14))
    rows = max(1, int(h // 16))
    for i in range(cols):
        for j in range(rows):
            wx = x + 5 + i * (w - 10) / cols
            wy = y + 5 + j * (h - 10) / rows
            d.rectangle([wx, wy, wx + 6, wy + 8], fill=win, outline=NAVY_D)

def car(d, x, y, w, body, top=None):
    h = w * 0.32
    d.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=body, outline=NAVY_D)
    d.polygon([(x + w * 0.18, y), (x + w * 0.30, y - h * 0.55), (x + w * 0.68, y - h * 0.55), (x + w * 0.82, y)], fill=top or body, outline=NAVY_D)
    for wx in (x + w * 0.20, x + w * 0.72):
        d.ellipse([wx, y + h - 4, wx + w * 0.13, y + h + 4], fill=BLACK, outline=NAVY_D)

def tree(d, x, y, s):
    d.line([x, y, x, y - s * 0.45], fill=(110, 80, 50), width=max(2, int(s * 0.08)))
    d.ellipse([x - s * 0.30, y - s, x + s * 0.30, y - s * 0.35], fill=GREEN, outline=GREEN_D)
    d.ellipse([x - s * 0.20, y - s * 0.85, x + s * 0.22, y - s * 0.30], fill=GREEN_D)

def cloud(d, x, y, s, fill=WHITE):
    d.ellipse([x, y, x + s, y + s * 0.45], fill=fill)
    d.ellipse([x + s * 0.2, y - s * 0.25, x + s * 0.8, y + s * 0.35], fill=fill)
    d.ellipse([x + s * 0.55, y - s * 0.1, x + s * 1.05, y + s * 0.45], fill=fill)

def flagpole(d, x, y, h, c1, c2=None):
    d.line([x, y, x, y - h], fill=NAVY_D, width=2)
    d.polygon([(x, y - h), (x + 22, y - h + 6), (x, y - h + 12)], fill=c1, outline=NAVY_D)
    if c2:
        d.polygon([(x, y - h + 6), (x + 22, y - h + 6), (x, y - h + 12)], fill=c2, outline=NAVY_D)

def barrel(d, x, y, s, color=(90, 120, 70)):
    d.rounded_rectangle([x, y, x + s * 0.7, y + s], radius=3, fill=color, outline=NAVY_D)
    d.ellipse([x, y - s * 0.12, x + s * 0.7, y + s * 0.12], fill=(140, 160, 110), outline=NAVY_D)
    d.line([x, y + s * 0.3, x + s * 0.7, y + s * 0.3], fill=NAVY_D, width=1)
    d.line([x, y + s * 0.65, x + s * 0.7, y + s * 0.65], fill=NAVY_D, width=1)

def star4(d, cx, cy, r, fill=WHITE):
    d.polygon([(cx, cy - r), (cx + r * 0.28, cy - r * 0.28), (cx + r, cy), (cx + r * 0.28, cy + r * 0.28),
               (cx, cy + r), (cx - r * 0.28, cy + r * 0.28), (cx - r, cy), (cx - r * 0.28, cy - r * 0.28)], fill=fill, outline=NAVY_D)

def explosion(d, cx, cy, r):
    for rr, col in ((1.0, (200, 60, 30)), (0.78, ORANGE), (0.55, YELLOW), (0.34, (255, 240, 180))):
        d.ellipse([cx - r * rr, cy - r * rr, cx + r * rr, cy + r * rr], fill=col, outline=NAVY_D)
    for a in range(8):
        ang = a * math.pi / 4
        x1, y1 = cx + math.cos(ang) * r * 0.9, cy + math.sin(ang) * r * 0.9
        x2, y2 = cx + math.cos(ang) * r * 1.35, cy + math.sin(ang) * r * 1.35
        d.line([x1, y1, x2, y2], fill=ORANGE, width=4)

def smoke(d, cx, cy, r, fill=(150, 150, 148)):
    for dx, dy, rr in ((-0.6, 0.1, 0.5), (0, -0.3, 0.6), (0.6, 0.05, 0.45), (0.1, 0.35, 0.4)):
        d.ellipse([cx + dx * r - rr * r, cy + dy * r - rr * r, cx + dx * r + rr * r, cy + dy * r + rr * r], fill=fill, outline=(120, 120, 118))

# ---------- data peta (lon/lat, ditulis dari pengetahuan geografi) ----------
NA = [(-168,66),(-162,60),(-155,58),(-150,61),(-140,60),(-135,57),(-130,54),(-126,49),(-124,42),(-121,35),(-115,30),(-111,25),(-107,23),(-102,19),(-97,16),(-93,15),(-89,13),(-86,12),(-83,9),(-79,9),(-81,13),(-84,16),(-87,20),(-90,21),(-91,19),(-96,19),(-97,25),(-94,29),(-90,30),(-85,30),(-81,26),(-80,31),(-76,34),(-75,38),(-73,41),(-70,43),(-67,45),(-64,44),(-60,46),(-55,48),(-55,52),(-60,55),(-64,58),(-67,58),(-72,61),(-78,62),(-84,64),(-90,66),(-94,68),(-100,68),(-110,68),(-120,69),(-130,70),(-140,70),(-150,71),(-158,71),(-164,68)]
GREENLAND = [(-58,64),(-52,60),(-45,60),(-41,63),(-35,66),(-28,68),(-22,70),(-20,74),(-24,76),(-32,78),(-42,77),(-52,74),(-57,70),(-60,66)]
SA = [(-79,9),(-77,5),(-79,1),(-81,-4),(-79,-8),(-76,-13),(-72,-18),(-70,-23),(-70,-28),(-72,-35),(-73,-42),(-74,-48),(-70,-53),(-66,-55),(-65,-49),(-63,-42),(-59,-36),(-54,-33),(-50,-29),(-44,-24),(-41,-20),(-38,-15),(-35,-9),(-35,-6),(-39,-3),(-43,-2),(-47,0),(-51,1),(-54,4),(-58,6),(-62,9),(-67,11),(-71,12),(-75,10)]
EUROPE = [(-10,36),(-9,38),(-9,42),(-5,43),(-2,44),(-1,46),(-4,48),(-2,49),(1,51),(4,52),(7,54),(8,56),(10,57),(12,56),(15,55),(18,56),(20,55),(23,57),(24,59),(22,60),(19,60),(15,60),(10,59),(6,58),(5,60),(8,62),(12,64),(16,66),(20,68),(25,70),(29,71),(31,70),(33,68),(36,66),(39,64),(42,62),(46,61),(49,59),(48,56),(45,54),(42,52),(40,50),(38,47),(35,45),(33,43),(30,41),(28,39),(26,37),(23,36),(21,37),(19,39),(17,40),(15,38),(13,38),(12,42),(10,44),(8,44),(6,43),(3,42),(0,39),(-2,37),(-6,36)]
AFRICA = [(-17,15),(-16,19),(-15,24),(-11,28),(-6,32),(-2,35),(3,37),(8,37),(11,34),(14,32),(19,31),(24,31),(29,31),(32,31),(34,28),(36,25),(38,21),(40,18),(42,15),(44,12),(46,11),(49,11),(51,10),(51,6),(48,3),(45,0),(42,-3),(40,-7),(39,-11),(37,-15),(36,-19),(34,-23),(32,-27),(29,-31),(26,-34),(21,-35),(18,-33),(16,-29),(14,-24),(13,-19),(12,-15),(13,-10),(12,-6),(9,-2),(9,3),(-7,4),(-12,8),(-15,11)]
ASIA = [(32,36),(35,36),(38,37),(41,39),(44,40),(47,41),(50,42),(53,44),(56,45),(59,47),(62,48),(65,50),(68,51),(71,53),(74,55),(77,57),(80,59),(83,61),(86,63),(89,65),(92,66),(95,68),(98,70),(101,71),(104,72),(107,73),(110,74),(113,73),(116,72),(119,71),(122,71),(125,71),(128,71),(131,71),(134,72),(137,72),(140,72),(143,71),(146,70),(149,70),(152,69),(155,68),(158,66),(160,63),(162,60),(164,60),(167,62),(170,65),(173,65),(176,65),(178,64),(175,62),(172,60),(169,58),(166,56),(163,54),(160,52),(157,51),(154,49),(151,47),(148,45),(145,43),(142,41),(140,38),(138,35),(136,33),(134,32),(132,30),(130,28),(128,26),(126,24),(124,22),(122,20),(120,18),(118,15),(116,12),(114,10),(112,8),(110,6),(108,4),(106,2),(104,1),(102,3),(100,6),(98,9),(96,12),(94,15),(92,17),(90,20),(88,22),(86,20),(84,18),(82,16),(80,13),(78,9),(76,9),(74,13),(72,17),(70,20),(68,22),(66,24),(64,25),(62,26),(60,25),(58,26),(56,27),(54,26),(52,27),(50,29),(48,30),(46,29),(44,29),(42,28),(40,27),(38,25),(36,24),(35,22),(34,20),(35,18),(37,16),(38,15),(40,14),(42,15),(41,17),(39,20),(37,24),(36,27),(35,29),(34,31),(35,33),(36,36)]
AUSTRALIA = [(113,-22),(114,-28),(115,-33),(118,-35),(124,-33),(129,-32),(132,-32),(135,-35),(138,-35),(140,-38),(145,-38),(150,-37),(153,-32),(153,-27),(150,-22),(146,-19),(142,-15),(142,-11),(140,-17),(136,-12),(132,-12),(130,-13),(126,-14),(122,-17),(118,-20)]
ISLANDS = [
    [(44,-16),(47,-15),(50,-16),(49,-20),(46,-24),(44,-25),(43,-21)],  # Madagaskar
    [(130,31),(132,33),(135,34),(137,35),(139,35),(141,39),(141,41),(139,42),(136,37),(133,35)],  # Honshu
    [(140,42),(142,42),(144,44),(143,45),(141,45),(140,43)],  # Hokkaido
    [(95,5),(98,3),(101,0),(104,-3),(106,-6),(104,-5),(100,-1),(97,3)],  # Sumatra
    [(105,-6),(108,-7),(111,-7),(114,-8),(114,-9),(110,-8),(107,-7)],  # Jawa
    [(109,1),(111,2),(114,3),(117,1),(118,-2),(116,-4),(113,-4),(110,-2)],  # Kalimantan
    [(131,-1),(134,-2),(137,-3),(141,-4),(145,-6),(147,-8),(146,-8),(142,-8),(138,-7),(134,-4),(131,-2)],  # Nugini
    [(173,-35),(176,-38),(178,-38),(176,-40),(174,-41),(173,-38)],  # NZ Utara
    [(167,-45),(169,-43),(171,-42),(173,-41),(172,-43),(169,-46),(167,-46)],  # NZ Selatan
    [(80,9),(81,8),(81,6),(80,6)],  # Sri Lanka
    [(120,18),(121,17),(122,14),(122,11),(121,10),(120,13),(119,16)],  # Filipina
    [(-5,50),(-3,53),(-5,56),(-3,58),(-1,57),(0,53),(1,51),(-2,50)],  # Inggris
    [(-22,64),(-18,63),(-14,64),(-15,66),(-20,66),(-23,65)],  # Islandia
    [(-85,22),(-80,23),(-75,20),(-74,20),(-78,21),(-83,22)],  # Kuba
    [(120,22),(121,23),(121,25),(120,25)],  # Taiwan
]
CONTINENTS = [NA, GREENLAND, SA, EUROPE, AFRICA, ASIA, AUSTRALIA] + ISLANDS

# 36 titik: (nomor, lon, lat, offset badge dx, dy) — lon/lat SAMA PERSIS seperti v1
DOTS = [
    (1, -75.5, 10.4, 17, 0), (2, -76.4, 37.0, -18, 16), (3, -91.3, 40.8, -23, 0),
    (4, 4.4, 50.9, -19, 8), (5, 37.6, 55.8, 62, 13), (6, 127.0, 37.5, -5, -9),
    (7, 160.0, -9.4, 13, -13), (8, 55.3, 25.2, 12, 17), (9, 4.3, 52.1, -13, 37),
    (10, -74.0, 40.7, 23, 18), (11, 30.7, 36.9, 22, -8), (12, 34.5, 31.5, -37, -8),
    (13, 12.5, 41.9, 21, 30), (14, 30.0, 1.7, 0, 22), (15, 125.7, 39.0, -24, -6),
    (16, 35.2, 32.0, 61, 28), (17, -2.2, 53.5, -43, 15), (18, 0.5, 52.8, 27, 12),
    (19, -77.0, 38.9, -17, -4), (20, -77.0, 38.9, 23, -4), (21, -3.7, 40.4, -47, 34),
    (22, -17.4, 14.7, -17, 15), (23, 6.1, 46.2, 7, 28), (24, 51.4, 35.7, 25, -12),
    (25, 90.4, 23.8, -26, -7), (26, 2.3, 48.9, -29, 42), (27, 151.2, -33.9, -14, 14),
    (28, 139.7, 35.7, 20, -10), (29, 56.5, 26.5, -26, 32), (30, 34.8, 32.1, -25, 35),
    (31, 35.2, 31.8, 17, 30), (32, 88.4, 22.6, 25, 14), (33, 74.1, 15.3, -7, 22),
    (34, 7.5, 51.5, 45, 24), (35, 31.7, 46.5, 61, 25), (36, 77.2, 28.6, 25, 1),
]
INDEX_NAMES = ["Cartagena", "Langley", "Middletown", "Brussels", "Moscow", "Seoul",
    "Honiara", "Dubai", "The Hague", "Brooklyn", "Antalya", "Gaza City",
    "Rome", "Akwe, Ituri", "Pyongyang", "West Bank", "Manchester", "Sandringham",
    "Washington", "Washington", "Madrid", "Dakar", "Geneva", "Tehran",
    "Dhaka", "Paris", "Sydney", "Tokyo", "Hormuz", "Tel Aviv",
    "Jerusalem", "Kolkata", "Goa", "Dortmund", "Kinburn Spit", "New Delhi"]

# ---------- proyeksi peta (panel kiri bawah) ----------
MAP_X0, MAP_Y0, MAP_W, MAP_H = 30, 756, 444, 130
LAT_TOP, LAT_BOT = 60.0, -55.0
def mx(lon):
    return MAP_X0 + (lon + 180.0) / 360.0 * MAP_W
def my(lat):
    return MAP_Y0 + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * MAP_H

# ---------- teks konten (SAMA PERSIS seperti v1) ----------
LARGE = [
    (1, "CARTAGENA SUPERMARKET SIEGE",
     "30 hostages taken in an \u00c9xito store; 10 freed, ~20 still held as captors demand $2M + safe passage.",
     "AMERICAS \u2022 REPORTED", "Sky News / IANS / Reuters", True),
    (2, "CIA + ODNI CYBERATTACK",
     "US spy agencies hit by a cyberattack on classified systems, CNN reports \u2014 2 agencies hit.",
     "NORTH AMERICA \u2022 REPORTED", "CNN, 25 Nov", False),
    (3, "IOWA LEAD-AZIDE DETONATION",
     "Army to blow up 9,500 lbs of ageing lead azide \u2014 the biggest such blast in nearly 50 years; plume 100+ miles.",
     "NORTH AMERICA \u2022 CONFIRMED", "Des Moines Register / US Army", False),
    (4, "NATO VOWS SPACE DEFENSE",
     "NATO vows to defend space after reports Russia may launch a nuclear-armed satellite, possibly Dec 2026.",
     "EUROPE \u2022 REPORTED", "25 Nov", False),
]
MEDIUM = [
    (5, "RUSSIA ACCUSES UKRAINE OF \u201cTERRORISM\u201d",
     "Moscow warns of severe consequences after drone strikes on 2 Russian ships \u2014 in the Gulf of Finland and off Benghazi.",
     "EUROPE \u2022 REPORTED", "25 Nov"),
    (6, "SOUTH KOREA EDUCATION MINISTER RESIGNS",
     "Minister Choi Kyo-jin quits over a national exam-cheating scandal.",
     "ASIA \u2022 CONFIRMED", "25 Nov"),
    (7, "AUSTRALIA\u2013SOLOMON ISLANDS SECURITY PACT",
     "Canberra named Honiara\u2019s primary security partner; no foreign military or security bases.",
     "PACIFIC \u2022 CONFIRMED", "AP, 25 Nov"),
    (8, "VAIBHAV 204 OFF 53 BALLS",
     "India A star smashes the fastest List A double century \u2014 204 off 53 balls, a world-record 28 sixes.",
     "ASIA / SPORT \u2022 CONFIRMED", "Rising Stars Asia Cup"),
    (9, "DUTCH COURT: CLIMATE TARGETS BINDING",
     "The Hague court keeps binding Dutch climate targets in force while the state\u2019s appeal proceeds.",
     "EUROPE \u2022 CONFIRMED", "NOS, 25 Nov"),
    (10, "HUAWEI GUILTY ON 10 OF 12 COUNTS",
     "Brooklyn jury convicts on bank fraud, wire fraud, sanctions violations and trade-secret theft.",
     "ASIA / TECH \u2022 REPORTED", "25 Nov"),
    (11, "COP31 ENDS WITHOUT A DEAL",
     "Antalya summit collapses as oil and gas producers block fossil-fuel phaseout language.",
     "CLIMATE \u2022 REPORTED", "25 Nov"),
    (12, "GAZA DEATH TOLL 74,746",
     "WAFA, 25 Nov; Oxfam: pollution risks across more than 99% of Gaza.",
     "MIDDLE EAST \u2022 REPORTED", "WAFA / Oxfam"),
]
ALSO = [
    (13, "266 MILLION FACE ACUTE FOOD INSECURITY"), (14, "WHO EVACUATES DRC EBOLA STAFF"),
    (15, "NORTH KOREA THREATENS SWISS OFFICE"), (16, "SETTLER ARSON CONDEMNED AS \u201cJEWISH TERRORISM\u201d"),
    (17, "12,000 EVACUATED FROM MANCHESTER CONCERT"), (18, "ANMER HALL BREAK-IN ARRESTS"),
    (19, "GIULIANI AWARDED MEDAL OF FREEDOM"), (20, "TRUMP SET TO UNVEIL NEW TARIFFS"),
    (21, "\u00c1BREGO GARC\u00cdA LEAVES FOR SPAIN"), (22, "SENEGAL AFCON CHAMPIONS REINSTATED"),
    (23, "GUKESH HOLDS SINDAROV IN OPENER"), (24, "IRANIAN SINGER GETS 74 LASHES"),
    (25, "SHEIKH HASINA ANNOUNCES RETURN"), (26, "MACRON WEIGHS SPENDING CAPS"),
    (27, "NSW $35M DRUG SYNDICATE CHARGED"), (28, "ASIAN TECH SHARES SLIDE"),
    (29, "LEWIS PUGH SWIMS HORMUZ"), (30, "ISRAEL: IRAN DEVELOPING CHEMICAL WEAPONS"),
    (31, "LIKUD FRAUD CLAIMS DISMISSED"), (32, "EAST BENGAL HISTORIC WIN"),
    (33, "BEN STOKES ENTERS IPL 2027 AUCTION"), (34, "ARSENAL HELD BY DORTMUND"),
    (35, "KINBURN SPIT RESCUE MISSION"), (36, "PT USHA OUT OF IOA RACE"),
]
NUMBERS = [
    ("30", "HOSTAGES TAKEN IN CARTAGENA"),
    ("9,500", "LBS OF LEAD AZIDE, IOWA BLAST"),
    ("74,746", "GAZA DEATH TOLL"),
    ("266M", "FACE ACUTE FOOD INSECURITY"),
    ("204", "RUNS OFF 53 BALLS \u2014 28 SIXES"),
    ("10 of 12", "COUNTS: HUAWEI GUILTY"),
]
DATECHECK = ("DATE CHECK \u2014 LEFT OUT: Anthropic $2T IPO (19 Nov) \u00b7 Russian extradition "
    "(5 Nov) \u00b7 Missiles over Poland (20 Nov) \u00b7 Tarwekamp blast (Dec 2024). "
    "Huawei verdict was 24 Nov, reported 25 Nov in Asia.")

# ---------- layout ----------
def badge(d, cx, cy, n, r=9):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BRICK, outline=WHITE, width=2)
    f = F(10 if r >= 9 else 9, bold=True)
    s = str(n)
    d.text((cx - tw(d, s, f) / 2, cy - f.size / 2 - 1), s, font=f, fill=WHITE)

def scene_layer(img, x0, y0, w, h, fn):
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    fn(ld, 0, 0, w, h)
    img.paste(lay, (x0, y0), lay)

# ---------- scene hero BESAR (detail, banyak elemen) ----------
def sc_cartagena(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 222, 170))
    d.ellipse([x + w - 52, y + 4, x + w - 16, y + 40], fill=(255, 200, 90), outline=ORANGE, width=2)
    # gedung supermarket
    bx, by, bw, bh = x + 30, y + 14, w - 220, h - 14
    d.rectangle([bx, by, bx + bw, by + bh], fill=CREAM2, outline=NAVY_D, width=2)
    d.rectangle([bx, by, bx + bw, by + 16], fill=BRICK, outline=NAVY_D)
    f = F(13, bold=True)
    d.text((bx + 8, by + 2), "\u00c9XITO", font=f, fill=WHITE)
    # awning merah-putih
    for i in range(8):
        col = BRICK if i % 2 == 0 else WHITE
        d.polygon([(bx + i * bw // 8, by + 16), (bx + (i + 1) * bw // 8, by + 16),
                   (bx + (i + 1) * bw // 8, by + 28), (bx + i * bw // 8, by + 28)], fill=col, outline=NAVY_D)
    # pintu kaca + rak barang di dalam
    d.rectangle([bx + 12, by + 34, bx + bw - 12, by + bh - 2], fill=(150, 200, 220), outline=NAVY_D)
    for r in range(2):
        yy = by + 42 + r * 10
        d.rectangle([bx + 16, yy, bx + bw - 16, yy + 7], fill=(120, 90, 60), outline=NAVY_D)
        for c in range(6):
            d.rectangle([bx + 20 + c * 22, yy + 1, bx + 30 + c * 22, yy + 6],
                        fill=[RED, GOLD, GREEN, (60, 90, 160), ORANGE, (120, 60, 140)][c], outline=NAVY_D)
    # sandera: 2 orang tangan ke atas
    person(d, bx + bw + 18, by + bh - 2, 26, (200, 220, 240), (60, 60, 90))
    person(d, bx + bw + 44, by + bh - 2, 26, (240, 200, 180), (80, 60, 40))
    # polisi + perisai
    person(d, bx + bw + 78, by + bh - 2, 28, NAVY, NAVY_D)
    d.rounded_rectangle([bx + bw + 84, by + bh - 26, bx + bw + 104, by + bh - 2], radius=4, fill=(60, 90, 160), outline=NAVY_D)
    # truk lapis baja
    tx = x + w - 96
    d.rectangle([tx, y + h - 30, tx + 88, y + h - 6], fill=(70, 100, 70), outline=NAVY_D, width=2)
    d.rectangle([tx + 58, y + h - 44, tx + 88, y + h - 30], fill=(70, 100, 70), outline=NAVY_D, width=2)
    for wx in (tx + 10, tx + 62):
        d.ellipse([wx, y + h - 10, wx + 14, y + h + 2], fill=BLACK, outline=NAVY_D)
    d.text((tx + 6, y + h - 27), "POLICE", font=F(8, bold=True), fill=WHITE)
    # pita kuning
    d.rectangle([x, y + h - 4, x + w, y + h], fill=YELLOW, outline=NAVY_D)
    d.text((x + 6, y + h - 4), "", font=F(7), fill=BLACK)

def sc_cia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY_D)
    for sx, sy in ((30, 12), (90, 8), (180, 14), (260, 9), (330, 13), (420, 10), (460, 16)):
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=WHITE)
    # gedung HQ putih berkolom
    bx, by, bw, bh = x + 150, y + 22, 190, h - 22
    d.polygon([(bx, by + 12), (bx + bw // 2, by), (bx + bw, by + 12)], fill=CREAM2, outline=NAVY_D)
    d.rectangle([bx, by + 12, bx + bw, by + bh], fill=CREAM2, outline=NAVY_D, width=2)
    for i in range(4):
        cx = bx + 18 + i * 48
        d.rectangle([cx, by + 16, cx + 12, by + bh - 4], fill=WHITE, outline=NAVY_D)
    d.rectangle([bx + 60, by + bh - 22, bx + bw - 60, by + bh], fill=NAVY_D, outline=NAVY_D)
    # antena parabola di atap
    d.line([bx + bw // 2, by, bx + bw // 2, by - 10], fill=WHITE, width=2)
    d.arc([bx + bw // 2 - 12, by - 22, bx + bw // 2 + 12, by - 2], 200, 340, fill=WHITE, width=3)
    # monitor besar kiri: layar hijau + segitiga peringatan
    mx0, my0, mw, mh = x + 14, y + 26, 120, 46
    d.rectangle([mx0, my0, mx0 + mw, my0 + mh], fill=(10, 30, 20), outline=WHITE, width=2)
    for i, ln in enumerate(["ACCESS DENIED", "CLASSIFIED //", "BREACH DETECTED", "CIA \u2022 ODNI"]):
        d.text((mx0 + 5, my0 + 4 + i * 10), ln, font=F(8, bold=(i == 2)), fill=(80, 220, 120) if i != 2 else (255, 80, 60))
    d.polygon([(mx0 + mw - 22, my0 + 6), (mx0 + mw - 8, my0 + 6), (mx0 + mw - 15, my0 + 20)], fill=YELLOW, outline=NAVY_D)
    # rak server kanan
    rx, ry, rw, rh = x + w - 130, y + 24, 116, 48
    d.rectangle([rx, ry, rx + rw, ry + rh], fill=(40, 46, 56), outline=WHITE, width=2)
    for r in range(3):
        yy = ry + 5 + r * 15
        d.rectangle([rx + 5, yy, rx + rw - 5, yy + 10], fill=(24, 30, 40), outline=NAVY_D)
        for c in range(6):
            col = (80, 220, 120) if (r + c) % 3 else (255, 80, 60)
            d.ellipse([rx + 10 + c * 17, yy + 3, rx + 15 + c * 17, yy + 8], fill=col)
    # kabel kuning penghubung
    d.line([mx0 + mw, my0 + mh - 8, bx, by + bh - 10], fill=YELLOW, width=2)
    d.line([bx + bw, by + bh - 10, rx, ry + rh - 8], fill=YELLOW, width=2)

def sc_iowa(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    cloud(d, x + 20, y + 8, 26)
    cloud(d, x + w - 90, y + 6, 22)
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(150, 170, 110))
    # rumah kecil + pagar kiri
    for hx in (x + 16, x + 66):
        d.polygon([(hx, y + h - 34), (hx + 16, y + h - 46), (hx + 32, y + h - 34)], fill=BRICK, outline=NAVY_D)
        d.rectangle([hx + 2, y + h - 34, hx + 30, y + h - 18], fill=CREAM2, outline=NAVY_D)
    d.line([x + 8, y + h - 22, x + 110, y + h - 22], fill=NAVY_D, width=2)
    # tumpukan barel
    for i in range(4):
        barrel(d, x + 120 + i * 20, y + h - 40, 26, (90, 120, 70))
    for i in range(3):
        barrel(d, x + 130 + i * 20, y + h - 62, 24, (120, 100, 60))
    # ledakan besar tengah-kanan
    ex, ey = x + w - 150, y + 34
    smoke(d, ex - 30, ey - 14, 22)
    smoke(d, ex + 34, ey - 10, 20)
    explosion(d, ex, ey + 8, 30)
    for i in range(6):
        d.ellipse([ex - 60 + i * 22, y + h - 24 + (i % 2) * 4, ex - 52 + i * 22, y + h - 16 + (i % 2) * 4], fill=ORANGE)
    # papan evakuasi + tenda FEMA kanan
    d.line([x + w - 62, y + h - 18, x + w - 62, y + h - 44], fill=NAVY_D, width=2)
    d.rectangle([x + w - 84, y + h - 58, x + w - 40, y + h - 44], fill=YELLOW, outline=NAVY_D)
    d.text((x + w - 82, y + h - 57), "5 MILE", font=F(7, bold=True), fill=NAVY_D)
    d.text((x + w - 82, y + h - 50), "ZONE", font=F(7, bold=True), fill=NAVY_D)
    d.polygon([(x + w - 34, y + h - 18), (x + w - 18, y + h - 40), (x + w - 2, y + h - 18)], fill=WHITE, outline=NAVY_D)
    d.text((x + w - 30, y + h - 30), "FEMA", font=F(7, bold=True), fill=NAVY_D)

def sc_nato(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY_D)
    for sx, sy in ((20, 10), (70, 22), (140, 8), (210, 16), (300, 10), (360, 20), (430, 12), (470, 26), (110, 30), (250, 30)):
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=WHITE)
    # busur Bumi bawah
    d.ellipse([x - 60, y + h - 46, x + w + 60, y + h + 90], fill=(50, 110, 190), outline=WHITE, width=2)
    d.ellipse([x + 60, y + h - 30, x + 140, y + h - 2], fill=GREEN, outline=NAVY_D)
    d.ellipse([x + w - 170, y + h - 26, x + w - 90, y + h - 4], fill=GREEN, outline=NAVY_D)
    cloud(d, x + 200, y + h - 34, 34, fill=(220, 235, 245))
    # roket kecil kiri atas
    rx, ry = x + 26, y + 14
    d.polygon([(rx, ry), (rx + 8, ry + 14), (rx + 16, ry)], fill=WHITE, outline=NAVY_D)
    d.rectangle([rx + 2, ry + 12, rx + 14, ry + 26], fill=BRICK, outline=NAVY_D)
    d.polygon([(rx + 4, ry + 26), (rx + 8, ry + 36), (rx + 12, ry + 26)], fill=ORANGE, outline=NAVY_D)
    # satelit tengah
    sx, sy = x + w - 190, y + 22
    d.rectangle([sx - 34, sy + 8, sx - 8, sy + 22], fill=(70, 110, 200), outline=WHITE, width=1)
    d.rectangle([sx + 8, sy + 8, sx + 34, sy + 22], fill=(70, 110, 200), outline=WHITE, width=1)
    d.rectangle([sx - 8, sy, sx + 8, sy + 30], fill=GOLD, outline=NAVY_D, width=2)
    d.arc([sx + 8, sy - 6, sx + 26, sy + 12], 300, 60, fill=WHITE, width=2)
    d.line([sx, sy + 30, sx, sy + 40], fill=WHITE, width=2)
    # perisai NATO kiri bawah
    px, py = x + 150, y + 34
    d.polygon([(px, py), (px + 46, py), (px + 46, py + 26), (px + 23, py + 44), (px, py + 26)], fill=(40, 70, 140), outline=GOLD, width=3)
    star4(d, px + 23, py + 20, 13, fill=WHITE)
    # bintang 4 penjuru kecil
    star4(d, x + 330, y + 44, 6, fill=GOLD)
    star4(d, x + 400, y + 52, 5, fill=WHITE)

# ---------- scene hero MEDIUM (239x58, tetap 4-6 elemen tiap adegan) ----------
def sc_russia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    cloud(d, x + 10, y + 4, 18)
    d.rectangle([x, y + 32, x + w, y + h], fill=(70, 130, 190))
    d.rectangle([x, y + 32, x + w, y + 35], fill=WHITE)
    # kapal kargo
    hx, hy = x + 40, y + 34
    d.polygon([(hx, hy), (hx + 120, hy), (hx + 108, hy + 16), (hx + 10, hy + 16)], fill=(90, 95, 105), outline=NAVY_D)
    for i, c in enumerate((RED, GOLD, GREEN, (60, 90, 160))):
        d.rectangle([hx + 14 + i * 26, hy - 12, hx + 36 + i * 26, hy], fill=c, outline=NAVY_D)
    d.rectangle([hx + 100, hy - 22, hx + 116, hy - 12], fill=WHITE, outline=NAVY_D)
    # drone di atas kapal
    dx, dy = x + 100, y + 12
    d.rectangle([dx - 8, dy - 3, dx + 8, dy + 3], fill=BLACK, outline=NAVY_D)
    d.line([dx - 14, dy - 6, dx + 14, dy - 6], fill=BLACK, width=2)
    d.line([dx - 14, dy + 6, dx + 14, dy + 6], fill=BLACK, width=2)
    d.line([dx, dy + 3, dx, dy + 12], fill=RED, width=2)
    # menara Kremlin kanan
    kx = x + w - 34
    d.rectangle([kx, y + 8, kx + 18, y + 32], fill=BRICK, outline=NAVY_D)
    d.ellipse([kx - 2, y - 2, kx + 20, y + 12], fill=GOLD, outline=NAVY_D)
    # segitiga peringatan
    d.polygon([(x + w - 30, y + 44), (x + w - 14, y + 44), (x + w - 22, y + 30)], fill=YELLOW, outline=NAVY_D)
    d.text((x + w - 25, y + 36), "!", font=F(9, bold=True), fill=NAVY_D)

def sc_korea(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 232, 210))
    # papan tulis
    d.rectangle([x + 10, y + 4, x + 100, y + 24], fill=(50, 100, 70), outline=NAVY_D)
    d.text((x + 14, y + 8), "EXAM  \u2713 \u2713 \u2717", font=F(9, bold=True), fill=WHITE)
    # meja + kertas ujian
    d.rectangle([x + 10, y + 40, x + w - 10, y + 48], fill=(140, 100, 60), outline=NAVY_D)
    for i in range(3):
        d.rectangle([x + 20 + i * 44, y + 30, x + 48 + i * 44, y + 40], fill=WHITE, outline=NAVY_D)
        d.line([x + 24 + i * 44, y + 34, x + 44 + i * 44, y + 34], fill=GRAY, width=1)
        d.line([x + 24 + i * 44, y + 37, x + 40 + i * 44, y + 37], fill=GRAY, width=1)
    # murid + menteri membungkuk
    person(d, x + 40, y + h - 2, 22, (60, 90, 160), (50, 50, 70))
    person(d, x + w - 60, y + h - 2, 24, (40, 40, 50), (40, 40, 50))
    # surat pengunduran diri + stempel merah
    d.rectangle([x + w - 96, y + 26, x + w - 64, y + 40], fill=WHITE, outline=NAVY_D)
    d.line([x + w - 92, y + 30, x + w - 68, y + 30], fill=GRAY, width=1)
    d.line([x + w - 92, y + 34, x + w - 72, y + 34], fill=GRAY, width=1)
    d.ellipse([x + w - 72, y + 33, x + w - 64, y + 41], fill=RED, outline=NAVY_D)

def sc_pact(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + 30], fill=(70, 150, 200))
    d.rectangle([x, y + 30, x + w, y + h], fill=(232, 210, 160))
    d.ellipse([x + w - 34, y + 4, x + w - 10, y + 28], fill=(255, 210, 110), outline=ORANGE, width=2)
    # palem kiri
    tree(d, x + 26, y + h - 4, 30)
    # dua tiang bendera
    flagpole(d, x + 70, y + h - 4, 34, (40, 80, 180))
    flagpole(d, x + 150, y + h - 4, 34, (40, 120, 80), (250, 210, 60))
    # jabat tangan: dua lengan bersilang
    d.line([x + 92, y + 34, x + 128, y + 44], fill=(232, 190, 150), width=6)
    d.line([x + 128, y + 34, x + 92, y + 44], fill=(210, 170, 130), width=6)
    d.ellipse([x + 102, y + 32, x + 118, y + 48], fill=(240, 200, 160), outline=NAVY_D)
    # ombak
    d.arc([x + 10, y + 26, x + 60, y + 40], 0, 180, fill=WHITE, width=2)
    d.arc([x + 170, y + 24, x + 220, y + 38], 0, 180, fill=WHITE, width=2)

def sc_vaibhav(d, x, y, w, h):
    # tribun + penonton
    d.rectangle([x, y, x + w, y + 16], fill=(90, 95, 105))
    for i in range(14):
        d.ellipse([x + 8 + i * 16, y + 5, x + 14 + i * 16, y + 11], fill=[RED, WHITE, GOLD, GREEN][i % 4])
    d.rectangle([x, y + 16, x + w, y + h], fill=(90, 160, 90))
    d.rectangle([x + 60, y + 22, x + w - 60, y + h - 2], fill=(150, 200, 130), outline=NAVY_D)
    # papan skor 204
    d.rectangle([x + w - 62, y + 20, x + w - 8, y + 40], fill=(20, 60, 30), outline=WHITE, width=2)
    d.text((x + w - 58, y + 22), "204", font=F(15, bold=True), fill=YELLOW)
    # pemukul + bat + bola + stumps
    person(d, x + 90, y + h - 2, 30, WHITE, WHITE, hair=(40, 40, 40))
    d.line([x + 100, y + 22, x + 118, y + 6], fill=(150, 110, 60), width=5)
    d.ellipse([x + 128, y + 8, x + 134, y + 14], fill=RED, outline=NAVY_D)
    d.line([x + 134, y + 11, x + 150, y + 8], fill=RED, width=1)
    d.line([x + 150, y + 11, x + 164, y + 8], fill=RED, width=1)
    for i in range(3):
        d.line([x + 150 + i * 4, y + h - 16, x + 150 + i * 4, y + h - 4], fill=YELLOW, width=2)
    # lampu sorot
    d.line([x + 12, y + 16, x + 12, y + 30], fill=NAVY_D, width=2)
    d.ellipse([x + 6, y + 28, x + 18, y + 36], fill=YELLOW, outline=NAVY_D)

def sc_dutch(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    cloud(d, x + 8, y + 4, 16)
    # turbin angin
    for tx in (x + 22, x + w - 30):
        d.line([tx, y + 12, tx, y + h - 14], fill=WHITE, width=3)
        for a in (90, 210, 330):
            ang = math.radians(a)
            d.line([tx, y + 12, tx + int(11 * math.cos(ang)), y + 12 + int(11 * math.sin(ang))], fill=WHITE, width=3)
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(120, 180, 100))
    # gedung pengadilan
    bx, by, bw, bh = x + 66, y + 14, 108, 30
    d.polygon([(bx, by + 8), (bx + bw // 2, by), (bx + bw, by + 8)], fill=CREAM2, outline=NAVY_D)
    d.rectangle([bx, by + 8, bx + bw, by + bh], fill=CREAM2, outline=NAVY_D, width=2)
    for i in range(3):
        cx = bx + 12 + i * 34
        d.rectangle([cx, by + 12, cx + 8, by + bh - 2], fill=WHITE, outline=NAVY_D)
    # palu + timbangan
    d.line([x + w - 44, y + 22, x + w - 22, y + 34], fill=(120, 80, 40), width=4)
    d.rectangle([x + w - 50, y + 14, x + w - 34, y + 26], fill=(120, 80, 40), outline=NAVY_D, width=2)
    d.ellipse([x + w - 46, y + 36, x + w - 30, y + 42], fill=(150, 110, 60), outline=NAVY_D)

def sc_huawei(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(210, 190, 160))
    # meja hakim kayu
    d.rectangle([x + 8, y + 30, x + w - 8, y + 44], fill=(110, 75, 45), outline=NAVY_D, width=2)
    d.rectangle([x + 8, y + 44, x + w - 8, y + h - 2], fill=(90, 60, 35), outline=NAVY_D)
    # ponsel + chip
    d.rectangle([x + 16, y + 8, x + 52, y + 28], fill=BLACK, outline=NAVY_D, width=2)
    d.rectangle([x + 19, y + 11, x + 49, y + 25], fill=(60, 140, 220), outline=NAVY_D)
    d.rectangle([x + 66, y + 8, x + 96, y + 28], fill=(40, 40, 50), outline=GOLD, width=2)
    for px in (70, 78, 86):
        d.line([px, y + 4, px, y + 8], fill=GOLD, width=2)
        d.line([px, y + 28, px, y + 32], fill=GOLD, width=2)
    # kertas vonis 10 OF 12
    d.rectangle([x + 108, y + 6, x + 168, y + 30], fill=WHITE, outline=NAVY_D, width=2)
    d.text((x + 112, y + 8), "10 OF 12", font=F(11, bold=True), fill=BRICK)
    d.text((x + 112, y + 21), "GUILTY", font=F(8, bold=True), fill=NAVY_D)
    # palu di atas meja
    d.line([x + 184, y + 18, x + 206, y + 30], fill=(120, 80, 40), width=4)
    d.rectangle([x + 176, y + 10, x + 192, y + 22], fill=(120, 80, 40), outline=NAVY_D, width=2)

def sc_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 225, 200))
    d.rectangle([x, y, x + w, y + 14], fill=(120, 140, 170))
    d.ellipse([x + w - 26, y + 2, x + w - 8, y + 12], fill=(255, 210, 110), outline=ORANGE)
    # meja konferensi + bendera
    d.rectangle([x + 10, y + 34, x + w - 10, y + 44], fill=(110, 75, 45), outline=NAVY_D, width=2)
    for i, c in enumerate((RED, (40, 80, 180), GREEN, GOLD, (120, 60, 140))):
        flagpole(d, x + 22 + i * 18, y + 34, 16, c)
    # globe di atas meja
    d.ellipse([x + 108, y + 16, x + 132, y + 40], fill=(50, 110, 190), outline=NAVY_D, width=2)
    d.ellipse([x + 114, y + 22, x + 122, y + 30], fill=GREEN, outline=NAVY_D)
    d.ellipse([x + 122, y + 30, x + 130, y + 36], fill=GREEN, outline=NAVY_D)
    # menara minyak + X merah
    dx = x + w - 52
    d.polygon([(dx, y + h - 4), (dx + 8, y + 18), (dx + 16, y + 18), (dx + 24, y + h - 4)], fill=(40, 40, 46), outline=NAVY_D)
    d.line([dx - 2, y + 14, dx + 26, y + 40], fill=RED, width=4)
    d.line([dx + 26, y + 14, dx - 2, y + 40], fill=RED, width=4)

def sc_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 220, 170))
    d.ellipse([x + w - 30, y + 4, x + w - 8, y + 26], fill=(255, 200, 90), outline=ORANGE, width=2)
    # skyline (satu gedung rusak)
    for i, (bx, bw, bh, brk) in enumerate([(8, 30, 26, 0), (42, 26, 34, 1), (72, 34, 22, 0), (110, 28, 30, 0)]):
        by = y + h - 12 - bh
        d.rectangle([x + bx, by, x + bx + bw, y + h - 12], fill=(150, 145, 135), outline=NAVY_D)
        if brk:
            d.polygon([(x + bx, by), (x + bx + 10, by - 6), (x + bx + 18, by), (x + bx + bw, by)], fill=(150, 145, 135), outline=NAVY_D)
        for wy in range(by + 5, y + h - 14, 9):
            d.rectangle([x + bx + 5, wy, x + bx + 11, wy + 5], fill=(60, 60, 70), outline=NAVY_D)
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(120, 110, 95))
    # truk bantuan
    tx = x + 150
    d.rectangle([tx, y + h - 30, tx + 52, y + h - 14], fill=WHITE, outline=NAVY_D, width=2)
    d.rectangle([tx + 52, y + h - 26, tx + 68, y + h - 14], fill=WHITE, outline=NAVY_D, width=2)
    d.text((tx + 12, y + h - 29), "+", font=F(14, bold=True), fill=RED)
    for wx in (tx + 8, tx + 54):
        d.ellipse([wx, y + h - 18, wx + 10, y + h - 8], fill=BLACK, outline=NAVY_D)
    # merpati + ranting zaitun
    d.ellipse([x + 210, y + 12, x + 228, y + 22], fill=WHITE, outline=NAVY_D)
    d.ellipse([x + 224, y + 6, x + 230, y + 12], fill=WHITE, outline=NAVY_D)
    d.polygon([(x + 228, y + 14), (x + 238, y + 18), (x + 228, y + 20)], fill=GOLD, outline=NAVY_D)
    d.line([x + 214, y + 24, x + 226, y + 30], fill=GREEN_D, width=2)
    d.ellipse([x + 222, y + 28, x + 228, y + 33], fill=GREEN, outline=GREEN_D)

SCENES = {1: sc_cartagena, 2: sc_cia, 3: sc_iowa, 4: sc_nato, 5: sc_russia,
          6: sc_korea, 7: sc_pact, 8: sc_vaibhav, 9: sc_dutch, 10: sc_huawei,
          11: sc_cop31, 12: sc_gaza}

# ---------- panel hero ----------
def draw_hero(img, x0, y0, w, h, num, title, body, tag, src, scene_h, top_story=False):
    d = ImageDraw.Draw(img)
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=CREAM2, outline=NAVY, width=2)
    if top_story:
        d.rectangle([x0, y0, x0 + w, y0 + 16], fill=BRICK, outline=NAVY)
        f = F(10, bold=True)
        t = "\u2605  TOP STORY  \u2605"
        d.text((x0 + (w - tw(d, t, f)) / 2, y0 + 3), t, font=f, fill=WHITE)
        scene_layer(img, x0 + 2, y0 + 18, w - 4, scene_h - 2, SCENES[num])
    else:
        scene_layer(img, x0 + 2, y0 + 2, w - 4, scene_h, SCENES[num])
    ty = y0 + scene_h + 8
    tf = fit_font(d, title, w - 16, 15 if h > 130 else 12, bold=True)
    for ln in wrap(d, title, tf, w - 16)[:2]:
        d.text((x0 + 8, ty), ln, font=tf, fill=NAVY_D)
        ty += tf.size + 2
    bf = F(10 if h > 130 else 9)
    # turunkan ukuran font sampai body muat 2 baris (jangan ada kata terpotong)
    while bf.size > 7 and len(wrap(d, body, bf, w - 16)) > 2:
        bf = F(bf.size - 1)
    ty = para(d, x0 + 8, ty + 2, body, bf, w - 16, INK, maxlines=2, lh=bf.size + 3)
    tagf = F(9 if h > 130 else 8, bold=True)
    d.text((x0 + 8, y0 + h - 13), tag, font=tagf, fill=BRICK)
    sf = F(9 if h > 130 else 8)
    d.text((x0 + w - 8 - tw(d, src, sf), y0 + h - 13), src, font=sf, fill=GRAY)
    badge(d, x0 + 13, y0 + 13, num, r=9)

# ---------- masthead + strip angka ----------
def draw_masthead(img):
    d = ImageDraw.Draw(img)
    title = "THE WORLD IN ONE DAY"
    tf = fit_font(d, title, W - 2 * M, 46, bold=True, serif=True)
    d.text(((W - tw(d, title, tf)) / 2, M), title, font=tf, fill=NAVY_D)
    sub = "WEDNESDAY 25 NOVEMBER 2026  \u2014  36 STORIES FROM 6 REGIONS"
    sf = F(13, bold=True)
    d.text(((W - tw(d, sub, sf)) / 2, M + 48), sub, font=sf, fill=BRICK)
    d.line([M, M + 66, W - M, M + 66], fill=NAVY, width=2)
    d.line([M, M + 69, W - M, M + 69], fill=NAVY, width=1)

def draw_numbers(img, y0, h):
    d = ImageDraw.Draw(img)
    d.rectangle([M, y0, W - M, y0 + h], fill=CREAM2, outline=NAVY, width=1)
    cw = (W - 2 * M) / 6.0
    for i, (num, lab) in enumerate(NUMBERS):
        cx = M + cw * i + cw / 2
        nf = fit_font(d, num, cw - 14, 30, bold=True)
        d.text((cx - tw(d, num, nf) / 2, y0 + 4), num, font=nf, fill=NAVY_D)
        lf = fit_font(d, lab, cw - 10, 9, bold=True)
        d.text((cx - tw(d, lab, lf) / 2, y0 + h - 14), lab, font=lf, fill=GRAY)
        if i:
            d.line([M + cw * i, y0 + 6, M + cw * i, y0 + h - 6], fill=NAVY, width=1)

# ---------- panel peta (kiri bawah) ----------
def draw_map_panel(img):
    x0, y0, w, h = M, 726, 460, 230
    d = ImageDraw.Draw(img)
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=PAPER, outline=NAVY, width=2)
    tf = F(11, bold=True)
    d.text((x0 + 8, y0 + 5), "WHERE IT HAPPENED \u2014 36 STORIES, 36 PLACES", font=tf, fill=NAVY_D)
    cf = F(9)
    d.text((x0 + 8, y0 + 20), "AMERICAS 6 \u00b7 EUROPE 12 \u00b7 MIDDLE EAST 6 \u00b7 ASIA 8 \u00b7 AFRICA 2 \u00b7 PACIFIC 2", font=cf, fill=GRAY)
    # peta digambar di layer sendiri seukuran kotak laut -> terpotong di batasnya
    lay = Image.new("RGBA", (MAP_W, MAP_H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    # laut + graticule (koordinat layer: kurangi MAP_X0/MAP_Y0)
    ld.rectangle([0, 0, MAP_W, MAP_H], fill=SEA)
    for lon in range(-150, 181, 30):
        lx = mx(lon) - MAP_X0
        ld.line([lx, 0, lx, MAP_H], fill=SEA_D, width=1)
    for lat in (-30, 0, 30):
        ly = my(lat) - MAP_Y0
        ld.line([0, ly, MAP_W, ly], fill=SEA_D, width=1)
    # benua: fill tan + garis pantai NAVY width 2
    for poly in CONTINENTS:
        pts = [(mx(lon) - MAP_X0, my(lat) - MAP_Y0) for lon, lat in poly]
        ld.polygon(pts, fill=LAND)
    for poly in CONTINENTS:
        pts = [(mx(lon) - MAP_X0, my(lat) - MAP_Y0) for lon, lat in poly]
        ld.line(pts + [pts[0]], fill=NAVY, width=2, joint="curve")
    # titik + badge (leader line dulu, lalu dot, lalu badge)
    pxs = {}
    for n, lon, lat, dx, dy in DOTS:
        px, py = mx(lon), my(lat)
        pxs[n] = (px, py)
        bx, by = px + dx, py + dy
        ld.line([px - MAP_X0, py - MAP_Y0, bx - MAP_X0, by - MAP_Y0], fill=NAVY, width=1)
    drawn = set()
    for n, lon, lat, dx, dy in DOTS:
        px, py = pxs[n]
        key = (round(px, 1), round(py, 1))
        if key not in drawn:
            lx, ly = px - MAP_X0, py - MAP_Y0
            ld.ellipse([lx - 3.5, ly - 3.5, lx + 3.5, ly + 3.5], fill=BRICK, outline=WHITE, width=1)
            drawn.add(key)
    for n, lon, lat, dx, dy in DOTS:
        px, py = pxs[n]
        bx, by = px + dx, py + dy
        badge(ld, bx - MAP_X0, by - MAP_Y0, n, r=8)
    img.paste(lay, (MAP_X0, MAP_Y0), lay)
    # REGION INDEX: 6 kolom x 6 baris
    inf = F(8)
    inb = F(8, bold=True)
    for i, name in enumerate(INDEX_NAMES):
        col, row = i % 6, i // 6
        ix = x0 + 8 + col * 75
        iy = y0 + 166 + row * 10
        ns = str(i + 1)
        d.text((ix, iy), ns, font=inb, fill=BRICK)
        d.text((ix + tw(d, ns, inb) + 3, iy), name, font=inf, fill=INK)
    return pxs

# ---------- panel ALSO ----------
def draw_also(img):
    x0, y0, w, h = 490, 726, 512, 230
    d = ImageDraw.Draw(img)
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=PAPER, outline=NAVY, width=2)
    tf = F(12, bold=True)
    d.text((x0 + 8, y0 + 5), "ALSO ON 25 NOVEMBER", font=tf, fill=NAVY_D)
    d.line([x0 + 8, y0 + 22, x0 + w - 8, y0 + 22], fill=BRICK, width=2)
    for i, (n, head) in enumerate(ALSO):
        col, row = i // 12, i % 12
        ix = x0 + 8 + col * 250
        iy = y0 + 30 + row * 16
        nf = F(10, bold=True)
        ns = str(n)
        d.text((ix, iy), ns, font=nf, fill=BRICK)
        hf = fit_font(d, head, 222, 10, bold=False, minsize=7)
        d.text((ix + tw(d, ns, nf) + 4, iy + (10 - hf.size) // 2), head, font=hf, fill=INK)

# ---------- DATE CHECK + footer ----------
def draw_bottom(img):
    d = ImageDraw.Draw(img)
    d.rectangle([M, 962, M + 6, 984], fill=BRICK)
    df = fit_font(d, DATECHECK, W - 2 * M - 14, 10, bold=True, minsize=8)
    lines = wrap(d, DATECHECK, df, W - 2 * M - 14)
    yy = 962
    for ln in lines[:2]:
        d.text((M + 12, yy), ln, font=df, fill=NAVY_D)
        yy += df.size + 2
    d.line([M, 988, W - M, 988], fill=NAVY, width=2)
    d.line([M, 991, W - M, 991], fill=NAVY, width=1)
    ff = F(10, bold=True)
    f1 = "Every story above happened or was first reported on Wednesday 25 November 2026."
    f2 = "Sources: Reuters \u00b7 CNN \u00b7 AP \u00b7 NOS \u00b7 Sky News \u00b7 IANS \u00b7 Des Moines Register \u00b7 WHO \u00b7 WFP"
    tot = tw(d, f1, ff) + 8 + tw(d, f2, F(9))
    sx = (W - tot) / 2
    d.text((sx, 994), f1, font=ff, fill=NAVY_D)
    d.text((sx + tw(d, f1, ff) + 8, 995), f2, font=F(9), fill=GRAY)

# ---------- build ----------
def build(path):
    img = Image.new("RGB", (W, H), CREAM)
    draw_masthead(img)
    draw_numbers(img, 90, 48)
    for i, (num, title, body, tag, src, top) in enumerate(LARGE):
        x0 = M + (i % 2) * (486 + 8)
        y0 = 144 + (i // 2) * (162 + 8)
        draw_hero(img, x0, y0, 486, 162, num, title, body, tag, src, 80, top_story=top)
    for i, (num, title, body, tag, src) in enumerate(MEDIUM):
        x0 = M + (i % 4) * (239 + 8)
        y0 = 482 + (i // 4) * (115 + 8)
        draw_hero(img, x0, y0, 239, 115, num, title, body, tag, src, 58)
    pxs = draw_map_panel(img)
    draw_also(img)
    draw_bottom(img)
    # debug: koordinat titik + jarak badge minimum
    print("MAP px:", {n: (round(pxs[n][0], 1), round(pxs[n][1], 1)) for n in sorted(pxs)})
    badges = {}
    for n, lon, lat, dx, dy in DOTS:
        badges[n] = (pxs[n][0] + dx, pxs[n][1] + dy)
    close = []
    mind = 1e9
    pair = None
    for a in sorted(badges):
        for b in sorted(badges):
            if b <= a:
                continue
            dist = math.hypot(badges[a][0] - badges[b][0], badges[a][1] - badges[b][1])
            if dist < mind:
                mind, pair = dist, (a, b)
            if dist < 18:
                close.append((a, b, round(dist, 1)))
    print("MAP min badge distance:", round(mind, 1), "px between", pair)
    print("MAP close badge pairs (<18px):", close)
    print("BOTTOM y = 1002  page H = 1024")
    img.save(path, "PNG")
    print("saved", path)

if __name__ == "__main__":
    build("/output/entry.png")
