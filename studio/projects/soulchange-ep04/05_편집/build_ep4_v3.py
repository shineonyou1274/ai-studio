#!/usr/bin/env python3
"""소울체인지 4화 편집 생성기 v3 (v2 + Gemini·블라인드 검수 반영: 교감 목소리 교체·립싱크, 로봇 같은 줄 재녹음, 공항 발음, 영혼 원 확대, 보낸 문자 말풍선 아래로).

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

# ---------- 컷 (v2 사이다형: 0초 [로밍발신] → 단톡으로 거짓말 확인 → 지우가 정중하게 뼈 있는 답장 → 담임 "보내지 마라" → 전송 → 학부모 항복 → 교감 등장) ----------
CUTS = [
    ('N3',  5.0, C/'N3.mp4', 0.0, 'pip',   1.0, 0),
    ('N2',  5.0, C/'N2.mp4', 0.0, 'pip_t', 1.0, 0),
    ('N4',  5.0, C/'N4.mp4', 0.0, 'pip_t', 1.0, 0),
    ('N1',  5.0, KIT/'episodes/ep4/clips/N1.mp4', 0.0, 'pip', 1.0, 0),
    ('m1',  5.0, KIT/'episodes/ep4/clips/m1.mp4', 0.0, 'pip', 1.0, 0),
    ('m2',  5.0, KIT/'episodes/ep4/clips/m2.mp4', 0.0, 'pip', 1.0, 0),
    ('N6',  5.0, C/'N6.mp4', 0.0, 'pip_t', 1.0, 0),
    ('N5',  5.4, C/'N5.mp4', 0.0, 'pip',   1.07, 0),
    ('m3',  5.5, KIT/'episodes/ep4/clips/m3.mp4', 0.0, 'pip', 1.1, 0),  # 교감 입 움직임(1.2~5.0초)을 대사 길이에 맞춰 늘림
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
LINES = [
    (X/'S4v4_해외에서보냈네.wav', 1.9, 1.0, True),
    (V/'v2/V4-04v2_하은이두통.wav', 5.2, 1.0, False),
    (X/'T3v4_공항이라고.wav', 8.7, 1.0, True),
    (V/'V4-05_담임DM_지금공항_teacher.wav', 10.4, 1.0, False),
    (W/'L1_지우속마음_못참지.wav', 15.4, 1.0, True),
    (X/'T1v4_보내지마라.wav', 20.4, 1.0, False),
    (W/'L3c_지우보낸문자.wav', 24.9, 1.0, False),
    (X/'T2v4_보냈구나.wav', 32.6, 1.0, True),
    (X/'VP_Gideon.wav', 41.3, 1.15, False),
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
sfx('s0', SMS, 0.3, 0.05); sfx('thud', '0.5*sin(2*PI*(90-50*t)*t)*exp(-9*t)', 0.5, 0.3)
sfx('p0', POP, 0.2, 5.1); sfx('s2', SMS, 0.3, 7.3); sfx('s1', SEND, 0.35, 10.3)
sfx('p1', POP, 0.2, 20.3); sfx('s3', SEND, 0.35, 24.75); sfx('s4', SMS, 0.3, 36.7)
sfx('dung', '0.35*sin(2*PI*(58+8*t)*t)*exp(-1.6*t)', 1.6, 41.0)
for k, (at, d) in enumerate([(10.6, 1.4), (17.6, 2.2), (22.8, 2.0)]):
    fc.append(f"anoisesrc=d={d}:c=brown:a=0.6:r=48000,bandpass=f=1800:w=900,volume='0.30*lt(mod(t,0.11),0.025)':eval=frame,"
              f"aformat=channel_layouts=stereo,adelay={int(at*1000)}:all=1[ty{k}]"); mixl.append(f'[ty{k}]')
# 공간 소리: 교무실(웅성 낮게) / 교실(빈 교실 바람)
def amb(lbl, a, b, lo, hi, vol):
    fc.append(f"anoisesrc=d={b-a:.2f}:c=pink:a=0.5:r=48000,bandpass=f={(lo+hi)//2}:w={hi-lo},volume={vol},"
              f"afade=t=in:d=0.3,afade=t=out:st={b-a-0.3:.2f}:d=0.3,aformat=channel_layouts=stereo,adelay={int(a*1000)}:all=1[{lbl}]")
    mixl.append(f'[{lbl}]')
amb('am_o1', 0, ST['N2'], 300, 2800, 0.05); amb('am_c1', ST['N2'], ST['N1'], 500, 2500, 0.04)
amb('am_o2', ST['N1'], ST['N6'], 300, 2800, 0.05); amb('am_c2', ST['N6'], ST['N5'], 500, 2500, 0.04)
amb('am_o3', ST['N5'], VID_END, 300, 2800, 0.06)
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
def bubble(a, b, style, side, y, text, tag=None, tagcol=''):
    an, x = (6, 1000) if side == 'R' else (4, 80)
    ev(a, b, style, rf"{{\an{an}\pos({x},{y})\fad(80,120)}}{text}", 4)
    if tag:
        nl = text.count(r'\N') + 1
        ty = y - {1: 58, 2: 88, 3: 118, 4: 148, 5: 178}[nl]
        tx = 820 if side == 'R' else 260
        ev(a, b, 'Tag', rf"{{\pos({tx},{ty})}}{tagcol}{tag}", 5)
def mono(a, b, text, tag, col, style='Mono'):
    ev(a, b, style, text, 2)
    ty = 1265 if r'\N' in text else 1335
    ev(a, b, 'Tag', rf"{{\pos(540,{ty})}}{col}{tag}", 3)

ev(0.0, 5.0, 'Label', r'{\an7\pos(40,90)}담임과 학생, 몸이 바뀌었다', 6)
ev(0.2, 4.9, 'Scene', r'{\an7\pos(40,190)}교무실 · 담임 몸에 지우 영혼', 6)
bubble(0.1, 5.0, 'DMg', 'L', 1160, r'[로밍발신] 하은 엄마\N선생님~ 하은이가\N두통이 심해서\N오늘 집에서 쉴게요.')
ev(0.3, 1.9, 'Emph', r'{\fad(60,150)}[로밍발신]', 7)
mono(1.9, 4.2, '헐… 해외에서 보냈네?', '지우 영혼 · 속마음', PINK)
ev(5.1, 7.2, 'Scene', r'{\an7\pos(40,190)}교실 · 지우 몸에 담임 영혼', 6)
bubble(5.2, 10.0, 'DMp', 'R', 860, r'쌤, 하은이 엄마가\N하은이 두통이래요.', '지우 영혼 · DM', PINK)
bubble(7.4, 10.0, 'DMg', 'L', 1160, r'[반 단톡] 하은\N나 공항 도착 ㅋㅋ')
mono(8.7, 10.0, '…공항이라고?', '담임 영혼 · 속마음', SKY)
bubble(10.4, 15.0, 'DMb', 'L', 1160, '하은이 지금 공항이다.', '담임 영혼 · DM', SKY)
mono(15.4, 17.8, '이건… 못 참지.', '지우 영혼 · 속마음', PINK)
for k, dots in enumerate(['•', '••', '•••'] * 4):
    a = 17.9 + k * 0.35
    if a < 24.7: ev(a, min(a + 0.35, 24.7), 'DMg', rf"{{\an6\pos(1000,1160)}}{dots}", 4)
bubble(20.4, 24.7, 'DMb', 'L', 860, r'지우야.\N그거 보내지 마라.', '담임 영혼 · DM', SKY)
bubble(24.85, 33.4, 'DMg', 'R', 1160, r'[보낸 문자] 어머님~\N하은이 두통 얼른\N나아야 할 텐데요.\N그런데 공항 와이파이는\N잘 되나요?', '지우 영혼 · 보낸 문자', PINK)
ev(32.4, 33.4, 'Read', r'{\an6\pos(1000,1340)}읽음', 4)
mono(32.6, 34.6, '하… 보냈구나.', '담임 영혼 · 속마음', SKY)
for k, dots in enumerate(['•', '••', '•••', '•', '••']):
    a = 35.1 + k * 0.32
    ev(a, a + 0.32, 'DMg', rf"{{\an4\pos(80,1160)}}{dots}", 4)
bubble(36.8, 40.4, 'DMg', 'L', 1160, r'[로밍발신] …선생님,\N하은이 내일 등교합니다^^;')
mono(41.3, 43.8, r'김 선생, 방금 학부모한테\N뭘 보낸 거예요?', '교감', '', 'Dlg')
mono(43.8, 45.9, '잠깐 나 좀 봅시다.', '교감', '', 'Dlg')

head = (KIT / 'soulchange_style.ass').read_text(encoding='utf-8').rstrip('\n')
(B / 'ep4.ass').write_text(head + '\n' + '\n'.join(EV) + '\n', encoding='utf-8')

# ---------- 합치기 ----------
out = HERE / 'ep4_v3.mp4'
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(B / 'joined.mp4'), '-i', str(B / 'mix.wav'),
     '-vf', f"ass={B/'ep4.ass'}:fontsdir={KIT/'fonts'}", '-map', '0:v', '-map', '1:a',
     '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-c:a', 'aac', '-b:a', '160k',
     '-t', str(TOT), '-movflags', '+faststart', str(out)])
json.dump({'cuts': ST, 'video_end': VID_END, 'total': TOT}, open(HERE / 'timeline_v3.json', 'w'), ensure_ascii=False, indent=1)
print('OK', out, TOT)
