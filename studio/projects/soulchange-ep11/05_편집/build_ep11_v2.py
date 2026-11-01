#!/usr/bin/env python3
"""소울체인지 11화 편집 v2 (사장님 v1 지적 "담임 몸인데 지우 목소리 아니잖아" → 지우 겉말을 담임 몸 목소리 + 여고생 말투로 다시 녹음).
v1: (대본 v1.2 「선생님은 언제 수업 준비해요?」).
담임의 하루(상담할 시간이 없다) → 방과 후 빈 교실 하은 상담 → "내가 이런 말 할 자격이 있나" → 하은 사과 → "나도 그랬어" → 지우 어머니 상담 신청 "엄마가, 온다고?"
사용: python3 build_ep11_v1.py [--plan]
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
P = EP.parent
V = EP / '04_생성물' / 'voices'
C = EP / '04_생성물' / 'clips'
TAG_ = 'v1'
B = HERE / f'build_{TAG_}'; B.mkdir(exist_ok=True)
VO = B / 'vo'; VO.mkdir(exist_ok=True)
FPS, W, H = 30, 1080, 1920
END_LEN = 5.7
ENDING = B / 'ending_ep11.mp4'      # make_ending.py 11 일
FONT = KIT / 'fonts/Jua-Regular.ttf'
f = lambda s: ImageFont.truetype(str(FONT), s)


def run(cmd, **kw):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, **kw)
    if r.returncode: raise SystemExit(' '.join(map(str, cmd))[:300] + '\n' + r.stderr[-2000:])
    return r


def dur_of(p):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)], capture_output=True, text=True).stdout)


# ---------- 1. 대사 ----------
SPEC = {
    'J01': dict(f='E11-01d_jiu_teacherbody.mp3', r=[(0, 3.40)], tempo=1.0),
    'J03': dict(f='E11-03d_jiu_teacherbody.mp3', r=[(0, 5.30)], tempo=1.0),
    'T05': dict(f='E11-05_teacher_inner.mp3', r=[(0, 2.55)], tempo=1.0),
    'J06': dict(f='E11-06d_jiu_teacherbody.mp3', r=[(0, 4.22)], tempo=1.0),
    'J07': dict(f='E11-07d_jiu_teacherbody.mp3', r=[(0, 5.10)], tempo=1.0),
    'J08': dict(f='E11-08_jiu_inner_student.mp3', r=[(0, 5.30)], tempo=1.05),
    'J09': dict(f='E11-09d_jiu_teacherbody.mp3', r=[(0, 2.80)], tempo=1.0),
    'H10': dict(f='E11-10_11_haeun_hallie_9화GATE.mp3', r=[(4.85, 8.20)], tempo=1.0),
    'H11': dict(f='E11-10_11_haeun_hallie_9화GATE.mp3', r=[(8.70, 10.90)], tempo=1.0),
    'J12': dict(f='E11-12d_jiu_teacherbody.mp3', r=[(0, 3.90)], tempo=1.0),
    'J14': dict(f='E11-14d_jiu_teacherbody.mp3', r=[(0, 2.11)], tempo=1.0),
}
D = vp.prep(SPEC, V, VO)
INNER = {'T05', 'J08'}
PHONE = set(); WHISPER = set(); MEMORY = set(); BEEP = ('', 0, 0)
LS_OFF = {'K1': 0.30, 'K3': 0.95, 'K6': 0.30, 'K9': 0.65, 'K12': 0.20, 'K14': 0.75}   # 립싱크 컷: 생성 영상 입이 녹음보다 늦은 만큼(입 움직임-소리로 잼)

# ---------- 2. 컷 ----------
L, CUTS = {}, []
t = 0.0
def cut(cid, src, ss, dur, pip=None, stretch=1.0, zoom=(1.0, 0.5, 0.5), vfx='', hold=False, fx=None, note=''):
    global t
    CUTS.append(dict(id=cid, src=src, ss=ss, dur=round(dur, 3), pip=pip, stretch=stretch, zoom=zoom, vfx=vfx, hold=hold, fx=fx, start=round(t, 3), note=note))
    t += dur
def at(lid, x):
    L[lid] = round(x, 3); return x + D[lid]
def end_(lid): return L[lid] + D[lid]
K = lambda n: C / f'{n}.mp4'
FB = "hue=s=0.30,eq=brightness=0.04:contrast=1.05,fade=t=in:d=0.12:color=white,"

cut('K0', K('K4'), 1.2, 1.0, note='첫 1초: 서류 더미 + 도장')
c0 = t; e = at('J01', c0 + LS_OFF['K1'])
cut('K1', K('K1'), 0, max(e + 0.5 - c0, 4.6), hold=True, pip='pip', note='메모 붙이며 "오늘은 하은이 상담만"')
c0 = t; CHAT0 = c0 + 0.4
cut('K2', K('K1'), 4.4, 5.2, fx='chat', note='코드: 메신저 알림 4개')
c0 = t; e = at('J03', c0 + LS_OFF['K3'])
cut('K3', K('K3'), 0, max(e + 0.4 - c0, 5.0), hold=True, pip='pip', note='"이런 걸 하루에 다 하라고?"')
cut('K4', K('K4'), 0, 3.6, stretch=0.8, note='전화 + 도장 몽타주, 시계 글자')
c0 = t; e = at('T05', c0 + 1.8)
cut('K5', K('K5'), 0, max(e + 0.4 - c0, 4.8), pip='pip_t', note='지우 몸(김병만)이 딸기우유 툭')
c0 = t; e = at('J06', c0 + LS_OFF['K6'])
cut('K6', K('K6'), 0, max(e + 0.4 - c0, 4.6), hold=True, pip='pip', note='빈 교실, 하은 어깨 너머 몰아붙임')
c0 = t; e = at('J07', c0 + 0.2)
cut('K7', K('K7'), 0, e + 0.3 - c0, stretch=1.1, hold=True, note='하은 손: 치마 끝')
c0 = t; e = at('J08', c0 + 0.3)
cut('K8', K('K8'), 0, e + 0.3 - c0, stretch=1.15, hold=True, pip='pip', note='담임 몸 눈 피함 + 속마음 "정서학대라던데"')
c0 = t; e = at('J09', c0 + LS_OFF['K9'])
cut('K9', K('K9'), 0, max(e + 0.3 - c0, 3.6), hold=True, pip='pip', note='벌떡 일어나 "자격이 있나"')
cut('FB1', P / 'soulchange-ep01/05_편집/ep1_공개본_720p.mp4', 1.0, 1.4, stretch=1.7, zoom=(1.12, 0.5, 0.45), vfx=FB, hold=True, note='회상 1화: 생결 내고 PC방 게시물')
c0 = t; e = at('H10', c0 + 0.5)
cut('K10', K('K10'), 0, max(e + 0.4 - c0, 4.6), hold=True, note='하은 뒷모습 허리 숙임 "죄송합니다"')
c0 = t; e = at('H11', c0 + 0.2)
cut('K11', K('K7'), 2.6, e + 0.4 - c0, stretch=1.2, hold=True, note='하은 손 폈다 쥠 "엄마는 제가 알아서"')
c0 = t; e = at('J12', c0 + LS_OFF['K12'])
cut('K12', K('K12'), 0, max(e + 0.5 - c0, 4.6), hold=True, pip='pip', note='의자 당겨 "나도 그랬어"')
c0 = t; MSG0 = c0 + 0.6
cut('K13', K('K14'), 0.1, 2.6, fx='msg', note='코드: 문자 "[상담 신청] 내일 16:00 — 지우 어머니"')
c0 = t; e = at('J14', c0 + LS_OFF['K14'])
cut('K14', K('K14'), 0, max(e + 0.8 - c0, 3.4), hold=True, pip='pip', note='"…엄마가, 온다고?"')
MAIN = round(t, 3); TOT = round(MAIN + END_LEN, 3)
print('본편', MAIN, '합계', TOT)
for c in CUTS:
    avail = (dur_of(c['src']) - c['ss']) * c['stretch']
    print(f"  {c['id']:5s} {c['start']:6.2f} +{c['dur']:.2f}  x{c['stretch']:.2f}" + (f"  멈춤 {c['dur'] - avail:.2f}" if c['dur'] > avail + 0.02 and not c['fx'] else ''))
for lid in sorted(L, key=L.get): print(f"    {lid:6s} {L[lid]:6.2f}-{end_(lid):6.2f}")
if '--plan' in sys.argv: sys.exit(0)



NOTI = [('[공문]', '체험학습 안전계획서 (오늘까지)'), ('[회의]', '학맞통 사례회의 (2교시)'), ('[요청]', '학부모 민원 회신 바랍니다'), ('[제출]', '수행평가 채점 결과 (오늘까지)')]
def bg_of(c, blur=16, dim=0.5):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(c['ss']), '-i', str(c['src']), '-frames:v', '1', '-vf', 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    bg = Image.frombytes('RGB', (W, H), raw[:W * H * 3]).filter(ImageFilter.GaussianBlur(blur))
    return Image.fromarray((np.asarray(bg, float) * dim).astype(np.uint8))


def chat_frames(c):
    """K2: 담임 몸 PC 메신저 알림이 하나씩 쌓임 / K13: 폰 문자 한 통."""
    n = round(c['dur'] * FPS); bg = bg_of(c); out = []
    for i in range(n):
        tt = c['start'] + i / FPS
        im = bg.copy(); d = ImageDraw.Draw(im)
        if c['fx'] == 'chat':
            for j, (tag, s) in enumerate(NOTI):
                ta = CHAT0 + j * 0.85
                if tt < ta: continue
                k_ = min(1.0, (tt - ta) / 0.15); y = 420 + j * 190; x = 80 + int((1 - k_) * 300)
                d.rounded_rectangle([x, y, x + 920, y + 160], 28, fill=(250, 250, 252), outline=(200, 205, 215), width=3)
                d.text((x + 36, y + 26), '메신저 | 방금', font=f(30), fill=(120, 125, 140))
                d.text((x + 36, y + 70), tag, font=f(50), fill=(220, 70, 60))
                d.text((x + 36 + d.textlength(tag, font=f(50)) + 18, y + 70), s, font=f(46), fill=(30, 30, 40))
        else:
            x0, y0 = 150, 520
            d.rounded_rectangle([x0, y0, x0 + 780, y0 + 980], 70, fill=(22, 22, 26))
            d.rounded_rectangle([x0 + 22, y0 + 22, x0 + 758, y0 + 958], 52, fill=(236, 238, 244))
            d.text((x0 + 60, y0 + 90), '<  학부모 상담 예약', font=f(40), fill=(30, 30, 30), anchor='lm')
            if tt >= MSG0:
                k_ = min(1.0, (tt - MSG0) / 0.12)
                d.rounded_rectangle([x0 + 60, y0 + 190, x0 + 720, y0 + 190 + int(300 * k_)], 30, fill=(255, 255, 255))
                if k_ >= 1:
                    for j, l in enumerate(['[상담 신청]', '내일 16:00', '신청자: 지우 어머니']):
                        d.text((x0 + 100, y0 + 230 + j * 80), l, font=f(52), fill=(220, 70, 60) if j == 2 else (30, 30, 40))
        out.append(np.asarray(im, np.uint8))
    return out


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
    if c['fx'] == 'card':
        write_frames([np.zeros((H, W, 3), np.uint8)] * nfr, out); seg_list.append(out); continue
    if c['fx'] in ('chat', 'msg'):
        write_frames(chat_frames(c)[:nfr], out); seg_list.append(out); continue
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
    if lid in MEMORY: ch += ",highpass=f=180,lowpass=f=5000,aecho=0.8:0.5:60|120:0.25|0.15,volume=-9dB"
    if lid == BEEP[0]: ch += f",volume=enable='between(t,{BEEP[1]:.2f},{BEEP[1] + BEEP[2]:.2f})':volume=0"
    ch += ",acompressor=threshold=-20dB:ratio=3:attack=5:release=120"
    ch += f",aformat=channel_layouts=stereo,adelay={int(st * 1000)}:all=1[v{i}]"
    fc.append(ch); mixl.append(f'[v{i}]')
def sfx(lbl, expr, d, at_, vol=1.0):
    fc.append(f"aevalsrc='{expr}':d={d}:s=48000,volume={vol},aformat=channel_layouts=stereo,adelay={int(at_ * 1000)}:all=1[{lbl}]"); mixl.append(f'[{lbl}]')
def noise(lbl, d, at_, filt, vol):
    fc.append(f"anoisesrc=d={d}:c=pink:a=0.5:r=48000,{filt},volume={vol},aformat=channel_layouts=stereo,adelay={int(at_ * 1000)}:all=1[{lbl}]"); mixl.append(f'[{lbl}]')
k = {c['id']: c for c in CUTS}
DINGX = '0.16*sin(2*PI*1320*t)*lt(t,0.08)+0.16*sin(2*PI*1760*t)*gt(t,0.12)*lt(t,0.24)'
for j in range(4): sfx(f'ding{j}', DINGX, 0.3, CHAT0 + j * 0.85, 0.45)
sfx('msg', DINGX, 0.3, MSG0, 0.5)
for j in range(6): sfx(f'stamp{j}', '0.5*sin(2*PI*90*t)*exp(-30*t)', 0.15, k['K4']['start'] + 0.3 + j * 0.5, 0.6)   # 도장 쾅쾅
sfx('chair', '0.18*sin(2*PI*(180-60*t)*t)*exp(-8*t)', 0.3, k['K9']['start'] + 0.2, 0.6)
sfx('boing', '0.20*sin(2*PI*(300+500*t)*t)*exp(-6*t)', 0.4, L['J14'], 0.5)
for j in range(2): sfx(f'dudung{j}', '0.55*sin(2*PI*(70-25*t)*t)*exp(-5*t)', 0.6, k['K14']['start'] + 0.05 + 0.32 * j, 0.45)
fc.append(f"anoisesrc=d=0.4:c=white:a=0.5:r=48000,highpass=f=2500,afade=t=in:d=0.15,afade=t=out:st=0.2:d=0.2,volume=0.10,aformat=channel_layouts=stereo,adelay={int(max(0, k['FB1']['start'] - 0.1) * 1000)}:all=1[fbw]"); mixl.append('[fbw]')
def amb(lbl, a, b, lo, hi, vol):
    a0 = max(0, a - 0.3)
    fc.append(f"anoisesrc=d={b - a0:.2f}:c=pink:a=0.5:r=48000,bandpass=f={(lo + hi) // 2}:w={hi - lo},volume={vol},"
              f"afade=t=in:d=0.3,afade=t=out:st={b - a0 - 0.3:.2f}:d=0.3,aformat=channel_layouts=stereo,adelay={int(a0 * 1000)}:all=1[{lbl}]"); mixl.append(f'[{lbl}]')
for c in CUTS:
    a, b = c['start'], c['start'] + c['dur']
    if c['id'] in ('K6', 'K7', 'K8', 'K9', 'K10', 'K11', 'K12'): amb(f"am_{c['id']}", a, b, 100, 500, 0.010)   # 빈 교실
    else: amb(f"am_{c['id']}", a, b, 300, 2800, 0.016)                                                     # 교무실
fc.append(f"anoisesrc=d={MAIN}:c=brown:a=0.5:r=48000,lowpass=f=350,volume=0.0105,afade=t=in:d=0.5,afade=t=out:st={MAIN - 0.4}:d=0.4,aformat=channel_layouts=stereo[room]"); mixl.append('[room]')
# 배경음: 담임의 하루(class·pulse, 바쁨) → 빈 교실(warm, 끊지 않고) → 끝 문자 직전 뚝
BGM_SECT = [('class', 1.0, k['K4']['start'] + k['K4']['dur'], 0.3), ('class', k['K5']['start'] + 0.1, k['K6']['start'] - 0.1, 0.6),
            ('warm', k['K6']['start'] + 0.3, k['K13']['start'] - 0.2, 1.0, 1.6), ('pulse', k['K13']['start'] + 0.3, L['J14'] - 0.2)]
BGM_I = bgm.make(BGM_SECT, [(VO / f'{lid}.wav', st) for lid, st in L.items()], MAIN, B / 'bgm.wav', target_lufs=-22.0, duck_db=-15.0, release=0.2)
ins += ['-i', B / 'bgm.wav']; mixl.append(f'[{len(ins) // 2 - 1}:a]')

fc.append(''.join(mixl) + f"amix=inputs={len(mixl)}:normalize=0,apad=whole_dur={MAIN},atrim=0:{MAIN}[aout]")
run(['ffmpeg', '-y', '-loglevel', 'error', *ins, '-filter_complex', ';'.join(fc), '-map', '[aout]', '-ar', '48000', B / 'mix_raw.wav'])
def meas(p):
    m = subprocess.run(['ffmpeg', '-i', str(p), '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', m)[-1]), float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', m)[-1])
I0, _ = meas(B / 'mix_raw.wav')
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', B / 'mix_raw.wav', '-af', f'volume={-14.0 - I0:.2f}dB,alimiter=limit=0.58:level=false:attack=2:release=60', '-ar', '48000', B / 'mix_main.wav'])
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', ENDING, '-vn', '-af', f'atrim=start=0.33,asetpts=PTS-STARTPTS,afade=t=in:d=0.02,apad=whole_dur={END_LEN}', '-ar', '48000', '-ac', '2', B / 'ending.wav'])   # 엔딩곡 앞에 잘려 붙은 \'싸-\' 0.33초 자름
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

for _a, _b in [(0.62, MAIN)]:
    ev(_a, _b, 'Label', r'{\an7\pos(40,140)\fs50}담임과 여고생, 몸이 바뀌었다', 6)
ev(0.0, 0.62, 'Label', r'{\an5\pos(540,640)\bord0\shad0\1c&H000000&\1a&H28&\p1\fad(0,120)}m 0 0 l 1080 0 1080 420 0 420{\p0}', 9)
ev(0.0, 0.62, 'Label', r'{\an5\pos(540,500)\fs50\bord0\fad(0,120)}소울체인지 11화', 10)
ev(0.0, 0.62, 'Label', r'{\an5\pos(540,610)\fs62\1c&HFFFFFF&\3c&H2020D0&\4c&H2020D0&\bord12\fad(0,120)}하은이 오는 날, 담임의 하루', 10)
ev(0.0, 0.62, 'Emph', r'{\an5\pos(540,750)\fs96\bord6\3c&H000000&\fad(0,120)}상담은 언제 해?', 10)
scene(cs('K1'), cs('K1') + 2.2, '아침 · 교무실')
say('J01', '좋아. 오늘은 하은이 상담만 제대로 하자.', '지우 영혼', PINK)
narr(cs('K2') + 0.2, ce('K2'), r'(학생은 몰랐던 담임의 하루)', 40, 300)
say('J03', r'아니... 이런 걸 하루에 다 하라고?\N도대체 수업할 시간이 있긴 한 거야?', '지우 영혼', PINK)
for j, s in enumerate(['1교시 뒤', '점심시간', '6교시 뒤']):
    ev(cs('K4') + j * 1.2, cs('K4') + j * 1.2 + 1.15, 'Label', r'{\an5\pos(540,860)\fs110\1c&H5AE3FF&\bord8\fad(80,80)}상담: ' + s + (' → 밀림' if j < 2 else ''), 10)
say('T05', '...그래서 내가 맨날 과자로 버텼지.', '(속마음) 담임 영혼', SKY, 'Mono')
scene(cs('K6'), cs('K6') + 2.2, '방과 후 · 빈 교실')
narr(cs('K6') + 0.3, ce('K6'), r"(가족 여행인데 체험학습 신청 없이\N'두통' 병결)", 40, 380)
say('J06', r'너 이렇게 될 줄 몰랐어?\N언젠가는 다 들통날 수 있는 일이었어.', '지우 영혼', PINK)
say('J07', r'네가 병결로 처리되더라도, 너는 거짓말쟁이라고\N계속 꼬리표가 따라다닐 거야.', '지우 영혼', PINK)
say('J08', r'...근데 이렇게 말해도 되나?\N한마디 잘못하면 정서학대라던데.', '(속마음) 지우 영혼', PINK, 'Mono')
narr(L['J08'] + 2.6, ce('K8'), r'(요즘 담임들의 속마음)', 560, 300)
say('J09', '에이, 내가 이런 말 할 자격이 있나.', '지우 영혼', PINK)
say('H10', '...선생님, 죄송합니다. 다시 이런 일 없을게요.', '하은')
say('H11', '엄마는... 제가 알아서 할게요.', '하은')
say('J12', r'...나도 그랬어.\N아, 아니, 선생님도... 그런 적 있어.', '지우 영혼', PINK)
narr(L['J12'] + 1.5, ce('K12'), r'(거의 들킬 뻔)', 600, 300)
scene(cs('K13'), ce('K13'), '그날 저녁')
say('J14', '...엄마가, 온다고?', '지우 영혼', PINK)

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
(B / 'ep11.ass').write_text(head + '\n' + '\n'.join(EV) + '\n', encoding='utf-8')

# ---------- 6. 합치기 ----------
en_j = '+'.join(f"between(t,{c['start']},{c['start'] + c['dur'] - 0.001:.3f})" for c in CUTS if c['pip'] == 'pip') or '0'
en_t = '+'.join(f"between(t,{c['start']},{c['start'] + c['dur'] - 0.001:.3f})" for c in CUTS if c['pip'] == 'pip_t') or '0'
vf = (f"[1:v]scale=300:300[pj];[2:v]scale=300:300[pt];"
      f"[0:v][pj]overlay=x=750:y=130:enable='{en_j}'[a];[a][pt]overlay=x=750:y=130:enable='{en_t}'[b];"
      f"[b]ass={B / 'ep11.ass'}:fontsdir={KIT / 'fonts'},format=yuv420p[vout]")
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', B / 'joined.mp4', '-i', KIT / 'pip.png', '-i', KIT / 'pip_t.png',
     '-filter_complex', vf, '-map', '[vout]', '-t', MAIN, '-r', FPS, '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', B / 'main_v.mp4'])
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', ENDING, '-an', '-vf', f'fps={FPS},format=yuv420p,setsar=1', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', B / 'ending_v.mp4'])
(B / 'vlist.txt').write_text(f"file '{B / 'main_v.mp4'}'\nfile '{B / 'ending_v.mp4'}'\n")
out = HERE / 'ep11_v2.mp4'
run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', B / 'vlist.txt', '-i', B / 'mix.wav',
     '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-t', TOT, '-movflags', '+faststart', out])
json.dump({'main': MAIN, 'total': TOT, 'loudness_LUFS': I2, 'true_peak_dBTP': TP2,
           'cuts': [{kk: (str(vv) if isinstance(vv, pathlib.Path) else vv) for kk, vv in c.items()} for c in CUTS],
           'lines': {lid: {'start': L[lid], 'end': round(end_(lid), 3), 'file': SPEC[lid]['f'], 'range': SPEC[lid]['r']} for lid in sorted(L, key=L.get)},
           'subs': SUBS, 'bgm': BGM_SECT}, open(HERE / 'timeline_v2.json', 'w'), ensure_ascii=False, indent=1)
print('OK', out, TOT)

