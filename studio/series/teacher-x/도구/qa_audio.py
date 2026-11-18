# 교사X 소리 확인 도구 (재발방지 체크리스트 관문 B·F)
# 하는 일
#  [완성 영상]  python3 qa_audio.py 완성.mp4 sub.ass
#    - 전체 LUFS(-14 목표)·최고점, 영상·소리 길이 차(0.05초 넘으면 경고)
#    - 마지막 대사 끝 → 영상 끝 = 말 없는 꼬리(5초 넘으면 경고)
#    - 대사 줄마다(자막 DV·DJ·DD·N 묶음) 완성 영상의 크기(LUFS)를 재서
#      앞뒤 대사와 2dB 넘게 차이 나거나, 같은 사람 평균과 3dB 넘게 차이 나면 경고
#  [받은 녹음]  python3 qa_audio.py --rec a01.wav a02.wav ...
#    - 파일마다 LUFS·길이·앞뒤 무음, 전체 가운데값과 3dB 넘게 차이 나면 경고
# 이 도구는 숫자만 잰다. 직접 듣지 못한 소리는 "확인했다"고 쓰지 않고 수치와 함께 사장님 청취를 부탁한다.
import sys, os, re, json, subprocess, argparse, statistics

ap = argparse.ArgumentParser()
ap.add_argument('video', nargs='?'); ap.add_argument('ass', nargs='?')
ap.add_argument('--rec', nargs='*', default=None)
ap.add_argument('--styles', default='DV,DJ,DD,N')
ap.add_argument('--tail-max', type=float, default=5.0)
ap.add_argument('--target', type=float, default=-14.0)
a = ap.parse_args()

def ebu(f, ss=None, t=None):
    c = ['ffmpeg', '-nostdin']
    if ss is not None: c += ['-ss', f'{ss:.3f}', '-t', f'{t:.3f}']
    c += ['-i', f, '-vn', '-af', 'ebur128=peak=true', '-f', 'null', '-']
    e = subprocess.run(c, capture_output=True, text=True).stderr
    I = float(re.findall(r'I:\s+(-?[0-9.]+|-inf) LUFS', e)[-1].replace('-inf', '-99'))
    pk = re.findall(r'Peak:\s+(-?[0-9.]+|-inf) dBFS', e)
    return I, (float(pk[-1].replace('-inf', '-99')) if pk else None)
def dur(f, sel):
    o = subprocess.run(['ffprobe', '-v', '0', '-select_streams', sel, '-show_entries', 'stream=duration', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout.strip()
    try: return float(o.splitlines()[0])
    except Exception: return None
def silence(f):
    e = subprocess.run(['ffmpeg', '-nostdin', '-i', f, '-af', 'silencedetect=n=-40dB:d=0.15', '-f', 'null', '-'], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r'silence_start: (-?[0-9.]+)', e)]; en = [float(x) for x in re.findall(r'silence_end: ([0-9.]+)', e)]
    return st, en

W = []
if a.rec:
    rows = []
    for f in a.rec:
        I, pk = ebu(f); d = dur(f, 'a:0'); st, en = silence(f)
        lead = en[0] if st and st[0] <= 0.01 and en else 0.0
        trail = d - st[-1] if st and (not en or st[-1] > en[-1]) else 0.0
        rows.append((os.path.basename(f), I, pk, d, lead, trail))
    med = statistics.median(r[1] for r in rows)
    print(f'| 파일 | LUFS | 최고점 | 길이 | 앞 무음 | 뒤 무음 | 판정 |\n|---|---|---|---|---|---|---|')
    for n, I, pk, d, l, t in rows:
        bad = []
        if abs(I - med) > 3: bad.append(f'크기 {I - med:+.1f}dB')
        if l > 0.6: bad.append('앞 무음 김')
        if t > 0.8: bad.append('뒤 무음 김')
        print(f'| {n} | {I:.1f} | {pk} | {d:.2f} | {l:.2f} | {t:.2f} | {"경고: " + ", ".join(bad) if bad else "ok"} |')
    print(f'\n가운데값 {med:.1f} LUFS. 같은 인물 줄끼리 비교할 것(인물마다 기준이 다름). 크기만 잼 — 톤·발음은 받아쓰기(asr.py)와 사장님 청취로.')
    sys.exit()

V = a.video
I, pk = ebu(V); dv = dur(V, 'v:0'); da = dur(V, 'a:0')
print(f'전체: {I:.1f} LUFS (목표 {a.target}) / 최고점 {pk} dBFS / 영상 {dv:.2f}초 · 소리 {da:.2f}초 (차 {abs(dv - da):.2f})')
if abs(I - a.target) > 1: W.append(f'전체 크기 {I:.1f} LUFS — 목표 {a.target}에서 1dB 넘게 벗어남')
if pk is not None and pk > -0.5: W.append(f'최고점 {pk} dBFS — 깨질 위험')
if dv and da and abs(dv - da) > 0.05: W.append(f'영상·소리 길이 차 {abs(dv - da):.2f}초')

# 자막에서 대사 줄 묶기: 같은 스타일 연속 + 틈 0.35초 이하 = 한 줄
def t2s(t): h, m, s = t.split(':'); return int(h) * 3600 + int(m) * 60 + float(s)
sty = set(a.styles.split(','))
ev = []
for l in open(a.ass, encoding='utf-8'):
    if not l.startswith('Dialogue:'): continue
    p = l[len('Dialogue:'):].split(',', 9)
    if p[3].strip() in sty: ev.append([t2s(p[1].strip()), t2s(p[2].strip()), p[3].strip(), re.sub(r'\{[^}]*\}', '', p[9]).strip()])
ev.sort()
L = []
for s, e, st, tx in ev:
    if L and L[-1][2] == st and s - L[-1][1] <= 0.35: L[-1][1] = max(L[-1][1], e); L[-1][3] += ' ' + tx
    else: L.append([s, e, st, tx])
for x in L:
    x.append(ebu(V, x[0], max(0.4, x[1] - x[0]))[0] if x[1] - x[0] >= 0.4 else None)
by = {}
for x in L:
    if x[4] is not None and x[4] > -60: by.setdefault(x[2], []).append(x[4])
avg = {k: statistics.median(v) for k, v in by.items()}
print('\n| 시각 | 누구(자막) | 대사 | LUFS | 같은 사람 평균과 | 앞 대사와 | 판정 |\n|---|---|---|---|---|---|---|')
prev = None
for x in L:
    s, e, st, tx, lu = x
    if lu is None or lu <= -60:
        print(f'| {s:.1f} | {st} | {tx[:24]} | (짧음) | | | |'); continue
    dm = lu - avg[st]; dp = (lu - prev) if prev is not None else 0
    bad = []
    if abs(dm) > 3: bad.append(f'같은 사람보다 {dm:+.1f}dB')
    if abs(dp) > 2: bad.append(f'앞 대사보다 {dp:+.1f}dB')
    if bad: W.append(f'{s:.1f}초 {st} "{tx[:20]}" — ' + ', '.join(bad))
    print(f'| {s:.1f} | {st} | {tx[:24]} | {lu:.1f} | {dm:+.1f} | {dp:+.1f} | {"경고" if bad else "ok"} |')
    prev = lu
last = max(x[1] for x in L) if L else 0
tail = dv - last
print(f'\n마지막 대사 끝 {last:.1f}초 → 말 없는 꼬리 {tail:.1f}초 (기준 {a.tail_max}초 이하)')
if tail > a.tail_max: W.append(f'말 없는 꼬리 {tail:.1f}초')
print('\n경고 %d건' % len(W)); [print(' -', w) for w in W]
print('주의: 완성 영상 크기에는 배경음이 섞여 있음(대사 중엔 낮춤). 앞뒤 2dB는 화자가 바뀌는 곳에서 자연스러울 수 있으니 경고 줄은 사장님 청취로 판단.')
