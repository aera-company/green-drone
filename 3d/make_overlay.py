import sys
from PIL import Image
m=Image.open('../public/media/drone-cutout.png').convert('RGBA')
bg=Image.new('RGBA',m.size,'white'); bg.alpha_composite(m)
a=Image.open('renders/_sil.png').split()[3]
red=Image.new('RGBA',m.size,(255,0,0,255))
bg.paste(red,(0,0),a.point(lambda v:int(v*0.5)))
bg.convert('RGB').save(sys.argv[1] if len(sys.argv)>1 else 'renders/_overlay.jpg',quality=88)
