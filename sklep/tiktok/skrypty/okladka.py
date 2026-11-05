# okładka strony na Facebooku 1640x624; napisy na środku u góry (mieszczą się w kadrze na telefonie, z dala od zdjęcia profilowego w lewym dolnym rogu)
# źródło: o2.png = hf_20261105_062410_382d5835-5303-4534-a79e-f10d07a9db36.png (seedream_v5_pro, 21:9, referencja packshot 94e71150)
import glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter
def font(pat): return sorted(p for p in glob.glob('/usr/share/fonts/**/*',recursive=True) if pat in p.split('/')[-1] and p.endswith('.otf'))[0]
SB=font('P052-Bold'); SI=font('P052-Italic')
W,H=1640,624
src=Image.open('o2.png').convert('RGB'); s=W/src.width; src=src.resize((W,int(src.height*s)),Image.LANCZOS)
base=src.crop((0,0,W,H)); base.save('okladka_bez_napisu.jpg',quality=93)
im=base.convert('RGBA')
glow=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(glow).ellipse((330,-80,1310,250),fill=(0,0,0,120)); glow=glow.filter(ImageFilter.GaussianBlur(50))
im=Image.alpha_composite(im,glow); d=ImageDraw.Draw(im)
def t(y,txt,f,c):
    w=d.textlength(txt,font=f); x=(W-w)/2
    for dx,dy in ((2,3),(0,3),(3,2)): d.text((x+dx,y+dy),txt,font=f,fill=(0,0,0,200))
    d.text((x,y),txt,font=f,fill=c)
t(14,'Leśny Kominek',ImageFont.truetype(SB,66),(255,255,255,255))
t(96,'Girlanda cedrowa, która wygląda jak żywa',ImageFont.truetype(SI,36),(255,240,215,255))
t(144,'Darmowa dostawa  ·  30 dni na zwrot  ·  lesnykominek.pl',ImageFont.truetype(SI,27),(245,225,180,255))
im.convert('RGB').save('okladka_facebook.jpg',quality=93)
