"""7화 맞춤 커버(1080x1920) — 4화 cover_ep4_v3.png 틀: 위 왼쪽 한입극장 명판 + 민트 리본 "소울체인지 N화",
위 60% 장면, 아래 남색, 빨간 작은 띠(상황 한 줄) + 노란 큰 글씨 두 줄(훅), 맨 아래 @twistbite_drama. Jua 하나만.
배경 = K12_elem.mp4 3.5초 — 담임 몸이 폰을 쥐고 놀라 입을 벌린 얼굴(영상 "아동학대요?!" 장면).
사용: python3 make_cover_ep7.py → cover_ep7_v1.png
"""
import subprocess, pathlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE.parent / '04_생성물/clips/K12_elem.mp4'
F = '/home/user/youtube-ops/series/_soulchange_kit/fonts/Jua-Regular.ttf'
f = lambda s: ImageFont.truetype(F, s)
W, H = 1080, 1920
NAVY, RED, MINT, CREAM, YEL, OUTL = (16, 24, 58), (216, 35, 42), (45, 190, 156), (255, 246, 227), (255, 226, 90), (11, 16, 48)

raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', '3.5', '-i', str(SRC), '-vf', 'scale=1080:1920:flags=lanczos',
                      '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
shot = Image.frombytes('RGB', (W, H), raw[:W * H * 3])
# 얼굴이 크게, 명판 아래로 오게 1.35배(얼굴 원본 x≈0.38·W)
z = 1.45; zw, zh = int(W * z), int(H * z); shot = shot.resize((zw, zh), Image.LANCZOS)
x0 = int(min(max(0.42 * zw - W / 2, 0), zw - W)); shot = shot.crop((x0, int(zh * 0.10), x0 + W, int(zh * 0.10) + H))
shot = Image.fromarray(np.clip(np.asarray(shot, float) * 1.04 + 4, 0, 255).astype(np.uint8))   # 조금 밝게

cv = Image.new('RGB', (W, H), NAVY)
cv.paste(shot.crop((0, 0, W, 1160)), (0, 70))
# 장면 아래끝을 남색으로 부드럽게
g = Image.new('L', (W, H), 0); gd = ImageDraw.Draw(g)
for y in range(880, 1240):
    gd.line([(0, y), (W, y)], fill=int(255 * min(1, (y - 880) / 340)))
cv = Image.composite(Image.new('RGB', (W, H), NAVY), cv, g)
d = ImageDraw.Draw(cv)

# 한입극장 명판 + 민트 리본(4화와 같은 자리·크기)
d.rounded_rectangle([56, 52, 480, 178], radius=18, fill=RED, outline=OUTL, width=6)
d.text((268, 115), '한입극장', font=f(98), fill=CREAM, stroke_width=8, stroke_fill=OUTL, anchor='mm')
d.polygon([(60, 196), (430, 196), (452, 232), (430, 268), (60, 268)], fill=MINT, outline=OUTL)
d.line([(60, 196), (430, 196), (452, 232), (430, 268), (60, 268), (60, 196)], fill=OUTL, width=5)
d.text((245, 232), '소울체인지 7화', font=f(50), fill=CREAM, stroke_width=5, stroke_fill=OUTL, anchor='mm')

# 빨간 작은 띠(상황 한 줄)
strip = '텀블러 건 학생 어머니가 왔다'   
tw = d.textlength(strip, font=f(48))
d.rectangle([70, 1158, 70 + tw + 56, 1246], fill=(232, 88, 84))
d.text((98, 1202), strip, font=f(48), fill=(255, 255, 255), anchor='lm')
# 노란 큰 글씨 두 줄(훅)
for i, line in enumerate(['그 욕,', '어디서 배웠을까']):
    d.text((70, 1300 + i * 168), line, font=f(132), fill=YEL, stroke_width=10, stroke_fill=OUTL, anchor='la')
d.text((540, 1832), '@twistbite_drama', font=f(42), fill=(220, 224, 240), anchor='mm')
cv.save(HERE / 'cover_ep7_v1.png')
print('OK', HERE / 'cover_ep7_v1.png')
