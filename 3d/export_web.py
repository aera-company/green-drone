"""PNG -> WebP para a rota /motion-proof. Uso: python3 3d/export_web.py desktop|mobile [qualidade]"""
import sys, os, glob
from PIL import Image
fmt = sys.argv[1]; q = int(sys.argv[2]) if len(sys.argv) > 2 else 76
src = f"3d/renders/shot_{fmt}"; dst = f"public/motion-proof/{fmt}"
os.makedirs(dst, exist_ok=True)
fs = sorted(glob.glob(os.path.join(src, "f*.png")))
total = 0
for i, f in enumerate(fs):
    out = os.path.join(dst, f"f{i:04d}.webp")
    Image.open(f).convert("RGB").save(out, "WEBP", quality=q, method=6)
    total += os.path.getsize(out)
print(fmt, len(fs), "quadros,", round(total / 1e6, 1), "MB")
if fmt == "desktop":
    for name, idx in (("reveal", 0), ("turn", 88), ("dark", 150)):
        Image.open(fs[idx]).convert("RGB").save(f"public/motion-proof/still-{name}.webp", "WEBP", quality=82, method=6)
