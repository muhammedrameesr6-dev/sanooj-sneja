#!/usr/bin/env python3
import sys
sys.path.insert(0, '/Users/rameesr/Library/Python/3.9/lib/python/site-packages')
from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageDraw, ImageFont
import math
import os

print("Starting photo editing and optimization...")

def apply_warm_tone(img, r_boost=1.06, g_boost=1.02, b_reduce=0.95):
    """Adds a romantic warm golden glow to the image."""
    r, g, b = img.split()
    r = r.point(lambda i: min(255, int(i * r_boost)))
    g = g.point(lambda i: min(255, int(i * g_boost)))
    b = b.point(lambda i: min(255, int(i * b_reduce)))
    return Image.merge('RGB', (r, g, b))

def apply_vignette(img, intensity=0.35, roundness=1.0):
    """Applies a soft natural vignette to draw focus to the center."""
    w, h = img.size
    mask = Image.new('L', (w, h), 255)
    cx, cy = w / 2, h / 2
    max_dist = math.sqrt((w/2)**2 + (h/2)**2)
    
    # Fast vignette using radial gradient in low-res then scaling up
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
    
    # Darken with black overlay
    black = Image.new('RGB', (w, h), (18, 22, 16))
    return Image.composite(img, black, vmask)

def enhance_photo(img, color=1.08, contrast=1.06, brightness=1.02, sharpness=1.15):
    """Enhance vibrancy, contrast, brightness, and sharpness."""
    if color != 1.0:
        img = ImageEnhance.Color(img).enhance(color)
    if brightness != 1.0:
        img = ImageEnhance.Brightness(img).enhance(brightness)
    if contrast != 1.0:
        img = ImageEnhance.Contrast(img).enhance(contrast)
    if sharpness != 1.0:
        img = ImageEnhance.Sharpness(img).enhance(sharpness)
    return img

os.makedirs('assets', exist_ok=True)

# -------------------------------------------------------------
# 1. HERO.JPG (From temple_traditional.jpg)
# -------------------------------------------------------------
print("1. Processing hero.jpg (Traditional Temple Attire)...")
im_temple = Image.open('photos_raw/temple_traditional.jpg').convert('RGB')
w, h = im_temple.size

# Crop so Sanooj & Sneja are centered with nice proportions (chest to above head)
# Keep temple lights in background, cut bottom passers-by
crop_box = (int(w * 0.04), int(h * 0.10), int(w * 0.96), int(h * 0.90))
im_hero_crop = im_temple.crop(crop_box)
im_hero = im_hero_crop.resize((1200, 1600), Image.Resampling.LANCZOS)
im_hero = apply_warm_tone(im_hero, r_boost=1.08, g_boost=1.03, b_reduce=0.92)
im_hero = enhance_photo(im_hero, color=1.12, contrast=1.08, brightness=1.03, sharpness=1.2)
im_hero = apply_vignette(im_hero, intensity=0.45, roundness=0.85)

# Add subtle bottom shadow gradient for hero text overlay readability
hw, hh = im_hero.size
grad = Image.new('RGBA', (hw, hh), (0, 0, 0, 0))
gdraw = ImageDraw.Draw(grad)
for y in range(int(hh * 0.55), hh):
    ratio = max(0.0, min(1.0, (y - hh * 0.55) / (hh * 0.45)))
    alpha = int(210 * (ratio ** 1.3))
    gdraw.line([(0, y), (hw, y)], fill=(20, 28, 18, alpha))
for y in range(0, int(hh * 0.25)):
    ratio = max(0.0, min(1.0, (int(hh * 0.25) - y) / (hh * 0.25)))
    alpha = int(120 * (ratio ** 1.2))
    gdraw.line([(0, y), (hw, y)], fill=(15, 20, 14, alpha))

im_hero.paste(grad, (0, 0), grad)
im_hero.save('assets/hero.jpg', 'JPEG', quality=94)
print("Saved assets/hero.jpg")

# -------------------------------------------------------------
# 2. GALLERY-4.JPG (Couple Tap-to-Reveal: Watercolor portrait)
# -------------------------------------------------------------
print("2. Processing gallery-4.jpg (Watercolor Portrait)...")
im_water = Image.open('photos_raw/watercolor.jpg').convert('RGB')
ww, wh = im_water.size

# Target 3:4 ratio for .couple-photo (e.g. 900 x 1200)
# Center around couple
target_ratio = 3.0 / 4.0
curr_ratio = ww / wh
if curr_ratio < target_ratio:
    # Need to crop height
    new_h = int(ww / target_ratio)
    top = int((wh - new_h) * 0.45) # Keep couple centered
    im_water_crop = im_water.crop((0, top, ww, top + new_h))
else:
    new_w = int(wh * target_ratio)
    left = int((ww - new_w) * 0.5)
    im_water_crop = im_water.crop((left, 0, left + new_w, wh))

im_water_out = im_water_crop.resize((900, 1200), Image.Resampling.LANCZOS)
im_water_out = enhance_photo(im_water_out, color=1.06, contrast=1.05, brightness=1.01, sharpness=1.15)
im_water_out.save('assets/gallery-4.jpg', 'JPEG', quality=95)
print("Saved assets/gallery-4.jpg")

# -------------------------------------------------------------
# 3. GALLERY-3.JPG (Photo Strip after Countdown: Indoor romantic gaze)
# -------------------------------------------------------------
print("3. Processing gallery-3.jpg (Romantic Gaze)...")
im_rom = Image.open('photos_raw/indoor_romantic.jpg').convert('RGB')
rw, rh = im_rom.size

# Landscape strip crop (around couple's upper body and expressions)
# Target ratio ~ 16:10 or 3:2
crop_top = int(rh * 0.12)
crop_bottom = int(rh * 0.78)
crop_h = crop_bottom - crop_top
crop_w = int(crop_h * 1.5)
crop_left = max(0, int((rw - crop_w) * 0.5))
crop_right = min(rw, crop_left + crop_w)

im_rom_crop = im_rom.crop((crop_left, crop_top, crop_right, crop_bottom))
im_rom_out = im_rom_crop.resize((1200, 800), Image.Resampling.LANCZOS)
im_rom_out = apply_warm_tone(im_rom_out, r_boost=1.05, g_boost=1.02, b_reduce=0.95)
im_rom_out = enhance_photo(im_rom_out, color=1.10, contrast=1.07, brightness=1.02, sharpness=1.15)
im_rom_out = apply_vignette(im_rom_out, intensity=0.25)
im_rom_out.save('assets/gallery-3.jpg', 'JPEG', quality=94)
print("Saved assets/gallery-3.jpg")

# -------------------------------------------------------------
# 4. GALLERY-2.JPG (Photo Strip after Save The Date: Outdoor close-up)
# -------------------------------------------------------------
print("4. Processing gallery-2.jpg (Outdoor Sunshine Close-up)...")
im_out = Image.open('photos_raw/outdoor_closeup.jpg').convert('RGB')
ow, oh = im_out.size

crop_top = int(oh * 0.10)
crop_bottom = int(oh * 0.85)
crop_h = crop_bottom - crop_top
crop_w = int(crop_h * 1.45)
crop_left = max(0, int((ow - crop_w) * 0.5))
crop_right = min(ow, crop_left + crop_w)

im_out_crop = im_out.crop((crop_left, crop_top, crop_right, crop_bottom))
im_out_out = im_out_crop.resize((1200, 800), Image.Resampling.LANCZOS)
im_out_out = apply_warm_tone(im_out_out, r_boost=1.04, g_boost=1.02, b_reduce=0.96)
im_out_out = enhance_photo(im_out_out, color=1.12, contrast=1.06, brightness=1.02, sharpness=1.2)
im_out_out = apply_vignette(im_out_out, intensity=0.20)
im_out_out.save('assets/gallery-2.jpg', 'JPEG', quality=94)
print("Saved assets/gallery-2.jpg")

# -------------------------------------------------------------
# 5. GALLERY-1.JPG (Photo Banner above Family: Temple with pattern shirt)
# -------------------------------------------------------------
print("5. Processing gallery-1.jpg (Temple Pattern Attire)...")
im_pat = Image.open('photos_raw/temple_pattern.jpg').convert('RGB')
pw, ph = im_pat.size

crop_top = int(ph * 0.18)
crop_bottom = int(ph * 0.78)
crop_h = crop_bottom - crop_top
crop_w = int(crop_h * 1.8)
crop_left = max(0, int((pw - crop_w) * 0.5))
crop_right = min(pw, crop_left + crop_w)

im_pat_crop = im_pat.crop((crop_left, crop_top, crop_right, crop_bottom))
im_pat_out = im_pat_crop.resize((1200, 660), Image.Resampling.LANCZOS)
im_pat_out = apply_warm_tone(im_pat_out, r_boost=1.06, g_boost=1.02, b_reduce=0.94)
im_pat_out = enhance_photo(im_pat_out, color=1.10, contrast=1.06, brightness=1.03, sharpness=1.18)
im_pat_out = apply_vignette(im_pat_out, intensity=0.30)
im_pat_out.save('assets/gallery-1.jpg', 'JPEG', quality=94)
print("Saved assets/gallery-1.jpg")

# -------------------------------------------------------------
# 6. SOFT-BG.JPG (Closing Section Background)
# -------------------------------------------------------------
print("6. Processing soft-bg.jpg...")
im_soft = Image.open('photos_raw/temple_traditional.jpg').convert('RGB')
im_soft = im_soft.resize((900, 1200), Image.Resampling.BILINEAR)
im_soft = im_soft.filter(ImageFilter.GaussianBlur(radius=28))
im_soft = apply_warm_tone(im_soft, r_boost=1.15, g_boost=1.05, b_reduce=0.85)
# Add warm ivory wash
tint = Image.new('RGB', (900, 1200), (245, 238, 224))
im_soft = Image.blend(im_soft, tint, 0.45)
im_soft.save('assets/soft-bg.jpg', 'JPEG', quality=90)
print("Saved assets/soft-bg.jpg")

# -------------------------------------------------------------
# 7. OG.JPG (Social Media Preview 1200 x 630)
# -------------------------------------------------------------
print("7. Processing og.jpg (Open Graph Preview)...")
og_canvas = Image.new('RGB', (1200, 630), (250, 247, 242)) # Ivory background

# Left side couple photo
og_photo = Image.open('photos_raw/temple_traditional.jpg').convert('RGB')
pw, ph = og_photo.size
# Crop upper body of couple
pcrop = og_photo.crop((int(pw * 0.05), int(ph * 0.12), int(pw * 0.95), int(ph * 0.88)))
pcrop = pcrop.resize((560, 630), Image.Resampling.LANCZOS)
pcrop = apply_warm_tone(pcrop, r_boost=1.08, g_boost=1.03, b_reduce=0.92)
pcrop = enhance_photo(pcrop, color=1.12, contrast=1.08, brightness=1.03, sharpness=1.2)

# Blend right edge into ivory
fade_width = 120
alpha_mask = Image.new('L', (560, 630), 255)
for x in range(560 - fade_width, 560):
    val = int(255 * (1.0 - (x - (560 - fade_width)) / fade_width))
    for y in range(630):
        alpha_mask.putpixel((x, y), val)

og_canvas.paste(pcrop, (0, 0), alpha_mask)

# Right side decorative elements and typography
draw = ImageDraw.Draw(og_canvas)

# Decorative borders
draw.rectangle([(20, 20), (1180, 610)], outline=(192, 155, 90), width=2) # Gold border
draw.rectangle([(26, 26), (1174, 604)], outline=(225, 218, 204), width=1)

# Try loading system font, fallback to default
font_title = None
font_sub = None
font_names = None
font_date = None

font_paths = [
    "/System/Library/Fonts/Supplemental/Georgia.ttf",
    "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
    "/System/Library/Fonts/Times.ttc"
]
for p in font_paths:
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

# Text positioning
rx = 620
draw.text((rx + 40, 120), "WEDDING INVITATION", fill=(61, 82, 48), font=font_title)
# Divider line
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

print("All photos edited and generated successfully!")
