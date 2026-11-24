#!/usr/bin/env python3
"""Render THE WORLD TODAY front page for 23 November 2026 (news-23 b159 heroes-scene).

Draws entry.png 1024x1024 with PIL. All 31 stories dated 23 Nov 2026.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
MUTED = (90, 86, 76)
RED = (185, 28, 28)
NAVY = (15, 42, 74)
NAVY2 = (24, 62, 104)
GOLD = (201, 162, 39)
GOLD_LT = (232, 196, 90)
TEAL = (14, 90, 92)
RULE = (200, 192, 172)
CARD_BG = (255, 255, 255)
MAP_BG = (214, 226, 232)
MAP_LAND = (168, 186, 196)

FD = "/usr/share/fonts/truetype/dejavu"
FL = "/usr/share/fonts/truetype/liberation"


def font(name, size):
    paths = {
        "bold": os.path.join(FD, "DejaVuSans-Bold.ttf"),
        "reg": os.path.join(FD, "DejaVuSans.ttf"),
        "italic": os.path.join(FL, "LiberationSans-Italic.ttf"),
        "mono": os.path.join(FD, "DejaVuSansMono.ttf"),
    }
    return ImageFont.truetype(paths[name], size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(draw, xy, s, fnt, fill=INK, anchor="la"):
    draw.text(xy, s, font=fnt, fill=fill, anchor=anchor)


def chip(draw, x, y, label, color):
    """Small REPORTED/CLAIM chip; returns width used."""
    f = font("bold", 8)
    w = int(draw.textlength(label, font=f)) + 10
    draw.rounded_rectangle([x, y, x + w, y + 13], radius=2, fill=color)
    draw.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return w


def hline(draw, y, x0=16, x1=1008, fill=RULE, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_scene_kospi(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=NAVY)
    # stars
    import random
    rnd = random.Random(7)
    for _ in range(24):
        sx = x + rnd.randint(4, w - 4)
        sy = y + rnd.randint(4, int(h * 0.35))
        draw.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
    # skyline
    base = y + h
    heights = [0.42, 0.62, 0.34, 0.72, 0.5, 0.66, 0.38, 0.58]
    bw = w // 8
    for i, fh in enumerate(heights):
        bx = x + i * bw
        bh = int(h * fh)
        draw.rectangle([bx + 2, base - bh, bx + bw - 2, base], fill=(10, 28, 52))
        for wy in range(base - bh + 8, base - 6, 14):
            for wx in range(bx + 6, bx + bw - 6, 10):
                if (wx + wy) % 3 == 0:
                    draw.rectangle([wx, wy, wx + 4, wy + 5], fill=GOLD_LT)
    # orange descending chart line
    pts = [(x + 12, y + 26), (x + w * 0.3, y + 44), (x + w * 0.55, y + 40),
           (x + w * 0.78, y + 66), (x + w - 12, y + 88)]
    draw.line(pts, fill=(255, 122, 26), width=4)
    for px, py in pts:
        draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 122, 26))
    # big number band
    draw.rectangle([x, y + h - 34, x + w, y + h], fill=(8, 22, 44))
    text(draw, (x + 10, y + h - 30), "-3.3%", font("bold", 24), fill=GOLD_LT)
    text(draw, (x + 118, y + h - 24), "KOSPI 4,708.54  ·  -161 PTS",
         font("bold", 11), fill=(255, 255, 255))


def draw_scene_guterres(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=TEAL)
    # globe
    cx, cy, r = x + w - 78, y + 62, 46
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(8, 60, 70),
                 outline=GOLD_LT, width=2)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=1)
    for k in range(-2, 3):
        draw.arc([cx - r + abs(k) * 12, cy - r, cx + r - abs(k) * 12, cy + r],
                 90, 270, fill=(140, 200, 200))
    draw.line([(cx - r, cy), (cx + r, cy)], fill=(140, 200, 200))
    draw.arc([cx - r, cy - 16, cx + r, cy + 16], 0, 360, fill=(140, 200, 200))
    # gold headline text (left column)
    text(draw, (x + 12, y + 12), "REGULATE AI", font("bold", 21), fill=GOLD_LT)
    text(draw, (x + 12, y + 38), "BEFORE IT'S", font("bold", 21), fill=GOLD_LT)
    text(draw, (x + 12, y + 64), "TOO LATE", font("bold", 21), fill=GOLD_LT)
    text(draw, (x + 12, y + 92), "150 DELEGATES", font("bold", 13), fill=(255, 255, 255))
    text(draw, (x + 12, y + 110), "BRIDGETOWN SUMMIT", font("bold", 11), fill=(255, 255, 255))
    # flags row
    flag_cols = [(185, 28, 28), (255, 255, 255), (15, 42, 74), (201, 162, 39),
                 (14, 120, 60), (255, 255, 255)]
    for i, c in enumerate(flag_cols):
        fx = x + 12 + i * 26
        draw.rectangle([fx, y + h - 22, fx + 20, y + h - 8], fill=c,
                       outline=(255, 255, 255))


def draw_scene_power(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(242, 236, 222))
    text(draw, (x + 12, y + 10), "ASIA POWER INDEX 2026", font("bold", 12), fill=INK)
    bars = [("US", 78.9, NAVY, (255, 255, 255)), ("CHINA", 73.6, RED, (255, 255, 255)),
            ("INDIA", 40.5, GOLD, INK)]
    by = y + 36
    for name, val, col, tcol in bars:
        bw = int((w - 110) * val / 85.0)
        draw.rectangle([x + 12, by, x + 12 + bw, by + 22], fill=col)
        text(draw, (x + 18, by + 5), name, font("bold", 11), fill=tcol)
        text(draw, (x + 18 + bw, by + 4), f"{val}", font("bold", 12), fill=INK)
        by += 34
    text(draw, (x + 12, y + h - 16), "GAP 5.3 — NARROWEST SINCE 2018",
         font("bold", 11), fill=RED)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 56], fill=INK)
    text(d, (16, 8), "THE WORLD TODAY", font("bold", 34), fill=(255, 255, 255))
    text(d, (1008, 14), "MONDAY", font("bold", 15), fill=GOLD_LT, anchor="ra")
    text(d, (1008, 34), "23 NOVEMBER 2026", font("bold", 15), fill=(255, 255, 255),
         anchor="ra")
    # kicker
    text(d, (16, 64), "SUM UP 23 NOVEMBER'S WORLD NEWS IN ONE IMAGE  ·  31 STORIES  ·  ALL DATED MONDAY 23 NOVEMBER 2026",
         font("bold", 11), fill=RED)
    hline(d, 84, width=2)

    # ---- number strip: 2 rows x 5 ----
    nums = [("-3.3%", "KOSPI FALLS"), ("5.3", "US–CHINA POWER GAP"),
            ("11,762", "EBOLA CASES, DRC"), ("10T WON", "SEOUL RESCUE FUND"),
            ("2%", "BILLIONAIRE TAX"), ("$450M", "SKUBAL METS DEAL"),
            ("165", "RUSSIAN MISSILES / WEEK"), ("12,000", "CLEARED, MANCHESTER"),
            ("264 KG", "EXPLOSIVES, LEBANON"), ("$107.3B", "ANTHROPIC IPO")]
    col_w = (W - 32) // 5
    for i, (val, lab) in enumerate(nums):
        cx = 16 + (i % 5) * col_w
        cy = 92 + (i // 5) * 34
        text(d, (cx + 4, cy), val, font("bold", 17), fill=NAVY)
        text(d, (cx + 4, cy + 20), lab, font("bold", 8), fill=MUTED)
    hline(d, 164, width=2)

    # ---- region bar ----
    text(d, (16, 172), "ASIA-PACIFIC 7   ·   AMERICAS 8   ·   MIDDLE EAST 6   ·   EUROPE 5   ·   AFRICA 3   ·   WORLD 2",
         font("bold", 11), fill=INK)
    text(d, (1008, 172), "31 STORIES", font("bold", 11), fill=RED, anchor="ra")
    hline(d, 192, width=2)

    # ---- heroes: 3 big scenes ----
    heroes = [
        ("AI ROUT HITS ASIA",
         "Kospi −3.3% to 4,708.54, sheds 161 pts; intraday −5.8%. Samsung −3.1%, SK Hynix −2.5%.",
         "REUTERS", "REPORTED", draw_scene_kospi),
        ("GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
         "Bridgetown summit: 150 delegates back a risk framework. A blueprint, not a treaty.",
         "AP", "REPORTED", draw_scene_guterres),
        ("US LEAD OVER CHINA AT RECORD LOW",
         "Asia Power Index 2026: US 78.9, China 73.6 — gap 5.3, narrowest since 2018.",
         "BLOOMBERG", "REPORTED", draw_scene_power),
    ]
    hx0, hy0 = 16, 200
    hw = (W - 32 - 2 * 12) // 3  # 320
    scene_h = 148
    for i, (head, body, src, tag, scene_fn) in enumerate(heroes):
        x = hx0 + i * (hw + 12)
        scene_fn(d, x, hy0, hw, scene_h)
        # headline below scene
        lines = wrap(d, head, font("bold", 15), hw)
        ly = hy0 + scene_h + 10
        for ln in lines[:2]:
            text(d, (x, ly), ln, font("bold", 15), fill=INK)
            ly += 19
        # body
        blines = wrap(d, body, font("reg", 11), hw)
        for ln in blines[:2]:
            text(d, (x, ly), ln, font("reg", 11), fill=(60, 56, 48))
            ly += 14
        # source + chip
        sy = hy0 + scene_h + 96
        text(d, (x, sy), src, font("bold", 9), fill=MUTED)
        chip(d, x + 78, sy - 1, tag, (14, 120, 60))
    hline(d, 470, width=2)
    text(d, (16, 478), "MORE OF THE DAY", font("bold", 12), fill=RED)

    # ---- 10 cards: 5 cols x 2 rows ----
    cards = [
        ("BESSENT DEMANDS NVIDIA ANSWERS", "Treasury chief presses the chipmaker over China sales.", "REUTERS", "REPORTED"),
        ("FBI PROBES NCIC HACK", "Police database breach under federal investigation.", "AP", "REPORTED"),
        ("TRUMP: IRAN STRIKES MAY RESUME", "President says strikes may resume in the New Year.", "BLOOMBERG", "REPORTED"),
        ("NASDAQ FUTURES +3%", "Holiday week lifts US futures.", "WSJ", "REPORTED"),
        ("SKUBAL SIGNS $450M METS DEAL", "Two-time Cy Young winner, nine years — a record for a pitcher.", "AP", "REPORTED"),
        ("TOM JACKSON DIES AT 75", "NFL star turned broadcaster dies.", "REUTERS", "REPORTED"),
        ("STATES SUE SPACEX", "States challenge the firm's AI safety claims.", "BLOOMBERG", "REPORTED"),
        ("ANTHROPIC IPO $107.3B", "Raised at $83/share on 19 Nov; debut close $97.17.", "WSJ", "REPORTED"),
        ("POLAND: 3 MISSILES CROSSED AIRSPACE", "Warsaw says Russian Kh-101s crossed the border.", "REUTERS", "CLAIM"),
        ("RUSSIAN NUCLEAR SATELLITE WARNING", "Intel warns of Moscow's orbital weapon.", "AP", "CLAIM"),
    ]
    cw = (W - 32 - 4 * 8) // 5  # 188
    chh = 92
    cy0 = 502
    for i, (head, body, src, tag) in enumerate(cards):
        cx = 16 + (i % 5) * (cw + 8)
        cy = cy0 + (i // 5) * (chh + 8)
        d.rectangle([cx, cy, cx + cw, cy + chh], fill=CARD_BG, outline=RULE)
        lines = wrap(d, head, font("bold", 11), cw - 12)
        ly = cy + 7
        for ln in lines[:2]:
            text(d, (cx + 6, ly), ln, font("bold", 11), fill=INK)
            ly += 13
        blines = wrap(d, body, font("reg", 9), cw - 12)
        for ln in blines[:2]:
            text(d, (cx + 6, ly), ln, font("reg", 9), fill=(60, 56, 48))
            ly += 11
        sy = cy + chh - 18
        text(d, (cx + 6, sy), src, font("bold", 8), fill=MUTED)
        chip(d, cx + cw - 62, sy - 1, tag, (14, 120, 60) if tag == "REPORTED" else RED)
    hline(d, 702, width=2)

    # ---- map + ALSO ----
    mx, my, mw, mh = 16, 712, 500, 168
    d.rectangle([mx, my, mx + mw, my + mh], fill=MAP_BG)
    text(d, (mx + 8, my + 6), "THE WORLD IN 13 PINS", font("bold", 11), fill=INK)
    # rough continent blobs
    d.ellipse([mx + 18, my + 34, mx + 150, my + 120], fill=MAP_LAND)   # N America
    d.ellipse([mx + 96, my + 108, mx + 168, my + 158], fill=MAP_LAND)  # S America
    d.ellipse([mx + 200, my + 30, mx + 330, my + 96], fill=MAP_LAND)   # Eurasia
    d.ellipse([mx + 210, my + 92, mx + 300, my + 150], fill=MAP_LAND)  # Africa
    d.ellipse([mx + 350, my + 96, mx + 470, my + 150], fill=MAP_LAND)  # SE Asia / Oceania
    pins = [
        (1, 344, 56), (2, 128, 118), (3, 96, 62), (4, 258, 58),
        (5, 238, 44), (6, 300, 52), (7, 288, 74), (8, 298, 98),
        (9, 326, 80), (10, 344, 100), (11, 268, 108), (12, 286, 122),
        (13, 262, 132),
    ]
    for n, px, py in pins:
        px, py = mx + px, my + py
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=(255, 255, 255), width=1)
        tf = font("bold", 9)
        tw = d.textlength(str(n), font=tf)
        d.text((px - tw / 2, py - 6), str(n), font=tf, fill=(255, 255, 255))
    text(d, (mx + 8, my + mh - 16), "Pins 1–7: Seoul · Bridgetown · Washington · Paris · Manchester · Kyiv · Antalya",
         font("reg", 8), fill=MUTED)
    # ALSO list (right of map)
    ax = 536
    text(d, (ax, 712), "ALSO ON MONDAY", font("bold", 12), fill=RED)
    also = [
        ("Paris: 100+ back 2% billionaire tax", False),
        ("Manchester: 12,000 cleared after scare", False),
        ("Zelenskyy: 165 Russian missiles in a week", False),
        ("COP31: the day after — Antalya pact rejected", False),
        ("Israel unity talks resume", False),
        ("Gaza: two killed in Israeli strike", False),
        ("West Bank settler attacks", False),
        ("Iran war: no deal in sight", False),
        ("Lebanon seizes 264 kg explosives", False),
        ("Bahrain: Iranian strike hits plant, 2 hurt", False),
        ("Benghazi: UN probe of port attacks", True),
        ("Sudan: drones downed over Khartoum", True),
        ("DRC: fighting traps Ebola teams", False),
        ("Bangladesh: Hasina jailed if she returns", False),
        ("Seoul minister quits over AI exam chaos", False),
        ("SK Telecom −7.3%", False),
        ("China eases margin rules (cuts to 80%)", False),
        ("Seoul readies 10T-won stabilisation fund", False),
    ]
    ay = 732
    for idx, (item, is_claim) in enumerate(also):
        col = idx // 9
        row = idx % 9
        ix = ax + col * 232
        iy = ay + row * 16
        text(d, (ix, iy), f"{idx + 1}.", font("bold", 9), fill=RED)
        max_w = 224 if col == 0 else 208
        lines = wrap(d, item, font("reg", 9), max_w)
        text(d, (ix + 16, iy), lines[0], font("reg", 9), fill=INK)
        if is_claim:
            chip(d, ix + 16 + int(d.textlength(lines[0], font=font("reg", 9))) + 4,
                 iy, "CLAIM", RED)

    # ---- DATE CHECK red box ----
    bx, by, bw, bh = 16, 892, 992, 74
    d.rectangle([bx, by, bx + bw, by + bh], outline=RED, width=2, fill=(253, 238, 238))
    text(d, (bx + 10, by + 6), "DATE CHECK — LEFT OUT (NOT 23 NOVEMBER)",
         font("bold", 11), fill=RED)
    left_out = ["Democrats reach 258 (22 Nov)", "Sparta II fire (22 Nov)",
                "El Chapo Isidro captured (22 Nov)", "EU–Indonesia pact (21 Nov)",
                "Nigeria boat (21 Nov)", "ICJ Myanmar ruling (19 Nov)"]
    for i, item in enumerate(left_out):
        col = i // 3
        row = i % 3
        text(d, (bx + 10 + col * 330, by + 26 + row * 14), "✕  " + item,
             font("reg", 10), fill=INK)
    text(d, (bx + 690, by + 6), "NOT YET", font("bold", 11), fill=RED)
    not_yet = ["Dymer search continues (14 missing)", "4 House races uncalled",
               "COP32 venue not set", "WHO evacuating trapped Ebola staff"]
    for i, item in enumerate(not_yet):
        text(d, (bx + 690, by + 26 + i * 11), "·  " + item, font("reg", 9), fill=INK)

    # ---- footer ----
    text(d, (16, 978), "SOURCES: REUTERS · AP · BLOOMBERG · WSJ — REPORTED = confirmed by wires · CLAIM = one side's claim",
         font("reg", 9), fill=MUTED)
    text(d, (16, 996), "THE WORLD TODAY — a one-image summary of Monday 23 November 2026. Figures as reported on the day.",
         font("italic", 9), fill=MUTED)
    hline(d, 1016, width=2)

    out = os.environ.get("ENTRY_OUT", "entry.png")
    img.save(out, optimize=True)
    print("saved", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    render()
