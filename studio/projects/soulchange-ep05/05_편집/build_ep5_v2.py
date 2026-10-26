#!/usr/bin/env python3
"""소울체인지 5화 「이거 갑질이잖아요」 편집 v1 (4화 build_ep4_v16.py와 같은 방식).

기준: 키트 제작규칙 v1 + soulchange_style.ass(Jua, \\fs \\fn \\i 덮어쓰기 없음) / 대본_v3 맨 위 사장님 메모 /
feedback.md 2026-10-26 "엔딩 포함 70초 이하, 으악은 빼도 돼".
- 본편 ≤ 64.3초 + 고정 엔딩 5.7초(series/엔딩/make_ending.py, 다음 화 = 화요일) ≤ 70.0초. 끝 카드 1.5초 대신 엔딩.
- V11 "으악…!" 삭제, 대사 전부 1.05배(음높이 유지 atempo, V20 앞부분만 1.1배), 줄 안의 긴 쉼 0.13초까지 줄임.
- 대사 조각 = vo_prep.py, 친구 폰 연락처 카드 = phone_card.py.
사용: python3 build_ep5_v2.py  → ep5_v2.mp4, timeline_v2.json

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
B = HERE / 'build_v2'; B.mkdir(exist_ok=True)
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
    'V04': dict(f='V04_담임겉_아이씨_raw.mp3', r=[(0, 1.15)]),
    # V05b(잘라 붙인 것)에서 두 번째 "하…"(0.70–1.40)를 빼서 "하… 지우 녀석, 하…"만
    'V05': dict(f='V05b_담임겉_지우녀석_cut_raw.mp3', r=[(0, 0.70), (1.40, 3.108)]),
    'F1a': dict(f='F1_후보B_Chloe_raw.mp3', r=[(0, 1.65)]),
    'F1b': dict(f='F1_후보B_Chloe_raw.mp3', r=[(1.80, 3.72)]),
    'F1c': dict(f='F1_후보B_Chloe_raw.mp3', r=[(4.12, 6.92)]),
    'F2a': dict(f='F2_후보A_Pixie_raw.mp3', r=[(0, 1.72)]),
    'F2b': dict(f='F2_후보A_Pixie_raw.mp3', r=[(1.85, 4.92)]),
    'V12': dict(f='V12_담임겉_이런짓까지2_raw.mp3', r=[(0, 2.15)], gap=0.30),   # "너네!" 뒤 쉼에 두 번째 쾅
    'V22': dict(f='V22_담임겉_대리부모라니_b_raw.mp3', r=[(0.15, 1.8)]),
    'V23': dict(f='V23_담임속_내알바아니지_a_raw.mp3', r=[(0.63, 3.6)]),            # 앞 한숨 0–0.63 자름
    'V13': dict(f='V13_교감_어느집딸_raw.mp3', r=[(0, 5.12)]),
    'V14': dict(f='V14_교감_인사시즌_raw.mp3', r=[(0, 6.05)]),
    'V15': dict(f='V15_지우_우리쌤기간제_raw.mp3', r=[(0, 5.8)]),
    'V16a': dict(f='V16_지우_지식이높은_a_raw.mp3', r=[(0, 1.40)]),               # "아니 참…" (K9 끝)
    'V16b': dict(f='V16_지우_지식이높은_a_raw.mp3', r=[(2.36, 7.8)]),             # "하." 숨소리 빼고 "지식이 높은 …"(K10)
    'V17': dict(f='V17_지우_협박_raw.mp3', r=[(0, 1.38)]),
    'V18': dict(f='V18_지우_갑질_v4낮게_raw.mp3', r=[(0, 2.12)]),
    'V19a': dict(f='V19a_교감_고지식허_a_raw.mp3', r=[(0, 1.70)], gap=0.22),
    'V19b': dict(f='V19b_교감_아니우리쌤_a_raw.mp3', r=[(0.12, 1.76)]),
    'V20a': dict(f='V20_교감_AI빙의수작_b_raw.mp3', r=[(0.12, 4.63)], tempo=1.1),  # 4.58–5.13 무음에서 자름, 1.1배(대본 v3 §1-4 처리 순서 2)
    'V20b': dict(f='V20_교감_AI빙의수작_b_raw.mp3', r=[(5.08, 7.2)]),
    'V21': dict(f='V21_지우속_헐설마_raw.mp3', r=[(0, 1.74)]),                     # "헐… 설마."까지
}
for s in SPEC.values():
    s.setdefault('tempo', T); s.setdefault('gap', G)
D = prep(SPEC, V, VO)
INNER = {'V03', 'V23', 'V21'}   # 속마음 = 영혼 목소리 + 잔향

# ---------- 2. 컷과 대사 배치 ----------
# 컷: id, 원본, 원본 시작, 원본 끝, 영혼 원, 화면 길이, 확대(zoom, 가로 기준점, 세로 기준점)
# 화면 길이 / (원본 끝 - 시작) = 늘림 배율(1.15 이하)
L = {}   # 대사 id → 전체 시간 시작
CUTS = []
t = 0.0
def cut(cid, src, ss, se, pip, dur, zoom=(1.0, 0.5, 0.5), note=''):
    global t
    CUTS.append(dict(id=cid, src=src, ss=ss, se=se, pip=pip, start=round(t, 3), dur=round(dur, 3), zoom=zoom, note=note))
    t += dur
def at(lid, x):
    L[lid] = round(x, 3); return x + D[lid]

c0 = t; e = at('V01', c0 + 0.08); e = at('V02', e + 0.10)
cut('K1', C / 'A1_K1.mp4', 0, 5.04, 'pip', e + 0.08 - c0)
c0 = t; e = at('V03', c0 + 0.06); e = at('V04', e + 0.10)          # 머리 벅벅(원본 3.25초) ≈ "아이씨"
cut('K2', PC / 'K02_P0.mp4', 1.5, None, 'pip_t', e + 0.08 - c0)
c0 = t; e = at('V05', c0 + 0.06)
cut('K3', C / 'C1_K3.mp4', 0, None, 'pip_t', e + 0.08 - c0, zoom=(1.1, 0.5, 0.0), note='치마 안 보이게 1.1배 위쪽 기준')
c0 = t; e = at('F1a', c0 + 0.06); e = at('F2a', e - 0.05); e = at('F1b', e + 0.02)   # 친구 둘 말이 거의 붙음
cut('K4', PC / 'K04_C2.mp4', 0, 5.04, 'pip_t', e + 0.06 - c0)
c0 = t; e = at('F1c', c0 + 0.05); e = at('F2b', e + 0.06)
cut('K5', PC / 'K05_P1.mp4', 0, 5.04, 'pip_t', e + 0.05 - c0, note='폰 하얀 화면에 "대리 엄마 ☎" 카드')
# K6a: P1b 원본 3.0초부터(폰 빠짐 → 쾅 3.42 · 4.00). ×1.127 → 쾅 0.47 · 1.13
k6a_st = 1.127; c0 = t
SLAM = [c0 + (3.42 - 3.0) * k6a_st, c0 + (4.00 - 3.0) * k6a_st]
e = at('V12', SLAM[0] + 0.13)                                       # v2: 첫 쾅 바로 뒤 "너네!"(쾅과 겹치지 않게), 둘째 쾅은 "너네!" 뒤 쉼 안
cut('K6a', PC / 'K06a_P1b.mp4', 3.0, 5.04, 'pip_t', (5.04 - 3.0) * k6a_st)
# K6b: C3 전체, ×1.06. 머리 감싼 채 "대리 부모라니…" → 원본 약 3.1초 털썩 → 속마음
k6b_st = 1.06; c0 = t
e = max(e + 0.05, c0 + 0.25); e = at('V22', e)
FLOP = c0 + 3.1 * k6b_st
e = at('V23', FLOP - 0.45)
cut('K6b', C / 'C3_K6b.mp4', 0, 5.04, 'pip_t', max(5.04 * k6b_st, e + 0.06 - c0), zoom=(1.2, 0.5, 0.0), note='책상 아래 치마 안 보이게 1.2배 위쪽 기준')
c0 = t; e = at('V13', c0 + 0.08)
cut('K7', C / 'A2_K7_교감어느집딸.mp4', 0, None, 'pip', e + 0.08 - c0)
c0 = t; e = at('V14', c0 + 0.06)
cut('K8', PC / 'K08_P2.mp4', 0, 5.04, 'pip', e + 0.06 - c0)
c0 = t; e = at('V15', c0 + 0.06); e = at('V16a', e + 0.10)
cut('K9', C / 'A3_K9_기간제였어요.mp4', 0, 6.04, 'pip', e + 0.06 - c0 + 0.6, note='v2: 끝 0.6초 연장 — "지식이 높은" 첫머리를 담임 몸 정면에서 시작')
c0 = t - 0.6; e = at('V16b', c0 + 0.04)
cut('K10', PC / 'K10_P3.mp4', 0.3, 5.04, 'pip', e + 0.06 - t, note='담임 몸 뒤통수 + 검지 → 손바닥 손짓, 대사는 화면 밖')
c0 = t; CHAIR = c0 + 0.03; e = at('V17', c0 + 0.30); e = at('V18', e + 0.12); HUSH = e
cut('K11', C / 'A4_K11_사이다.mp4', 0, None, 'pip', e + 0.22 - c0, note='끝 정적 약 0.3초')
k12a_st = 1.15; c0 = t
e = at('V19a', c0 + 0.04); e = at('V19b', e + 0.10); e = at('V20a', e + 0.08)
cut('K12a', C / 'A5a_K12a_교감끝훅.mp4', 0, 6.04, 'pip', 6.04 * k12a_st, note='V20 앞부분 끝 약 0.3초가 K12b로 넘어감(화면 밖 교감)')
c0 = t; e = at('V20b', e + 0.12); e = at('V21', e + 0.12); DUNG = e + 0.02
cut('K12b', PC / 'K12b.mp4', 0, None, 'pip', e + 0.25 - c0, zoom=(1.12, 0.65, 0.35), note='Dreamina AI 배지 없애려고 1.12배 확대·오른쪽 아래 기준')
MAIN = round(t, 3)
TOT = round(MAIN + END_LEN, 3)
print('본편', MAIN, '합계', TOT)
for c in CUTS:
    used = (c['se'] - c['ss']) if c['se'] else c['dur']
    c['stretch'] = round(c['dur'] / used, 3)
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
    vf = (f"[0:v]trim=start={c['ss']}:duration={used:.3f},setpts=(PTS-STARTPTS)*{c['stretch']},fps={FPS},"
          f"scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,")
    if z != 1.0:
        sw, sh = int(round(1080 * z / 2) * 2), int(round(1920 * z / 2) * 2)
        vf += f"scale={sw}:{sh}:flags=lanczos,crop=1080:1920:{int((sw - 1080) * ax)}:{int((sh - 1920) * ay)},"
    vf += "setsar=1,format=yuv420p,tpad=stop_mode=clone:stop_duration=0.5[v]"
    run(['ffmpeg', '-y', '-loglevel', 'error', '-i', c['src'], '-filter_complex', vf, '-map', '[v]',
         '-frames:v', round(c['dur'] * FPS), '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', out])
    if c['id'] in ('K5', 'K6a'):
        run(['python3', HERE / 'phone_card.py', out, B / f"seg_{c['id']}_card.mp4"]); out = B / f"seg_{c['id']}_card.mp4"
    seg_list.append(out)
(B / 'list.txt').write_text(''.join(f"file '{p}'\n" for p in seg_list))
run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', B / 'list.txt', '-c', 'copy', B / 'joined.mp4'])

# ---------- 4. 소리 ----------
HALL = 'aecho=0.85:0.6:45:0.12'
GAIN = {'V19b': 2.0, 'V19a': 1.0}   # 끝 훅 "…아니, 우리 쌤?" 또렷하게(대본 v3 §1-4)
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
k5 = k['K5']; PHONE_IN = k5['start'] + 2.85 * k5['stretch']    # 폰이 화면에 들어오는 순간(원본 약 2.85초)
sfx('ding', DING, 0.3, PHONE_IN, 0.6)
for j, x in enumerate(SLAM):
    fc.append(f"anoisesrc=d=0.35:c=brown:a=0.9:r=48000,lowpass=f=900,highpass=f=60,afade=t=out:st=0.02:d=0.3:curve=exp,volume=1.6,"
              f"aformat=channel_layouts=stereo,adelay={int(x * 1000)}:all=1[bang{j}]"); mixl.append(f'[bang{j}]')
sfx('flop', FLOPS, 0.5, FLOP, 0.7)
k8 = k['K8']
for j, x in enumerate([1.45, 1.95]): sfx(f'tap{j}', TAP, 0.15, k8['start'] + x * k8['stretch'], 0.6)
sfx('dung1', DUNGX, 1.2, L['V14'] + 1.45, 0.45)      # "기간제" 무렵
fc.append(f"anoisesrc=d=0.6:c=brown:a=0.5:r=48000,bandpass=f=600:w=500,volume='0.5*lt(mod(t,0.05),0.03)':eval=frame,"
          f"afade=t=out:st=0.3:d=0.3,aformat=channel_layouts=stereo,adelay={int(CHAIR * 1000)}:all=1[chair]"); mixl.append('[chair]')
sfx('thud', THUD, 0.5, L['V18'], 0.8)
sfx('dung2', DUNGX, 1.2, DUNG, 0.5)

def amb(lbl, a, b, lo, hi, vol):
    a0 = max(0, a - 0.3)
    fc.append(f"anoisesrc=d={b - a0:.2f}:c=pink:a=0.5:r=48000,bandpass=f={(lo + hi) // 2}:w={hi - lo},volume={vol},"
              f"afade=t=in:d=0.3,afade=t=out:st={b - a0 - 0.3:.2f}:d=0.3,aformat=channel_layouts=stereo,adelay={int(a0 * 1000)}:all=1[{lbl}]")
    mixl.append(f'[{lbl}]')
CLASS = {'K2', 'K3', 'K4', 'K5', 'K6a', 'K6b'}
for c in CUTS:
    a, b = c['start'], c['start'] + c['dur']
    if c['id'] == 'K11': b = HUSH + 0.05            # "갑질이잖아요!" 끝에 웅성 뚝 → 정적
    if c['id'] == 'K12a': continue                   # 정적
    if c['id'] in CLASS: amb(f"am_{c['id']}", a, b, 500, 2500, 0.022)
    else: amb(f"am_{c['id']}", a, b, 300, 2800, 0.018)
# 룸톤(약 30%): 낮은 웅웅거림을 본편 내내
fc.append(f"anoisesrc=d={MAIN}:c=brown:a=0.5:r=48000,lowpass=f=350,volume=0.0105,afade=t=in:d=0.5,afade=t=out:st={MAIN - 0.4}:d=0.4,aformat=channel_layouts=stereo[room]"); mixl.append('[room]')
fc.append(''.join(mixl) + f"amix=inputs={len(mixl)}:normalize=0,apad=whole_dur={MAIN},atrim=0:{MAIN}[aout]")
run(['ffmpeg', '-y', '-loglevel', 'error', *ins, '-filter_complex', ';'.join(fc), '-map', '[aout]', '-ar', '48000', B / 'mix_raw.wav'])

def meas(p):
    m = subprocess.run(['ffmpeg', '-i', str(p), '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', m)[-1]), float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', m)[-1])
# 2단계 음량(실시간 loudnorm 안 씀): 본편을 재고 고정 게인 + 리미터 → 엔딩(-13.8 LUFS, 그대로) 이어 붙임 → 전체 다시 재서 미세 게인
I0, _ = meas(B / 'mix_raw.wav')
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', B / 'mix_raw.wav', '-af',
     f'volume={-14.0 - I0:.2f}dB,alimiter=limit=0.63:level=false:attack=2:release=60', '-ar', '48000', B / 'mix_main.wav'])
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', B1 / 'ending_ep5.mp4', '-vn', '-ar', '48000', '-ac', '2', B / 'ending.wav'])
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', B / 'mix_main.wav', '-i', B / 'ending.wav', '-filter_complex',
     '[0:a][1:a]concat=n=2:v=0:a=1[a]', '-map', '[a]', '-ar', '48000', B / 'mix_full_raw.wav'])
I1, _ = meas(B / 'mix_full_raw.wav')
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', B / 'mix_full_raw.wav', '-af',
     f'volume={-14.0 - I1:.2f}dB,alimiter=limit=0.63:level=false:attack=2:release=60', '-ar', '48000', B / 'mix.wav'])
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
    ev(a, b, style, r'{\an2\pos(540,1400)' + fad + '}' + text, 2)
    ty = 1276 if r'\N' in text else 1338
    ev(a, b, 'Tag', rf"{{\an2\pos(540,{ty}){fad}}}{col}{tag}", 3)
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
ev(0.0, k1['dur'], 'Label', r'{\an7\pos(40,90)}담임과 학생, 몸이 바뀌었다', 6)
ev(0.0, k1['dur'], 'Scene', r'{\an7\pos(40,190)}교무실 · 담임 몸에 지우 영혼', 6)   # v2: 0초부터
# v2: 지난 화 한 줄(1.6초). K1 첫 1.6초는 얼굴이 화면 위쪽(y≈200~650)이라 위에 두면 이마·눈을 가림 → 첫 대사 자막 바로 아래(손·무릎 쪽)
ev(0.0, 1.6, 'Label', r'{\an8\pos(540,1440)\fad(0,150)}지난 화 · 담임 몸의 지우가 하은 엄마에게\N"일본에선 다 나은 것 같던데요?^^"', 6)
say('V01', [(r'하은이 어머니가\N방금 나한테 전화하셨어요.', None)], '교감')
say('V02', [('네? 아니… 제가…', None)], '지우 영혼', PINK)
k2 = k['K2']
ev(k2['start'], k2['start'] + 2.4, 'Scene', r'{\an7\pos(40,190)}같은 시각 · 교실 · 지우 몸에 담임 영혼', 6)
say('V03', [('난 이제 죽었다…', None)], '담임 영혼 · 속마음', SKY, 'Mono')
say('V04', [('아이씨…', None)], '담임 영혼', SKY)
say('V05', [('하… 지우 녀석, 하…', None)], '담임 영혼', SKY)
say('F1a', [('야, 너 왜 그래?', None)], '친구 1', hold=0.0)
say('F2a', [('미친 거야?', None)], '친구 2', hold=0.0, delay=0.35)   # 앞 0.4초는 웃음(흐흐) — 자막은 말 시작에 맞춤
say('F1b', [('너 요새 생결 못 써서 심심하지?', None)], '친구 1')
say('F1c', [(r'가자! 이 언니가\N현체 쓰게 도와줄게.', None)], '친구 1', hold=0.05)
say('F2b', [(r'대리 부모 해 줄 번호\N하나 따 놨다.', None)], '친구 2')
say('V12', [('너네!', None), ('이런 짓까지 해?', '이런')], '담임 영혼', SKY)
say('V22', [('대리 부모라니…', None)], '담임 영혼', SKY)
say('V23', [(r'아… 몰라.\N내 알 바 아니지.', None)], '담임 영혼 · 속마음', SKY, 'Mono')
k7 = k['K7']
ev(k7['start'], k7['start'] + 1.6, 'Scene', r'{\an7\pos(40,190)}다시 교무실', 6)
say('V13', [(r'하은이가 어느 집 딸인지,\N그렇게 말했건만…', None), ('에이… 쯧쯧.', '에이', 3.14)], '교감')
say('V14', [('곧 인사 시즌인데…', None), (r'기간제 연장, 안 하고 싶다는\N뜻으로 이해해도 되겠죠?', 1.88)], '교감')
say('V15', [(r'아니, 하은이 집이 뭐…\N왜요?', None), (r'그리고…\N우리 쌤이 기간제였어요?', '그리고')], '지우 영혼', PINK, hold=0.08)
say('V16a', [('아니 참…', None)], '지우 영혼', PINK, hold=0.06)
say('V16b', [(r'지식이 높은\N고지식하신 교감쌤께서,', None), ('무섭기까지 하면 단가요?', 2.58)], '지우 영혼 (담임 몸)', PINK)   # v2: 뒤통수 컷이 교감으로 읽히지 않게
say('V17', [('왜 협박을 해요?', None)], '지우 영혼', PINK, hold=0.1)
a18 = L['V18']; b18 = k['K11']['start'] + k['K11']['dur']
ev(a18, b18, 'Emph', r'{\pos(540,700)\fad(60,150)}이거\N갑질이잖아요!', 7)
ev(a18, b18, 'Tag', rf"{{\pos(540,520)\fad(60,150)}}{PINK}지우 영혼", 7)
SUBS.append((round(a18, 2), round(b18, 2), '이거 갑질이잖아요!'))
say('V19a', [('고지식? 허…', None)], '교감', hold=0.1)
say('V19b', [('…아니, 우리 쌤?', None)], '교감', hold=0.08)
say('V20a', [(r'김 선생, 요새 몸 바뀌는\NAI 빙의 드라마가 유행이더만,', None)], '교감', hold=0.12)
say('V20b', [(r'또 그런 걸로\N넘어가려는 수작인가요?', None)], '교감', hold=0.1)
say('V21', [('헐… 설마.', None)], '지우 영혼 · 속마음', PINK, 'Mono', end=MAIN - 0.05)

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
(B / 'ep5.ass').write_text(head + '\n' + '\n'.join(EV) + '\n', encoding='utf-8')

# ---------- 6. 합치기: 본편(영혼 원 + 자막) → 엔딩 이어 붙이기 ----------
en_j = '+'.join(f"between(t,{c['start']},{c['start'] + c['dur'] - 0.001:.3f})" for c in CUTS if c['pip'] == 'pip')
en_t = '+'.join(f"between(t,{c['start']},{c['start'] + c['dur'] - 0.001:.3f})" for c in CUTS if c['pip'] == 'pip_t')
vf = (f"[1:v]scale=300:300[pj];[2:v]scale=300:300[pt];"
      f"[0:v][pj]overlay=x=750:y=70:enable='{en_j}'[a];[a][pt]overlay=x=750:y=70:enable='{en_t}'[b];"
      f"[b]ass={B / 'ep5.ass'}:fontsdir={KIT / 'fonts'},format=yuv420p[vout]")
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', B / 'joined.mp4', '-i', KIT / 'pip.png', '-i', KIT / 'pip_t.png',
     '-filter_complex', vf, '-map', '[vout]', '-t', MAIN, '-r', FPS, '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', B / 'main_v.mp4'])
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', B1 / 'ending_ep5.mp4', '-an', '-vf', f'fps={FPS},format=yuv420p,setsar=1',
     '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', B / 'ending_v.mp4'])
(B / 'vlist.txt').write_text(f"file '{B / 'main_v.mp4'}'\nfile '{B / 'ending_v.mp4'}'\n")
out = HERE / 'ep5_v2.mp4'
run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', B / 'vlist.txt', '-i', B / 'mix.wav',
     '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-t', TOT, '-movflags', '+faststart', out])
json.dump({'main': MAIN, 'ending': END_LEN, 'total': TOT, 'loudness_LUFS': I2, 'true_peak_dBTP': TP2,
           'cuts': [{kk: (str(vv) if isinstance(vv, pathlib.Path) else vv) for kk, vv in c.items()} for c in CUTS],
           'lines': {lid: {'start': L[lid], 'end': round(L[lid] + D[lid], 3), 'tempo': SPEC[lid]['tempo'], 'file': SPEC[lid]['f'],
                           'range': SPEC[lid]['r'], 'inner': lid in INNER} for lid in sorted(L, key=L.get)},
           'subs': SUBS, 'sfx': {'slam': SLAM, 'flop': FLOP, 'phone_in': PHONE_IN, 'hush': HUSH}},
          open(HERE / 'timeline_v2.json', 'w'), ensure_ascii=False, indent=1)
print('OK', out, TOT)
