# 녹음 쉼 줄이기: 앞뒤 무음 자르고, 0.4초 넘는 쉼만 0.3초로. 사용: python3 gentle.py in.mp3 out.wav
# 처리 뒤 silencedetect로 문장 사이 쉼이 0.25초 아래로 줄지 않았는지 확인할 것(실수표 C2)
import sys,subprocess,numpy as np,wave
src,dst=sys.argv[1],sys.argv[2]; sr=44100
a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','0','-i',src,'-ac','1','-ar',str(sr),'-f','s16le','-']),np.int16).astype(np.float32)
w=int(sr*0.02); n=len(a)//w; r=np.array([np.sqrt((a[i*w:(i+1)*w]**2).mean()) for i in range(n)])
th=max(r.max()*0.04,150); v=r>th
idx=np.where(v)[0]; s0=max(0,idx[0]-3); s1=min(n,idx[-1]+6)
keep=[]; i=s0;
while i<s1:
    if not v[i]:
        j=i
        while j<s1 and not v[j]: j+=1
        L=j-i
        keep.append((i, i+min(L,15) if L>20 else j))  # pauses >0.4s -> 0.3s
        i=j
    else:
        j=i
        while j<s1 and v[j]: j+=1
        keep.append((i,j)); i=j
out=np.concatenate([a[x*w:y*w] for x,y in keep]).astype(np.int16)
with wave.open(dst,'wb') as f: f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes(out.tobytes())
print(dst, round(len(out)/sr,2))
