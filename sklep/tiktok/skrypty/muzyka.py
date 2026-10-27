# pozytywka: "O Tannenbaum" (melodia ludowa, domena publiczna), 3/4, ok. 96 bpm
import numpy as np, wave
SR=44100; BPM=96; B=60/BPM
N={'G4':392.0,'A4':440.0,'B4':493.88,'C5':523.25,'D5':587.33,'E5':659.25,'F5':698.46,'G5':783.99,'A5':880.0,'C4':261.63,'F4':349.23,'G3':196.0,'E4':329.63,'D4':293.66}
line=[('G4',1),('C5',.75),('C5',.25),('C5',1.5),('D5',.5),('E5',.75),('E5',.25),('E5',1.5),('E5',.5),('D5',.5),('E5',.5),('F5',1),('B4',1),('D5',1),('C5',1),(None,1)]
mel=line*3
def bell(f,d,amp):
    t=np.arange(int(SR*min(d+1.2,3.0)))/SR
    env=np.exp(-t*3.2)
    s=(np.sin(2*np.pi*f*t)+.35*np.sin(2*np.pi*2*f*t)*np.exp(-t*5)+.18*np.sin(2*np.pi*3.01*f*t)*np.exp(-t*7)+.08*np.sin(2*np.pi*4.2*f*t)*np.exp(-t*9))
    att=np.minimum(1,t/0.010)
    return s*env*att*amp
tot=sum(d for _,d in mel)*B+3
out=np.zeros(int(SR*tot)); t0=0.0
for n,d in mel:
    if n:
        s=bell(N[n],d*B,.5); i=int(t0*SR); out[i:i+len(s)]+=s[:len(out)-i]
    t0+=d*B
# delikatny akompaniament: akord na każdy takt (3 ćwierćnuty), zaczyna po przedtakcie
t=1*B; bar=0; chords=[['C4','E4','G4'],['C4','E4','G4'],['G3','D4','F4'],['C4','E4','G4']]
while t<t0:
    ch=chords[bar%4]
    for k,n in enumerate(ch):
        s=bell(N[n],3*B,.10); i=int((t+k*0.02)*SR); out[i:i+len(s)]+=s[:len(out)-i]
    t+=3*B; bar+=1
# prosty pogłos
rev=np.zeros_like(out)
for dl,g in [(0.031,.35),(0.047,.3),(0.071,.25),(0.113,.2),(0.167,.15),(0.241,.1)]:
    k=int(dl*SR); rev[k:]+=out[:-k]*g
out=out+rev*.6
out=out/np.max(np.abs(out))*0.7
st=np.stack([out,np.roll(out,int(0.012*SR))*0.95],1)
w=wave.open('muzyka.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((st*32767).astype('<i2').tobytes()); w.close()
print('dlugosc',round(len(out)/SR,1))
