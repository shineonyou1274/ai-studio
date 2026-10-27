#!/usr/bin/env python3
"""소울체인지 6화 「텀블러에 침을」 편집 v1 (5화 v8 방식 그대로, 크레딧 0).

기준: 대본_v4.md 3절 컷 표 + 5-2절 연출표 + 4절 녹음 + 9절 결정, feedback.md, AGENTS.md "편집으로 살리는 방법".
- 본편 ≤ 64.3초 + 고정 엔딩 5.7초(make_ending.py 6 화 — 7화는 11/3 화(사장님 정정 2026-10-27: 6화 11/1 일 공개)) ≤ 70.0초.
- 겉말 = 몸 목소리, 속마음 = 영혼 목소리 + aecho=0.85:0.6:45:0.12, 빙의 풀림 "헐—" = sc_student_body + 같은 잔향 + 영혼 원 지지직(코드).
- 자막: 키트 헤더 + 우리 스타일(DlgB/MonoB 80% 상자, 화자 Tag 색 상자), 쇼츠 아래 27%·위 6% 밖.
- 입이 안 맞는 곳은 교차 편집(H2 ↔ K07 옆자리 선생님 뒷모습), 녹음이 길면 배속.
- 배경음 = bgm.py(코드 합성), 웃음 박자에서 뚝 끊음. 그 학생·최 선생님 쪽에는 웃음 효과음 없음.
사용: python3 build_ep6_v4.py → ep6_v4.mp4, timeline_v4.json

v4(Gemini v3 검수): DM 상대 이름·입력창·폰 위 자막, 쪽지(○ 직접 그림, 수첩 종이 질감), 벤치 학생 머리 윤곽(bench_hood.py),
"헐—" 지지직 소리 + 분홍 번쩍 자막, "아… 아, 걔" 1.15배 +2dB, 회상 자막 "…놀리던 학생들".

v2(2026-10-27 사장님 "내용 전달이 거의 안 돼"): 첫 장면 = 5화 실제 교감 얼굴(H1 안 씀)+이름표, 아부는 담임 몸 얼굴(K08),
최 선생님 울음 먼저 보이고 상황 자막, 해설 자막 5개, "회상 · 작년", DM 받는 사람 표시, 마지막은 대각선 분할(창가 지우 몸 ↔ 벤치).
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
PC = KIT / 'episodes/ep6/clips'
B = HERE / 'build_v4'; B.mkdir(exist_ok=True)
E5 = EP.parent / 'soulchange-ep05' / '04_생성물' / 'clips'
P5 = KIT / 'episodes/ep5/clips'
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


# ---------- 1. 대사 조각 (생성로그 ★ 채택 테이크) ----------
T, G = 1.05, 0.13
SPEC = {
    'E01': dict(f='E6-01_jiu_inner_student_raw.mp3', r=[(0.10, 1.50)]),
    'E02': dict(f='E6-02_jiu_teacherbody_raw.mp3', r=[(0, 3.40)], tempo=1.15),        # 교감 입이 움직이기 전에 끝나게
    'E03': dict(f='E6-03_vp_arthur_raw.mp3', r=[(0, 1.80)], gap=0.20),
    'E04': dict(f='E6-04_vp_arthur_raw.mp3', r=[(0, 2.10)], gap=0.20),                # 2.53–4.18 받아쓰기 안 되는 소리는 뺌
    'E05a': dict(f='E6-05_t1_helena_raw.mp3', r=[(0.10, 0.92)]),                      # "들었어요?"
    'E05b': dict(f='E6-05_t1_helena_raw.mp3', r=[(1.25, 3.75)]),                      # "텀블러에, 누가 침을 뱉었대요."
    'E06': dict(f='E6-06_t1_helena_raw.mp3', r=[(0.15, 2.70)], gap=0.25),
    'E07': dict(f='E6-07_s1_dylan_raw.mp3', r=[(0, 3.40)]),
    'E08': dict(f='E6-08d_jiu_leak_student_raw.mp3', r=[(0, 0.60)], tempo=1.0),       # ★d "헐"
    'E09a': dict(f='E6-09_jiu_teacherbody_raw.mp3', r=[(0.10, 2.80)], gap=0.18),      # "헐.. 헐레벌떡.. 놀랐습니다"
    'E09b': dict(f='E6-09_jiu_teacherbody_raw.mp3', r=[(3.35, 5.10)]),                # "진짜 그런 애가 있다고요?"
    'E10': dict(f='E6-10_t1_helena_raw.mp3', r=[(0, 3.50)], gap=0.22),
    'E11': dict(f='E6-11_jiu_teacherbody_raw.mp3', r=[(0, 2.75)], gap=0.18, tempo=1.15),   # v4: 크게 벌린 입에 맞게 빠르게(+2dB는 GAIN)
    'E12': dict(f='E6-12_jiu_inner_student_raw.mp3', r=[(0.05, 2.40)], gap=0.22),
    'E13': dict(f='E6-13_jiu_dm_student_raw.mp3', r=[(0, 3.45)], gap=0.20),
    'E14a': dict(f='E6-14_friend_pixie_raw.mp3', r=[(1.12, 2.98)]),                   # 앞 웃음(0–1.1) 뺌
    'E14b': dict(f='E6-14_friend_pixie_raw.mp3', r=[(3.38, 5.90)]),
    'E15': dict(f='E6-15_teacher_studentbody_raw.mp3', r=[(0.10, 2.36)]),
    'E16': dict(f='E6-16_teacher_inner_teacher_raw.mp3', r=[(0.05, 2.05)], gap=0.18),
    'E17': dict(f='E6-17_teacher_studentbody_raw.mp3', r=[(0, 0.70), (2.94, 4.92)], gap=0.25),   # 헛기침 셋 → 하나 + "경치가… 좋구나."
}
for s in SPEC.values():
    s.setdefault('tempo', T); s.setdefault('gap', G)
D = prep(SPEC, V, VO)
INNER = {'E01', 'E08', 'E12', 'E16'}   # 잔향: 속마음 3줄 + 빙의 풀림 "헐—"

# ---------- 2. 컷과 대사 배치 ----------
L, CUTS = {}, []
t = 0.0
def cut(cid, src, ss, se, pip, dur, zoom=(1.0, 0.5, 0.5), note='', fx=None, stretch=None, still=None, push=0.12):
    global t
    CUTS.append(dict(id=cid, src=src, ss=ss, se=se, pip=pip, start=round(t, 3), dur=round(dur, 3), zoom=zoom, note=note, fx=fx, st=stretch, still=still, push=push))
    t += dur
def at(lid, x):
    L[lid] = round(x, 3); return x + D[lid]

# K1 v2: H1 교감이 5화 교감과 다르게 생겨 담임처럼 보임(사장님) → H1 안 씀.
#  K1a 5화 교감 클로즈업(A5a 안경 올리며 노려봄) + 지난 화 한 줄 + 이름표 "교감" + 속마음 "…또 그 눈빛."
#  K1b 담임 몸 얼굴(K08 웃으며 말함) — 아부 "교장 포스세요!"  /  K1c 5화 교감(A2, 말하는 입) "흠흠… 그래요?"
c0 = t
e = at('E01', c0 + 0.90)
cut('K1a', E5 / 'A5a_K12a_교감끝훅.mp4', 0.7, 2.4, 'pip', 1.7 * 1.15, note='5화 교감 클로즈업(안경 올리며 노려봄) — 지난 화 + "…또 그 눈빛."', stretch=1.15)
c0 = t; e = at('E02', c0 + 0.12)
cut('K1b', PC / 'K08.mp4', 0.8, None, 'pip', e + 0.10 - c0, note='담임 몸(지우 영혼) 웃으며 말함 — 아부', stretch=1.15)
K8_USED = 0.8 + CUTS[-1]['dur'] / 1.15
c0 = t; e = at('E03', c0 + 0.12)
cut('K1c', E5 / 'A2_K7_교감어느집딸.mp4', 0.2, None, 'pip', e + 0.15 - c0, zoom=(1.1, 1.0, 1.0), note='5화 교감(말하는 입, AI 배지 잘라 냄) — "흠흠… 그래요?"')
CHIME = L['E03'] + 0.05
# K2: 최 선생님 뒷모습, 블라인드. 흐느낌(작게) → 교감 화면 밖 "문, 문부터 닫읍시다!" → 문 탁 → "들었어요?"
c0 = t; SOB = c0 + 0.05
e = at('E04', c0 + 1.20)   # v2: 우는 최 선생님을 먼저 1.2초 보여 주고
DOOR = c0 + (3.4 - 1.2) * 1.15
e = at('E05a', max(e + 0.25, DOOR + 0.25))
cut('K2', PC / 'K02.mp4', 1.2, None, 'pip', e + 0.12 - c0, stretch=1.15, note='최 선생님 뒷모습(얼굴 0), 교감 팔이 문을 닫음. 향수병은 왼쪽 아래 1.2–2.0초만')
c0 = t; e = at('E05b', c0 + 0.12); DUNG1 = e + 0.05
cut('K3', PC / 'K03.mp4', 0, None, 'pip', e + 0.40 - c0, note='인서트: 텀블러 역광 돌리 인(침 뱉는 장면 없음)')
# K4: 손이 쪽지를 펴 듦(원본 2.2–4.0) → K4b 코드 쪽지 인서트(손글씨 합성, 형광등 깜빡임)
c0 = t; RUSTLE = c0 + 0.15
e = at('E06', c0 + 0.20)
cut('K4', PC / 'K04.mp4', 2.2, 4.0, 'pip', 1.8, note='인서트: 손·베이지 소매가 쪽지를 펴 듦')
cut('K4b', None, 0, None, 'pip', e + 0.30 - t, fx='note', note='코드 인서트: 쪽지 손글씨 "최○○ 티○년 / 냄새 싫어. 없어져." 천천히 다가감 + 형광등 깜빡')
c0 = t; e = at('E07', c0 + 0.15)
cut('K5', PC / 'K05.mp4', 0, None, 'pip', e + 0.30 - c0, fx='flash', note='회상: 채도 낮춤·가장자리 어둡게. 남학생 컵 시늉 → 최 선생님 손이 출석부 꽉')
# K6a = H2 0–1.2(놀라 입 벌림 → 두 손으로 입 막음) + "헐—" 빙의 풀림 + 영혼 원 지지직
h2s = 1.15; c0 = t
e = at('E08', c0 + 0.06); GLITCH = (L['E08'], L['E08'] + 0.45)
cut('K6a', C / 'H2_K6.mp4', 0, 1.2, 'pip', 1.2 * h2s, note='두 손으로 입 막음 — "헐—"(여고생 목소리 + 잔향) + 영혼 원 지지직')
cut('K7a', PC / 'K07.mp4', 0, 1.4, 'pip', 1.4, note='옆자리 선생님이 고개를 반쯤 돌렸다 돌아감(얼굴 옆선만) — 정적')
# K6b: "…헐, 헐" = H2 손 내림(2.0–2.9) → "…레벌떡… 놀랐습니다" = 옆자리 선생님 뒷모습(듣는 사람) → "진짜 그런 애가 있다고요?" = H2 말하는 입(4.4~)
c0 = t; e = at('E09a', c0 + 0.06)
cut('K6b', C / 'H2_K6.mp4', 2.0, 2.87, 'pip', 0.87 * h2s, note='손을 내림(입 안 맞는 구간을 짧게)')
cut('K7x', PC / 'K07.mp4', 2.0, None, 'pip', e + 0.10 - t, note='듣는 옆자리 선생님 뒷모습 — "…레벌떡… 놀랐습니다" 화면 밖')
c0 = t; e = at('E09b', c0 + 0.12)
cut('K6c', C / 'H2_K6.mp4', 4.4, 6.04, 'pip', e + 0.10 - c0, note='담임 몸 말하는 입 — "진짜 그런 애가 있다고요?"')
c0 = t; e = at('E10', c0 + 0.15)
cut('K7b', PC / 'K07.mp4', 4.5, None, 'pip', e + 0.30 - c0, note='옆자리 선생님 뒷모습(얼굴 안 보임) — "알잖아요, 작년에 선생님 반이었던…" 뒤 정적 0.3')
# K8 v2: K08 앞부분은 K1b 아부에 썼으므로 "아… 아, 걔. 네, 네."는 5화 A3(담임 몸 말하는 입) → 속마음은 K08 뒤(웃음 빠지고 폰, 입 다묾)
c0 = t; e = at('E11', c0 + 0.05)
cut('K8', E5 / 'A3_K9_기간제였어요.mp4', 2.0, None, 'pip', e + 0.10 - c0, zoom=(1.15, 0.5, 0.2), note='5화 A3 담임 몸 말하는 입(1.15배) — 아는 척', stretch=1.13)
c0 = t; e = at('E12', c0 + 0.15)
cut('K8b', PC / 'K08.mp4', max(3.2, K8_USED), 5.04, 'pip', (5.04 - max(3.2, K8_USED)) * 1.15, note='웃음 빠지고 눈 굴리며 폰 꺼냄(입 다묾) — 속마음', stretch=1.15)
# K9: 코드 폰 화면(담임 폰에서 지우가 보내는 DM). 속마음 끝이 걸쳐 넘어옴
c0 = t
e = at('E13', max(L['E12'] + D['E12'] + 0.45, c0 + 0.35))   # v4: 폰이 다 올라온 뒤 첫 말풍선
_w = [w for w in [('대박', 0.56), ('작년', 1.82)]]
BUB = [L['E13'], L['E13'] + 1.70 / SPEC['E13']['tempo']]
cut('K9', None, 0, None, 'pip', e + 0.45 - c0, fx='dm', note='코드 인서트: 담임 폰, 여고생 말투 DM 입력 → 말풍선 두 개 → 읽음')
# K10 = H3(지우 몸): 폰 실눈·없는 안경(0–3) → 찡그리며 투덜(입 움직임 3.0~). 치마가 보이는 아래쪽은 1.25배 위 기준으로 잘라 냄
k10s = 1.13; c0 = t; BUZZ = c0 + 0.05
e = at('E14a', c0 + 0.90)
e = at('E15', max(e + 0.25, c0 + 3.0 * k10s))
cut('K10', C / 'H3_K10.mp4', 0, None, 'pip_t', e + 0.25 - c0, zoom=(1.25, 0.5, 0.0), note='지우 몸 폰 실눈·없는 안경 → "…요즘 폰 글씨가 작아." 치마 안 보이게 1.25배', stretch=k10s)
# K11 v2 사장님: 창밖 보는 쪽과 벤치가 같은 방향이라 안 이어짐 → 대각선 분할. 아래 왼쪽 = 창가 지우 몸(담임 영혼), 위 오른쪽 = 벤치 먼 뒷모습.
#  속마음·친구 놀림 동안 = 5화 C2(지우 몸, 위를 올려다봄, 입 다묾) / "에헴. 경치가 좋구나." = 5화 C1(없는 안경 미간 밀기 + 말하는 입, 중년 몸짓)
c0 = t
e = at('E16', c0 + 0.40); DUNG2 = e + 0.05
e = at('E14b', e + 0.90)
SPLIT_SW = e + 0.15                                       # 얼굴 컷을 C2 → C1으로 바꾸는 시각
e = at('E17', e + 0.25)
cut('K11', None, 0, None, 'pip_t', e + 0.50 - c0, fx='split', note='대각선 분할: 아래 왼쪽 지우 몸(5화 C2 → C1), 위 오른쪽 벤치 먼 뒷모습(K11 1.6배). 그 학생 쪽 웃음 장치 없음')
DING = e + 0.15
MAIN = round(t, 3); TOT = round(MAIN + END_LEN, 3)
print('본편', MAIN, '합계', TOT)
for c in CUTS:
    if c['src'] is None: c['stretch'] = 1.0; c['se'] = c['ss']; print(f"  {c['id']:5s} {c['start']:6.2f} +{c['dur']:.2f}  코드"); continue
    if c['st']: c['stretch'] = c['st']; c['se'] = round(c['ss'] + c['dur'] / c['st'], 3)
    else:
        if c['se'] is None: c['se'] = round(c['ss'] + c['dur'], 3)
        c['stretch'] = round(c['dur'] / (c['se'] - c['ss']), 3)
    print(f"  {c['id']:5s} {c['start']:6.2f} +{c['dur']:.2f}  src {c['ss']}-{c['se']} x{c['stretch']}")
    assert c['stretch'] <= 1.151, c
assert MAIN <= MAIN_MAX + 1e-6, f'본편 {MAIN} > {MAIN_MAX}'

# ---------- 3. 영상 조각 ----------
def note_frames(n):
    """v4 쪽지 인서트: K04 손에 든 것과 같은 수첩 종이(위쪽 스프링 구멍이 찢긴 가장자리, 연한 파란 줄),
    종이 결·구김 음영·그림자·기울기·필름 입자. 욕의 ○는 Jua에 없어 원을 직접 그림."""
    rnd = np.random.default_rng(6)
    pw, ph = 860, 1080
    base = np.full((ph, pw, 3), (238, 236, 228), float)
    base += rnd.normal(0, 3.0, (ph, pw, 1))                                  # 종이 결
    yy, xx = np.mgrid[0:ph, 0:pw]
    for k in range(5):                                                        # 구김 음영(접힌 자국)
        a_, b_, c_ = rnd.normal(size=3); d_ = (a_ * xx + b_ * yy - c_ * 300 - rnd.uniform(200, 700)) / math.hypot(a_, b_)
        base += (np.exp(-(d_ / 18) ** 2) * -14 + np.exp(-((d_ - 22) / 30) ** 2) * 6)[..., None]
    base[int(ph * 0.48):int(ph * 0.48) + 3] -= 18                              # 가로로 한 번 접은 자국
    paper = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(paper)
    for y in range(150, ph - 40, 72): d.line([(30, y), (pw - 30, y)], fill=(165, 188, 222), width=2)
    pen = (48, 50, 66)
    def text_o(x, y, parts, size):                                            # 글자 사이 ○는 원으로
        for p_ in parts:
            if p_ == '○':
                r_ = size * 0.36; cy = y + size * 0.55
                d.ellipse([x + 4, cy - r_, x + 4 + 2 * r_, cy + r_], outline=pen, width=6); x += 2 * r_ + 14
            else:
                d.text((x, y), p_, font=f(size), fill=pen); x += d.textlength(p_, font=f(size))
    text_o(90, 250, ['최', '○', '○', ' 티', '○', '년'], 112)
    d.text((90, 470), '냄새 싫어.', font=f(100), fill=pen)
    d.text((90, 620), '없어져.', font=f(100), fill=pen)
    # 위쪽 스프링 구멍 찢긴 가장자리(투명으로 오려 냄)
    mask = Image.new('L', (pw, ph), 255); md = ImageDraw.Draw(mask)
    edge = [(0, 0)]
    for x in range(0, pw + 1, 8): edge.append((x, 18 + int(rnd.normal(0, 3))))
    edge += [(pw, 0)]; md.polygon(edge, fill=0)
    for x in range(40, pw - 20, 52): md.ellipse([x, 22, x + 22, 44], fill=0)
    paper = paper.convert('RGBA'); paper.putalpha(mask)
    paper = paper.rotate(-5, expand=True, resample=Image.BICUBIC)
    bg = Image.new('RGB', (W, H), (46, 54, 62))
    gb = np.asarray(bg, float) + rnd.normal(0, 4, (H, W, 1)); bg = Image.fromarray(np.clip(gb, 0, 255).astype(np.uint8))
    px, py = (W - paper.width) // 2, 230
    sh = Image.new('RGBA', paper.size, (0, 0, 0, 0)); sh.putalpha(paper.split()[3].point(lambda v: v * 150 // 255))
    bg.paste(Image.new('RGB', paper.size, (0, 0, 0)), (px + 26, py + 34), sh.split()[3].filter(ImageFilter.GaussianBlur(18)))   # 그림자
    bg.paste(paper, (px, py), paper)
    bg = bg.filter(ImageFilter.GaussianBlur(0.9))
    fr = []
    for i in range(n):
        z = 1.0 + 0.10 * i / max(1, n - 1)
        w, h = W / z, H / z
        im = bg.transform((W, H), Image.EXTENT, ((W - w) / 2, (H - h) * 0.40, (W + w) / 2, (H - h) * 0.40 + h), Image.BICUBIC)
        a = np.asarray(im, float) + rnd.normal(0, 6, (H, W, 1))              # 필름 입자
        if i in (3, 4, 11): a *= 0.72                                         # 형광등 깜빡
        fr.append(np.clip(a, 0, 255).astype(np.uint8))
    return fr


def dm_frames(n, start, bub, src_bg, rise_at=0.0):
    """K9 폰 화면: 담임 폰(지우 영혼이 씀) → '지우'에게 여고생 말투 DM. 말풍선은 녹음 시간에 맞춰 톡 튀어나옴.
    폰이 아래에서 올라오고(0.35초) 손에 든 것처럼 조금씩 흔들림 — 멈춘 화면처럼 보이지 않게."""
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-sseof', '-0.1', '-i', str(src_bg), '-frames:v', '1', '-vf', 'scale=1080:1920', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                         capture_output=True).stdout
    bg = Image.frombytes('RGB', (W, H), raw[:W * H * 3]).filter(ImageFilter.GaussianBlur(14))
    bg = Image.fromarray((np.asarray(bg, float) * 0.55).astype(np.uint8))
    pw, ph = 660, 1180
    msgs = ['쌤!!! 대박 사건ㅠㅠ', '작년 쌤 반 애래요;;']
    fr = []
    for i in range(n):
        tt = start + i / FPS; lt = i / FPS
        rise = min(1.0, max(0.0, lt - rise_at) / 0.35); rise = rise * rise * (3 - 2 * rise)   # v4: 앞 속마음 자막이 끝난 뒤 올라옴
        x0 = (W - pw) // 2 + int(8 * math.sin(2 * math.pi * 0.7 * lt))
        y0 = 470 + int((1 - rise) * 1300) + int(6 * math.sin(2 * math.pi * 1.1 * lt))
        im = bg.copy(); d = ImageDraw.Draw(im)
        d.rounded_rectangle([x0, y0, x0 + pw, y0 + ph], 70, fill=(22, 22, 26))
        sx0, sy0, sx1, sy1 = x0 + 22, y0 + 22, x0 + pw - 22, y0 + ph - 22
        d.rounded_rectangle([sx0, sy0, sx1, sy1], 52, fill=(236, 238, 244))
        d.rectangle([sx0, sy0 + 40, sx1, sy0 + 150], fill=(222, 225, 234))
        d.text((sx0 + 36, sy0 + 95), '<  지우 폰 (지금은 쌤)', font=f(44), fill=(30, 30, 30), anchor='lm')   # v4: 받는 쪽 = 지우 폰, 안에 담임
        y = sy0 + 220
        for k in range(len(msgs)):
            if tt < bub[k]: continue
            sc = min(1.0, 0.6 + (tt - bub[k]) / 0.12 * 0.4)
            fs = int(56 * sc); tw = d.textlength(msgs[k], font=f(fs))
            d.rounded_rectangle([sx1 - 36 - tw - 50, y, sx1 - 36, y + int(108 * sc)], 34, fill=(255, 140, 190))
            d.text((sx1 - 36 - 25, y + int(54 * sc)), msgs[k], font=f(fs), fill=(255, 255, 255), anchor='rm')
            y += 136
        if tt >= bub[-1] + 1.2:
            d.text((sx1 - 36, y - 6), '읽음', font=f(34), fill=(120, 120, 130), anchor='ra')
        d.rounded_rectangle([sx0 + 24, sy1 - 130, sx1 - 24, sy1 - 40], 40, fill=(255, 255, 255))
        if tt < bub[-1]:
            d.text((sx0 + 60, sy1 - 85), '입력 중' + '.' * (1 + int(tt * 6) % 3), font=f(40), fill=(150, 150, 160), anchor='lm')   # v4: Jua에 • 없음(□로 깨짐)
        else:
            d.text((sx0 + 60, sy1 - 85), '메시지 입력', font=f(40), fill=(175, 175, 185), anchor='lm')
        z = 1.0 + 0.08 * i / max(1, n - 1); w, h = W / z, H / z
        im = im.transform((W, H), Image.EXTENT, ((W - w) / 2, (H - h) / 2, (W + w) / 2, (H - h) / 2 + h), Image.BICUBIC)
        fr.append(np.asarray(im, np.uint8))
    return fr


def write_frames(fr, out):
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p', str(out)], input=np.stack(fr).tobytes(), check=True)


seg_list = []
run(['python3', HERE / 'bench_hood.py', PC / 'K11.mp4', B / 'K11_hood.mp4'])   # v4: 벤치 학생 숙인 머리 윤곽
for c in CUTS:
    out = B / f"seg_{c['id']}.mp4"; nfr = round(c['dur'] * FPS)
    if c['fx'] == 'note':
        write_frames(note_frames(nfr), out); seg_list.append(out); continue
    if c['fx'] == 'dm':
        write_frames(dm_frames(nfr, c['start'], BUB, B / 'seg_K8b.mp4', rise_at=max(0.0, L['E12'] + D['E12'] + 0.08 - c['start'])), out); seg_list.append(out); continue
    if c['fx'] == 'split':   # v2: 대각선 분할(선 (0,300)–(1080,1500)), 아래 왼쪽 = 얼굴, 위 오른쪽 = 벤치
        dA1 = round(SPLIT_SW - c['start'], 3); dA2 = round(c['dur'] - dA1, 3)
        mk = Image.new('L', (W, H), 0); ImageDraw.Draw(mk).polygon([(0, 300), (W, 1500), (W, H), (0, H)], fill=255)
        mk.save(B / 'split_mask.png')
        ln = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(ln)
        ld.line([(0, 300), (W, 1500)], fill=(20, 20, 30, 255), width=22); ld.line([(0, 300), (W, 1500)], fill=(255, 255, 255, 255), width=12)
        ln.save(B / 'split_line.png')
        # 얼굴: C2(얼굴 (534,690) → 1.6배 → (330,900)) / C1(얼굴 (540,990) → 1.25배 → (330,1000)). 둘 다 좌우 뒤집어 시선이 위 오른쪽 벤치 쪽을 향하게
        fa = (f"[0:v]trim=start=0.3:duration={dA1 / 1.0:.3f},setpts=PTS-STARTPTS,fps={FPS},scale=1728:3072,crop=1080:1920:104:204,hflip,setsar=1[a1];"
              f"[1:v]trim=start=3.0:duration={min(2.0, dA2):.3f},setpts=PTS-STARTPTS,fps={FPS},scale=1512:2688,crop=1080:1920:6:386,hflip,setsar=1,"
              f"tpad=stop_mode=clone:stop_duration=3[a2];[a1][a2]concat=n=2:v=1:a=0,trim=duration={c['dur']:.3f}[fa];"
              f"[2:v]trim=start=1.0:duration={c['dur']:.3f},setpts=PTS-STARTPTS,fps={FPS},scale=1728:3072[bb];"
              f"color=c=0x2a2620:s={W}x{H}:r={FPS}:d={c['dur']:.3f}[bk];[bk][bb]overlay=x=-248:y=80[bn];"
              f"[3:v]format=gray,scale={W}:{H}[mk];[fa][mk]alphamerge[fm];[bn][fm]overlay=0:0[cm];[cm][4:v]overlay=0:0,format=yuv420p[v]")
        run(['ffmpeg', '-y', '-loglevel', 'error', '-i', P5 / 'K04_C2.mp4', '-i', E5 / 'C1_K3.mp4', '-i', B / 'K11_hood.mp4',
             '-loop', '1', '-i', B / 'split_mask.png', '-loop', '1', '-i', B / 'split_line.png',
             '-filter_complex', fa, '-map', '[v]', '-frames:v', nfr, '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', out])
        seg_list.append(out); continue
    z, ax, ay = c['zoom']; used = c['se'] - c['ss']
    vf = (f"[0:v]trim=start={c['ss']}:duration={used:.3f},setpts=(PTS-STARTPTS)*{c['stretch']},fps={FPS},"
          f"scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,")
    if z != 1.0:
        sw, sh = int(round(1080 * z / 2) * 2), int(round(1920 * z / 2) * 2)
        vf += f"scale={sw}:{sh}:flags=lanczos,crop=1080:1920:{int((sw - 1080) * ax)}:{int((sh - 1920) * ay)},"
    if c['fx'] == 'flash':   # 회상: 채도 낮춤 + 뿌옇게 + 가장자리 어둡게
        vf += "eq=saturation=0.45:brightness=0.03:contrast=0.92,gblur=sigma=1.2,vignette=PI/4.5,"
    vf += "setsar=1,format=yuv420p,tpad=stop_mode=clone:stop_duration=0.5[v]"
    run(['ffmpeg', '-y', '-loglevel', 'error', '-i', c['src'], '-filter_complex', vf, '-map', '[v]',
         '-frames:v', nfr, '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', out])
    seg_list.append(out)
(B / 'list.txt').write_text(''.join(f"file '{p}'\n" for p in seg_list))
run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', B / 'list.txt', '-c', 'copy', B / 'joined.mp4'])

# 영혼 원 지지직(빙의 풀림 1단계, 약하게): 가로 조각 밀림 + 색 갈라짐 + 주사선 + 테두리 흐려짐
pip = Image.open(KIT / 'pip.png').convert('RGBA').resize((300, 300), Image.LANCZOS)
GDIR = B / 'glitch'; GDIR.mkdir(exist_ok=True)
gn = round((GLITCH[1] - GLITCH[0]) * FPS)
for i in range(gn):
    rnd = random.Random(i * 7 + 3); a = np.asarray(pip).copy()
    for _ in range(5):
        y0 = rnd.randint(0, 280); hgt = rnd.randint(6, 26); dx = rnd.randint(-22, 22)
        a[y0:y0 + hgt] = np.roll(a[y0:y0 + hgt], dx, axis=1)
    a[..., 0] = np.roll(a[..., 0], 4, axis=1); a[..., 2] = np.roll(a[..., 2], -4, axis=1)
    a[::4, :, :3] = (a[::4, :, :3] * 0.6).astype(np.uint8)
    rgb = a[..., :3].astype(float); g_ = rgb.mean(axis=2, keepdims=True)
    a[..., :3] = (rgb * 0.6 + g_ * 0.4).astype(np.uint8)
    Image.fromarray(a).save(GDIR / f'g_{i:02d}.png')

# ---------- 4. 소리 ----------
HALL = 'aecho=0.85:0.6:45:0.12'
GAIN = {'E01': 2.0, 'E12': 1.0, 'E16': 1.0, 'E11': 2.0}   # 속삭임 속마음이 겉말보다 작게 녹음됨
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
CHIMEX = '0.18*sin(2*PI*1568*t)*exp(-6*t)+0.12*sin(2*PI*2349*t)*exp(-8*t)'
DUNGX = '0.35*sin(2*PI*(58+8*t)*t)*exp(-1.6*t)'
DOORX = '0.6*sin(2*PI*(120-60*t)*t)*exp(-22*t)+0.2*sin(2*PI*520*t)*exp(-50*t)'
BUZZX = '0.18*sin(2*PI*150*t)*(0.5+0.5*sin(2*PI*25*t))*lt(mod(t,0.5),0.35)'
SEND = '0.18*sin(2*PI*(700+1600*t)*t)*exp(-12*t)'
DINGX = '0.16*sin(2*PI*1320*t)*lt(t,0.08)+0.16*sin(2*PI*1760*t)*gt(t,0.12)*lt(t,0.24)'
sfx('chime', CHIMEX, 0.6, CHIME, 0.5)
# v4: 빙의 풀림 "헐—" — 지지직(짧게 끊기는 전기 잡음) 0.4초, 목소리보다 작게
fc.append(f"anoisesrc=d=0.42:c=white:a=0.5:r=48000,highpass=f=1800,volume='0.10*lt(mod(t,0.045),0.022)*(0.6+0.4*sin(2*PI*57*t))':eval=frame,"
          f"afade=t=out:st=0.3:d=0.12,aformat=channel_layouts=stereo,adelay={int(GLITCH[0] * 1000)}:all=1[zap]"); mixl.append('[zap]')
for k in range(3):   # 최 선생님 흐느낌: 눌린 숨소리(작게, 장난 효과 없음)
    fc.append(f"anoisesrc=d=0.45:c=pink:a=0.5:r=48000,bandpass=f=900:w=700,afade=t=in:d=0.08,afade=t=out:st=0.15:d=0.3,volume=0.10,"
              f"aformat=channel_layouts=stereo,adelay={int((SOB + 0.55 * k) * 1000)}:all=1[sob{k}]"); mixl.append(f'[sob{k}]')
sfx('door', DOORX, 0.4, DOOR, 0.8)
sfx('dung1', DUNGX, 1.2, DUNG1, 0.45)
noise('rustle', 0.6, RUSTLE, 'highpass=f=1500,afade=t=in:d=0.05,afade=t=out:st=0.3:d=0.3', 0.08)
for k in range(10):   # K9 입력음
    noise(f'ty{k}', 0.04, CUTS[[c['id'] for c in CUTS].index('K9')]['start'] + 0.10 + 0.13 * k, 'bandpass=f=2500:w=1500', 0.10)
for k, b_ in enumerate(BUB): sfx(f'send{k}', SEND, 0.35, b_, 0.6)
sfx('buzz', BUZZX, 0.9, BUZZ, 0.5)
sfx('dung2', DUNGX, 1.2, DUNG2, 0.40)
sfx('ding', DINGX, 0.3, DING, 0.5)
# 공간 소리
def amb(lbl, a, b, lo, hi, vol):
    a0 = max(0, a - 0.3)
    fc.append(f"anoisesrc=d={b - a0:.2f}:c=pink:a=0.5:r=48000,bandpass=f={(lo + hi) // 2}:w={hi - lo},volume={vol},"
              f"afade=t=in:d=0.3,afade=t=out:st={b - a0 - 0.3:.2f}:d=0.3,aformat=channel_layouts=stereo,adelay={int(a0 * 1000)}:all=1[{lbl}]")
    mixl.append(f'[{lbl}]')
OFFICE = {'K1a', 'K1b', 'K1c', 'K2', 'K6a', 'K7a', 'K6b', 'K7x', 'K6c', 'K7b', 'K8', 'K8b', 'K9'}
EMPTY = {'K3', 'K4', 'K4b'}
CLASS = {'K5', 'K10', 'K11'}
for c in CUTS:
    a, b = c['start'], c['start'] + c['dur']
    if c['id'] in OFFICE: amb(f"am_{c['id']}", a, b, 300, 2800, 0.018)
    elif c['id'] in EMPTY: amb(f"am_{c['id']}", a, b, 200, 900, 0.010)
    elif c['id'] == 'K11': amb(f"am_{c['id']}", a, b, 500, 2500, 0.010)   # 교실 소리 낮아짐
    else: amb(f"am_{c['id']}", a, b, 500, 2500, 0.022)
fc.append(f"anoisesrc=d={MAIN}:c=brown:a=0.5:r=48000,lowpass=f=350,volume=0.0105,afade=t=in:d=0.5,afade=t=out:st={MAIN - 0.4}:d=0.4,aformat=channel_layouts=stereo[room]"); mixl.append('[room]')
# 배경음: 아부 코미디(가벼운 펄스) → 사건(똑딱·드론) → "헐—"에서 뚝 → 아는 척·DM·노안(가벼운 펄스) → 훅(느린 단조 화음) → 친구 놀림 직전 뚝
k = {c['id']: c for c in CUTS}
BGM_SECT = [('class', k['K1b']['start'], k['K2']['start']),
            ('tense', k['K2']['start'] + 0.3, L['E08']),
            ('class', k['K8']['start'], k['K11']['start']),
            ('sad', k['K11']['start'], L['E14b'] - 0.05)]
BGM_I = bgm.make(BGM_SECT, [(VO / f'{lid}.wav', st) for lid, st in L.items()], MAIN, B / 'bgm.wav', target_lufs=-28.0, duck_db=-15.0)
ins += ['-i', B / 'bgm.wav']; mixl.append(f'[{len(ins) // 2 - 1}:a]')
fc.append(''.join(mixl) + f"amix=inputs={len(mixl)}:normalize=0,apad=whole_dur={MAIN},atrim=0:{MAIN}[aout]")
run(['ffmpeg', '-y', '-loglevel', 'error', *ins, '-filter_complex', ';'.join(fc), '-map', '[aout]', '-ar', '48000', B / 'mix_raw.wav'])

def meas(p):
    m = subprocess.run(['ffmpeg', '-i', str(p), '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', m)[-1]), float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', m)[-1])
I0, _ = meas(B / 'mix_raw.wav')
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', B / 'mix_raw.wav', '-af', f'volume={-14.0 - I0:.2f}dB,alimiter=limit=0.58:level=false:attack=2:release=60', '-ar', '48000', B / 'mix_main.wav'])
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', B / 'ending_ep6.mp4', '-vn', '-ar', '48000', '-ac', '2', B / 'ending.wav'])
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', B / 'mix_main.wav', '-i', B / 'ending.wav', '-filter_complex', '[0:a][1:a]concat=n=2:v=0:a=1[a]', '-map', '[a]', '-ar', '48000', B / 'mix_full_raw.wav'])
I1, _ = meas(B / 'mix_full_raw.wav')
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', B / 'mix_full_raw.wav', '-af', f'volume={-14.0 - I1:.2f}dB,alimiter=limit=0.58:level=false:attack=2:release=60', '-ar', '48000', B / 'mix.wav'])
I2, TP2 = meas(B / 'mix.wav'); print('loudness', I2, 'TP', TP2, 'bgm', BGM_I)

# ---------- 5. 자막 ----------
def ts(x):
    h_, m_ = int(x // 3600), int(x % 3600 // 60); s_ = x % 60
    return f"{h_}:{m_:02d}:{s_:05.2f}"
PINK, SKY = 'J', 'T'
TAGSTYLE = {('J', False): 'TagJ', ('T', False): 'TagT', ('', False): 'TagW', ('J', True): 'TagJi', ('T', True): 'TagTi'}
EV, PEND, SUBS = [], [], []
def ev(a, b, style, text, layer=1):
    EV.append(f"Dialogue: {layer},{ts(a)},{ts(b)},{style},,0,0,0,,{text}")
def say(lid, text, tag, col='', style='Dlg', hold=0.15, delay=0.0, end=None):
    a = L[lid] + delay; b = end if end else L[lid] + D[lid] + hold
    PEND.append(dict(a=a, b=b, text=text, tag=tag, col=col, style=style, grp=lid))
def emit(x):
    fad = r'\fad(60,100)'
    if x['grp'] == 'E08':   # v4: 빙의 풀림 자막 — 분홍 상자로 지지직 번쩍(설명 글자 없음)
        fad = r'\3a&H00&\3c&HB45FFF&\t(0,70,\3c&H000000&)\t(70,140,\3c&HB45FFF&)\t(140,210,\3c&H000000&)\t(210,280,\3c&HB45FFF&)\t(280,400,\3c&H000000&)'
    ev(x['a'], x['b'], x['style'] + 'B', r'{\an2\pos(540,1330)' + fad + '}' + x['text'], 2)
    ty = 1181 if r'\N' in x['text'] else 1243
    ev(x['a'], x['b'], TAGSTYLE[(x['col'], x['style'] == 'Mono')], rf"{{\an2\pos(540,{ty})\fad(60,100)}}{x['tag']}", 3)

ev(0.0, k['K1b']['start'] + k['K1b']['dur'], 'Label', r'{\an7\pos(40,140)}담임과 학생, 몸이 바뀌었다', 6)
ev(0.0, 1.9, 'Label', r'{\an8\pos(540,990)\fad(0,150)}지난 화 · 교감이 "몸 바뀌는 드라마"를 들먹이며\N담임 몸의 지우를 의심했다', 6)
ev(0.0, k['K1a']['dur'], 'TagW', r'{\an7\pos(60,640)\fad(0,120)}교감', 6)                 # 교감 얼굴 옆 이름표
ev(k['K1b']['start'], k['K1b']['start'] + 2.4, 'Scene', r'{\an7\pos(40,240)}교무실 · 담임 몸에 지우 영혼', 6)
ev(k['K1c']['start'], k['K1c']['start'] + k['K1c']['dur'], 'TagW', r'{\an7\pos(60,640)\fad(80,120)}교감', 6)
say('E01', '…또 그 눈빛.', '(속마음) 지우 영혼', PINK, 'Mono')
say('E02', r'교감 선생님,\N오늘 완전 교장 포스세요!', '지우 영혼', PINK)
say('E03', '흠흠… 그래요?', '교감')
ev(k['K2']['start'], k['K2']['start'] + k['K2']['dur'], 'Scene', r'{\an7\pos(40,240)}옆 반 최 선생님이 울고 있다', 6)
# 해설 자막(예능 자막, 대사만큼 크게, 화자 Tag 없음)
def narr(a, b, text, x=40, y=430):
    ev(a, b, 'Narr', rf'{{\an7\pos({x},{y})\frz5\fad(120,150)}}{text}', 8)
narr(L['E04'] + 0.5, k['K2']['start'] + k['K2']['dur'], r'(위로보다\N소문 단속이 먼저)')
ev(k['K3']['start'], k['K3']['start'] + k['K3']['dur'], 'Scene', r'{\an7\pos(40,240)}누군가 최 선생님 텀블러에…', 6)
ev(k['K4']['start'], k['K4b']['start'] + k['K4b']['dur'], 'Scene', r'{\an7\pos(40,240)}텀블러 옆에 떨어진 욕 쪽지', 6)
say('E04', '문, 문부터 닫읍시다!', '교감')
say('E05a', '들었어요?', '옆자리 선생님', hold=0.05)
say('E05b', r'텀블러에,\N누가 침을 뱉었대요.', '옆자리 선생님')
say('E06', '쪽지엔… 담임 욕까지.', '옆자리 선생님')
ev(k['K5']['start'], k['K5']['start'] + k['K5']['dur'], 'Scene', r'{\an7\pos(40,240)}회상 · 작년, 최 선생님을 놀리던 학생들', 6)
say('E07', r'쌤, 요새는\N텀블러 안 들고 다니세요?', '옆 반 학생')
say('E08', '헐—', '지우 영혼', PINK, hold=0.25)
say('E09a', '…헐, 헐레벌떡… 놀랐습니다.', '지우 영혼', PINK)
narr(L['E09a'], L['E09b'], r'(당황해서\N아무 말 대잔치 중)')   # v3: 사장님 2026-10-27
say('E09b', '…진짜 그런 애가 있다고요?', '지우 영혼', PINK)
say('E10', r'알잖아요,\N작년에 선생님 반이었던…', '옆자리 선생님', hold=0.3)
narr(L['E10'] + 1.2, k['K7b']['start'] + k['K7b']['dur'], r'(작년 담임 반\N아이 짓?)')
say('E11', '아… 아, 걔. 네, 네.', '지우 영혼', PINK)
say('E12', r'…누군데?\N쌤한테 물어봐야지.', '(속마음) 지우 영혼', PINK, 'Mono', hold=0.05)   # v4: 폰이 올라오기 전에 끝
ev(k['K9']['start'], k['K9']['start'] + k['K9']['dur'], 'Scene', r'{\an7\pos(40,240)}지우 → 진짜 담임(지우 몸)에게 DM', 6)
ev(k['K10']['start'], k['K10']['start'] + 2.0, 'Scene', r'{\an7\pos(40,240)}같은 시각 · 교실 · 지우 몸에 담임 영혼', 6)
narr(L['E15'] + 0.3, k['K10']['start'] + k['K10']['dur'], r'(시력은\N빙의가 안 됐나?)', 40, 880)
# 받은 DM(받는 사람 화면 = 글자만, 목소리 없음)
ev(k['K10']['start'] + 0.1, k['K10']['start'] + 1.6, 'DMp', r'{\an4\pos(80,860)\fad(80,120)}쌤!!! 대박 사건ㅠㅠ\N작년 쌤 반 애래요;;', 4)
ev(k['K10']['start'] + 0.1, k['K10']['start'] + 1.6, 'TagJ', r'{\an1\pos(80,770)\fad(80,120)}지우가 담임에게 · DM', 5)
say('E14a', '지우야, 너 노안 왔냐?', '반 친구')
say('E15', '…요즘 폰 글씨가 작아.', '담임 영혼', SKY)
say('E16', '…쟤가 왜 또 혼자…', '(속마음) 담임 영혼', SKY, 'Mono', hold=0.4)
narr(L['E16'] + 0.3, L['E14b'] - 0.05, r'(작년 우리 반…\N그 아이)', 560, 700)
say('E14b', r'야, 너 왜 할아버지처럼\N창밖 봐?', '반 친구')
say('E17', '…에헴. 경치가… 좋구나.', '담임 영혼', SKY, end=MAIN - 0.05)
PEND.sort(key=lambda x: x['a'])
for i, x in enumerate(PEND):
    nxt = next((y for y in PEND[i + 1:] if y['grp'] != x['grp']), None)
    if nxt and x['b'] > nxt['a'] - 0.03: x['b'] = nxt['a'] - 0.03
    emit(x); SUBS.append((round(x['a'], 2), round(x['b'], 2), x['text'].replace(r'\N', ' ')))

head = (KIT / 'soulchange_style.ass').read_text(encoding='utf-8').rstrip('\n')
OWN = ("Style: Narr,Jua,66,&H005AE3FF,&H005AE3FF,&H80000000,&H80000000,0,0,0,0,100,100,0,0,3,8,0,2,0,0,0,1\n"
       "Style: DlgB,Jua,62,&H00FFFFFF,&H00FFFFFF,&H33000000,&H33000000,0,0,0,0,100,100,0,0,3,10,0,2,0,0,0,1\n"
       "Style: MonoB,Jua,60,&H00E6F2FF,&H00E6F2FF,&H33402A20,&H33402A20,0,0,0,0,100,100,0,0,3,10,0,2,0,0,0,1\n"
       "Style: TagJ,Jua,54,&H00FFFFFF,&H00FFFFFF,&H009A4FE0,&H009A4FE0,0,0,0,0,100,100,0,0,3,9,0,2,0,0,0,1\n"
       "Style: TagT,Jua,54,&H00FFFFFF,&H00FFFFFF,&H00C07A2A,&H00C07A2A,0,0,0,0,100,100,0,0,3,9,0,2,0,0,0,1\n"
       "Style: TagW,Jua,54,&H00FFFFFF,&H00FFFFFF,&H00606066,&H00606066,0,0,0,0,100,100,0,0,3,9,0,2,0,0,0,1\n"
       "Style: TagJi,Jua,54,&H00C88CFF,&H00C88CFF,&H00303038,&H00303038,0,0,0,0,100,100,0,0,3,9,0,2,0,0,0,1\n"
       "Style: TagTi,Jua,54,&H00FFC88C,&H00FFC88C,&H00303038,&H00303038,0,0,0,0,100,100,0,0,3,9,0,2,0,0,0,1")
head = head.replace('\n[Events]', '\n' + OWN + '\n[Events]', 1) if '\n\n[Events]' not in head else head.replace('\n\n[Events]', '\n' + OWN + '\n\n[Events]', 1)
assert 'TagJ,' in head
(B / 'ep6.ass').write_text(head + '\n' + '\n'.join(EV) + '\n', encoding='utf-8')

# ---------- 6. 합치기: 영혼 원(+지지직) + 자막 → 엔딩 ----------
en_j = '+'.join(f"between(t,{c['start']},{c['start'] + c['dur'] - 0.001:.3f})" for c in CUTS if c['pip'] == 'pip')
en_t = '+'.join(f"between(t,{c['start']},{c['start'] + c['dur'] - 0.001:.3f})" for c in CUTS if c['pip'] == 'pip_t')
vf = (f"[1:v]scale=300:300[pj];[2:v]scale=300:300[pt];[3:v]setpts=PTS-STARTPTS+{GLITCH[0]:.3f}/TB[gl];"
      f"[0:v][pj]overlay=x=750:y=130:enable='{en_j}'[a];[a][pt]overlay=x=750:y=130:enable='{en_t}'[b];"
      f"[b][gl]overlay=x=750:y=130:eof_action=pass:enable='between(t,{GLITCH[0]:.3f},{GLITCH[1]:.3f})'[c];"
      f"[c]ass={B / 'ep6.ass'}:fontsdir={KIT / 'fonts'},format=yuv420p[vout]")
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', B / 'joined.mp4', '-i', KIT / 'pip.png', '-i', KIT / 'pip_t.png',
     '-framerate', FPS, '-i', GDIR / 'g_%02d.png',
     '-filter_complex', vf, '-map', '[vout]', '-t', MAIN, '-r', FPS, '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', B / 'main_v.mp4'])
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', B / 'ending_ep6.mp4', '-an', '-vf', f'fps={FPS},format=yuv420p,setsar=1',
     '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', B / 'ending_v.mp4'])
(B / 'vlist.txt').write_text(f"file '{B / 'main_v.mp4'}'\nfile '{B / 'ending_v.mp4'}'\n")
out = HERE / 'ep6_v4.mp4'
run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', B / 'vlist.txt', '-i', B / 'mix.wav',
     '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-t', TOT, '-movflags', '+faststart', out])
json.dump({'main': MAIN, 'ending': END_LEN, 'total': TOT, 'loudness_LUFS': I2, 'true_peak_dBTP': TP2,
           'cuts': [{kk: (str(vv) if isinstance(vv, pathlib.Path) else vv) for kk, vv in c.items()} for c in CUTS],
           'lines': {lid: {'start': L[lid], 'end': round(L[lid] + D[lid], 3), 'tempo': SPEC[lid]['tempo'], 'file': SPEC[lid]['f'],
                           'range': SPEC[lid]['r'], 'inner': lid in INNER} for lid in sorted(L, key=L.get)},
           'subs': SUBS, 'glitch': GLITCH, 'bgm': BGM_SECT},
          open(HERE / 'timeline_v4.json', 'w'), ensure_ascii=False, indent=1)
print('OK', out, TOT)
