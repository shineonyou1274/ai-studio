#!/usr/bin/env python3
"""소울체인지 4화 편집 생성기 v11 (사장님 10/24 지적: 단톡 폰 화면·카톡 울림, 일본 사진, 골탕 대사, 다급한 담임 영혼 새 컷, 학부모 해외로밍 전화, 나이 든 교감 목소리). 이전: v3 (v2 + Gemini·블라인드 검수 반영: 교감 목소리 교체·립싱크, 로봇 같은 줄 재녹음, 공항 발음, 영혼 원 확대, 보낸 문자 말풍선 아래로).

키트 규칙: soulchange_style.ass 헤더만 사용(\\fs \\fn \\i 덮어쓰기 없음), 말풍선 860/1000/1160,
Emph 1번, PIP 오른쪽 위 200px 컷 내내, 끝 카드 1.5초, 대사 -18 LUFS → 최종 -14 LUFS / TP -3dB.
사용: python3 build_ep4.py  (결과: build/ep4_v1.mp4)
"""
import os, subprocess, json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
KIT = pathlib.Path('/home/user/youtube-ops/series/_soulchange_kit')
EP = HERE.parent
V = EP / '04_생성물' / 'voices'
C = EP / '04_생성물' / 'clips'
B = HERE / 'build'; B.mkdir(exist_ok=True)
FPS = 30

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: raise SystemExit(' '.join(map(str, cmd)) + '\n' + r.stderr[-2000:])

# ---------- 컷 (v11: 해외로밍 문자 → 단톡 폰 화면(일본 사진) → "하은이 지금 일본이다" → 이건 못 참지 → 담임 영혼 다급("안 돼, 보내지 마"·"아무것도 하지 마") → 지우 "골탕 좀 드셔 보세요~" 전송 → 하은이 어머니 해외로밍 전화 "실수하신 겁니다" → 교감) ----------
K4 = KIT/'episodes/ep4/clips'
CUTS = [
    ('N3',  5.0, C/'N3.mp4', 0.0, 'pip',   1.0, 0),
    ('N2',  5.6, C/'N2.mp4', 0.0, 'pip_t', 1.11, 0),
    ('N4',  4.0, C/'N4.mp4', 0.0, 'pip_t', 1.0, 0),
    ('N1',  4.5, K4/'N1.mp4', 0.0, 'pip', 1.0, 0),
    ('N7',  4.5, C/'N7.mp4', 0.0, 'pip_t', 1.0, 0),   # v11 새 컷: 지우 몸(담임 영혼) 다급하게 폰 입력
    ('m1',  4.0, K4/'m1.mp4', 0.0, 'pip', 1.0, 0),
    ('m2',  5.4, K4/'m2.mp4', 0.0, 'pip', 1.07, 0),
    ('N3b', 1.9, C/'N3.mp4', 3.0, 'pip',   1.0, 0),   # 보낸 문자 낭독 끝까지 담임 몸(지우 영혼) 폰 화면 위에서
    ('N6',  4.2, C/'N6.mp4', 0.8, 'pip_t', 1.0, 0),
    ('N5',  4.5, C/'N5.mp4', 0.0, 'pip',   1.0, 0),   # 해외로밍 전화 수신
    ('N1b', 3.0, K4/'N1.mp4', 2.0, 'pip', 1.0, 0),    # 전화 듣는 담임 몸(지우 영혼)
    ('m3',  4.25, K4/'m3.mp4', 1.1, 'pip', 1.08, 0),  # 교감 입 움직임 맞춤(대사는 컷 시작 + 0.5초)
]
END = 1.5
t = 0; ST = {}
for c in CUTS:
    ST[c[0]] = round(t, 3); t += c[1]
VID_END = round(t, 3); TOT = round(VID_END + END, 3)

# ---------- 영상 조각 ----------
seg_list = []
for cid, dur, src, ss, pip, stretch, freeze in CUTS:
    out = B / f'seg_{cid}.mp4'
    nat = dur - freeze
    vf = (f"[0:v]trim=start={ss}:duration={nat/stretch:.3f},setpts=(PTS-STARTPTS)*{stretch},"
          f"scale=1080:1920:flags=lanczos,setsar=1,fps={FPS}")
    if freeze:
        vf += (f",tpad=stop_mode=clone:stop_duration={freeze},"
               f"zoompan=z='if(lt(on,{int(nat*FPS)}),1,1+0.10*(on-{int(nat*FPS)})/{int(freeze*FPS)})':"
               f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps={FPS}")
    vf += f",format=yuv420p[b];[1:v]scale=300:300[p];[b][p]overlay=x=750:y=70[v]"
    run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(src), '-i', str(KIT / f'{pip}.png'),
         '-filter_complex', vf, '-map', '[v]', '-frames:v', str(round(dur * FPS)), '-an',
         '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', str(out)])
    seg_list.append(out)
# 끝 카드
(B / 't_end1.txt').write_text('소울체인지 4화', encoding='utf-8')
(B / 't_end2.txt').write_text('다음 화에 계속', encoding='utf-8')
font = KIT / 'fonts/Jua-Regular.ttf'
run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', f'color=c=0x0b0b12:s=1080x1920:r={FPS}:d={END}',
     '-vf', f"drawtext=fontfile={font}:textfile={B/'t_end1.txt'}:fontsize=96:fontcolor=0xffe35a:x=(w-text_w)/2:y=820,"
            f"drawtext=fontfile={font}:textfile={B/'t_end2.txt'}:fontsize=48:fontcolor=0xdddddd:x=(w-text_w)/2:y=980,"
            "fade=t=in:st=0:d=0.3,format=yuv420p",
     '-frames:v', str(round(END * FPS)), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', str(B / 'seg_end.mp4')])
seg_list.append(B / 'seg_end.mp4')
(B / 'list.txt').write_text(''.join(f"file '{p}'\n" for p in seg_list))
run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', str(B / 'list.txt'), '-c', 'copy', str(B / 'joined.mp4')])

# ---------- 대사 (파일, 시작, 배속, 속마음 잔향) ----------
HALL = 'aecho=0.85:0.6:45:0.12'
W = V/'v4'; X = V/'v5'
Y = V/'v8'
LINES = [
    (X/'S4v4_해외에서보냈네.wav', 1.2, 1.0, True),
    (Y/'T5_일본이라고.wav', 10.0, 1.0, True),
    (Y/'T6_지금일본이다.wav', 10.9, 1.0, False),       # 보낸 사람(담임 영혼) 화면이라 낭독
    (W/'L1_지우속마음_못참지.wav', 14.9, 1.0, True),
    (Y/'T7e_안돼안돼_끝낮춤.wav', 19.4, 1.0, True),            # 담임 영혼 속마음, 다급
    (Y/'T8c_아무것도하지마.wav', 21.8, 1.0, False),     # 보낸 사람(담임 영혼) 화면이라 낭독
    (Y/'S5_골탕.wav', 24.1, 1.0, True),                 # 지우 영혼 속마음, 보내기 직전
    (Y/'S6_보낸문자_일본.wav', 27.1, 1.08, False),
    (V/'v7/GT_a_끅끅_teacher_low_-28.wav', 29.6, 1.0, False),
    (X/'T2v4_보냈구나.wav', 35.4, 1.0, True),
    (Y/'P_엄마A_Vera_전화.wav', 40.8, 1.0, False),      # 하은이 어머니 = Vera(사장님 선택 A), 해외로밍 전화 음질
    (Y/'VP_교감A_Arthur.wav', 47.1, 1.0, False),        # 교감 = Arthur (사장님 선택 A)
]
ins, fc, mixl = [], [], []
for i, (f, at, tempo, hall) in enumerate(LINES):
    ins += ['-i', str(f)]
    chain = f"[{i}:a]aresample=48000,aformat=channel_layouts=mono"  # 입력은 이미 -18 LUFS로 맞춘 파일(loudnorm은 타이밍을 밀어서 쓰지 않음)
    if tempo != 1.0: chain += f",atempo={tempo}"
    if hall: chain += f",{HALL}"
    chain += f",acompressor=threshold=-20dB:ratio=3:attack=5:release=120,aformat=channel_layouts=stereo,adelay={int(at*1000)}:all=1[v{i}]"
    fc.append(chain); mixl.append(f'[v{i}]')

def sfx(lbl, expr, d, at, vol=1.0):
    fc.append(f"aevalsrc='{expr}':d={d}:s=48000,volume={vol},aformat=channel_layouts=stereo,adelay={int(at*1000)}:all=1[{lbl}]")
    mixl.append(f'[{lbl}]')
SMS = '0.22*sin(2*PI*1320*t)*lt(t,0.08)+0.22*sin(2*PI*1760*t)*gt(t,0.12)*lt(t,0.22)'   # 문자 도착 "띠링"
SEND = '0.18*sin(2*PI*(700+1600*t)*t)*exp(-12*t)'                                     # 전송 "슉"
POP = '0.2*sin(2*PI*980*t)*exp(-30*t)'                                                # 수신 "톡"
KT = '0.2*sin(2*PI*1568*t)*lt(t,0.07)+0.2*sin(2*PI*2093*t)*gt(t,0.09)*lt(t,0.2)'   # 단톡 알림 "띵동"(카톡 실제 소리는 쓰지 않음)
RING = '0.16*sin(2*PI*880*t)*(0.6+0.4*sin(2*PI*16*t))*lt(mod(t,0.7),0.45)'          # 전화 벨
sfx('s0', SMS, 0.3, 0.05, 0.6); sfx('thud', '0.5*sin(2*PI*(90-50*t)*t)*exp(-9*t)', 0.5, 0.3)
sfx('p0', POP, 0.2, 5.1); sfx('k1', KT, 0.25, 7.2, 0.4); sfx('k2', KT, 0.25, 7.65, 0.4); sfx('k3', KT, 0.25, 8.4, 0.3)
sfx('s1', SEND, 0.35, 13.9); sfx('s1b', SEND, 0.35, 23.4); sfx('p1', POP, 0.2, 23.6)
sfx('s3', SEND, 0.35, 27.0); sfx('ring', RING, 1.45, 39.2, 0.8)
sfx('dung', '0.35*sin(2*PI*(58+8*t)*t)*exp(-1.6*t)', 1.2, 45.9, 0.5)
for k, (at, d) in enumerate([(12.6, 1.2), (17.2, 1.8), (21.0, 0.7)]):
    fc.append(f"anoisesrc=d={d}:c=brown:a=0.6:r=48000,bandpass=f=1800:w=900,volume='0.30*lt(mod(t,0.11),0.025)':eval=frame,"
              f"aformat=channel_layouts=stereo,adelay={int(at*1000)}:all=1[ty{k}]"); mixl.append(f'[ty{k}]')
# 공간 소리: 교무실(웅성 낮게) / 교실(빈 교실 바람)
def amb(lbl, a, b, lo, hi, vol):
    a0 = max(0, a - 0.3)   # 앞 구간과 0.3초 겹쳐 크로스페이드(컷마다 소리가 뚝 끊기지 않게)
    fc.append(f"anoisesrc=d={b-a0:.2f}:c=pink:a=0.5:r=48000,bandpass=f={(lo+hi)//2}:w={hi-lo},volume={vol},"
              f"afade=t=in:d=0.3,afade=t=out:st={b-a0-0.3:.2f}:d=0.3,aformat=channel_layouts=stereo,adelay={int(a0*1000)}:all=1[{lbl}]")
    mixl.append(f'[{lbl}]')
CLASS = {'N2', 'N4', 'N7', 'N6'}   # 교실 컷, 나머지는 교무실
ends = [ST[c[0]] + c[1] for c in CUTS]
for (cid, *_), e in zip(CUTS, ends):
    if cid in CLASS: amb(f'am_{cid}', ST[cid], e, 500, 2500, 0.015)
    else: amb(f'am_{cid}', ST[cid], e, 300, 2800, 0.018)
# 룸톤: 낮은 웅웅거림(냉난방·먼 웅성)을 영상 내내 아주 작게
fc.append(f"anoisesrc=d={VID_END}:c=brown:a=0.5:r=48000,lowpass=f=350,volume=0.0105,afade=t=in:d=0.5,afade=t=out:st={VID_END-0.4}:d=0.4,aformat=channel_layouts=stereo[room]"); mixl.append('[room]')
fc.append(''.join(mixl) + f"amix=inputs={len(mixl)}:normalize=0,apad=whole_dur={TOT},atrim=0:{TOT},"
          "anull[aout]")
run(['ffmpeg', '-y', '-loglevel', 'error', *ins, '-filter_complex', ';'.join(fc), '-map', '[aout]', '-ar', '48000', str(B / 'mix_raw.wav')])
# 2단계 음량: 재고 나서 고정 게인 + 리미터(실시간 loudnorm은 소리를 약 2초 앞당겨서 쓰지 않음)
import re
m = subprocess.run(['ffmpeg', '-i', str(B / 'mix_raw.wav'), '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', m)[-1])
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(B / 'mix_raw.wav'), '-af',
     f'volume={-14.0 - I:.2f}dB,alimiter=limit=0.63:level=false:attack=2:release=60', '-ar', '48000', str(B / 'mix.wav')])

# ---------- 자막 ----------
def ts(x):
    h, m = int(x // 3600), int(x % 3600 // 60); s = x % 60
    return f"{h}:{m:02d}:{s:05.2f}"
PINK, SKY = r'{\c&HC88CFF&}', r'{\c&HFFC88C&}'
EV = []
def ev(a, b, style, text, layer=1):
    EV.append(f"Dialogue: {layer},{ts(a)},{ts(b)},{style},,0,0,0,,{text}")
def bubble(a, b, style, side, y, text, tag=None, tagcol='', fad=r'\fad(80,120)'):
    an, x = (6, 900) if side == 'R' else (4, 80)   # 오른쪽 말풍선은 쇼츠 좋아요 버튼 열을 피해 x=900
    ev(a, b, style, rf"{{\an{an}\pos({x},{y}){fad}}}{text}", 4)
    if tag:
        nl = text.count(r'\N') + 1
        ty = y - {1: 58, 2: 88, 3: 118, 4: 148, 5: 178}[nl]
        tx = 720 if side == 'R' else 260
        ev(a, b, 'Tag', rf"{{\pos({tx},{ty})}}{tagcol}{tag}", 5)
def mono(a, b, text, tag, col, style='Mono'):
    ev(a, b, style, text, 2)
    ty = 1265 if r'\N' in text else 1335
    ev(a, b, 'Tag', rf"{{\pos(540,{ty})}}{col}{tag}", 3)

ev(0.0, 5.0, 'Label', r'{\an7\pos(40,90)}담임과 학생, 몸이 바뀌었다', 6)
ev(0.2, 4.9, 'Scene', r'{\an7\pos(40,190)}교무실 · 담임 몸에 지우 영혼', 6)
bubble(0.1, 5.0, 'DMg', 'L', 1160, r'[해외로밍]\N선생님~ 하은이가\N두통이 심해서\N오늘 집에서 쉴게요.')
ev(0.1, 5.0, 'Scene', r'{\an1\pos(80,1000)}하은이 어머니 · 해외로밍 문자', 6)
ev(0.2, 2.6, 'Emph', r'{\pos(540,700)\fad(60,200)}해외로밍 문자\N하은이 어머니', 7)
mono(1.2, 3.8, '헐… 해외에서 보냈네?', '지우 영혼 · 속마음', PINK)
ev(5.1, 7.2, 'Scene', r'{\an7\pos(40,190)}교실 · 지우 몸에 담임 영혼', 6)
# 메신저 관습 — 받은 말풍선 왼쪽, 보낸 말풍선 오른쪽. 이름표는 'A가 B에게' 하나의 틀
bubble(5.2, 7.3, 'DMp', 'L', 860, r'쌤, 하은이 엄마가\N하은이 두통이래요.', '지우가 담임에게 · DM', PINK)
# 7.3~10.0초 반 단톡 폰 화면(겹침 이미지)
mono(10.0, 10.9, '…일본이라고?', '담임 영혼 · 속마음', SKY)
bubble(10.85, 14.6, 'DMb', 'R', 1160, '하은이 지금 일본이다.', '담임이 지우에게 · DM', SKY)
mono(14.9, 17.2, '이건… 못 참지.', '지우 영혼 · 속마음', PINK)
for k, dots in enumerate(['•', '••', '•••'] * 2):
    a = 17.3 + k * 0.3
    ev(a, a + 0.3, 'DMg', rf"{{\an6\pos(900,1160)}}{dots}", 4)
ev(19.1, 20.8, 'Scene', r'{\an7\pos(40,190)}교실 · 지우 몸에 담임 영혼', 6)
mono(19.4, 21.6, '안 돼, 안 돼… 보내지 마.', '담임 영혼 · 속마음', SKY)
bubble(21.75, 23.6, 'DMb', 'R', 1160, '너, 아무것도 하지 마.', '담임이 지우에게 · DM', SKY)
bubble(23.6, 25.6, 'DMb', 'L', 860, '너, 아무것도 하지 마.', '담임이 지우에게 · DM', SKY)
mono(24.1, 26.9, '어디 한번… 골탕 좀 드셔 보세요~', '지우 영혼 · 속마음', PINK)
# 펀치라인은 소리("근데…" 약 30.8초)와 함께 보이게 두 번에 나눠 띄움
SENT1 = r'[보낸 문자] 어머님~\N하은이 두통 얼른\N나아야 할 텐데요.'
bubble(27.05, 30.8, 'DMg', 'R', 1160, SENT1, '지우가 하은이 어머니에게 · 문자', PINK, fad=r'\fad(80,0)')
bubble(30.8, 34.9, 'DMg', 'R', 1160, SENT1 + r'\N근데 단톡 사진 보니까\N일본에선 다 나은 것 같던데요?^^', '지우가 하은이 어머니에게 · 문자', PINK, fad=r'\fad(0,120)')
ev(34.2, 34.9, 'Read', r'{\an6\pos(900,1420)}읽음', 4)
ev(34.9, 37.0, 'Scene', r'{\an7\pos(40,190)}교실 · 지우 몸에 담임 영혼', 6)
mono(35.4, 37.4, '하… 보냈구나.', '담임 영혼 · 속마음', SKY)
# 39.2~40.75초 해외로밍 전화 수신 화면(겹침 이미지)
mono(40.8, 43.4, '뭐라고요? 무슨 말씀이세요?', '하은이 어머니 · 전화', '', 'Dlg')
mono(43.4, 46.4, '선생님, 지금 실수하신 겁니다.', '하은이 어머니 · 전화', '', 'Dlg')
ev(46.6, 48.4, 'Scene', r'{\an7\pos(40,190)}잠시 뒤 · 교무실에 교감이 왔다', 6)
mono(47.1, 50.6, r'김 선생, 방금 학부모한테\N뭘 보낸 거예요?', '교감', '', 'Dlg')

head = (KIT / 'soulchange_style.ass').read_text(encoding='utf-8').rstrip('\n')
(B / 'ep4.ass').write_text(head + '\n' + '\n'.join(EV) + '\n', encoding='utf-8')

# ---------- 합치기 ----------
out = HERE / 'ep4_v12.mp4'
IMG = EP / '04_생성물' / 'images'
OVL = [(IMG/'ovl_단톡.png', 7.3, 10.0), (IMG/'ovl_전화.png', 39.2, 40.75), (IMG/'ovl_통화중.png', 40.75, 46.5)]   # make_overlays.py로 만든 폰 화면
vf = []; last = '0:v'
for k, (p, a, b) in enumerate(OVL):
    vf.append(f"[{k+2}:v]format=rgba,fade=t=in:st={a}:d={0.2 if k != 2 else 0.01}:alpha=1,fade=t=out:st={b-0.2}:d=0.2:alpha=1[o{k}];"
              f"[{last}][o{k}]overlay=0:0:enable='between(t,{a},{b})'[w{k}]")
    last = f'w{k}'
vf.append(f"[{last}]ass={B/'ep4.ass'}:fontsdir={KIT/'fonts'}[vout]")
ovl_in = sum([['-loop', '1', '-t', str(TOT), '-i', str(p)] for p, _, _ in OVL], [])
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(B / 'joined.mp4'), '-i', str(B / 'mix.wav'), *ovl_in,
     '-filter_complex', ';'.join(vf), '-map', '[vout]', '-map', '1:a',
     '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-c:a', 'aac', '-b:a', '160k',
     '-t', str(TOT), '-movflags', '+faststart', str(out)])
json.dump({'cuts': ST, 'video_end': VID_END, 'total': TOT}, open(HERE / 'timeline_v12.json', 'w'), ensure_ascii=False, indent=1)
print('OK', out, TOT)
