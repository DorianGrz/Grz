# karuzela zdjęć: 5 slajdów (4 zdjęcia + oferta)
# python3 karuzela.py     -> Facebook 1080x1350 (karuzela_N.jpg)
# python3 karuzela.py tt  -> TikTok 1080x1920, napis nad zdjęciem w strefie bezpiecznej (karuzela_tt_N.jpg)
# ostatni slajd w 2 wersjach: z kodem START10 (do 8.11) i _bez_kodu (od 9.11)
# zdjęcia źródłowe: /home/user/foto/n*.png (zdjęcia produktu ze sklepu, 2048x2048, ../zdjecia_produktu.json)
import glob, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
def font(pat):
    return sorted(p for p in glob.glob('/usr/share/fonts/**/*',recursive=True) if pat in p.split('/')[-1] and p.endswith('.otf'))[0]
SB=font('P052-Bold'); SI=font('P052-Italic')
S='/home/user/foto/'; W,H=1080,1350
# (plik, przesunięcie kadru w poziomie 0..1, gdzie napis, tytuł, podtytuł)
SL=[
 ('n31',0.5,'bottom','Wygląda jak żywa','Girlanda cedrowa, która nie gubi igieł'),
 ('n2',0.55,'bottom','Gęste gałązki','w naturalnym kolorze cedru'),
 ('n13',0.45,'top','Na schody…','…kominek, drzwi albo okno'),
 ('n21',0.5,'bottom','Na stół wigilijny','jako gęsty zielony bieżnik'),
]
KOD='Kod START10: 10% taniej do 8.11'
def oferta(f1,f2,f3,kod):
    r=[('Zestaw Kominek: 2 × 1,5 m',f2,(255,255,255)),('Zestaw Cały dom: 4 × 1,5 m',f2,(255,255,255)),('',f2,None),
       ('Darmowa dostawa',f1,(255,255,255)),('30 dni na zwrot',f1,(255,255,255)),('',f2,None),
       ('Zamów do 10 grudnia,',f2,(245,232,205)),('zdąży na święta',f2,(245,232,205)),('',f2,None)]
    if kod: r+=[(KOD,f1.font_variant(size=int(f1.size*0.70)),(255,214,120)),('',f2,None)]
    return r+[('lesnykominek.pl',f3,(245,225,180))]
def base(name,fx):
    im=Image.open(S+name+'.png').convert('RGB'); im=im.resize((H,H),Image.LANCZOS)
    x=int((H-W)*fx); return im.crop((x,0,x+W,H))
def shade(im,where,h=580,a=215):
    g=Image.new('L',(1,h))
    for i in range(h): g.putpixel((0,i),int(a*(1-i/h)**1.6) if where=='top' else int(a*(i/h)**1.6))
    g=g.resize((W,h)); blk=Image.new('RGB',(W,h),(0,0,0))
    y=0 if where=='top' else H-h
    reg=im.crop((0,y,W,y+h)); reg=Image.composite(blk,reg,g); im.paste(reg,(0,y)); return im
def text(d,y,t,f,fill,w0=W):
    w=d.textlength(t,font=f); x=(w0-w)/2
    for dx,dy in ((2,3),(0,3),(3,2)): d.text((x+dx,y+dy),t,font=f,fill=(0,0,0))
    d.text((x,y),t,font=f,fill=fill)
def wiersze(d,y,rows,w0,gap):
    for t,f,c in rows:
        if t: text(d,y,t,f,c,w0)
        y+=int(f.size*1.45) if t else gap
# --- Facebook 1080x1350
def slide(i,name,fx,where,t1,t2):
    im=shade(base(name,fx),where); d=ImageDraw.Draw(im)
    f1=ImageFont.truetype(SB,80); f2=ImageFont.truetype(SI,52)
    # w kolażu na tablicy Facebook przycina zdjęcia do kwadratu (ok. 135 px z góry i z dołu), więc napis bliżej środka
    y=170 if where=='top' else H-345
    text(d,y,t1,f1,(255,255,255)); text(d,y+108,t2,f2,(255,242,220))
    im.save(f'karuzela_{i}.jpg',quality=92)
def koniec(i,kod):
    im=base('n6',0.5); im=ImageEnhance.Brightness(im.filter(ImageFilter.GaussianBlur(7))).enhance(0.32); d=ImageDraw.Draw(im)
    f1=ImageFont.truetype(SB,66); f2=ImageFont.truetype(SI,46); f3=ImageFont.truetype(SB,58)
    wiersze(d,200 if kod else 250,oferta(f1,f2,f3,kod),W,40)
    im.save(f'karuzela_{i}'+('' if kod else '_bez_kodu')+'.jpg',quality=92)
# --- TikTok 1080x1920: napis nad zdjęciem, zdjęcie bez napisu niżej, tło: to samo zdjęcie rozmyte
TW,TH=1080,1920
def tlo_tt(name):
    im=Image.open(S+name+'.png').convert('RGB').resize((TH,TH),Image.LANCZOS)
    x=(TH-TW)//2; im=im.crop((x,0,x+TW,TH)).filter(ImageFilter.GaussianBlur(30))
    return ImageEnhance.Brightness(im).enhance(0.45)
def slide_tt(i,name,fx,where,t1,t2):
    bg=tlo_tt(name); ph=base(name,fx).resize((880,1100),Image.LANCZOS); bg.paste(ph,(100,420))
    d=ImageDraw.Draw(bg); f1=ImageFont.truetype(SB,76); f2=ImageFont.truetype(SI,48)
    sz=76
    while d.textlength(t1,font=f1)>880: sz-=4; f1=ImageFont.truetype(SB,sz)
    text(d,190,t1,f1,(255,255,255),TW); text(d,300,t2,f2,(255,242,220),TW)
    bg.save(f'karuzela_tt_{i}.jpg',quality=92)
def koniec_tt(i,kod):
    bg=tlo_tt('n6'); d=ImageDraw.Draw(bg)
    f1=ImageFont.truetype(SB,72); f2=ImageFont.truetype(SI,50); f3=ImageFont.truetype(SB,64)
    wiersze(d,380 if kod else 430,oferta(f1,f2,f3,kod),TW,45)
    bg.save(f'karuzela_tt_{i}'+('' if kod else '_bez_kodu')+'.jpg',quality=92)
if __name__=='__main__':
    tt=sys.argv[1:]==['tt']
    for i,s in enumerate(SL,1): (slide_tt if tt else slide)(i,*s)
    for kod in (True,False): (koniec_tt if tt else koniec)(len(SL)+1,kod)
