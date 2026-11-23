# 교사X 9화 화면 글자 그림 v1 — 자리·기울기는 잰 값(cv2 연결 성분·minAreaRect, 격자 4배 환산)
# 907 폰 알림 거품 4개: 가운데 (1054,737)(1029,852)(1005,968)(981,1084), 긴 변 444, 화면 시계방향 +8.8~9.2° → PIL -9
# 920 조직도: 빨간 칸 (758,899) 안쪽 442x240 / 아래 칸 가운데 x 384·636·884·1132, y 1420, 약 220x300
# 924 점수 동그라미 (620,880)·(1332,888) / 927 표: 칸 가운데 x 326·706·1106, 머리줄 y 1120, 강조줄 y 1192, 제목 y 905
# 903 노트북 화면 답 칸 x 688~1400, y 1000~1320 / 908 제목칸 y 672~800, 빨간 접수칸 (782,1836) / 901 리본 꼬리 x 1073~1316, y 1545~2215
# 샌드박스 ~/ep10 에서 실행 → ~/ep10/ov/*.png
from PIL import Image, ImageDraw, ImageFont
import os, random
H = '/home/user/'; I = H + 'ep10/img/'; O = H + 'ep10/ov/'; os.makedirs(O, exist_ok=True)
F = H + 'fonts/NanumGothicBold.ttf'; FR = H + 'fonts/NanumGothic.ttf'; PEN = H + 'fonts/NanumPen.ttf'
def f(s, p=F): return ImageFont.truetype(p, s)
def tag(im, x=60, y=120):
    d = ImageDraw.Draw(im); d.rounded_rectangle((x, y, x + 340, y + 76), radius=16, fill=(0, 0, 0)); d.text((x + 170, y + 38), '극 중 설정', font=f(38), fill='white', anchor='mm')
def tilted(im, center, lines, size, angle, fill=(25, 25, 35), font=F, gap=1.3, width=None, pad=10, align='lm'):
    ft = f(size, font); lh = int(size * gap)
    w = width or int(max(ft.getlength(l) for l in lines)) + pad * 2; h = lh * len(lines) + pad * 2
    L = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for k, l in enumerate(lines):
        y = pad + lh * k + lh / 2
        d.text((pad, y) if align == 'lm' else (w / 2, y), l, font=ft, fill=fill, anchor=align)
    R = L.rotate(angle, resample=Image.BICUBIC, expand=True)
    im.paste(R, (int(center[0] - R.width / 2), int(center[1] - R.height / 2)), R)

# 901 리본 꼬리 '축 승진'(세로)
im = Image.open(I + 'i901.png').convert('RGB'); d = ImageDraw.Draw(im)
for k, ch in enumerate('축승진'):
    d.text((1190, 1700 + k * 105), ch, font=f(86), fill=(255, 236, 160), anchor='mm', stroke_width=3, stroke_fill=(120, 0, 0))
im.save(O + 'o901.png')

# 903 학생 노트북 AI 답(가운데에 '초록 고양이' 노랑 바탕)
im = Image.open(I + 'i903.png').convert('RGB'); d = ImageDraw.Draw(im)
d.rounded_rectangle((680, 990, 1410, 1330), 14, fill=(250, 250, 252))
L = [('광합성은 빛 에너지를 화학 에너지로', None), ('바꾸는 과정입니다. 엽록체 속', None), ('엽록소가 빛을 흡수하는데, 마치 ', '초록 고양이'), ('처럼 잎은 햇빛을 머금고…', None)]
y = 1030
for t, hl in L:
    x = 705; d.text((x, y), t, font=f(40, FR), fill=(40, 40, 50), anchor='lm'); x += f(40, FR).getlength(t)
    if hl:
        w = f(40).getlength(hl); d.rectangle((x - 4, y - 26, x + w + 4, y + 26), fill=(255, 226, 60)); d.text((x, y), hl, font=f(40), fill=(20, 20, 20), anchor='lm')
    y += 78
im.save(O + 'o903.png')

# 906 보고서 7장이 하나씩 쌓임(장마다 '초록 고양이' 형광펜) — 906 책상 위에 코드로 그린 종이
bg = Image.open(I + 'i906.png').convert('RGB')
random.seed(9)
def page(k):
    p = Image.new('RGBA', (860, 1180), (252, 252, 248, 255)); d = ImageDraw.Draw(p)
    d.text((60, 70), '통합과학 수행평가 보고서', font=f(40), fill=(40, 40, 60))
    d.text((60, 125), f'{k}번째 학생', font=f(28, FR), fill=(120, 120, 130))
    y = 210
    for i in range(16):
        if i == 7:
            t1 = '엽록소가 빛을 흡수하는데, 마치 '; d.text((60, y), t1, font=f(32, FR), fill=(60, 60, 70), anchor='lm')
            x = 60 + f(32, FR).getlength(t1); w = f(32).getlength('초록 고양이')
            d.rectangle((x - 4, y - 22, x + w + 4, y + 22), fill=(255, 230, 40)); d.text((x, y), '초록 고양이', font=f(32), fill=(10, 10, 10), anchor='lm')
        else:
            d.rounded_rectangle((60, y - 8, 60 + random.randint(560, 740), y + 8), 6, fill=(200, 200, 205))
        y += 58
    return p
stack = bg.copy()
for k in range(1, 8):
    pg = page(k).rotate(random.uniform(-7, 7), resample=Image.BICUBIC, expand=True)
    stack.paste(pg, (int(760 - pg.width / 2 + random.randint(-50, 50)), int(1300 - pg.height / 2 + random.randint(-40, 40))), pg)
    stack.save(O + f'o906p{k}.png')

# 907 정우 폰 잠금화면 알림 4개(주말 밤·아침)
im = Image.open(I + 'i907.png').convert('RGB')
N = [((1054, 737), '토 23:41', 'AI 쓰지 말라는 말이 어디 있었나요?'), ((1029, 852), '일 07:12', '애들한테 함정을 판 거예요?'),
     ((1005, 968), '일 22:03', '내일 학교로 찾아가겠습니다.'), ((981, 1084), '일 22:05', '부재중 전화 3통')]
for (cx, cy), t, msg in N:
    tilted(im, (cx + 18, cy), [t + '  ' + msg], 22, -9, fill=(30, 30, 45), width=380)
im.save(O + 'o907.png')

# 908 민원 접수 화면(위쪽 국기·건물은 확대로 화면 밖)
im = Image.open(I + 'i908.png').convert('RGB'); d = ImageDraw.Draw(im)
d.text((900, 548), '국민신문고 · 민원 접수', font=f(34), fill='white', anchor='lm')
d.text((130, 736), '[민원] 수행평가 감점 이의 — 통합과학', font=f(42), fill=(30, 40, 70), anchor='lm')
d.text((1110, 1840), '접수 완료', font=f(58), fill=(200, 30, 30), anchor='lm')
tag(im, 1080, 900); im.save(O + 'o908.png')

# 920 민원대응팀 조직도
im = Image.open(I + 'i920.png').convert('RGB'); d = ImageDraw.Draw(im)
d.text((760, 700), '학교 민원대응팀', font=f(58), fill=(30, 50, 110), anchor='mm')
d.text((758, 870), '팀장', font=f(52), fill=(180, 20, 20), anchor='mm'); d.text((758, 950), '교감', font=f(78), fill=(20, 20, 30), anchor='mm')
for x, t in zip([384, 636, 884, 1132], ['행정\n실장', '교무\n부장', '학년\n부장', '상담\n교사']):
    d.multiline_text((x, 1420), t, font=f(46), fill=(30, 40, 70), anchor='mm', align='center', spacing=14)
tag(im, 1100, 260); im.save(O + 'o920.png')

# 924 같은 점수 두 장
im = Image.open(I + 'i924.png').convert('RGB'); d = ImageDraw.Draw(im)
for x, y in [(620, 880), (1332, 888)]:
    d.text((x, y), '18', font=f(96, PEN), fill=(200, 20, 30), anchor='mm')
d.text((380, 1840), 'AI가 쓴 보고서', font=f(46), fill=(255, 255, 255), anchor='mm', stroke_width=6, stroke_fill=(0, 0, 0))
d.text((1140, 1840), '밤새 손으로 쓴 보고서', font=f(46), fill=(255, 255, 255), anchor='mm', stroke_width=6, stroke_fill=(0, 0, 0))
im.save(O + 'o924.png')

# 927 인사 발령 화면
im = Image.open(I + 'i927.png').convert('RGB'); d = ImageDraw.Draw(im)
d.text((720, 905), '학교법인 ○○학원 인사 발령', font=f(50), fill=(20, 30, 70), anchor='mm')
for x, t in zip([326, 706, 1106], ['직위', '성명', '발령일']): d.text((x, 1120), t, font=f(38), fill=(40, 50, 80), anchor='mm')
for x, t in zip([326, 706, 1106], ['교장', '독고다해', '2027. 3. 1.']): d.text((x, 1192), t, font=f(44), fill=(160, 0, 0), anchor='mm')
for x, t in zip([326, 706, 1106], ['교감', '○○○', '유임']): d.text((x, 1280), t, font=f(36, FR), fill=(60, 60, 70), anchor='mm')
tag(im, 1120, 60); im.save(O + 'o927.png')
print('ok')
