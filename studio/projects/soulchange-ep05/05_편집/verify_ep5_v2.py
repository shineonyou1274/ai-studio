"""5화 v1 확인: 길이, 음량/트루피크, 1초마다 프레임 contact sheet, 검은 프레임, 최종 믹스 받아쓰기 vs 자막 시간 비교.
사용: python3 verify_ep5_v2.py → contact_v2.png, build/verify.json
"""
import json, pathlib, re, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
B = HERE / 'build_v2'
MP4 = HERE / 'ep5_v2.mp4'
TL = json.load(open(HERE / 'timeline_v2.json'))
F = '/home/user/youtube-ops/series/_soulchange_kit/fonts/Jua-Regular.ttf'

dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', MP4], capture_output=True, text=True).stdout)
m = subprocess.run(['ffmpeg', '-i', MP4, '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', m)[-1]); TP = float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', m)[-1])
print(f'길이 {dur:.3f}s  음량 {I} LUFS  트루피크 {TP} dBTP')

# contact sheet: 0.5, 1.5, ... (1초마다)
N = int(dur); tw, th = 216, 384
sheet = Image.new('RGB', (10 * tw, ((N + 9) // 10) * (th + 24)), (20, 20, 20)); d = ImageDraw.Draw(sheet)
blacks = []
for i in range(N):
    t = i + 0.5
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t}', '-i', MP4, '-frames:v', '1', '-vf', f'scale={tw}:{th}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                         capture_output=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(th, tw, 3)
    if a.mean() < 12: blacks.append(t)
    x, y = (i % 10) * tw, (i // 10) * (th + 24)
    sheet.paste(Image.fromarray(a), (x, y + 24)); d.text((x + 4, y + 2), f'{t:.1f}s', font=ImageFont.truetype(F, 18), fill=(255, 230, 90))
sheet.save(HERE / 'contact_v2.png')
bd = subprocess.run(['ffmpeg', '-i', MP4, '-vf', 'blackdetect=d=0.1:pix_th=0.08', '-an', '-f', 'null', '-'], capture_output=True, text=True).stderr
bd = re.findall(r'black_start:([\d.]+) black_end:([\d.]+)', bd)
print('검은 프레임(1초 샘플):', blacks, ' blackdetect:', bd)

# 최종 믹스 받아쓰기 → 자막과 시작 시간 비교
from faster_whisper import WhisperModel
wm = WhisperModel('small', device='cpu', compute_type='int8')
a = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', MP4, '-t', str(TL['main']), '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'],
                                 capture_output=True).stdout, np.float32)
segs, _ = wm.transcribe(a, language='ko', word_timestamps=True, beam_size=5)
W = [(w.word.strip(), round(w.start, 2), round(w.end, 2)) for s in segs for w in s.words]
print('받아쓰기:', ' '.join(f'{w}@{s}' for w, s, _ in W))
# 자막마다: 자막 시작 근처(±1.5초)에서 첫 낱말이 비슷한 받아쓰기 낱말을 찾아 차이를 잰다
def norm(x): return re.sub(r'[^가-힣A-Za-z]', '', x)
rows = []
for a0, b0, txt in TL['subs']:
    first = norm(txt)[:2]
    cand = [(abs(s - a0), s, w) for w, s, _ in W if first and norm(w)[:2] == first and abs(s - a0) < 1.5]
    if cand:
        dlt, s, w = min(cand); rows.append(dict(sub=txt, sub_start=a0, heard=w, heard_start=s, diff=round(a0 - s, 2)))
    else:
        rows.append(dict(sub=txt, sub_start=a0, heard=None, heard_start=None, diff=None))
bad = [r for r in rows if r['diff'] is not None and abs(r['diff']) > 0.3]
for r in rows: print(f"  {r['sub_start']:6.2f} {r['sub'][:24]:26s} 들림 {r['heard']}@{r['heard_start']} 차 {r['diff']}")
print('0.3초 넘게 어긋난 줄:', bad)
json.dump(dict(duration=dur, I=I, TP=TP, blacks=blacks, blackdetect=bd, words=W, rows=rows, bad=bad), open(B / 'verify.json', 'w'), ensure_ascii=False, indent=1)
