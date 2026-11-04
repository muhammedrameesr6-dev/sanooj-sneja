#!/usr/bin/env python3
import sys
sys.path.insert(0, '/Users/rameesr/Library/Python/3.9/lib/python/site-packages')
from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageDraw, ImageFont
import math
import os

print("Updating photos with new user assignments...")

def apply_warm_tone(img, r_boost=1.05, g_boost=1.02, b_reduce=0.95):
    r, g, b = img.split()
    r = r.point(lambda i: min(255, int(i * r_boost)))
    g = g.point(lambda i: min(255, int(i * g_boost)))
    b = b.point(lambda i: min(255, int(i * b_reduce)))
    return Image.merge('RGB', (r, g, b))

def enhance_photo(img, color=1.08, contrast=1.06, brightness=1.02, sharpness=1.15):
    if color != 1.0:
        img = ImageEnhance.Color(img).enhance(color)
    if brightness != 1.0:
        img = ImageEnhance.Brightness(img).enhance(brightness)
    if contrast != 1.0:
        img = ImageEnhance.Contrast(img).enhance(contrast)
    if sharpness != 1.0:
        img = ImageEnhance.Sharpness(img).enhance(sharpness)
    return img

def apply_vignette(img, intensity=0.35, roundness=1.0):
    w, h = img.size
    vw, vh = int(w / 4), int(h / 4)
    vmask = Image.new('L', (vw, vh), 255)
    vcx, vcy = vw / 2, vh / 2
    vmax = math.sqrt(vcx**2 + vcy**2)
    pixels = vmask.load()
    for y in range(vh):
        for x in range(vw):
            dx = (x - vcx)
            dy = (y - vcy) / roundness
            d = math.sqrt(dx*dx + dy*dy) / vmax
            if d > 0.4:
                factor = 1.0 - ((d - 0.4) / 0.6) * intensity
                factor = max(0.0, min(1.0, factor))
                pixels[x, y] = int(255 * factor)
            else:
                pixels[x, y] = 255
    vmask = vmask.resize((w, h), Image.Resampling.BILINEAR)
    black = Image.new('RGB', (w, h), (18, 22, 16))
    return Image.composite(img, black, vmask)

# -------------------------------------------------------------
# 1. HERO.JPG -> WATERCOLOR ARTWORK (as requested: "front pageil ee image")
# -------------------------------------------------------------
print("1. Creating assets/hero.jpg from watercolor artwork...")
im_water = Image.open('photos_raw/watercolor.jpg').convert('RGB')
ww, wh = im_water.size

# Target 1200 x 1600 (3:4 ratio)
# Sanooj & Sneja are centered with watercolor splashes around
target_w, target_h = 1200, 1600
# Resize proportionally
im_hero = im_water.resize((target_w, target_h), Image.Resampling.LANCZOS)
im_hero = enhance_photo(im_hero, color=1.08, contrast=1.06, brightness=1.02, sharpness=1.2)

# Add bottom gradient overlay so hero names ("Sanooj & Sneja") have great readability
grad = Image.new('RGBA', (target_w, target_h), (0, 0, 0, 0))
gdraw = ImageDraw.Draw(grad)

# Soft darkening starting below their faces (from y=62% downwards)
start_y = int(target_h * 0.60)
for y in range(start_y, target_h):
    ratio = max(0.0, min(1.0, (y - start_y) / (target_h - start_y)))
    alpha = int(215 * (ratio ** 1.3))
    gdraw.line([(0, y), (target_w, y)], fill=(22, 28, 20, alpha))

# Very subtle top gradient (for any header/verse)
top_y = int(target_h * 0.22)
for y in range(0, top_y):
    ratio = max(0.0, min(1.0, (top_y - y) / top_y))
    alpha = int(95 * (ratio ** 1.2))
    gdraw.line([(0, y), (target_w, y)], fill=(20, 26, 18, alpha))

im_hero.paste(grad, (0, 0), grad)
im_hero.save('assets/hero.jpg', 'JPEG', quality=95)
print("Saved assets/hero.jpg")

# -------------------------------------------------------------
# 2. GALLERY-4.JPG -> SUNSET OUTDOOR (as requested: "Tap to revel")
# -------------------------------------------------------------
print("2. Creating assets/gallery-4.jpg from sunset outdoor photoshoot...")
im_sunset = Image.open('photos_raw/sunset_outdoor.jpg').convert('RGB')
sw, sh = im_sunset.size

# Target 900 x 1200 (exact 3:4 aspect ratio for .couple-photo)
# Crop centered on both from thigh up, keeping the warm sky and rim lighting
target_ratio = 3.0 / 4.0
curr_ratio = sw / sh
if curr_ratio > target_ratio:
    crop_w = int(sh * target_ratio)
    left = int((sw - crop_w) * 0.5)
    im_sunset_crop = im_sunset.crop((left, 0, left + crop_w, sh))
else:
    crop_h = int(sw / target_ratio)
    top = int((sh - crop_h) * 0.25) # keep head and upper body
    im_sunset_crop = im_sunset.crop((0, top, sw, top + crop_h))

im_sunset_out = im_sunset_crop.resize((900, 1200), Image.Resampling.LANCZOS)
im_sunset_out = apply_warm_tone(im_sunset_out, r_boost=1.06, g_boost=1.02, b_reduce=0.94)
im_sunset_out = enhance_photo(im_sunset_out, color=1.12, contrast=1.08, brightness=1.03, sharpness=1.2)
im_sunset_out.save('assets/gallery-4.jpg', 'JPEG', quality=95)
print("Saved assets/gallery-4.jpg (Tap to reveal)")

# -------------------------------------------------------------
# 3. GALLERY-1.JPG -> TRADITIONAL KASAVU TEMPLE
# -------------------------------------------------------------
print("3. Updating assets/gallery-1.jpg with traditional kasavu temple photo...")
im_temple = Image.open('photos_raw/temple_traditional.jpg').convert('RGB')
tw, th = im_temple.size

# Wide banner crop (1200 x 660)
crop_top = int(th * 0.12)
crop_bottom = int(th * 0.76)
crop_h = crop_bottom - crop_top
crop_w = int(crop_h * 1.8)
crop_left = max(0, int((tw - crop_w) * 0.5))
crop_right = min(tw, crop_left + crop_w)

im_temple_crop = im_temple.crop((crop_left, crop_top, crop_right, crop_bottom))
im_temple_out = im_temple_crop.resize((1200, 660), Image.Resampling.LANCZOS)
im_temple_out = apply_warm_tone(im_temple_out, r_boost=1.06, g_boost=1.02, b_reduce=0.94)
im_temple_out = enhance_photo(im_temple_out, color=1.10, contrast=1.06, brightness=1.02, sharpness=1.18)
im_temple_out = apply_vignette(im_temple_out, intensity=0.30)
im_temple_out.save('assets/gallery-1.jpg', 'JPEG', quality=94)
print("Saved assets/gallery-1.jpg")

# -------------------------------------------------------------
# 4. OG.JPG -> UPDATE WITH SUNSET OUTDOOR OR WATERCOLOR
# -------------------------------------------------------------
print("4. Updating og.jpg with new couple photo...")
og_canvas = Image.new('RGB', (1200, 630), (250, 247, 242))

og_photo = Image.open('photos_raw/sunset_outdoor.jpg').convert('RGB')
pw, ph = og_photo.size
pcrop = og_photo.crop((int(pw * 0.05), int(ph * 0.08), int(pw * 0.95), int(ph * 0.85)))
pcrop = pcrop.resize((560, 630), Image.Resampling.LANCZOS)
pcrop = apply_warm_tone(pcrop, r_boost=1.06, g_boost=1.02, b_reduce=0.94)
pcrop = enhance_photo(pcrop, color=1.12, contrast=1.08, brightness=1.03, sharpness=1.2)

fade_width = 120
alpha_mask = Image.new('L', (560, 630), 255)
for x in range(560 - fade_width, 560):
    val = int(255 * (1.0 - (x - (560 - fade_width)) / fade_width))
    for y in range(630):
        alpha_mask.putpixel((x, y), val)

og_canvas.paste(pcrop, (0, 0), alpha_mask)

draw = ImageDraw.Draw(og_canvas)
draw.rectangle([(20, 20), (1180, 610)], outline=(192, 155, 90), width=2)
draw.rectangle([(26, 26), (1174, 604)], outline=(225, 218, 204), width=1)

font_title, font_sub, font_names, font_date = None, None, None, None
for p in ["/System/Library/Fonts/Supplemental/Georgia.ttf", "/System/Library/Fonts/Supplemental/Times New Roman.ttf", "/System/Library/Fonts/Times.ttc"]:
    if os.path.exists(p):
        try:
            font_title = ImageFont.truetype(p, 24)
            font_names = ImageFont.truetype(p, 58)
            font_sub = ImageFont.truetype(p, 22)
            font_date = ImageFont.truetype(p, 26)
            break
        except Exception:
            pass

if not font_title:
    font_title = ImageFont.load_default()
    font_names = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_date = ImageFont.load_default()

rx = 620
draw.text((rx + 40, 120), "WEDDING INVITATION", fill=(61, 82, 48), font=font_title)
draw.line([(rx + 40, 165), (rx + 160, 165)], fill=(192, 155, 90), width=2)
draw.text((rx + 40, 195), "Sanooj & Sneja", fill=(30, 36, 32), font=font_names)
draw.text((rx + 40, 290), "Monday, December 28, 2026", fill=(192, 155, 90), font=font_date)
draw.text((rx + 40, 335), "Muhurtham: 11:45 AM – 12:30 PM", fill=(90, 99, 88), font=font_sub)
draw.line([(rx + 40, 390), (rx + 480, 390)], fill=(225, 218, 204), width=1)
draw.text((rx + 40, 420), "Sree Sundareswara Temple", fill=(45, 55, 40), font=font_sub)
draw.text((rx + 40, 455), "Talap, Kannur", fill=(90, 99, 88), font=font_sub)
draw.text((rx + 40, 515), "Reception to follow · Kannur & Vatakara", fill=(140, 155, 126), font=font_sub)

og_canvas.save('og.jpg', 'JPEG', quality=95)
print("Saved og.jpg")

print("All updates completed successfully!")
