# paczka na miesiąc v2 (9.11–8.12): 2 filmy dziennie = 30 starych z build12 (wieczór) + 30 nowych (rano)
# nowe ujęcia 8.11 (Higgsfield): v1 odkurzanie igieł (grok), v2 sypiące się suche gałązki (grok), s1 schody od dnia do wieczora (kling),
# s1 i g1 NIE używać (8.11): śnieg pada w środku domu, w s1 na girlandzie wyskakują lampki; t1 stół wigilijny (grok); f1 (kominek, grok) NIE używać: od ok. 1 s na girlandzie wyrasta kokarda
# zmiany wg Doriana: bez dopisków „nie są w zestawie”, na FB 3 hasztagi (#dekoracjeswiateczne #girlanda #święta jak w igly_schody, 15 tys. wyśw.)
# python3 build13.py           -> renderuje nowe 30 (TT i FB), kopiuje stare 30 z /home/user/n2/miesiac, pisze harmonogramy
import subprocess, os, shutil, datetime, types, sys
src=open('/home/user/n2/build12.py').read()
b12=types.ModuleType('b12'); b12.__dict__['__name__']='b12'; exec(src,b12.__dict__)
card=b12.card; termin=b12.termin; V=b12.V; DNI=b12.DNI
T_SCHODY,T_KOMINEK,T_STOL,T_DOM,T_KOT=b12.T_SCHODY,b12.T_KOMINEK,b12.T_STOL,b12.T_DOM,b12.T_KOT
C='/home/user/n2/clips/'; OUT='/home/user/n2/miesiac2/'
FB_TAGS='#dekoracjeswiateczne #girlanda #święta'
Q=(['Który pomysł wybierasz?','Napisz w komentarzu'],['Który pomysł wybierasz?','Link w opisie ↑'])
G=(['Gdzie ją powiesisz?','Napisz w komentarzu'],['Gdzie ją powiesisz?','Link w opisie ↑'])
Z=(['Zamów do 10 grudnia,','zdąży na święta'],['Zamów do 10 grudnia','Link w opisie ↑'])
# (nazwa, segmenty, napisy, opis, hasztagi TT, własna plansza końcowa (TT, FB) albo None)
W=[
 ('igly_odkurzacz_schody',[('v1',2.2,1.0),('n2',4.8,0.2)],[(0,2.2,['Co roku','odkurzanie igieł?']),(2.2,4.6,['W tym roku','zero sprzątania'])],
  'Co roku odkurzanie igieł spod choinki? W tym roku zero sprzątania 🌲 Girlanda cedrowa, która wygląda jak żywa i nie gubi igieł.',T_SCHODY,None),
 ('lista_kominek_schody_stol',[('c3',2.0,0.3),('p1',2.6,4.8),('t1',3.4,1.4)],[(0,2.0,['Na kominek…']),(2.0,4.6,['…na schody…']),(4.6,6.0,['…albo na stół'])],
  'Kominek, schody czy stół wigilijny? Jedna girlanda, trzy pomysły 🌲 Który wybierasz?',T_DOM,Q),
 ('igly_sypia_sie_kominek',[('v2',2.2,1.2),('p2',4.8,3.0)],[(0,2.2,['Wystarczy dotknąć…']),(2.2,4.6,['A ta nie gubi','igieł'])],
  'Wystarczy dotknąć i igły lecą na podłogę? Ta girlanda nie gubi igieł i wygląda jak żywa 🌲🔥',T_KOMINEK,None),
 ('tania_vs_cedr_dotyk',[('n3',2.0,0.3),('n4',2.6,0.3),('p1',2.4,5.0)],[(0,2.0,['Tania girlanda','wygląda sztucznie…']),(2.0,4.6,['A ta miękka','jak prawdziwy cedr'])],
  'Tania girlanda wygląda sztucznie. Ta jest miękka i gęsta jak prawdziwy cedr 🌲',T_DOM,None),
 ('igly_obrus_stol',[('c12',1.2,0.5),('c2',1.0,0.8),('t1',4.8,0.2)],[(0,2.2,['Igły w obrusie','na Wigilię?']),(2.2,4.6,['W tym roku','stół bez igieł'])],
  'Igły w obrusie na Wigilię? W tym roku stół bez igieł 🌲 Girlanda, która wygląda jak żywa przez całe święta.',T_STOL,None),
 ('igly_odkurzacz_salon',[('v1',2.2,0.5),('c3',4.8,0.3)],[(0,2.2,['Znowu odkurzasz','igły?']),(2.2,4.6,['A ta wygląda tak samo','aż do stycznia'])],
  'Znowu odkurzasz igły? Ta girlanda wygląda tak samo aż do stycznia 🌲',T_KOMINEK,None),
 ('kot_schody_wieczorem',[('n5',2.2,0.0),('n6',1.0,0.5),('p1',3.8,4.0)],[(0,2.2,['Kot: 1','gałązki: 0']),(2.2,4.6,['W tym roku','kot nie ma szans'])],
  'Kot 1 : gałązki 0 😹 W tym roku girlanda, która nie gubi igieł 🌲',T_KOT,None),
 ('igly_sypia_sie_schody_kokardy',[('v2',2.2,1.2),('n2',4.8,0.2)],[(0,2.2,['Tak wygląda żywa','girlanda po tygodniu']),(2.2,4.6,['A ta przetrwa','całe święta'])],
  'Tak wygląda żywa girlanda po tygodniu… A ta przetrwa całe święta 🌲',T_SCHODY,None),
 ('igly_miekka_okno',[('c2',1.0,0.6),('c12',1.2,2.0),('k3',4.8,0.2)],[(0,2.2,['Żywe gałązki','po tygodniu…']),(2.2,4.6,['A ta miękka','jak prawdziwy cedr'])],
  'Żywe gałązki po tygodniu? Ta girlanda jest miękka jak prawdziwy cedr i nie gubi igieł 🌲',T_DOM,None),
 ('lista_schody_szafka_sypialnia',[('p1',2.4,5.0),('k1',2.4,0.5),('k3',3.2,1.0)],[(0,2.4,['Na schody…']),(2.4,4.8,['…pod telewizor…']),(4.8,6.0,['…albo nad łóżko'])],
  'Schody, szafka RTV czy sypialnia? Gdzie powiesisz swoją girlandę? 🌲',T_DOM,G),
 ('pusty_kominek_w_kilka_minut',[('c0',1.6,0.2),('c8',2.4,0.3),('p2',3.0,4.8)],[(0,1.6,['Pusty kominek?']),(1.6,4.0,['Kilka minut…','i gotowe na święta'])],
  'Pusty kominek? Kilka minut i gotowe na święta 🌲 Girlanda, która wygląda jak żywa i nie gubi igieł.',T_KOMINEK,None),
 ('igly_odkurzacz_stol',[('v1',2.2,1.0),('k2',4.8,0.2)],[(0,2.2,['Co roku igły','pod stołem?']),(2.2,4.6,['A ta nad stołem','całe święta'])],
  'Co roku igły pod stołem? Ta girlanda nad stołem wygląda tak samo przez całe święta 🌲',T_STOL,None),
 ('puste_schody_wieczorem',[('n0',1.6,0.5),('n1',2.4,0.5),('p1',3.0,5.0)],[(0,1.6,['Puste schody?']),(1.6,4.0,['Kilka minut…','i gotowe na święta'])],
  'Puste schody? Kilka minut i gotowe na święta 🌲',T_SCHODY,None),
 ('igly_bombki_zielona',[('c12',1.2,0.5),('c2',1.0,0.8),('c9',3.8,0.2)],[(0,2.2,['Twoja girlanda','po tygodniu…']),(2.2,3.6,['Ta zostaje','zielona do stycznia'])],
  'Twoja girlanda po tygodniu? Ta zostaje zielona do stycznia 🌲',T_DOM,None),
 ('igly_sypia_sie_stol',[('v2',2.2,1.2),('t1',4.8,0.2)],[(0,2.2,['Wystarczy dotknąć…']),(2.2,4.6,['A ta na stole','przez całe święta'])],
  'Wystarczy dotknąć i igły lecą? Ta na stole wygląda tak samo przez całe święta 🌲',T_STOL,None),
 ('z_pudelka_miekka_schody',[('c7',2.0,0.2),('n4',2.4,0.3),('p1',2.6,5.0)],[(0,2.0,['Prosto z pudełka…']),(2.0,4.4,['…gęsta i miękka'])],
  'Prosto z pudełka: gęsta, miękka i od razu gotowa na schody 🌲',T_SCHODY,None),
 ('igly_zamiatanie_ogien',[('c2',1.0,1.6),('c12',1.2,2.0),('c3',2.0,0.3),('p2',2.8,5.0)],[(0,2.2,['Ile igieł zamiotłaś','w zeszłym roku?']),(2.2,4.6,['W tym roku','zero sprzątania'])],
  'Ile igieł zamiotłaś w zeszłym roku? W tym roku zero sprzątania 🌲🔥',T_KOMINEK,None),
 ('igly_odkurzacz_wieszanie',[('v1',2.2,0.8),('c1',4.8,0.6)],[(0,2.2,['Igły w dywanie','aż do lutego?']),(2.2,4.6,['A ta nie gubi','igieł'])],
  'Igły w dywanie aż do lutego? Ta girlanda nie gubi igieł 🌲',T_KOMINEK,None),
 ('tania_vs_cedr_stol',[('n3',2.0,0.3),('n4',2.2,0.3),('t1',2.8,2.0)],[(0,2.0,['Nie kupuj','takiej girlandy']),(2.0,4.2,['Ta wygląda','jak żywa'])],
  'Nie kupuj girlandy, która wygląda jak plastik. Ta wygląda jak żywa, nawet na stole wigilijnym 🌲',T_STOL,None),
 ('lista_kominek_schody_stol_2',[('p2',2.4,5.0),('n2',2.4,1.0),('k2',3.2,1.0)],[(0,2.4,['Na kominek…']),(2.4,4.8,['…na schody…']),(4.8,6.0,['…albo nad stół'])],
  'Kominek, schody czy stół? Który pomysł wybierasz? 🌲',T_DOM,Q),
 ('igly_schody_trzech_kroli_2',[('c2',1.0,0.6),('c12',1.2,0.5),('n2',4.8,0.2)],[(0,2.2,['Tak kończy','żywa girlanda…']),(2.2,4.6,['A ta przetrwa','do Trzech Króli'])],
  'Tak kończy żywa girlanda… A ta przetrwa do Trzech Króli 🌲',T_SCHODY,None),
 ('kot_kto_zrzucil_kominek',[('n6',1.8,0.2),('n5',1.2,0.8),('p2',4.0,3.6)],[(0,3.0,['Kto zrzucił','gałązki?']),(3.0,5.0,['W tym roku','igieł nie będzie'])],
  'Kto zrzucił gałązki? 😹 W tym roku igieł na podłodze nie będzie 🌲',T_KOT,None),
 ('igly_sypia_sie_sypialnia',[('v2',2.2,1.2),('k3',4.8,0.2)],[(0,2.2,['Żywa girlanda','już się sypie?']),(2.2,4.6,['A ta w sypialni','przez całe święta'])],
  'Żywa girlanda już się sypie? Ta w sypialni wygląda tak samo przez całe święta 🌲',T_DOM,None),
 ('igly_odkurzacz_schody_grudzien',[('v1',2.2,1.0),('n2',4.8,0.2)],[(0,2.2,['Co roku igły','na całym dywanie?']),(2.2,4.6,['Tak mogą wyglądać','Twoje schody w grudniu'])],
  'Co roku igły na całym dywanie? Tak mogą wyglądać Twoje schody w grudniu 🌲',T_SCHODY,None),
 ('igly_odkurzacz_miekka',[('v1',2.2,0.5),('n4',4.8,0.2)],[(0,2.2,['Znowu odkurzasz','igły?']),(2.2,4.6,['Ta jest miękka','i nie gubi igieł'])],
  'Znowu odkurzasz igły? Ta girlanda jest miękka jak prawdziwy cedr i nie gubi igieł 🌲',T_DOM,None),
 ('igly_sypia_sie_szafka',[('v2',2.2,1.2),('k1',4.8,0.2)],[(0,2.2,['Żywe gałązki','po tygodniu…']),(2.2,4.6,['A ta pod telewizorem','całe święta'])],
  'Żywe gałązki po tygodniu? Ta pod telewizorem wygląda tak samo przez całe święta 🌲',T_DOM,None),
 ('wyglada_jak_zywa',[('n4',2.4,0.3),('p1',2.4,5.0),('p2',2.0,5.5)],[(0,2.4,['Wygląda jak żywa…']),(2.4,4.8,['…a nie gubi igieł'])],
  'Wygląda jak żywa, a nie gubi igieł 🌲 Miękka, gęsta i gotowa na całe święta.',T_DOM,None),
 ('igly_sypia_sie_schody_wieczorem',[('v2',2.2,1.2),('p1',4.8,3.0)],[(0,2.2,['Wystarczy dotknąć…']),(2.2,4.6,['A ta przetrwa','całe święta'])],
  'Wystarczy dotknąć i igły lecą? Ta girlanda przetrwa całe święta 🌲',T_SCHODY,None),
 ('lista_grudzien',[('t1',2.4,1.0),('p2',2.0,5.5),('n2',3.6,1.0)],[(0,2.4,['Stół wigilijny…']),(2.4,4.4,['…kominek…']),(4.4,6.0,['…i schody'])],
  'Stół wigilijny, kominek i schody: jedna girlanda na całe święta 🌲',T_DOM,Z),
 ('igly_odkurzacz_ostatnie_dni',[('v1',2.2,0.5),('p1',4.8,3.0)],[(0,2.2,['Odkurzanie igieł','w Wigilię?']),(2.2,4.6,['Zamów do 10 grudnia,','zdąży na święta'])],
  'Odkurzanie igieł w Wigilię? Ta girlanda nie gubi igieł i wygląda jak żywa 🌲',T_SCHODY,None),
]
def after(segs): return set(s[0] for s in segs[1:])
IGLY={'c12','c2'}; STOL={'t1','k2'}
def konflikt(a,b):
    # ten sam dzień: bez wspólnego ujęcia „po”, bez dwóch początków ze starymi igłami, bez dwóch stołów
    ca=set(s[0] for s in a); cb=set(s[0] for s in b)
    return bool(after(a)&after(b)) or (a[0][0] in IGLY and b[0][0] in IGLY) or bool(ca&STOL and cb&STOL)
# przydział: dzień i -> rano nowy, wieczór stary; zamiana, gdy para się gryzie
# przydział zamrożony 8.11 (po wymianie f1 na c3/p2), żeby nie przetasować gotowego harmonogramu
ORDER=[0, 1, 2, 3, 6, 5, 4, 7, 9, 8, 10, 11, 12, 15, 14, 13, 22, 17, 18, 21, 20, 19, 16, 23, 24, 25, 26, 27, 29, 28]
order=list(range(len(W)))
for i in ([] if ORDER else range(len(order))):
    if konflikt(W[order[i]][1],V[i][1]):
        for j in range(i+1,len(order)):
            if not konflikt(W[order[j]][1],V[i][1]) and not konflikt(W[order[i]][1],V[j][1]):
                order[i],order[j]=order[j],order[i]; break
if ORDER: order=ORDER
def opis(o,tags,i,fb):
    _,t=termin(i)
    r=[o,t,'📦 Darmowa dostawa i 30 dni na zwrot.']
    if not fb: r.append('💬 Żywa czy sztuczna? Napisz w komentarzu 👇')
    r.append('👉 Sklep: https://lesnykominek.pl/fb' if fb else '👉 Sklep: lesnykominek.pl')
    r.append(FB_TAGS if fb else tags)
    return '\n\n'.join(r)
def tydz(i): return i//7+1 if i<28 else 4
def sciezka(i,pora,name,fb):
    d,_=termin(i); return f"{OUT}tydzien_{tydz(i)}/{'facebook' if fb else 'tiktok'}/{d.strftime('%m-%d')}_{pora}_{name}{'_fb' if fb else ''}.mp4"
def make(i,w,fb):
    name,segs,caps,_,_,end=w; total=round(sum(s[1] for s in segs),2)
    endl=(end[1] if fb else end[0]) if end else (b12.END_FB if fb else b12.END_TT)
    caps=caps+[(caps[-1][1],total,endl)]
    inp=[]; fil=[]
    for k,(c,d,ss) in enumerate(segs):
        inp+=['-ss',f'{ss}','-t',f'{d+0.1:.2f}','-i',C+c+'.mp4']
        fil.append(f"[{k}:v]scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30,setsar=1,trim=end={d:.3f},setpts=PTS-STARTPTS[v{k}]")
    n=len(segs); fil.append(''.join(f'[v{k}]' for k in range(n))+f'concat=n={n}:v=1:a=0,fps=30,setpts=N/30/TB[cat]'); last='cat'; idx=n
    for k,(a,b,lines) in enumerate(caps):
        png=f'/tmp/c13_{name}_{int(fb)}_{k}.png'; card(lines,png,y=150+(95 if fb else 0),small='lesnykominek.pl' if k==len(caps)-1 else None)
        inp+=['-loop','1','-t',f'{total:.2f}','-i',png]
        fil.append(f"[{last}][{idx}:v]overlay=0:0:enable='gte(t,{a:.2f})*lt(t,{b:.2f})'[o{k}]"); last=f'o{k}'; idx+=1
    inp+=['-i','/home/user/n2/muzyka.wav']; fil.append(f"[{idx}:a]atrim=0:{total:.2f},afade=t=in:d=0.05,afade=t=out:st={total-0.4:.2f}:d=0.4[a]")
    out=sciezka(i,'1rano',name,fb); os.makedirs(os.path.dirname(out),exist_ok=True)
    cmd=['ffmpeg','-v','error','-y',*inp,'-filter_complex',';'.join(fil),'-map',f'[{last}]','-map','[a]','-t',f'{total:.2f}','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart',out]
    r=subprocess.run(cmd,capture_output=True,text=True); print(name,int(fb),r.returncode,total,r.stderr[-200:],flush=True)
def stare(i):
    name=V[i][0]; d,_=termin(i)
    for fb in (False,True):
        src=f"/home/user/n2/miesiac/tydzien_{tydz(i)}/{'facebook' if fb else 'tiktok'}/{d.strftime('%m-%d')}_{name}{'_fb' if fb else ''}.mp4"
        dst=sciezka(i,'2wieczor',name,fb); os.makedirs(os.path.dirname(dst),exist_ok=True); shutil.copy(src,dst)
def harmonogram():
    for w in range(1,5):
        txt=[f'TYDZIEŃ {w}: 2 filmy dziennie (rano i wieczorem), ten sam film na TikToku i Facebooku',
             'Godziny: rano pon–pt 12:00, sob–ndz 10:30; wieczór pon–pt 19:30, sob–ndz 20:00.',
             'Przy publikacji ZAWSZE włącz etykietę SI (FB: „Dodaj etykietę SI”, TT: „Treść wygenerowana przez AI”).','']
        for i in range(30):
            if tydz(i)!=w: continue
            d,_=termin(i); we=d.weekday()>=5
            nw=W[order[i]]; ov=V[i]
            for pora,godz,name,o,tags,plik in (('RANO','10:30' if we else '12:00',nw[0],nw[3],nw[4],'1rano'),('WIECZÓR','20:00' if we else '19:30',ov[0],ov[3],ov[5],'2wieczor')):
                txt+=['='*60,f"{d.strftime('%d.%m')} ({DNI[d.weekday()]}) {pora}, {godz}",'',
                      f"TIKTOK: tiktok/{d.strftime('%m-%d')}_{plik}_{name}.mp4",'',opis(o,tags,i,False),'',
                      f"FACEBOOK: facebook/{d.strftime('%m-%d')}_{plik}_{name}_fb.mp4",'',opis(o,tags,i,True),'']
        p=f'{OUT}tydzien_{w}/00_HARMONOGRAM_I_OPISY.txt'; os.makedirs(os.path.dirname(p),exist_ok=True)
        open(p,'w').write('\n'.join(txt))
if __name__=='__main__':
    only=sys.argv[1:]
    for i in range(30):
        if not only: stare(i)
        w=W[order[i]]
        if only and w[0] not in only: continue
        for fb in (False,True): make(i,w,fb)
    harmonogram()
