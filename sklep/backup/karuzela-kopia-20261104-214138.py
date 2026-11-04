# karuzela zdjęć (post na Facebooka / tryb zdjęć na TikToku): 7 slajdów 1080x1350 z napisami
# zdjęcia źródłowe: /home/user/foto/n*.png (zdjęcia produktu ze sklepu, 2048x2048, ../zdjecia_produktu.json)
import glob, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
def font(pat):
    return sorted(p for p in glob.glob('/usr/share/fonts/**/*',recursive=True) if pat in p.split('/')[-1] and p.endswith('.otf'))[0]
SB=font('P052-Bold'); SI=font('P052-Italic')
S='/home/user/foto/'; W,H=1080,1350
# (plik, przesunięcie kadru w poziomie 0..1, gdzie napis, tytuł, podtytuł)
SL=[
 ('n31',0.5,'top','Wygląda jak żywa','Girlanda cedrowa, która nie gubi igieł'),
 ('n2',0.55,'bottom','Gęste gałązki','w naturalnym kolorze cedru'),
 ('n13',0.45,'top','Na schody…','…kominek, drzwi albo okno'),
 ('n21',0.5,'bottom','Na stół wigilijny','jako gęsty zielony bieżnik'),
 ('n15',0.6,'top','Wyjmujesz i rozkładasz','gotowe w kilka minut'),
 ('n5',0.5,'bottom','Zestaw Cały dom','4 × 1,5 m, starczy na drzwi albo schody'),
]
def base(name,fx):
    im=Image.open(S+name+'.png').convert('RGB'); im=im.resize((H,H),Image.LANCZOS)
    x=int((H-W)*fx); return im.crop((x,0,x+W,H))
def shade(im,where,h=580,a=215):
    g=Image.new('L',(1,h))
    for i in range(h): g.putpixel((0,i),int(a*(1-i/h)**1.6) if where=='top' else int(a*(i/h)**1.6))
    g=g.resize((W,h)); blk=Image.new('RGB',(W,h),(0,0,0))
    y=0 if where=='top' else H-h
    reg=im.crop((0,y,W,y+h)); reg=Image.composite(blk,reg,g); im.paste(reg,(0,y)); return im
def text(d,y,t,f,fill):
    w=d.textlength(t,font=f); x=(W-w)/2
    for dx,dy in ((2,3),(0,3),(3,2)): d.text((x+dx,y+dy),t,font=f,fill=(0,0,0))
    d.text((x,y),t,font=f,fill=fill)
def slide(i,name,fx,where,t1,t2):
    im=shade(base(name,fx),where); d=ImageDraw.Draw(im)
    f1=ImageFont.truetype(SB,80); f2=ImageFont.truetype(SI,52)
    y=90 if where=='top' else H-260
    text(d,y,t1,f1,(255,255,255)); text(d,y+108,t2,f2,(255,242,220))
    im.save(f'karuzela_{i}.jpg',quality=92)
def koniec(i):
    im=base('n6',0.5); im=ImageEnhance.Brightness(im.filter(ImageFilter.GaussianBlur(7))).enhance(0.32); d=ImageDraw.Draw(im)
    f1=ImageFont.truetype(SB,66); f2=ImageFont.truetype(SI,46); f3=ImageFont.truetype(SB,58)
    rows=[('Zestaw Kominek: 2 × 1,5 m',f2,(255,255,255)),('Zestaw Cały dom: 4 × 1,5 m',f2,(255,255,255)),('',f2,None),
          ('Darmowa dostawa',f1,(255,255,255)),('30 dni na zwrot',f1,(255,255,255)),('',f2,None),
          ('Zamów do 10 grudnia,',f2,(245,232,205)),('zdąży na święta',f2,(245,232,205)),('',f2,None),('lesnykominek.pl',f3,(245,225,180))]
    y=250
    for t,f,c in rows:
        if t: text(d,y,t,f,c)
        y+=int(f.size*1.45) if t else 40
    im.save(f'karuzela_{i}.jpg',quality=92)
if __name__=='__main__':
    for i,s in enumerate(SL,1): slide(i,*s)
    koniec(len(SL)+1)
