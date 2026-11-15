import base64, os, re
from PIL import Image, ImageDraw

ROOT = os.getcwd()
with open(os.path.join(ROOT, "icon-src", "photo_base64.txt")) as f:
    img_bytes = base64.b64decode(f.read())
tmp = os.path.join(ROOT, "icon-src", "photo.jpg")
with open(tmp, "wb") as f:
    f.write(img_bytes)

im = Image.open(tmp).convert("RGB")
# Verified square face crop for this photo (2048x1152): box 391,76-1241,926
crop = im.crop((391, 76, 1241, 926))
base = crop.resize((1024, 1024), Image.LANCZOS)
RES = os.path.join(ROOT, "androidApp", "src", "main", "res")

def circle(img):
    s = img.size[0]
    mask = Image.new("L", (s * 4, s * 4), 0)
    d = ImageDraw.Draw(mask); d.ellipse((0, 0, s * 4, s * 4), fill=255)
    mask = mask.resize((s, s), Image.LANCZOS)
    out = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    out.paste(img.convert("RGB"), (0, 0), mask)
    return out

densities = {"mdpi": (48, 108), "hdpi": (72, 162), "xhdpi": (96, 216), "xxhdpi": (144, 324), "xxxhdpi": (192, 432)}
for name, (px, fg) in densities.items():
    d = os.path.join(RES, f"mipmap-{name}")
    sq = base.resize((px, px), Image.LANCZOS)
    sq.save(os.path.join(d, "ic_launcher.webp"), "WEBP", quality=95)
    circle(sq).save(os.path.join(d, "ic_launcher_round.webp"), "WEBP", quality=95)
    fimg = base.resize((fg, fg), Image.LANCZOS)
    fimg.save(os.path.join(d, "ic_launcher_foreground.webp"), "WEBP", quality=95)
    fimg.save(os.path.join(d, "ic_launcher_round_foreground.webp"), "WEBP", quality=95)
    print(name, "done")

base.resize((432, 432), Image.LANCZOS).save(os.path.join(RES, "drawable", "app_icon.png"))
cr = os.path.join(ROOT, "composeApp", "src", "commonMain", "composeResources", "drawable")
base.resize((432, 432), Image.LANCZOS).convert("RGBA").save(os.path.join(cr, "app_icon.png"))
circle(base.resize((432, 432), Image.LANCZOS)).save(os.path.join(cr, "circle_app_icon.png"))
base.resize((512, 512), Image.LANCZOS).save(os.path.join(ROOT, "fastlane", "metadata", "android", "en-US", "images", "icon.png"))

# Drop monochrome from adaptive icons so the photo shows instead of a themed silhouette
for p in ["ic_launcher.xml", "ic_launcher_round.xml"]:
    fp = os.path.join(RES, "mipmap-anydpi-v26", p)
    lines = [l for l in open(fp) if "monochrome" not in l]
    open(fp, "w").writelines(lines)
print("all icons generated")
