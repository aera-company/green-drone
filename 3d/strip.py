"""Tira horizontal de renders (fundo branco) com rótulos. Uso: python3 strip.py saida.jpg img1:rot1 img2:rot2 ..."""
import sys
from PIL import Image, ImageDraw, ImageFont
out = sys.argv[1]
items = [a.split(":", 1) for a in sys.argv[2:]]
W, H = 1000, 667
f = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 28)
cols = 2 if len(items) > 2 else len(items)
rows = (len(items) + cols - 1) // cols
sheet = Image.new('RGB', (cols * W + (cols + 1) * 30, rows * (H + 50) + 30), (247, 247, 248))
d = ImageDraw.Draw(sheet)
for i, (p, lab) in enumerate(items):
    im = Image.open(p).convert('RGBA').resize((W, H))
    bg = Image.new('RGBA', (W, H), 'white'); bg.alpha_composite(im)
    x = 30 + (i % cols) * (W + 30); y = 30 + (i // cols) * (H + 50)
    sheet.paste(bg.convert('RGB'), (x, y)); d.text((x, y + H + 8), lab, fill=(26, 26, 46), font=f)
sheet = sheet.resize((sheet.width // 2, sheet.height // 2), Image.LANCZOS)
sheet.save(out, quality=88)
