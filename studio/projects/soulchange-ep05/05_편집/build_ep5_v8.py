#!/usr/bin/env python3
"""소울체인지 5화 「이거 갑질이잖아요」 편집 v1 (4화 build_ep4_v16.py와 같은 방식).

기준: 키트 제작규칙 v1 + soulchange_style.ass(Jua, \\fs \\fn \\i 덮어쓰기 없음) / 대본_v3 맨 위 사장님 메모 /
feedback.md 2026-10-26 "엔딩 포함 70초 이하, 으악은 빼도 돼".
- 본편 ≤ 64.3초 + 고정 엔딩 5.7초(series/엔딩/make_ending.py, 다음 화 = 화요일) ≤ 70.0초. 끝 카드 1.5초 대신 엔딩.
- V11 "으악…!" 삭제, 대사 전부 1.05배(음높이 유지 atempo, V20 앞부분만 1.1배), 줄 안의 긴 쉼 0.13초까지 줄임.
- 대사 조각 = vo_prep.py, 친구 폰 연락처 카드 = phone_card.py.
사용: python3 build_ep5_v8.py  → ep5_v8.mp4, timeline_v8.json

v8(2026-10-27 사장님 + Gemini v6/v7): 해설 자막 크게·얼굴 옆, 책상 쾅은 짧은 충격 2번(흔들림) → 지우 몸 얼굴, 교감 듣는 컷은 정지 프레임+천천히 다가감,
P2 손가락 짧게·잘라 냄, A2 "AI" 배지 잘라 냄, 일어선 뒤 앉은 그림 안 씀, "지식이 높은…" 1.13배 +2dB, 코드로 만든 긴장 배경음(bgm.py, 대사 아래 줄임).

v7(2026-10-27 사장님): K11에 해설 자막 "(들킬까 봐 괜히 버럭)" 하나 추가. 나머지는 v6와 같음.

v6(2026-10-27 사장님): K6a 옆 친구 안 보이게 1.5배, 교무실 끝 순서 바꿈(… 우리 쌤? → AI 빙의 수작 → 헐 설마 → 일어나 갑질 → 지식이 높은 … → 교감 "고지식? 허…"로 끝), 교차 편집.

v5(2026-10-27): K6a→K6b 휩 팬 + 의자·발소리(친구들이 자리를 뜸), 두 번째 헛기침(V24 b), K11 정지를 얼굴이 늘어나기 시작하는 원본 프레임 70에서
깨끗한 프레임 80으로 건너뛰며 시작(흔들림·두 번째 펀치 인·쿵은 고함에), P3 배경 흐림 훨씬 세게.

v4(2026-10-27): K11 = 새 A4(A4_K11_v2_audioref, 원본 0.25초부터) + 고함 얼굴이 늘어나기 전 프레임 80(3.333초)에서 정지·만화 효과(freeze_fx.py),
V17·V18 = 고함 테이크(1.3배·1.25배), 헛기침 = V24, 자막·Tag 어두운 상자(불투명 80%), P3(K10) 배경 흐림.

v3(Gemini 검수 v2 반려 반영, 06_검수/gemini_검수.md): 자막을 쇼츠 아래 UI(아래 27%) 위로(글자 아래끝 y≤1340),
화자 Tag를 우리 스타일(Jua 54, 화자 색 상자)로 크게, 속마음 Tag는 어두운 상자+색 글자로 구별, V03–V04 사이 0.25초,
P1b는 손 뭉개짐(원본 3.0–3.37) 뒤 첫 쾅 순간(3.40)부터, P1 뒤 C2 0.45초 다시 보여 주기,
P3는 가장 또렷한 1.9초(검지 → 손바닥)만, 나머지는 A3 뒷부분을 1.2배 당겨 씀, 위 라벨·영혼 원은 위 6%(쇼츠 위 막대) 아래로.

v2(블라인드 검수 v1 반영, 06_검수/블라인드_v1.md): 자막·Tag 위치를 \\pos로 고정(Tag는 늘 자막 덩어리 바로 위),
자막끼리 겹치지 않게, "너네!" 위 쾅 소리가 남자 목소리처럼 읽히던 것(낮은 음 sine) → 소음형 쾅 + "너네!"를 첫 쾅 뒤로,
맨 앞 1.6초 '지난 화' 한 줄 + 장소 라벨 0초부터, K10 앞 0.6초는 A3(담임 몸 정면) 연장 + Tag "지우 영혼 (담임 몸)".
"""
import json, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from vo_prep import prep

KIT = pathlib.Path('/home/user/youtube-ops/series/_soulchange_kit')
EP = HERE.parent
V = EP / '04_생성물' / 'voices'
C = EP / '04_생성물' / 'clips'
PC = KIT / 'episodes/ep5/clips'
B = HERE / 'build_v8'; B.mkdir(exist_ok=True)
B1 = HERE / 'build'   # 엔딩 영상(make_ending.py 결과)은 v1 것을 그대로 씀
VO = B / 'vo'
ENDING = pathlib.Path('/home/user/ai-studio/studio/series/엔딩')
FPS = 30
END_LEN = 5.7
MAIN_MAX = 70.0 - END_LEN


def run(cmd, **kw):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, **kw)
    if r.returncode: raise SystemExit(' '.join(map(str, cmd)) + '\n' + r.stderr[-2000:])
    return r


# ---------- 1. 대사 조각 (채택 테이크: 생성로그.md ★ / 측정.txt ★ / 대본_v2 4절) ----------
T = 1.05
G = 0.13   # 줄 안 쉼 상한(초)
SPEC = {
    'V01': dict(f='V01_교감_전화하셨어요_raw.mp3', r=[(0, 3.3)]),
    'V02': dict(f='V02_지우_네아니제가_v4_raw.mp3', r=[(0, 2.1)], gap=0.18),
    'V03': dict(f='V03_담임속_죽었다_v4_raw.mp3', r=[(0, 1.7)]),
    'V04': dict(f='V04i_담임속_아이씨_raw.mp3', r=[(0.05, 1.2)]),          # v5 사장님: 겉말 → 담임 영혼 속마음(sc_teacher_body 속삭임)
    # V05b(잘라 붙인 것)에서 두 번째 "하…"(0.70–1.40)를 빼서 "하… 지우 녀석, 하…"만
    'V05': dict(f='V05i_담임속_지우녀석_raw.mp3', r=[(0.05, 3.0)]),            # v5: 속마음
    'F1a': dict(f='F1_후보B_Chloe_raw.mp3', r=[(0, 1.65)]),
    'F1b': dict(f='F1_후보B_Chloe_raw.mp3', r=[(1.80, 3.72)]),
    'F1c': dict(f='F1_후보B_Chloe_raw.mp3', r=[(4.12, 6.92)]),
    'F2a': dict(f='F2_후보A_Pixie_raw.mp3', r=[(0, 1.72)]),
    'F2b': dict(f='F2_후보A_Pixie_raw.mp3', r=[(1.85, 4.92)]),
    'V12': dict(f='V12_담임겉_이런짓까지2_raw.mp3', r=[(0, 2.15)], gap=0.30),   # "너네!" 뒤 쉼에 두 번째 쾅
    'V22': dict(f='V22i_담임속_대리부모라니_raw.mp3', r=[(0.15, 1.75)]),        # v5: 속마음
    'V23': dict(f='V23_담임속_내알바아니지_a_raw.mp3', r=[(0.63, 3.6)]),            # 앞 한숨 0–0.63 자름
    'V13': dict(f='V13_교감_어느집딸_raw.mp3', r=[(0, 5.12)]),
    'V14': dict(f='V14_교감_인사시즌_raw.mp3', r=[(0, 6.05)]),
    'V15': dict(f='V15_지우_우리쌤기간제_raw.mp3', r=[(0, 5.8)]),
    'V16a': dict(f='V16_지우_지식이높은_a_raw.mp3', r=[(0, 1.40)]),               # "아니 참…" (K9 끝)
    'V16b': dict(f='V16_지우_지식이높은_a_raw.mp3', r=[(2.36, 7.8)], tempo=1.13),   # v8: 고함 뒤라 더 빠르고 세게(+2dB는 GAIN)             # "하." 숨소리 빼고 "지식이 높은 …"(K10)
    'V17': dict(f='V17_지우_협박_shout_a_raw.mp3', r=[(0, 1.42)], tempo=1.3),     # v4: 고함 테이크(사장님 "목소리가 차분해")
    'V18': dict(f='V18_지우_갑질_shout_a_raw.mp3', r=[(0.08, 1.62)], tempo=1.25),
    'V19a': dict(f='V19a_교감_고지식허_a_raw.mp3', r=[(0, 1.70)], gap=0.22),
    'V19b': dict(f='V19b_교감_아니우리쌤_a_raw.mp3', r=[(0.12, 1.76)]),
    'V20a': dict(f='V20_교감_AI빙의수작_b_raw.mp3', r=[(0.12, 4.63)], tempo=1.1),  # 4.58–5.13 무음에서 자름, 1.1배(대본 v3 §1-4 처리 순서 2)
    'V20b': dict(f='V20_교감_AI빙의수작_b_raw.mp3', r=[(5.08, 7.2)]),
    'V21': dict(f='V21_지우속_헐설마_raw.mp3', r=[(0, 1.74)]),                     # "헐… 설마."까지
}
for s in SPEC.values():
    s.setdefault('tempo', T); s.setdefault('gap', G)
D = prep(SPEC, V, VO)
INNER = {'V03', 'V04', 'V05', 'V22', 'V23', 'V21'}   # 속마음 = 영혼 목소리 + 잔향 (v5: V04·V05·V22 추가)

# ---------- 2. 컷과 대사 배치 ----------
# 컷: id, 원본, 원본 시작, 원본 끝, 영혼 원, 화면 길이, 확대(zoom, 가로 기준점, 세로 기준점)
# 화면 길이 / (원본 끝 - 시작) = 늘림 배율(1.15 이하)
L = {}   # 대사 id → 전체 시간 시작
CUTS = []
t = 0.0
def cut(cid, src, ss, se, pip, dur, zoom=(1.0, 0.5, 0.5), note='', still=None, push=0.12, shake=False):
    global t
    CUTS.append(dict(id=cid, src=src, ss=ss, se=se, pip=pip, start=round(t, 3), dur=round(dur, 3), zoom=zoom, note=note, still=still, push=push, shake=shake))
    t += dur
def at(lid, x):
    L[lid] = round(x, 3); return x + D[lid]

c0 = t; e = at('V01', c0 + 0.08); e = at('V02', e + 0.10)
cut('K1', C / 'A1_K1.mp4', 0, 5.04, 'pip', e + 0.08 - c0)
c0 = t; e = at('V03', c0 + 0.06); e = at('V04', e + 0.25)          # v3: 속마음과 겉말 사이 0.25초. 머리 벅벅(원본 3.25초) ≈ "아이씨"
cut('K2', PC / 'K02_P0.mp4', 1.5, None, 'pip_t', e + 0.08 - c0)
c0 = t; e = at('V05', c0 + 0.06)
# v5: V05가 속마음이 되어 입이 크게 벌어진 C1(원본 0.6초~ 찡그리며 입 벌림)은 "하…" 한숨까지만, "지우 녀석…"은 뒷모습(P0 다른 테이크, 앞으로 푹 숙임)으로
cut('K3', C / 'C1_K3.mp4', 0, 1.2, 'pip_t', 1.2, zoom=(1.1, 0.5, 0.0), note='치마 안 보이게 1.1배 위쪽 기준. v5: 입 다묾→찡그림(한숨)까지만')
cut('K3b', PC / 'K02_P0_take2.mp4', 1.0, None, 'pip_t', e + 0.08 - t, note='v5: 뒷모습(입 안 보임) — 속마음 "지우 녀석…"')
c0 = t; e = at('F1a', c0 + 0.06); e = at('F2a', e - 0.05); e = at('F1b', e + 0.02)   # 친구 둘 말이 거의 붙음
cut('K4', PC / 'K04_C2.mp4', 0, 5.04, 'pip_t', e + 0.06 - c0)
c0 = t; e = at('F1c', c0 + 0.05); e = at('F2b', e + 0.06)
cut('K5', PC / 'K05_P1.mp4', 0.6, 5.04, 'pip_t', e - 0.25 - c0, note='폰 하얀 화면에 "대리 엄마 ☎" 카드. v3: 팔이 어깨에 감기는 앞 0.6초를 빼고 "가자!"에서 컷')
cut('K5b', PC / 'K04_C2.mp4', 0.95, 1.60, 'pip_t', 0.65, note='v3: P1→P1b 사이 지우 몸 얼굴 반응(입 다묾, 친구 둘 올려다봄) 0.65초, F2b 끝이 걸침')
# K6a v8 사장님("책상 쾅이 어색"): 쾅을 짧은 충격 2번(각 0.3초, 1.5배·흔들림)만 보이고 바로 지우 몸 얼굴(C1, 말하는 입)로
c0 = t
SLAM = [c0 + 0.02, c0 + 0.37]
e = at('V12', SLAM[0] + 0.13)                                       # "너네!"는 쾅 두 번 위, "이런 짓까지 해?"는 얼굴 위
cut('K6a', PC / 'K06a_P1b.mp4', 3.40, 3.75, 'pip_t', 0.35, zoom=(1.5, 0.3, 0.75), shake=True, note='v8: 첫 쾅 0.35초, 1.5배(옆 친구 안 보임), 흔들림')
cut('K6a2', PC / 'K06a_P1b.mp4', 3.98, 4.28, 'pip_t', 0.30, zoom=(1.6, 0.35, 0.8), shake=True, note='v8: 둘째 쾅 0.3초, 1.6배, 흔들림')
cut('K6r', C / 'C1_K3.mp4', 2.5, None, 'pip_t', e + 0.05 - t, zoom=(1.1, 0.5, 0.0), note='v8: 지우 몸 얼굴(찡그리며 말함) — "이런 짓까지 해?", 친구 없음')
# K6b: C3 전체, ×1.06. 머리 감싼 채 "대리 부모라니…" → 원본 약 3.1초 털썩 → 속마음
k6b_st = 1.06; c0 = t
e = max(e + 0.05, c0 + 0.25); e = at('V22', e)
FLOP = c0 + 3.1 * k6b_st
e = at('V23', FLOP - 0.45)
cut('K6b', C / 'C3_K6b.mp4', 0, 5.04, 'pip_t', max(5.04 * k6b_st, e + 0.06 - c0), zoom=(1.2, 0.5, 0.0), note='책상 아래 치마 안 보이게 1.2배 위쪽 기준')
c0 = t; e = at('V13', c0 + 0.08)
cut('K7', C / 'A2_K7_교감어느집딸.mp4', 0, None, 'pip', e + 0.08 - c0, zoom=(1.1, 1.0, 1.0), note='v8: 왼쪽 위 Dreamina/Higgsfield "AI" 배지 → 1.1배, 오른쪽 아래 기준으로 잘라 냄')
c0 = t; e = at('V14', c0 + 0.06)
# v8 Gemini: P2 손가락이 길고 일그러짐 → 짧게, 서류철 쪽(왼쪽 아래)으로 1.45배 잘라 손가락 마디를 화면 가장자리로. 사이에 듣는 담임 몸(A1 앞부분, 입 다묾)
cut('K8', PC / 'K08_P2.mp4', 1.5, 2.3, 'pip', 0.85, zoom=(1.45, 0.0, 0.85), note='v8: 서류철 톡톡 — 짧게, 서류철 쪽으로 잘라 손가락 마디 덜 보이게')
cut('K8l', C / 'A1_K1.mp4', 0.2, 2.6, 'pip', 2.5, zoom=(1.3, 0.9, 0.0), note='v8: 듣는 담임 몸(입 다묾, 눈만 굴림) — "기간제 연장" 교감 화면 밖. 교감 손·폰은 잘라 냄')
cut('K8c', PC / 'K08_P2.mp4', 3.25, 5.04, 'pip', e + 0.06 - t, zoom=(1.3, 0.0, 1.0), note='v8: 서류철을 미는 손 — 서류철 쪽으로 잘라 냄')
# v6 사장님 순서(교차 편집으로 입 모양 가리기):
#  교감 협박(V14) → 지우 "아니, 하은이 집이 뭐… 왜요? 그리고… 우리 쌤이 기간제였어요?" → 교감 "…아니, 우리 쌤?" → 교감 "김 선생, … 수작인가요?"
#  → 지우 영혼 속마음 "헐… 설마." → 담임 몸 일어나 "왜 협박을 해요? 이거 갑질이잖아요!"(정지) → "지식이 높은 … 단가요?" → 교감 "고지식? 허…"(끝, 정적) → 엔딩
k12a_st = 1.15
c0 = t; e = at('V15', c0 + 0.06)
# A3 첫 0.75초는 입 다문 채 눈 깜빡임 → "아니, 하은이…" 첫머리는 듣는 교감(A5a 2.45–3.15, 입 다묾)
cut('K8b', C / 'A5a_K12a_교감끝훅.mp4', 2.6, None, 'pip', 0.8, zoom=(1.0, 0.55, 0.35), still=2.6, note='v8: 듣는 교감 — 입 다문 프레임 정지 + 눈 쪽으로 천천히 다가감')
cut('K9', C / 'A3_K9_기간제였어요.mp4', 0.75, None, 'pip', e + 0.12 - t, note='담임 몸(지우 영혼) 말하는 입')
c0 = t
e = at('V19b', c0 + 0.15)
cut('K12g', C / 'A5a_K12a_교감끝훅.mp4', 1.3, 2.4, 'pip', 1.1 * k12a_st, note='교감 안경 올림 — "…아니, 우리 쌤?"')
e = at('V20a', e + 0.08)
# 교감 입이 다문 원본 2.25–3.35는 듣는 담임 몸(A3 첫 0.95초, 입 다묾)으로, 원본 5.5~(입 다묾)은 K12b로 일찍 넘김
cut('K12r', C / 'A3_K9_기간제였어요.mp4', 0.0, 0.95, 'pip', 0.95 * k12a_st, note='듣는 담임 몸(입 다묾) — "쌤?" 끝 + "김 선생," 화면 밖')
cut('K12a2', C / 'A5a_K12a_교감끝훅.mp4', 3.35, 5.5, 'pip', 2.15 * k12a_st, note='교감 입 움직이는 구간만 — "요새 몸 바뀌는 AI 빙의…"')
c0 = t; e = at('V20b', e + 0.12); e = at('V21', e + 0.12); DUNG = e + 0.02
cut('K12b', PC / 'K12b.mp4', 0, None, 'pip', e + 0.25 - c0, zoom=(1.12, 0.65, 0.35), note='담임 몸 "헉" → 입 막음(교감 화면 밖 "수작인가요?" + 속마음 "헐… 설마."). AI 배지 없애려고 1.12배')
# K11: 새 A4 원본 0.5초부터, 원본 프레임 69까지 실제 영상 → 깨끗한 프레임 80으로 건너뛰어 정지
K11_SS, FREEZE_N = 0.5, 80
DEFORM_N = 70
K11_LIVE_FR = int((DEFORM_N / 24 - K11_SS) * FPS)
c0 = t; CHAIR = c0 + 0.03
FREEZE_AT = c0 + K11_LIVE_FR / FPS
e = at('V17', c0 + (1.125 - K11_SS))                            # 입이 처음 'O'로 벌어지는 원본 1.125초
e = at('V18', FREEZE_AT + 0.35 - 0.50)                          # "갑질이잖아요!" 큰 소리가 번쩍 0.35초 뒤 흔들림에
SHOUT_AT = L['V18'] + 0.50
HUSH = L['V18'] + D['V18']
K11_DUR = HUSH + 0.03 - c0
cut('K11', C / 'A4_K11_v2_audioref.mp4', K11_SS, K11_SS + K11_DUR, 'pip', K11_DUR, note='새 A4 원본 0.5초부터, 프레임 69까지 → 깨끗한 프레임 80으로 건너뛰어 정지 + 번쩍·펀치 인, 고함에 흔들림·집중선')
# v8 Gemini: 일어선 뒤 앉은 그림 금지 → "지식이 높은 …" = 듣는 교감(정지) → 선 담임 몸(A4 v2 허리에 손) → 듣는 교감(A2 정지) → 선 담임 몸(A4 옛 컷, 낮은 각도 넓게)
_f = 1.05 / SPEC['V16b']['tempo']                                 # 낱말 시간(1.05배 기준) → 이번 배속
c0 = t; e = at('V16b', c0 + 0.12)
cut('K16a', C / 'A5a_K12a_교감끝훅.mp4', 5.9, None, 'pip', 0.12 + 0.80 * _f, zoom=(1.0, 0.55, 0.35), still=5.9, note='v8: 듣는 교감 굳은 얼굴(정지+다가감) — "지식이 높은" 화면 밖')
cut('K16b', C / 'A4_K11_v2_audioref.mp4', 1.55, None, 'pip', L['V16b'] + 2.50 * _f - 0.10 - t, zoom=(1.15, 0.5, 0.2), note='v8: 선 담임 몸, 허리에 손 — "고지식하신 교감쌤께서,"')
cut('K16c', C / 'A2_K7_교감어느집딸.mp4', 0.1, None, 'pip', 0.70, zoom=(1.1, 1.0, 1.0), still=0.1, note='v8: 듣는 교감(A2 첫 프레임 정지+다가감, AI 배지 잘라 냄) — "무섭기까지" 첫머리')
cut('K16d', C / 'A4_K11_사이다.mp4', 2.4, None, 'pip', e + 0.10 - t, zoom=(1.1, 0.5, 0.3), note='v8: 선 담임 몸(옛 A4 낮은 각도, 허리에 손, 말하는 입) — "…하면 단가요?"')
# 끝: 교감 "고지식? 허…" + 어이없는 얼굴, 짧은 정적 → 엔딩
c0 = t; e = at('V19a', c0 + 0.25)
cut('Kend', C / 'A5a_K12a_교감끝훅.mp4', 0, 0.98, 'pip', 0.98 * k12a_st, note='교감 "고지식?"(원본 0–0.6 말하는 입) · "허…"(입 오므림). 원본 1.0초~ 안경 올리기는 앞 K12g와 겹쳐 안 씀 → 마지막 프레임을 천천히 다가가며 정적')
END_HOLD = max(0.0, e + 0.60 - t)                               # "허…" 뒤 정적 약 0.6초: 마지막 프레임에서 천천히 다가감
if END_HOLD > 0:
    CUTS[-1]['dur'] = round(CUTS[-1]['dur'] + END_HOLD, 3); CUTS[-1]['hold'] = END_HOLD; t += END_HOLD
MAIN = round(t, 3)
TOT = round(MAIN + END_LEN, 3)
print('본편', MAIN, '합계', TOT)
for c in CUTS:
    if c.get('still') is not None:
        c['se'] = c['ss']; c['stretch'] = 1.0
        print(f"  {c['id']:5s} {c['start']:6.2f} +{c['dur']:.2f}  정지 프레임 {c['still']}"); continue
    used = (c['se'] - c['ss']) if c['se'] else c['dur'] - c.get('hold', 0)
    c['stretch'] = round((c['dur'] - c.get('hold', 0)) / used, 3)
    if c['se'] is None: c['se'] = round(c['ss'] + c['dur'], 3)
    print(f"  {c['id']:5s} {c['start']:6.2f} +{c['dur']:.2f}  src {c['ss']}-{c['se']} x{c['stretch']}")
    assert c['stretch'] <= 1.151, c
assert MAIN <= MAIN_MAX + 1e-6, f'본편 {MAIN} > {MAIN_MAX}'

# ---------- 3. 영상 조각 ----------
seg_list = []
for c in CUTS:
    out = B / f"seg_{c['id']}.mp4"
    z, ax, ay = c['zoom']
    used = c['se'] - c['ss']
    if c.get('still') is not None:   # v8: 정지 프레임 + 천천히 다가감(입이 움직이지 않는 듣는 컷)
        nfr = round(c['dur'] * FPS)
        vf = (f"[0:v]trim=start={c['still']}:duration=0.1,setpts=PTS-STARTPTS,fps={FPS},"
              f"scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,")
        if z != 1.0:
            sw, sh = int(round(1080 * z / 2) * 2), int(round(1920 * z / 2) * 2)
            vf += f"scale={sw}:{sh}:flags=lanczos,crop=1080:1920:{int((sw - 1080) * ax)}:{int((sh - 1920) * ay)},"
        fx, fy = (ax, ay) if z == 1.0 else (0.55, 0.35)
        vf += (f"tpad=stop_mode=clone:stop_duration={c['dur'] + 0.3:.2f},zoompan=z='1+{c['push']}*on/{nfr}':"
               f"x='iw*{fx}-(iw/zoom*{fx})':y='ih*{fy}-(ih/zoom*{fy})':d=1:s=1080x1920:fps={FPS},setsar=1,format=yuv420p[v]")
        run(['ffmpeg', '-y', '-loglevel', 'error', '-i', c['src'], '-filter_complex', vf, '-map', '[v]',
             '-frames:v', nfr, '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', out])
        seg_list.append(out); continue
    vf = (f"[0:v]trim=start={c['ss']}:duration={used:.3f},setpts=(PTS-STARTPTS)*{c['stretch']},fps={FPS},"
          f"scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,")
    if z != 1.0:
        sw, sh = int(round(1080 * z / 2) * 2), int(round(1920 * z / 2) * 2)
        vf += f"scale={sw}:{sh}:flags=lanczos,crop=1080:1920:{int((sw - 1080) * ax)}:{int((sh - 1920) * ay)},"
    if c.get('shake'):   # v8: 쾅 충격 — 처음 0.25초 크게 흔들리고 잦아듦
        vf += "crop=1000:1778:x='40+36*sin(t*95)*exp(-t*9)':y='71+36*cos(t*83)*exp(-t*9)',scale=1080:1920:flags=lanczos,"
    if c['id'] == 'K10':   # v4: 뒤 선생님들이 멈춰 보임 → 앞쪽(담임 몸 뒤통수·손, 화면 오른쪽 가운데)만 또렷하게, 나머지 흐림
        # v5: 훨씬 세게(σ 9→24) + 또렷한 곳을 앞쪽 담임 몸(오른쪽 아래 타원: 뒤통수·몸·들어 올린 팔)으로 좁힘, 뒤 선생님 셋은 완전히 흐림
        # v5: 뒤 선생님 셋은 화면 왼쪽 0.15~0.5, 치켜든 검지·뒤통수는 0.55~1.0 → 가로 경계(0.48~0.58)로 왼쪽을 σ 24로 흐림
        # v5: 뒤 선생님 셋(화면 0.15~0.65, 높이 0.3~0.45)이 손 바로 뒤라 가로 경계로는 손까지 흐려짐 →
        # 또렷한 곳 = 치켜든 손(0.43,0.44) 타원 ∪ 뒤통수(0.86,0.42) 타원 ∪ 오른쪽 아래 팔·몸, 나머지 σ 24
        _s1 = "clip((1-pow((X-0.43*W)/(0.11*W),2)-pow((Y-0.44*H)/(0.09*H),2))/0.3,0,1)"
        _s2 = "clip((1-pow((X-0.86*W)/(0.20*W),2)-pow((Y-0.42*H)/(0.20*H),2))/0.3,0,1)"
        _s3 = "clip((Y-0.55*H)/(0.06*H),0,1)*clip((X-0.45*W)/(0.10*W),0,1)"
        vf += ("split[sa][sb];[sb]gblur=sigma=24,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':"
               f"a='255*(1-max({_s1},max({_s2},{_s3})))'[sbl];[sa][sbl]overlay,")
    if c.get('hold'):   # v6: 끝 컷 — 마지막 프레임을 늘리고 컷 전체를 천천히 다가감(1.0→1.08)
        vf += f"tpad=stop_mode=clone:stop_duration={c['hold'] + 0.2:.2f},zoompan=z='1+0.08*on/{round(c['dur'] * FPS)}':x='iw/2-(iw/zoom/2)':y='ih*0.4-(ih/zoom*0.4)':d=1:s=1080x1920:fps={FPS},"
    vf += "setsar=1,format=yuv420p,tpad=stop_mode=clone:stop_duration=0.5[v]"
    run(['ffmpeg', '-y', '-loglevel', 'error', '-i', c['src'], '-filter_complex', vf, '-map', '[v]',
         '-frames:v', round(c['dur'] * FPS), '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', out])
    if c['id'] == 'K11':   # v4: 정지 전까지만 실제 프레임, 그 뒤는 freeze_fx.py
        live = B / 'seg_K11_live.mp4'
        run(['ffmpeg', '-y', '-loglevel', 'error', '-i', out, '-frames:v', K11_LIVE_FR, '-c', 'copy', live])
        nf = round(c['dur'] * FPS) - K11_LIVE_FR
        run(['python3', HERE / 'freeze_fx2.py', live, c['src'], FREEZE_N, nf, 580, 470, 300, B / 'seg_K11_fx.mp4', f'{SHOUT_AT - FREEZE_AT:.3f}']); out = B / 'seg_K11_fx.mp4'
    if c['id'] == 'K5':   # v5: K6a는 폰이 이미 빠진 뒤라 카드 합성 안 함(책상 반사광을 화면으로 잘못 잡아 카드가 붙던 것 고침)
        run(['python3', HERE / 'phone_card.py', out, B / f"seg_{c['id']}_card.mp4"]); out = B / f"seg_{c['id']}_card.mp4"
    seg_list.append(out)
# v5: K6a → K6b 휩 팬(앞 4프레임 + 뒤 5프레임, 길이 그대로)
ia, ib = [c['id'] for c in CUTS].index('K6r'), [c['id'] for c in CUTS].index('K6b')
run(['python3', HERE / 'whip.py', seg_list[ia], seg_list[ib], 4, 5, B / 'seg_K6a_w.mp4', B / 'seg_K6b_w.mp4'])
seg_list[ia], seg_list[ib] = B / 'seg_K6a_w.mp4', B / 'seg_K6b_w.mp4'   # (파일 이름은 v5 그대로, 앞 컷 = K6r)
WHIP_AT = k6b_start = CUTS[ib]['start']
(B / 'list.txt').write_text(''.join(f"file '{p}'\n" for p in seg_list))
run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', B / 'list.txt', '-c', 'copy', B / 'joined.mp4'])

# ---------- 4. 소리 ----------
HALL = 'aecho=0.85:0.6:45:0.12'
def meas_I(p):
    m = subprocess.run(['ffmpeg', '-i', str(p), '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', m)[-1])
GAIN = {'V19b': 2.0, 'V19a': 1.0, 'V16b': 2.0}   # 끝 훅 "…아니, 우리 쌤?" 또렷하게(대본 v3 §1-4)
ins, fc, mixl = [], [], []
for i, (lid, st) in enumerate(sorted(L.items(), key=lambda kv: kv[1])):
    ins += ['-i', VO / f'{lid}.wav']
    ch = f"[{i}:a]aresample=48000,aformat=channel_layouts=mono"
    if lid in INNER: ch += f",{HALL}"
    ch += ",acompressor=threshold=-20dB:ratio=3:attack=5:release=120"
    if lid in GAIN: ch += f",volume={GAIN[lid]}dB"
    ch += f",aformat=channel_layouts=stereo,adelay={int(st * 1000)}:all=1[v{i}]"
    fc.append(ch); mixl.append(f'[v{i}]')
NV = len(ins) // 2

def sfx(lbl, expr, d, at_, vol=1.0):
    fc.append(f"aevalsrc='{expr}':d={d}:s=48000,volume={vol},aformat=channel_layouts=stereo,adelay={int(at_ * 1000)}:all=1[{lbl}]")
    mixl.append(f'[{lbl}]')
BUZZ = '0.18*sin(2*PI*150*t)*(0.5+0.5*sin(2*PI*25*t))*lt(mod(t,0.5),0.35)'          # 폰 진동 "부르르"
DING = '0.22*sin(2*PI*1320*t)*lt(t,0.08)+0.22*sin(2*PI*1760*t)*gt(t,0.12)*lt(t,0.22)'   # "띠링"
BANG = None   # v2: 책상 "쾅"은 아래 소음 버스트(낮은 sine은 받아쓰기·음높이에서 남자 목소리로 읽힘)
FLOPS = '0.6*sin(2*PI*(80-40*t)*t)*exp(-10*t)'                                          # 엎드리는 "털썩"
TAP = '0.25*sin(2*PI*900*t)*exp(-60*t)'                                                 # 손가락 "톡"
DUNGX = '0.35*sin(2*PI*(58+8*t)*t)*exp(-1.6*t)'                                         # 낮은 "둥"
THUD = '0.5*sin(2*PI*(90-50*t)*t)*exp(-9*t)'                                            # "쿵"
k = {c['id']: c for c in CUTS}
sfx('buzz', BUZZ, 1.0, 0.0, 0.5)
k5 = k['K5']; PHONE_IN = k5['start'] + (2.85 - k5['ss']) * k5['stretch']    # 폰이 화면에 들어오는 순간(원본 약 2.85초)
sfx('ding', DING, 0.3, PHONE_IN, 0.6)
# v3 사장님: C2 지우 몸 주먹 헛기침(원본 약 2.9초)에 "크흠, 흠" — sc_student_body 헛기침 녹음이 없어 임시로 만듦:
# "크" = 짧은 띠 소음, "흠" = 쓰지 않는 V11(으악, sc_student_body) 앞 '으' 0.22–0.42초를 낮은 통과로 막힌 소리처럼. 【임시 — 사장님 녹음으로 바꿀 자리】
COUGH_AT = k['K4']['start'] + 2.9 * k['K4']['stretch']
# v4: 임시 소리 대신 사장님 녹음 V24_지우몸_헛기침_raw.mp3(0.65초). 대사보다 약 4dB 작게(-22 LUFS 근처).
ins += ['-i', V / 'V24_지우몸_헛기침_raw.mp3']; ci = len(ins) // 2 - 1
_ci = meas_I(V / 'V24_지우몸_헛기침_raw.mp3')
fc.append(f"[{ci}:a]aresample=48000,aformat=channel_layouts=mono,volume={-22.0 - _ci:.2f}dB,aformat=channel_layouts=stereo,adelay={int(COUGH_AT * 1000)}:all=1[cough]"); mixl.append('[cough]')
# v5: 두 번째 헛기침 — C2 원본 3.46–3.62초 머리가 꾸벅 숙여지는 움직임(프레임 차이 최대 7.4, 첫 기침 2.96초 다음 큰 움직임)에 V24 b(다른 테이크, 소리 0.06초부터)
COUGH2_AT = k['K4']['start'] + (3.48 - 0.06) * k['K4']['stretch']
ins += ['-i', V / 'V24_지우몸_헛기침_b_raw.mp3']; ci2 = len(ins) // 2 - 1
_ci2 = meas_I(V / 'V24_지우몸_헛기침_b_raw.mp3')
fc.append(f"[{ci2}:a]aresample=48000,aformat=channel_layouts=mono,volume={-22.0 - _ci2:.2f}dB,aformat=channel_layouts=stereo,adelay={int(COUGH2_AT * 1000)}:all=1[cough2]"); mixl.append('[cough2]')
# v5: 친구들이 자리를 뜸 — 의자 끄는 소리 + 휩 "휙" + 멀어지는 발소리 4번
fc.append(f"anoisesrc=d=0.45:c=brown:a=0.6:r=48000,bandpass=f=700:w=500,volume='0.45*(0.6+0.4*sin(2*PI*28*t))':eval=frame,afade=t=in:d=0.05,afade=t=out:st=0.25:d=0.2,"
          f"aformat=channel_layouts=stereo,adelay={int((WHIP_AT - 0.30) * 1000)}:all=1[chair2]"); mixl.append('[chair2]')
fc.append(f"anoisesrc=d=0.3:c=pink:a=0.5:r=48000,highpass=f=800,lowpass=f=5000,afade=t=in:d=0.12,afade=t=out:st=0.12:d=0.18,volume=0.35,"
          f"aformat=channel_layouts=stereo,adelay={int((WHIP_AT - 0.14) * 1000)}:all=1[whoosh]"); mixl.append('[whoosh]')
for j in range(4):
    sfx(f'step{j}', '0.6*sin(2*PI*(140-60*t)*t)*exp(-30*t)', 0.12, WHIP_AT + 0.05 + 0.24 * j, 0.32 * (1 - 0.2 * j))
for j, x in enumerate(SLAM):
    fc.append(f"anoisesrc=d=0.35:c=brown:a=0.9:r=48000,lowpass=f=900,highpass=f=60,afade=t=out:st=0.02:d=0.3:curve=exp,volume=1.6,"
              f"aformat=channel_layouts=stereo,adelay={int(x * 1000)}:all=1[bang{j}]"); mixl.append(f'[bang{j}]')
sfx('flop', FLOPS, 0.5, FLOP, 0.7)
k8 = k['K8']
for j, x in enumerate([1.45, 1.95]): sfx(f'tap{j}', TAP, 0.15, k8['start'] + x * k8['stretch'], 0.6)
sfx('dung1', DUNGX, 1.2, L['V14'] + 1.45, 0.45)      # "기간제" 무렵
fc.append(f"anoisesrc=d=0.6:c=brown:a=0.5:r=48000,bandpass=f=600:w=500,volume='0.5*lt(mod(t,0.05),0.03)':eval=frame,"
          f"afade=t=out:st=0.3:d=0.3,aformat=channel_layouts=stereo,adelay={int(CHAIR * 1000)}:all=1[chair]"); mixl.append('[chair]')
sfx('thud', THUD, 0.5, SHOUT_AT, 0.9)   # v5: "쿵"은 고함(흔들림) 순간에
sfx('dung2', DUNGX, 1.2, DUNG, 0.5)

def amb(lbl, a, b, lo, hi, vol):
    a0 = max(0, a - 0.3)
    fc.append(f"anoisesrc=d={b - a0:.2f}:c=pink:a=0.5:r=48000,bandpass=f={(lo + hi) // 2}:w={hi - lo},volume={vol},"
              f"afade=t=in:d=0.3,afade=t=out:st={b - a0 - 0.3:.2f}:d=0.3,aformat=channel_layouts=stereo,adelay={int(a0 * 1000)}:all=1[{lbl}]")
    mixl.append(f'[{lbl}]')
CLASS = {'K2', 'K3', 'K3b', 'K4', 'K5', 'K5b', 'K6a', 'K6a2', 'K6r', 'K6b'}
for c in CUTS:
    a, b = c['start'], c['start'] + c['dur']
    if c['id'] == 'K11': b = HUSH + 0.05            # "갑질이잖아요!" 끝에 웅성 뚝 → 정적
    if c['id'] in ('K16a', 'K16b', 'K16c', 'K16d', 'Kend'): continue   # 정적(고함 뒤부터 끝까지)
    if c['id'] in CLASS: amb(f"am_{c['id']}", a, b, 500, 2500, 0.022)
    else: amb(f"am_{c['id']}", a, b, 300, 2800, 0.018)
# 룸톤(약 30%): 낮은 웅웅거림을 본편 내내
fc.append(f"anoisesrc=d={MAIN}:c=brown:a=0.5:r=48000,lowpass=f=350,volume=0.0105,afade=t=in:d=0.5,afade=t=out:st={MAIN - 0.4}:d=0.4,aformat=channel_layouts=stereo[room]"); mixl.append('[room]')
# v8: 코드로 만든 배경음(bgm.py) — 교실 가벼운 펄스(작게) / 교감 압박 긴장(똑딱·드론) → "기간제였어요?" 끝에서 뚝 → AI 빙의 의심·"헐… 설마" 더 긴장 → 고함 정지 순간 뚝 → 끝까지 정적
import bgm
BGM_SECT = [('class', k['K4']['start'], SLAM[0]),
            ('tense', k['K7']['start'], L['V15'] + D['V15'] + 0.05),
            ('tense2', L['V20a'], FREEZE_AT)]
BGM_I = bgm.make(BGM_SECT, [(VO / f'{lid}.wav', st) for lid, st in L.items()], MAIN, B / 'bgm.wav', target_lufs=-28.0)
print('bgm 덕킹 뒤 통합 음량', BGM_I)
ins += ['-i', B / 'bgm.wav']; mixl.append(f'[{len(ins) // 2 - 1}:a]')
fc.append(''.join(mixl) + f"amix=inputs={len(mixl)}:normalize=0,apad=whole_dur={MAIN},atrim=0:{MAIN}[aout]")
run(['ffmpeg', '-y', '-loglevel', 'error', *ins, '-filter_complex', ';'.join(fc), '-map', '[aout]', '-ar', '48000', B / 'mix_raw.wav'])

def meas(p):
    m = subprocess.run(['ffmpeg', '-i', str(p), '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', m)[-1]), float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', m)[-1])
# 2단계 음량(실시간 loudnorm 안 씀): 본편을 재고 고정 게인 + 리미터 → 엔딩(-13.8 LUFS, 그대로) 이어 붙임 → 전체 다시 재서 미세 게인
I0, _ = meas(B / 'mix_raw.wav')
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', B / 'mix_raw.wav', '-af',
     f'volume={-14.0 - I0:.2f}dB,alimiter=limit=0.58:level=false:attack=2:release=60', '-ar', '48000', B / 'mix_main.wav'])
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', B1 / 'ending_ep5.mp4', '-vn', '-ar', '48000', '-ac', '2', B / 'ending.wav'])
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', B / 'mix_main.wav', '-i', B / 'ending.wav', '-filter_complex',
     '[0:a][1:a]concat=n=2:v=0:a=1[a]', '-map', '[a]', '-ar', '48000', B / 'mix_full_raw.wav'])
I1, _ = meas(B / 'mix_full_raw.wav')
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', B / 'mix_full_raw.wav', '-af',
     f'volume={-14.0 - I1:.2f}dB,alimiter=limit=0.58:level=false:attack=2:release=60', '-ar', '48000', B / 'mix.wav'])
I2, TP2 = meas(B / 'mix.wav')
print('loudness', I2, 'TP', TP2)

# ---------- 5. 자막 ----------
def words(lid):
    """처리된 대사 파일의 낱말 시간(faster-whisper small int8, float32 배열)."""
    cache = B / 'words.json'
    db = json.loads(cache.read_text()) if cache.exists() else {}
    key = f"{lid}:{D[lid]}"
    if key not in db:
        import numpy as np
        from faster_whisper import WhisperModel
        global _WM
        if '_WM' not in globals(): _WM = WhisperModel('small', device='cpu', compute_type='int8')
        a = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', str(VO / f'{lid}.wav'), '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'],
                                         capture_output=True).stdout, np.float32)
        segs, _ = _WM.transcribe(a, language='ko', word_timestamps=True, beam_size=5)
        db[key] = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]
        cache.write_text(json.dumps(db, ensure_ascii=False))
    return db[key]

def dip(lid, x, before=0.35, after=0.10):
    """받아쓰기 낱말 시작(x) 앞뒤에서 소리가 가장 작은 10ms 자리 = 실제 낱말 경계(whisper 낱말 시간은 0.3초쯤 흔들림)."""
    import numpy as np
    a = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', str(VO / f'{lid}.wav'), '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'],
                                     capture_output=True).stdout, np.float32)
    h = 160; n = len(a) // h; r = np.sqrt((a[:n * h].reshape(n, h) ** 2).mean(1))
    i0, i1 = max(0, int((x - before) * 100)), min(n, int((x + after) * 100) + 1)
    return round((i0 + int(np.argmin(r[i0:i1]))) / 100 + 0.01, 3)

def split_at(lid, word, default):
    if isinstance(word, float): return word   # 직접 잰 경계(소리 크기 골짜기 + 짧은 구간 받아쓰기로 확인)
    for w, s, _ in words(lid):
        if w.startswith(word): return dip(lid, s)
    print('  ! 낱말 못 찾음', lid, word, '→ 기본값', default); return default

def ts(x):
    h, m = int(x // 3600), int(x % 3600 // 60); s = x % 60
    return f"{h}:{m:02d}:{s:05.2f}"
PINK, SKY = r'{\c&HC88CFF&}', r'{\c&HFFC88C&}'
TAGSTYLE = {(PINK, False): 'TagJ', (SKY, False): 'TagT', ('', False): 'TagW', (PINK, True): 'TagJi', (SKY, True): 'TagTi', ('', True): 'TagW'}
EV = []
def ev(a, b, style, text, layer=1):
    EV.append(f"Dialogue: {layer},{ts(a)},{ts(b)},{style},,0,0,0,,{text}")
PEND = []   # v2: 대사 자막을 모았다가 겹침을 없앤 뒤 쓴다
def line(a, b, text, tag, col='', style='Dlg', fin=60, fout=100, grp=None):
    PEND.append(dict(a=a, b=b, text=text, tag=tag, col=col, style=style, fin=fin, fout=fout, grp=grp))
def emit(a, b, text, tag, col='', style='Dlg', fin=60, fout=100, grp=None):
    # v2: 자막과 Tag 모두 \pos로 고정(libass 충돌 회피가 자리를 옮기지 못하게). 자막 아래끝 y=1400,
    # 글자 위끝 = 한 줄 1342 / 두 줄 1280(실측) → Tag 아래끝을 그 바로 위(1338 / 1276)에 둔다.
    fad = rf'\fad({fin},{fout})'
    # v3: 글자 아래끝 y≈1340(쇼츠 아래 UI 27% 위). 실측 글자 위끝 한 줄 1294 / 두 줄 1232,
    # Tag(Jua 54 상자) 아래끝을 그 위 8px에 → \pos y = 위끝 - 16
    # v4: 대사도 어두운 상자(DlgB/MonoB, 불투명 80%). 상자 아래끝 1339(실측), 위끝 한 줄 1257 / 두 줄 1195 → Tag 상자 아래끝을 그 6px 위에
    ev(a, b, style + 'B', r'{\an2\pos(540,1330)' + fad + '}' + text, 2)
    ty = 1181 if r'\N' in text else 1243
    ts_ = TAGSTYLE[(col, style == 'Mono')]
    ev(a, b, ts_, rf"{{\an2\pos(540,{ty}){fad}}}{tag}", 3)
SUBS = []   # 받아쓰기 비교용 (시작, 끝, 글)
def say(lid, parts, tag, col='', style='Dlg', hold=0.15, end=None, delay=0.0):
    """parts = [(자막 글, 이 조각이 시작하는 낱말 or None)]. 자막은 소리 시작~끝(+hold)."""
    a0 = L[lid] + delay; b0 = L[lid] + D[lid]
    starts = [a0 + (0 if pt[1] is None else split_at(lid, pt[1], pt[2] if len(pt) > 2 else 0)) for pt in parts]
    for j, (txt, *_) in enumerate(parts):
        a = starts[j] if j else a0
        b = starts[j + 1] if j + 1 < len(parts) else (end if end else b0 + hold)
        line(a, b, txt, tag, col, style, fin=60 if j == 0 else 0, fout=100 if j == len(parts) - 1 else 0, grp=lid)
        SUBS.append((round(a, 2), round(b, 2), txt.replace(r'\N', ' ')))

k1 = k['K1']
ev(0.0, k1['dur'], 'Label', r'{\an7\pos(40,140)}담임과 학생, 몸이 바뀌었다', 6)
ev(0.0, k1['dur'], 'Scene', r'{\an7\pos(40,240)}교무실 · 담임 몸에 지우 영혼', 6)   # v2: 0초부터
# v3: 지난 화 한 줄(1.6초). 얼굴(y≈200~650) 아래, 첫 대사 Tag(y≈1145~) 위 = 가슴 높이
ev(0.0, 1.6, 'Label', r'{\an8\pos(540,990)\fad(0,150)}지난 화 · 담임 몸의 지우가 하은 엄마에게\N"일본에선 다 나은 것 같던데요?^^"', 6)
say('V01', [(r'하은이 어머니가\N방금 나한테 전화하셨어요.', None)], '교감')
say('V02', [('네? 아니… 제가…', None)], '지우 영혼', PINK)
k2 = k['K2']
ev(k2['start'], k2['start'] + 2.4, 'Scene', r'{\an7\pos(40,240)}같은 시각 · 교실 · 지우 몸에 담임 영혼', 6)
say('V03', [('난 이제 죽었다…', None)], '(속마음) 담임 영혼', SKY, 'Mono')
say('V04', [('아이씨…', None)], '(속마음) 담임 영혼', SKY, 'Mono')
say('V05', [('하… 지우 녀석…', None)], '(속마음) 담임 영혼', SKY, 'Mono')   # v5: 새 녹음은 끝 "하…"가 따로 안 들림
say('F1a', [('야, 너 왜 그래?', None)], '친구 1', hold=0.0)
say('F2a', [('미친 거야?', None)], '친구 2', hold=0.0, delay=0.35)   # 앞 0.4초는 웃음(흐흐) — 자막은 말 시작에 맞춤
say('F1b', [('너 요새 생결 못 써서 심심하지?', None)], '친구 1')
say('F1c', [(r'가자! 이 언니가\N현체 쓰게 도와줄게.', None)], '친구 1', hold=0.05)
say('F2b', [(r'대리 부모 해 줄 번호\N하나 따 놨다.', None)], '친구 2')
say('V12', [('너네!', None), ('이런 짓까지 해?', '이런')], '담임 영혼 (지우 몸)', SKY)   # v3: 손만 보이는 컷
say('V22', [('대리 부모라니…', None)], '(속마음) 담임 영혼', SKY, 'Mono')
say('V23', [(r'아… 몰라.\N내 알 바 아니지.', None)], '(속마음) 담임 영혼', SKY, 'Mono')
k7 = k['K7']
ev(k7['start'], k7['start'] + 1.6, 'Scene', r'{\an7\pos(40,240)}다시 교무실', 6)
say('V13', [(r'하은이가 어느 집 딸인지,\N그렇게 말했건만…', None), ('에이… 쯧쯧.', '에이', 3.14)], '교감')
say('V14', [('곧 인사 시즌인데…', None), (r'기간제 연장, 안 하고 싶다는\N뜻으로 이해해도 되겠죠?', 1.88)], '교감')
say('V15', [(r'아니, 하은이 집이 뭐…\N왜요?', None), (r'그리고…\N우리 쌤이 기간제였어요?', '그리고')], '지우 영혼', PINK, hold=0.08)
say('V16b', [(r'지식이 높은\N고지식하신 교감쌤께서,', None), ('무섭기까지 하면 단가요?', 2.58)], '지우 영혼 (담임 몸)', PINK, hold=0.0)   # v4: 새 A4 컷(49.216)으로 넘어가기 전에 끝   # v2: 뒤통수 컷이 교감으로 읽히지 않게
say('V17', [('왜 협박을 해요?', None)], '지우 영혼', PINK, hold=0.1)
a18 = L['V18']; b18 = k['K11']['start'] + k['K11']['dur']
# v7 사장님: 해설 자막 — 담임 몸이 일어나기 시작할 때부터 고함·정지가 끝날 때까지. 대사 상자(위끝 1195~)·Tag(1110~)와 Emph(약 820–1040) 사이, 얼굴(위쪽 0–40%) 아래
_k11 = k['K11']
# v8 사장님: 크게(Jua 66), 얼굴 옆 빈 곳(영혼 원 반대쪽 = 왼쪽), 조금 기울임. 일어나는 동안은 머리 왼쪽, 정지(얼굴 확대) 뒤에는 왼쪽 위 구석으로 한 번 옮김
ev(_k11['start'] + 0.05, FREEZE_AT, 'Narr', r'{\an7\pos(36,330)\frz7\fad(120,0)}(들킬까 봐\N괜히 버럭)', 8)
ev(FREEZE_AT, _k11['start'] + _k11['dur'], 'Narr', r'{\an7\pos(30,150)\frz7\fad(0,150)}(들킬까 봐\N괜히 버럭)', 8)
ev(a18, b18, 'Emph', r'{\pos(540,930)\fad(60,150)}이거\N갑질이잖아요!', 7)   # v4: 새 A4는 얼굴이 y≈720까지(펀치 인 포함) → 가슴 높이
ev(a18, b18, 'TagJ', r"{\an2\pos(540,800)\fad(60,150)}지우 영혼", 7)
SUBS.append((round(a18, 2), round(b18, 2), '이거 갑질이잖아요!'))
say('V19a', [('고지식? 허…', None)], '교감', end=MAIN - 0.05)   # v6: 끝 대사, 정적 동안 자막 유지
say('V19b', [('…아니, 우리 쌤?', None)], '교감', hold=0.08)
say('V20a', [(r'김 선생, 요새 몸 바뀌는\NAI 빙의 드라마가 유행이더만,', None)], '교감', hold=0.12)
say('V20b', [(r'또 그런 걸로\N넘어가려는 수작인가요?', None)], '교감', hold=0.1)
say('V21', [('헐… 설마.', None)], '(속마음) 지우 영혼', PINK, 'Mono', hold=0.2)

# v2: 서로 다른 줄의 자막이 한 화면에 같이 있지 않게 — 앞 줄 끝을 다음 줄 시작 0.03초 전으로 자름
PEND.sort(key=lambda x: x['a'])
for i, x in enumerate(PEND):
    nxt = next((y for y in PEND[i + 1:] if y['grp'] != x['grp']), None)
    if nxt and x['b'] > nxt['a'] - 0.03: x['b'] = nxt['a'] - 0.03
    if x['grp'] == 'V17': x['b'] = min(x['b'], L['V18'] - 0.03)   # Emph와도 겹치지 않게
    emit(**x)
SUBS = [(round(x['a'], 2), round(x['b'], 2), x['text'].replace(r'\N', ' ')) for x in PEND] + [s_ for s_ in SUBS if s_[2] == '이거 갑질이잖아요!']
SUBS.sort()
head = (KIT / 'soulchange_style.ass').read_text(encoding='utf-8').rstrip('\n')
# v3: 화자 Tag 우리 스타일(키트는 읽기만, 사장님 결정이 키트보다 앞섬). Jua 54(키트 Tag 38의 약 1.4배), 상자(BorderStyle 3)
OWN = ("Style: Narr,Jua,66,&H005AE3FF,&H005AE3FF,&H80000000,&H80000000,0,0,0,0,100,100,0,0,3,8,0,2,0,0,0,1\n"   # v7: 해설(편집자 말) — 노란 글자, 검은 상자 50%, 화자 Tag 없음
       "Style: DlgB,Jua,62,&H00FFFFFF,&H00FFFFFF,&H33000000,&H33000000,0,0,0,0,100,100,0,0,3,10,0,2,0,0,0,1\n"   # v4: 겉말, 검은 상자 80%
       "Style: MonoB,Jua,60,&H00E6F2FF,&H00E6F2FF,&H33402A20,&H33402A20,0,0,0,0,100,100,0,0,3,10,0,2,0,0,0,1\n"   # v4: 속마음, 남색 상자 80%
       "Style: TagJ,Jua,54,&H00FFFFFF,&H00FFFFFF,&H009A4FE0,&H009A4FE0,0,0,0,0,100,100,0,0,3,9,0,2,0,0,0,1\n"   # 지우 영혼: 분홍 상자 흰 글자
       "Style: TagT,Jua,54,&H00FFFFFF,&H00FFFFFF,&H00C07A2A,&H00C07A2A,0,0,0,0,100,100,0,0,3,9,0,2,0,0,0,1\n"   # 담임 영혼: 하늘 상자 흰 글자
       "Style: TagW,Jua,54,&H00FFFFFF,&H00FFFFFF,&H00606066,&H00606066,0,0,0,0,100,100,0,0,3,9,0,2,0,0,0,1\n"   # 교감·친구: 어두운 상자 흰 글자
       "Style: TagJi,Jua,54,&H00C88CFF,&H00C88CFF,&H00303038,&H00303038,0,0,0,0,100,100,0,0,3,9,0,2,0,0,0,1\n"  # 지우 속마음: 어두운 상자 분홍 글자
       "Style: TagTi,Jua,54,&H00FFC88C,&H00FFC88C,&H00303038,&H00303038,0,0,0,0,100,100,0,0,3,9,0,2,0,0,0,1")   # 담임 속마음: 어두운 상자 하늘 글자
head = head.replace('\n\n[Events]', '\n' + OWN + '\n\n[Events]') if '\n\n[Events]' in head else head.replace('\n[Events]', '\n' + OWN + '\n[Events]')
assert 'TagJ,' in head
(B / 'ep5.ass').write_text(head + '\n' + '\n'.join(EV) + '\n', encoding='utf-8')

# ---------- 6. 합치기: 본편(영혼 원 + 자막) → 엔딩 이어 붙이기 ----------
en_j = '+'.join(f"between(t,{c['start']},{c['start'] + c['dur'] - 0.001:.3f})" for c in CUTS if c['pip'] == 'pip')
en_t = '+'.join(f"between(t,{c['start']},{c['start'] + c['dur'] - 0.001:.3f})" for c in CUTS if c['pip'] == 'pip_t')
vf = (f"[1:v]scale=300:300[pj];[2:v]scale=300:300[pt];"
      f"[0:v][pj]overlay=x=750:y=130:enable='{en_j}'[a];[a][pt]overlay=x=750:y=130:enable='{en_t}'[b];"
      f"[b]ass={B / 'ep5.ass'}:fontsdir={KIT / 'fonts'},format=yuv420p[vout]")
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', B / 'joined.mp4', '-i', KIT / 'pip.png', '-i', KIT / 'pip_t.png',
     '-filter_complex', vf, '-map', '[vout]', '-t', MAIN, '-r', FPS, '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', B / 'main_v.mp4'])
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', B1 / 'ending_ep5.mp4', '-an', '-vf', f'fps={FPS},format=yuv420p,setsar=1',
     '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', B / 'ending_v.mp4'])
(B / 'vlist.txt').write_text(f"file '{B / 'main_v.mp4'}'\nfile '{B / 'ending_v.mp4'}'\n")
out = HERE / 'ep5_v8.mp4'
run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', B / 'vlist.txt', '-i', B / 'mix.wav',
     '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-t', TOT, '-movflags', '+faststart', out])
json.dump({'main': MAIN, 'ending': END_LEN, 'total': TOT, 'loudness_LUFS': I2, 'true_peak_dBTP': TP2,
           'cuts': [{kk: (str(vv) if isinstance(vv, pathlib.Path) else vv) for kk, vv in c.items()} for c in CUTS],
           'lines': {lid: {'start': L[lid], 'end': round(L[lid] + D[lid], 3), 'tempo': SPEC[lid]['tempo'], 'file': SPEC[lid]['f'],
                           'range': SPEC[lid]['r'], 'inner': lid in INNER} for lid in sorted(L, key=L.get)},
           'subs': SUBS, 'sfx': {'slam': SLAM, 'flop': FLOP, 'phone_in': PHONE_IN, 'hush': HUSH, 'freeze_at': FREEZE_AT, 'shout_at': SHOUT_AT, 'cough': COUGH_AT, 'cough2': COUGH2_AT, 'whip_at': WHIP_AT, 'bgm': BGM_SECT}},
          open(HERE / 'timeline_v8.json', 'w'), ensure_ascii=False, indent=1)
print('OK', out, TOT)
