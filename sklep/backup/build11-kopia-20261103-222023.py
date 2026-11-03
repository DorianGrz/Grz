# warianty zwycięzcy zywe_galazki: igły na dywanie na start, potem nasze nowe ujęcia "wow", napisy w strefie bezpiecznej TikToka
# klipy: c2, c12 (stare, ../klipy.json), p1, p2 (przejazd), k1, k3 (aesthetic) w /home/user/n2/clips
import subprocess, sys
from PIL import Image, ImageDraw, ImageFont
F=[l.split(':')[0] for l in subprocess.run(['fc-list'],capture_output=True,text=True).stdout.splitlines() if 'Montserrat-ExtraBold' in l][0]
C='/home/user/n2/clips/'
# strefa bezpieczna TikToka w 720x1280: góra od ~110 px, dół do ~950 px, prawa krawędź do ~630 px
CX=360; MAXW=540
def card(lines, out, y=150, size=58, small=None, ys=None):
    im=Image.new('RGBA',(720,1280),(0,0,0,0)); d=ImageDraw.Draw(im)
    sz=size
    while lines:
        f=ImageFont.truetype(F,sz)
        if max(d.textlength(t,font=f) for t in lines)<=MAXW or sz<30: break
        sz-=2
    lh=int(sz*1.22)
    for k,t in enumerate(lines):
        w=d.textlength(t,font=f)
        d.text((CX-w/2,y+k*lh),t,font=f,fill=(255,255,255,255),stroke_width=max(3,sz//14),stroke_fill=(0,0,0,235))
    if small:
        if ys is None: ys=y+len(lines)*lh+24
        f2=ImageFont.truetype(F,40); w=d.textlength(small,font=f2)
        d.text((CX-w/2,ys),small,font=f2,fill=(240,214,160,255),stroke_width=4,stroke_fill=(0,0,0,235))
    im.save(out)
END=['Żywa czy sztuczna?','Napisz w komentarzu']
# segment: (klip, długość, start w klipie); napis: (od, do, linie, mały napis, y)
V={
'igly_ogien':(
  [('c12',2.2,0.5),('c2',1.4,0.8),('p2',4.4,1.6)],
  [(0,3.6,['Żywe gałązki','po tygodniu…'],None,150),(3.6,6.0,['A ta wygląda tak samo','aż do stycznia'],None,150),(6.0,8.0,END,'lesnykominek.pl',150)]),
'igly_schody':(
  [('c12',2.2,0.5),('c2',1.4,0.8),('p1',4.4,3.4)],
  [(0,3.6,['Żywe gałązki','po tygodniu…'],None,150),(3.6,6.0,['A ta przetrwa','całe święta'],None,150),(6.0,8.0,END,'lesnykominek.pl',150)]),
'igly_zamiatanie':(
  [('c2',2.0,0.6),('c12',1.6,1.2),('k3',2.4,0.8),('k1',2.0,1.0)],
  [(0,3.6,['Ile igieł zamiotłaś','w zeszłym roku?'],None,150),(3.6,6.0,['W tym roku','zero'],None,150),(6.0,8.0,END,'lesnykominek.pl',150)]),
'zywe_galazki_2':(
  [('c12',2.2,0.5),('c2',1.6,0.8),('p1',2.6,4.6),('p2',2.6,4.4)],
  [(0,3.8,['Żywe gałązki','po tygodniu…'],None,150),(3.8,6.4,['A ta wygląda tak samo','aż do stycznia'],None,150),(6.4,9.0,END,'lesnykominek.pl',150)]),
}
def make(name):
    segs,caps=V[name]; total=sum(s[1] for s in segs)
    inp=[]; fil=[]
    for i,(c,d,ss) in enumerate(segs):
        inp+=['-ss',f'{ss}','-t',f'{d+0.1:.2f}','-i',C+c+'.mp4']
        fil.append(f"[{i}:v]scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30,setsar=1,trim=end={d:.3f},setpts=PTS-STARTPTS[v{i}]")
    n=len(segs); fil.append(''.join(f'[v{i}]' for i in range(n))+f'concat=n={n}:v=1:a=0[cat]'); last='cat'; idx=n
    for k,(a,b,lines,small,y) in enumerate(caps):
        png=f'{name}_{k}.png'; card(lines,png,y=y or 150,small=small)
        inp+=['-loop','1','-t',f'{total:.2f}','-i',png]
        fil.append(f"[{last}][{idx}:v]overlay=0:0:enable='between(t,{a:.2f},{b-0.01:.2f})'[o{k}]"); last=f'o{k}'; idx+=1
    inp+=['-i','muzyka.wav']; fil.append(f"[{idx}:a]atrim=0:{total:.2f},afade=t=in:d=0.05,afade=t=out:st={total-0.4:.2f}:d=0.4[a]")
    cmd=['ffmpeg','-v','error','-y',*inp,'-filter_complex',';'.join(fil),'-map',f'[{last}]','-map','[a]','-t',f'{total:.2f}','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart',name+'.mp4']
    r=subprocess.run(cmd,capture_output=True,text=True); print(name,r.returncode,round(total,2),r.stderr[-300:],flush=True)
if __name__=="__main__":
    for nm in (sys.argv[1:] or list(V)): make(nm)
