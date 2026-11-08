# paczka na miesiąc (9.11–8.12): 30 filmów po 6–7 s, każdy w wersji TikTok i Facebook, plus opisy i harmonogram
# wzór z analizy (FB i TT 2–8.11): początek z problemem (igły na dywanie, tania girlanda, kot, puste schody), zmiana do ok. 2 s,
# potem ujęcie „po”: najlepiej schody wieczorem i kominek z ogniem; napisy w strefie bezpiecznej, bez przerw na zmianach
# n5 (kot): od ok. 2,5 s kamera gwałtownie opada na podłogę, więc bierzemy tylko 0–2,2 s
# klipy w /home/user/n2/clips (adresy w ../klipy.json), muzyka.wav z muzyka.py; python3 build12.py [nazwa ...]
import subprocess, sys, os, datetime
from PIL import Image, ImageDraw, ImageFont
F=[l.split(':')[0] for l in subprocess.run(['fc-list'],capture_output=True,text=True).stdout.splitlines() if 'Montserrat-ExtraBold' in l][0]
C='/home/user/n2/clips/'; OUT='/home/user/n2/miesiac/'
CX=360; MAXW=540
def card(lines, out, y=150, size=58, small=None):
    im=Image.new('RGBA',(720,1280),(0,0,0,0)); d=ImageDraw.Draw(im); sz=size
    while True:
        f=ImageFont.truetype(F,sz)
        if max(d.textlength(t,font=f) for t in lines)<=MAXW or sz<30: break
        sz-=2
    lh=int(sz*1.22)
    for k,t in enumerate(lines):
        w=d.textlength(t,font=f)
        d.text((CX-w/2,y+k*lh),t,font=f,fill=(255,255,255,255),stroke_width=max(3,sz//14),stroke_fill=(0,0,0,235))
    if small:
        f2=ImageFont.truetype(F,40); w=d.textlength(small,font=f2)
        d.text((CX-w/2,y+len(lines)*lh+24),small,font=f2,fill=(240,214,160,255),stroke_width=4,stroke_fill=(0,0,0,235))
    im.save(out)
END_TT=['Żywa czy sztuczna?','Napisz w komentarzu']; END_FB=['Żywa czy sztuczna?','Link w opisie ↑']
# uwagi do opisu, gdy w kadrze widać dodatki
LAMPKI='✨ Lampki nie są w zestawie.'; KOKARDY='✨ Kokardy i lampki nie są w zestawie.'; SWIECE='✨ Świece i ozdoby nie są w zestawie.'
STOL='✨ Kokardy i świece nie są w zestawie.'; BOMBKI='✨ Lampki i bombki nie są w zestawie.'
T_SCHODY='#girlanda #schody #dekoracjeświąteczne #święta #bożenarodzenie'
T_KOMINEK='#girlanda #kominek #dekoracjeświąteczne #święta #bożenarodzenie'
T_STOL='#girlanda #stółwigilijny #wigilia #dekoracjeświąteczne #święta'
T_DOM='#girlanda #dekoracjeświąteczne #wystrójwnętrz #święta #bożenarodzenie'
T_KOT='#kot #girlanda #dekoracjeświąteczne #święta #bożenarodzenie'
# (nazwa, segmenty [(klip, długość, start)], napisy [(od, do, linie)] – ostatni napis to plansza końcowa, opis, uwaga, hasztagi)
V=[
 ('01_igly_schody_wieczorem',[('c12',1.2,0.5),('c2',1.0,0.8),('p1',4.8,3.2)],
  [(0,2.2,['Żywe gałązki','po tygodniu…']),(2.2,4.6,['A ta przetrwa','całe święta'])],
  'Żywe gałązki po tygodniu? Igły na całym dywanie 😅 Ta girlanda przetrwa całe święta i wygląda jak żywa 🌲',None,T_SCHODY),
 ('02_igly_kominek_ogien',[('c2',1.0,0.6),('c12',1.2,2.0),('p2',4.8,3.0)],
  [(0,2.2,['Co roku igły','na całym dywanie?']),(2.2,4.6,['A ta wygląda tak samo','aż do stycznia'])],
  'Co roku igły na całym dywanie? Ta girlanda nie usycha i posłuży na kolejne święta 🌲🔥',None,T_KOMINEK),
 ('03_tania_vs_cedr_schody',[('n3',2.0,0.3),('n4',2.2,0.3),('p1',2.8,5.0)],
  [(0,2.0,['Tania girlanda','wygląda sztucznie…']),(2.0,4.2,['A ta jak','prawdziwy cedr'])],
  'Tania girlanda wygląda sztucznie z daleka. Ta jest gęsta, miękka i wygląda jak prawdziwy cedr 🌲',None,T_DOM),
 ('04_kot_igly_szafka',[('n5',2.2,0.0),('n6',1.0,0.5),('k1',3.8,0.2)],
  [(0,2.2,['Kot: 1','gałązki: 0']),(2.2,4.6,['W tym roku','bez igieł na podłodze'])],
  'Kot 1 : gałązki 0 😹 Wasz też tak robi? W tym roku bez igieł na podłodze 🌲',LAMPKI,T_KOT),
 ('05_igly_schody_kokardy',[('c12',1.2,2.0),('c2',1.0,1.6),('n2',4.8,0.2)],
  [(0,2.2,['Ile igieł zamiotłaś','w zeszłym roku?']),(2.2,4.6,['W tym roku','zero sprzątania'])],
  'Ile igieł zamiotłaś w zeszłym roku? W tym roku zero sprzątania 🌲 Girlanda, która wygląda jak żywa i nie gubi igieł.',KOKARDY,T_SCHODY),
 ('06_igly_stol_wigilijny',[('c2',1.0,0.6),('c12',1.2,0.5),('k2',4.8,0.2)],
  [(0,2.2,['Twoja girlanda','po tygodniu…']),(2.2,4.6,['A ta na stole','przez całe święta'])],
  'Twoja girlanda po tygodniu? Igły w obrusie i na podłodze 😅 Ta wygląda tak samo przez całe święta 🌲',STOL,T_STOL),
 ('07_puste_schody_przemiana',[('n0',1.6,0.5),('n1',2.4,0.5),('p1',3.0,5.0)],
  [(0,1.6,['Puste schody?']),(1.6,4.0,['Kilka minut…','i gotowe na święta'])],
  'Puste schody? Kilka minut i gotowe na święta 🌲 Girlanda cedrowa, która wygląda jak żywa i nie gubi igieł.',None,T_SCHODY),
 ('08_igly_salon_kominek',[('c12',1.2,0.5),('c2',1.0,0.6),('c3',4.8,0.3)],
  [(0,2.2,['Igły w dywanie','aż do lutego?']),(2.2,4.6,['A ta wygląda tak samo','aż do stycznia'])],
  'Igły w dywanie aż do lutego? Ta girlanda nie gubi igieł i wygląda tak samo przez całe święta 🌲',SWIECE,T_KOMINEK),
 ('09_igly_bombki_zblizenie',[('c2',1.0,0.6),('c12',1.2,2.0),('c9',3.8,0.2)],
  [(0,2.2,['Żywa girlanda','już się sypie?']),(2.2,3.6,['Ta jest gęsta','jak prawdziwy cedr'])],
  'Żywa girlanda już się sypie? Ta jest gęsta jak prawdziwy cedr i nie gubi igieł 🌲',BOMBKI,T_DOM),
 ('10_z_pudelka_kominek',[('c7',2.0,0.2),('n4',2.0,0.3),('c6',3.0,0.5)],
  [(0,2.0,['Prosto z pudełka…']),(2.0,4.0,['…gęsta i miękka'])],
  'Prosto z pudełka: gęsta, miękka i od razu gotowa na kominek 🌲 Wygląda jak żywa, a nie gubi igieł.',None,T_KOMINEK),
 ('11_igly_szafka_tv',[('c12',1.2,0.5),('c2',1.0,0.8),('k1',4.8,0.2)],
  [(0,2.2,['Znowu odkurzasz','igły?']),(2.2,4.6,['A ta nie gubi','igieł'])],
  'Znowu odkurzasz igły? Ta girlanda nie gubi igieł i wygląda jak żywa przez całe święta 🌲',LAMPKI,T_DOM),
 ('12_igly_schody_kokarda_dzien',[('c2',1.0,1.6),('c12',1.2,2.0),('c10',4.8,0.2)],
  [(0,2.2,['Tak kończy','żywa girlanda…']),(2.2,4.6,['Schody gotowe','na całe święta'])],
  'Tak kończy żywa girlanda… A ta zostaje gęsta i zielona przez całe święta 🌲',KOKARDY,T_SCHODY),
 ('13_tania_vs_cedr_kominek',[('n3',2.0,0.3),('n4',2.2,0.3),('p2',2.8,4.8)],
  [(0,2.0,['Nie kupuj','takiej girlandy']),(2.0,4.2,['Ta wygląda','jak żywa'])],
  'Nie kupuj girlandy, która z daleka wygląda jak plastik. Ta wygląda jak prawdziwy cedr 🌲🔥',None,T_KOMINEK),
 ('14_igly_sypialnia',[('c12',1.2,0.5),('c2',1.0,0.6),('k3',4.8,0.2)],
  [(0,2.2,['Żywe gałązki','po tygodniu…']),(2.2,4.6,['A ta w sypialni','przez całe święta'])],
  'Żywe gałązki po tygodniu? Igły wszędzie 😅 Ta w sypialni wygląda tak samo przez całe święta 🌲',LAMPKI,T_DOM),
 ('15_igly_schody_wieczorem_2',[('c2',1.0,1.6),('c12',1.2,2.0),('p1',4.8,3.0)],
  [(0,2.2,['Co roku igły','na całym dywanie?']),(2.2,4.6,['W tym roku','zero sprzątania'])],
  'Co roku igły na całym dywanie? W tym roku zero sprzątania 🌲 Girlanda cedrowa, która wygląda jak żywa i nie gubi igieł.',None,T_SCHODY),
 ('16_pusty_kominek_przemiana',[('c0',1.6,0.2),('c1',2.4,0.3),('c3',3.0,2.0)],
  [(0,1.6,['Pusty kominek?']),(1.6,4.0,['Kilka minut…','i gotowe na święta'])],
  'Pusty kominek? Kilka minut i gotowe na święta 🌲 Girlanda cedrowa, która wygląda jak żywa i nie gubi igieł.',SWIECE,T_KOMINEK),
 ('17_kot_kominek',[('n5',1.6,0.3),('n6',1.2,0.4),('p2',4.2,3.4)],
  [(0,2.8,['Kot kontra','żywe gałązki']),(2.8,5.0,['W tym roku','kot nie ma szans'])],
  'Kot kontra żywe gałązki 😹 W tym roku girlanda, która nie gubi igieł, nawet gdy kot próbuje 🌲',None,T_KOT),
 ('18_igly_kominek_ogien_2',[('c12',1.2,0.5),('c2',1.0,0.8),('p2',4.8,3.0)],
  [(0,2.2,['Ile igieł zamiotłaś','w zeszłym roku?']),(2.2,4.6,['A ta nie gubi','igieł'])],
  'Ile igieł zamiotłaś w zeszłym roku? Ta girlanda nie gubi igieł i wygląda jak żywa 🌲🔥',None,T_KOMINEK),
 ('19_igly_schody_kokardy_2',[('c2',1.0,0.6),('c12',1.2,0.5),('n2',4.8,0.2)],
  [(0,2.2,['Igły w dywanie','aż do lutego?']),(2.2,4.6,['A ta przetrwa','całe święta'])],
  'Igły w dywanie aż do lutego? Ta girlanda przetrwa całe święta i wygląda jak żywa 🌲',KOKARDY,T_SCHODY),
 ('20_igly_stol_wigilijny_2',[('c12',1.2,2.0),('c2',1.0,1.6),('k2',4.8,0.2)],
  [(0,2.2,['Żywa girlanda','już się sypie?']),(2.2,4.6,['Stół wigilijny','bez igieł w obrusie'])],
  'Żywa girlanda już się sypie? W tym roku stół wigilijny bez igieł w obrusie 🌲',STOL,T_STOL),
 ('21_z_pudelka_na_kominek',[('c7',2.0,0.2),('c8',2.2,0.3),('p2',2.8,4.0)],
  [(0,2.0,['Prosto z pudełka…']),(2.0,4.2,['…na kominek','w kilka minut'])],
  'Prosto z pudełka na kominek w kilka minut 🌲 Gęsta girlanda, która wygląda jak żywa i nie gubi igieł.',None,T_KOMINEK),
 ('22_igly_salon_kominek_2',[('c2',1.0,0.6),('c12',1.2,2.0),('c3',4.8,0.3)],
  [(0,2.2,['Twoja girlanda','po tygodniu…']),(2.2,4.6,['A ta przetrwa','całe święta'])],
  'Twoja girlanda po tygodniu? Ta przetrwa całe święta i wygląda jak żywa 🌲',SWIECE,T_KOMINEK),
 ('23_tania_vs_cedr_kokardy',[('n3',2.0,0.3),('n4',2.2,0.3),('n2',2.8,1.0)],
  [(0,2.0,['Tania girlanda','wygląda sztucznie…']),(2.0,4.2,['A ta jak','prawdziwy cedr'])],
  'Tania girlanda wygląda sztucznie. Ta jest gęsta i wygląda jak prawdziwy cedr, nawet z bliska 🌲',KOKARDY,T_SCHODY),
 ('24_igly_szafka_tv_2',[('c2',1.0,1.6),('c12',1.2,2.0),('k1',4.8,0.2)],
  [(0,2.2,['Co roku igły','na całym dywanie?']),(2.2,4.6,['A ta wygląda tak samo','aż do stycznia'])],
  'Co roku igły na całym dywanie? Ta girlanda wygląda tak samo aż do stycznia 🌲',LAMPKI,T_DOM),
 ('25_igly_schody_do_trzech_kroli',[('c12',1.2,0.5),('c2',1.0,0.8),('p1',4.8,3.2)],
  [(0,2.2,['Tak kończy','żywa girlanda…']),(2.2,4.6,['A ta przetrwa','do Trzech Króli'])],
  'Tak kończy żywa girlanda… A ta przetrwa do Trzech Króli i posłuży na kolejne święta 🌲',None,T_SCHODY),
 ('26_puste_schody_kokardy',[('n0',1.6,0.5),('n1',2.4,0.5),('n2',3.0,1.0)],
  [(0,1.6,['Puste schody?']),(1.6,4.0,['Jedna girlanda…','i święta w domu'])],
  'Puste schody? Jedna girlanda i święta w domu 🌲 Wygląda jak żywa i nie gubi igieł.',KOKARDY,T_SCHODY),
 ('27_igly_bialy_kominek',[('c2',1.0,0.6),('c12',1.2,0.5),('c6',3.8,0.2)],
  [(0,2.2,['Znowu odkurzasz','igły?']),(2.2,3.6,['Wystarczy','jedna girlanda'])],
  'Znowu odkurzasz igły? Wystarczy jedna girlanda, która wygląda jak żywa i nie gubi igieł 🌲',None,T_KOMINEK),
 ('28_igly_sypialnia_2',[('c2',1.0,1.6),('c12',1.2,2.0),('k3',4.8,0.2)],
  [(0,2.2,['Ile igieł zamiotłaś','w zeszłym roku?']),(2.2,4.6,['W tym roku','zero sprzątania'])],
  'Ile igieł zamiotłaś w zeszłym roku? W tym roku zero sprzątania, nawet w sypialni 🌲',LAMPKI,T_DOM),
 ('29_kot_schody',[('n5',2.2,0.0),('n6',1.0,0.5),('n2',3.8,0.5)],
  [(0,2.2,['Kot: 1','gałązki: 0']),(2.2,4.6,['W tym roku','igieł nie będzie'])],
  'Kot 1 : gałązki 0 😹 W tym roku igieł na podłodze nie będzie 🌲',KOKARDY,T_KOT),
 ('30_ostatnie_dni_schody',[('c12',1.2,0.5),('c2',1.0,0.8),('p1',4.8,3.0)],
  [(0,2.2,['Żywe gałązki','po tygodniu…']),(2.2,4.6,['Zamów do 10 grudnia,','zdąży na święta'])],
  'Żywe gałązki po tygodniu? Ta girlanda wygląda jak żywa przez całe święta 🌲',None,T_SCHODY),
]
START=datetime.date(2026,11,9)
DNI=['poniedziałek','wtorek','środa','czwartek','piątek','sobota','niedziela']
def termin(i):
    d=START+datetime.timedelta(days=i)
    if d>=datetime.date(2026,12,6): t='⏳ Ostatnie dni! Zamów do 10 grudnia, a zdąży na święta.'
    elif d>=datetime.date(2026,12,1): t='⏳ Zostało kilka dni: zamów do 10 grudnia, a zdąży na święta.'
    else: t='⏳ Zamów do 10 grudnia, a zdąży na święta.'
    return d,t
def opis(i,fb):
    _,_,_,o,uw,tags=V[i]; d,t=termin(i)
    r=[o,t,'📦 Darmowa dostawa i 30 dni na zwrot.']
    if uw: r.append(uw)
    if not fb: r.append('💬 Żywa czy sztuczna? Napisz w komentarzu 👇')
    r.append('👉 Sklep: https://lesnykominek.pl/fb' if fb else '👉 Sklep: lesnykominek.pl')
    r.append(tags)
    return '\n\n'.join(r)
def make(i,fb):
    name,segs,caps=V[i][:3]; total=round(sum(s[1] for s in segs),2)
    caps=caps+[(caps[-1][1],total,END_FB if fb else END_TT)]
    inp=[]; fil=[]
    for k,(c,d,ss) in enumerate(segs):
        inp+=['-ss',f'{ss}','-t',f'{d+0.1:.2f}','-i',C+c+'.mp4']
        fil.append(f"[{k}:v]scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30,setsar=1,trim=end={d:.3f},setpts=PTS-STARTPTS[v{k}]")
    n=len(segs); fil.append(''.join(f'[v{k}]' for k in range(n))+f'concat=n={n}:v=1:a=0,fps=30,setpts=N/30/TB[cat]'); last='cat'; idx=n
    for k,(a,b,lines) in enumerate(caps):
        png=f'/tmp/cap_{name}_{int(fb)}_{k}.png'; card(lines,png,y=150+(95 if fb else 0),small='lesnykominek.pl' if k==len(caps)-1 else None)
        inp+=['-loop','1','-t',f'{total:.2f}','-i',png]
        fil.append(f"[{last}][{idx}:v]overlay=0:0:enable='gte(t,{a:.2f})*lt(t,{b:.2f})'[o{k}]"); last=f'o{k}'; idx+=1
    inp+=['-i','/home/user/n2/muzyka.wav']; fil.append(f"[{idx}:a]atrim=0:{total:.2f},afade=t=in:d=0.05,afade=t=out:st={total-0.4:.2f}:d=0.4[a]")
    d,_=termin(i); sub=('facebook' if fb else 'tiktok')
    out=f"{OUT}tydzien_{i//7+1 if i<28 else 4}/{sub}/{d.strftime('%m-%d')}_{name}{'_fb' if fb else ''}.mp4"
    os.makedirs(os.path.dirname(out),exist_ok=True)
    cmd=['ffmpeg','-v','error','-y',*inp,'-filter_complex',';'.join(fil),'-map',f'[{last}]','-map','[a]','-t',f'{total:.2f}','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart',out]
    r=subprocess.run(cmd,capture_output=True,text=True); print(name,int(fb),r.returncode,total,r.stderr[-200:],flush=True)
def harmonogram():
    for w in range(1,5):
        rows=[k for k in range(len(V)) if (k//7+1 if k<28 else 4)==w]
        txt=[f'TYDZIEŃ {w}: 1 film dziennie, ten sam na TikToku i Facebooku',
             'Godzina: pon–pt 19:30, sob–ndz 20:00. Przy publikacji ZAWSZE włącz etykietę SI (FB: „Dodaj etykietę SI”, TT: „Treść wygenerowana przez AI”).','']
        for k in rows:
            d,_=termin(k); name=V[k][0]
            txt+=['='*60,f"{d.strftime('%d.%m')} ({DNI[d.weekday()]}), {'20:00' if d.weekday()>=5 else '19:30'}",'',
                  f"TIKTOK: tiktok/{d.strftime('%m-%d')}_{name}.mp4",'',opis(k,False),'',
                  f"FACEBOOK: facebook/{d.strftime('%m-%d')}_{name}_fb.mp4",'',opis(k,True),'']
        p=f'{OUT}tydzien_{w}/00_HARMONOGRAM_I_OPISY.txt'; os.makedirs(os.path.dirname(p),exist_ok=True)
        open(p,'w').write('\n'.join(txt))
if __name__=='__main__':
    names=sys.argv[1:]
    for i,v in enumerate(V):
        if names and v[0] not in names: continue
        for fb in (False,True): make(i,fb)
    harmonogram()
