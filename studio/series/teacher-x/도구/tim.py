# 편집용 녹음(ed/aXX.wav)마다 소리 시작 v0·끝 v1(소리 크기 기준)과 단어 시각을 timing.json으로.
# 자를 때는 단어 시각이 아니라 v0/v1·RMS 쉼을 쓴다(받아쓰기 시각은 실제 말끝보다 0.3초 빠를 수 있음).
import json,glob,numpy as np,wave
from faster_whisper import WhisperModel
m=WhisperModel("medium",compute_type="int8"); out={}
for f in sorted(glob.glob('/home/user/ep2/ed/a*.wav')):
    c=f[-6:-4]; w=wave.open(f); a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float); sr=w.getframerate()
    h=int(sr*0.02); r=np.array([np.sqrt((a[i*h:(i+1)*h]**2).mean()) for i in range(len(a)//h)]); v=np.where(r>max(r.max()*0.05,150))[0]
    segs,_=m.transcribe(f,language='ko',word_timestamps=True)
    words=[(x.word.strip(),round(x.start,2),round(x.end,2)) for s in segs for x in s.words]
    out[c]={'dur':round(len(a)/sr,2),'v0':round(v[0]*0.02,2),'v1':round((v[-1]+1)*0.02,2),'words':words}
json.dump(out,open('/home/user/ep2/timing.json','w'),ensure_ascii=False)
print('done')
