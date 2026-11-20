# 교사X 8화(폐강) 화면 글자 그림 v1 — 자리·기울기는 measure_obj.py로 잰 값(눈대중 금지, 재발방지 체크리스트 관문 C)
# 841 결과표: 머리줄 (795,627) 높이 78, 분홍 줄 (763,1054) 높이 67, 기울기 0 / 칸 경계 x 90·314·574·862·1146·1436
# 844 세특 화면: 머리줄 가운데 (1015,739) 화면 시계방향 +3.6° → PIL -3.6
# 846 종이: 표 줄 화면 시계방향 -10° → PIL +10, 펜촉 (880,1930) 오른쪽 아래 여백에 손글씨
# 847 폰 알림: (1011,1011) 화면 시계방향 +11.2° → PIL -11.2, 가로 403·세로 104
# 샌드박스 ~/ep9 에서 실행 → ~/ep9/ov/*.png. '극 중 설정' 표시.
from PIL import Image, ImageDraw, ImageFont
import os
H = '/home/user/'; I = H + 'ep9/img/'; O = H + 'ep9/ov/'; os.makedirs(O, exist_ok=True)
F = H + 'fonts/NanumGothicBold.ttf'; PEN = H + 'fonts/NanumPen.ttf'
def f(s, p=F): return ImageFont.truetype(p, s)
def tag(im, x=60, y=120):
    d = ImageDraw.Draw(im); d.rounded_rectangle((x, y, x + 340, y + 76), radius=16, fill=(0, 0, 0)); d.text((x + 170, y + 38), '극 중 설정', font=f(38), fill='white', anchor='mm')
def tilted(im, center, lines, size, angle, fill=(25, 25, 35), font=F, gap=1.3, align='mm', width=None, pad=12):
    ft = f(size, font); lh = int(size * gap)
    w = width or int(max(ft.getlength(l) for l in lines)) + pad * 2; h = lh * len(lines) + pad * 2
    L = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for k, l in enumerate(lines):
        y = pad + lh * k + lh / 2
        d.text((pad, y) if align == 'lm' else (w / 2, y), l, font=ft, fill=fill, anchor='lm' if align == 'lm' else 'mm')
    R = L.rotate(angle, resample=Image.BICUBIC, expand=True)
    im.paste(R, (int(center[0] - R.width / 2), int(center[1] - R.height / 2)), R)

# 841 수강신청 결과표
im = Image.open(I + 'i841.png').convert('RGB'); d = ImageDraw.Draw(im)
X = [90, 314, 574, 862, 1146, 1436]; cx = [(X[i] + X[i + 1]) / 2 for i in range(5)]
for c, t in zip(cx, ['과목', '학년', '신청', '담당', '결과']):
    d.text((c, 627), t, font=f(40), fill='white', anchor='mm')
rows = [('문학', '2', '142명', '독고다해', '개설'), ('확률과 통계', '2', '98명', '김○○', '개설'), ('영어Ⅱ', '2', '121명', '박○○', '개설'),
        ('한국지리', '2', '64명', '이○○', '개설'), ('물리학', '2', '27명', '최○○', '개설')]
for k, r in enumerate(rows):
    y = 700 + k * 72 - 6
    for c, t in zip(cx, r): d.text((c, y), t, font=f(34), fill=(35, 40, 55), anchor='mm')
for c, t, col in zip(cx, ['세포와 물질대사', '2', '3명', '안정우', '폐강'], [(120, 10, 20)] * 4 + [(200, 0, 0)]):
    d.text((c, 1054), t, font=f(36 if t != '세포와 물질대사' else 30), fill=col, anchor='mm')
tag(im, 1100, 60); im.save(O + 'o841.png')

# 844 세특 화면
im = Image.open(I + 'i844.png').convert('RGB')
tilted(im, (1080, 712), ['세부능력 및 특기사항'], 44, -3.6, fill=(20, 40, 90))
tilted(im, (585, 690), ['이름'], 38, -3.6, fill=(20, 40, 90))
tilted(im, (720, 548), ['통합과학 · 학생 312명'], 34, -3.6, fill=(240, 245, 255))
tag(im, 1100, 60); im.save(O + 'o844.png')  # v2: 왼쪽 위 시간·설명 글자와 닿아 오른쪽 위로

# 846 빨간 만년필 손글씨
im = Image.open(I + 'i846.png').convert('RGB')
tilted(im, (940, 2190), ['교사 1명 = 과목 4개', '= 시험 4개', '= 세특 312명'], 72, 10, fill=(185, 20, 30), font=PEN, gap=1.15, align='lm', width=520)
im.save(O + 'o846.png')

# 847 폰 알림
im = Image.open(I + 'i847.png').convert('RGB')
tilted(im, (1011, 1011), ['[학교법인] 재단 사무국', '차기 교장 공모 일정 안내'], 30, -11.2, fill=(25, 25, 35), gap=1.35, align='lm', width=400)
tag(im, 60, 120); im.save(O + 'o847.png')

# 838 마지막 프레임: 2K 원본에서 얼굴 쪽 9:16
im = Image.open(I + 'i838.png').convert('RGB'); W, Hh = im.size
cw = int(W * 0.62); ch = int(cw * 16 / 9); x0 = int(W * 0.2); y0 = 0
im.crop((x0, y0, x0 + cw, y0 + ch)).resize((1520, 2688), Image.LANCZOS).save(O + 'o838f.png')
print('ok')
