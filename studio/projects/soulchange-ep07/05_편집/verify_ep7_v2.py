"""5화 v1 확인: 길이, 음량/트루피크, 1초마다 프레임 contact sheet, 검은 프레임, 최종 믹스 받아쓰기 vs 자막 시간 비교.
사용: python3 verify_ep7_v1.py → contact_v1.png, build/verify.json
"""
import json, pathlib, re, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
import sys
TAG = sys.argv[1] if len(sys.argv) > 1 else 'v2'
B = HERE / f'build_{TAG}'
MP4 = HERE / f'ep7_{TAG}.mp4'
TL = json.load(open(HERE / f'timeline_{TAG}.json'))
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
    im = Image.fromarray(a).convert('RGBA')   # v3: 쇼츠 UI 흉내 — 아래 27%·위 6%에 반투명 상자
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.rectangle([0, int(th * 0.73), tw, th], fill=(255, 0, 0, 70)); od.rectangle([0, 0, tw, int(th * 0.06)], fill=(255, 0, 0, 70))
    sheet.paste(Image.alpha_composite(im, ov).convert('RGB'), (x, y + 24)); d.text((x + 4, y + 2), f'{t:.1f}s', font=ImageFont.truetype(F, 18), fill=(255, 230, 90))
sheet.save(HERE / f'contact_{TAG}.png')
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

# v3: 자막만 검은 바탕에 그려 아래 27%(y>1401)·위 6%(y<115)에 글자 픽셀이 있는지 0.1초마다 확인
KIT = '/home/user/youtube-ops/series/_soulchange_kit'
raw = subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i', f"color=c=black:s=1080x1920:r=10:d={TL['main']}",
                      '-vf', f"ass={B / 'ep7.ass'}:fontsdir={KIT}/fonts,format=gray", '-f', 'rawvideo', '-'], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, 1920, 1080)
low = [round(i / 10, 1) for i in range(len(fr)) if fr[i, 1402:].max() > 40]
top = [round(i / 10, 1) for i in range(len(fr)) if fr[i, :115].max() > 40]
lowest = int(max(np.nonzero(f.max(1) > 40)[0].max() for f in fr if f.max() > 40))
print('아래 27%에 자막 픽셀:', low[:10], len(low), ' 위 6%:', top[:10], len(top), ' 가장 낮은 자막 픽셀 y =', lowest)
# v3: 멈춰 보이는 구간(본편, 0.1초 간격 프레임 차이가 아주 작은 상태가 1초 넘게)
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(MP4), '-t', str(TL['main']), '-vf', 'fps=10,scale=108:192,format=gray', '-f', 'rawvideo', '-'],
                     capture_output=True).stdout
g = np.frombuffer(raw, np.uint8).reshape(-1, 192, 108).astype(float)
dif = np.abs(np.diff(g, axis=0)).mean(axis=(1, 2))
runs, st = [], None
for i, d_ in enumerate(dif):
    if d_ < 0.6 and st is None: st = i
    if d_ >= 0.6 and st is not None:
        if i - st >= 10: runs.append((st / 10, i / 10))
        st = None
if st is not None and len(dif) - st >= 10: runs.append((st / 10, len(dif) / 10))
print('1초 넘게 거의 안 움직이는 구간(차이<0.6):', runs)
# 속마음(영혼 목소리) vs 겉말(몸 목소리) 음높이
import parselmouth
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(MP4), '-ac', '1', '-ar', '16000', str(B / 'mono.wav')])
snd = parselmouth.Sound(str(B / 'mono.wav'))
def med(a, b):
    p = snd.extract_part(a, b).to_pitch(time_step=0.02, pitch_floor=70, pitch_ceiling=600).selected_array['frequency']; p = p[p > 0]
    return int(np.median(p)) if len(p) else None
for lid, l in TL['lines'].items():
    print(f"음높이 {lid}: {med(l['start'], l['end'])} Hz ({l['start']}–{l['end']})")
# 0.125초 프레임 시트(구간별)
def sheet(a, b, name, step=0.125):
    ts_ = [a + step * i for i in range(int(round((b - a) / step)) + 1)]
    tw, th = 162, 288; cols = 12
    sh = Image.new('RGB', (cols * tw, ((len(ts_) + cols - 1) // cols) * (th + 22)), (20, 20, 20)); dd = ImageDraw.Draw(sh)
    for i, t in enumerate(ts_):
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t}', '-i', str(MP4), '-frames:v', '1', '-vf', f'scale={tw}:{th}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                             capture_output=True).stdout
        x, y = (i % cols) * tw, (i // cols) * (th + 22)
        sh.paste(Image.frombytes('RGB', (tw, th), raw), (x, y + 22)); dd.text((x + 4, y + 2), f'{t:.3f}', font=ImageFont.truetype(F, 15), fill=(255, 230, 90))
    sh.save(HERE / name)
_c = {c['id']: c for c in TL['cuts']}
if TAG == 'v2':
    sheet(0.0, _c['K3b']['start'] + _c['K3b']['dur'], 'frames_v2_1_교무실-상담.png', 0.25)
    sheet(_c['K4']['start'], _c['K7']['start'] + 1.0, 'frames_v2_2_교실-향수.png', 0.25)
    sheet(_c['K7']['start'] + 1.0, TL['main'], 'frames_v2_3_욕-DM-허리.png', 0.25)
