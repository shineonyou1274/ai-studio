# 교사X 10화 v4 준비 — 9번 새 대사(모든 책임은, 교장인 제가 지겠습니다) 녹음·입 영상, 16·18 입 영상 다시 → timing/off/voice_end 다시
import subprocess, json, wave, os, shutil
import numpy as np
E='/home/user/ep11/'; A=E+'ed/'; V=E+'v/'; AU=E+'au/'
subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-i',AU+'c09n10.mp3','-ac','1','-ar','44100',A+'a09.wav'],check=True)
for c,src in [('09','v09n'),('16','v16c'),('18','v18n')]:
    if not os.path.exists(V+f'v{c}_v3.mp4'): shutil.copy(V+f'v{c}.mp4',V+f'v{c}_v3.mp4')
    shutil.copy(V+src+'.mp4',V+f'v{c}.mp4')
from faster_whisper import WhisperModel
m=WhisperModel('medium',compute_type='int8'); TJ=json.load(open(E+'timing.json'))
f=A+'a09.wav'; w=wave.open(f); a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float); sr=w.getframerate()
h=int(sr*0.02); r=np.array([np.sqrt((a[i*h:(i+1)*h]**2).mean()) for i in range(len(a)//h)]); v=np.where(r>max(r.max()*0.05,150))[0]
segs,_=m.transcribe(f,language='ko',word_timestamps=True)
TJ['09']={'dur':round(len(a)/sr,2),'v0':round(v[0]*0.02,2),'v1':round((v[-1]+1)*0.02,2),'words':[(x.word.strip(),round(x.start,2),round(x.end,2)) for s in segs for x in s.words]}
json.dump(TJ,open(E+'timing.json','w'),ensure_ascii=False)
def env(p):
    b=subprocess.check_output(['ffmpeg','-nostdin','-v','error','-i',p,'-ac','1','-ar','16000','-f','s16le','-']); a=np.frombuffer(b,np.int16).astype(float)
    return np.array([np.sqrt((a[i*320:(i+1)*320]**2).mean()) for i in range(len(a)//320)])
OFF=json.load(open(E+'off.json')); VE=json.load(open(E+'voice_end.json'))
for c in ['09','16','18']:
    r=env(V+f'v{c}.mp4'); v=np.where(r>max(r.max()*0.08,100))[0]
    VE['v'+c]=round(float((v[-1]+1)*0.02),2); OFF[c]=max(0.0,round(float(v[0]*0.02-TJ[c]['v0']),2))
json.dump(OFF,open(E+'off.json','w')); json.dump(VE,open(E+'voice_end.json','w'))
print(TJ['09']['words']); print({c:(OFF[c],VE['v'+c]) for c in ['09','16','18']})
