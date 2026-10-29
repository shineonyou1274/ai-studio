#!/usr/bin/env python3
"""소울체인지 8화 편집 v1 (대본 v5, 사장님 2026-10-29 "70초 넘어도 돼. 립싱크만 맞으면 되지").

흐름
- K1 교무실: 교감(화면 밖) "상담 보고서 오늘 안에" → 담임 몸(지우 영혼) "넵!" + 새끼손가락으로 귀 뒤로 넘김 (립싱크 컷)
- K2 보고서 작성자 칸: 펜 → 코드 확대 `지우` 박박 → `김○○` / 속마음 "...큰일 날 뻔."
- K3 같은 시각 교실(7화 K4 재사용, 좌우 반전) → 담임 영혼 DM "최 쌤은 원칙만, 나는 과자랑 유튜브만. 둘 다 걔를 몰랐지."
- K4a 다음 날 문간 남학생 셋 → 사과 / K5a "너희가, 이걸 다 알아?"(립싱크) / K6 목록(코드) / K5b "꺄, 나도 딸기우유—"(빙의 풀림, 립싱크) / K4b "변성기다"
- K7 병가 중인 최 쌤 빈 책상에 목록 붙이고 테이프 꾹꾹 + 교감 "벽에 종이…" + "넵! 안 뗄 거지만."
- K8 벤치 이어폰 / K10 늙크크 단톡 + 하은 오사카 사진 + "아악, 사건이 끊이질 않네…"
- RP 완성 보고서(코드) "여기요오." → K11a 교감 "하… 왜 자꾸 이런 일이…" 수화기(립싱크) → K11b 역광 최 쌤 "조금만 시간을 주시겠어요?"
립싱크 컷(K1·H2·K11a)은 녹음 원본을 쉼 줄이기 없이 그대로 쓰고, 컷 안 시각을 생성 때 넣은 오디오와 같게 둔다.
사용: python3 build_ep8_v1.py [--plan]
"""
import json, pathlib, random, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import vo_prep as vp
import bgm

KIT = pathlib.Path('/home/user/youtube-ops/series/_soulchange_kit')
EP = HERE.parent
V = EP / '04_생성물' / 'voices'
C = EP / '04_생성물' / 'clips'
IMG = EP / '04_생성물' / 'images'
EP7C = EP.parent / 'soulchange-ep07' / '04_생성물' / 'clips'
E6 = EP.parent / 'soulchange-ep06' / '04_생성물' / 'clips'
TAG_ = 'v1'
B = HERE / f'build_{TAG_}'; B.mkdir(exist_ok=True)
VO = B / 'vo'; VO.mkdir(exist_ok=True)
FONT = KIT / 'fonts/Jua-Regular.ttf'
FPS, W, H = 30, 1080, 1920
END_LEN = 5.7
ENDING = B / 'ending_ep8.mp4'          # make_ending.py 8 일 ("다음 화 일요일 18시")
f = lambda s: ImageFont.truetype(str(FONT), s)


def run(cmd, **kw):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, **kw)
    if r.returncode: raise SystemExit(' '.join(map(str, cmd)) + '\n' + r.stderr[-2000:])
    return r


def dur_of(p):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)], capture_output=True, text=True).stdout)


# ---------- 1. 대사 ----------
SPEC = {
    'A01': dict(f='E8v5-01_vp_arthur.mp3', r=[(0, 4.21)], tempo=1.10, gap=0.15),        # 교감 "김 선생, 어제 상담 보고서. 오늘 안에 내요. 조용히."
    'KN': dict(f='E8v5-03_jiu_inner_student.mp3', r=[(0, 1.41)], tempo=1.0),           # 속마음 "...큰일 날 뻔."
    'DM5': dict(f='E8v5-05_teacher_dm_teacher.mp3', r=[(0, 7.16)], tempo=1.12, gap=0.22),  # DM "최 쌤은 원칙만, 나는 과자랑 유튜브만. 둘 다 걔를 몰랐지."
    'S1a': dict(f='E8v5-07_s1_dylan.mp3', r=[(0, 3.60)], tempo=1.0, gap=0.25),          # "아, 밀지 마... 쌤, 이거요."
    'S1b': dict(f='E8v5-07_s1_dylan.mp3', r=[(3.60, 7.48)], tempo=1.0, gap=0.30),       # "...최 쌤한테, 텀블러로 놀린 거... 죄송하다고요."
    'S1c': dict(f='E8v5-07_s1_dylan.mp3', r=[(7.48, 9.94)], tempo=1.0, gap=0.20),       # "다 알죠. 맨날 같이 있는데."
    'S1d': dict(f='E8v5-07_s1_dylan.mp3', r=[(9.94, 12.28)], tempo=1.05, gap=0.20),     # "...방금, 쌤 목소리 왜 저래?"
    'BYS': dict(f='E8v5-08_jiu_teacherbody.mp3', r=[(0, 1.54)], tempo=1.0),             # "...벼, 변성기다."
    'NA': dict(f='E8v5-08_jiu_teacherbody.mp3', r=[(1.54, 3.50)], tempo=1.05, gap=0.20),  # "넵! ...안 뗄 거지만."
    'YGY': dict(f='E8v5-08_jiu_teacherbody.mp3', r=[(3.50, 4.99)], tempo=1.0),          # "여기요오."
    'EM': dict(f='E8v5-09_jiu_inner_student.mp3', r=[(0, 3.47)], tempo=1.05),          # 속마음 "엄마도 모르는 걸, 애들은 알았네."
    'VPW': dict(f='E8v5-10_vp_arthur.mp3', r=[(0, 3.96)], tempo=1.08, gap=0.15),        # 교감 "거, 벽에 종이 붙이지 맙시다. 이사장님 오시는데."
    'JAK': dict(f='E8v5-11_teacher_inner_teacher.mp3', r=[(0, 2.77)], tempo=1.0),      # 담임 속마음 "...작년엔, 내가 틀어 줬는데."
    'OLD1': dict(f='E8v5-12_teacher_studentbody.mp3', r=[(0, 8.28)], tempo=1.20, gap=0.22),   # "키읔, 키읔, 키읔... 다들... 영크크하게... 방가방가... 물결..."
    'OLD2': dict(f='E8v5-12_teacher_studentbody.mp3', r=[(8.28, 11.92)], tempo=1.08, gap=0.25),   # "...웃는 눈인데. ...이거밖에 못 하나, 나."
    'OLD3': dict(f='E8v5-12_teacher_studentbody.mp3', r=[(11.92, 17.87)], tempo=1.15, gap=0.20),  # "아악, 사건이 끊이질 않네... 하은이네 일본 갔다 오면, 이제 또 어떻게 하냐."
    'CHOI': dict(f='E8v5-13_choi_celine.mp3', r=[(0, 7.55)], tempo=1.06, gap=0.25),     # 최 쌤 "교감 선생님, 아직 아이 이야기는 하나도 안 들었잖아요. 조금만 시간을 주시겠어요?"
}
D = vp.prep(SPEC, V, VO)
# 립싱크 컷용: 쉼 줄이기·빠르기 없이 원본 그대로(생성 때 넣은 오디오와 같은 시각)
RAW = {'NEP': ('E8v5-02_jiu_teacherbody.mp3', 0, 0.91), 'NEO': ('E8v5-04_jiu_teacherbody.mp3', 0, 2.35),
       'LEAK': ('E8v5-06a_jiu_leak_student.mp3', 0, 2.19), 'VPH': ('E8v5-10_vp_arthur.mp3', 3.90, 7.00)}
for lid, (fn, a_, b_) in RAW.items():
    x = vp.decode(V / fn, a_, b_); tmp = VO / f'{lid}_t.wav'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(vp.SR), '-ac', '1', '-i', '-', str(tmp)], input=x.astype(np.float32).tobytes(), check=True)
    g = -18.0 - vp.lufs(tmp)
    run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-af', f'volume={g:.2f}dB,alimiter=limit=0.7:level=false:attack=1:release=50,afade=t=in:d=0.01,areverse,afade=t=in:d=0.02,areverse',
         '-ar', '48000', '-c:a', 'pcm_s16le', VO / f'{lid}.wav'])
    tmp.unlink(); D[lid] = round(dur_of(VO / f'{lid}.wav'), 3); SPEC[lid] = dict(f=fn, r=[(a_, b_)], tempo=1.0)
INNER = {'KN', 'EM', 'JAK', 'LEAK'}      # 속마음·빙의 풀림 = 영혼 목소리 + 잔향

# ---------- 2. 컷 ----------
L, CUTS = {}, []
t = 0.0
def cut(cid, src, ss, dur, pip='pip', stretch=1.0, zoom=(1.0, 0.5, 0.5), fx=None, vfx='', hold=False, note=''):
    """src의 ss부터 stretch배로 늘려 dur초. 원본이 모자라면 hold=True일 때 끝 프레임을 멈춰 천천히 다가감."""
    global t
    CUTS.append(dict(id=cid, src=src, ss=ss, dur=round(dur, 3), pip=pip, stretch=stretch, zoom=zoom, fx=fx, vfx=vfx, hold=hold, start=round(t, 3), note=note))
    t += dur
def at(lid, x):
    L[lid] = round(x, 3); return x + D[lid]
def end_(lid): return L[lid] + D[lid]
def fit(src, ss, need, lo=1.0, hi=1.15):
    avail = dur_of(src) - ss - 0.04
    return min(hi, max(lo, need / avail))

K1C, K2C, K4C, H2C, K7C, K8C, K11A, K11B = (C / f'{n}.mp4' for n in ('K1', 'K2', 'K4', 'H2', 'K7', 'K8', 'K11a', 'K11b'))
# K1 — 교감(화면 밖) → "넵!"(립싱크: 생성 오디오 3.70초) → 새끼손가락 귀 넘김
c0 = t; e = at('A01', c0 + 0.05)
s1 = min(1.25, max(1.0, (e + 0.12) / 3.70)); NEP_T = c0 + 3.70 * s1
at('NEP', NEP_T)
cut('K1', K1C, 0, dur_of(K1C) * s1 - 0.05, stretch=s1, note=f'담임 몸 끄덕끄덕 → "넵!"(원본 3.70초, x{s1:.2f}) → 귀 뒤로 넘김')
TUCK = (end_('NEP') + 0.1, c0 + dur_of(K1C) * s1 - 0.05)
# K2 — 펜(원본 0–2.4) → 코드 확대: 작성자 칸
cut('K2v', K2C, 0, 2.4, note='보고서 작성자 칸에 펜으로 씀')
c0 = t; SCRIB = (c0 + 0.55, c0 + 1.05); KIMT = c0 + 1.15
e = at('KN', c0 + 1.25)
cut('K2c', None, 0, max(2.4, e + 0.25 - c0), fx='box', note='코드: 작성자 칸 지우 → 박박 → 김○○')
# K3 — 같은 시각 교실(7화 K4 0–2.6 좌우 반전) → DM 화면
cut('K3a', EP7C / 'K4.mp4', 0.0, 2.3, pip='pip_t', vfx='hflip,', note='7화 K4 재사용(좌우 반전) — 지우 몸 검지 타자')
c0 = t; e = at('DM5', c0 + 0.15)
cut('K3b', None, 0, e + 0.45 - c0, pip='pip_t', fx='dm5', note='코드: 지우 폰에서 담임 영혼이 보냄')
SEND3 = end_('DM5') + 0.03
# K4a — 다음 날 문간: 떠밀기(0–2.5) → 종이 내밂(2.5–7.5)
c0 = t; e = at('S1a', c0 + 0.20); SHOVE = c0 + 0.9
e = at('S1b', max(e + 0.25, c0 + 2.6))
need = e + 0.20 - c0; k4s = fit(K4C, 0, need, hi=1.10) if need > 7.4 else 1.0
cut('K4a', K4C, 0, need, stretch=k4s, hold=True, note='남학생 셋 뒷모습: 떠밀기 → 종이 내밂')
# K5a — "너희가, 이걸 다 알아?" (립싱크: 생성 오디오 0.20초)
c0 = t; at('NEO', c0 + 0.20); RUSTLE = c0 + 0.05
cut('K5a', H2C, 0, 2.85, note='담임 몸 종이 받아 가슴에 꼭 → "너희가, 이걸 다 알아?"')
# K6 — 목록(코드)
c0 = t; e = at('S1c', c0 + 0.20)
K6D = max(4.2, e + 0.9 - c0); K6Z = (c0 + K6D - 1.55, c0 + K6D - 1.0)      # '센 향수 냄새' 멈춤 → 0.55초 뒤 '딸기우유'로 줌
cut('K6', None, 0, K6D, fx='list', note='코드: 아이들 목록 — 센 향수 냄새에서 멈춤 → 딸기우유로 줌')
# K5b — "꺄, 나도 딸기우유—"(립싱크: 생성 오디오 3.10초 → 원본 2.85부터라 컷 안 0.25초)
c0 = t; e = at('LEAK', c0 + 0.25); GLITCH = (L['LEAK'], min(end_('LEAK'), L['LEAK'] + 1.6))
e = at('S1d', e + 0.15)
cut('K5b', H2C, 2.85, min(dur_of(H2C) - 2.85 - 0.04, e - c0 + 0.1), note='담임 몸 손으로 입 → 굳은 웃음, 눈만 아이들 쪽')
# K4b — 문간 셋 서로 쳐다봄, 맨 뒤 웃음 참기(원본 7.5–10) — "변성기다" → 큽
c0 = t; e = at('BYS', max(end_('S1d') + 0.20, c0 + 0.25)); KUP = e + 0.30
cut('K4b', K4C, 7.5, max(2.4, KUP + 0.55 - c0), stretch=1.0, hold=True, note='셋 서로 쳐다봄 → 맨 뒤 웃음 참기')
# K7 — 빈 최 쌤 책상: 종이 붙임(0–4) → 테이프 꾹꾹(4–8)
c0 = t; e = at('EM', c0 + 0.30)
e = at('VPW', e + 0.20)
e = at('NA', e + 0.12)
need = e + 0.35 - c0; k7s = fit(K7C, 0, need)
cut('K7', K7C, 0, need, stretch=k7s, hold=True, note='병가 중 최 쌤 빈 책상 — 목록 붙이고 테이프 꾹꾹')
TAPE = [c0 + x * k7s for x in (4.6, 5.6, 6.9)]
# K8 — 벤치(뒤에서): 조심조심 앉음 → 이어폰 받아 꾸벅
c0 = t; e = at('JAK', c0 + 2.30)
need = e + 0.35 - c0; k8s = fit(K8C, 0, need)
cut('K8', K8C, 0, need, pip='pip_t', stretch=k8s, hold=True, note='벤치: 지우 몸 아저씨처럼 앉음 → 이어폰 받음')
# K10 — 늙크크 단톡(코드)
c0 = t; e = at('OLD1', c0 + 0.35); SENT = e + 0.10
CHAT = [(SENT, 'me', 'ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ\n다들 영크크하게\n방가방가~^^'), (SENT + 0.35, '민서', '?'), (SENT + 0.70, '반장', '지우 늙크크됨?ㅋ'),
        (SENT + 1.05, '체육부장', '구려ㅋ 누가 요즘 ^^ 씀'), (SENT + 1.45, '민서', '근데 이 드라마 만든 사람도\n올크크 아님?ㅋ')]
e = at('OLD2', SENT + 1.95); DEL = e + 0.10
CHAT += [(DEL + 0.35, '민서', '이미 캡처함ㅋ'), (DEL + 0.85, '하은', '[사진]\n오사카 도착~')]
e = at('OLD3', DEL + 1.30)
cut('K10', None, 0, e + 0.45 - c0, pip='pip_t', fx='chat', note='코드: 반 단톡 — 늙크크 → 삭제 → 하은 오사카 사진')
# RP — 완성 보고서(코드) "여기요오."
c0 = t; e = at('YGY', c0 + 0.15)
cut('RP', None, 0, max(2.2, e + 0.35 - c0), fx='report', note='코드: 완성된 상담 보고서(판단하지 않음 밑줄)')
# K11a — 교감 "하... 왜 자꾸 이런 일이..." (립싱크: 생성 오디오 0.60초) → 수화기
c0 = t; at('VPH', c0 + 0.60); CLACK = c0 + 4.1
cut('K11a', K11A, 0, dur_of(K11A) - 0.05, note='교감 이마 짚고 한숨 → 수화기 듦')
# K11b — 역광 최 쌤
c0 = t; DOOR = c0 + 0.15; e = at('CHOI', c0 + 1.30)
need = e + 0.70 - c0; kbs = fit(K11B, 0, need)
cut('K11b', K11B, 0, need, stretch=kbs, hold=True, note='문 열림 → 역광 최 쌤 실루엣')
MAIN = round(t, 3); TOT = round(MAIN + END_LEN, 3)
print('본편', MAIN, '합계', TOT)
for c in CUTS:
    if c['src'] is None: print(f"  {c['id']:5s} {c['start']:6.2f} +{c['dur']:.2f}  {c['fx']}"); continue
    avail = (dur_of(c['src']) - c['ss']) * c['stretch']
    print(f"  {c['id']:5s} {c['start']:6.2f} +{c['dur']:.2f}  src {c['ss']}+ x{c['stretch']:.2f}" + (f"  멈춤 {c['dur'] - avail:.2f}" if c['dur'] > avail + 0.02 else ''))
for lid in sorted(L, key=L.get): print(f"    {lid:5s} {L[lid]:6.2f}-{end_(lid):6.2f}")
if '--plan' in sys.argv: sys.exit(0)


# ---------- 3. 영상 조각 ----------
def grab(src, tsec, flip=False):
    vf = 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920' + (',hflip' if flip else '')
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{tsec}', '-i', str(src), '-frames:v', '1', '-vf', vf, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    return Image.frombytes('RGB', (W, H), raw[:W * H * 3])


def push_frames(img, n, z1=0.06, z0=1.0):
    out = []
    for i in range(n):
        z = z0 + z1 * i / max(1, n - 1); w, h = W / z, H / z
        out.append(np.asarray(img.transform((W, H), Image.EXTENT, ((W - w) / 2, (H - h) / 2 * 0.8, (W + w) / 2, (H - h) / 2 * 0.8 + h), Image.BICUBIC), np.uint8))
    return out


def drift(fr, z1=0.035):
    n = len(fr); out = []
    for i, a_ in enumerate(fr):
        z = 1.0 + z1 * i / max(1, n - 1); w, h = W / z, H / z
        out.append(np.asarray(Image.fromarray(a_).transform((W, H), Image.EXTENT, ((W - w) / 2, (H - h) / 2, (W + w) / 2, (H + h) / 2), Image.BILINEAR), np.uint8))
    return out


def write_frames(fr, out):
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p', str(out)], input=np.stack(fr).tobytes(), check=True)


def dim_blur(img, s=14, k=0.55):
    return Image.fromarray((np.asarray(img.filter(ImageFilter.GaussianBlur(s)), float) * k).astype(np.uint8))


def txt(d, xy, s, font, fill, anchor='la'):
    """Jua에 없는 ○는 직접 그림."""
    x, y = xy
    if '○' not in s:
        d.text((x, y), s, font=font, fill=fill, anchor=anchor); return
    size = font.size; total = sum(size * 0.9 if ch == '○' else d.textlength(ch, font=font) for ch in s)
    if anchor[0] == 'r': x -= total
    elif anchor[0] == 'm': x -= total / 2
    for ch in s:
        if ch == '○':
            r_ = size * 0.36; cy = y + size * 0.55 if anchor[1] == 'a' else y
            d.ellipse([x + size * 0.08, cy - r_, x + size * 0.08 + 2 * r_, cy + r_], outline=fill, width=max(3, size // 14)); x += size * 0.9
        else:
            d.text((x, y), ch, font=font, fill=fill, anchor='l' + anchor[1]); x += d.textlength(ch, font=font)


def report_img(scale=1.0, author='김○○', scribble=1.0, hl=False):
    """상담 보고서 A4 한 장(RGB)."""
    pw, ph = 900, 1272
    im = Image.new('RGB', (pw, ph), (250, 250, 247)); d = ImageDraw.Draw(im)
    pen = (35, 38, 48)
    d.text((pw // 2, 70), '학부모 상담 결과 보고', font=f(54), fill=pen, anchor='ma')
    d.line([(60, 150), (pw - 60, 150)], fill=pen, width=3)
    rows = ['일시: 10월 ○일', '장소: 상담실', '참석: 학부모(어머니), 작년 담임']
    for i, r_ in enumerate(rows): txt(d, (70, 180 + i * 56), r_, f(34), pen)
    d.line([(60, 360), (pw - 60, 360)], fill=(180, 180, 180), width=2)
    items = ['1. 어머니는 작년 담임이 학생에게', '    정서학대를 했다고 말씀하심.', '2. 상담 중 어머니가 쓴 표현 가운데', '    하나가 학생 쪽지의 표현과 같음.',
             '3. 같은 반 학생들에 따르면, 학생은', '    센 향수 냄새, 큰 소리, 갑자기 어깨를', '    만지는 것을 힘들어함.',
             '4. 확인된 사실만 적었으며,', '    학대 여부는 판단하지 않음.']
    for i, r_ in enumerate(items):
        y = 390 + i * 62; txt(d, (70, y), r_, f(36), pen)
        if hl and i == 8: d.rectangle([150, y + 44, 640, y + 54], fill=(255, 214, 40))
    # 작성자 칸
    d.rectangle([380, 1040, pw - 30, 1180], outline=pen, width=3); d.line([(510, 1040), (510, 1180)], fill=pen, width=3)
    d.text((445, 1110), '작성자', font=f(34), fill=pen, anchor='mm')
    if scribble > 0:
        hand = (40, 60, 150)
        d.text((535, 1070), '지우', font=f(64), fill=hand)
        rnd = random.Random(3)
        n_ = int(14 * min(1, scribble))
        for j in range(n_):
            y0 = 1080 + rnd.randint(0, 50); d.line([(525 + rnd.randint(-6, 6), y0), (675 + rnd.randint(-8, 8), y0 + rnd.randint(-14, 14))], fill=hand, width=6)
    if author: txt(d, (700, 1072), author, f(54), (40, 60, 150))
    return im


def box_frames(c):
    """K2c: 작성자 칸 확대 — 지우 → 박박 → 김○○."""
    n = round(c['dur'] * FPS); bg = dim_blur(grab(K2C, 1.5), 10, 0.7); out = []
    for i in range(n):
        tt = c['start'] + i / FPS
        sc = 0 if tt < SCRIB[0] else min(1, (tt - SCRIB[0]) / (SCRIB[1] - SCRIB[0]))
        im_r = report_img(author='김○○' if tt >= KIMT else '', scribble=1.0 if sc == 0 else 1.0 + sc * 0)
        if sc > 0:   # 박박: 줄 수를 시간에 따라 늘림
            dd = ImageDraw.Draw(im_r); rnd = random.Random(7)
            for j in range(int(18 * sc)):
                y0 = 1078 + rnd.randint(0, 56); dd.line([(520 + rnd.randint(-6, 6), y0), (680 + rnd.randint(-8, 8), y0 + rnd.randint(-16, 16))], fill=(40, 60, 150), width=8)
        crop = im_r.crop((360, 1000, 900, 1220)).resize((1040, 424), Image.LANCZOS)
        im = bg.copy(); im.paste(crop, (20, 690))
        out.append(np.asarray(im, np.uint8))
    return drift(out, 0.05)


def report_frames(c):
    n = round(c['dur'] * FPS); bg = dim_blur(grab(K11A, 0.3), 16, 0.5)
    rp = report_img(hl=True).resize((700, 989), Image.LANCZOS)
    out = []
    for i in range(n):
        lt = i / FPS; im = bg.copy(); dy = int(max(0, 1 - lt / 0.25) * 500)   # 아래에서 쑥 내밂
        im.paste(rp, (190, 200 + dy)); out.append(np.asarray(im, np.uint8))
    return drift(out, 0.04)


def list_frames(c):
    """K6: 공책 종이 위 여러 사람 글씨가 줄마다 나타남 → 센 향수 냄새 멈춤 → 딸기우유로 줌."""
    n = round(c['dur'] * FPS)
    paper = Image.open(IMG / 'K6_종이.png').convert('RGB').resize((1080, 1930), Image.LANCZOS).crop((0, 5, 1080, 1925))
    LINES = [('걔가 좋아하는 거', (40, 40, 50), 68, -1.5), ('- 이어폰으로 같은 노래 반복', (30, 60, 160), 54, 1.0), ('- 운동장 끝 벤치', (60, 60, 60), 56, -0.5),
             ('- 딸기우유', (200, 60, 110), 60, 1.5), ('- 혼자 있는 10분', (30, 60, 160), 54, -1.0), ('', None, 0, 0),
             ('싫어하는 거', (40, 40, 50), 68, 0.8), ('- 센 향수 냄새', (60, 60, 60), 58, -1.2), ('- 큰 소리', (30, 60, 160), 54, 0.5),
             ('- 갑자기 어깨 만지는 거', (200, 60, 110), 52, -0.8), ('', None, 0, 0), ('- ○반 애들', (40, 40, 50), 54, 0)]
    y0, lh = 250, 118
    base_imgs = []
    shown = [k for k, l in enumerate(LINES) if l[1]]
    t_show = {k: 0.15 + j * 0.22 for j, k in enumerate(shown)}
    PERF, STRAW = 7, 3
    for i in range(n):
        tt = c['start'] + i / FPS; lt = i / FPS
        im = paper.copy(); d = ImageDraw.Draw(im)
        for k, (s, col, sz, rot) in enumerate(LINES):
            if not col or lt < t_show[k]: continue
            layer = Image.new('RGBA', (1000, sz + 40), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
            txt(ld, (10, 10), s, f(sz), col + (255,)); layer = layer.rotate(rot, resample=Image.BICUBIC, expand=False)
            im.paste(layer, (130, y0 + k * lh), layer)
        if tt >= K6Z[0]:   # 센 향수 냄새 빨간 밑줄
            k_ = min(1, (tt - K6Z[0]) / 0.25); yy = y0 + PERF * lh + 78
            d.line([(150, yy), (150 + 470 * k_, yy)], fill=(225, 40, 40), width=8)
        if tt >= K6Z[1]:   # 딸기우유로 빠른 줌
            z = 1 + 0.9 * min(1, (tt - K6Z[1]) / 0.25); cx, cy = 360, y0 + STRAW * lh + 40
            w, h = W / z, H / z; x0 = min(max(0, cx - w / 2), W - w); y_ = min(max(0, cy - h / 2), H - h)
            im = im.transform((W, H), Image.EXTENT, (x0, y_, x0 + w, y_ + h), Image.BICUBIC)
        base_imgs.append(np.asarray(im, np.uint8))
    return base_imgs


def phone_base(bg, header, y0=300, ph_=1330):
    im = bg.copy(); d = ImageDraw.Draw(im)
    x0, pw = 110, 860
    d.rounded_rectangle([x0, y0, x0 + pw, y0 + ph_], 70, fill=(22, 22, 26))
    sx0, sy0, sx1, sy1 = x0 + 22, y0 + 22, x0 + pw - 22, y0 + ph_ - 22
    d.rounded_rectangle([sx0, sy0, sx1, sy1], 52, fill=(186, 206, 224))
    d.rectangle([sx0, sy0 + 40, sx1, sy0 + 150], fill=(170, 192, 214))
    d.text((sx0 + 34, sy0 + 95), header, font=f(42), fill=(30, 30, 30), anchor='lm')
    return im, (sx0, sy0, sx1, sy1)


def dm5_frames(c):
    n = round(c['dur'] * FPS); bg = dim_blur(grab(EP7C / 'K4.mp4', 1.2, flip=True))
    out = []
    for i in range(n):
        tt = c['start'] + i / FPS
        im, (sx0, sy0, sx1, sy1) = phone_base(bg, '<  쌤 (지금 지우 몸)'); d = ImageDraw.Draw(im)
        d.text((sx1 - 34, sy0 + 190), '담임 영혼이 보냄', font=f(34), fill=(40, 110, 200), anchor='ra')
        if tt >= L['DM5']:
            sc = min(1.0, 0.6 + (tt - L['DM5']) / 0.12 * 0.4); fs = int(60 * sc); lines = ['최 쌤은 원칙만,', '나는 과자랑 유튜브만.', '둘 다 걔를 몰랐지.']
            lh = int(76 * sc); tw = max(d.textlength(l, font=f(fs)) for l in lines); bh = lh * 3 + 34; y = sy0 + 250
            d.rounded_rectangle([sx1 - 30 - tw - 48, y, sx1 - 30, y + bh], 30, fill=(80, 150, 230))
            for j, l in enumerate(lines): d.text((sx1 - 54, y + 17 + j * lh), l, font=f(fs), fill=(255, 255, 255), anchor='ra')
        d.rounded_rectangle([sx0 + 24, sy1 - 120, sx1 - 24, sy1 - 40], 40, fill=(255, 255, 255))
        d.text((sx0 + 60, sy1 - 80), '입력 중...' if tt < L['DM5'] + 0.2 else '메시지 입력', font=f(38), fill=(170, 170, 180), anchor='lm')
        out.append(np.asarray(im, np.uint8))
    return drift(out)


def chat_frames(c):
    """K10: 반 단톡. 입력창에 한 글자씩(독수리) → 보냄 → 아이들 말풍선 → 내 말풍선 삭제 → 하은 사진."""
    n = round(c['dur'] * FPS); bg = dim_blur(grab(E6 / 'H3_K10.mp4', 0.2), 16, 0.5)
    typed = 'ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ 다들 영크크하게 방가방가~^^'
    t0, t1 = L['OLD1'], SENT - 0.05
    out = []
    for i in range(n):
        tt = c['start'] + i / FPS
        im, (sx0, sy0, sx1, sy1) = phone_base(bg, '<  우리 반 (28)', 250, 900); d = ImageDraw.Draw(im)
        items = [(ta, who, s) for ta, who, s in CHAT if tt >= ta]
        y = sy0 + 180
        vis = []
        for ta, who, s in items:
            if who == 'me' and tt >= DEL: s = '메시지가 삭제되었습니다.'
            vis.append((ta, who, s))
        hgt = lambda s: 230 if s.startswith('[사진]') else 58 * len(s.split('\n')) + 32
        tot = sum(hgt(s) + (44 if w != 'me' else 0) + 18 for _, w, s in vis)
        y = sy1 - 150 - tot
        for ta, who, s in vis:
            sc = min(1.0, 0.6 + (tt - ta) / 0.12 * 0.4); fs = int(46 * sc); lines = s.split('\n'); lh = int(58 * sc)
            tw = max(d.textlength(l, font=f(fs)) for l in lines); bh = lh * len(lines) + 32
            if who == 'me':
                deleted = s.startswith('메시지가')
                d.rounded_rectangle([sx1 - 30 - tw - 44, y, sx1 - 30, y + bh], 28, fill=(235, 235, 235) if deleted else (255, 230, 80))
                for j, l in enumerate(lines): d.text((sx1 - 52, y + 16 + j * lh), l, font=f(fs), fill=(150, 150, 150) if deleted else (30, 30, 30), anchor='ra')
            else:
                d.text((sx0 + 40, y), who, font=f(32), fill=(60, 60, 70)); y += 44
                if s.startswith('[사진]'):
                    d.rounded_rectangle([sx0 + 30, y, sx0 + 30 + 360, y + 230], 24, fill=(255, 255, 255))
                    ph = Image.new('RGB', (330, 150), (120, 170, 220)); pd = ImageDraw.Draw(ph)
                    pd.rectangle([0, 100, 330, 150], fill=(90, 120, 90)); pd.ellipse([230, 20, 290, 80], fill=(255, 220, 140))
                    im.paste(ph.filter(ImageFilter.GaussianBlur(3)), (sx0 + 45, y + 15)); d = ImageDraw.Draw(im)
                    d.text((sx0 + 50, y + 178), '오사카 도착~', font=f(38), fill=(30, 30, 30)); bh = 230
                else:
                    d.rounded_rectangle([sx0 + 30, y, sx0 + 30 + tw + 44, y + bh], 28, fill=(255, 255, 255))
                    for j, l in enumerate(lines): d.text((sx0 + 52, y + 16 + j * lh), l, font=f(fs), fill=(30, 30, 30))
            y += bh + 18
        # 위로 밀려난 말풍선은 머리 띠 뒤로 숨김(스크롤)
        top = sy0 + 160
        im.paste(phone_base(bg, '<  우리 반 (28)', 250, 900)[0].crop((0, 0, W, top)), (0, 0)); d = ImageDraw.Draw(im)
        # 입력창: 독수리 타법(글자마다 띄엄띄엄, 중간에 한 번 지움)
        d.rounded_rectangle([sx0 + 24, sy1 - 120, sx1 - 24, sy1 - 40], 40, fill=(255, 255, 255))
        if t0 <= tt < t1:
            k_ = (tt - t0) / (t1 - t0); m_ = int(len(typed) * k_)
            if 0.45 < k_ < 0.52: m_ = max(0, m_ - 3)
            shown = typed[:m_]; shown = shown[-17:]
            d.text((sx0 + 60, sy1 - 80), shown + ('|' if int(tt * 3) % 2 else ''), font=f(40), fill=(30, 30, 30), anchor='lm')
        else:
            d.text((sx0 + 60, sy1 - 80), '메시지 입력', font=f(38), fill=(170, 170, 180), anchor='lm')
        out.append(np.asarray(im, np.uint8))
    return drift(out, 0.02)


CUTS_BY = {c['id']: c for c in CUTS}
seg_list = []
FX = {'box': box_frames, 'report': report_frames, 'list': list_frames, 'dm5': dm5_frames, 'chat': chat_frames}
for c in CUTS:
    out = B / f"seg_{c['id']}.mp4"; nfr = round(c['dur'] * FPS)
    if c['fx']:
        write_frames(FX[c['fx']](c)[:nfr], out); seg_list.append(out); continue
    z, ax, ay = c['zoom']; used = c['dur'] / c['stretch']
    vf = (f"[0:v]trim=start={c['ss']}:duration={used + 0.1:.3f},setpts=(PTS-STARTPTS)*{c['stretch']},fps={FPS},"
          f"scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920," + c['vfx'])
    if z != 1.0:
        sw, sh = int(round(1080 * z / 2) * 2), int(round(1920 * z / 2) * 2)
        vf += f"scale={sw}:{sh}:flags=lanczos,crop=1080:1920:{int((sw - 1080) * ax)}:{int((sh - 1920) * ay)},"
    vf += "setsar=1,format=rgb24[v]"
    r2 = subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(c['src']), '-filter_complex', vf, '-map', '[v]', '-frames:v', str(nfr), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    mv = list(np.frombuffer(r2, np.uint8).reshape(-1, H, W, 3))
    if len(mv) < nfr:
        mv += push_frames(Image.fromarray(mv[-1]), nfr - len(mv), 0.08 if c['hold'] else 0.02)
    write_frames(mv[:nfr], out); seg_list.append(out)
(B / 'list.txt').write_text(''.join(f"file '{p}'\n" for p in seg_list))
run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', B / 'list.txt', '-c', 'copy', B / 'joined.mp4'])

# 영혼 원 지지직(빙의 풀림) — 7화보다 세게
pip = Image.open(KIT / 'pip.png').convert('RGBA').resize((300, 300), Image.LANCZOS)
GDIR = B / 'glitch'; GDIR.mkdir(exist_ok=True)
for p_ in GDIR.glob('*.png'): p_.unlink()
gn = round((GLITCH[1] - GLITCH[0]) * FPS)
for i in range(gn):
    rnd = random.Random(i * 7 + 3); a = np.asarray(pip).copy()
    for _ in range(12):
        y0 = rnd.randint(0, 280); hgt = rnd.randint(6, 34); dx = rnd.randint(-48, 48)
        a[y0:y0 + hgt] = np.roll(a[y0:y0 + hgt], dx, axis=1)
    a[..., 0] = np.roll(a[..., 0], 9, axis=1); a[..., 2] = np.roll(a[..., 2], -9, axis=1)
    a[::3, :, :3] = (a[::3, :, :3] * 0.45).astype(np.uint8)
    Image.fromarray(a).save(GDIR / f'g_{i:02d}.png')

# ---------- 4. 소리 ----------
HALL = 'aecho=0.85:0.6:45:0.12'
ins, fc, mixl = [], [], []
for i, (lid, st) in enumerate(sorted(L.items(), key=lambda kv: kv[1])):
    ins += ['-i', VO / f'{lid}.wav']
    ch = f"[{i}:a]aresample=48000,aformat=channel_layouts=mono"
    if lid in INNER: ch += f",{HALL}"
    ch += ",acompressor=threshold=-20dB:ratio=3:attack=5:release=120"
    ch += f",aformat=channel_layouts=stereo,adelay={int(st * 1000)}:all=1[v{i}]"
    fc.append(ch); mixl.append(f'[v{i}]')
def sfx(lbl, expr, d, at_, vol=1.0):
    fc.append(f"aevalsrc='{expr}':d={d}:s=48000,volume={vol},aformat=channel_layouts=stereo,adelay={int(at_ * 1000)}:all=1[{lbl}]"); mixl.append(f'[{lbl}]')
def noise(lbl, d, at_, filt, vol):
    fc.append(f"anoisesrc=d={d}:c=pink:a=0.5:r=48000,{filt},volume={vol},aformat=channel_layouts=stereo,adelay={int(at_ * 1000)}:all=1[{lbl}]"); mixl.append(f'[{lbl}]')
k = CUTS_BY
DINGX = '0.16*sin(2*PI*1320*t)*lt(t,0.08)+0.16*sin(2*PI*1760*t)*gt(t,0.12)*lt(t,0.24)'
TAKX = '0.6*sin(2*PI*(200-90*t)*t)*exp(-40*t)+0.2*sin(2*PI*900*t)*exp(-70*t)'
SEND = '0.18*sin(2*PI*(700+1600*t)*t)*exp(-12*t)'
TINK = '0.14*sin(2*PI*1568*t)*exp(-14*t)'
sfx('sparkle', '0.10*sin(2*PI*(1800+900*t)*t)*exp(-6*t)', 0.5, TUCK[0], 0.8)                 # 귀 넘김 반짝
for j in range(6): noise(f'pen{j}', 0.12, k['K2v']['start'] + 0.3 + 0.32 * j, 'bandpass=f=3500:w=2500', 0.07)   # 펜 사각
for j in range(7): noise(f'scr{j}', 0.08, SCRIB[0] + 0.07 * j, 'bandpass=f=2500:w=2000', 0.16)            # 박박
for j in range(5): noise(f'tp{j}', 0.05, k['K3a']['start'] + 0.3 + 0.4 * j, 'bandpass=f=2000:w=1200', 0.10)   # 검지 톡
sfx('send3', SEND, 0.35, SEND3, 0.5)
sfx('shove', TAKX, 0.3, SHOVE, 0.5)
noise('rustle', 0.45, RUSTLE, 'highpass=f=2500,afade=t=in:d=0.05,afade=t=out:st=0.2:d=0.25', 0.12)
for j in range(10): noise(f'pc{j}', 0.06, k['K6']['start'] + 0.15 + 0.22 * j, 'bandpass=f=4000:w=2500', 0.06)   # 연필 사각
sfx('zing', '0.12*sin(2*PI*(400+1400*t)*t)*exp(-3*t)', 0.4, K6Z[1], 0.7)
fc.append(f"anoisesrc=d={GLITCH[1] - GLITCH[0]:.2f}:c=white:a=0.5:r=48000,highpass=f=1800,volume='0.16*lt(mod(t,0.04),0.02)*(0.6+0.4*sin(2*PI*57*t))':eval=frame,"
          f"afade=t=out:st={GLITCH[1] - GLITCH[0] - 0.15:.2f}:d=0.15,aformat=channel_layouts=stereo,adelay={int(GLITCH[0] * 1000)}:all=1[zap]"); mixl.append('[zap]')
noise('kup', 0.18, KUP, 'bandpass=f=900:w=700,afade=t=in:d=0.02,afade=t=out:st=0.08:d=0.1', 0.35)       # 웃음 참는 큽
for j, x in enumerate(TAPE): sfx(f'tape{j}', TAKX, 0.25, x, 0.45)
noise('wind', k['K8']['dur'], k['K8']['start'], 'lowpass=f=600,afade=t=in:d=0.4', 0.03)
for j in range(14): noise(f'ty{j}', 0.05, L['OLD1'] + 0.15 + (SENT - 0.3 - L['OLD1']) * j / 14, 'bandpass=f=2000:w=1200', 0.11)   # 독수리 톡...톡
sfx('send10', SEND, 0.35, SENT, 0.5)
for j, (ta, who, s) in enumerate(CHAT):
    if who != 'me': sfx(f'ding{j}', DINGX, 0.3, ta, 0.45)
sfx('del', '0.18*sin(2*PI*(900-700*t)*t)*exp(-10*t)', 0.3, DEL, 0.6)
sfx('clack', TAKX, 0.3, CLACK, 0.7)
fc.append(f"anoisesrc=d=0.9:c=brown:a=0.6:r=48000,bandpass=f=600:w=500,volume='0.35*(0.6+0.4*sin(2*PI*9*t))':eval=frame,afade=t=in:d=0.1,afade=t=out:st=0.6:d=0.3,"
          f"aformat=channel_layouts=stereo,adelay={int(DOOR * 1000)}:all=1[door]"); mixl.append('[door]')     # 문 끼익
def amb(lbl, a, b, lo, hi, vol):
    a0 = max(0, a - 0.3)
    fc.append(f"anoisesrc=d={b - a0:.2f}:c=pink:a=0.5:r=48000,bandpass=f={(lo + hi) // 2}:w={hi - lo},volume={vol},"
              f"afade=t=in:d=0.3,afade=t=out:st={b - a0 - 0.3:.2f}:d=0.3,aformat=channel_layouts=stereo,adelay={int(a0 * 1000)}:all=1[{lbl}]"); mixl.append(f'[{lbl}]')
for c in CUTS:
    a, b = c['start'], c['start'] + c['dur']
    if c['id'] in ('K3a', 'K3b', 'K10'): amb(f"am_{c['id']}", a, b, 500, 2500, 0.022)
    elif c['id'] == 'K8': amb(f"am_{c['id']}", a, b, 200, 800, 0.014)
    else: amb(f"am_{c['id']}", a, b, 300, 2800, 0.016)
fc.append(f"anoisesrc=d={MAIN}:c=brown:a=0.5:r=48000,lowpass=f=350,volume=0.0105,afade=t=in:d=0.5,afade=t=out:st={MAIN - 0.4}:d=0.4,aformat=channel_layouts=stereo[room]"); mixl.append('[room]')
# 배경음: 교무실 가벼움 → 교실 DM(미스터리) → 아이들(펄스) → 딸기우유 직전 뚝 → 변성기 뒤 펄스 → 최 쌤 책상(가벼움) → 벤치(잔잔) → 단톡(펄스) → 보고서·교감(대치) → 문 열리기 직전 뚝 → 최 쌤(잔잔)
BGM_SECT = [('class', 0.0, k['K3a']['start']), ('mystery', k['K3a']['start'], k['K4a']['start']), ('pulse', k['K4a']['start'] + 0.1, L['LEAK'] - 0.05),
            ('pulse', KUP + 0.1, k['K7']['start']), ('class', k['K7']['start'], k['K8']['start']), ('mystery', k['K8']['start'], k['K10']['start']),
            ('pulse', k['K10']['start'], k['RP']['start']), ('confront', k['RP']['start'], DOOR - 0.05), ('mystery', L['CHOI'] - 0.2, MAIN)]
BGM_I = bgm.make(BGM_SECT, [(VO / f'{lid}.wav', st) for lid, st in L.items()], MAIN, B / 'bgm.wav', target_lufs=-21.0, duck_db=-15.0, release=0.2)
ins += ['-i', B / 'bgm.wav']; mixl.append(f'[{len(ins) // 2 - 1}:a]')
fc.append(''.join(mixl) + f"amix=inputs={len(mixl)}:normalize=0,apad=whole_dur={MAIN},atrim=0:{MAIN}[aout]")
run(['ffmpeg', '-y', '-loglevel', 'error', *ins, '-filter_complex', ';'.join(fc), '-map', '[aout]', '-ar', '48000', B / 'mix_raw.wav'])
def meas(p):
    m = subprocess.run(['ffmpeg', '-i', str(p), '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', m)[-1]), float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', m)[-1])
I0, _ = meas(B / 'mix_raw.wav')
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', B / 'mix_raw.wav', '-af', f'volume={-14.0 - I0:.2f}dB,alimiter=limit=0.58:level=false:attack=2:release=60', '-ar', '48000', B / 'mix_main.wav'])
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', ENDING, '-vn', '-ar', '48000', '-ac', '2', B / 'ending.wav'])
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
def say(lid, text, tag, col='', style='Dlg', hold=0.15, end=None, start=None, grp=None):
    if lid not in L: return
    a = start if start is not None else L[lid]; b = end if end else L[lid] + D[lid] + hold
    PEND.append(dict(a=a, b=b, text=text, tag=tag, col=col, style=style, grp=grp or lid))
def emit(x):
    fad = r'\fad(60,100)'
    if x['grp'] == 'LEAK':   # 빙의 풀림: 분홍 상자 번쩍
        fad = r'\3a&H00&\3c&HB45FFF&\t(0,70,\3c&H000000&)\t(70,140,\3c&HB45FFF&)\t(140,210,\3c&H000000&)\t(210,280,\3c&HB45FFF&)\t(280,400,\3c&H000000&)\t(400,480,\3c&HB45FFF&)'
    ev(x['a'], x['b'], x['style'] + 'B', r'{\an2\pos(540,1330)' + fad + '}' + x['text'], 2)
    if x['tag']:
        ty = 1181 if r'\N' in x['text'] else 1243
        ev(x['a'], x['b'], TAGSTYLE[(x['col'], x['style'] == 'Mono')], rf"{{\an2\pos(540,{ty})\fad(60,100)}}{x['tag']}", 3)
def narr(a, b, text, x=40, y=430):
    ev(a, b, 'Narr', rf'{{\an7\pos({x},{y})\frz5\fad(120,150)}}{text}', 8)
def scene(a, b, text):
    ev(a, b, 'Scene', r'{\an7\pos(40,240)}' + text, 6)
cs = lambda i: k[i]['start']; ce = lambda i: k[i]['start'] + k[i]['dur']

ev(0.0, ce('K2c'), 'Label', r'{\an7\pos(40,140)}담임과 학생, 몸이 바뀌었다', 6)
ev(0.0, 0.62, 'Label', r'{\an5\pos(540,640)\bord0\shad0\1c&H000000&\1a&H28&\p1\fad(0,120)}m 0 0 l 1080 0 1080 420 0 420{\p0}', 9)
ev(0.0, 0.62, 'Label', r'{\an5\pos(540,500)\fs50\bord0\fad(0,120)}소울체인지 8화', 10)
ev(0.0, 0.62, 'Label', r'{\an5\pos(540,610)\fs62\1c&HFFFFFF&\3c&H2020D0&\4c&H2020D0&\bord12\fad(0,120)}상담 보고서를 써야 한다', 10)
ev(0.0, 0.62, 'Emph', r'{\an5\pos(540,750)\fs88\bord6\3c&H000000&\fad(0,120)}엄마도 모르는 걸, 애들은 알았다', 10)
scene(0.62, cs('K2v'), '교무실 · 담임 몸에 지우 영혼')
say('A01', r'김 선생, 어제 상담 보고서.\N오늘 안에 내요. 조용히.', '교감')
say('NEP', '넵!', '지우 영혼', PINK, hold=0.3)
narr(TUCK[0], TUCK[1], r'(몸은 아저씨,\N손끝은 여고생)', 40, 430)
say('KN', '...큰일 날 뻔.', '(속마음) 지우 영혼', PINK, 'Mono')
scene(cs('K3a'), cs('K3a') + 2.0, '같은 시각 · 교실 · 지우 몸에 담임 영혼')
scene(cs('K4a'), cs('K4a') + 2.0, '다음 날 · 교무실')
say('S1a', '아, 밀지 마... 쌤, 이거요.', '옆 반 학생')
say('S1b', r'...최 쌤한테, 텀블러로 놀린 거...\N죄송하다고요.', '옆 반 학생')
say('NEO', '...너희가, 이걸 다 알아?', '지우 영혼', PINK)
say('S1c', '다 알죠. 맨날 같이 있는데.', '옆 반 학생')
say('LEAK', '꺄, 나도 딸기우유!', '지우 영혼', PINK, hold=0.1)
say('S1d', '...방금, 쌤 목소리 왜 저래?', '옆 반 학생')
say('BYS', '...벼, 변성기다.', '지우 영혼', PINK)
narr(end_('BYS') + 0.1, ce('K4b'), r'(쉰 살의 변성기)', 600, 430)
scene(cs('K7'), cs('K7') + 2.2, '최 쌤 자리 · 병가 중')
say('EM', '엄마도 모르는 걸, 애들은 알았네.', '(속마음) 지우 영혼', PINK, 'Mono')
say('VPW', r'거, 벽에 종이 붙이지 맙시다.\N이사장님 오시는데.', '교감')
say('NA', '넵! ...안 뗄 거지만.', '지우 영혼', PINK)
scene(cs('K8'), cs('K8') + 2.0, '점심시간 · 운동장 벤치')
narr(cs('K8') + 0.3, L['JAK'] - 0.1, r'(텀블러 건 학생)', 600, 700)
say('JAK', '...작년엔, 내가 틀어 줬는데.', '(속마음) 담임 영혼', SKY, 'Mono')
scene(cs('K10'), cs('K10') + 1.8, '쉬는 시간 · 반 단톡방')
say('OLD1', r'키읔, 키읔, 키읔... 다들...\N영크크하게... 방가방가... 물결...', '담임 영혼', SKY)
say('OLD2', r'...웃는 눈인데.\N...이거밖에 못 하나, 나.', '담임 영혼', SKY)
say('OLD3', r'아악, 사건이 끊이질 않네...\N하은이네 일본 갔다 오면, 이제 또 어떻게 하냐.', '담임 영혼', SKY)
scene(cs('RP'), ce('K11a'), '교감 자리')
say('YGY', '여기요오.', '지우 영혼', PINK)
say('VPH', '하... 왜 자꾸 이런 일이...', '교감')
say('CHOI', r'교감 선생님, 아직 아이 이야기는\N하나도 안 들었잖아요.', '최 선생님 (지금 담임)', end=L['CHOI'] + D['CHOI'] * 0.62)
say('CHOI', '조금만 시간을 주시겠어요?', '최 선생님 (지금 담임)', start=L['CHOI'] + D['CHOI'] * 0.62 + 0.03, grp='CHOI2')
narr(DOOR + 0.3, L['CHOI'] - 0.05, r'(병가 중이던\N최 선생님)', 40, 430)
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
(B / 'ep8.ass').write_text(head + '\n' + '\n'.join(EV) + '\n', encoding='utf-8')

# ---------- 6. 합치기 ----------
en_j = '+'.join(f"between(t,{c['start']},{c['start'] + c['dur'] - 0.001:.3f})" for c in CUTS if c['pip'] == 'pip')
en_t = '+'.join(f"between(t,{c['start']},{c['start'] + c['dur'] - 0.001:.3f})" for c in CUTS if c['pip'] == 'pip_t')
vf = (f"[1:v]scale=300:300[pj];[2:v]scale=300:300[pt];[3:v]setpts=PTS-STARTPTS+{GLITCH[0]:.3f}/TB[gl];"
      f"[0:v][pj]overlay=x=750:y=130:enable='{en_j}'[a];[a][pt]overlay=x=750:y=130:enable='{en_t}'[b];"
      f"[b][gl]overlay=x=750:y=130:eof_action=pass:enable='between(t,{GLITCH[0]:.3f},{GLITCH[1]:.3f})'[c];"
      f"[c]ass={B / 'ep8.ass'}:fontsdir={KIT / 'fonts'},format=yuv420p[vout]")
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', B / 'joined.mp4', '-i', KIT / 'pip.png', '-i', KIT / 'pip_t.png',
     '-framerate', FPS, '-i', GDIR / 'g_%02d.png',
     '-filter_complex', vf, '-map', '[vout]', '-t', MAIN, '-r', FPS, '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', B / 'main_v.mp4'])
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', ENDING, '-an', '-vf', f'fps={FPS},format=yuv420p,setsar=1',
     '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', B / 'ending_v.mp4'])
(B / 'vlist.txt').write_text(f"file '{B / 'main_v.mp4'}'\nfile '{B / 'ending_v.mp4'}'\n")
out = HERE / f'ep8_{TAG_}.mp4'
run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', B / 'vlist.txt', '-i', B / 'mix.wav',
     '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-t', TOT, '-movflags', '+faststart', out])
json.dump({'main': MAIN, 'ending': END_LEN, 'total': TOT, 'loudness_LUFS': I2, 'true_peak_dBTP': TP2,
           'cuts': [{kk: (str(vv) if isinstance(vv, pathlib.Path) else vv) for kk, vv in c.items()} for c in CUTS],
           'lines': {lid: {'start': L[lid], 'end': round(end_(lid), 3), 'file': SPEC[lid]['f'], 'range': SPEC[lid]['r'], 'inner': lid in INNER} for lid in sorted(L, key=L.get)},
           'subs': SUBS, 'glitch': GLITCH, 'bgm': BGM_SECT}, open(HERE / f'timeline_{TAG_}.json', 'w'), ensure_ascii=False, indent=1)
print('OK', out, TOT)
