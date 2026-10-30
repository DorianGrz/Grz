# nowe filmy (schody, porównanie, kot); czasy w sekundach filmu; klipy n0–n6 w /home/user/nowe/clips (adresy w ../klipy.json)
import subprocess, sys, json
from PIL import Image, ImageDraw, ImageFont
F=[l.split(':')[0] for l in subprocess.run(['fc-list'],capture_output=True,text=True).stdout.splitlines() if 'Montserrat-ExtraBold' in l][0]
C='/home/user/nowe/clips/'
def card(lines, out, y=280, size=62, small=None):
    im=Image.new('RGBA',(720,1280),(0,0,0,0)); d=ImageDraw.Draw(im); sz=size
    while True:
        f=ImageFont.truetype(F,sz)
        if max([d.textlength(t,font=f) for t in lines] or [0])<=640 or sz<30: break
        sz-=2
    lh=int(sz*1.22)
    for k,t in enumerate(lines):
        w=d.textlength(t,font=f); d.text(((720-w)/2,y+k*lh),t,font=f,fill=(255,255,255,255),stroke_width=max(3,sz//14),stroke_fill=(0,0,0,235))
    if small:
        f2=ImageFont.truetype(F,40); w=d.textlength(small,font=f2)
        d.text(((720-w)/2,1040),small,font=f2,fill=(240,214,160,255),stroke_width=4,stroke_fill=(0,0,0,235))
    im.save(out)
def endcard(out):
    im=Image.new('RGBA',(720,1280),(10,20,15,165)); d=ImageDraw.Draw(im)
    for txt,sz,y,c in [('lesnykominek.pl',84,540,(232,206,150,255)),('Darmowa dostawa · 30 dni na zwrot',32,665,(255,255,255,235))]:
        f=ImageFont.truetype(F,sz)
        while d.textlength(txt,font=f)>650: sz-=2; f=ImageFont.truetype(F,sz)
        d.text(((720-d.textlength(txt,font=f))/2,y),txt,font=f,fill=c)
    im.save(out)
endcard('end.png'); Image.new('RGBA',(720,1280),(255,255,255,70)).save('flash.png')
def dur(p): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout)
# segs: (klip, od [s], start w klipie); caps: (od, do, linie, mały napis, y); audio: 'muzyka' albo (plik_glosu, czas_adresu)
V={
'schody_przemiana':dict(segs=[('n0',0,0.2),('n1',2.2,0.3),('n2',5.6,0.2)],total=9.6,audio='muzyka',
  caps=[(0,5.6,['Dodajmy girlandę','na schody'],None,280),(5.6,9.6,['Z kokardami','czy bez?'],'lesnykominek.pl',280)]),
'schody_wieczorem':dict(segs=[('n2',0,0.0)],total=5.0,audio='muzyka',
  caps=[(0,3.0,['Tak mogą wyglądać','Twoje schody w grudniu'],None,280),(3.0,5.0,['Zapisz na grudzień'],'lesnykominek.pl',280)]),
'kot_vs_galazki':dict(segs=[('n5',0,0.0),('n6',2.6,0.3),('n4',5.0,0.3),('n2',7.4,0.3)],total=10.0,audio='muzyka',
  caps=[(0,2.6,['Grudzień','z żywymi gałązkami…'],None,280),(2.6,5.0,['Kot: to nie ja'],None,280),(5.0,7.4,['Ta girlanda','nie gubi igieł'],None,280),(7.4,10.0,['Kto ma takiego kota?'],'lesnykominek.pl',280)]),
'nie_popelnij_bledu':dict(segs=[('n3',0,0.0),('n4',6.8,0.2),('n2',9.78,0.0)],audio=('nie_popelnij_bledu.wav',12.1),
  caps=[(0,2.92,['Nie popełnij','tego błędu']),(2.92,6.8,['Tania girlanda','wygląda sztucznie']),(6.8,9.78,['Ta jest gęsta','jak prawdziwy cedr']),(9.78,12.1,['Wygląda jak żywa'])]),
}
def make(name):
    v=V[name]; D=0.12 if v['audio']!='muzyka' else 0.0
    if v['audio']=='muzyka': total=v['total']; tl=None
    else:
        wav,tl=v['audio']; tl+=D; total=max(dur(wav)+D+0.5,tl+1.8)
    segs=v['segs']; st=[s[1]+(D if s[1] else 0) for s in segs]+[total]
    inp=[]; fil=[]
    for i,(c,_,ss) in enumerate(segs):
        T=st[i+1]-st[i]; av=dur(C+c+'.mp4')-ss-0.05; sp=min(1.0,av/T)
        inp+=['-ss',f'{ss}','-i',C+c+'.mp4']
        fil.append(f"[{i}:v]setpts=PTS/{sp:.4f},scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30,setsar=1,trim=end={T:.3f},setpts=PTS-STARTPTS[v{i}]")
        print(name,c,'od',round(st[i],2),'T',round(T,2),'tempo',round(sp,2))
    n=len(segs); fil.append(''.join(f'[v{i}]' for i in range(n))+f'concat=n={n}:v=1:a=0[cat]'); last='cat'; idx=n
    if n>1:
        cuts='+'.join(f"between(t,{s:.2f},{s+0.07:.2f})" for s in st[1:-1])
        inp+=['-loop','1','-t',f'{total:.2f}','-i','flash.png']; fil.append(f"[{last}][{idx}:v]overlay=0:0:enable='{cuts}'[fl]"); last='fl'; idx+=1
    for k,cp in enumerate(v['caps']):
        a,b,lines=cp[0],cp[1],cp[2]; small=cp[3] if len(cp)>3 else None; y=cp[4] if len(cp)>4 else 280
        a+=D if a else 0; b=b+D
        if tl: b=min(b,tl)
        png=f'{name}_{k}.png'; card(lines,png,y=y,small=small)
        inp+=['-loop','1','-t',f'{total:.2f}','-i',png]
        fil.append(f"[{last}][{idx}:v]overlay=0:0:enable='between(t,{a:.2f},{b-0.02:.2f})'[o{k}]"); last=f'o{k}'; idx+=1
    if tl:
        inp+=['-loop','1','-t',f'{total:.2f}','-i','end.png']; fil.append(f"[{last}][{idx}:v]overlay=0:0:enable='gte(t,{tl:.2f})'[ve]"); last='ve'; idx+=1
        inp+=['-i',wav]; fil.append(f"[{idx}:a]adelay={int(D*1000)}|{int(D*1000)},apad,atrim=0:{total:.2f},afade=t=out:st={total-0.25:.2f}:d=0.25[a]")
    else:
        inp+=['-i','muzyka.wav']; fil.append(f"[{idx}:a]atrim=0:{total:.2f},afade=t=in:d=0.05,afade=t=out:st={total-0.4:.2f}:d=0.4[a]")
    cmd=['ffmpeg','-v','error','-y',*inp,'-filter_complex',';'.join(fil),'-map',f'[{last}]','-map','[a]','-t',f'{total:.2f}','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart',name+'.mp4']
    r=subprocess.run(cmd,capture_output=True,text=True); print(name,r.returncode,round(total,2),r.stderr[-300:],flush=True)
if __name__=='__main__':
    for nm in (sys.argv[1:] or list(V)): make(nm)
