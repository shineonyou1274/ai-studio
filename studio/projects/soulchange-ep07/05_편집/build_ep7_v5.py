#!/usr/bin/env python3
"""소울체인지 7화 편집 v5 (교감 지시 장면 = VP_lipsync_test.mp4(E7v5-01b 오디오 참조 립싱크). 영상과 녹음을 같은 구간·같은 배속으로 잘라 입을 맞춤).

--- 아래는 v4 설명 ---
소울체인지 7화 편집 v4 (사장님·Gemini v3 지적: '그 학생' → '해당 학생', 교감 새 녹음 E7v5-01b, 탁자 모양 맞추기(K2·K12 자르기), 회상 진입 번쩍임, 배경음 키움·대치 긴장·구두 소리, 헛기침 뒤 뻐끔 0.5초 덜어 냄).

--- 아래는 v3 설명 ---
소울체인지 7화 편집 v3 (v2 + 어머니 "갑자기 웬 향수요?", 요소 손 컷 자동 교체, K12 요소 컷, Gemini 지적: 회상 효과·DM 겹침·배경음·과장 표정).

--- 아래는 v2 설명 ---
소울체인지 7화 편집 v2 (대본 v5 + "6번 최종", 사장님 2026-10-27 지적, 크레딧 0).

바뀐 흐름
- 첫머리: 메신저 문자(K0) 없앰 → 교무실에서 교감이 말로 지시(E7v5-01). 5화 교감 컷(입 안 맞음)과
  담임 몸(지우 영혼)이 웃으며 듣는 6화 K08 컷을 번갈아 붙임. 교감 "웃으면서, 조용히." → "네, 네!"
- 김 선생 = 해당 학생의 작년 담임(지금 담임은 병가). 신고 이야기 전부 뺌(E7-04·05·14·17, 옛 K11 DM, "엄마를, 제가요?", "해야죠, 뭐." 안 씀).
- 상담: 어머니 "작년에 선생님이 우리 애한테 한 정서학대" → 속마음 "정서학대...? 우리 쌤이?!" → 탁자 밑 DM 글자 "쌤!!! 정서학대래요??"
- 교실: 친구 "누구랑 그렇게 열심히 톡해?" → "...쉿. 어른 일이다." → 친구 "웬 어른? 너 요즘 이상해."
- 향수: 킁킁 → 속마음 두 줄(둘째 줄은 6화 최 쌤 자리 회상 화면) → 손으로 입 "헐!"(6화 E6-08d + 지지직) → 기침 → "향수가... 고급지시네요"
- 욕 뒤: A 쪽지 속마음 → B 지우 DM → C 담임 DM → D 지우 DM → 어머니 퇴장 → E 벤치 담임 속마음 → F 담임 DM → G "아동학대요?!" 벌떡 → "아이고, 허리야..." → H 받은 DM(글자만)
- DM(보냄)은 보내는 쪽 화면에 말풍선 + 녹음, 받은 DM(H)은 글자만.
사용: python3 build_ep7_v2.py            → ep7_v2.mp4 (본편 64초 안, CUT_SET 적용)
      python3 build_ep7_v2.py --full     → ep7_v2_full.mp4 (아무것도 안 뺀 참고본, 길이 제한 없음)
"""
import json, math, pathlib, random, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from vo_prep import prep
import bgm

LONG = '--long' in sys.argv
FULL = LONG   # 길이 검사 안 함
# 64초를 넘을 때 빼는 것(코디네이터 순서: 1 쉼·빠르기 → 2 R2 "흠흠" → 3 "살펴 가세요" → 4 어머니 첫 대사 → 그 뒤는 후보)
STEP14 = {'HM', 'E13', 'E01short', 'D_trim', 'F_trim'}          # 코디네이터 1~4단계(+D·F 앞 토막)
PROPOSE = {'C_cut', 'E_cut', 'F_short', 'D_cut'}             # 그래도 넘쳐서 편집장이 더 뺀 후보
CUT_SET = STEP14 if LONG else STEP14 | PROPOSE

KIT = pathlib.Path('/home/user/youtube-ops/series/_soulchange_kit')
EP = HERE.parent
V = EP / '04_생성물' / 'voices'
C = EP / '04_생성물' / 'clips'
PC = KIT / 'episodes/ep7/clips'
PC6 = KIT / 'episodes/ep6/clips'
E5 = EP.parent / 'soulchange-ep05' / '04_생성물' / 'clips'
E6 = EP.parent / 'soulchange-ep06' / '04_생성물' / 'clips'
V6 = EP.parent / 'soulchange-ep06' / '04_생성물' / 'voices'
BENCH = EP.parent / 'soulchange-ep06' / '05_편집' / 'build_v5' / 'K11_hood.mp4'   # 6화 K11(벤치 머리 윤곽 보정본)
TAG_ = 'v5_long' if LONG else 'v5'
B = HERE / f'build_{TAG_}'; B.mkdir(exist_ok=True)
VO = B / 'vo'
FONT = KIT / 'fonts/Jua-Regular.ttf'
FPS, W, H = 30, 1080, 1920
END_LEN = 5.7
MAIN_MAX = 64.0
ENDING = HERE / 'build_v1' / 'ending_ep7.mp4'     # make_ending.py 7 금 ("다음 화 금요일 18시")
f = lambda s: ImageFont.truetype(str(FONT), s)


def run(cmd, **kw):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, **kw)
    if r.returncode: raise SystemExit(' '.join(map(str, cmd)) + '\n' + r.stderr[-2000:])
    return r


def dur_of(p):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)], capture_output=True, text=True).stdout)


# ---------- 1. 대사 ----------
T, G = 1.15, 0.10
SPEC = {
    # 교감(Arthur) 말로 지시 — 세 토막(교차 편집용)
    'E02a': dict(f='E7-02_jiu_teacherbody_raw.mp3', r=[(0, 0.95)], tempo=1.10),             # "네, 네!"
    'E01': dict(f='E7-01_mother_soraya_raw.mp3', r=[(0, 2.05)] if 'E01short' in CUT_SET else [(0, 5.40)], gap=0.25, tempo=1.08),
    'E02b': dict(f='E7-02_jiu_teacherbody_raw.mp3', r=[(1.30, 4.75)], tempo=1.15, gap=0.15),   # "품격... 넘치죠, 그럼요!"
    'V02': dict(f='E7v5-02_mother_soraya_raw.mp3', r=[(0, 4.05)], tempo=1.08),              # "작년에 선생님이 우리 애한테 한 정서학대, 잊으셨어요?"
    'V03': dict(f='E7v5-03_jiu_inner_student_raw.mp3', r=[(0, 2.40)], gap=0.18, tempo=1.08),   # 속마음 "정서학대...? 우리 쌤이?!"
    'V04': dict(f='E7v5-04_friend_pixie_raw.mp3', r=[(0, 2.90)]),                          # "지우야, 누구랑 그렇게 열심히 톡해?"
    'E06': dict(f='E7-06_teacher_studentbody_raw.mp3', r=[(0, 2.10)], gap=0.18, tempo=1.08),   # "...쉿. 어른 일이다."
    'V05': dict(f='E7v5-05_friend_pixie_raw.mp3', r=[(0, 3.70)], gap=0.18),                # "웬 어른? 너 요즘 이상해."
    'V06a': dict(f='E7v5-06_jiu_inner_student_raw.mp3', r=[(0, 3.30)], gap=0.18),          # 속마음 "이 향수 냄새... 어디서 맡아 봤더라?"
    'V06b': dict(f='E7v5-06_jiu_inner_student_raw.mp3', r=[(3.85, 6.40)], gap=0.18),       # 속마음 "...아. 최 쌤 향수랑 똑같잖아?"
    'E09c': dict(f='E7-09_jiu_teacherbody_raw.mp3', r=[(0, 0.82)], tempo=1.0),             # v4: 기침 꼬리 줄임              # 기침
    'E09': dict(f='E7-09_jiu_teacherbody_raw.mp3', r=[(3.02, 6.45)], tempo=1.25, gap=0.12),   # "향수가... 아주... 고급지시네요..."
    'E10a': dict(f='E7-10_mother_soraya_raw.mp3', r=[(0, 1.15)], tempo=1.0),                # "향수요?!"
    'E10c': dict(f='E7v5-14_mother_soraya_raw.mp3', r=[(0, 1.65)], tempo=1.08),             # "...갑자기 웬 향수요?" (v3 새 녹음)
    'E10b': dict(f='E7-10_mother_soraya_raw.mp3', r=[(1.62, 4.58)], tempo=1.05),            # "애 하나 때문에 집안이 곤란한데, 그 담임" (욕은 삐)
    'V07': dict(f='E7v5-07_jiu_inner_student_raw.mp3', r=[(0, 6.65)], gap=0.18),           # A 속마음
    'V08a': dict(f='E7v5-08_jiu_dm_student_raw.mp3', r=[(0, 1.92)], gap=0.18),             # B "쌤, 쪽지에 있던 거요."
    'V08b': dict(f='E7v5-08_jiu_dm_student_raw.mp3', r=[(1.98, 5.05)]),                    # B "그거 아무래도 그 애 엄마 이야기 같은데요?"
    'V09': dict(f='E7v5-09_teacher_dm_teacher_raw.mp3', r=[(0, 3.45)], gap=0.22),          # C "엄마? 엄마라니. 그거 무슨 말이야?"
    'V10a': dict(f='E7v5-10_jiu_dm_student_raw.mp3', r=[(0, 2.45)]),                       # D "이건 그냥 제 촉인데요."
    'V10b': dict(f='E7v5-10_jiu_dm_student_raw.mp3', r=[(2.92, 4.30)]),                    # D "아니, 확실해요."
    'V10c': dict(f='E7v5-10_jiu_dm_student_raw.mp3', r=[(4.72, 7.95)]),                    # D "아무래도 자기 엄마에 대한 불만을 써 둔 것 같아요."
    'E12': dict(f='E7-12_mother_soraya_raw.mp3', r=[(0, 2.55)]),                            # "애는 엄마가 제일 잘 알아요!"
    'E13': dict(f='E7-13_jiu_teacherbody_raw.mp3', r=[(0, 1.80)]),                          # "살... 살... 살펴 가세요..."
    'HM': dict(f='E6-03_vp_arthur_raw.mp3', r=[(0, 1.00)], tempo=1.0),                     # 6화 교감 "흐흠..."
    'V11': dict(f='E7v5-11_teacher_inner_teacher_raw.mp3', r=[(0, 3.55)], gap=0.30, tempo=1.08),   # E 담임 속마음 "그럴 리가... 그렇다면 그게 다..."
    'V12a': dict(f='E7v5-12_teacher_dm_teacher_raw.mp3', r=[(0, 1.88)]),                   # F "이거 아동학대일 수도 있겠다."
    'V12b': dict(f='E7v5-12_teacher_dm_teacher_raw.mp3', r=[(2.26, 3.40)]),                # F "정신 바짝 차려."
    'V12c': dict(f='E7v5-12_teacher_dm_teacher_raw.mp3', r=[(3.62, 6.60)], gap=0.15),      # F "아직 직접적인 증거는 없으니, 좀 더 알아봐야겠다."
    'V13': dict(f='E7v5-13_jiu_teacherbody_raw.mp3', r=[(0, 0.95)], tempo=1.0),             # G "아동학대요?!"(담임 몸 고함)
    'E16b': dict(f='E7-16b_jiu_teacherbody_raw.mp3', r=[(1.45, 3.20)], tempo=1.05),         # "아이고, 허리야..."
}
OLD6 = {'HM': dict(f='E6-03_vp_arthur_raw.mp3', r=[(0, 1.00)], tempo=1.0),
        'HUL': dict(f='E6-08d_jiu_leak_student_raw.mp3', r=[(0, 0.60)], tempo=1.0)}       # 6화 "헐!" 다시 씀
SPEC.pop('HM')
DROP = set()
if 'HM' in CUT_SET: DROP.add('HM')
if 'E13' in CUT_SET: DROP.add('E13')
if 'E01short' in CUT_SET: DROP.add('E02b')          # "품격" 말이 빠지면 "품격... 넘치죠"도 뺀다
if 'D_trim' in CUT_SET: DROP |= {'V10a', 'V10b'}
if 'F_trim' in CUT_SET: DROP.add('V12b')
if 'C_cut' in CUT_SET: DROP.add('V09')
if 'E_cut' in CUT_SET: DROP.add('V11')
if 'F_short' in CUT_SET: DROP |= {'V12b', 'V12c'}
if 'E10a_cut' in CUT_SET: DROP.add('E10a')
if 'B_short' in CUT_SET: DROP.add('V08a')
if 'D_cut' in CUT_SET: DROP |= {'V10a', 'V10b', 'V10c'}
for s in list(SPEC.values()) + list(OLD6.values()):
    s.setdefault('tempo', T); s.setdefault('gap', G)
SPEC = {k_: v_ for k_, v_ in SPEC.items() if k_ not in DROP}
OLD6 = {k_: v_ for k_, v_ in OLD6.items() if k_ not in DROP}
D = prep(SPEC, V, VO); D.update(prep(OLD6, V6, VO)); SPEC.update(OLD6)
# v5 교감 립싱크: 녹음과 영상(VP_lipsync_test, 녹음 0초 = 영상 0초)을 같은 구간으로 잘라 같은 배속(VPS)으로 줄인다.
#   쉼을 줄이려 구간 사이(0.80–1.04, 3.10–3.56, 7.20–7.58)를 덜어 냄 → 영상은 펀치 인 크기를 바꿔 이음매를 감춤. vo_prep의 쉼 줄이기는 쓰지 않음(입이 어긋나므로).
VPCLIP = C / 'VP_lipsync_test.mp4'; VPS = 1.12
VPSEG = [('VPa', 0.00, 0.80), ('VPb', 1.04, 3.10), ('VPc', 3.56, 7.20), ('VPd', 7.58, 9.45)]
import vo_prep as _vp
_full = _vp.decode(V / 'E7v5-01b_vp_arthur_raw.mp3', 0, 10.0)
_tmp = VO / '_vp_full.wav'
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(_vp.SR), '-ac', '1', '-i', '-', str(_tmp)], input=_full.astype(np.float32).tobytes(), check=True)
_g = -18.0 - _vp.lufs(_tmp)
for lid, a_, b_ in VPSEG:
    run(['ffmpeg', '-y', '-v', 'error', '-ss', a_, '-to', b_, '-i', _tmp, '-af', f'volume={_g:.2f}dB,alimiter=limit=0.7:level=false:attack=1:release=50,afade=t=in:d=0.01,areverse,afade=t=in:d=0.02,areverse,atempo={VPS}',
         '-ar', '48000', '-c:a', 'pcm_s16le', VO / f'{lid}.wav'])
    D[lid] = round(dur_of(VO / f'{lid}.wav'), 3); SPEC[lid] = dict(f='E7v5-01b_vp_arthur_raw.mp3', r=[(a_, b_)], tempo=VPS, gap=None)
INNER = {'V03', 'V06a', 'V06b', 'HUL', 'V07', 'V11'}     # 속마음 = 영혼 목소리 + 잔향
has = lambda lid: lid in D

# ---------- 2. 컷 ----------
L, CUTS = {}, []
t = 0.0
def cut(cid, src, ss, se, pip, dur, zoom=(1.0, 0.5, 0.5), note='', fx=None, stretch=None, ph=None, vfx='', hold=None):
    global t
    CUTS.append(dict(id=cid, src=src, ss=ss, se=se, pip=pip, start=round(t, 3), dur=round(dur, 3), zoom=zoom, note=note, fx=fx, st=stretch,
                     ph=ph, vfx=vfx, hold=hold))
    t += dur
def at(lid, x):
    L[lid] = round(x, 3); return x + D[lid]
def end_(lid): return L[lid] + D[lid]
ELEMZ = (1.2, 0.5, 1.0)     # 요소 손 컷: 1.2배, 아래 기준으로 잘라 위쪽 턱·얼굴을 뺌
def hand(cid, fnames, dur, label, note):
    """어머니 손 컷: [(파일, 시작초, 확대)] 앞에서부터 있는 파일을 씀(1.15배까지 늘리고 모자라면 끝 프레임), 하나도 없으면 임시 화면."""
    for p, ss, zm in fnames:
        if p.exists():
            avail = dur_of(p) - ss; stt = min(1.15, max(1.0, dur / avail))
            cut(cid, p, ss, None, 'pip', dur, zoom=zm, stretch=stt, note=note + f' — {p.name}'); return
    cut(cid, None, 0, None, 'pip', dur, fx='ph', ph=label, note=note + f' — 【임시 화면】 ' + ' 또는 '.join(x[0].name for x in fnames) + ' 오면 자동으로 바뀜')
NOZ = (1.0, 0.5, 0.5)
K1E = C / 'K1_elem_test.mp4'

# OP v5: 교무실 교감 립싱크 컷(VP_lipsync_test) 네 토막 — 녹음 토막과 시작·길이·배속이 같다. 왼쪽 담임 뒤통수(검은 머리)는 1.35배 확대로 대부분 빼고 남는 가장자리는 강하게 흐림.
c0 = t
VPZ = {'VPa': (1.35, 0.62, 0.30), 'VPb': (1.50, 0.66, 0.30), 'VPc': (1.35, 0.62, 0.32), 'VPd': (1.42, 0.60, 0.28)}
for lid, a_, b_ in VPSEG:
    at(lid, t)
    cut('OP_' + lid, VPCLIP, a_, b_, 'pip', D[lid], stretch=1 / VPS, zoom=VPZ[lid], note=f'교감 립싱크 컷 원본 {a_}–{b_}초, 녹음 같은 구간')
    CUTS[-1]['eblur'] = (0.13, 0.95)          # 왼쪽 13%·오른쪽 5% 강하게 흐림(담임 뒤통수·어깨)
e = at('E02a', t + 0.08)
cut('OPd', PC6 / 'K08.mp4', 1.55, None, 'pip', end_('E02a') + 0.15 - t, note='6화 K08 담임 몸 활짝 웃음 — "네, 네!"')
# K1 어머니 손 — "우리 아이는 아무 문제가 없어요.(순둥이, 타고난 품격이 있는 아이라구요!)"
c0 = t; TAK = c0 + (0.32 if K1E.exists() else 0.05)    # K1_elem_test: 원본 0.8초에 손바닥 탁
e = at('E01', c0 + 0.20)
hand('K1', [(K1E, 0.45, ELEMZ), (PC / 'K01.mp4', 0, NOZ)], e + (0.08 if has('E02b') else 0.25) - c0, 'K1 자리 (어머니 손)\n손바닥 탁 + 가방 속 향수병', '어머니 손: 탁자 탁, 가방 입구 향수병')
if has('E02b'):   # K3a 담임 몸 굽신 웃음
    c0 = t; e = at('E02b', c0 + 0.08)
    cut('K3a', PC / 'K03.mp4', 0.1, None, 'pip', e + 0.08 - c0, stretch=min(1.15, max(1.0, (e + 0.08 - c0) / 2.5)), note='담임 몸 굽신 웃음 — "품격... 넘치죠, 그럼요!"')
# K2 어머니 손가락 — "작년에 선생님이 우리 애한테 한 정서학대, 잊으셨어요?"
c0 = t; e = at('V02', c0 + 0.10)
_k2 = len(CUTS)
hand('K2', [(C / 'K2_elem.mp4', 2.30, (1.6, 1.0, 0.18)), (PC / 'K02.mp4', 0, NOZ)], e + 0.10 - c0, 'K2 자리 (어머니 손)\n검지로 콕, 탁자 톡톡', '어머니 손가락 콕')
if CUTS[_k2]['src'] is not None and 'K2_elem' in str(CUTS[_k2]['src']): CUTS[_k2]['focus'] = (0.70, 0.36, 0.42)   # v4: 손 주변만 또렷, 탁자 모서리는 흐림
# K3b 웃음 빠짐 → 탁자 밑 폰 두 엄지 — 속마음 "정서학대...? 우리 쌤이?!" → DM 글자 "쌤!!! 정서학대래요??"
c0 = t; ZOOM_T = c0 + 0.05
e = at('V03', c0 + 0.12)
cut('K3b', PC / 'K03.mp4', 2.95, 5.04, 'pip', e + 0.45 - c0, stretch=1.15, hold=True, note='v3: 과장된 눈(2.5–2.9) 뺌, 2.95부터 → 폰 두 엄지 → 끝 프레임 멈춤+다가감 / v2: ' + '눈 커짐 → 탁자 밑 폰 두 엄지(입 다묾) — 속마음 + DM 글자')
DM1 = end_('V03') + 0.05
# K4 교실(지우 몸, 담임 영혼): 폰 두드림 → "쉿" — 친구 화면 밖
k4s = 1.15; c0 = t; TYPE4 = c0 + 0.2
e = at('V04', c0 + 0.12)
e = at('E06', max(e + 0.12, c0 + 2.55 * k4s))
K4END = (dur_of(C / 'K4.mp4') - 0.02) * k4s
e = at('V05', e + 0.15)
cut('K4', C / 'K4.mp4', 0, None, 'pip_t', min(K4END, e + 0.15 - c0), stretch=k4s, note='지우 몸(담임 영혼) 폰 두드림 → "쉿"')
# K4b 6화 H3 지우 몸 콧등 잡고 귀찮은 얼굴(입 다묾) — 친구 "웬 어른? 너 요즘 이상해." 말꼬리
if e + 0.15 > t + 0.2:
    cut('K4b', E6 / 'H3_K10.mp4', 1.75, 3.30, 'pip_t', e + 0.15 - t, stretch=min(1.15, max(1.0, (e + 0.15 - t) / 1.55)), note='6화 H3 지우 몸 콧등 잡음 — 친구 말꼬리')
# K6a 담임 몸(K06 0–0.7) 킁킁 → 입 다문 얼굴 멈추고 천천히 다가감 — 속마음 1
c0 = t; SNIFF = c0 + 0.06
e = at('V06a', c0 + 0.45)
if K1E.exists():   # v3: 과장된 입(원본 0.0–0.3) 뺀 짧은 킁킁 0.5초 → 어머니 가방 속 향수병(요소 K1 3.0~)
    cut('K6a', PC / 'K06.mp4', 0.28, 0.70, 'pip', 0.48, stretch=1.15, note='담임 몸 킁킁(짧게)')
    _need = e + 0.10 - t
    cut('K6s', K1E, 2.6, None, 'pip', _need, zoom=ELEMZ, stretch=min(1.15, max(1.0, _need / (dur_of(K1E) - 2.6))),
        vfx=f"zoompan=z='1+0.10*on/{round(_need * FPS)}':x='iw*0.62-(iw/zoom*0.62)':y='ih*0.6-(ih/zoom*0.6)':d=1:s=1080x1920:fps={FPS},", note='요소 K1 가방 속 향수병으로 다가감 — 속마음 1')
    CUTS[-1]['vfx'] += f"fade=t=out:st={_need - 0.10:.3f}:d=0.10:color=white,"     # v4: 회상 들어가기 직전 흰 번쩍임
else:
    cut('K6a', PC / 'K06.mp4', 0.0, 0.70, 'pip', e + 0.10 - c0, stretch=1.15, hold=True, note='담임 몸 킁킁(0–0.7) → 입 다문 프레임 멈춤 + 다가감')
# K6f 회상: 6화 K02 최 쌤 자리, 책상 위 향수병 쪽으로 다가감(흑백 기운) — 속마음 2 "...아. 최 쌤 향수랑 똑같잖아?"
c0 = t; e = at('V06b', c0 + 0.12)
cut('K6f', PC6 / 'K02.mp4', 0.3, None, 'pip', e + 0.15 - c0, zoom=(1.45, 0.0, 0.62),
    vfx="hue=s=0.30,eq=brightness=0.03:contrast=1.05,", hold=False, note='회상: 6화 K02 최 쌤 자리 + 향수병 — v3 플래시백(흰 번쩍임 들고 남, 채도 낮춤, 가장자리 흐림·어둡게)')
CUTS[-1]['flash'] = True
# K6 손으로 입 "헐!"(빙의 풀림 2단계) → 기침 → 굳은 웃음 "향수가... 고급지시네요..."
k6s = 1.15; c0 = t; SS6 = 1.05    # v3: 눈 크게 뜬 손 입막음(0.75–1.05) 줄임 + 천천히 다가감
e = at('HUL', c0 + 0.06); GLITCH = (L['HUL'], L['HUL'] + 0.65)
e = at('E09c', max(e + 0.30, c0 + (2.75 - SS6) * k6s))
K6CUT, K6RES = 3.22, 3.62     # v4: 주먹 기침 끝(3.22) ~ 말 시작 전 입만 뻐끔(3.62)을 덜어 내고, 이어지는 컷은 1.12배 펀치 인
cut('K6', PC / 'K06.mp4', SS6, K6CUT, 'pip', (K6CUT - SS6) * k6s, stretch=k6s, vfx="zoompan=z='1+0.07*on/150':x='iw/2-(iw/zoom/2)':y='ih*0.4-(ih/zoom*0.4)':d=1:s=1080x1920:fps=30,", note='담임 몸: 손으로 입 "헐!" → 주먹 기침')
e = at('E09', max(e + 0.05, t + 0.05))
K6END = (dur_of(PC / 'K06.mp4') - K6RES) * k6s - 0.04
cut('K6c', PC / 'K06.mp4', K6RES, None, 'pip', min(e + 0.20 - t, K6END), stretch=k6s, zoom=(1.12, 0.5, 0.3), note='담임 몸: 손으로 입 "헐!" → 기침 → 굳은 웃음으로 말함')
# K7 어머니 손 — "향수요?!" → "애 하나 때문에 집안이 곤란한데, 그 담임 (삐)!"
K7E, K10E = C / 'K7_elem.mp4', C / 'K10_elem.mp4'
c0 = t
if has('E10a'):
    e = at('E10a', max(c0, end_('E09')) + 0.28)
    if has('E10c'): e = at('E10c', e + 0.10)
    e = at('E10b', e + 0.10)
else:
    e = at('E10b', max(c0, end_('E09')) + 0.30)
BEEP = e - 0.02; THUD7 = BEEP + 0.50
if K7E.exists() and K10E.exists() and has('E10c'):
    # v3: 말꼬리 + "향수요?!" = 요소 K10 앞(가방 위 두 손, 0–1.4) → "갑자기 웬 향수요?"부터 요소 K7(끈 비틀기 → 들어 올림 → 탁 내려놓음)
    _k7a = min(L['E10c'] - 0.08 - c0, 1.40 * 1.15)
    cut('K7a', K10E, 0.0, 1.40, 'pip', _k7a, stretch=1.15, note='요소 K10 앞: 가방 위 두 손 — "향수요?!"')
    _k7s = min(1.15, max(1.0, (BEEP + 0.50 - t) / 5.0)); THUD7 = t + 3.0 * _k7s       # 원본 3.0초에 가방을 탁 내려놓음
    cut('K7', K7E, 0.0, None, 'pip', BEEP + 0.50 - t, stretch=_k7s, note='요소 K7: 끈 비틀기 → 들어 올림 → 탁 — "갑자기 웬 향수요?" → 욕(삐)')
else:
  hand('K7', [(K7E, 0, NOZ), (PC / 'K07.mp4', 0, NOZ)], BEEP + 0.62 - c0, 'K7 자리 (어머니 손)\n가방 끈 비틀기, 탁자에 툭', '어머니 손: 가방 끈 꽉 → 툭')
# K8 A: 쪽지 다시(욕 동그라미, "냄새 싫어" 밑줄) — 속마음
c0 = t; e = at('V07', c0 + 0.25)
cut('K8', None, 0, None, 'pip', e + 0.15 - c0, fx='note', note='코드: 6화 쪽지 — A 속마음')
# K8b B: 상담실 탁자 밑, 지우(담임 몸) 폰에서 보냄
c0 = t; e = c0 + 0.12
for lid in ('V08a', 'V08b'):
    if has(lid): e = at(lid, e + 0.10)
if not has('V09'):   # C를 빼면 B와 D를 한 화면에서 이어 보냄
    for lid in ('V10a', 'V10b', 'V10c'):
        if has(lid): e = at(lid, e + 0.12)
cut('KB', None, 0, None, 'pip', e + 0.12 - c0, fx='dmB', note='코드: 상담실 탁자 밑 폰, 지우가 보냄(말풍선 둘)')
# C: 교실, 지우 몸(담임 영혼)이 폰을 보며 보냄 — 6화 H3 폰 보는 0–1.7 + 멈춤 다가감, 말풍선은 자막 쪽 DM 상자
if has('V09'):
    c0 = t; e = at('V09', c0 + 0.20)
    cut('KC', E6 / 'H3_K10.mp4', 0.1, 1.65, 'pip_t', e + 0.12 - c0, stretch=1.15, hold=True, note='6화 H3 지우 몸 폰 봄 — C 담임 DM(보냄)')
# D: 상담실 폰, 지우가 보냄
if has('V09'):
  c0 = t; e = c0 + 0.15
  for lid in ('V10a', 'V10b', 'V10c'):
    if has(lid): e = at(lid, e + 0.10)
  cut('KD', None, 0, None, 'pip', e + 0.15 - c0, fx='dmD', note='코드: 상담실 폰, 지우가 보냄')
# K10 어머니 손 — "애는 엄마가 제일 잘 알아요!" → 의자 끽 → 문 쾅 (→ "살... 살펴 가세요...")
c0 = t; e = at('E12', c0 + 0.15); CHAIR = e + 0.08; DOOR = e + 0.50
if (C / 'K10_elem.mp4').exists(): CHAIR = c0 + 0.25; DOOR = c0 + 2.75      # 요소 K10: 원본 1.5초에 가방 들고 일어남, 4.5초쯤 문 쪽으로 나감
if has('E13'): e = at('E13', DOOR + 0.30)
else: e = DOOR + 0.25
K10SS = 1.4 if 'K7a' in [c_['id'] for c_ in CUTS] else 0.0     # 앞 1.4초는 K7a에서 씀
hand('K10', [(K10E, K10SS, NOZ), (PC / 'K10.mp4', 0, NOZ)], max(e + 0.12 - c0, 3.0) if K10E.exists() else e + 0.12 - c0, 'K10 자리 (어머니 손)\n가방 낚아채고 일어남', '어머니 손: 가방 낚아채고 일어남')
if has('HM'):   # R2 그 시각 교무실 "흐흠..."
    c0 = t; e = at('HM', c0 + 0.35)
    cut('R2', E5 / 'A5a_K12a_교감끝훅.mp4', 2.45, 3.15, 'pip', e + 0.30 - c0, note='5화 교감(입 다묾) — "흐흠..."')
# E: 교실 창밖 벤치(6화 재사용) — 담임 영혼 속마음
if has('V11'):
  c0 = t; e = at('V11', c0 + 0.25)
  cut('K5', BENCH, 1.0, None, 'pip_t', e + 0.20 - c0, note='6화 K11 벤치 먼 뒷모습 — E 담임 속마음')
# F: 교실, 지우 몸 폰에서 담임 영혼이 보냄(코드 폰)
c0 = t; e = c0 + 0.15
for lid in ('V12a', 'V12b', 'V12c'):
    if has(lid): e = at(lid, e + 0.10)
cut('KF', None, 0, None, 'pip_t', e + 0.12 - c0, fx='dmF', note='코드: 지우 폰(지금은 쌤)에서 보냄')
# G: K12 담임 몸(빈 의자 앞) 폰 꼭 쥠 → "아동학대요?!" → 놀라 벌떡 → 허리
K12E = C / 'K12_elem.mp4'
# K12_elem(상담실 탁자, 폰 쥠 → 놀라 일어남 → 허리)이 있으면 그것. 동작 시각(K12E_T)은 클립을 보고 맞춘다 — 지금 값은 가정.
K12E_T = dict(ss=1.6, shout=2.65, crack=3.75, waist=4.0)   # 0–2.5 폰 봄, 2.6–3.0 놀라 일어남(입 벌림), 4.0~ 고개 젖혀 신음
k12s = 1.15; c0 = t
if K12E.exists():
    T12 = K12E_T
    e = at('V13', c0 + (T12['shout'] - T12['ss']) * k12s); CRACK = c0 + (T12['crack'] - T12['ss']) * k12s
    e = at('E16b', max(e + 0.25, c0 + (T12['waist'] - T12['ss']) * k12s))
    cut('K12', K12E, T12['ss'], None, 'pip', e + 0.10 - c0, stretch=k12s, zoom=(1.25, 0.5, 0.0), note='요소 K12(상담실): 폰 쥠 → "아동학대요?!" → 벌떡 → 허리')
else:
    SS12 = 1.3
    e = at('V13', c0 + (2.0 - SS12) * k12s)
    CRACK = c0 + (3.30 - SS12) * k12s
    e = at('E16b', max(e + 0.25, c0 + (3.55 - SS12) * k12s))
    cut('K12', C / 'K12.mp4', SS12, None, 'pip', e + 0.10 - c0, stretch=k12s, note='옛 K12(배경이 교실) — K12_elem.mp4 오면 자동으로 바뀜')
# H: 받은 DM(글자만)
c0 = t; DING = c0 + 0.45
cut('K13', None, 0, None, 'pip', 1.65, fx='dmH', note='코드: 담임 몸 폰에 온 DM(글자만, 소리 없음)')
MAIN = round(t, 3); TOT = round(MAIN + END_LEN, 3)
print('본편', MAIN, '합계', TOT, '뺀 것', sorted(CUT_SET))
for c in CUTS:
    if c['src'] is None: c['stretch'] = 1.0; c['se'] = c['ss']; print(f"  {c['id']:5s} {c['start']:6.2f} +{c['dur']:.2f}  {c['fx']}"); continue
    if c['hold']:
        c['stretch'] = c['st']; print(f"  {c['id']:5s} {c['start']:6.2f} +{c['dur']:.2f}  src {c['ss']}-{c['se']} x{c['st']} + 멈춤 {c['dur'] - (c['se'] - c['ss']) * c['st']:.2f}")
        continue
    if c['st']: c['stretch'] = c['st']; c['se'] = round(c['ss'] + c['dur'] / c['st'], 3)
    else:
        if c['se'] is None: c['se'] = round(c['ss'] + c['dur'], 3)
        c['stretch'] = round(min(1.15, c['dur'] / (c['se'] - c['ss'])), 3)
    over = c['se'] - dur_of(c['src'])
    print(f"  {c['id']:5s} {c['start']:6.2f} +{c['dur']:.2f}  src {c['ss']}-{c['se']} x{c['stretch']}" + (f"  ★원본 끝 넘음 {over:.2f}" if over > 0.05 else ''))
    assert c['stretch'] <= 1.151, c
if not FULL: assert MAIN <= MAIN_MAX + 1e-6, f'본편 {MAIN} > {MAIN_MAX}'
if '--plan' in sys.argv: sys.exit(0)


# ---------- 3. 영상 조각 ----------
def grab(src, tsec):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{tsec}', '-i', str(src), '-frames:v', '1', '-vf', 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    return Image.frombytes('RGB', (W, H), raw[:W * H * 3])


def push_frames(img, n, z1=0.06, z0=1.0):
    out = []
    for i in range(n):
        z = z0 + z1 * i / max(1, n - 1); w, h = W / z, H / z
        out.append(np.asarray(img.transform((W, H), Image.EXTENT, ((W - w) / 2, (H - h) / 2 * 0.8, (W + w) / 2, (H - h) / 2 * 0.8 + h), Image.BICUBIC), np.uint8))
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


def phone(img_bg, header, bubbles, tt, side='R', col=(255, 140, 190), y_top=380, ph_=1200, rise=1.0, hint='', tag='', tagcol=(200, 60, 140), pw=700, big=False):
    """폰 화면 하나. bubbles = [(나타나는 시각, 글)]; side R = 보낸 쪽(오른쪽), L = 받은 쪽(왼쪽)."""
    im = img_bg.copy(); d = ImageDraw.Draw(im)
    x0 = (W - pw) // 2; y0 = y_top + int((1 - rise) * 1400)
    d.rounded_rectangle([x0, y0, x0 + pw, y0 + ph_], 70, fill=(22, 22, 26))
    sx0, sy0, sx1, sy1 = x0 + 22, y0 + 22, x0 + pw - 22, y0 + ph_ - 22
    d.rounded_rectangle([sx0, sy0, sx1, sy1], 52, fill=(236, 238, 244))
    d.rectangle([sx0, sy0 + 40, sx1, sy0 + 150], fill=(222, 225, 234))
    d.text((sx0 + 34, sy0 + 95), header, font=f(42), fill=(30, 30, 30), anchor='lm')
    y = sy0 + 190
    F0, LH0 = (62, 78) if big else (46, 58)
    if tag and bubbles and tt >= bubbles[0][0]:   # v3: 화자 태그는 말풍선 위에 작게
        if side == 'R': d.text((sx1 - 34, y), tag, font=f(34), fill=tagcol, anchor='ra')
        else: d.text((sx0 + 34, y), tag, font=f(34), fill=tagcol, anchor='la')
        y += 50
    for k, (ta, txt) in enumerate(bubbles):
        if tt < ta: continue
        sc = min(1.0, 0.6 + (tt - ta) / 0.12 * 0.4); fs = int(F0 * sc)
        lines = txt.split('\n'); lh = int(LH0 * sc)
        tw = max(d.textlength(l, font=f(fs)) for l in lines); bh = lh * len(lines) + 32
        if side == 'R':
            d.rounded_rectangle([sx1 - 30 - tw - 44, y, sx1 - 30, y + bh], 30, fill=col)
            for i, l in enumerate(lines): d.text((sx1 - 30 - 22, y + 16 + i * lh), l, font=f(fs), fill=(255, 255, 255), anchor='ra')
        else:
            d.rounded_rectangle([sx0 + 30, y, sx0 + 30 + tw + 44, y + bh], 30, fill=col)
            for i, l in enumerate(lines): d.text((sx0 + 52, y + 16 + i * lh), l, font=f(fs), fill=(30, 30, 30), anchor='la')
        y += bh + 20
    d.rounded_rectangle([sx0 + 24, sy1 - 120, sx1 - 24, sy1 - 40], 40, fill=(255, 255, 255))
    d.text((sx0 + 60, sy1 - 80), hint, font=f(38), fill=(170, 170, 180), anchor='lm')
    return im


def drift(fr, z1=0.035):
    """코드 화면이 멈춰 보이지 않게 아주 천천히 다가감."""
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


def k8_frames(n):
    bg = dim_blur(grab(PC / 'K06.mp4', 4.9))
    paper = note_photo().resize((560, 703), Image.LANCZOS)
    fr = []
    for i in range(n):
        lt = i / FPS
        im = bg.copy(); d = ImageDraw.Draw(im)
        x0, y0 = 170, 300
        d.rounded_rectangle([x0, y0, x0 + 740, y0 + 1000], 70, fill=(22, 22, 26))
        d.rounded_rectangle([x0 + 22, y0 + 22, x0 + 718, y0 + 978], 52, fill=(18, 18, 20))
        z = 1.0 + 0.35 * min(1, lt / 0.6)
        pz = paper.resize((int(560 * z), int(703 * z)), Image.LANCZOS)
        box = Image.new('RGBA', (696, 956), (18, 18, 20, 255)); box.paste(pz, (348 - pz.width // 2 + int(60 * (z - 1)), 478 - pz.height // 2 + int(120 * (z - 1))), pz)
        im.paste(box.convert('RGB'), (x0 + 22, y0 + 22))
        d = ImageDraw.Draw(im)
        sx = (x0 + 22 + 348 - pz.width // 2 + int(60 * (z - 1))); sy = (y0 + 22 + 478 - pz.height // 2 + int(120 * (z - 1)))
        s_ = pz.width / 860
        if lt > 0.8:
            k_ = min(1, (lt - 0.8) / 0.5)
            d.arc([sx + 60 * s_, sy + 220 * s_, sx + 820 * s_, sy + 400 * s_], -200, -200 + 360 * k_, fill=(230, 40, 40), width=9)
        tu = 0.25 + (L['V07'] - CUTS_BY['K8']['start']) + 3.2      # "냄새는..." 나올 때 밑줄
        if lt > tu:
            k_ = min(1, (lt - tu) / 0.35)
            yy = sy + 590 * s_; d.line([(sx + 85 * s_, yy), (sx + (85 + 470 * k_) * s_, yy)], fill=(230, 40, 40), width=9)
        fr.append(np.asarray(im, np.uint8))
    return fr


def dm_seg(c, bg, header, items, side, col, recv=False, tag='', tagcol=(200, 60, 140)):
    """items = [(lid 또는 절대 시각, 말풍선 글)] — 말풍선은 그 녹음이 시작할 때 뜸."""
    nfr = round(c['dur'] * FPS); bubs = []
    for key, txt in items:
        ta = (L[key] if isinstance(key, str) else key) - c['start']
        bubs.append((ta, txt))
    last = bubs[-1][0] if bubs else 0
    return [np.asarray(phone(bg, header, bubs, i / FPS, side=side, col=col, rise=min(1, i / FPS / 0.3),
                             hint=('메시지 입력' if recv or i / FPS >= last + 0.2 else '입력 중...'), tag=tag, tagcol=tagcol, pw=820, big=True), np.uint8) for i in range(nfr)]


CUTS_BY = {c['id']: c for c in CUTS}
seg_list = []
for c in CUTS:
    out = B / f"seg_{c['id']}.mp4"; nfr = round(c['dur'] * FPS)
    if c['fx'] == 'ph':
        write_frames(ph_frames(nfr, c['ph']), out); seg_list.append(out); continue
    if c['fx'] == 'note':
        write_frames(drift(k8_frames(nfr)), out); seg_list.append(out); continue
    if c['fx'] == 'dmB':
        bg = dim_blur(grab(PC / 'K03.mp4', 4.6))
        items = [(lid, txt) for lid, txt in [('V08a', '쌤, 쪽지에\n있던 거요.'), ('V08b', '그거 아무래도\n그 애 엄마 이야기\n같은데요?')] if has(lid)]
        if not has('V09'):
            items += [(lid, txt) for lid, txt in [('V10a', '이건 그냥 제 촉인데요.'), ('V10b', '아니, 확실해요.'),
                                                   ('V10c', '아무래도 자기 엄마에 대한\n불만을 써 둔 것 같아요.')] if has(lid)]
        write_frames(drift(dm_seg(c, bg, '<  쌤 (지금 지우 몸)', items, 'R', (255, 120, 180), tag='지우 영혼이 보냄', tagcol=(215, 60, 140))), out)
        seg_list.append(out); continue
    if c['fx'] == 'dmD':
        bg = dim_blur(grab(PC / 'K03.mp4', 4.9), 18, 0.5)
        items = [(lid, txt) for lid, txt in [('V10a', '이건 그냥 제 촉인데요.'), ('V10b', '아니, 확실해요.'),
                                              ('V10c', '아무래도 자기 엄마에 대한\n불만을 써 둔 것 같아요.')] if has(lid)]
        prev = [(c['start'] + 0.01, '쌤, 쪽지에 있던 거요.'), (c['start'] + 0.01, '그거 아무래도\n그 애 엄마 이야기\n같은데요?')]
        if has('V09'): prev.append((c['start'] + 0.01, '엄마? 엄마라니.\n그거 무슨 말이야?'))
        fr = []
        for i in range(nfr):   # 앞 대화는 작게 위로 밀려 있고, 새 말풍선만 커지며 뜸 — 받은 C는 왼쪽(글자만)
            im = phone(bg, '<  쌤 (지금 지우 몸)', [], i / FPS, rise=1.0, hint='입력 중...' if i / FPS < (L[items[-1][0]] - c['start']) + 0.2 else '메시지 입력')
            d = ImageDraw.Draw(im); y = 590
            if has('V09'):
                d.rounded_rectangle([222, y, 222 + 380, y + 120], 26, fill=(255, 255, 255))
                d.text((244, y + 16), '엄마? 엄마라니.', font=f(40), fill=(30, 30, 30)); d.text((244, y + 64), '그거 무슨 말이야?', font=f(40), fill=(30, 30, 30))
                y += 150
            for lid, txt in items:
                ta = L[lid] - c['start']
                if i / FPS < ta: continue
                sc = min(1.0, 0.6 + (i / FPS - ta) / 0.12 * 0.4); fs = int(46 * sc); lines = txt.split('\n'); lh = int(58 * sc)
                tw = max(d.textlength(l, font=f(fs)) for l in lines); bh = lh * len(lines) + 32
                d.rounded_rectangle([858 - 30 - tw - 44, y, 858 - 30, y + bh], 30, fill=(255, 120, 180))
                for j, l in enumerate(lines): d.text((858 - 52, y + 16 + j * lh), l, font=f(fs), fill=(255, 255, 255), anchor='ra')
                y += bh + 20
            fr.append(np.asarray(im, np.uint8))
        write_frames(fr, out); seg_list.append(out); continue
    if c['fx'] == 'dmF':
        bg = dim_blur(grab(C / 'K4.mp4', 1.0))
        items = [(lid, txt) for lid, txt in [('V12a', '이거 아동학대일\n수도 있겠다.'), ('V12b', '정신 바짝 차려.'),
                                              ('V12c', '아직 직접적인 증거는\n없으니, 좀 더\n알아봐야겠다.')] if has(lid)]
        write_frames(drift(dm_seg(c, bg, '<  지우 (지금 쌤 몸)', items, 'R', (80, 150, 230), tag='담임 영혼이 보냄', tagcol=(40, 110, 200))), out); seg_list.append(out); continue
    if c['fx'] == 'dmH':
        bg = dim_blur(grab(C / 'K12.mp4', 4.9))
        write_frames(dm_seg(c, bg, '<  지우 (지금 쌤 몸)', [(DING, '...허리 조심해라.\n내 몸이다.')], 'L', (200, 225, 255), recv=True, tag='담임 영혼이 보냄', tagcol=(40, 110, 200)), out)
        seg_list.append(out); continue
    z, ax, ay = c['zoom']; used = c['se'] - c['ss']
    vf = (f"[0:v]trim=start={c['ss']}:duration={used:.3f},setpts=(PTS-STARTPTS)*{c['stretch']},fps={FPS},"
          f"scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,")
    if z != 1.0:
        sw, sh = int(round(1080 * z / 2) * 2), int(round(1920 * z / 2) * 2)
        vf += f"scale={sw}:{sh}:flags=lanczos,crop=1080:1920:{int((sw - 1080) * ax)}:{int((sh - 1920) * ay)},"
    if c['id'] == 'K3b':   # "띠용" 짧은 줌
        _t0 = ZOOM_T - c['start']
        vf += f"zoompan=z='if(lt(on,{int(_t0 * FPS)}),1,if(lt(on,{int(_t0 * FPS) + 5}),1+0.12*(on-{int(_t0 * FPS)})/5,1.12))':x='iw/2-(iw/zoom/2)':y='ih*0.35-(ih/zoom*0.35)':d=1:s=1080x1920:fps={FPS},"
    if c['id'] == 'K6f':   # 회상: 천천히 다가감
        vf += f"zoompan=z='1+0.10*on/{nfr}':x='iw*0.2-(iw/zoom*0.2)':y='ih*0.6-(ih/zoom*0.6)':d=1:s=1080x1920:fps={FPS},"
    vf += c['vfx']
    if c.get('eblur'):   # v5: 왼쪽·오른쪽 가장자리 강하게 흐림(담임 뒤통수 검은 머리)
        vf += "setsar=1,format=rgb24,tpad=stop_mode=clone:stop_duration=2.0[v]"
        r2 = subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(c['src']), '-filter_complex', vf, '-map', '[v]', '-frames:v', str(nfr), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
        mv = np.frombuffer(r2, np.uint8).reshape(-1, H, W, 3)
        l_, r_ = c['eblur']; xx = np.arange(W) / W
        m = np.clip(np.maximum((l_ - xx) / 0.06 + 1, (xx - r_) / 0.04 + 1), 0, 1)[None, :, None]
        fr = []
        for a_ in mv:
            bl = np.asarray(Image.fromarray(a_).resize((W // 16, H // 16), Image.BILINEAR).filter(ImageFilter.GaussianBlur(2)).resize((W, H), Image.BILINEAR), float)
            fr.append(np.clip(a_ * (1 - m) + bl * m * 0.9, 0, 255).astype(np.uint8))
        write_frames(fr[:nfr], out); seg_list.append(out); continue
    if c.get('focus'):   # v4: 얕은 심도 흉내 — 손 주변 타원만 또렷하고 바깥(탁자 모서리)은 흐리게
        vf += "setsar=1,format=rgb24,tpad=stop_mode=clone:stop_duration=2.0[v]"
        r2 = subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(c['src']), '-filter_complex', vf, '-map', '[v]', '-frames:v', str(nfr), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
        mv = np.frombuffer(r2, np.uint8).reshape(-1, H, W, 3)
        fx_, fy_, fr_ = c['focus']; yy, xx = np.mgrid[0:H, 0:W]
        rr = np.sqrt(((xx - W * fx_) / (W * fr_)) ** 2 + ((yy - H * fy_) / (H * fr_ * 0.75)) ** 2)
        m = np.clip((rr - 0.75) / 0.6, 0, 1)[..., None]
        fr = []
        for a_ in mv:
            bl = np.asarray(Image.fromarray(a_).resize((W // 10, H // 10), Image.BILINEAR).filter(ImageFilter.GaussianBlur(2.5)).resize((W, H), Image.BILINEAR), float)
            fr.append(np.clip(a_ * (1 - m) + bl * m * 0.85 + a_ * 0 , 0, 255).astype(np.uint8))
        write_frames(fr[:nfr], out); seg_list.append(out); continue
    if c.get('flash'):   # v3 플래시백: 채도 낮춤(vfx) + 가장자리 흐림·어둡게 + 처음·끝 흰 번쩍임
        vf += "setsar=1,format=rgb24,tpad=stop_mode=clone:stop_duration=2.0[v]"
        r2 = subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(c['src']), '-filter_complex', vf, '-map', '[v]', '-frames:v', str(nfr), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
        mv = np.frombuffer(r2, np.uint8).reshape(-1, H, W, 3)
        yy, xx = np.mgrid[0:H, 0:W]; rr = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
        m = np.clip((rr - 0.55) / 0.5, 0, 1)[..., None]                       # 가장자리일수록 1
        fr = []
        for i, a_ in enumerate(mv):
            bl = np.asarray(Image.fromarray(a_).resize((W // 8, H // 8), Image.BILINEAR).filter(ImageFilter.GaussianBlur(3)).resize((W, H), Image.BILINEAR), float)
            x_ = a_.astype(float) * (1 - m) + bl * m; x_ *= (1 - 0.45 * m)
            x_ = x_ * 0.92 + np.array([18, 12, 0]) * 1.0                       # 살짝 바랜 색
            lt = i / FPS; w_ = (1.0 if lt < 0.10 else max(0.0, 1 - (lt - 0.10) / 0.35) * 0.95) + max(0.0, 1 - (c['dur'] - lt) / 0.15) * 0.8   # v4: 첫 0.1초 온통 흰색 → 0.35초에 걸쳐 빠짐
            x_ = x_ * (1 - w_) + 255 * w_
            fr.append(np.clip(x_, 0, 255).astype(np.uint8))
        write_frames(fr[:nfr], out); seg_list.append(out); continue
    if c['hold']:   # 움직이는 부분만 만들고, 끝 프레임은 멈춰 천천히 다가감
        nmov = round(used * c['stretch'] * FPS)
        vf += "setsar=1,format=rgb24[v]"
        r2 = subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(c['src']), '-filter_complex', vf, '-map', '[v]', '-frames:v', str(nmov), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                            capture_output=True).stdout
        mv = np.frombuffer(r2, np.uint8).reshape(-1, H, W, 3)
        fr = list(mv) + push_frames(Image.fromarray(mv[-1]), nfr - len(mv), 0.10, 1.0)
        write_frames(fr[:nfr], out); seg_list.append(out); continue
    vf += "setsar=1,format=yuv420p,tpad=stop_mode=clone:stop_duration=2.0[v]"
    run(['ffmpeg', '-y', '-loglevel', 'error', '-i', c['src'], '-filter_complex', vf, '-map', '[v]',
         '-frames:v', nfr, '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', out])
    seg_list.append(out)
(B / 'list.txt').write_text(''.join(f"file '{p}'\n" for p in seg_list))
run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', B / 'list.txt', '-c', 'copy', B / 'joined.mp4'])

# 영혼 원 지지직(빙의 풀림 "헐!")
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
GAIN = {'HUL': 1.5}
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
k = CUTS_BY
DINGX = '0.16*sin(2*PI*1320*t)*lt(t,0.08)+0.16*sin(2*PI*1760*t)*gt(t,0.12)*lt(t,0.24)'
TAKX = '0.6*sin(2*PI*(200-90*t)*t)*exp(-40*t)+0.2*sin(2*PI*900*t)*exp(-70*t)'
DOORX = '0.6*sin(2*PI*(120-60*t)*t)*exp(-22*t)+0.2*sin(2*PI*520*t)*exp(-50*t)'
SEND = '0.18*sin(2*PI*(700+1600*t)*t)*exp(-12*t)'
BOING = '0.20*sin(2*PI*(300+500*t)*t)*exp(-6*t)'
sfx('tak', TAKX, 0.3, TAK, 0.8)
for j in range(2): sfx(f'tt{j}', '0.4*sin(2*PI*1100*t)*exp(-90*t)', 0.08, k['K2']['start'] + 1.0 + 0.25 * j, 0.5)   # 손톱 톡톡
sfx('boing', BOING, 0.4, ZOOM_T, 0.45)
noise('fbw', 0.45, k['K6f']['start'] - 0.15, 'highpass=f=1200,afade=t=in:d=0.2,afade=t=out:st=0.2:d=0.25', 0.10)   # 회상 들어갈 때 쉭
for j in range(8): noise(f'th{j}', 0.04, DM1 - 0.9 + 0.11 * j, 'bandpass=f=2500:w=1500', 0.08)        # 엄지 다다닥
sfx('send1', SEND, 0.35, DM1, 0.5)
for j in range(5): noise(f'eg{j}', 0.05, TYPE4 + 0.45 * j, 'bandpass=f=2000:w=1200', 0.10)            # 교실 폰 톡톡
for j in range(2): noise(f'sn{j}', 0.16, SNIFF + 0.22 * j, 'bandpass=f=1800:w=2400,afade=t=in:d=0.04,afade=t=out:st=0.08:d=0.08', 0.20)   # 킁킁
fc.append(f"anoisesrc=d=0.65:c=white:a=0.5:r=48000,highpass=f=1800,volume='0.13*lt(mod(t,0.04),0.02)*(0.6+0.4*sin(2*PI*57*t))':eval=frame,"
          f"afade=t=out:st=0.5:d=0.15,aformat=channel_layouts=stereo,adelay={int(GLITCH[0] * 1000)}:all=1[zap]"); mixl.append('[zap]')   # 지지직
sfx('beep', '0.25*sin(2*PI*1000*t)', 0.55, BEEP, 1.0)
sfx('thud7', TAKX, 0.3, THUD7, 0.8)
noise('sw1', 0.25, k['K8']['start'] + 0.8, 'highpass=f=2500,afade=t=in:d=0.05,afade=t=out:st=0.1:d=0.15', 0.08)
for lid in ('V08a', 'V08b', 'V09', 'V10a', 'V10b', 'V10c', 'V12a', 'V12b', 'V12c'):
    if has(lid): sfx(f's_{lid}', SEND, 0.35, end_(lid) + 0.02, 0.45)        # 보냄 "슉"
fc.append(f"anoisesrc=d=0.45:c=brown:a=0.6:r=48000,bandpass=f=700:w=500,volume='0.45*(0.6+0.4*sin(2*PI*28*t))':eval=frame,afade=t=in:d=0.05,afade=t=out:st=0.25:d=0.2,"
          f"aformat=channel_layouts=stereo,adelay={int(CHAIR * 1000)}:all=1[chair]"); mixl.append('[chair]')
sfx('door', DOORX, 0.5, DOOR, 0.9)
if (C / 'K10_elem.mp4').exists() and 'K10' in k:   # v4: 구두 또각(원본 2.1~4.5초 걸음)
    HEEL = '0.5*sin(2*PI*2600*t)*exp(-90*t)+0.35*sin(2*PI*(420-200*t)*t)*exp(-60*t)'
    for j, ts0 in enumerate(np.arange(2.1, 4.6, 0.42)):
        sfx(f'heel{j}', HEEL, 0.12, k['K10']['start'] + (ts0 - K10SS) * k['K10']['stretch'], 0.55 * (1 - 0.08 * j))
sfx('crack', '0.5*sin(2*PI*180*t)*exp(-60*t)*lt(mod(t,0.07),0.03)', 0.25, CRACK, 0.7)
fc.append(f"anoisesrc=d=0.4:c=brown:a=0.6:r=48000,bandpass=f=500:w=400,volume='0.4*(0.6+0.4*sin(2*PI*22*t))':eval=frame,afade=t=out:st=0.2:d=0.2,"
          f"aformat=channel_layouts=stereo,adelay={int((L['V13'] + 0.55) * 1000)}:all=1[chair2]"); mixl.append('[chair2]')   # 벌떡 의자
sfx('ding', DINGX, 0.3, DING, 0.5)

def amb(lbl, a, b, lo, hi, vol):
    a0 = max(0, a - 0.3)
    fc.append(f"anoisesrc=d={b - a0:.2f}:c=pink:a=0.5:r=48000,bandpass=f={(lo + hi) // 2}:w={hi - lo},volume={vol},"
              f"afade=t=in:d=0.3,afade=t=out:st={b - a0 - 0.3:.2f}:d=0.3,aformat=channel_layouts=stereo,adelay={int(a0 * 1000)}:all=1[{lbl}]")
    mixl.append(f'[{lbl}]')
for c in CUTS:
    a, b = c['start'], c['start'] + c['dur']
    if c['id'] in ('K4', 'K4b', 'KC', 'KF'): amb(f"am_{c['id']}", a, b, 500, 2500, 0.022)        # 교실
    elif c['id'] in ('K5',): amb(f"am_{c['id']}", a, b, 200, 800, 0.012)
    elif c['id'].startswith('OP') or c['id'] == 'R2': amb(f"am_{c['id']}", a, b, 300, 2800, 0.018)   # 교무실
    else: amb(f"am_{c['id']}", a, b, 250, 1200, 0.008)                                        # 상담실
fc.append(f"anoisesrc=d={MAIN}:c=brown:a=0.5:r=48000,lowpass=f=350,volume=0.0105,afade=t=in:d=0.5,afade=t=out:st={MAIN - 0.4}:d=0.4,aformat=channel_layouts=stereo[room]"); mixl.append('[room]')
# 배경음: 교무실(가벼운 펄스) → 상담 압박 → "띠용"에서 뚝 → 교실 → 향수(떨림) → "향수요?!" 직전 뚝 → 쪽지·DM(단조) → 벤치·F(단조) → "아동학대요?!"에서 뚝
# v4 배경음: 대사 없는 곳 약 -24 LUFS, 대사 아래 15dB 낮춤(돌아오는 시간 0.2초로 짧게 → 대사 사이 쉼에서 들림)
#   교무실(가벼움) → 어머니 대치 0:08~0:14(현 떨림 + 낮은 맥박) → "띠용" 뚝 → 교실 친구(펄스) → 향수 추리(미스터리) → "향수요?!" 직전 뚝
#   → 어머니 대치 0:35~0:56(현 떨림 + 맥박, 쪽지·DM 동안에도 이어짐) → 담임 DM(미스터리) → "아동학대요?!" 직전 0.4초 정적
#   → 일어나는 펄스 → 허리 삐끗(우두둑)에서 뚝 → 끝 가벼움
BGM_T = -21.0
BGM_SECT = [('class', 0.0, k['K1']['start']),
            ('confront', k['K1']['start'] + 0.15, ZOOM_T),
            ('pulse', k['K4']['start'], k['K6a']['start']),
            ('mystery', k['K6a']['start'] + 0.1, end_('E09') + 0.05),
            ('confront', L['E10a'] + 0.05, k['KF']['start']),
            ('mystery', k['KF']['start'], L['V13'] - 0.40),
            ('pulse', end_('V13') + 0.05, CRACK - 0.02),   # 짧음(일어나는 순간만)
            ('class', end_('E16b') + 0.05, MAIN)]
BGM_I = bgm.make(BGM_SECT, [(VO / f'{lid}.wav', st) for lid, st in L.items()], MAIN, B / 'bgm.wav', target_lufs=BGM_T, duck_db=-15.0, release=0.2)
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
    if x['grp'] == 'HUL':   # 빙의 풀림: 분홍 상자 번쩍
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

ev(0.0, ce('OPd'), 'Label', r'{\an7\pos(40,140)}담임과 학생, 몸이 바뀌었다', 6)
# 첫 화면 띠(0–0.6초)
ev(0.0, 0.62, 'Label', r'{\an5\pos(540,640)\bord0\shad0\1c&H000000&\1a&H28&\p1\fad(0,120)}m 0 0 l 1080 0 1080 420 0 420{\p0}', 9)
ev(0.0, 0.62, 'Label', r'{\an5\pos(540,500)\fs50\bord0\fad(0,120)}소울체인지 7화', 10)
ev(0.0, 0.62, 'Label', r'{\an5\pos(540,610)\fs62\1c&HFFFFFF&\3c&H2020D0&\4c&H2020D0&\bord12\fad(0,120)}해당 학생 어머니가 왔다', 10)
ev(0.0, 0.62, 'Emph', r'{\an5\pos(540,750)\fs96\bord6\3c&H000000&\fad(0,120)}그 욕, 어디서 배웠을까', 10)
scene(0.62, ce('OPd'), '교무실 · 교감이 김 선생(지금은 지우)에게')
say('VPa', r'김 선생, 텀블러 건\N학생 어머님 오셨어요.', '', end=end_('VPb') + 0.10, grp='VP1')                      # 첫 장면 이름표 없음
say('VPc', r'담임이 병가라,\N작년 담임인 김 선생이 좀 맡아요.', '')
say('VPd', '웃으면서, 조용히.', '')
say('E02a', '네, 네!', '')
narr(L['VPd'] + 0.3, ce('OPd'), r'(교장 되기 전에\N조용히만...)', 40, 430)
scene(cs('K1'), cs('K1') + 2.6, '상담실 · 텀블러 사건 해당 학생의 어머니')
say('E01', r'우리 아이는 아무 문제가 없어요.\N순둥이, 타고난 품격이 있는 아이라구요!' if has('E02b') else '우리 아이는 아무 문제가 없어요.', '해당 학생 어머니')
if has('E02b'):
    say('E02b', '품격... 넘치죠, 그럼요!', '지우 영혼', PINK)
    narr(L['E02b'] + 0.4, ce('K3a'), r'(일단 무조건 굽신)', 40, 430)
say('V02', r'작년에 선생님이 우리 애한테 한\N정서학대, 잊으셨어요?', '해당 학생 어머니')
say('V03', '정서학대...? 우리 쌤이?!', '(속마음) 지우 영혼', PINK, 'Mono')
ev(DM1, ce('K3b'), 'DMp', r'{\an6\pos(1000,860)\fad(80,120)}쌤!!! 정서학대래요??', 4)
ev(DM1, ce('K3b'), 'TagJ', r'{\an3\pos(1000,770)\fad(80,120)}지우가 쌤에게 · DM', 5)
scene(cs('K4'), cs('K4') + 2.2, '같은 시각 · 교실 · 지우 몸에 담임 영혼')
say('V04', '지우야, 누구랑 그렇게 열심히 톡해?', '반 친구')
say('E06', '...쉿. 어른 일이다.', '담임 영혼', SKY)
say('V05', '웬 어른? 너 요즘 이상해.', '반 친구')
narr(L['V05'] + 0.4, ce('K4b') if 'K4b' in k else ce('K4'), r'(못 들은 척)', 620, 430)
scene(cs('K6a'), cs('K6a') + 2.0, '다시 상담실')
say('V06a', '이 향수 냄새... 어디서 맡아 봤더라?', '(속마음) 지우 영혼', PINK, 'Mono')
say('V06b', '...아. 최 쌤 향수랑 똑같잖아?', '(속마음) 지우 영혼', PINK, 'Mono')
scene(cs('K6f'), ce('K6f'), '6화 · 최 쌤 자리')
say('HUL', '헐!', '지우 영혼', PINK, hold=0.25)
say('E09c', '크흠!', '지우 영혼', PINK, hold=0.05)
say('E09', r'향수가... 아주...\N고급지시네요...', '지우 영혼', PINK)
narr(L['E09'] + 0.3, ce('K6'), r'(수습 실패)', 640, 430)
say('E10a', '향수요?!', '해당 학생 어머니', hold=0.1)
say('E10c', '...갑자기 웬 향수요?', '해당 학생 어머니', hold=0.1)
say('E10b', r'애 하나 때문에 집안이 곤란한데,\N그 담임 티' + CIRC + '년!', '해당 학생 어머니', end=BEEP + 0.65)
scene(cs('K8'), ce('K8'), '6화의 쪽지 · 같은 욕')
say('V07', r'쪽지에 써 있던 거랑 똑같은 욕을 하시네...\N냄새는... 향수를 말하는 건가?', '(속마음) 지우 영혼', PINK, 'Mono')
# v3: DM 화면은 말풍선만(아래 자막·위 상황 자막 뺌) — scene
# v3: DM 화면은 말풍선만(아래 자막·위 상황 자막 뺌) — say
# v3: DM 화면은 말풍선만(아래 자막·위 상황 자막 뺌) — say
if has('V09'):
    scene(cs('KC'), ce('KC'), '교실 · 쌤이 지우에게 DM')
    say('V09', r'엄마? 엄마라니.\N그거 무슨 말이야?', '담임 영혼 · DM', SKY)
if 'KD' in k: scene(cs('KD'), ce('KD'), '탁자 밑 · 지우가 쌤에게 DM')
say('V10a', '이건 그냥 제 촉인데요.', '지우 영혼 · DM', PINK)
say('V10b', '아니, 확실해요.', '지우 영혼 · DM', PINK)
say('V10c', r'아무래도 자기 엄마에 대한\N불만을 써 둔 것 같아요.', '지우 영혼 · DM', PINK)
say('E12', '애는 엄마가 제일 잘 알아요!', '해당 학생 어머니')
say('E13', '살... 살... 살펴 가세요...', '지우 영혼', PINK)
if has('HM'):
    scene(cs('R2'), ce('R2'), '그 시각 · 교무실')
    say('HM', '흐흠...', '교감', hold=0.2)
    narr(L['HM'] + 0.2, ce('R2'), r'(조용히 끝났다고\N믿는 중)', 40, 430)
if 'K5' in k: scene(cs('K5'), ce('K5'), '교실 창밖 · 해당 학생')
say('V11', r'그럴 리가...\N그렇다면 그게 다...', '(속마음) 담임 영혼', SKY, 'Mono')
if 'K5' in k: narr(L['V11'] + 0.8, ce('K5'), r'(작년 그 일이\N떠오른다)', 40, 700)
# v3: DM 화면은 말풍선만(아래 자막·위 상황 자막 뺌) — scene
# v3: DM 화면은 말풍선만(아래 자막·위 상황 자막 뺌) — say
# v3: DM 화면은 말풍선만(아래 자막·위 상황 자막 뺌) — say
# v3: DM 화면은 말풍선만(아래 자막·위 상황 자막 뺌) — say
say('V13', '아동학대요?!', '지우 영혼', PINK, hold=0.1)
say('E16b', '아이고, 허리야...', '지우 영혼', PINK)
narr(L['E16b'] + 0.1, ce('K12'), r'(몸은 50대)', 600, 430)
# v3: DM 화면은 말풍선만(아래 자막·위 상황 자막 뺌) — scene
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
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', ENDING, '-an', '-vf', f'fps={FPS},format=yuv420p,setsar=1',
     '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', B / 'ending_v.mp4'])
(B / 'vlist.txt').write_text(f"file '{B / 'main_v.mp4'}'\nfile '{B / 'ending_v.mp4'}'\n")
out = HERE / f'ep7_{TAG_}.mp4'
run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', B / 'vlist.txt', '-i', B / 'mix.wav',
     '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-t', TOT, '-movflags', '+faststart', out])
json.dump({'main': MAIN, 'ending': END_LEN, 'total': TOT, 'loudness_LUFS': I2, 'true_peak_dBTP': TP2, 'cut_set': sorted(CUT_SET),
           'cuts': [{kk: (str(vv) if isinstance(vv, pathlib.Path) else vv) for kk, vv in c.items()} for c in CUTS],
           'lines': {lid: {'start': L[lid], 'end': round(L[lid] + D[lid], 3), 'tempo': SPEC[lid]['tempo'], 'file': SPEC[lid]['f'],
                           'range': SPEC[lid]['r'], 'inner': lid in INNER} for lid in sorted(L, key=L.get)},
           'subs': SUBS, 'glitch': GLITCH, 'bgm': BGM_SECT, 'placeholders': [c['id'] for c in CUTS if c['fx'] == 'ph']},
          open(HERE / f'timeline_{TAG_}.json', 'w'), ensure_ascii=False, indent=1)
print('OK', out, TOT, '임시 화면:', [c['id'] for c in CUTS if c['fx'] == 'ph'])
