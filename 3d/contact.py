"""Folha de contato dos quadros de uma pasta. Uso: python3 contact.py pasta saida.jpg [colunas]"""
import sys, glob, os
from PIL import Image, ImageDraw, ImageFont
d, out = sys.argv[1], sys.argv[2]; cols = int(sys.argv[3]) if len(sys.argv) > 3 else 4
fs = sorted(glob.glob(os.path.join(d, "f*.png")))
ims = [Image.open(f).convert("RGB") for f in fs]
w, h = ims[0].size; tw = 480; th = int(h * tw / w)
f = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 18)
rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (cols * (tw + 10) + 10, rows * (th + 34) + 10), (30, 30, 34))
dr = ImageDraw.Draw(sheet)
for i, (im, fn) in enumerate(zip(ims, fs)):
    x = 10 + (i % cols) * (tw + 10); y = 10 + (i // cols) * (th + 34)
    sheet.paste(im.resize((tw, th)), (x, y)); dr.text((x, y + th + 6), os.path.basename(fn), fill=(220, 220, 220), font=f)
sheet.save(out, quality=85)
