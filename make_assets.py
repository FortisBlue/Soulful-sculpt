"""
Creates gift-card.png and copies + converts the treatment photo to WebP.
Run from the soulful-sculpt-v3 directory.
"""
from PIL import Image, ImageDraw, ImageFont
import math, os, shutil

OUT_DIR = r"C:\Users\Jay\soulful-sculpt-v3"
PHOTO_SRC = r"C:\Users\Jay\Downloads\ChatGPT Image May 20, 2026, 11_56_00 AM (2).png"

# ── TREATMENT PHOTO → WebP ─────────────────────────────────────────────────
img = Image.open(PHOTO_SRC).convert("RGB")
# Crop to a nice 4:3 landscape hero (take centre-crop)
w, h = img.size
target_ratio = 4 / 3
if w / h > target_ratio:
    new_w = int(h * target_ratio)
    left = (w - new_w) // 2
    img = img.crop((left, 0, left + new_w, h))
else:
    new_h = int(w / target_ratio)
    top = int((h - new_h) * 0.62)  # face/hands sit in lower 60% of portrait
    img = img.crop((0, top, w, top + new_h))

img = img.resize((660, 495), Image.LANCZOS)
img.save(os.path.join(OUT_DIR, "gift-card-hero.webp"), "WEBP", quality=88)
print("Saved gift-card-hero.webp")

# ── GIFT CARD PNG ──────────────────────────────────────────────────────────
CARD_W, CARD_H = 460, 290
RADIUS       = 18
BG_COLOR     = (235, 224, 210)      # warm beige
BORDER_COLOR = (215, 200, 182)
TEXT_COLOR   = (90, 68, 48)
ACCENT_COLOR = (158, 102, 80)       # terracotta

card = Image.new("RGBA", (CARD_W + 20, CARD_H + 20), (0, 0, 0, 0))
shadow = Image.new("RGBA", (CARD_W + 20, CARD_H + 20), (0, 0, 0, 0))
draw_sh = ImageDraw.Draw(shadow)
draw_sh.rounded_rectangle([12, 12, CARD_W + 14, CARD_H + 14],
                           radius=RADIUS, fill=(180, 160, 140, 90))
card = Image.alpha_composite(card, shadow)

draw = ImageDraw.Draw(card)
draw.rounded_rectangle([6, 6, CARD_W + 8, CARD_H + 8],
                        radius=RADIUS, fill=BG_COLOR, outline=BORDER_COLOR, width=1)

# ── Sun mark (hand-drawn style) ──────────────────────────────────────────
cx, cy = CARD_W // 2 + 6, 88
R_INNER = 11
R_OUTER = 22
RAY_COUNT = 12

def pt(angle_deg, r):
    a = math.radians(angle_deg - 90)
    return cx + r * math.cos(a), cy + r * math.sin(a)

for i in range(RAY_COUNT):
    ang = i * (360 / RAY_COUNT)
    draw.line([pt(ang, R_INNER + 3), pt(ang, R_OUTER)],
              fill=ACCENT_COLOR, width=1)

draw.ellipse([cx - R_INNER, cy - R_INNER, cx + R_INNER, cy + R_INNER],
             outline=ACCENT_COLOR, width=1, fill=None)
draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4],
             fill=ACCENT_COLOR)

# ── Text ─────────────────────────────────────────────────────────────────
# Try Windows system fonts
def load_font(names, size):
    dirs = [r"C:\Windows\Fonts"]
    for name in names:
        for d in dirs:
            p = os.path.join(d, name)
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, size)
                except Exception:
                    pass
    return ImageFont.load_default()

font_brand  = load_font(["georgia.ttf", "Georgia.ttf", "times.ttf"], 20)
font_sub    = load_font(["calibril.ttf", "georgia.ttf", "arial.ttf"], 11)

# "SOULFUL SCULPT"
brand = "SOULFUL SCULPT"
# Centre it
bbox = draw.textbbox((0, 0), brand, font=font_brand, spacing=6)
tw = bbox[2] - bbox[0]
draw.text(((CARD_W - tw) // 2 + 6, cy + 26), brand,
          font=font_brand, fill=TEXT_COLOR, spacing=3)

# Letter-spaced effect by drawing character by character
sub = "BY TENIELLE"
char_w = 8
total = len(sub) * char_w + (len(sub) - 1) * 3
x_start = (CARD_W - total) // 2 + 6
for j, ch in enumerate(sub):
    draw.text((x_start + j * (char_w + 3), cy + 54),
              ch, font=font_sub, fill=ACCENT_COLOR)

card.save(os.path.join(OUT_DIR, "gift-card.png"), "PNG")
print("Saved gift-card.png")
print("All assets ready.")
