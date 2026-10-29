"""소울체인지 커버 3종(웃음 A · 반전 B · 긴장 C) — 회차 설정은 아래 EP. 틀 = 7화 커버 + 상황 띠(2026-10-29).
사용: python3 make_covers.py <회차> → projects/soulchange-epNN/05_편집/cover_epN_A/B/C.png + 비교
"""
import subprocess, pathlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import sys
P = pathlib.Path('/home/user/ai-studio/studio/projects')
KE = pathlib.Path('/home/user/youtube-ops/series/_soulchange_kit/episodes')
N = int(sys.argv[1])
HERE = P / f'soulchange-ep{N:02d}' / '05_편집'
F = '/home/user/youtube-ops/series/_soulchange_kit/fonts/Jua-Regular.ttf'
f = lambda s: ImageFont.truetype(F, s)
W, H = 1080, 1920
NAVY, RED, MINT, CREAM, YEL, OUTL = (16, 24, 58), (216, 35, 42), (45, 190, 156), (255, 246, 227), (255, 226, 90), (11, 16, 48)

E6, E7, E8 = (P / f'soulchange-ep0{n}/04_생성물/clips' for n in (6, 7, 8))
EP = {
    6: {'A': dict(src=KE / 'ep6/clips/K08.mp4', t=1.0, z=1.30, cx=0.45, top=0.04, strip='교감의 의심을 받던 날', hook=['교감한테', '"교장 포스세요!"']),
        'B': dict(src=E6 / 'H2_K6.mp4', t=0.45, z=1.30, cx=0.45, top=0.04, strip='텀블러 소문을 듣자마자', hook=['담임 몸에서', '여고생 목소리가?']),
        'C': dict(src=KE / 'ep6/clips/K11.mp4', t=1.0, z=1.15, cx=0.55, top=0.0, strip='텀블러에 누가 침을 뱉었다', hook=['창밖 벤치에', '혼자 앉은 아이'])},
    7: {'A': dict(src=KE / 'ep7/clips/K06.mp4', t=0.3, z=1.25, cx=0.45, top=0.05, strip='어머니 가방에서 난 냄새', hook=['향수 칭찬했다가', '학부모 폭발']),
        'B': dict(src=E7 / 'K12_elem.mp4', t=3.5, z=1.45, cx=0.42, top=0.10, strip='텀블러 건 학생 어머니가 왔다', hook=['그 욕,', '어디서 배웠을까']),
        'C': dict(src=E7 / 'K7_elem.mp4', t=4.2, z=1.15, cx=0.50, top=0.02, strip='학부모 상담실', hook=['"우리 애는', '문제없어요"'])},
    8: {'A': dict(src=E8 / 'K1.mp4', t=5.75, z=1.35, cx=0.50, top=0.06, strip='상담 보고서를 써야 하는데', hook=['50대 담임이', '머리를 귀 뒤로?!']),
        'B': dict(src=E8 / 'H2_v2.mp4', t=5.6, z=1.30, cx=0.50, top=0.04, strip='딸기우유를 보자마자', hook=['쌤 목소리', '왜 저래?']),
        'C': dict(src=E8 / 'K11b_v2.mp4', t=6.6, z=1.25, cx=0.50, top=0.02, strip='교감이 수화기를 든 순간', hook=['병가 중이던 담임이', '돌아왔다'])},
}
VARIANTS = EP[N]


def grab(src, t):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', str(src), '-vf', 'scale=1080:1920:flags=lanczos',
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
    d.text((245, 232), f'소울체인지 {N}화', font=f(50), fill=CREAM, stroke_width=5, stroke_fill=OUTL, anchor='mm')
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
    im = cover(v); im.save(HERE / f'cover_ep{N}_{k}.png'); ims.append(im)
sheet = Image.new('RGB', (W * 3 + 80, H + 140), (240, 240, 240)); d = ImageDraw.Draw(sheet)
for i, (k, im) in enumerate(zip(VARIANTS, ims)):
    sheet.paste(im, (20 + i * (W + 20), 120)); d.text((20 + i * (W + 20) + W // 2, 60), k, font=f(80), fill=(30, 30, 30), anchor='mm')
sheet.resize((sheet.width // 3, sheet.height // 3)).save(HERE / f'cover_ep{N}_비교.png')
print('OK')
