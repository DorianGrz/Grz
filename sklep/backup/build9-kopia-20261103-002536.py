# filmy w stylu „aesthetic”: jedno ujęcie wieczorem, mały elegancki napis na środku, pozytywka
import subprocess, sys, glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter
def font(pat):
    f=[p for p in glob.glob('/usr/share/fonts/**/*',recursive=True) if pat in p.split('/')[-1]]
    return sorted(f)[0]
SERIF_I=font('P052-Italic'); SERIF_B=font('P052-Bold')
C='/home/user/n2/clips/'
def card(lines, out, size=50, small=None, y=None, fnt=None):
    im=Image.new('RGBA',(720,1280),(0,0,0,0)); f=ImageFont.truetype(fnt or SERIF_I,size); d=ImageDraw.Draw(im)
    lh=int(size*1.25); H=lh*len(lines); y0=y if y is not None else 620-H//2
    sh=Image.new('RGBA',(720,1280),(0,0,0,0)); ds=ImageDraw.Draw(sh)
    for k,t in enumerate(lines):
        w=d.textlength(t,font=f); ds.text(((720-w)/2+2,y0+k*lh+3),t,font=f,fill=(0,0,0,200))
    if small:
        for k,(t,sz) in enumerate(small):
            f2=ImageFont.truetype(SERIF_B if k==0 else SERIF_I,sz); w=d.textlength(t,font=f2); ds.text(((720-w)/2+2,y0+H+30+k*int(sz*1.4)+3),t,font=f2,fill=(0,0,0,200))
    sh=sh.filter(ImageFilter.GaussianBlur(6))
    glow=Image.new('RGBA',(720,1280),(0,0,0,0)); dg=ImageDraw.Draw(glow); bh=H+(len(small)*60+40 if small else 0)
    dg.ellipse((-60,y0-90,780,y0+bh+90),fill=(0,0,0,110)); glow=glow.filter(ImageFilter.GaussianBlur(45))
    im=Image.alpha_composite(im,glow); im=Image.alpha_composite(im,sh); im=Image.alpha_composite(im,sh); d=ImageDraw.Draw(im)
    for k,t in enumerate(lines):
        w=d.textlength(t,font=f); d.text(((720-w)/2,y0+k*lh),t,font=f,fill=(255,255,255,255))
    if small:
        for k,(t,sz) in enumerate(small):
            f2=ImageFont.truetype(SERIF_B if k==0 else SERIF_I,sz); w=d.textlength(t,font=f2)
            d.text(((720-w)/2,y0+H+30+k*int(sz*1.4)),t,font=f2,fill=(245,225,180,255) if k==0 else (255,255,255,240))
    im.save(out)
CTA=[('lesnykominek.pl',48),('Zamów do 10 grudnia, zdąży na święta',34)]
V={
'szafka_rtv':('k1',[(0,3.2,['Twój znak, żeby w tym roku','mieć taką girlandę'],None),(3.2,5.0,['Twój znak, żeby w tym roku','mieć taką girlandę'],CTA)]),
'nad_stolem':('k2',[(0,3.2,['Jedyna dekoracja,','jakiej potrzebujesz na święta'],None),(3.2,5.0,['Jedyna dekoracja,','jakiej potrzebujesz na święta'],CTA)]),
'nad_lozkiem':('k3',[(0,3.2,['Taka puszysta…','a wygląda jak żywa'],None),(3.2,5.0,['Taka puszysta…','a wygląda jak żywa'],CTA)]),
}
def make(name):
    clip,caps=V[name]; total=5.0
    inp=['-i',C+clip+'.mp4']; fil=[f"[0:v]scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30,setsar=1,trim=end={total},setpts=PTS-STARTPTS[v]"]; last='v'; idx=1
    for k,(a,b,lines,small) in enumerate(caps):
        png=f'{name}_{k}.png'; card(lines,png,small=small); inp+=['-loop','1','-t',f'{total}','-i',png]
        fil.append(f"[{last}][{idx}:v]overlay=0:0:enable='between(t,{a},{b-0.01})'[o{k}]"); last=f'o{k}'; idx+=1
    inp+=['-i','muzyka.wav']; fil.append(f"[{idx}:a]atrim=0:{total},afade=t=in:d=0.05,afade=t=out:st={total-0.4}:d=0.4[a]")
    cmd=['ffmpeg','-v','error','-y',*inp,'-filter_complex',';'.join(fil),'-map',f'[{last}]','-map','[a]','-t',f'{total}','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart',name+'.mp4']
    r=subprocess.run(cmd,capture_output=True,text=True); print(name,r.returncode,r.stderr[-300:],flush=True)
if __name__=='__main__':
    for nm in (sys.argv[1:] or list(V)): make(nm)
