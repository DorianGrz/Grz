# krótkie filmy (muzyka + napis), klipy w /home/user/clips (adresy w ../klipy.json)
import subprocess, sys
from PIL import Image, ImageDraw, ImageFont
F=[l.split(':')[0] for l in subprocess.run(['fc-list'],capture_output=True,text=True).stdout.splitlines() if 'Montserrat-ExtraBold' in l][0]
C='/home/user/clips/'
def card(lines, out, y=300, size=58, small=None):
    im=Image.new('RGBA',(720,1280),(0,0,0,0)); d=ImageDraw.Draw(im)
    sz=size
    while True:
        f=ImageFont.truetype(F,sz)
        if max([d.textlength(t,font=f) for t in lines] or [0])<=640 or sz<30: break
        sz-=2
    lh=int(sz*1.22)
    for k,t in enumerate(lines):
        w=d.textlength(t,font=f)
        d.text(((720-w)/2,y+k*lh),t,font=f,fill=(255,255,255,255),stroke_width=max(3,sz//14),stroke_fill=(0,0,0,235))
    if small:
        f2=ImageFont.truetype(F,40); w=d.textlength(small,font=f2)
        d.text(((720-w)/2,1040),small,font=f2,fill=(240,214,160,255),stroke_width=4,stroke_fill=(0,0,0,235))
    im.save(out)
# segment: (klip, długość, start w klipie); napis: (od, do, linie, mały napis na dole, y)
V={
'girlanda_marzen':(
  [('c10',2.8,0.3),('c9',2.4,0.5),('c11',2.8,0.4)],
  [(0,8.0,['Kiedy w końcu znalazłaś','girlandę, która wygląda','jak żywa…'],None,300),(5.2,8.0,[],'lesnykominek.pl',None)]),
'kiedys_vs_teraz':(
  [('c14',2.4,0.5),('c12',1.8,0.6),('c2',1.4,0.8),('c5',1.4,0.2),('c7',1.5,0.6),('c10',1.8,0.5),('c11',1.8,0.6),('c3',2.6,0.6)],
  [(0,5.6,['Dekorowanie domu','kiedyś…'],None,280),(5.6,7.0,['Vs…'],None,280),(7.0,12.1,['Dekorowanie domu','teraz'],None,280),(12.1,14.7,['Napisz „CHCĘ”','w komentarzu'],'lesnykominek.pl',280)]),
'caly_dom':(
  [('c10',2.6,0.3),('c11',2.2,0.6),('c9',2.0,0.6),('c1',5.0,0.8)],
  [(0,2.6,['Jedna girlanda','i cały dom gotowy','na święta'],None,280),(2.6,4.8,['Drzwi'],None,280),(4.8,6.8,['Z bombkami'],None,280),(6.8,9.2,['Kominek'],None,280),(9.2,11.8,['Od którego miejsca','zaczynasz?'],'lesnykominek.pl',280)]),
}
def make(name):
    segs,caps=V[name]; total=sum(s[1] for s in segs)
    inp=[]; fil=[]
    for i,(c,d,ss) in enumerate(segs):
        inp+=['-ss',f'{ss}','-t',f'{d+0.1:.2f}','-i',C+c+'.mp4']
        fil.append(f"[{i}:v]scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30,setsar=1,trim=end={d:.3f},setpts=PTS-STARTPTS[v{i}]")
    n=len(segs); fil.append(''.join(f'[v{i}]' for i in range(n))+f'concat=n={n}:v=1:a=0[cat]'); last='cat'; idx=n
    for k,(a,b,lines,small,y) in enumerate(caps):
        png=f'{name}_{k}.png'; card(lines,png,y=y or 300,small=small)
        inp+=['-loop','1','-t',f'{total:.2f}','-i',png]
        fil.append(f"[{last}][{idx}:v]overlay=0:0:enable='between(t,{a:.2f},{b-0.01:.2f})'[o{k}]"); last=f'o{k}'; idx+=1
    inp+=['-i','muzyka.wav']; fil.append(f"[{idx}:a]atrim=0:{total:.2f},afade=t=in:d=0.05,afade=t=out:st={total-0.4:.2f}:d=0.4[a]")
    cmd=['ffmpeg','-v','error','-y',*inp,'-filter_complex',';'.join(fil),'-map',f'[{last}]','-map','[a]','-t',f'{total:.2f}','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart',name+'.mp4']
    r=subprocess.run(cmd,capture_output=True,text=True); print(name,r.returncode,round(total,2),r.stderr[-300:],flush=True)
for nm in (sys.argv[1:] or list(V)): make(nm)
