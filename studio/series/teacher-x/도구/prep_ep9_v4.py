# 교사X 9화 v4 준비 — 샌드박스 ~/ep10 에서 실행 (prep_ep9.py 다음)
# 1) 다시 녹음(교감 현실 톤 05·06·08·10·14·16, 다해 17~21 A테이크, 학부모 p1·p2) → ed/aNN.wav (옛것은 ed/v3old/)
# 2) 새 입 영상 v/v4/*.mp4 → v/vNN.mp4 (옛것은 v/v3old/)
# 3) timing.json 바뀐 줄 다시, off.json(말소리 시작 차이), voice_end.json(클립 말소리 끝 — 듣는 화면 확인용, 사장님 11/23 지적)
import subprocess, json, wave, os, shutil, glob
import numpy as np
E = '/home/user/ep10/'; A = E + 'ed/'; V = E + 'v/'
os.makedirs(A + 'v3old', exist_ok=True); os.makedirs(V + 'v3old', exist_ok=True)
NEW = {'05': 'x05', '06': 'x06', '08': 'x08', '10': 'x10', '14': 'x14', '16': 'x16', '17': 'x17A', '18': 'x18A', '19': 'x19A', '20': 'x20A', '21': 'x21A', 'p1': 'xP1', 'p2': 'xP2'}
for c, src in NEW.items():
    if os.path.exists(A + f'a{c}.wav') and not os.path.exists(A + f'v3old/a{c}.wav'): shutil.copy(A + f'a{c}.wav', A + f'v3old/a{c}.wav')
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', A + f'v4/{src}.wav', '-ac', '1', '-ar', '44100', A + f'a{c}.wav'], check=True)
for p in glob.glob(V + 'v4/*.mp4'):
    n = os.path.basename(p)
    if os.path.exists(V + n) and not os.path.exists(V + 'v3old/' + n): shutil.copy(V + n, V + 'v3old/' + n)
    shutil.copy(p, V + n)
from faster_whisper import WhisperModel
m = WhisperModel('medium', compute_type='int8'); TJ = json.load(open(E + 'timing.json'))
for c in NEW:
    f = A + f'a{c}.wav'; w = wave.open(f); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float); sr = w.getframerate()
    h = int(sr * 0.02); r = np.array([np.sqrt((a[i*h:(i+1)*h]**2).mean()) for i in range(len(a)//h)]); v = np.where(r > max(r.max()*0.05, 150))[0]
    segs, _ = m.transcribe(f, language='ko', word_timestamps=True)
    TJ[c] = {'dur': round(len(a)/sr, 2), 'v0': round(v[0]*0.02, 2), 'v1': round((v[-1]+1)*0.02, 2), 'words': [(x.word.strip(), round(x.start, 2), round(x.end, 2)) for s in segs for x in s.words]}
json.dump(TJ, open(E + 'timing.json', 'w'), ensure_ascii=False)
def env(p):
    b = subprocess.check_output(['ffmpeg', '-nostdin', '-v', 'error', '-i', p, '-ac', '1', '-ar', '16000', '-f', 's16le', '-']); a = np.frombuffer(b, np.int16).astype(float)
    h = 320; return np.array([np.sqrt((a[i*h:(i+1)*h]**2).mean()) for i in range(len(a)//h)])
OFF, VE = {}, {}
for p in sorted(glob.glob(V + 'v[0-9][0-9].mp4')):
    c = os.path.basename(p)[1:3]
    try: r = env(p)
    except subprocess.CalledProcessError: continue
    if len(r) == 0 or r.max() < 50: continue
    v = np.where(r > max(r.max()*0.08, 100))[0]
    VE['v' + c] = round((v[-1]+1)*0.02, 2)
    if c in TJ: OFF[c] = max(0.0, round(v[0]*0.02 - TJ[c]['v0'], 2))
json.dump(OFF, open(E + 'off.json', 'w')); json.dump(VE, open(E + 'voice_end.json', 'w'))
print('OFF', OFF); print('VOICE_END', VE); print({c: (TJ[c]['v0'], TJ[c]['v1']) for c in NEW})
