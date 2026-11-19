# 교사X 커버 v2 — 썸네일_판단기준_v1.md(사장님 11/18 "클릭하고 싶게, 궁금해서")에 맞춘 틀
#  - 얼굴을 찾아 화면 폭의 약 45%로 키워 위쪽에 둠(감정이 큰 얼굴 하나)
#  - 큰 글씨 2줄(한 줄 9자 안), 강조 낱말 1개만 노랑, 나머지 흰색. 빨간 띠 없음. 회차 표시는 작게
#  - feed(): 폭 180px(쇼츠 피드 크기) 비교판
# 샌드박스 실행. 얼굴 찾기 모델은 qa_text/qa_faces와 같은 YuNet(~/.cache/qa/face_yunet.onnx)
import os, subprocess
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
F = '/home/user/fonts/BlackHanSans-Regular.ttf'
if not os.path.exists(F): F = '/home/user/fonts/NanumGothicBold.ttf'
FS = '/home/user/fonts/NanumGothicBold.ttf'
W, H = 1080, 1920
MP = os.path.expanduser('~/.cache/qa/face_yunet.onnx')

def face_box(im):
    if not os.path.exists(MP):
        os.makedirs(os.path.dirname(MP), exist_ok=True)
        subprocess.run(['curl', '-sfL', '-o', MP, 'https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx'], check=True)
    s = 1280 / max(im.size); sm = im.resize((int(im.width * s), int(im.height * s)))
    det = cv2.FaceDetectorYN.create(MP, '', (sm.width, sm.height), 0.6)
    _, r = det.detect(cv2.cvtColor(np.asarray(sm), cv2.COLOR_RGB2BGR))
    if r is None: return None
    x, y, w, h = max(r, key=lambda q: q[2] * q[3])[:4] / s
    return x, y, w, h

def cover(src, lines, out, key=None, face_frac=0.45, face_y=0.30, ep='교사X 4화', dx=0.0):
    """lines: 2줄 문자열, key: 노랑으로 칠할 낱말(줄 안에 그대로 있어야 함)"""
    im = Image.open(src).convert('RGB'); fb = face_box(im)
    if fb:
        x, y, w, h = fb; sc = W * face_frac / w
        sc = max(sc, W / im.width, H / im.height)  # 화면을 다 채우게
        big = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
        cx = (x + w / 2) * sc + dx * W; cy = (y + h / 2) * sc
        x0 = int(min(max(0, cx - W / 2), big.width - W)); y0 = int(min(max(0, cy - H * face_y), big.height - H))
        im = big.crop((x0, y0, x0 + W, y0 + H))
    else:
        r = max(W / im.width, H / im.height); im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1)).crop((0, 0, W, H))
    # 아래쪽 어둡게(글자 자리)
    g = Image.new('L', (1, H))
    for yy in range(H): g.putpixel((0, yy), int(max(0, (yy - H * 0.50) / (H * 0.50)) ** 1.2 * 225))
    im.paste(Image.new('RGB', (W, H), (5, 6, 12)), (0, 0), g.resize((W, H)))
    d = ImageDraw.Draw(im)
    fe = ImageFont.truetype(FS, 38); d.rounded_rectangle((44, 56, 270, 124), 12, fill=(0, 0, 0)); d.text((64, 66), ep, font=fe, fill=(235, 235, 235))
    y = 1250
    for t in lines:
        size = 150
        while ImageFont.truetype(F, size).getlength(t) > W - 90: size -= 4
        f = ImageFont.truetype(F, size); x = (W - f.getlength(t)) / 2
        parts = t.split(key) if key and key in t else [t]
        for i, p in enumerate(parts):
            d.text((x, y), p, font=f, fill='white', stroke_width=8, stroke_fill='black'); x += f.getlength(p)
            if i < len(parts) - 1:
                d.text((x, y), key, font=f, fill=(255, 214, 0), stroke_width=8, stroke_fill='black'); x += f.getlength(key)
        y += int(size * 1.18)
    im.save(out); return out

NAVY = (16, 28, 58); YEL = (255, 214, 0)
def series(src, ep, title, lines, out, face_frac=0.42, face_y=0.36, dx=0.0):
    """시리즈 통일 틀(사장님 11/18 "썸네일만 봐도 제목과 회차 알 수 있게 통일감"):
    위 = 남색 띠 [교사X] + 노란 칸 [N화] + 「회차 제목」 (모든 화 같은 자리·색·크기)
    아래 = 댓글을 부르는 질문(A vs B / 더 ○○한 건?). lines = [[(글자, 색), ...], ...] 줄마다 조각"""
    tmp = out + '.base.png'
    cover(src, [], tmp, face_frac=face_frac, face_y=face_y, ep='', dx=dx)
    im = Image.open(tmp).convert('RGB'); os.remove(tmp); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, 230), fill=NAVY)                       # 위 띠(앞의 회차 칸을 덮음)
    fl = ImageFont.truetype(F, 92); d.text((50, 62), '교사X', font=fl, fill='white')
    x = 50 + fl.getlength('교사X') + 26
    fn = ImageFont.truetype(F, 80); n = f'{ep}화'; nw = fn.getlength(n)
    d.rounded_rectangle((x, 56, x + nw + 40, 176), 18, fill=YEL); d.text((x + 20, 70), n, font=fn, fill=NAVY)
    x += nw + 40 + 30
    ft = 84  # 「」는 Black Han Sans에 없어 빈칸으로 나옴 → 괄호 없이
    while ImageFont.truetype(F, ft).getlength(title) > W - x - 40: ft -= 2
    d.text((x, 116), title, font=ImageFont.truetype(F, ft), fill='white', anchor='lm')
    y = 1200
    # 글자 뒤 어두운 띠(흰 셔츠 위 흰 글자가 사라지던 문제, 11/19 3화 '야'·6화 '약')
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.rounded_rectangle((24, y - 40, W - 24, y + int(140 * 1.2) * len(lines) + 20), 36, fill=(0, 0, 0, 165))
    im = Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB'); d = ImageDraw.Draw(im)
    for segs in lines:
        txt = ''.join(t for t, c in segs); size = 140
        while ImageFont.truetype(F, size).getlength(txt) > W - 80: size -= 4
        f = ImageFont.truetype(F, size); x = (W - f.getlength(txt)) / 2
        for t, c in segs:
            d.text((x, y), t, font=f, fill=c, stroke_width=8, stroke_fill='black'); x += f.getlength(t)
        y += int(size * 1.2)
    im.save(out); return out

def feed(paths, labels, out):
    """쇼츠 피드 크기(폭 180px)로 나란히 — 판단기준 7"""
    tw, th = 180, 320; fl = ImageFont.truetype(FS, 15)
    S = Image.new('RGB', (len(paths) * (tw + 12) + 12, th + 40), (255, 255, 255)); d = ImageDraw.Draw(S)
    for i, (p, l) in enumerate(zip(paths, labels)):
        S.paste(Image.open(p).convert('RGB').resize((tw, th), Image.LANCZOS), (12 + i * (tw + 12), 8)); d.text((12 + i * (tw + 12), th + 14), l, font=fl, fill=(0, 0, 0))
    S.save(out, quality=88); return out
