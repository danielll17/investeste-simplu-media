import numpy as np, wave, sys
sr=44100; bpm=76; beat=60/bpm; dur=float(sys.argv[1]) if len(sys.argv)>1 else 34
t_total=int(sr*dur); out=np.zeros(t_total)
def note(f): return 440*2**((f-69)/12)
def env(n,a=0.02,r=0.3):
    e=np.ones(n); A=min(int(a*sr),n//2); R=min(int(r*sr),n//2)
    e[:A]=np.linspace(0,1,A); e[-R:]*=np.linspace(1,0,R); return e
chords=[[57,60,64],[53,57,60],[48,52,55],[55,59,62]]  # Am F C G
bar=beat*4; t=0; i=0
while t<dur:
    c=chords[i%4]; n=int(min(bar,dur-t)*sr); tt=np.arange(n)/sr
    pad=sum(0.6*np.sin(2*np.pi*note(m)*tt)+0.2*np.sin(2*np.pi*note(m)*2*tt+0.3) for m in c)
    pad+=0.5*np.sin(2*np.pi*note(c[0]-12)*tt)
    s=int(t*sr); out[s:s+n]+=0.08*pad*env(n,0.4,0.6)
    # arpeggio
    for k in range(8):
        st=t+k*beat/2
        if st>=dur: break
        m=c[k%3]+12; ln=int(0.5*sr); ln=min(ln,t_total-int(st*sr)); tt2=np.arange(ln)/sr
        pl=np.sin(2*np.pi*note(m)*tt2)*np.exp(-tt2*6)
        p=int(st*sr); out[p:p+ln]+=0.06*pl
    # soft kick on 1 and 3
    for k in (0,2):
        st=t+k*beat
        if st>=dur: break
        ln=min(int(0.25*sr),t_total-int(st*sr)); tt3=np.arange(ln)/sr
        kk=np.sin(2*np.pi*(55+60*np.exp(-tt3*30))*tt3)*np.exp(-tt3*12)
        p=int(st*sr); out[p:p+ln]+=0.25*kk
    t+=bar; i+=1
# simple lowpass smoothing
k=np.ones(8)/8; out=np.convolve(out,k,'same')
fade=int(2*sr); out[-fade:]*=np.linspace(1,0,fade); out[:int(0.5*sr)]*=np.linspace(0,1,int(0.5*sr))
out=out/np.max(np.abs(out))*0.6
w=wave.open(sys.argv[2],'w'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
