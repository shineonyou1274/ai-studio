# 교사X 글자 전수 확인 도구 (재발방지 체크리스트 관문 E). 사장님 11/18 "매번 텍스트 문제야"
# 하는 일
#  1) 자막 파일(.ass)의 글자 하나하나를 따로 그려서 글자 상자를 잼 → 화면 가장자리에 닿으면 '잘림 위험',
#     같은 시각에 뜬 다른 글자 상자와 겹치면 '겹침', 얼굴(입 쪽 아래 절반)과 겹치면 '얼굴 가림'
#  2) 그림 속 글자 컷(타임라인 json)과 모든 자막 구간의 시작·중간·끝 프레임을 완성 영상에서 뽑아 확인판(jpg)으로 묶음
#  3) 경고 목록을 qa_text_report.md로 씀 → 경고 0건 + 확인판을 눈으로 본 뒤에만 "글자 확인했다"고 보고
# 사용(샌드박스): python3 qa_text.py 완성.mp4 sub.ass [--tl timeline.json] [--out 폴더]
#   timeline.json = 편집 스크립트가 남기는 [[시작초, 끝초, "이름"], ...] (그림 속 글자 컷, 이름이 o로 시작하는 그림)
import sys, os, re, json, subprocess, argparse, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument('video'); ap.add_argument('ass')
ap.add_argument('--tl', default=None)
ap.add_argument('--out', default=None)
ap.add_argument('--fonts', default=os.path.expanduser('~/fonts'))
ap.add_argument('--edge', type=int, default=8, help='가장자리에서 이만큼(px) 안이면 잘림 위험')
ap.add_argument('--rows', type=int, default=4, help='확인판 한 장에 넣을 줄 수')
a = ap.parse_args()
OUT = a.out or os.path.join(os.path.dirname(os.path.abspath(a.video)), 'qa_text')
os.makedirs(OUT, exist_ok=True)
FB = os.path.join(a.fonts, 'NanumGothicBold.ttf')
def font(s): return ImageFont.truetype(FB, s)

def run(c): subprocess.run(c, check=True)
def probe(v):
    o = subprocess.check_output(['ffprobe', '-v', '0', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,r_frame_rate:format=duration', '-of', 'json', v])
    j = json.loads(o); s = j['streams'][0]; n, d = s['r_frame_rate'].split('/')
    return s['width'], s['height'], float(n) / float(d), float(j['format']['duration'])
W, H, FPS, DUR = probe(a.video)

# ---- 자막 읽기
def t2s(t): h, m, s = t.split(':'); return int(h) * 3600 + int(m) * 60 + float(s)
def s2t(x): x = max(0, x); return f"{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}"
txt = open(a.ass, encoding='utf-8').read()
head, body = txt.split('[Events]', 1)
fmt_line = [l for l in body.splitlines() if l.startswith('Format:')]
EVS = []
for l in body.splitlines():
    if not l.startswith('Dialogue:'): continue
    p = l[len('Dialogue:'):].split(',', 9)
    EVS.append(dict(st=t2s(p[1].strip()), en=t2s(p[2].strip()), style=p[3].strip(), text=p[9], raw=p))
def vis(s): return re.sub(r'\{[^}]*\}', '', s).replace('\\N', ' / ')

# ---- 글자 하나씩 따로 그려 상자 재기(마젠타 바탕 → 바탕과 다른 픽셀)
tmp = tempfile.mkdtemp()
def measure(ev, i):
    d = ev['en'] - ev['st']
    p = list(ev['raw']); p[1] = s2t(0); p[2] = s2t(d)
    f = os.path.join(tmp, f'e{i}.ass')
    open(f, 'w', encoding='utf-8').write(head + '[Events]\n' + '\n'.join(fmt_line) + '\nDialogue:' + ','.join(p) + '\n')
    ts = [max(0, min(d - 0.05, x)) for x in (0.08, d * 0.5, d - 0.06)]
    sel = '+'.join(f'eq(n,{n})' for n in sorted({int(round(t * FPS)) for t in ts}))
    o = os.path.join(tmp, f'e{i}_%d.png')
    run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'color=c=0xFF00FF:s={W}x{H}:r={FPS}:d={d + 0.1:.3f}',
         '-vf', f"ass={f}:fontsdir={a.fonts},select='{sel}'", '-vsync', '0', o])
    box = None; k = 1
    while os.path.exists(o % k):
        m = np.asarray(Image.open(o % k).convert('RGB')).astype(int); os.remove(o % k); k += 1
        diff = np.abs(m - np.array([255, 0, 255])).sum(2) > 60
        ys, xs = np.nonzero(diff)
        if len(xs) < 30: continue
        b = [xs.min(), ys.min(), xs.max(), ys.max()]
        box = b if box is None else [min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3])]
    return box

# ---- 얼굴 찾기(YuNet, 없으면 건너뜀)
FACE = None
try:
    import cv2
    mp = os.path.expanduser('~/.cache/qa/face_yunet.onnx')
    if not os.path.exists(mp):
        os.makedirs(os.path.dirname(mp), exist_ok=True)
        run(['curl', '-sfL', '-o', mp, 'https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx'])
    FACE = cv2.FaceDetectorYN.create(mp, '', (W, H), 0.7)
except Exception as e:
    print('얼굴 찾기 없이 진행:', e)
def faces(im):
    if FACE is None: return []
    import cv2
    arr = cv2.cvtColor(np.asarray(im.convert('RGB')), cv2.COLOR_RGB2BGR)
    FACE.setInputSize((arr.shape[1], arr.shape[0]))
    _, r = FACE.detect(arr)
    return [] if r is None else [[int(x[0]), int(x[1]), int(x[0] + x[2]), int(x[1] + x[3])] for x in r]

def inter(b1, b2):
    return max(0, min(b1[2], b2[2]) - max(b1[0], b2[0])) * max(0, min(b1[3], b2[3]) - max(b1[1], b2[1]))

# ---- 완성 영상에서 프레임 뽑기(한 번에)
items = []
for i, ev in enumerate(EVS):
    items.append(dict(kind='자막', st=ev['st'], en=ev['en'], label=f"{ev['style']} {vis(ev['text'])}", ev=ev, i=i))
if a.tl:
    for s, e, nm in json.load(open(a.tl)):
        items.append(dict(kind='그림글자', st=s, en=e, label=nm))
items.sort(key=lambda x: x['st'])
for it in items:
    d = it['en'] - it['st']
    it['fr'] = [int(round(min(DUR - 0.15, it['st'] + x) * FPS)) for x in (min(0.06, d / 3), d / 2, max(d - 0.06, d * 2 / 3))]
need = sorted({n for it in items for n in it['fr']})
fdir = os.path.join(tmp, 'f'); os.makedirs(fdir)
FR = {}
for n in need:  # 프레임마다 따로 찾아감(긴 select 식은 ffmpeg가 못 읽음)
    FR[n] = os.path.join(fdir, f'{n:05d}.jpg')
    run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', f'{min(n / FPS + 0.5 / FPS, DUR - 0.12):.4f}', '-i', a.video, '-frames:v', '1', '-q:v', '3', FR[n]])
    if not os.path.exists(FR[n]):  # 끝 프레임은 뒤에서 찾음
        run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-sseof', '-0.3', '-i', a.video, '-frames:v', '1', '-q:v', '3', FR[n]])

# ---- 검사
WARN = []
for it in items:
    if it['kind'] != '자막': continue
    it['box'] = b = measure(it['ev'], it['i'])
    if b is None: continue
    e = a.edge
    if b[0] < e or b[1] < e or b[2] > W - 1 - e or b[3] > H - 1 - e:
        WARN.append((it['st'], '잘림 위험', it['label'], f'상자 {b}'))
    fs = faces(Image.open(FR[it['fr'][1]]))
    for f in fs:
        mouth = [f[0], (f[1] + f[3]) // 2, f[2], f[3]]  # 얼굴 아래 절반(입 쪽)
        if inter(b, mouth) > 0.15 * (mouth[2] - mouth[0]) * (mouth[3] - mouth[1]):
            WARN.append((it['st'], '얼굴 가림', it['label'], f'얼굴 {f}'))
    it['faces'] = fs
subs = [x for x in items if x['kind'] == '자막' and x.get('box')]
for i in range(len(subs)):
    for j in range(i + 1, len(subs)):
        x, y = subs[i], subs[j]
        if min(x['en'], y['en']) - max(x['st'], y['st']) > 0.05 and inter(x['box'], y['box']) > 0:
            WARN.append((max(x['st'], y['st']), '겹침', x['label'] + '  ↔  ' + y['label'], ''))

# ---- 확인판
TW = 240; TH = int(TW * H / W); LH = 64
sheets = []
def tile(it, n):
    im = Image.open(FR[n]).convert('RGB').resize((TW, TH)); dr = ImageDraw.Draw(im); sx = TW / W
    bad = any(abs(w[0] - it['st']) < 0.01 and w[2].startswith(it['label'][:20]) for w in WARN)
    if it.get('box'):
        b = it['box']; dr.rectangle([b[0] * sx, b[1] * sx, b[2] * sx, b[3] * sx], outline=(255, 40, 40) if bad else (40, 255, 80), width=2)
    for f in it.get('faces', []):
        dr.rectangle([f[0] * sx, f[1] * sx, f[2] * sx, f[3] * sx], outline=(60, 160, 255), width=1)
    return im
for k in range(0, len(items), a.rows):
    grp = items[k:k + a.rows]
    S = Image.new('RGB', (TW * 3, (TH + LH) * len(grp)), (20, 20, 24)); dr = ImageDraw.Draw(S)
    for r, it in enumerate(grp):
        y = r * (TH + LH)
        lab = f"{it['st']:.2f}–{it['en']:.2f}s [{it['kind']}] {it['label']}"
        dr.text((6, y + 4), lab[:46], font=font(18), fill=(255, 230, 120))
        dr.text((6, y + 30), lab[46:92], font=font(18), fill=(255, 230, 120))
        for c, n in enumerate(it['fr']):
            S.paste(tile(it, n), (c * TW, y + LH))
    p = os.path.join(OUT, f'sheet_{k // a.rows + 1:02d}.jpg'); S.save(p, quality=72); sheets.append(p)

WARN.sort()
rep = [f'# 글자 전수 확인 — {os.path.basename(a.video)}', '',
       f'- 자막 {len([x for x in items if x["kind"] == "자막"])}개, 그림 속 글자 컷 {len([x for x in items if x["kind"] != "자막"])}개, 확인판 {len(sheets)}장({OUT})',
       f'- 자동 경고 {len(WARN)}건 (잘림 위험·겹침·얼굴 가림). 확인판의 초록 상자 = 글자, 빨강 = 경고, 파랑 = 얼굴',
       '- 자동 검사는 자막만 잼. **그림 속 글자(기울기·잘림)는 확인판을 눈으로 봐야 함**', '']
rep += [f'| {t:.2f}s | {k} | {l} | {m} |' for t, k, l, m in WARN] if WARN else ['경고 없음']
open(os.path.join(OUT, 'qa_text_report.md'), 'w').write('\n'.join(rep) + '\n')
print('\n'.join(rep))
