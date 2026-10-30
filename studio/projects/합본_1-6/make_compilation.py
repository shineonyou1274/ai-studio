#!/usr/bin/env python3
"""소울체인지 1~6화 몰아보기(가로 16:9, 사장님 2026-10-30 "1-6을 하나로 편집해서 한번 올리고 싶어. 어색한 거 빼고 자연스럽게").

구성: 여는 카드(3초) → 화마다 [장 카드 1.6초 → 본편] → 맺는 카드(4초)
화면: 가운데 세로 영상(608x1080), 양옆은 같은 영상을 크게 흐리고 어둡게. 왼쪽 위에 지금 화 번호·제목.
화마다 뺀 것: 각 화의 고정 엔딩·다음 편 카드, 첫 화면 제목 띠(4~6화 0.62초), 2화 앞 1화 다시 보기·제목 카드(0~3.0초).
음량: 화마다 -14 LUFS로 맞춤.
사용: python3 make_compilation.py [--v N]
"""
import pathlib, subprocess, sys, json
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
P = HERE.parent
KIT = pathlib.Path('/home/user/youtube-ops/series/_soulchange_kit')
F = str(KIT / 'fonts/Jua-Regular.ttf'); f = lambda s: ImageFont.truetype(F, s)
TAG = 'v' + (sys.argv[sys.argv.index('--v') + 1] if '--v' in sys.argv else '1')
B = HERE / f'build_{TAG}'; B.mkdir(exist_ok=True)
W, H, FPS = 1920, 1080, 30
NAVY, RED, MINT, CREAM, YEL, OUTL = (16, 24, 58), (216, 35, 42), (45, 190, 156), (255, 246, 227), (255, 226, 90), (11, 16, 48)

def dur(p): return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)], capture_output=True, text=True).stdout)
EPS = [  # (화, 파일, 시작, 끝, 장 제목)
    (1, P / 'soulchange-ep01/05_편집/ep1_공개본_720p.mp4', 0.0, 42.50, '생결 쓰고 PC방 간 날'),
    (2, P / 'soulchange-ep02/05_편집/ep2_공개본_720p.mp4', 3.00, 52.30, '담임 몸으로 등교한 날'),
    (3, P / 'soulchange-ep03/05_편집/ep3_공개본_720p.mp4', 0.0, 42.40, '두통도 생결 되나요?'),
    (4, P / 'soulchange-ep04/05_편집/ep4_v19.mp4', 0.62, None, '해외 로밍 문자'),
    (5, P / 'soulchange-ep05/05_편집/ep5_v8b.mp4', 0.62, None, '교감쌤, 이거 갑질이잖아요!'),
    (6, P / 'soulchange-ep06/05_편집/ep6_v6.mp4', 0.62, None, '텀블러에 침을'),
]
EPS = [(n, p, a, b if b else round(dur(p) - 5.7, 3), t) for n, p, a, b, t in EPS]


def run(cmd):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True)
    if r.returncode: raise SystemExit(' '.join(map(str, cmd))[:400] + '\n' + r.stderr[-1500:])


def card(path, lines, sub=None):
    im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
    d.rounded_rectangle([760, 250, 1160, 360], radius=18, fill=RED, outline=OUTL, width=6)
    d.text((960, 305), '한입극장', font=f(84), fill=CREAM, stroke_width=7, stroke_fill=OUTL, anchor='mm')
    for i, (s, size, col) in enumerate(lines):
        d.text((960, 470 + i * 130), s, font=f(size), fill=col, stroke_width=8 if col == YEL else 0, stroke_fill=OUTL, anchor='mm')
    if sub: d.text((960, 940), sub, font=f(40), fill=(200, 205, 225), anchor='mm')
    im.save(path)


def label(path, n, title):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(60, 60), (360, 60), (382, 100), (360, 140), (60, 140)], fill=MINT + (255,), outline=OUTL + (255,))
    d.text((210, 100), f'소울체인지 {n}화', font=f(46), fill=CREAM, stroke_width=4, stroke_fill=OUTL, anchor='mm')
    d.text((64, 170), title, font=f(44), fill=(255, 255, 255), stroke_width=5, stroke_fill=OUTL)
    d.text((W - 64, H - 60), '@twistbite_drama', font=f(34), fill=(220, 224, 240), anchor='rs')
    im.save(path)


def still(png, secs, out, tone=None):
    a = ['-f', 'lavfi', '-t', str(secs), '-i', 'anullsrc=r=48000:cl=stereo']
    run(['ffmpeg', '-y', '-v', 'error', '-loop', '1', '-t', secs, '-i', png, *a, '-vf', f'fps={FPS},format=yuv420p,fade=t=in:d=0.3,fade=t=out:st={secs - 0.3}:d=0.3',
         '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-c:a', 'aac', '-b:a', '192k', '-shortest', out])


def lufs(p, a, b):
    r = subprocess.run(['ffmpeg', '-ss', str(a), '-to', str(b), '-i', str(p), '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    import re; return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', r)[-1])


segs = []
card(B / 'open.png', [('소울체인지', 120, YEL), ('1~6화 몰아보기', 96, CREAM)], '생결 쓰고 PC방 간 날, 담임과 몸이 바뀌었다')
still(B / 'open.png', 3.0, B / 'seg_00_open.mp4'); segs.append(B / 'seg_00_open.mp4')
for n, p, a, b, title in EPS:
    card(B / f'ch{n}.png', [(f'{n}화', 140, YEL), (title, 80, CREAM)])
    still(B / f'ch{n}.png', 1.6, B / f'seg_{n}a.mp4'); segs.append(B / f'seg_{n}a.mp4')
    label(B / f'lab{n}.png', n, title)
    g = -14.0 - lufs(p, a, b); d_ = b - a
    fc = (f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,fps={FPS},split[v1][v2];"
          f"[v1]scale={W}:-2,crop={W}:{H},gblur=sigma=40,eq=brightness=-0.18:saturation=0.8[bg];"
          f"[v2]scale=-2:{H}[fg];[bg][fg]overlay=(W-w)/2:0[c];[c][1:v]overlay=0:0,format=yuv420p,"
          f"fade=t=in:d=0.25,fade=t=out:st={d_ - 0.25:.3f}:d=0.25[v];"
          f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,volume={g:.2f}dB,"
          f"alimiter=limit=0.89:level=false,afade=t=in:d=0.15,afade=t=out:st={d_ - 0.25:.3f}:d=0.25[a]")
    out = B / f'seg_{n}b.mp4'
    run(['ffmpeg', '-y', '-v', 'error', '-i', p, '-i', B / f'lab{n}.png', '-filter_complex', fc, '-map', '[v]', '-map', '[a]',
         '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-c:a', 'aac', '-b:a', '192k', '-r', FPS, out])
    segs.append(out); print(n, round(a, 2), round(b, 2), f'{g:+.1f}dB')
card(B / 'close.png', [('7화는 쇼츠에서', 96, YEL), ('화요일 18시', 96, CREAM)], '구독하고 다음 이야기도 함께 봐요')
still(B / 'close.png', 4.0, B / 'seg_99_close.mp4'); segs.append(B / 'seg_99_close.mp4')
(B / 'list.txt').write_text(''.join(f"file '{s}'\n" for s in segs))
out = HERE / f'소울체인지_1-6화_몰아보기_{TAG}.mp4'
run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', B / 'list.txt', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19',
     '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out])
chap, t = [], 3.0
for n, p, a, b, title in EPS:
    chap.append(f'{int(t // 60)}:{int(t % 60):02d} {n}화 {title}'); t += 1.6 + (b - a)
(HERE / f'챕터_{TAG}.txt').write_text('0:00 시작\n' + '\n'.join(chap) + '\n', encoding='utf-8')
print('OK', out, round(dur(out), 1)); print('\n'.join(chap))
