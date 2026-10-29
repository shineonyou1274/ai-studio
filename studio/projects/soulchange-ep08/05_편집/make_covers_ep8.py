"""8화 맞춤 커버 3종(1080x1920) — 7화 커버 틀 + 상황 고정 띠(처음 보는 사람용, 2026-10-29 채널 분석 반영).
A 웃음: K1 귀 뒤로 넘기는 담임 몸 / B 반전: H2_v2 손으로 입 막은 담임 몸 / C 긴장: K11b_v2 역광 최 쌤
사용: python3 make_covers_ep8.py → cover_ep8_A.png, cover_ep8_B.png, cover_ep8_C.png, cover_ep8_비교.png
"""
import subprocess, pathlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
CL = HERE.parent / '04_생성물/clips'
F = '/home/user/youtube-ops/series/_soulchange_kit/fonts/Jua-Regular.ttf'
f = lambda s: ImageFont.truetype(F, s)
W, H = 1080, 1920
NAVY, RED, MINT, CREAM, YEL, OUTL = (16, 24, 58), (216, 35, 42), (45, 190, 156), (255, 246, 227), (255, 226, 90), (11, 16, 48)

VARIANTS = {
    'A': dict(src='K1.mp4', t=5.75, z=1.35, cx=0.50, top=0.06, strip='상담 보고서를 써야 하는데', hook=['50대 담임이', '머리를 귀 뒤로?!']),
    'B': dict(src='H2_v2.mp4', t=5.6, z=1.30, cx=0.50, top=0.04, strip='딸기우유를 보자마자', hook=['쌤 목소리', '왜 저래?']),
    'C': dict(src='K11b_v2.mp4', t=6.6, z=1.25, cx=0.50, top=0.02, strip='교감이 수화기를 든 순간', hook=['병가 중이던 담임이', '돌아왔다']),
}


def grab(src, t):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', str(CL / src), '-vf', 'scale=1080:1920:flags=lanczos',
                          '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    return Image.frombytes('RGB', (W, H), raw[:W * H * 3])


def cover(v):
    shot = grab(v['src'], v['t'])
    zw, zh = int(W * v['z']), int(H * v['z']); shot = shot.resize((zw, zh), Image.LANCZOS)
    x0 = int(min(max(v['cx'] * zw - W / 2, 0), zw - W)); y0 = int(zh * v['top'])
    shot = shot.crop((x0, y0, x0 + W, y0 + H))
    shot = Image.fromarray(np.clip(np.asarray(shot, float) * 1.05 + 5, 0, 255).astype(np.uint8))
    cv = Image.new('RGB', (W, H), NAVY); cv.paste(shot.crop((0, 0, W, 1160)), (0, 70))
    g = Image.new('L', (W, H), 0); gd = ImageDraw.Draw(g)
    for y in range(880, 1240): gd.line([(0, y), (W, y)], fill=int(255 * min(1, (y - 880) / 340)))
    cv = Image.composite(Image.new('RGB', (W, H), NAVY), cv, g); d = ImageDraw.Draw(cv)
    # 한입극장 명판 + 민트 리본
    d.rounded_rectangle([56, 52, 480, 178], radius=18, fill=RED, outline=OUTL, width=6)
    d.text((268, 115), '한입극장', font=f(98), fill=CREAM, stroke_width=8, stroke_fill=OUTL, anchor='mm')
    d.polygon([(60, 196), (430, 196), (452, 232), (430, 268), (60, 268)], fill=MINT, outline=OUTL)
    d.line([(60, 196), (430, 196), (452, 232), (430, 268), (60, 268), (60, 196)], fill=OUTL, width=5)
    d.text((245, 232), '소울체인지 8화', font=f(50), fill=CREAM, stroke_width=5, stroke_fill=OUTL, anchor='mm')
    # 상황 고정 띠(처음 보는 사람도 한눈에)
    tag = '담임 몸에 여고생 영혼'
    tw = d.textlength(tag, font=f(46))
    d.rounded_rectangle([60, 292, 60 + tw + 48, 362], radius=34, fill=(255, 255, 255), outline=OUTL, width=4)
    d.text((84, 327), tag, font=f(46), fill=OUTL, anchor='lm')
    # 빨간 띠 + 노란 훅
    tw = d.textlength(v['strip'], font=f(48))
    d.rectangle([70, 1158, 70 + tw + 56, 1246], fill=(232, 88, 84))
    d.text((98, 1202), v['strip'], font=f(48), fill=(255, 255, 255), anchor='lm')
    fs = 132 if max(len(x) for x in v['hook']) <= 8 else 112
    for i, line in enumerate(v['hook']):
        d.text((70, 1300 + i * (fs + 36)), line, font=f(fs), fill=YEL, stroke_width=10, stroke_fill=OUTL, anchor='la')
    d.text((540, 1832), '@twistbite_drama', font=f(42), fill=(220, 224, 240), anchor='mm')
    return cv


ims = []
for k, v in VARIANTS.items():
    im = cover(v); im.save(HERE / f'cover_ep8_{k}.png'); ims.append(im)
sheet = Image.new('RGB', (W * 3 + 80, H + 140), (240, 240, 240)); d = ImageDraw.Draw(sheet)
for i, (k, im) in enumerate(zip(VARIANTS, ims)):
    sheet.paste(im, (20 + i * (W + 20), 120)); d.text((20 + i * (W + 20) + W // 2, 60), k, font=f(80), fill=(30, 30, 30), anchor='mm')
sheet.resize((sheet.width // 3, sheet.height // 3)).save(HERE / 'cover_ep8_비교.png')
print('OK')
