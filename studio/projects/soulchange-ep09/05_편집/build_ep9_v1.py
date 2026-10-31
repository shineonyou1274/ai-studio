#!/usr/bin/env python3
"""소울체인지 9화 편집 v1 (대본 v3.1, 컷 = zcre Seedance 2.5 K1~K12 + Higgsfield 보충 K10b·K10c).

흐름
- K0 첫 1초: 담임 몸 폰을 귀에 대고 씩 웃음(K5 끝)
- 모의고사 날 아침 교실: K1 뻘쭘한 조례 + 아이들 수군 "담임 왜 저러냐?" / K2 지우 몸 "샘 이야기하시잖아. 조용히 해." → 친구2 "너 요즘 진짜 이상해."
- K3 친구1 "쌤… 저 생조 쓸래요." → K4 "그래? 흠… 어머니한테 확인 전화할 거야." → (수화기) "네~ 엄마예요~"
- K5 "어머니, 지난번에 다리 다치신 건 다 나으셨어요?" → 대리 엄마 "네? 아… 네. 덕분에 나았습니다…" 뚝 → K6 친구1 굳음 + "어머님, 다리 다치신 적 없으시지?" → K7 지우 몸 박수 속마음 "저걸 저렇게 잡네."
- 점심: K8 최 쌤 목록 → K9 벤치 → K10 최 쌤 멘트 앞(립싱크) → K11 덤불 몰래 응원단 + 교감 "시간은 딱 오늘까지요." → K10b 멘트 중간(립싱크) → K9 와이드 위 멘트 이어짐 → K10c "너희가 좋은 어른이 되도록…" → K12 현석 후드 벗음 "엄마한테, 말해 볼게요."
zcre 컷은 생성할 때 원 녹음을 오디오 참조로 넣었으므로, 녹음 토막을 컷 안 입 움직임 시각에 맞춰 놓는다(생성로그 zcre 분석값).
사용: python3 build_ep9_v1.py [--plan]
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
TAG_ = 'v1'
B = HERE / f'build_{TAG_}'; B.mkdir(exist_ok=True)
VO = B / 'vo'; VO.mkdir(exist_ok=True)
FPS, W, H = 30, 1080, 1920
END_LEN = 5.7
ENDING = B / 'ending_ep9.mp4'      # make_ending.py 9 화
f = lambda s: ImageFont.truetype(str(KIT / 'fonts/Jua-Regular.ttf'), s)


def run(cmd, **kw):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, **kw)
    if r.returncode: raise SystemExit(' '.join(map(str, cmd))[:300] + '\n' + r.stderr[-2000:])
    return r


def dur_of(p):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)], capture_output=True, text=True).stdout)


# ---------- 1. 대사 ----------
# 립싱크 토막: 쉼 줄이기·빠르기 없이 원본 그대로(LS), 나머지는 vo_prep(쉼 줄이기)
LS = {  # id: (파일, 시작, 끝)
    'J01': ('E9-01_jiu_teacherbody.mp3', 0.0, 5.72),
    'T02a': ('E9-02_teacher_studentbody.mp3', 0.10, 0.64), 'T02b': ('E9-02_teacher_studentbody.mp3', 0.84, 2.36), 'T02c': ('E9-02_teacher_studentbody.mp3', 2.58, 3.30),
    'F04a': ('E9-04_friend1_chloe.mp3', 0.10, 1.05), 'F04b': ('E9-04_friend1_chloe.mp3', 1.36, 3.12),
    'J05': ('E9-05_jiu_teacherbody.mp3', 0.0, 4.75),
    'J07a': ('E9-07_jiu_teacherbody.mp3', 0.0, 3.60),
    'C09a': ('E9-09a_choi_celine.mp3', 0.0, 15.31),
    'C09b1': ('E9-09b_choi_celine.mp3', 0.0, 8.15),
    'C09b2': ('E9-09b_choi_celine.mp3', 8.15, 18.0),
    'C09b3': ('E9-09b_choi_celine.mp3', 18.0, 22.13),
}
SPEC = {
    'W12': dict(f='E9-12_friend2_pixie_whisper.mp3', r=[(0, 1.80)], tempo=1.0),
    'W13': dict(f='E9-13_friend1_chloe_whisper.mp3', r=[(0, 3.08)], tempo=1.05, gap=0.2),
    'F03': dict(f='E9-03_friend2_pixie.mp3', r=[(0, 2.93)], tempo=1.05, gap=0.2),
    'M06a': dict(f='E9-06_fakemom_petra.mp3', r=[(0, 2.40)], tempo=1.0),
    'M06b': dict(f='E9-06_fakemom_petra.mp3', r=[(2.40, 8.12)], tempo=1.08, gap=0.25),
    'J07b': dict(f='E9-07_jiu_teacherbody.mp3', r=[(4.25, 7.16)], tempo=1.0, gap=0.25),
    'T08': dict(f='E9-08_teacher_inner_teacher.mp3', r=[(0, 2.19)], tempo=1.0),
    'VP10': dict(f='E9-10_vp_arthur.mp3', r=[(0, 2.43)], tempo=1.0),
    'H11': dict(f='E9-11_hyeonseok_evan.mp3', r=[(0, 2.77)], tempo=1.0),
}
D = vp.prep(SPEC, V, VO)
for lid, (fn, a_, b_) in LS.items():
    x = vp.decode(V / fn, a_, b_); tmp = VO / f'{lid}_t.wav'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(vp.SR), '-ac', '1', '-i', '-', str(tmp)], input=x.astype(np.float32).tobytes(), check=True)
    g = -18.0 - vp.lufs(tmp)
    run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-af', f'volume={g:.2f}dB,alimiter=limit=0.7:level=false:attack=1:release=50,afade=t=in:d=0.01,areverse,afade=t=in:d=0.02,areverse',
         '-ar', '48000', '-c:a', 'pcm_s16le', VO / f'{lid}.wav'])
    tmp.unlink(); D[lid] = round(dur_of(VO / f'{lid}.wav'), 3); SPEC[lid] = dict(f=fn, r=[(a_, b_)], tempo=1.0)
INNER = {'T08'}
PHONE = {'M06a', 'M06b'}         # 수화기 소리
WHISPER = {'W12', 'W13'}         # 작게 수군

# ---------- 2. 컷 ----------
L, CUTS = {}, []
t = 0.0
def cut(cid, src, ss, dur, pip='pip', stretch=1.0, zoom=(1.0, 0.5, 0.5), vfx='', hold=False, note=''):
    global t
    CUTS.append(dict(id=cid, src=src, ss=ss, dur=round(dur, 3), pip=pip, stretch=stretch, zoom=zoom, vfx=vfx, hold=hold, start=round(t, 3), note=note))
    t += dur
def at(lid, x):
    L[lid] = round(x, 3); return x + D[lid]
def end_(lid): return L[lid] + D[lid]
K = lambda n: C / f'{n}.mp4'

cut('K0', K('K5'), 7.0, 1.0, note='첫 1초: 담임 몸 폰을 귀에 대고 씩 웃음')
# K1 교탁 조례(입이 녹음과 잘 안 맞아 넓게 씀) + 수군
c0 = t; e = at('J01', c0 + 0.15)
at('W12', c0 + 3.9); e2 = at('W13', end_('W12') + 0.05)
cut('K1', K('K1'), 0, max(dur_of(K('K1')) - 0.05, e + 0.2 - c0), hold=True, note='담임 몸 뻘쭘한 조례 → 손으로 귀 쪽')
TUCK = (c0 + 4.2, c0 + 6.0)
# K2 지우 몸(김병만 영혼) "조용히 해" — 생성 입 1.35 / 2.45 / 4.05
c0 = t
at('T02a', c0 + 1.33); at('T02b', c0 + 2.40); e = at('T02c', c0 + 4.03)
e = at('F03', max(e + 0.15, end_('W13') + 0.1))
cut('K2', K('K2'), 0, e + 0.15 - c0, pip='pip_t', hold=True, note='지우 몸 돌아보며 "조용히 해" → 친구2 화면 밖')
# K3 친구1 "쌤… 저 생조 쓸래요." — 생성 입 1.75 / 3.15
c0 = t; at('F04a', c0 + 1.60); e = at('F04b', c0 + 3.12)
cut('K3', K('K3'), 0, max(e + 0.2 - c0, 4.9), zoom=(1.15, 0.5, 0.3), note='친구1 배를 감싸며 "생조 쓸래요" (명찰 글자는 1.15배로 일부 뺌)')
# K4 담임 몸 "그래? 흠… 확인 전화할 거야." — 원음 그대로 0초 → 5.4초 폰 귀에 → 수화기 "네~ 엄마예요~"
c0 = t; at('J05', c0 + 0.05); e = at('M06a', c0 + 5.75)
cut('K4', K('K4'), 0, e + 0.2 - c0, hold=True, vfx="crop=iw:ih*0.82:0:0,scale=1080:1920,", note='담임 몸 끄덕 → 폰 귀에(손가락 뭉개짐은 아래를 잘라 덜어 냄)')
RING = c0 + 5.45
# K5 "어머니, 지난번에…" — 생성 입 0.25~ → 대리 엄마 당황 → 뚝
c0 = t; at('J07a', c0 + 0.12); e = at('M06b', c0 + 4.6); HANG = e + 0.05
cut('K5', K('K5'), 0, min(e + 0.35 - c0, 8.0), hold=True, note='담임 몸 통화 → 듣고 씩 웃음')
if HANG + 0.3 > t: cut('K5h', K('K5'), 7.8, HANG + 0.3 - t, hold=True, note='끝 프레임 멈춤')
# K6 친구1 굳음(크래시 줌) + 담임 몸 화면 밖 "어머님, 다리 다치신 적 없으시지?"
c0 = t; e = at('J07b', c0 + 0.25)
cut('K6', K('K6'), 0.4, max(e + 0.3 - c0, 3.0), zoom=(1.12, 0.5, 0.25), note='친구1 굳음 + 뒤 친구 웃음 참기 (명찰은 1.12배·위쪽 기준으로 일부 뺌)')
# K7 지우 몸 박수 + 속마음
c0 = t; e = at('T08', c0 + 1.6)
cut('K7', K('K7'), 0, max(e + 0.3 - c0, 4.0), pip='pip_t', note='지우 몸(김병만 영혼) 박수, 입 다묾')
# K8 점심 최 쌤 자리 (대사 없음)
cut('K8', K('K8'), 0.3, 4.6, pip=None, note='최 쌤 손: 목록 쓸다가 멈춤 → 향수병을 듦')
# K9 벤치 와이드: 최 쌤 와서 앉음
cut('K9', K('K9'), 0, 5.2, pip=None, note='벤치 뒤 와이드: 최 쌤 와서 앉음')
# K10 최 쌤 멘트 앞(립싱크, 원음 0초)
c0 = t; e = at('C09a', c0 + 0.0)
cut('K10', K('K10'), 0, max(e + 0.2 - c0, dur_of(K('K10')) - 0.05), pip=None, hold=True, note='최 쌤 옆얼굴 "현석아… 미안해."')
# K11 덤불 몰래 응원단 → 교감 손목시계 "시간은 딱 오늘까지요."
c0 = t; e = at('VP10', c0 + 3.6); SNIFF = c0 + 0.4
cut('K11', K('K11'), 0, max(e + 0.3 - c0, 6.0), pip=None, hold=True, note='담임 몸 손수건 훌쩍 → 교감 등장')
# K10b 멘트 중간 앞(립싱크) — Higgsfield 보충
c0 = t; e = at('C09b1', c0 + 0.0)
cut('K10b', K('K10b'), 0, max(e + 0.25 - c0, 3.0), pip=None, hold=True, note='최 쌤 "그런데 말이야… 잘못한 거야."')
# K9 와이드 위로 멘트 이어짐(얼굴 안 보임) — 원본 3.5초부터 천천히
c0 = t; e = at('C09b2', c0 + 0.1)
cut('K9b', K('K9'), 2.5, e + 0.15 - c0, pip=None, stretch=1.25, hold=True, note='벤치 뒤 와이드(느리게) 위로 "그건 분명히… 혼내려고 여기 있는 게 아니야."')
# K10c "너희가 좋은 어른이 되도록…" — Higgsfield 보충(오디오 0.3초 뒤 시작)
c0 = t; e = at('C09b3', c0 + 0.30)
cut('K10c', K('K10c'), 0, max(e + 0.3 - c0, 4.5), pip=None, hold=True, note='최 쌤 미소 "너희가 좋은 어른이 되도록…"')
# K12 현석 후드 벗음 → "엄마한테, 말해 볼게요."
c0 = t; e = at('H11', c0 + 2.9)
cut('K12', K('K12'), 0, max(e + 0.6 - c0, 5.0), pip=None, hold=True, note='현석 후드 벗고 고개 듦')
MAIN = round(t, 3); TOT = round(MAIN + END_LEN, 3)
print('본편', MAIN, '합계', TOT)
for c in CUTS:
    avail = (dur_of(c['src']) - c['ss']) * c['stretch']
    print(f"  {c['id']:5s} {c['start']:6.2f} +{c['dur']:.2f}  src {c['ss']}+ x{c['stretch']:.2f}" + (f"  멈춤 {c['dur'] - avail:.2f}" if c['dur'] > avail + 0.02 else ''))
for lid in sorted(L, key=L.get): print(f"    {lid:6s} {L[lid]:6.2f}-{end_(lid):6.2f}")
if '--plan' in sys.argv: sys.exit(0)


# ---------- 3. 영상 조각 ----------
def push_frames(img, n, z1=0.06):
    out = []
    for i in range(n):
        z = 1 + z1 * i / max(1, n - 1); w, h = W / z, H / z
        out.append(np.asarray(img.transform((W, H), Image.EXTENT, ((W - w) / 2, (H - h) / 2 * 0.8, (W + w) / 2, (H - h) / 2 * 0.8 + h), Image.BICUBIC), np.uint8))
    return out


def write_frames(fr, out):
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p', str(out)], input=np.stack(fr).tobytes(), check=True)


seg_list = []
for c in CUTS:
    out = B / f"seg_{c['id']}.mp4"; nfr = round(c['dur'] * FPS)
    z, ax, ay = c['zoom']; used = c['dur'] / c['stretch']
    vf = (f"[0:v]trim=start={c['ss']}:duration={used + 0.1:.3f},setpts=(PTS-STARTPTS)*{c['stretch']},fps={FPS},{c['vfx']}"
          f"scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,")
    if z != 1.0:
        sw, sh = int(round(1080 * z / 2) * 2), int(round(1920 * z / 2) * 2)
        vf += f"scale={sw}:{sh}:flags=lanczos,crop=1080:1920:{int((sw - 1080) * ax)}:{int((sh - 1920) * ay)},"
    vf += "setsar=1,format=rgb24[v]"
    r2 = subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(c['src']), '-filter_complex', vf, '-map', '[v]', '-frames:v', str(nfr), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    mv = list(np.frombuffer(r2, np.uint8).reshape(-1, H, W, 3))
    if len(mv) < nfr: mv += push_frames(Image.fromarray(mv[-1]), nfr - len(mv), 0.08 if c['hold'] else 0.02)
    write_frames(mv[:nfr], out); seg_list.append(out)
(B / 'list.txt').write_text(''.join(f"file '{p}'\n" for p in seg_list))
run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', B / 'list.txt', '-c', 'copy', B / 'joined.mp4'])

# ---------- 4. 소리 ----------
HALL = 'aecho=0.85:0.6:45:0.12'
ins, fc, mixl = [], [], []
for i, (lid, st) in enumerate(sorted(L.items(), key=lambda kv: kv[1])):
    ins += ['-i', VO / f'{lid}.wav']
    ch = f"[{i}:a]aresample=48000,aformat=channel_layouts=mono"
    if lid in INNER: ch += f",{HALL}"
    if lid in PHONE: ch += ",highpass=f=350,lowpass=f=3200,acompressor=threshold=-18dB:ratio=4,volume=-2dB"
    if lid in WHISPER: ch += ",highpass=f=200,volume=-9dB"
    ch += ",acompressor=threshold=-20dB:ratio=3:attack=5:release=120"
    ch += f",aformat=channel_layouts=stereo,adelay={int(st * 1000)}:all=1[v{i}]"
    fc.append(ch); mixl.append(f'[v{i}]')
def sfx(lbl, expr, d, at_, vol=1.0):
    fc.append(f"aevalsrc='{expr}':d={d}:s=48000,volume={vol},aformat=channel_layouts=stereo,adelay={int(at_ * 1000)}:all=1[{lbl}]"); mixl.append(f'[{lbl}]')
def noise(lbl, d, at_, filt, vol):
    fc.append(f"anoisesrc=d={d}:c=pink:a=0.5:r=48000,{filt},volume={vol},aformat=channel_layouts=stereo,adelay={int(at_ * 1000)}:all=1[{lbl}]"); mixl.append(f'[{lbl}]')
k = {c['id']: c for c in CUTS}
sfx('sparkle', '0.10*sin(2*PI*(1800+900*t)*t)*exp(-6*t)', 0.5, TUCK[0], 0.8)
sfx('ring', '0.12*sin(2*PI*440*t)*lt(mod(t,0.5),0.35)', 0.8, RING, 0.6)                       # 신호음
sfx('hang', '0.25*sin(2*PI*480*t)*lt(t,0.12)', 0.15, HANG, 0.9)                                 # 뚝
sfx('zoom', '0.12*sin(2*PI*(300+1200*t)*t)*exp(-4*t)', 0.4, k['K6']['start'], 0.8)              # 크래시 줌
for j in range(4): noise(f'clap{j}', 0.05, k['K7']['start'] + 0.3 + 0.35 * j, 'bandpass=f=2200:w=1800', 0.35)
noise('sniff', 0.3, SNIFF, 'bandpass=f=1800:w=2400,afade=t=in:d=0.05,afade=t=out:st=0.15:d=0.15', 0.20)
fc.append(f"anoisesrc=d=0.7:c=pink:a=0.5:r=48000,lowpass=f=900,volume=0.04,afade=t=in:d=0.2,afade=t=out:st=0.4:d=0.3,aformat=channel_layouts=stereo,adelay={int((k['K12']['start'] + 1.6) * 1000)}:all=1[hood]"); mixl.append('[hood]')
def amb(lbl, a, b, lo, hi, vol):
    a0 = max(0, a - 0.3)
    fc.append(f"anoisesrc=d={b - a0:.2f}:c=pink:a=0.5:r=48000,bandpass=f={(lo + hi) // 2}:w={hi - lo},volume={vol},"
              f"afade=t=in:d=0.3,afade=t=out:st={b - a0 - 0.3:.2f}:d=0.3,aformat=channel_layouts=stereo,adelay={int(a0 * 1000)}:all=1[{lbl}]"); mixl.append(f'[{lbl}]')
for c in CUTS:
    a, b = c['start'], c['start'] + c['dur']
    if c['id'] in ('K0', 'K1', 'K2', 'K3', 'K4', 'K5', 'K5h', 'K6', 'K7'): amb(f"am_{c['id']}", a, b, 500, 2500, 0.026)     # 아침 교실 웅성
    elif c['id'] == 'K8': amb('am_K8', a, b, 300, 2800, 0.014)
    else: amb(f"am_{c['id']}", a, b, 150, 700, 0.016)                                                                      # 운동장 바람
fc.append(f"anoisesrc=d={MAIN}:c=brown:a=0.5:r=48000,lowpass=f=350,volume=0.0105,afade=t=in:d=0.5,afade=t=out:st={MAIN - 0.4}:d=0.4,aformat=channel_layouts=stereo[room]"); mixl.append('[room]')
# 배경음: 아침 교실(펄스) → 확인 전화(미스터리) → 들통 뚝 → 박수(가벼움) → 점심(잔잔) → 최 쌤 멘트(잔잔, 크게 낮춤) → 교감 한 줄(가벼움) → 멘트 → 현석 대답 직전 뚝
BGM_SECT = [('pulse', 0.0, k['K4']['start']), ('mystery', k['K4']['start'], k['K6']['start'] - 0.02),
            ('class', end_('J07b') + 0.1, k['K8']['start']), ('mystery', k['K8']['start'], k['K11']['start']),
            ('pulse', k['K11']['start'] + 0.1, k['K10b']['start']), ('mystery', k['K10b']['start'], L['H11'] - 0.6)]
BGM_I = bgm.make(BGM_SECT, [(VO / f'{lid}.wav', st) for lid, st in L.items()], MAIN, B / 'bgm.wav', target_lufs=-22.0, duck_db=-15.0, release=0.2)
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

# ---------- 5. 자막 ----------
def ts(x):
    h_, m_ = int(x // 3600), int(x % 3600 // 60); s_ = x % 60
    return f"{h_}:{m_:02d}:{s_:05.2f}"
PINK, SKY = 'J', 'T'
TAGSTYLE = {('J', False): 'TagJ', ('T', False): 'TagT', ('', False): 'TagW', ('J', True): 'TagJi', ('T', True): 'TagTi'}
EV, PEND, SUBS = [], [], []
def ev(a, b, style, text, layer=1): EV.append(f"Dialogue: {layer},{ts(a)},{ts(b)},{style},,0,0,0,,{text}")
def say(lid, text, tag, col='', style='Dlg', hold=0.15, end=None, start=None, grp=None, y=1330):
    if lid not in L: return
    a = start if start is not None else L[lid]; b = end if end else L[lid] + D[lid] + hold
    PEND.append(dict(a=a, b=b, text=text, tag=tag, col=col, style=style, grp=grp or lid, y=y))
def emit(x):
    ev(x['a'], x['b'], x['style'] + 'B', r'{\an2\pos(540,' + str(x['y']) + r')\fad(60,100)}' + x['text'], 2)
    if x['tag']:
        ty = x['y'] - (149 if r'\N' in x['text'] else 87)
        ev(x['a'], x['b'], TAGSTYLE[(x['col'], x['style'] == 'Mono')], rf"{{\an2\pos(540,{ty})\fad(60,100)}}{x['tag']}", 3)
def narr(a, b, text, x=40, y=430): ev(a, b, 'Narr', rf'{{\an7\pos({x},{y})\frz5\fad(120,150)}}{text}', 8)
def scene(a, b, text): ev(a, b, 'Scene', r'{\an7\pos(40,240)}' + text, 6)
cs = lambda i: k[i]['start']; ce = lambda i: k[i]['start'] + k[i]['dur']

ev(0.62, MAIN, 'Label', r'{\an7\pos(40,140)\fs50}담임과 여고생, 몸이 바뀌었다', 6)
ev(0.0, 0.62, 'Label', r'{\an5\pos(540,640)\bord0\shad0\1c&H000000&\1a&H28&\p1\fad(0,120)}m 0 0 l 1080 0 1080 420 0 420{\p0}', 9)
ev(0.0, 0.62, 'Label', r'{\an5\pos(540,500)\fs50\bord0\fad(0,120)}소울체인지 9화', 10)
ev(0.0, 0.62, 'Label', r'{\an5\pos(540,610)\fs62\1c&HFFFFFF&\3c&H2020D0&\4c&H2020D0&\bord12\fad(0,120)}모의고사 날 아침, 생조 전화', 10)
ev(0.0, 0.62, 'Emph', r'{\an5\pos(540,750)\fs96\bord6\3c&H000000&\fad(0,120)}어머니, 다리는 괜찮으세요?', 10)
scene(cs('K1'), cs('K1') + 2.2, '모의고사 날 아침 · 교실 · 담임 몸에 지우 영혼')
say('J01', r'자, 오늘 모의고사고... 그래서...\N아무튼... 파이팅...', '지우 영혼', PINK)
narr(TUCK[0] - 1.2, TUCK[0] + 0.4, r'(조례도 여고생 말투)', 40, 430)
say('W12', '...담임 왜 저러냐?', '반 친구', y=1560)
say('W13', '...말투 완전 우리 같아.', '반 친구', y=1560)
say('T02b', r'얘들아, 샘 이야기하시잖아.\N조용히 해.', '담임 영혼', SKY, start=L['T02a'], end=end_('T02c') + 0.15, grp='T02')
narr(L['T02a'] - 0.2, end_('T02c'), r'(애어른 모드)', 600, 430)
say('F03', '...너 요즘 진짜 이상해.', '반 친구')
say('F04a', '쌤... 저 생조 쓸래요.', '친구', start=L['F04a'], end=end_('F04b') + 0.2, grp='F04')
say('J05', r'그래? 흠...\N어머니한테 확인 전화할 거야.', '지우 영혼', PINK)
narr(L['J05'] + 0.6, L['M06a'] - 0.1, r'(현역 고딩의 눈)', 600, 430)
say('M06a', '네~ 엄마예요~', '수화기 너머 "엄마"')
say('J07a', r'어머니, 지난번에 다리 다치신 건\N다 나으셨어요?', '지우 영혼', PINK)
say('M06b', r'네? 아... 네. 덕분에 나았습니다.\N그럼 바빠서 이만 끊습니다.', '수화기 너머 "엄마"')
say('J07b', r'...어머님,\N다리 다치신 적 없으시지?', '지우 영혼', PINK)
narr(L['J07b'] + 0.3, ce('K6'), r'(대리 부모, 들통)', 40, 430)
say('T08', '...저걸 저렇게 잡네.', '(속마음) 담임 영혼', SKY, 'Mono')
scene(cs('K8'), ce('K8'), '점심시간 · 최 쌤 자리')
narr(cs('K8') + 0.8, ce('K8'), r'(센 향수 냄새...)', 600, 430)
scene(cs('K9'), ce('K9'), '점심시간 · 운동장 벤치')
CH = '최 선생님 (지금 담임)'
say('C09a', r'현석아, 선생님이랑 잠깐 얘기할 수 있어?\N...오늘은 괜찮아?', CH, end=L['C09a'] + 6.1)
say('C09a', r'선생님은 네가 힘들어하는 냄새가\N있는 줄 몰랐어.', CH, start=L['C09a'] + 6.1, end=L['C09a'] + 10.4, grp='C09a2')
say('C09a', r'미리 알았다면, 절대 그렇게 두지\N않았을 거야. 미안해.', CH, start=L['C09a'] + 10.4, end=end_('C09a') + 0.2, grp='C09a3')
narr(cs('K11') + 0.2, L['VP10'] - 0.1, r'(몰래 응원단)', 600, 430)
say('VP10', '...시간은 딱 오늘까지요.', '교감')
say('C09b1', r'그런데 말이야. 그렇다고 해서,\N선생님한테 욕을 쓰고', CH, end=L['C09b1'] + 4.6)
say('C09b1', r'텀블러에 침을 뱉은 일이\N괜찮아지는 건 아니야.', CH, start=L['C09b1'] + 4.6, end=end_('C09b1') + 0.1, grp='C09b1b')
say('C09b2', r'그건 분명히 잘못한 거야.\N그래도 선생님은 너한테 기회를 주고 싶어.', CH, end=L['C09b2'] + 5.0)
say('C09b2', r'선생님은 너희를 혼내려고\N여기 있는 게 아니야.', CH, start=L['C09b2'] + 5.0, end=end_('C09b2') + 0.1, grp='C09b2b')
say('C09b3', r'너희가 좋은 어른이 되도록,\N옆에서 도우려고 있는 거야.', CH)
say('H11', '...엄마한테, 말해 볼게요.', '현석')
PEND.sort(key=lambda x: x['a'])
for i, x in enumerate(PEND):
    nxt = next((y for y in PEND[i + 1:] if y['grp'] != x['grp'] and y['y'] == x['y']), None)
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
(B / 'ep9.ass').write_text(head + '\n' + '\n'.join(EV) + '\n', encoding='utf-8')

# ---------- 6. 합치기 ----------
en_j = '+'.join(f"between(t,{c['start']},{c['start'] + c['dur'] - 0.001:.3f})" for c in CUTS if c['pip'] == 'pip') or '0'
en_t = '+'.join(f"between(t,{c['start']},{c['start'] + c['dur'] - 0.001:.3f})" for c in CUTS if c['pip'] == 'pip_t') or '0'
vf = (f"[1:v]scale=300:300[pj];[2:v]scale=300:300[pt];"
      f"[0:v][pj]overlay=x=750:y=130:enable='{en_j}'[a];[a][pt]overlay=x=750:y=130:enable='{en_t}'[b];"
      f"[b]ass={B / 'ep9.ass'}:fontsdir={KIT / 'fonts'},format=yuv420p[vout]")
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', B / 'joined.mp4', '-i', KIT / 'pip.png', '-i', KIT / 'pip_t.png',
     '-filter_complex', vf, '-map', '[vout]', '-t', MAIN, '-r', FPS, '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', B / 'main_v.mp4'])
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', ENDING, '-an', '-vf', f'fps={FPS},format=yuv420p,setsar=1', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', B / 'ending_v.mp4'])
(B / 'vlist.txt').write_text(f"file '{B / 'main_v.mp4'}'\nfile '{B / 'ending_v.mp4'}'\n")
out = HERE / f'ep9_{TAG_}.mp4'
run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', B / 'vlist.txt', '-i', B / 'mix.wav',
     '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-t', TOT, '-movflags', '+faststart', out])
json.dump({'main': MAIN, 'total': TOT, 'loudness_LUFS': I2, 'true_peak_dBTP': TP2,
           'cuts': [{kk: (str(vv) if isinstance(vv, pathlib.Path) else vv) for kk, vv in c.items()} for c in CUTS],
           'lines': {lid: {'start': L[lid], 'end': round(end_(lid), 3), 'file': SPEC[lid]['f'], 'range': SPEC[lid]['r']} for lid in sorted(L, key=L.get)},
           'subs': SUBS, 'bgm': BGM_SECT}, open(HERE / f'timeline_{TAG_}.json', 'w'), ensure_ascii=False, indent=1)
print('OK', out, TOT)
