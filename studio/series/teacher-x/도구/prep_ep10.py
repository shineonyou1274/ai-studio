# 교사X 10화 편집 준비 — 샌드박스 ~/ep11 에서 실행
# 1) 채택 녹음 → ed/aNN.wav (05 = 05·06t2·07 묶음, 09 = 09t3·10 묶음, 20 = 새 대사 n1)
# 2) 영상 vNN.mp4 (16 = 16b 다시 뽑은 것), 반응 k2NN.mp4
# 3) timing.json(말소리 시작·끝·낱말), off.json(클립 말소리 시작 차이), voice_end.json(클립 말소리 끝)
import subprocess, json, wave, os, glob, shutil
import numpy as np
E='/home/user/ep11/'; A=E+'ed/'; V=E+'v/'; AU=E+'au/'; os.makedirs(A,exist_ok=True)
SRC={'01':'a01.wav','02':'a02.mp3','03':'a03.mp3','04':'a04.mp3','05':'c0507.mp3','08':'a08.mp3','09':'c0910.mp3','11':'a11.mp3','12':'a12.mp3','13':'a13.mp3',
     '14':'a14.mp3','15':'a15.mp3','16':'a16.mp3','17':'a17.mp3','18':'a18.mp3','19':'a19.mp3','20':'a20n1.wav'}
for c,s in SRC.items(): subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-i',AU+s,'-ac','1','-ar','44100',A+f'a{c}.wav'],check=True)
if os.path.exists(V+'v16b.mp4'):
    if not os.path.exists(V+'v16_old.mp4'): shutil.copy(V+'v16.mp4',V+'v16_old.mp4')
    shutil.copy(V+'v16b.mp4',V+'v16.mp4')
from faster_whisper import WhisperModel
m=WhisperModel('medium',compute_type='int8'); TJ={}
for c in SRC:
    f=A+f'a{c}.wav'; w=wave.open(f); a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float); sr=w.getframerate()
    h=int(sr*0.02); r=np.array([np.sqrt((a[i*h:(i+1)*h]**2).mean()) for i in range(len(a)//h)]); v=np.where(r>max(r.max()*0.05,150))[0]
    segs,_=m.transcribe(f,language='ko',word_timestamps=True)
    TJ[c]={'dur':round(len(a)/sr,2),'v0':round(v[0]*0.02,2),'v1':round((v[-1]+1)*0.02,2),'words':[(x.word.strip(),round(x.start,2),round(x.end,2)) for s in segs for x in s.words]}
json.dump(TJ,open(E+'timing.json','w'),ensure_ascii=False)
def env(p):
    b=subprocess.check_output(['ffmpeg','-nostdin','-v','error','-i',p,'-ac','1','-ar','16000','-f','s16le','-']); a=np.frombuffer(b,np.int16).astype(float)
    h=320; return np.array([np.sqrt((a[i*h:(i+1)*h]**2).mean()) for i in range(len(a)//h)])
OFF,VE={},{}
for p in sorted(glob.glob(V+'v[0-9][0-9].mp4')):
    c=os.path.basename(p)[1:3]
    try: r=env(p)
    except subprocess.CalledProcessError: continue
    if len(r)==0 or r.max()<50: continue
    v=np.where(r>max(r.max()*0.08,100))[0]
    VE['v'+c]=round((v[-1]+1)*0.02,2)
    if c in TJ: OFF[c]=max(0.0,round(v[0]*0.02-TJ[c]['v0'],2))
json.dump(OFF,open(E+'off.json','w')); json.dump(VE,open(E+'voice_end.json','w'))
print('OFF',OFF); print('VE',VE); print({c:(TJ[c]['v0'],TJ[c]['v1'],' '.join(w for w,_,_ in TJ[c]['words'])) for c in TJ})
