# film ze zdjęć produktu (bez ruchu AI i bez lektora): 5 zdjęć po 1,1 s z lekkim przybliżeniem + plansza końcowa, pozytywka
# 720x1280; zdjęcie w całości na środku, w tle to samo zdjęcie rozmyte; napisy w strefie bezpiecznej TikToka
# FB=1 -> wersja na Facebooka z „Link w komentarzu ↓”
import glob, os, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
def font(pat):
    return sorted(p for p in glob.glob('/usr/share/fonts/**/*',recursive=True) if pat in p.split('/')[-1] and p.endswith('.otf'))[0]
SB=font('P052-Bold'); SI=font('P052-Italic')
S='/home/user/foto/'; W,H=720,1280; FPS=30
FB=bool(os.environ.get('FB'))
SL=[('n31','Wygląda jak żywa'),('n2','Gęste gałązki cedru'),('n13','Na schody'),('n21','Na stół wigilijny'),('n5','Nad drzwi')]
DUR=1.1; END=1.5
def text(d,y,t,f,fill):
    w=d.textlength(t,font=f); x=(W-w)/2
    for dx,dy in ((2,3),(0,3),(3,2)): d.text((x+dx,y+dy),t,font=f,fill=(0,0,0))
    d.text((x,y),t,font=f,fill=fill)
def tlo(img):
    b=img.resize((H,H)).crop(((H-W)//2,0,(H-W)//2+W,H)).filter(ImageFilter.GaussianBlur(28))
    return ImageEnhance.Brightness(b).enhance(0.55)
def klatki():
    f1=ImageFont.truetype(SB,58); f2=ImageFont.truetype(SI,36); f3=ImageFont.truetype(SB,50)
    for name,t in SL:
        img=Image.open(S+name+'.png').convert('RGB'); bg=tlo(img); img=img.resize((730,730),Image.LANCZOS); n=int(DUR*FPS)
        for k in range(n):
            z=1.0+0.06*k/n; s=int(680*z); fr=bg.copy()
            im=img.resize((s,s),Image.BICUBIC); c=(s-680)//2; im=im.crop((c,c,c+680,c+680))
            fr.paste(im,(20,300)); d=ImageDraw.Draw(fr); text(d,170,t,f1,(255,255,255)); yield fr
    img=Image.open(S+'n6.png').convert('RGB'); bg0=tlo(img)
    rows=[('Darmowa dostawa',f3,(255,255,255)),('30 dni na zwrot',f3,(255,255,255)),('',f2,None),
          ('Zamów do 10 grudnia,',f2,(245,232,205)),('zdąży na święta',f2,(245,232,205)),('',f2,None),
          (('Link w komentarzu ↓' if FB else 'lesnykominek.pl'),f3,(245,225,180))]
    n=int(END*FPS)
    for k in range(n):
        # plansza końcowa z wolnym przybliżeniem tła, żeby nie wyglądała na zacięcie
        z=1.0+0.05*k/n; sw,sh=int(W*z),int(H*z); bg=bg0.resize((sw,sh),Image.BICUBIC).crop(((sw-W)//2,(sh-H)//2,(sw-W)//2+W,(sh-H)//2+H))
        d=ImageDraw.Draw(bg); y=330
        for t,f,c in rows:
            if t: text(d,y,t,f,c)
            y+=int(f.size*1.45) if t else 30
        yield bg
def make():
    total=len(SL)*DUR+END; out='pokaz_zdjec'+('_fb' if FB else '')+'.mp4'
    p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
        '-i','muzyka.wav','-filter_complex',f'[1:a]atrim=0:{total},afade=t=in:d=0.05,afade=t=out:st={total-0.4}:d=0.4[a]',
        '-map','0:v','-map','[a]','-t',f'{total}','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',
        '-c:a','aac','-b:a','160k','-movflags','+faststart',out],stdin=subprocess.PIPE)
    for fr in klatki(): p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait(); print(out,p.returncode,total)
if __name__=='__main__': make()
