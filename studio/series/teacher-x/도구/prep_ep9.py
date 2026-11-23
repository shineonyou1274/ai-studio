# 교사X 9화 편집 준비 — 샌드박스 ~/ep10 에서 실행
# 1) 채택 녹음 → ed/aNN.wav(44.1k 모노)  2) timing.json(말소리 시작·끝 + 낱말 시각)  3) off.json(클립 소리 ↔ 원래 녹음 상호상관)
# 채택 테이크(생성로그): 02=t4, 06=t2, 15=t4, 17=t2, 22=t2, 나머지 t1
import subprocess, json, wave, glob, os
import numpy as np
E = '/home/user/ep10/'; A = E + 'ed/'; V = E + 'v/'
TAKE = {'02': 'r02t4', '06': 'r06t2', '15': 'r15t4', '17': 'r17t2', '22': 'r22t2'}
codes = [f'{i:02d}' for i in range(1, 25)]
for c in codes:
    src = A + TAKE.get(c, 'r' + c) + '.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-ac', '1', '-ar', '44100', A + f'a{c}.wav'], check=True)
from faster_whisper import WhisperModel
m = WhisperModel('medium', compute_type='int8'); out = {}
for c in codes:
    f = A + f'a{c}.wav'; w = wave.open(f); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float); sr = w.getframerate()
    h = int(sr * 0.02); r = np.array([np.sqrt((a[i*h:(i+1)*h]**2).mean()) for i in range(len(a)//h)]); v = np.where(r > max(r.max()*0.05, 150))[0]
    segs, _ = m.transcribe(f, language='ko', word_timestamps=True)
    out[c] = {'dur': round(len(a)/sr, 2), 'v0': round(v[0]*0.02, 2), 'v1': round((v[-1]+1)*0.02, 2),
              'words': [(x.word.strip(), round(x.start, 2), round(x.end, 2)) for s in segs for x in s.words]}
json.dump(out, open(E + 'timing.json', 'w'), ensure_ascii=False)
def load(p, sr=8000):
    b = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(sr), '-f', 's16le', '-'])
    return np.abs(np.frombuffer(b, np.int16).astype(float))
off = {}
for c in codes:
    if not os.path.exists(V + f'v{c}.mp4'): continue
    try: a = load(V + f'v{c}.mp4')
    except subprocess.CalledProcessError: continue
    if len(a) == 0: continue
    r = load(A + f'a{c}.wav')
    k = np.convolve(a, np.ones(80)/80, 'same'); q = np.convolve(r, np.ones(80)/80, 'same')
    k -= k.mean(); q -= q.mean(); cc = np.correlate(k, q, 'full'); lag = (np.argmax(cc) - (len(q)-1)) / 8000
    off[c] = max(0.0, round(lag, 2))
json.dump(off, open(E + 'off.json', 'w'))
print('timing', {c: (out[c]['v0'], out[c]['v1']) for c in codes}); print('off', off)
