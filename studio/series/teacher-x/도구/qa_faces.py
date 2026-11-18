# 교사X 얼굴 대조판 (재발방지 체크리스트 관문 C) — 그림이 나오면 영상 전에 인물별로 얼굴을 모아 나이·머리·안경을 비교
# 사용: python3 qa_faces.py faces.json [--out faces.jpg]
#   faces.json = {"교감": {"ref": "시트.png", "imgs": ["img/i701.png", "v/v05.mp4@1.2", ...]}, "다해": {...}}
#   (영상은 "파일@초"로 그 시각 프레임)
# 줄마다 맨 앞 = 기준(시트·1화 얼굴, 노란 테두리), 뒤 = 이번 화 컷. 얼굴을 못 찾은 칸은 빨강 '얼굴 못 찾음'.
# 얼굴 비교는 눈으로 한다. 이 도구는 크기·자리를 맞춰 나란히 놓아 줄 뿐이다.
import sys, os, json, subprocess, argparse, tempfile
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser(); ap.add_argument('map'); ap.add_argument('--out', default='faces.jpg')
ap.add_argument('--per-row', type=int, default=7); ap.add_argument('--fonts', default=os.path.expanduser('~/fonts'))
a = ap.parse_args()
FT = ImageFont.truetype(os.path.join(a.fonts, 'NanumGothicBold.ttf'), 16)
mp = os.path.expanduser('~/.cache/qa/face_yunet.onnx')
if not os.path.exists(mp):
    os.makedirs(os.path.dirname(mp), exist_ok=True)
    subprocess.run(['curl', '-sfL', '-o', mp, 'https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx'], check=True)
DET = cv2.FaceDetectorYN.create(mp, '', (320, 320), 0.6)
tmp = tempfile.mkdtemp()
base = os.path.dirname(os.path.abspath(a.map))

def load(src):
    if '@' in src and src.split('@')[0].endswith(('.mp4', '.mov')):
        f, t = src.rsplit('@', 1); o = os.path.join(tmp, f'{abs(hash(src))}.png')
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', t, '-i', os.path.join(base, f), '-frames:v', '1', o], check=True)
        return Image.open(o).convert('RGB')
    return Image.open(os.path.join(base, src)).convert('RGB')
def face(im):
    s = 1280 / max(im.size); sm = im.resize((int(im.width * s), int(im.height * s)))
    arr = cv2.cvtColor(np.asarray(sm), cv2.COLOR_RGB2BGR); DET.setInputSize((arr.shape[1], arr.shape[0]))
    _, r = DET.detect(arr)
    if r is None: return None
    x, y, w, h = max(r, key=lambda q: q[2] * q[3])[:4] / s
    m = 0.55; cx, cy = x + w / 2, y + h / 2 - h * 0.08; half = max(w, h) * (0.5 + m)
    return im.crop((int(cx - half), int(cy - half * 1.15), int(cx + half), int(cy + half * 1.15)))
TW, TH, LH = 180, 207, 22
M = json.load(open(a.map)); rows = []
for name, d in M.items():
    cells = [(d['ref'], True)] if d.get('ref') else []
    cells += [(s, False) for s in d['imgs']]
    for k in range(0, len(cells), a.per_row): rows.append((name if k == 0 else '', cells[k:k + a.per_row]))
S = Image.new('RGB', (110 + TW * a.per_row, (TH + LH) * len(rows)), (24, 24, 28)); dr = ImageDraw.Draw(S)
for r, (name, cells) in enumerate(rows):
    y = r * (TH + LH); dr.text((10, y + TH // 2), name, font=ImageFont.truetype(os.path.join(a.fonts, 'NanumGothicBold.ttf'), 26), fill='white')
    for c, (src, ref) in enumerate(cells):
        x = 110 + c * TW
        try: im = load(src); f = face(im)
        except Exception as e: im, f = None, None
        if f is not None: S.paste(f.resize((TW - 6, TH - 6)), (x + 3, y + 3))
        else:
            dr.rectangle([x + 3, y + 3, x + TW - 3, y + TH - 3], outline=(230, 50, 50), width=3); dr.text((x + 30, y + TH // 2), '얼굴 못 찾음', font=FT, fill=(230, 80, 80))
        if ref: dr.rectangle([x + 1, y + 1, x + TW - 1, y + TH - 1], outline=(255, 210, 60), width=4)
        dr.text((x + 4, y + TH + 2), ('기준 ' if ref else '') + os.path.basename(src)[:20], font=FT, fill=(220, 220, 220))
S.save(a.out, quality=80); print('ok', a.out, S.size)
