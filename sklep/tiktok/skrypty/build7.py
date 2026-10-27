# krótkie filmy z lektorem (warianty zwycięzcy persona_glowna_2); czasy w sekundach głosu (ts.json z faster-whisper)
import subprocess, sys, json
sys.path.insert(0,'/home/user/tt6'); from build6 import card, F, C
from PIL import Image, ImageDraw, ImageFont
D=0.12; TS=json.load(open('ts.json'))
def endcard(out):
    im=Image.new('RGBA',(720,1280),(10,20,15,165)); d=ImageDraw.Draw(im)
    for txt,sz,y,c in [('lesnykominek.pl',84,540,(232,206,150,255)),('Darmowa dostawa · 30 dni na zwrot',32,665,(255,255,255,235))]:
        f=ImageFont.truetype(F,sz)
        while d.textlength(txt,font=f)>650: sz-=2; f=ImageFont.truetype(F,sz)
        d.text(((720-d.textlength(txt,font=f))/2,y),txt,font=f,fill=c)
    im.save(out)
endcard('end.png')
def dur(p): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout)
# (klip, start w sekundach głosu, start w klipie); napisy (od, do, linie); czas pojawienia adresu
V={
'igly_krotka':([('c2',0,0.2),('c12',5.38,0.3),('c9',8.76,0.4),('c10',10.74,0.3),('c3',12.98,0.6)],
  [(0,2.88,['Co roku kupujesz','żywe gałązki?']),(2.88,5.38,['Zobacz je','po tygodniu']),(5.38,8.76,['Suche, a igły','są wszędzie']),(8.76,10.74,['Ta wygląda','jak żywa']),(10.74,12.98,['Nie usycha','i nie gubi igieł'])],13.82),
'igly_dywan':([('c12',0,0.2),('c2',3.46,0.2),('c7',6.06,0.6),('c10',7.4,0.3),('c3',10.8,0.6)],
  [(0,3.46,['Ile razy zamiatałaś','igły z dywanu?']),(3.46,6.06,['Żywe gałązki usychają','po tygodniu']),(6.06,7.4,['Ta girlanda nie']),(7.4,10.8,['Wygląda jak żywa','i posłuży na kolejne święta'])],11.62),
}
def make(name):
    segs,caps,tl=V[name]; vod=TS[name]['dur']; tl+=D
    total=max(vod+D+0.5,tl+1.8)
    st=[s[1]+(D if s[1] else 0) for s in segs]+[total]
    inp=[]; fil=[]
    for i,(c,_,ss) in enumerate(segs):
        T=st[i+1]-st[i]; av=dur(C+c+'.mp4')-ss; sp=min(1.0,av/T)
        if c=='c5': av=min(av,1.9-ss); sp=min(1.0,av/T)
        inp+=['-ss',f'{ss}','-i',C+c+'.mp4']
        fil.append(f"[{i}:v]setpts=PTS/{sp:.4f},scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30,setsar=1,trim=end={T:.3f},setpts=PTS-STARTPTS[v{i}]")
    n=len(segs); fil.append(''.join(f'[v{i}]' for i in range(n))+f'concat=n={n}:v=1:a=0[cat]'); last='cat'; idx=n
    cuts='+'.join(f"between(t,{s:.2f},{s+0.07:.2f})" for s in st[1:-1])
    Image.new('RGBA',(720,1280),(255,255,255,70)).save('flash.png')
    inp+=['-loop','1','-t',f'{total:.2f}','-i','flash.png']; fil.append(f"[{last}][{idx}:v]overlay=0:0:enable='{cuts}'[fl]"); last='fl'; idx+=1
    for k,(a,b,lines) in enumerate(caps):
        png=f'{name}_{k}.png'; card(lines,png,y=280); a+=D if a else 0; b=min(b+D,tl)
        inp+=['-loop','1','-t',f'{total:.2f}','-i',png]
        fil.append(f"[{last}][{idx}:v]overlay=0:0:enable='between(t,{a:.2f},{b-0.02:.2f})'[o{k}]"); last=f'o{k}'; idx+=1
    inp+=['-loop','1','-t',f'{total:.2f}','-i','end.png']; fil.append(f"[{last}][{idx}:v]overlay=0:0:enable='gte(t,{tl:.2f})'[vout]"); idx+=1
    inp+=['-i',name+'.wav']; fil.append(f"[{idx}:a]adelay={int(D*1000)}|{int(D*1000)},apad,atrim=0:{total:.2f},afade=t=out:st={total-0.25:.2f}:d=0.25[a]")
    cmd=['ffmpeg','-v','error','-y',*inp,'-filter_complex',';'.join(fil),'-map','[vout]','-map','[a]','-t',f'{total:.2f}','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart',name+'.mp4']
    r=subprocess.run(cmd,capture_output=True,text=True); print(name,r.returncode,round(total,2),r.stderr[-300:],flush=True)
for nm in (sys.argv[1:] or list(V)): make(nm)
