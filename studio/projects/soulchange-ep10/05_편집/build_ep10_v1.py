#!/usr/bin/env python3
"""소울체인지 10화 편집 v1 (대본 v1.1 「도와줘요」).

흐름: 그날 밤 현석이네(현석 "엄마. 나한테 왜 그랬어…도와줘요" → 엄마 손이 향수병을 내려놓음 → 창가 뒷모습, 말없이 생각)
→ 다음 날 아침 벤치(8화 K8 재사용: 이어폰) "어제, 엄마한테 말했어." → 지우 몸(김병만 영혼) 눈시울 "잘했다, 현석아." → 어깨 토닥 실수 "아, 미안. …어깨."
→ 오후 교무실: 엄마·현석 손잡고 → 엄마 "도와주세요." → 교감 도움 전화(립싱크) → 상담실 섬유유연제·향수병 "저도 바꿀게요, 향수." / "…같은 거 쓰셨구나." / 지우 속마음 "…다행이다."
→ 단톡 하은 귀국 → 김병만 DM "근데 너, 생결 쓰고 PC방 간 그날은?" → 지우(담임 몸) "…헐." → 1화 게시물 '좋아요' 회상 0.6초
사용: python3 build_ep10_v1.py [--plan]
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
ENDING = B / 'ending_ep10.mp4'      # make_ending.py 10 금
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
    'H01': dict(f='E10-01_hyeonseok_evan.mp3', r=[(0, 3.08)], tempo=1.0),
    'H02': dict(f='E10-02_hyeonseok_evan.mp3', r=[(0, 11.08)], tempo=1.0, gap=0.45),
    'H03': dict(f='E10-03_hyeonseok_evan.mp3', r=[(0, 8.05)], tempo=1.0, gap=0.5),
    'H05': dict(f='E10-05_hyeonseok_evan.mp3', r=[(0, 2.85)], tempo=1.0),
    'T06': dict(f='E10-06_teacher_inner_teacher.mp3', r=[(0, 2.27)], tempo=1.0),
    'T07': dict(f='E10-07_teacher_studentbody.mp3', r=[(0, 2.69)], tempo=1.05, gap=0.3),
    'M08': dict(f='E10-08_mother_soraya.mp3', r=[(0, 8.20)], tempo=1.0, gap=0.4),
    'C10': dict(f='E10-10_choi_celine.mp3', r=[(0, 3.24)], tempo=1.0, gap=0.25),
    'M11': dict(f='E10-11_mother_soraya.mp3', r=[(0, 2.27)], tempo=1.0),
    'J12': dict(f='E10-12_jiu_inner_student.mp3', r=[(0, 2.43)], tempo=1.0),
    'T13': dict(f='E10-13_teacher_dm_teacher.mp3', r=[(0, 7.47)], tempo=1.05, gap=0.3),
    'J14': dict(f='E10-14_jiu_teacherbody.mp3', r=[(0, 2.43)], tempo=1.0, gap=0.2),
}
D = vp.prep(SPEC, V, VO)
LS = {'VP09': ('E10-09_vp_arthur.mp3', 0.0, 5.15)}   # 교감 립싱크 컷(생성 오디오와 같은 0초)
for lid, (fn, a_, b_) in LS.items():
    x = vp.decode(V / fn, a_, b_); tmp = VO / f'{lid}_t.wav'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(vp.SR), '-ac', '1', '-i', '-', str(tmp)], input=x.astype(np.float32).tobytes(), check=True)
    g = -18.0 - vp.lufs(tmp)
    run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-af', f'volume={g:.2f}dB,alimiter=limit=0.7:level=false:attack=1:release=50', '-ar', '48000', '-c:a', 'pcm_s16le', VO / f'{lid}.wav'])
    tmp.unlink(); D[lid] = round(dur_of(VO / f'{lid}.wav'), 3); SPEC[lid] = dict(f=fn, r=[(a_, b_)], tempo=1.0)
INNER = {'T06', 'J12'}
PHONE = set(); WHISPER = set()

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

cut('K0', K('K3'), 0.2, 1.0, note='첫 1초: 엄마 손이 향수병을 꽉 쥠')
c0 = t; e = at('H01', c0 + 1.0)
cut('K1', K('K1'), 0, max(e + 0.4 - c0, 4.6), hold=True, note='밤 거실, 현석 어깨 너머 + 엄마 손')
c0 = t; e = at('H02', c0 + 0.2)
cut('K2', K('K2'), 0, e + 0.4 - c0, stretch=1.15, hold=True, note='현석 소매를 당겨 쥠(한여름 긴팔)')
c0 = t; e = at('H03', c0 + 0.2)
cut('K3', K('K3'), 0, e + 0.5 - c0, stretch=1.15, hold=True, note='엄마 손이 향수병을 내려놓고 손을 뗌')
cut('K4', K('K4'), 0, 4.6, note='엄마 창가 뒷모습, 손으로 입 — 말없이 생각')
# 다음 날 아침 벤치 — 8화 K8 재사용(지우 몸 조심조심 앉음 → 이어폰 받음)
c0 = t; e = at('H05', c0 + 3.3)
cut('K5', P / 'soulchange-ep08/04_생성물/clips/K8.mp4', 0, max(e + 0.3 - c0, 5.0), pip='pip_t', hold=True, note='8화 K8 재사용: 벤치 이어폰')
c0 = t; e = at('T06', c0 + 1.0)
cut('K6', K('K6'), 0, max(e + 0.6 - c0, 4.0), pip='pip_t', note='지우 몸 눈시울 끄덕')
c0 = t; e = at('T07', c0 + 2.6)
cut('K7', K('K7'), 0, max(e + 0.3 - c0, 5.0), pip='pip_t', hold=True, note='어깨 토닥 → 움찔 → 손 거둠')
cut('K8', K('K8'), 0, 3.6, note='엄마·현석 손잡고 교무실로')
c0 = t; e = at('M08', c0 + 0.3)
cut('K9', K('K9'), 0, e + 0.4 - c0, hold=True, stretch=1.1, note='엄마 뒷모습 + 최 쌤 끄덕')
c0 = t; e = at('VP09', c0 + 0.0)
cut('K10', K('K10'), 0, max(e + 0.3 - c0, dur_of(K('K10')) - 0.05), hold=True, note='교감 도움 전화(립싱크)')
c0 = t; e = at('C10', c0 + 1.6); e = at('M11', e + 0.3); e = at('J12', e + 0.35)
cut('K11', K('K11'), 0, e + 0.4 - c0, stretch=1.15, hold=True, note='섬유유연제 봉투 + 향수병 슬쩍')
# 단톡 → DM (코드)
c0 = t; CHAT0 = c0 + 0.4
e = at('T13', c0 + 2.4)
cut('K12', P / 'soulchange-ep06/04_생성물/clips/H3_K10.mp4', 0.2, e + 0.5 - c0, pip='pip_t', fx='chat', note='코드: 단톡 하은 귀국 → 김병만 DM')
# 지우(담임 몸) "…헐." — 7화 K12 놀란 얼굴 재사용 → 1화 '좋아요' 회상
c0 = t; e = at('J14', c0 + 0.35)
cut('K13', P / 'soulchange-ep07/04_생성물/clips/K12_elem.mp4', 2.3, max(e + 0.2 - c0, 1.6), pip='pip', zoom=(1.25, 0.5, 0.0), note='7화 K12 재사용: 담임 몸 폰 보고 굳음')
cut('FB1', P / 'soulchange-ep01/05_편집/ep1_공개본_720p.mp4', 1.2, 1.4, vfx=FB, hold=True, note='회상 1화: 생결 내고 PC방 게시물 + 담임 좋아요')
MAIN = round(t, 3); TOT = round(MAIN + END_LEN, 3)
print('본편', MAIN, '합계', TOT)
for c in CUTS:
    avail = (dur_of(c['src']) - c['ss']) * c['stretch']
    print(f"  {c['id']:5s} {c['start']:6.2f} +{c['dur']:.2f}  x{c['stretch']:.2f}" + (f"  멈춤 {c['dur'] - avail:.2f}" if c['dur'] > avail + 0.02 and not c['fx'] else ''))
for lid in sorted(L, key=L.get): print(f"    {lid:6s} {L[lid]:6.2f}-{end_(lid):6.2f}")
if '--plan' in sys.argv: sys.exit(0)


def chat_frames(c):
    """K12: 지우 폰(지금 김병만) 반 단톡 → DM 화면."""
    n = round(c['dur'] * FPS)
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', '0.3', '-i', str(c['src']), '-frames:v', '1', '-vf', 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    bg = Image.frombytes('RGB', (W, H), raw[:W * H * 3]).filter(ImageFilter.GaussianBlur(16))
    bg = Image.fromarray((np.asarray(bg, float) * 0.5).astype(np.uint8))
    chat = [(CHAT0, '민서', '하은이 내일 귀국ㅋ'), (CHAT0 + 0.5, '반장', '미인정결 3일 각'), (CHAT0 + 0.9, '체육부장', '오사카 기념품 사 오냐ㅋ')]
    DMT = L['T13']
    out = []
    for i in range(n):
        tt = c['start'] + i / FPS
        im = bg.copy(); d = ImageDraw.Draw(im)
        x0, y0, pw, ph = 110, 260, 860, 900
        d.rounded_rectangle([x0, y0, x0 + pw, y0 + ph], 70, fill=(22, 22, 26))
        sx0, sy0, sx1, sy1 = x0 + 22, y0 + 22, x0 + pw - 22, y0 + ph - 22
        dm = tt >= DMT - 0.3
        d.rounded_rectangle([sx0, sy0, sx1, sy1], 52, fill=(236, 238, 244) if dm else (186, 206, 224))
        d.rectangle([sx0, sy0 + 40, sx1, sy0 + 150], fill=(222, 225, 234) if dm else (170, 192, 214))
        d.text((sx0 + 34, sy0 + 95), '<  김병만 쌤 (지금 지우 몸)' if dm else '<  우리 반 (28)', font=f(40), fill=(30, 30, 30), anchor='lm')
        y = sy0 + 190
        if not dm:
            for ta, who, s in chat:
                if tt < ta: continue
                d.text((sx0 + 40, y), who, font=f(32), fill=(60, 60, 70)); y += 44
                tw = d.textlength(s, font=f(46)); d.rounded_rectangle([sx0 + 30, y, sx0 + 30 + tw + 44, y + 78], 28, fill=(255, 255, 255))
                d.text((sx0 + 52, y + 16), s, font=f(46), fill=(30, 30, 30)); y += 100
        else:
            d.text((sx1 - 34, y), '담임 영혼이 보냄', font=f(34), fill=(40, 110, 200), anchor='ra'); y += 54
            sc = min(1.0, 0.6 + (tt - DMT) / 0.12 * 0.4) if tt >= DMT else 0
            if sc > 0:
                lines = ['현석이 일은 잘 끝났다.', '근데 너, 생결 쓰고', 'PC방 간 그날은?', '아직 아무한테도', '말 안 했지?']
                fs = int(50 * sc); lh = int(66 * sc); tw = max(d.textlength(l, font=f(fs)) for l in lines); bh = lh * len(lines) + 34
                d.rounded_rectangle([sx1 - 30 - tw - 48, y, sx1 - 30, y + bh], 30, fill=(80, 150, 230))
                for j, l in enumerate(lines): d.text((sx1 - 54, y + 17 + j * lh), l, font=f(fs), fill=(255, 255, 255), anchor='ra')
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
    if c['fx'] == 'chat':
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
    ch += ",acompressor=threshold=-20dB:ratio=3:attack=5:release=120"
    ch += f",aformat=channel_layouts=stereo,adelay={int(st * 1000)}:all=1[v{i}]"
    fc.append(ch); mixl.append(f'[v{i}]')
def sfx(lbl, expr, d, at_, vol=1.0):
    fc.append(f"aevalsrc='{expr}':d={d}:s=48000,volume={vol},aformat=channel_layouts=stereo,adelay={int(at_ * 1000)}:all=1[{lbl}]"); mixl.append(f'[{lbl}]')
def noise(lbl, d, at_, filt, vol):
    fc.append(f"anoisesrc=d={d}:c=pink:a=0.5:r=48000,{filt},volume={vol},aformat=channel_layouts=stereo,adelay={int(at_ * 1000)}:all=1[{lbl}]"); mixl.append(f'[{lbl}]')
k = {c['id']: c for c in CUTS}
k = {c['id']: c for c in CUTS}
SEND = '0.18*sin(2*PI*(700+1600*t)*t)*exp(-12*t)'
DINGX = '0.16*sin(2*PI*1320*t)*lt(t,0.08)+0.16*sin(2*PI*1760*t)*gt(t,0.12)*lt(t,0.24)'
sfx('bottle', '0.30*sin(2*PI*2400*t)*exp(-40*t)', 0.2, k['K3']['start'] + 2.6, 0.5)            # 병 내려놓는 소리
for j in range(3): sfx(f'ding{j}', DINGX, 0.3, CHAT0 + [0, 0.5, 0.9][j], 0.45)
sfx('send', SEND, 0.35, end_('T13') + 0.05, 0.5)
sfx('boing', '0.20*sin(2*PI*(300+500*t)*t)*exp(-6*t)', 0.4, L['J14'], 0.5)
fc.append(f"anoisesrc=d=0.4:c=white:a=0.5:r=48000,highpass=f=2500,afade=t=in:d=0.15,afade=t=out:st=0.2:d=0.2,volume=0.10,aformat=channel_layouts=stereo,adelay={int((k['FB1']['start'] - 0.1) * 1000)}:all=1[fbw]"); mixl.append('[fbw]')
def amb(lbl, a, b, lo, hi, vol):
    a0 = max(0, a - 0.3)
    fc.append(f"anoisesrc=d={b - a0:.2f}:c=pink:a=0.5:r=48000,bandpass=f={(lo + hi) // 2}:w={hi - lo},volume={vol},"
              f"afade=t=in:d=0.3,afade=t=out:st={b - a0 - 0.3:.2f}:d=0.3,aformat=channel_layouts=stereo,adelay={int(a0 * 1000)}:all=1[{lbl}]"); mixl.append(f'[{lbl}]')
for c in CUTS:
    a, b = c['start'], c['start'] + c['dur']
    if c['id'] in ('K0', 'K1', 'K2', 'K3', 'K4'): amb(f"am_{c['id']}", a, b, 100, 400, 0.010)          # 밤 집 — 아주 조용
    elif c['id'] in ('K5', 'K6', 'K7'): amb(f"am_{c['id']}", a, b, 150, 700, 0.016)                  # 운동장 바람
    else: amb(f"am_{c['id']}", a, b, 300, 2800, 0.016)
fc.append(f"anoisesrc=d={MAIN}:c=brown:a=0.5:r=48000,lowpass=f=350,volume=0.0105,afade=t=in:d=0.5,afade=t=out:st={MAIN - 0.4}:d=0.4,aformat=channel_layouts=stereo[room]"); mixl.append('[room]')
# 배경음: 밤 집(느린 피아노 warm) → 벤치(warm) → 어깨 실수 뒤 가벼움(class) → 교무실 도움 요청(warm) → 향수 동지(class) → 단톡(pulse) → "헐" 직전 뚝
BGM_SECT = [('warm', 1.0, k['K5']['start'] - 0.1), ('warm', k['K5']['start'] + 0.2, k['K7']['start'] + 2.2),
            ('class', end_('T07') + 0.1, k['K8']['start']), ('warm', k['K8']['start'] + 0.1, k['K11']['start']),
            ('class', k['K11']['start'] + 0.1, k['K12']['start']), ('pulse', k['K12']['start'], L['J14'] - 0.3)]
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
ev(0.0, 0.62, 'Label', r'{\an5\pos(540,500)\fs50\bord0\fad(0,120)}소울체인지 10화', 10)
ev(0.0, 0.62, 'Label', r'{\an5\pos(540,610)\fs62\1c&HFFFFFF&\3c&H2020D0&\4c&H2020D0&\bord12\fad(0,120)}그날 밤, 현석이네 집', 10)
ev(0.0, 0.62, 'Emph', r'{\an5\pos(540,750)\fs96\bord6\3c&H000000&\fad(0,120)}엄마, 나한테 왜 그랬어', 10)
scene(cs('K1'), cs('K1') + 2.4, '그날 밤 · 현석이네 집')
say('H01', '엄마. 나한테 왜 그랬어.', '현석')
say('H02', r'나, 많이 힘들었어. 나도 노력했어.', '현석', end=L['H02'] + D['H02'] * 0.42)
say('H02', r'엄마 냄새가 나면 숨이 막혔는데...\N그래도 엄마 사랑해.', '현석', start=L['H02'] + D['H02'] * 0.42, grp='H02b')
say('H03', r'근데 가끔은, 그냥 훨훨\N날아가고 싶었어.', '현석', end=L['H03'] + D['H03'] * 0.5)
say('H03', r'...이제 버틸 힘이 없어. 도와줘요.', '현석', start=L['H03'] + D['H03'] * 0.5, grp='H03b')
scene(cs('K5'), cs('K5') + 2.4, '다음 날 아침 · 운동장 벤치')
say('H05', '...어제, 엄마한테 말했어.', '현석')
say('T06', '...잘했다, 현석아.', '(속마음) 담임 영혼', SKY, 'Mono')
say('T07', '아, 미안. ...어깨.', '담임 영혼', SKY)
narr(L['T07'] + 0.2, ce('K7'), r'(싫어하는 거:\N갑자기 어깨 만지는 거)', 40, 430)
scene(cs('K8'), cs('K8') + 2.2, '그날 오후 · 교무실')
say('M08', r'어제 애가... 저한테 그러더라고요.', '현석 어머니', end=L['M08'] + D['M08'] * 0.4)
say('M08', r'저도 어떻게 해야 할지 모르겠어요.\N도와주세요.', '현석 어머니', start=L['M08'] + D['M08'] * 0.4, grp='M08b')
say('VP09', r'...네, 학교입니다. 아이랑 어머님이\N같이 도움을 받고 싶어 하셔서요.', '교감')
narr(cs('K10') + 0.2, ce('K10'), r'(이번엔 다른 전화)', 600, 430)
scene(cs('K11'), cs('K11') + 2.0, '상담실')
say('C10', '...저도 바꿀게요, 향수.', '최 선생님 (지금 담임)')
say('M11', '...같은 거 쓰셨구나.', '현석 어머니')
narr(L['C10'] - 0.2, end_('M11'), r'(어색한 동지애)', 600, 430)
say('J12', '...다행이다.', '(속마음) 지우 영혼', PINK, 'Mono')
scene(cs('K12'), cs('K12') + 1.8, '쉬는 시간 · 지우 폰(지금 김병만 쌤)')
say('J14', '...헐.', '지우 영혼', PINK)
scene(cs('FB1'), ce('FB1'), '1화 · 생결 내고 PC방 간 날')
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
(B / 'ep10.ass').write_text(head + '\n' + '\n'.join(EV) + '\n', encoding='utf-8')

# ---------- 6. 합치기 ----------
en_j = '+'.join(f"between(t,{c['start']},{c['start'] + c['dur'] - 0.001:.3f})" for c in CUTS if c['pip'] == 'pip') or '0'
en_t = '+'.join(f"between(t,{c['start']},{c['start'] + c['dur'] - 0.001:.3f})" for c in CUTS if c['pip'] == 'pip_t') or '0'
vf = (f"[1:v]scale=300:300[pj];[2:v]scale=300:300[pt];"
      f"[0:v][pj]overlay=x=750:y=130:enable='{en_j}'[a];[a][pt]overlay=x=750:y=130:enable='{en_t}'[b];"
      f"[b]ass={B / 'ep10.ass'}:fontsdir={KIT / 'fonts'},format=yuv420p[vout]")
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', B / 'joined.mp4', '-i', KIT / 'pip.png', '-i', KIT / 'pip_t.png',
     '-filter_complex', vf, '-map', '[vout]', '-t', MAIN, '-r', FPS, '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', B / 'main_v.mp4'])
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', ENDING, '-an', '-vf', f'fps={FPS},format=yuv420p,setsar=1', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', B / 'ending_v.mp4'])
(B / 'vlist.txt').write_text(f"file '{B / 'main_v.mp4'}'\nfile '{B / 'ending_v.mp4'}'\n")
out = HERE / f'ep10_{TAG_}.mp4'
run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', B / 'vlist.txt', '-i', B / 'mix.wav',
     '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-t', TOT, '-movflags', '+faststart', out])
json.dump({'main': MAIN, 'total': TOT, 'loudness_LUFS': I2, 'true_peak_dBTP': TP2,
           'cuts': [{kk: (str(vv) if isinstance(vv, pathlib.Path) else vv) for kk, vv in c.items()} for c in CUTS],
           'lines': {lid: {'start': L[lid], 'end': round(end_(lid), 3), 'file': SPEC[lid]['f'], 'range': SPEC[lid]['r']} for lid in sorted(L, key=L.get)},
           'subs': SUBS, 'bgm': BGM_SECT}, open(HERE / f'timeline_{TAG_}.json', 'w'), ensure_ascii=False, indent=1)
print('OK', out, TOT)

