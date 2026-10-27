#!/usr/bin/env python3
"""소울체인지 7화 「그 욕은 엄마 말이었다」 편집 v1 (6화 v5 방식, 크레딧 0).

기준: 대본_v4.md 3절 컷 표 + 5-2절, 6화 사장님 지적(상황 자막·해설 자막·입 맞춤·J컷·Jua에 없는 글자 금지·첫 장면 이름표 없음).
- 어머니 손 컷 K1·K2·K7·K10은 PC Dreamina(10/28~10/31)가 episodes/ep7/clips/K01.mp4·K02.mp4·K07.mp4·K10.mp4로 올림.
  → 파일이 있으면 그 파일, 없으면 임시 화면(상담실 흐림 + "K1 자리(어머니 손)"). 다시 돌리기만 하면 바꿔 끼워짐.
- 본편 ≤ 64.3초 + 고정 엔딩 5.7초(make_ending.py 7 금) ≤ 70.0초.
- 겉말 = 몸 목소리, 속마음 = 영혼 목소리 + aecho=0.85:0.6:45:0.12, 빙의 풀림 2단계 "헐.. 최 쌤 향수 냄새" = sc_student_body + 잔향 + 영혼 원 지지직(6화보다 세게).
- 욕은 녹음의 해당 구간을 잘라 내고 "삐", 자막의 ○는 ASS 그림(원)으로.
사용: python3 build_ep7_v1.py → ep7_v1.mp4, timeline_v1.json
"""
import json, math, pathlib, random, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from vo_prep import prep
import bgm

KIT = pathlib.Path('/home/user/youtube-ops/series/_soulchange_kit')
EP = HERE.parent
V = EP / '04_생성물' / 'voices'
C = EP / '04_생성물' / 'clips'
PC = KIT / 'episodes/ep7/clips'
E5 = EP.parent / 'soulchange-ep05' / '04_생성물' / 'clips'
V6 = EP.parent / 'soulchange-ep06' / '04_생성물' / 'voices'
BENCH = EP.parent / 'soulchange-ep06' / '05_편집' / 'build_v5' / 'K11_hood.mp4'   # 6화 K11(벤치 머리 윤곽 보정본)
B = HERE / 'build_v1'; B.mkdir(exist_ok=True)
VO = B / 'vo'
FONT = KIT / 'fonts/Jua-Regular.ttf'
FPS, W, H = 30, 1080, 1920
END_LEN = 5.7
MAIN_MAX = 70.0 - END_LEN
f = lambda s: ImageFont.truetype(str(FONT), s)


def run(cmd, **kw):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, **kw)
    if r.returncode: raise SystemExit(' '.join(map(str, cmd)) + '\n' + r.stderr[-2000:])
    return r


def dur_of(p):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)], capture_output=True, text=True).stdout)


# ---------- 1. 대사 (생성로그 ★) ----------
T, G = 1.05, 0.13
SPEC = {
    'E01': dict(f='E7-01_mother_soraya_raw.mp3', r=[(0, 5.40)], gap=0.30),
    'E02a': dict(f='E7-02_jiu_teacherbody_raw.mp3', r=[(0, 0.95)], tempo=1.10),                # "네, 네!"
    'E02b': dict(f='E7-02_jiu_teacherbody_raw.mp3', r=[(1.30, 4.75)], tempo=1.15, gap=0.18),   # "품격... 넘치죠, 그럼요!"
    'E03': dict(f='E7-03_mother_soraya_raw.mp3', r=[(0, 3.55)]),
    'E04': dict(f='E7-04_jiu_inner_student_raw.mp3', r=[(0.70, 2.55)]),                        # 앞 숨 빼고 "작년 담임? 우리 쌤?!"
    'E05': dict(f='E7-05_friend_pixie_raw.mp3', r=[(0.95, 3.20)]),                            # 앞 웃음 뺌
    'E06': dict(f='E7-06_teacher_studentbody_raw.mp3', r=[(0, 2.10)], gap=0.20),
    'E07': dict(f='E7-07_teacher_dm_teacher_raw.mp3', r=[(0, 3.35)]),
    'E08': dict(f='E7-08b_jiu_leak_student_raw.mp3', r=[(0, 2.30)], gap=0.18, tempo=1.10),     # ★b
    'E09c': dict(f='E7-09_jiu_teacherbody_raw.mp3', r=[(0, 1.08)], tempo=1.0),                 # 기침 한 번
    'E09': dict(f='E7-09_jiu_teacherbody_raw.mp3', r=[(3.02, 6.45)], tempo=1.20, gap=0.15),    # "향수가... 아주... 고급지시네요..."
    'E10a': dict(f='E7-10_mother_soraya_raw.mp3', r=[(0, 1.15)]),                              # "향수요?!"
    'E10b': dict(f='E7-10_mother_soraya_raw.mp3', r=[(1.62, 4.58)]),                           # "애 하나 때문에 집안이 곤란한데, 그 담임" (욕 4.56–5.18은 잘라 내고 삐)
    'E11': dict(f='E7-11_jiu_inner_student_raw.mp3', r=[(0, 4.00)], tempo=1.10, gap=0.20),
    'E12': dict(f='E7-12_mother_soraya_raw.mp3', r=[(0, 2.55)]),
    'E13': dict(f='E7-13_jiu_teacherbody_raw.mp3', r=[(0, 1.80)]),
    'HM': dict(f='E6-03_vp_arthur_raw.mp3', r=[(0, 1.00)], tempo=1.0),                         # 6화 교감 "흐흠..."
    'E14': dict(f='E7-14_teacher_dm_teacher_raw.mp3', r=[(0, 2.95)]),
    'E15': dict(f='E7-15_jiu_inner_student_raw.mp3', r=[(0, 2.00)]),
    'E16a': dict(f='E7-16b_jiu_teacherbody_raw.mp3', r=[(0, 0.98)], tempo=1.0),                # ★b "해야죠, 뭐."
    'E16b': dict(f='E7-16b_jiu_teacherbody_raw.mp3', r=[(0.98, 3.20)]),                        # "아이고, 허리야..."
    'E17': dict(f='E7-17_teacher_dm_teacher_raw.mp3', r=[(0, 2.40)]),
}
for s in SPEC.values():
    s.setdefault('tempo', T); s.setdefault('gap', G)
_hm = SPEC.pop('HM'); D = prep(SPEC, V, VO); D.update(prep({'HM': _hm}, V6, VO)); SPEC['HM'] = _hm
INNER = {'E04', 'E08', 'E11', 'E15'}

# ---------- 2. 컷 ----------
L, CUTS = {}, []
t = 0.0
def cut(cid, src, ss, se, pip, dur, zoom=(1.0, 0.5, 0.5), note='', fx=None, stretch=None, still=None, push=0.12, ph=None):
    global t
    CUTS.append(dict(id=cid, src=src, ss=ss, se=se, pip=pip, start=round(t, 3), dur=round(dur, 3), zoom=zoom, note=note, fx=fx, st=stretch,
                     still=still, push=push, ph=ph))
    t += dur
def at(lid, x):
    L[lid] = round(x, 3); return x + D[lid]
def hand(cid, fname, dur, label, note):
    """어머니 손 컷: PC 파일이 있으면 그것(5초까지 1.15배 이하로 늘리고 모자라면 마지막 프레임 유지), 없으면 임시 화면."""
    p = PC / fname
    if p.exists():
        avail = dur_of(p)
        stt = min(1.15, max(1.0, dur / avail))
        cut(cid, p, 0, None, 'pip', dur, stretch=stt, note=note + f' — {fname}')
    else:
        cut(cid, None, 0, None, 'pip', dur, fx='ph', ph=label, note=note + f' — 【임시 화면】 {fname} 오면 자동으로 바뀜')

# K0: 교감 메신저(코드) — 이름표 없음, 글자로 상황
c0 = t
cut('K0', None, 0, None, 'pip', 2.6, fx='msg', note='코드: 담임 폰 학교 메신저, 교감 말풍선 셋')
# K1 어머니 손(탁 + 가방 속 향수병) — "우리 아이는 아무 문제가 없어요. 순둥이, 타고난 품격이 있는 아이라구요!"
SOB = None
c0 = t; TAK = c0 + 0.05
e = at('E01', c0 + 0.20)
e = at('E02a', e + 0.10)                                     # "네, 네!"는 어머니 손 위로 먼저(J컷) — 담임 몸 얼굴로 넘어감
hand('K1', 'K01.mp4', e - 0.05 - c0, 'K1 자리 (어머니 손)\n손바닥 탁 + 가방 속 향수병', '어머니 손: 탁자 탁, 가방 입구 향수병')
# K3a: 담임 몸 굽신(K03 0–2.6, 웃으며 끄덕이며 말함)
c0 = t; e = at('E02b', c0 + 0.08)
cut('K3a', PC / 'K03.mp4', 0.1, None, 'pip', e + 0.08 - c0, note='담임 몸(지우 영혼) 굽신 웃음 — "품격... 넘치죠, 그럼요!"', stretch=min(1.15, max(1.0, (e + 0.08 - c0) / 2.5)))
# K2 어머니 손가락 콕 — "작년 담임이 한 정서학대, 잊으셨어요?"
c0 = t; e = at('E03', c0 + 0.10)
hand('K2', 'K02.mp4', e + 0.10 - c0, 'K2 자리 (어머니 손)\n검지로 콕, 탁자 톡톡', '어머니 손가락 콕')
# K3b: 웃음 빠지고 눈 커짐 → 탁자 밑 폰 두 엄지(K03 2.5–5.04) — 속마음 "작년 담임? 우리 쌤?!"
c0 = t; ZOOM_T = c0 + 0.05
e = at('E04', c0 + 0.15)
cut('K3b', PC / 'K03.mp4', 2.5, 5.04, 'pip', max(e + 0.40 - c0, 2.54), note='눈 커짐 → 탁자 밑 폰 두 엄지(입 다묾) — 속마음')
DM1 = (k3b_e := t) - 1.2
# K4 = H(지우 몸): 폰 두드림(0–2.5) → "쉿"(2.5~). 친구 화면 밖 → "쉿. 어른 일이다."
k4s = 1.1; c0 = t; TYPE4 = c0 + 0.2
e = at('E05', c0 + 0.30)
e = at('E06', max(e + 0.15, c0 + 2.55 * k4s))
cut('K4', C / 'K4.mp4', 0, None, 'pip_t', e + 0.20 - c0, stretch=k4s, note='지우 몸(담임 영혼) 폰 검지 타자 → "쉿"(아크, 역광)')
# K5: 6화 벤치(재사용, 머리 윤곽 보정본) — 담임 영혼 DM(보냄) "맞아, 나야. 노래 틀어 줬다 민원."
c0 = t; e = at('E07', c0 + 0.20); SEND5 = e + 0.05
cut('K5', BENCH, 1.0, None, 'pip_t', e + 0.30 - c0, note='6화 K11 재사용(벤치 먼 뒷모습) — 담임 DM')
# K6: 담임 몸(K06) 두 손으로 입 → "헐.. 최 쌤 향수 냄새"(빙의 풀림 2단계) → 주먹 기침 → 굳은 웃음 "향수가... 아주... 고급지시네요..."
k6s = 1.15; c0 = t
e = at('E08', c0 + 0.25); GLITCH = (L['E08'], L['E08'] + D['E08'])
e = at('E09c', max(e + 0.10, c0 + (2.75 - 0.6) * k6s))      # 주먹 기침(원본 2.75–3.25)
e = at('E09', max(e + 0.05, c0 + (3.5 - 0.6) * k6s))        # 말하는 입(원본 3.5~)
K6END = (dur_of(PC / 'K06.mp4') - 0.6) * k6s - 0.04             # 원본 끝에서 멈추지 않게: 남은 말꼬리는 어머니 손 위로(L컷)
cut('K6', PC / 'K06.mp4', 0.6, None, 'pip', min(e + 0.20 - c0, K6END), stretch=k6s, note='담임 몸: 손으로 입 → 기침 → 굳은 웃음으로 말함(카메라 정면 응시는 원본 약점)')
# K7 어머니 손(가방 끈 비틀기 → 툭) — "향수요?!" → "애 하나 때문에 집안이 곤란한데, 그 담임 (삐)!"
c0 = t
e = at('E10a', max(c0, L['E09'] + D['E09']) + 0.40)         # 말꼬리가 어머니 손 위로 넘어온 뒤 정적 0.4초
e = at('E10b', e + 0.15); BEEP = e - 0.02; THUD7 = BEEP + 0.55
hand('K7', 'K07.mp4', BEEP + 0.85 - c0, 'K7 자리 (어머니 손)\n가방 끈 비틀기, 탁자에 툭', '어머니 손: 가방 끈 꽉 → 툭')
# K8: 코드 — 담임 폰의 6화 쪽지 사진, 욕 줄에 빨간 동그라미, 둘째 줄 밑줄 — 속마음 "같은 욕. 걔가 싫었던 건, 엄마였어."
c0 = t; e = at('E11', c0 + 0.30)
cut('K8', None, 0, None, 'pip', e + 0.35 - c0, fx='note', note='코드: 6화 쪽지 사진 확대 → 욕 줄 빨간 동그라미 → "냄새 싫어" 밑줄')
# K10 어머니 손(가방 낚아채고 일어남) — "애는 엄마가 제일 잘 알아요!" → 의자 끽 → 문 쾅 → 화면 밖 "살... 살펴 가세요..."
c0 = t; e = at('E12', c0 + 0.15); CHAIR = e + 0.10; DOOR = e + 0.55
e = at('E13', DOOR + 0.30)
hand('K10', 'K10.mp4', e + 0.15 - c0, 'K10 자리 (어머니 손)\n가방 낚아채고 일어남', '어머니 손: 가방 낚아채고 일어남, 코트 자락')
# R2: 그 시각 교무실, 5화 교감(입 다문 굳은 얼굴 → 정지+다가감) "흐흠..." — 문 쾅 잔향을 먼저 깔고(J컷)
c0 = t; e = at('HM', c0 + 0.35)
cut('R2', E5 / 'A5a_K12a_교감끝훅.mp4', 2.45, 3.15, 'pip', e + 0.30 - c0, stretch=None, note='5화 교감(입 다묾) — "흐흠..." (6화 E6-03 앞부분)')
# K11: 코드 — 지우 몸(담임 영혼) 폰에서 보내는 DM "신고는 담임이 해. 지금 담임은 너."
c0 = t; e = at('E14', c0 + 0.45)
BUB11 = [L['E14'], L['E14'] + 1.30 / 1.05]
cut('K11', None, 0, None, 'pip_t', e + 0.35 - c0, fx='dm11', note='코드: 지우 폰(지금은 쌤)에서 담임 폰으로 DM 두 개')
# K12 = H: 폰 꼭 쥐고 빈 의자(0–2) → 벌떡(2.5–3) → 허리 짚고 찡그림(3.5~). 속마음 → "해야죠, 뭐." → "아이고, 허리야..."
k12s = 1.15; c0 = t
e = at('E15', c0 + 0.20)
e = at('E16a', max(e + 0.15, c0 + 2.35 * k12s))            # 일어나기 시작할 때
CRACK = c0 + 3.30 * k12s
e = at('E16b', max(e + 0.10, c0 + 3.55 * k12s))            # 허리 짚고 입 벌림
cut('K12', C / 'K12.mp4', 0, None, 'pip', e + 0.10 - c0, stretch=k12s, note='담임 몸: 폰 꼭 쥐고 빈 의자 → 벌떡 → 허리')
# K13: 코드 — 담임 몸 폰에 온 DM "허리 조심해라. 내 몸이다." (보낸 담임 영혼 목소리)
c0 = t; e = at('E17', c0 + 0.35); DING = e + 0.10
cut('K13', None, 0, None, 'pip', e + 0.45 - c0, fx='dm13', note='코드: 담임 폰(지금은 지우)에 온 DM')
MAIN = round(t, 3); TOT = round(MAIN + END_LEN, 3)
print('본편', MAIN, '합계', TOT)
for c in CUTS:
    if c['src'] is None: c['stretch'] = 1.0; c['se'] = c['ss']; print(f"  {c['id']:5s} {c['start']:6.2f} +{c['dur']:.2f}  {c['fx']}"); continue
    if c['st']: c['stretch'] = c['st']; c['se'] = round(c['ss'] + c['dur'] / c['st'], 3)
    else:
        if c['se'] is None: c['se'] = round(c['ss'] + c['dur'], 3)
        c['stretch'] = round(min(1.15, c['dur'] / (c['se'] - c['ss'])), 3)
    print(f"  {c['id']:5s} {c['start']:6.2f} +{c['dur']:.2f}  src {c['ss']}-{c['se']} x{c['stretch']}")
    assert c['stretch'] <= 1.151, c
assert MAIN <= MAIN_MAX + 1e-6, f'본편 {MAIN} > {MAIN_MAX}'


# ---------- 3. 영상 조각 ----------
def grab(src, tsec):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{tsec}', '-i', str(src), '-frames:v', '1', '-vf', 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    return Image.frombytes('RGB', (W, H), raw[:W * H * 3])


def push_frames(img, n, z1=0.06):
    out = []
    for i in range(n):
        z = 1.0 + z1 * i / max(1, n - 1); w, h = W / z, H / z
        out.append(np.asarray(img.transform((W, H), Image.EXTENT, ((W - w) / 2, (H - h) / 2, (W + w) / 2, (H - h) / 2 + h), Image.BICUBIC), np.uint8))
    return out


def ph_frames(n, label):
    """임시 화면: 상담실(K03 첫 프레임) 흐림 + 어두운 띠 + 자리 이름."""
    bg = grab(PC / 'K03.mp4', 0.2).filter(ImageFilter.GaussianBlur(22))
    bg = Image.fromarray((np.asarray(bg, float) * 0.6).astype(np.uint8)); d = ImageDraw.Draw(bg)
    d.rounded_rectangle([90, 640, 990, 1060], 40, fill=(20, 20, 26))
    d.rounded_rectangle([90, 640, 990, 1060], 40, outline=(255, 200, 80), width=6)
    d.text((540, 700), '임시 화면', font=f(46), fill=(255, 200, 80), anchor='mm')
    for i, ln in enumerate(label.split('\n')):
        d.text((540, 800 + i * 90), ln, font=f(64 if i == 0 else 52), fill=(255, 255, 255), anchor='mm')
    return push_frames(bg, n, 0.03)


def phone(img_bg, header, bubbles, tt, side='R', col=(255, 140, 190), y_top=380, ph_=1200, rise=1.0, hint=''):
    """폰 화면 하나 그리기. bubbles = [(나타나는 시각, 글)]; side R = 보낸 쪽(오른쪽), L = 받은 쪽(왼쪽)."""
    im = img_bg.copy(); d = ImageDraw.Draw(im)
    pw = 700; x0 = (W - pw) // 2; y0 = y_top + int((1 - rise) * 1400)
    d.rounded_rectangle([x0, y0, x0 + pw, y0 + ph_], 70, fill=(22, 22, 26))
    sx0, sy0, sx1, sy1 = x0 + 22, y0 + 22, x0 + pw - 22, y0 + ph_ - 22
    d.rounded_rectangle([sx0, sy0, sx1, sy1], 52, fill=(236, 238, 244))
    d.rectangle([sx0, sy0 + 40, sx1, sy0 + 150], fill=(222, 225, 234))
    d.text((sx0 + 34, sy0 + 95), header, font=f(42), fill=(30, 30, 30), anchor='lm')
    y = sy0 + 210
    for k, (ta, txt) in enumerate(bubbles):
        if tt < ta: continue
        sc = min(1.0, 0.6 + (tt - ta) / 0.12 * 0.4); fs = int(48 * sc)
        lines = txt.split('\n'); lh = int(62 * sc)
        tw = max(d.textlength(l, font=f(fs)) for l in lines); bh = lh * len(lines) + 36
        if side == 'R':
            d.rounded_rectangle([sx1 - 30 - tw - 44, y, sx1 - 30, y + bh], 30, fill=col)
            for i, l in enumerate(lines): d.text((sx1 - 30 - 22, y + 18 + i * lh), l, font=f(fs), fill=(255, 255, 255), anchor='ra')
        else:
            d.rounded_rectangle([sx0 + 30, y, sx0 + 30 + tw + 44, y + bh], 30, fill=col)
            for i, l in enumerate(lines): d.text((sx0 + 52, y + 18 + i * lh), l, font=f(fs), fill=(30, 30, 30), anchor='la')
        y += bh + 24
    d.rounded_rectangle([sx0 + 24, sy1 - 120, sx1 - 24, sy1 - 40], 40, fill=(255, 255, 255))
    d.text((sx0 + 60, sy1 - 80), hint, font=f(38), fill=(170, 170, 180), anchor='lm')
    return im


def write_frames(fr, out):
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p', str(out)], input=np.stack(fr).tobytes(), check=True)


def dim_blur(img, s=14, k=0.55):
    return Image.fromarray((np.asarray(img.filter(ImageFilter.GaussianBlur(s)), float) * k).astype(np.uint8))


def note_photo():
    """6화 쪽지(수첩 종이) 사진 — 원은 직접 그림."""
    rnd = np.random.default_rng(6); pw, ph = 860, 1080
    base = np.full((ph, pw, 3), (238, 236, 228), float) + rnd.normal(0, 3.0, (ph, pw, 1))
    paper = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(paper)
    for y in range(150, ph - 40, 72): d.line([(30, y), (pw - 30, y)], fill=(165, 188, 222), width=2)
    pen = (48, 50, 66); x = 90; y0 = 250
    for p_ in ['최', '○', '○', ' 티', '○', '년']:
        if p_ == '○':
            r_ = 40; cy = y0 + 62; d.ellipse([x + 4, cy - r_, x + 4 + 2 * r_, cy + r_], outline=pen, width=6); x += 2 * r_ + 14
        else:
            d.text((x, y0), p_, font=f(112), fill=pen); x += d.textlength(p_, font=f(112))
    d.text((90, 470), '냄새 싫어.', font=f(100), fill=pen); d.text((90, 620), '없어져.', font=f(100), fill=pen)
    mask = Image.new('L', (pw, ph), 255); md = ImageDraw.Draw(mask)
    for xx in range(40, pw - 20, 52): md.ellipse([xx, 22, xx + 22, 44], fill=0)
    md.rectangle([0, 0, pw, 16], fill=0)
    paper = paper.convert('RGBA'); paper.putalpha(mask)
    return paper


def k8_frames(n, start):
    bg = dim_blur(grab(PC / 'K06.mp4', 4.9))
    paper = note_photo().resize((560, 703), Image.LANCZOS)
    fr = []
    for i in range(n):
        lt = i / FPS
        im = bg.copy(); d = ImageDraw.Draw(im)
        x0, y0 = 170, 300
        d.rounded_rectangle([x0, y0, x0 + 740, y0 + 1000], 70, fill=(22, 22, 26))
        d.rounded_rectangle([x0 + 22, y0 + 22, x0 + 718, y0 + 978], 52, fill=(18, 18, 20))
        z = 1.0 + 0.35 * min(1, lt / 0.6)                     # 사진 확대
        pz = paper.resize((int(560 * z), int(703 * z)), Image.LANCZOS)
        cx, cy = x0 + 370, y0 + 470
        box = Image.new('RGBA', (696, 956), (18, 18, 20, 255)); box.paste(pz, (348 - pz.width // 2 + int(60 * (z - 1)), 478 - pz.height // 2 + int(120 * (z - 1))), pz)
        im.paste(box.convert('RGB'), (x0 + 22, y0 + 22))
        d = ImageDraw.Draw(im)
        sx = (x0 + 22 + 348 - pz.width // 2 + int(60 * (z - 1))); sy = (y0 + 22 + 478 - pz.height // 2 + int(120 * (z - 1)))
        s_ = pz.width / 860
        if lt > 0.8:   # 욕 줄 빨간 동그라미(그려지듯)
            k = min(1, (lt - 0.8) / 0.5)
            bb = [sx + 60 * s_, sy + 220 * s_, sx + 820 * s_, sy + 400 * s_]
            d.arc(bb, -200, -200 + 360 * k, fill=(230, 40, 40), width=9)
        if lt > 1.6:   # "냄새 싫어" 밑줄
            k = min(1, (lt - 1.6) / 0.35)
            yy = sy + 590 * s_; d.line([(sx + 85 * s_, yy), (sx + (85 + 470 * k) * s_, yy)], fill=(230, 40, 40), width=9)
        fr.append(np.asarray(im, np.uint8))
    return fr


seg_list = []
for c in CUTS:
    out = B / f"seg_{c['id']}.mp4"; nfr = round(c['dur'] * FPS)
    if c['fx'] == 'ph':
        write_frames(ph_frames(nfr, c['ph']), out); seg_list.append(out); continue
    if c['fx'] == 'msg':
        bg = dim_blur(grab(PC / 'K03.mp4', 0.2))
        bubs = [(0.15, '[교감] 김 선생,\n오늘 그 어머님 상담.'), (0.75, '무조건 웃으면서.\n조용히^^'), (1.35, '(이사장님 귀에 들어가면\n곤란합니다)')]
        write_frames([np.asarray(phone(bg, '<  학교 메신저 (교감)', bubs, i / FPS, side='L', col=(255, 255, 255), rise=1.0), np.uint8) for i in range(nfr)], out)
        seg_list.append(out); continue
    if c['fx'] == 'note':
        write_frames(k8_frames(nfr, c['start']), out); seg_list.append(out); continue
    if c['fx'] == 'dm11':
        bg = dim_blur(grab(C / 'K4.mp4', 4.9))
        bubs = [(BUB11[0] - c['start'], '신고는 담임이 해.'), (BUB11[1] - c['start'], '지금 담임은 너.')]
        fr = [np.asarray(phone(bg, '<  김 선생 폰 (지금은 지우)', bubs, i / FPS, side='R', col=(80, 150, 230), rise=min(1, i / FPS / 0.35),
                               hint='입력 중...' if i / FPS < bubs[-1][0] else '메시지 입력'), np.uint8) for i in range(nfr)]
        write_frames(fr, out); seg_list.append(out); continue
    if c['fx'] == 'dm13':
        bg = dim_blur(grab(C / 'K12.mp4', 4.9))
        bubs = [(L['E17'] - c['start'], '...허리 조심해라.\n내 몸이다.')]
        fr = [np.asarray(phone(bg, '<  지우 폰 (지금은 쌤)', bubs, i / FPS, side='L', col=(200, 225, 255), rise=min(1, i / FPS / 0.3), hint='메시지 입력'), np.uint8)
              for i in range(nfr)]
        write_frames(fr, out); seg_list.append(out); continue
    z, ax, ay = c['zoom']; used = c['se'] - c['ss']
    vf = (f"[0:v]trim=start={c['ss']}:duration={used:.3f},setpts=(PTS-STARTPTS)*{c['stretch']},fps={FPS},"
          f"scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,")
    if z != 1.0:
        sw, sh = int(round(1080 * z / 2) * 2), int(round(1920 * z / 2) * 2)
        vf += f"scale={sw}:{sh}:flags=lanczos,crop=1080:1920:{int((sw - 1080) * ax)}:{int((sh - 1920) * ay)},"
    if c['id'] == 'K3b':   # "띠용" 짧은 줌(코드)
        _t0 = ZOOM_T - c['start']
        vf += f"zoompan=z='if(lt(on,{int(_t0 * FPS)}),1,if(lt(on,{int(_t0 * FPS) + 5}),1+0.12*(on-{int(_t0 * FPS)})/5,1.12))':x='iw/2-(iw/zoom/2)':y='ih*0.35-(ih/zoom*0.35)':d=1:s=1080x1920:fps={FPS},"
    vf += "setsar=1,format=yuv420p,tpad=stop_mode=clone:stop_duration=2.0[v]"
    run(['ffmpeg', '-y', '-loglevel', 'error', '-i', c['src'], '-filter_complex', vf, '-map', '[v]',
         '-frames:v', nfr, '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', out])
    seg_list.append(out)
(B / 'list.txt').write_text(''.join(f"file '{p}'\n" for p in seg_list))
run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', B / 'list.txt', '-c', 'copy', B / 'joined.mp4'])

# 영혼 원 지지직(빙의 풀림 2단계 — 6화보다 세게)
pip = Image.open(KIT / 'pip.png').convert('RGBA').resize((300, 300), Image.LANCZOS)
GDIR = B / 'glitch'; GDIR.mkdir(exist_ok=True)
for p_ in GDIR.glob('*.png'): p_.unlink()
gn = round((GLITCH[1] - GLITCH[0]) * FPS)
for i in range(gn):
    rnd = random.Random(i * 7 + 3); a = np.asarray(pip).copy()
    for _ in range(8):
        y0 = rnd.randint(0, 280); hgt = rnd.randint(6, 30); dx = rnd.randint(-36, 36)
        a[y0:y0 + hgt] = np.roll(a[y0:y0 + hgt], dx, axis=1)
    a[..., 0] = np.roll(a[..., 0], 7, axis=1); a[..., 2] = np.roll(a[..., 2], -7, axis=1)
    a[::3, :, :3] = (a[::3, :, :3] * 0.5).astype(np.uint8)
    rgb = a[..., :3].astype(float); g_ = rgb.mean(axis=2, keepdims=True)
    a[..., :3] = (rgb * 0.45 + g_ * 0.55).astype(np.uint8)
    Image.fromarray(a).save(GDIR / f'g_{i:02d}.png')

# ---------- 4. 소리 ----------
HALL = 'aecho=0.85:0.6:45:0.12'
GAIN = {'E04': 1.0, 'E11': 1.0, 'E15': 1.0}
ins, fc, mixl = [], [], []
for i, (lid, st) in enumerate(sorted(L.items(), key=lambda kv: kv[1])):
    ins += ['-i', VO / f'{lid}.wav']
    ch = f"[{i}:a]aresample=48000,aformat=channel_layouts=mono"
    if lid in INNER: ch += f",{HALL}"
    ch += ",acompressor=threshold=-20dB:ratio=3:attack=5:release=120"
    if lid in GAIN: ch += f",volume={GAIN[lid]}dB"
    ch += f",aformat=channel_layouts=stereo,adelay={int(st * 1000)}:all=1[v{i}]"
    fc.append(ch); mixl.append(f'[v{i}]')

def sfx(lbl, expr, d, at_, vol=1.0):
    fc.append(f"aevalsrc='{expr}':d={d}:s=48000,volume={vol},aformat=channel_layouts=stereo,adelay={int(at_ * 1000)}:all=1[{lbl}]")
    mixl.append(f'[{lbl}]')
def noise(lbl, d, at_, filt, vol):
    fc.append(f"anoisesrc=d={d}:c=pink:a=0.5:r=48000,{filt},volume={vol},aformat=channel_layouts=stereo,adelay={int(at_ * 1000)}:all=1[{lbl}]")
    mixl.append(f'[{lbl}]')
k = {c['id']: c for c in CUTS}
DINGX = '0.16*sin(2*PI*1320*t)*lt(t,0.08)+0.16*sin(2*PI*1760*t)*gt(t,0.12)*lt(t,0.24)'
TAKX = '0.6*sin(2*PI*(200-90*t)*t)*exp(-40*t)+0.2*sin(2*PI*900*t)*exp(-70*t)'
DOORX = '0.6*sin(2*PI*(120-60*t)*t)*exp(-22*t)+0.2*sin(2*PI*520*t)*exp(-50*t)'
DUNGX = '0.35*sin(2*PI*(58+8*t)*t)*exp(-1.6*t)'
SEND = '0.18*sin(2*PI*(700+1600*t)*t)*exp(-12*t)'
BOING = '0.20*sin(2*PI*(300+500*t)*t)*exp(-6*t)'
for j, ta in enumerate([0.15, 0.75, 1.35]): sfx(f'm{j}', DINGX, 0.3, k['K0']['start'] + ta, 0.45)
sfx('tak', TAKX, 0.3, TAK, 0.8)
for j in range(2): sfx(f'tt{j}', '0.4*sin(2*PI*1100*t)*exp(-90*t)', 0.08, k['K2']['start'] + 1.2 + 0.25 * j, 0.5)   # 손톱 톡톡
sfx('boing', BOING, 0.4, ZOOM_T, 0.45)
for j in range(8): noise(f'th{j}', 0.04, ZOOM_T + 0.9 + 0.12 * j, 'bandpass=f=2500:w=1500', 0.08)        # 엄지 다다닥
for j in range(4): noise(f'eg{j}', 0.05, TYPE4 + 0.55 * j, 'bandpass=f=2000:w=1200', 0.10)              # 독수리 톡…톡…
sfx('send5', SEND, 0.35, SEND5, 0.5)
fc.append(f"anoisesrc=d=0.6:c=white:a=0.5:r=48000,highpass=f=1800,volume='0.13*lt(mod(t,0.04),0.02)*(0.6+0.4*sin(2*PI*57*t))':eval=frame,"
          f"afade=t=out:st=0.45:d=0.15,aformat=channel_layouts=stereo,adelay={int(GLITCH[0] * 1000)}:all=1[zap]"); mixl.append('[zap]')   # 지지직(6화보다 길고 셈)
sfx('beep', '0.25*sin(2*PI*1000*t)', 0.55, BEEP, 1.0)
sfx('thud7', TAKX, 0.3, THUD7, 0.8)
noise('sw1', 0.25, k['K8']['start'] + 0.8, 'highpass=f=2500,afade=t=in:d=0.05,afade=t=out:st=0.1:d=0.15', 0.08)
noise('sw2', 0.25, k['K8']['start'] + 1.6, 'highpass=f=2500,afade=t=in:d=0.05,afade=t=out:st=0.1:d=0.15', 0.08)
fc.append(f"anoisesrc=d=0.45:c=brown:a=0.6:r=48000,bandpass=f=700:w=500,volume='0.45*(0.6+0.4*sin(2*PI*28*t))':eval=frame,afade=t=in:d=0.05,afade=t=out:st=0.25:d=0.2,"
          f"aformat=channel_layouts=stereo,adelay={int(CHAIR * 1000)}:all=1[chair]"); mixl.append('[chair]')
sfx('door', DOORX, 0.5, DOOR, 0.9)
fc.append(f"aevalsrc='{DOORX}':d=0.5:s=48000,volume=0.35,aecho=0.8:0.7:120:0.4,lowpass=f=900,aformat=channel_layouts=stereo,adelay={int((k['R2']['start'] + 0.05) * 1000)}:all=1[door2]"); mixl.append('[door2]')
sfx('dung', DUNGX, 1.2, k['K11']['start'] + 0.2, 0.45)
for j, b_ in enumerate(BUB11): sfx(f'send11{j}', SEND, 0.35, b_, 0.5)
sfx('crack', '0.5*sin(2*PI*180*t)*exp(-60*t)*lt(mod(t,0.07),0.03)', 0.25, CRACK, 0.7)
sfx('ding', DINGX, 0.3, DING, 0.5)

def amb(lbl, a, b, lo, hi, vol):
    a0 = max(0, a - 0.3)
    fc.append(f"anoisesrc=d={b - a0:.2f}:c=pink:a=0.5:r=48000,bandpass=f={(lo + hi) // 2}:w={hi - lo},volume={vol},"
              f"afade=t=in:d=0.3,afade=t=out:st={b - a0 - 0.3:.2f}:d=0.3,aformat=channel_layouts=stereo,adelay={int(a0 * 1000)}:all=1[{lbl}]")
    mixl.append(f'[{lbl}]')
for c in CUTS:
    a, b = c['start'], c['start'] + c['dur']
    if c['id'] in ('K4',): amb(f"am_{c['id']}", a, b, 500, 2500, 0.022)
    elif c['id'] in ('K5',): amb(f"am_{c['id']}", a, b, 200, 800, 0.012)
    elif c['id'] in ('R2',): amb(f"am_{c['id']}", a, b, 300, 2800, 0.018)
    else: amb(f"am_{c['id']}", a, b, 250, 1200, 0.008)     # 상담실: 조용한 방
fc.append(f"anoisesrc=d={MAIN}:c=brown:a=0.5:r=48000,lowpass=f=350,volume=0.0105,afade=t=in:d=0.5,afade=t=out:st={MAIN - 0.4}:d=0.4,aformat=channel_layouts=stereo[room]"); mixl.append('[room]')
# 배경음: 상담 압박(똑딱) → "띠용"에서 뚝 → 교실(가벼운 펄스) → 벤치(단조) → 향수 장면(떨림) → "향수요?!" 직전 뚝 → 쪽지(단조) → 신고·결심(단조) → "해야죠, 뭐."에서 뚝
BGM_SECT = [('tense', k['K1']['start'], ZOOM_T),
            ('class', k['K4']['start'], k['K5']['start']),
            ('sad', k['K5']['start'], k['K6']['start']),
            ('tense2', k['K6']['start'], L['E09'] + D['E09'] + 0.05),
            ('sad', k['K8']['start'], k['K10']['start']),
            ('sad', k['K11']['start'], L['E16a'])]
BGM_I = bgm.make(BGM_SECT, [(VO / f'{lid}.wav', st) for lid, st in L.items()], MAIN, B / 'bgm.wav', target_lufs=-28.0, duck_db=-15.0)
ins += ['-i', B / 'bgm.wav']; mixl.append(f'[{len(ins) // 2 - 1}:a]')
fc.append(''.join(mixl) + f"amix=inputs={len(mixl)}:normalize=0,apad=whole_dur={MAIN},atrim=0:{MAIN}[aout]")
run(['ffmpeg', '-y', '-loglevel', 'error', *ins, '-filter_complex', ';'.join(fc), '-map', '[aout]', '-ar', '48000', B / 'mix_raw.wav'])

def meas(p):
    m = subprocess.run(['ffmpeg', '-i', str(p), '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', m)[-1]), float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', m)[-1])
I0, _ = meas(B / 'mix_raw.wav')
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', B / 'mix_raw.wav', '-af', f'volume={-14.0 - I0:.2f}dB,alimiter=limit=0.58:level=false:attack=2:release=60', '-ar', '48000', B / 'mix_main.wav'])
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', B / 'ending_ep7.mp4', '-vn', '-ar', '48000', '-ac', '2', B / 'ending.wav'])
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', B / 'mix_main.wav', '-i', B / 'ending.wav', '-filter_complex', '[0:a][1:a]concat=n=2:v=0:a=1[a]', '-map', '[a]', '-ar', '48000', B / 'mix_full_raw.wav'])
I1, _ = meas(B / 'mix_full_raw.wav')
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', B / 'mix_full_raw.wav', '-af', f'volume={-14.0 - I1:.2f}dB,alimiter=limit=0.58:level=false:attack=2:release=60', '-ar', '48000', B / 'mix.wav'])
I2, TP2 = meas(B / 'mix.wav'); print('loudness', I2, 'TP', TP2, 'bgm', BGM_I)

# ---------- 5. 자막 (Jua에 없는 … ○ • — 안 씀: 줄임표는 마침표 셋, ○는 ASS 그림) ----------
def ts(x):
    h_, m_ = int(x // 3600), int(x % 3600 // 60); s_ = x % 60
    return f"{h_}:{m_:02d}:{s_:05.2f}"
PINK, SKY = 'J', 'T'
TAGSTYLE = {('J', False): 'TagJ', ('T', False): 'TagT', ('', False): 'TagW', ('J', True): 'TagJi', ('T', True): 'TagTi'}
CIRC = r'{\p1}m 0 22 b 0 10 10 0 22 0 b 34 0 44 10 44 22 b 44 34 34 44 22 44 b 10 44 0 34 0 22 m 6 22 b 6 31 13 38 22 38 b 31 38 38 31 38 22 b 38 13 31 6 22 6 b 13 6 6 13 6 22{\p0}'
EV, PEND, SUBS = [], [], []
def ev(a, b, style, text, layer=1):
    EV.append(f"Dialogue: {layer},{ts(a)},{ts(b)},{style},,0,0,0,,{text}")
def say(lid, text, tag, col='', style='Dlg', hold=0.15, end=None, start=None):
    a = start if start is not None else L[lid]; b = end if end else L[lid] + D[lid] + hold
    PEND.append(dict(a=a, b=b, text=text, tag=tag, col=col, style=style, grp=lid))
def emit(x):
    fad = r'\fad(60,100)'
    if x['grp'] == 'E08':   # 빙의 풀림: 분홍 상자 번쩍(설명 글자 없음)
        fad = r'\3a&H00&\3c&HB45FFF&\t(0,70,\3c&H000000&)\t(70,140,\3c&HB45FFF&)\t(140,210,\3c&H000000&)\t(210,280,\3c&HB45FFF&)\t(280,400,\3c&H000000&)\t(400,480,\3c&HB45FFF&)\t(480,600,\3c&H000000&)'
    ev(x['a'], x['b'], x['style'] + 'B', r'{\an2\pos(540,1330)' + fad + '}' + x['text'], 2)
    ty = 1181 if r'\N' in x['text'] else 1243
    ev(x['a'], x['b'], TAGSTYLE[(x['col'], x['style'] == 'Mono')], rf"{{\an2\pos(540,{ty})\fad(60,100)}}{x['tag']}", 3)
def narr(a, b, text, x=40, y=430):
    ev(a, b, 'Narr', rf'{{\an7\pos({x},{y})\frz5\fad(120,150)}}{text}', 8)
def scene(a, b, text):
    ev(a, b, 'Scene', r'{\an7\pos(40,240)}' + text, 6)

ev(0.0, k['K1']['start'] + k['K1']['dur'], 'Label', r'{\an7\pos(40,140)}담임과 학생, 몸이 바뀌었다', 6)
scene(0.0, k['K0']['dur'], '교감이 담임 몸의 지우에게 보낸 메시지')
# 첫 화면 띠(대본 K0: 0–0.5초) — 소울체인지 7화 / 빨간 띠 / 노란 큰 글씨
ev(0.0, 0.62, 'Label', r'{\an5\pos(540,640)\bord0\shad0\1c&H000000&\1a&H28&\p1\fad(0,120)}m 0 0 l 1080 0 1080 420 0 420{\p0}', 9)
ev(0.0, 0.62, 'Label', r'{\an5\pos(540,500)\fs50\bord0\fad(0,120)}소울체인지 7화', 10)
ev(0.0, 0.62, 'Label', r'{\an5\pos(540,610)\fs62\1c&HFFFFFF&\3c&H2020D0&\4c&H2020D0&\bord12\fad(0,120)}그 학생 어머니가 왔다', 10)
ev(0.0, 0.62, 'Emph', r'{\an5\pos(540,750)\fs96\bord6\3c&H000000&\fad(0,120)}그 욕, 어디서 배웠을까', 10)
narr(1.6, k['K0']['dur'] + 0.4, r'(교장 되기 전에\N조용히만...)', 250, 1195)
scene(k['K1']['start'], k['K1']['start'] + 3.0, '상담실 · 텀블러 사건 그 학생의 어머니')
say('E01', r'우리 아이는 아무 문제가 없어요.\N순둥이, 타고난 품격이 있는 아이라구요!', '그 학생 어머니')
say('E02a', '네, 네!', '지우 영혼', PINK, hold=0.05)
say('E02b', '품격... 넘치죠, 그럼요!', '지우 영혼', PINK)
narr(L['E02b'] + 0.4, k['K3a']['start'] + k['K3a']['dur'], r'(일단 무조건 굽신)', 40, 430)
say('E03', r'작년 담임이 한 정서학대,\N잊으셨어요?', '그 학생 어머니')
say('E04', '...작년 담임? 우리 쌤?!', '(속마음) 지우 영혼', PINK, 'Mono')
ev(DM1, k['K3b']['start'] + k['K3b']['dur'], 'DMp', r'{\an6\pos(1000,860)\fad(80,120)}쌤!!! 작년 담임 = 쌤??', 4)
ev(DM1, k['K3b']['start'] + k['K3b']['dur'], 'TagJ', r'{\an3\pos(1000,770)\fad(80,120)}지우가 담임에게 · DM', 5)
scene(k['K4']['start'], k['K4']['start'] + 2.0, '같은 시각 · 교실 · 지우 몸에 담임 영혼')
say('E05', '지우야, 독수리 타법 뭐야?', '반 친구')
say('E06', '...쉿. 어른 일이다.', '담임 영혼', SKY)
say('E07', r'맞아, 나야.\N노래 틀어 줬다 민원.', '담임 영혼 · DM', SKY)
narr(L['E07'] + 0.6, k['K5']['start'] + k['K5']['dur'], r'(작년, 저 아이에게\N노래를 틀어 줬다가...)', 40, 700)
say('E08', '헐.. 최 쌤 향수 냄새', '지우 영혼', PINK, hold=0.2)
say('E09c', '크흠!', '지우 영혼', PINK, hold=0.05)
say('E09', r'향수가... 아주...\N고급지시네요...', '지우 영혼', PINK)
narr(L['E09'] + 0.3, k['K6']['start'] + k['K6']['dur'], r'(수습 실패)', 640, 430)
say('E10a', '향수요?!', '그 학생 어머니', hold=0.1)
say('E10b', r'애 하나 때문에 집안이 곤란한데,\N그 담임 티' + CIRC + '년!', '그 학생 어머니', end=BEEP + 0.7)
say('E11', r'...같은 욕.\N걔가 싫었던 건, 엄마였어.', '(속마음) 지우 영혼', PINK, 'Mono')
scene(k['K8']['start'], k['K8']['start'] + k['K8']['dur'], '6화의 쪽지 · 같은 욕')
say('E12', '애는 엄마가 제일 잘 알아요!', '그 학생 어머니')
say('E13', '살... 살... 살펴 가세요...', '지우 영혼', PINK)
scene(k['R2']['start'], k['R2']['start'] + k['R2']['dur'], '그 시각 · 교무실')
say('HM', '흐흠...', '교감', hold=0.2)
narr(L['HM'] + 0.2, k['R2']['start'] + k['R2']['dur'], r'(조용히 끝났다고\N믿는 중)', 40, 430)
scene(k['K11']['start'], k['K11']['start'] + k['K11']['dur'], '진짜 담임(지우 몸)이 보낸 DM')
say('E14', r'신고는 담임이 해.\N지금 담임은 너.', '담임 영혼 · DM', SKY)
say('E15', '...엄마를, 제가요?', '(속마음) 지우 영혼', PINK, 'Mono')
say('E16a', '...해야죠, 뭐.', '지우 영혼', PINK, hold=0.05)
say('E16b', '아이고, 허리야...', '지우 영혼', PINK)
narr(L['E16b'] + 0.1, k['K12']['start'] + k['K12']['dur'], r'(몸은 50대)', 600, 430)
say('E17', r'...허리 조심해라.\N내 몸이다.', '담임 영혼 · DM', SKY, end=MAIN - 0.05)
PEND.sort(key=lambda x: x['a'])
for i, x in enumerate(PEND):
    nxt = next((y for y in PEND[i + 1:] if y['grp'] != x['grp']), None)
    if nxt and x['b'] > nxt['a'] - 0.03: x['b'] = nxt['a'] - 0.03
    emit(x); SUBS.append((round(x['a'], 2), round(x['b'], 2), re.sub(r'\{[^}]*\}', '', x['text']).replace(r'\N', ' ')))

head = (KIT / 'soulchange_style.ass').read_text(encoding='utf-8').rstrip('\n')
OWN = ("Style: Narr,Jua,66,&H005AE3FF,&H005AE3FF,&H80000000,&H80000000,0,0,0,0,100,100,0,0,3,8,0,2,0,0,0,1\n"
       "Style: DlgB,Jua,62,&H00FFFFFF,&H00FFFFFF,&H33000000,&H33000000,0,0,0,0,100,100,0,0,3,10,0,2,0,0,0,1\n"
       "Style: MonoB,Jua,60,&H00E6F2FF,&H00E6F2FF,&H33402A20,&H33402A20,0,0,0,0,100,100,0,0,3,10,0,2,0,0,0,1\n"
       "Style: TagJ,Jua,54,&H00FFFFFF,&H00FFFFFF,&H009A4FE0,&H009A4FE0,0,0,0,0,100,100,0,0,3,9,0,2,0,0,0,1\n"
       "Style: TagT,Jua,54,&H00FFFFFF,&H00FFFFFF,&H00C07A2A,&H00C07A2A,0,0,0,0,100,100,0,0,3,9,0,2,0,0,0,1\n"
       "Style: TagW,Jua,54,&H00FFFFFF,&H00FFFFFF,&H00606066,&H00606066,0,0,0,0,100,100,0,0,3,9,0,2,0,0,0,1\n"
       "Style: TagJi,Jua,54,&H00C88CFF,&H00C88CFF,&H00303038,&H00303038,0,0,0,0,100,100,0,0,3,9,0,2,0,0,0,1\n"
       "Style: TagTi,Jua,54,&H00FFC88C,&H00FFC88C,&H00303038,&H00303038,0,0,0,0,100,100,0,0,3,9,0,2,0,0,0,1")
head = head.replace('\n[Events]', '\n' + OWN + '\n[Events]', 1)
assert 'TagJ,' in head
(B / 'ep7.ass').write_text(head + '\n' + '\n'.join(EV) + '\n', encoding='utf-8')

# ---------- 6. 합치기 ----------
en_j = '+'.join(f"between(t,{c['start']},{c['start'] + c['dur'] - 0.001:.3f})" for c in CUTS if c['pip'] == 'pip')
en_t = '+'.join(f"between(t,{c['start']},{c['start'] + c['dur'] - 0.001:.3f})" for c in CUTS if c['pip'] == 'pip_t')
vf = (f"[1:v]scale=300:300[pj];[2:v]scale=300:300[pt];[3:v]setpts=PTS-STARTPTS+{GLITCH[0]:.3f}/TB[gl];"
      f"[0:v][pj]overlay=x=750:y=130:enable='{en_j}'[a];[a][pt]overlay=x=750:y=130:enable='{en_t}'[b];"
      f"[b][gl]overlay=x=750:y=130:eof_action=pass:enable='between(t,{GLITCH[0]:.3f},{GLITCH[1]:.3f})'[c];"
      f"[c]ass={B / 'ep7.ass'}:fontsdir={KIT / 'fonts'},format=yuv420p[vout]")
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', B / 'joined.mp4', '-i', KIT / 'pip.png', '-i', KIT / 'pip_t.png',
     '-framerate', FPS, '-i', GDIR / 'g_%02d.png',
     '-filter_complex', vf, '-map', '[vout]', '-t', MAIN, '-r', FPS, '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', B / 'main_v.mp4'])
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', B / 'ending_ep7.mp4', '-an', '-vf', f'fps={FPS},format=yuv420p,setsar=1',
     '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', B / 'ending_v.mp4'])
(B / 'vlist.txt').write_text(f"file '{B / 'main_v.mp4'}'\nfile '{B / 'ending_v.mp4'}'\n")
out = HERE / 'ep7_v1.mp4'
run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', B / 'vlist.txt', '-i', B / 'mix.wav',
     '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-t', TOT, '-movflags', '+faststart', out])
json.dump({'main': MAIN, 'ending': END_LEN, 'total': TOT, 'loudness_LUFS': I2, 'true_peak_dBTP': TP2,
           'cuts': [{kk: (str(vv) if isinstance(vv, pathlib.Path) else vv) for kk, vv in c.items()} for c in CUTS],
           'lines': {lid: {'start': L[lid], 'end': round(L[lid] + D[lid], 3), 'tempo': SPEC[lid]['tempo'], 'file': SPEC[lid]['f'],
                           'range': SPEC[lid]['r'], 'inner': lid in INNER} for lid in sorted(L, key=L.get)},
           'subs': SUBS, 'glitch': GLITCH, 'bgm': BGM_SECT, 'placeholders': [c['id'] for c in CUTS if c['fx'] == 'ph']},
          open(HERE / 'timeline_v1.json', 'w'), ensure_ascii=False, indent=1)
print('OK', out, TOT, '임시 화면:', [c['id'] for c in CUTS if c['fx'] == 'ph'])
