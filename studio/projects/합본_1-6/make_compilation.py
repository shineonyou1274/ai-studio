#!/usr/bin/env python3
"""소울체인지 1~6화 몰아보기 v2 = Gemini 합본 검수 반영: 2화 끝 "지금은 네가 담임이잖아"·"망했다" 살림, 4~6화 첫 대사 살림(영상만 첫 화면 띠 뒤 프레임으로 멈춤),
4화 단톡 머리 "3학년 2반" → "2학년 3반"(2화 알람과 통일), 오픈런·현체 풀이, 4화·6화 장 카드 부제, 오른쪽 위 영혼 안내(분홍·하늘).

--- v1 ---
소울체인지 1~6화 몰아보기(가로 16:9, 사장님 2026-10-30 "1-6을 하나로 편집해서 한번 올리고 싶어. 어색한 거 빼고 자연스럽게").

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
EPS = [  # (화, 파일, 소리 시작, 영상 시작, 끝, 장 제목, 장 부제, 풀이 [(파일 기준 시각, 끝, 글)])
    (1, P / 'soulchange-ep01/05_편집/ep1_공개본_720p.mp4', 0.0, 0.0, 42.50, '생결 쓰고 PC방 간 날', '1부 - 지우네 반 이야기', []),
    (2, P / 'soulchange-ep02/05_편집/ep2_공개본_720p.mp4', 2.90, 2.90, 54.80, '담임 몸으로 등교한 날', '', []),
    (3, P / 'soulchange-ep03/05_편집/ep3_공개본_720p.mp4', 0.0, 0.0, 42.40, '두통도 생결 되나요?', '', [(5.8, 10.5, '오픈런 = 가게 문 열자마자\n달려가 줄 서기')]),
    (4, P / 'soulchange-ep04/05_편집/ep4_v19.mp4', 0.0, 0.62, None, '해외 로밍 문자', '3화 끝, 그 문자를 보낸 학부모는?', []),
    (5, P / 'soulchange-ep05/05_편집/ep5_v8b.mp4', 0.0, 0.62, None, '교감쌤, 이거 갑질이잖아요!', '', [(16.2, 21.0, '현체 = 현장체험학습\n(학교 밖 체험, 출석 인정)')]),
    (6, P / 'soulchange-ep06/05_편집/ep6_v6.mp4', 0.0, 0.62, None, '텀블러에 침을', '2부 - 옆 반 최 선생님 이야기', []),
]
EPS = [(n, p, a, v, b if b else round(dur(p) - 5.7, 3), t, sub, notes) for n, p, a, v, b, t, sub, notes in EPS]
PATCH = {4: (7.45, 9.95)}     # 4화 단톡 머리 글씨 덮기(원본 1080x1920 기준)


def run(cmd):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True)
    if r.returncode: raise SystemExit(' '.join(map(str, cmd))[:400] + '\n' + r.stderr[-1500:])


def card(path, lines, sub=None, top=None):
    im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
    d.rounded_rectangle([760, 250, 1160, 360], radius=18, fill=RED, outline=OUTL, width=6)
    d.text((960, 305), '한입극장', font=f(84), fill=CREAM, stroke_width=7, stroke_fill=OUTL, anchor='mm')
    for i, (s, size, col) in enumerate(lines):
        d.text((960, 470 + i * 130), s, font=f(size), fill=col, stroke_width=8 if col == YEL else 0, stroke_fill=OUTL, anchor='mm')
    if sub: d.text((960, 940), sub, font=f(40), fill=(200, 205, 225), anchor='mm')
    if top: d.text((960, 200), top, font=f(46), fill=(140, 230, 205), anchor='mm')
    im.save(path)


def label(path, n, title):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(60, 60), (360, 60), (382, 100), (360, 140), (60, 140)], fill=MINT + (255,), outline=OUTL + (255,))
    d.text((210, 100), f'소울체인지 {n}화', font=f(46), fill=CREAM, stroke_width=4, stroke_fill=OUTL, anchor='mm')
    d.text((64, 170), title, font=f(44), fill=(255, 255, 255), stroke_width=5, stroke_fill=OUTL)
    d.text((W - 64, H - 60), '@twistbite_drama', font=f(34), fill=(220, 224, 240), anchor='rs')
    # 오른쪽 위 영혼 안내(처음 보는 사람용)
    x0, y0 = 1330, 60
    d.rounded_rectangle([x0, y0, W - 50, y0 + 150], radius=24, fill=(10, 14, 36, 200))
    for i, (col, txt_) in enumerate([((255, 110, 180), '아저씨 몸 = 여고생 지우 영혼'), ((90, 170, 255), '여고생 몸 = 50대 담임 영혼')]):
        cy = y0 + 45 + i * 60
        d.ellipse([x0 + 22, cy - 16, x0 + 54, cy + 16], fill=col + (255,), outline=(255, 255, 255, 255), width=3)
        d.text((x0 + 70, cy), txt_, font=f(34), fill=(255, 255, 255), anchor='lm')
    im.save(path)


def note_png(path, text):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    lines = text.split('\n'); tw = max(d.textlength(l, font=f(40)) for l in lines)
    d.rounded_rectangle([50, 760, 50 + tw + 60, 760 + 60 * len(lines) + 40], radius=22, fill=(255, 226, 90, 235), outline=OUTL + (255,), width=4)
    for i, l in enumerate(lines): d.text((80, 780 + i * 60), l, font=f(40), fill=OUTL)
    im.save(path)


def patch_png(path):
    im = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([272, 296, 660, 358], fill=(169, 190, 211, 255))
    d.text((282, 328), '2학년 3반 단톡   28', font=f(46), fill=(30, 30, 40), anchor='lm')
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
for n, p, a, v, b, title, sub, notes in EPS:
    card(B / f'ch{n}.png', [(f'{n}화', 140, YEL), (title, 80, CREAM)], sub or None)
    still(B / f'ch{n}.png', 1.6, B / f'seg_{n}a.mp4'); segs.append(B / f'seg_{n}a.mp4')
    label(B / f'lab{n}.png', n, title)
    g = -14.0 - lufs(p, a, b); d_ = b - a; hold = v - a
    ins = ['-i', p, '-i', B / f'lab{n}.png']; pre = '[0:v]'
    fc = ''
    if n in PATCH:
        patch_png(B / 'patch.png'); ins += ['-i', B / 'patch.png']; k_ = len(ins) // 2 - 1
        fc += f"[0:v][{k_}:v]overlay=0:0:enable='between(t,{PATCH[n][0]},{PATCH[n][1]})'[src];"; pre = '[src]'
    fc += (f"{pre}trim={v}:{b},setpts=PTS-STARTPTS,fps={FPS},tpad=start_duration={hold:.3f}:start_mode=clone,split[v1][v2];"
           f"[v1]scale={W}:-2,crop={W}:{H},gblur=sigma=40,eq=brightness=-0.18:saturation=0.8[bg];"
           f"[v2]scale=-2:{H}[fg];[bg][fg]overlay=(W-w)/2:0[c0];[c0][1:v]overlay=0:0[c1];")
    last = 'c1'
    for j, (ta, tb, txt_) in enumerate(notes):
        note_png(B / f'note{n}_{j}.png', txt_); ins += ['-i', B / f'note{n}_{j}.png']; k_ = len(ins) // 2 - 1
        fc += f"[{last}][{k_}:v]overlay=0:0:enable='between(t,{ta - a:.2f},{tb - a:.2f})'[n{j}];"; last = f'n{j}'
    fc += (f"[{last}]format=yuv420p,fade=t=in:d=0.25,fade=t=out:st={d_ - 0.25:.3f}:d=0.25[v];"
           f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,volume={g:.2f}dB,"
           f"alimiter=limit=0.89:level=false,afade=t=in:d=0.05,afade=t=out:st={d_ - 0.25:.3f}:d=0.25[a]")
    out = B / f'seg_{n}b.mp4'
    run(['ffmpeg', '-y', '-v', 'error', *ins, '-filter_complex', fc, '-map', '[v]', '-map', '[a]',
         '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-c:a', 'aac', '-b:a', '192k', '-r', FPS, '-t', f'{d_:.3f}', out])
    segs.append(out); print(n, round(a, 2), round(b, 2), f'{g:+.1f}dB')
card(B / 'close.png', [('7화는 쇼츠에서', 96, YEL), ('화요일 18시', 96, CREAM)], '구독하고 다음 이야기도 함께 봐요')
still(B / 'close.png', 4.0, B / 'seg_99_close.mp4'); segs.append(B / 'seg_99_close.mp4')
(B / 'list.txt').write_text(''.join(f"file '{s}'\n" for s in segs))
out = HERE / f'소울체인지_1-6화_몰아보기_{TAG}.mp4'
run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', B / 'list.txt', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19',
     '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out])
chap, t = [], 3.0
for n, p, a, v, b, title, sub, notes in EPS:
    chap.append(f'{int(t // 60)}:{int(t % 60):02d} {n}화 {title}'); t += 1.6 + (b - a)
(HERE / f'챕터_{TAG}.txt').write_text('0:00 시작\n' + '\n'.join(chap) + '\n', encoding='utf-8')
print('OK', out, round(dur(out), 1)); print('\n'.join(chap))
