import sys
from PIL import Image
m=Image.open('../public/media/drone-cutout.png').convert('RGBA')
r=Image.open(sys.argv[1]).convert('RGBA').resize(m.size)
W,H=m.size
sheet=Image.new('RGB',(W*2,H),'white')
a=Image.new('RGBA',m.size,'white'); a.alpha_composite(m); sheet.paste(a.convert('RGB'),(0,0))
b=Image.new('RGBA',m.size,'white'); b.alpha_composite(r); sheet.paste(b.convert('RGB'),(W,0))
sheet.save(sys.argv[2],quality=88)
