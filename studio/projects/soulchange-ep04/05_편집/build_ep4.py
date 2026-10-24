#!/usr/bin/env python3
"""소울체인지 4화 편집 생성기 v1 (대본 v3 + 2026-10-24 청취 지적 반영).

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

# ---------- 컷 (시작, 길이, 소스, 소스 시작, PIP, 늘리기 배율, 끝 정지 초) ----------
CUTS = [
    ('k0',  1.5, KIT/'episodes/ep3/clips/n2.mp4', 3.0, 'pip',   1.0, 0),
    ('m1',  5.0, KIT/'episodes/ep4/clips/m1.mp4', 0.0, 'pip',   1.0, 0),
    ('m2',  5.0, KIT/'episodes/ep4/clips/m2.mp4', 0.0, 'pip',   1.0, 0),
    ('N1',  5.0, KIT/'episodes/ep4/clips/N1.mp4', 0.0, 'pip',   1.0, 0),
    ('m3',  5.0, KIT/'episodes/ep4/clips/m3.mp4', 0.0, 'pip',   1.0, 0),
    ('m4',  5.0, KIT/'episodes/ep4/clips/m4.mp4', 0.0, 'pip',   1.0, 0),
    ('N2',  5.0, C/'N2.mp4', 0.0, 'pip_t', 1.0, 0),
    ('N3',  5.0, C/'N3.mp4', 0.0, 'pip',   1.0, 0),
    ('N4',  5.0, C/'N4.mp4', 0.0, 'pip_t', 1.0, 0),
    ('N5',  5.4, C/'N5.mp4', 0.0, 'pip',   1.07, 0),
    ('N2b', 3.6, C/'N2.mp4', 1.4, 'pip_t', 1.0, 0),   # 담임 영혼이 지우 DM을 받아 읽는 반응(N2 뒷부분 재사용)
    ('N6',  6.4, C/'N6.mp4', 0.0, 'pip_t', 1.0, 1.4), # 끝 1.4초는 마지막 프레임 정지 + 천천히 확대
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
    vf += f",format=yuv420p[b];[1:v]scale=200:200[p];[b][p]overlay=x=850:y=90[v]"
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
LINES = [
    (KIT/'episodes/ep3/voices/P2_학부모협박문자_Ainsley.wav', 0.15, 1.2, False),
    (V/'E4A1_v2.wav', 6.6, 1.0, False),
    (V/'E4I1_v3.wav', 9.8, 1.1, True),
    (KIT/'episodes/ep4/voices/E4V1.mp3', 19.2, 1.05, False),
    (V/'v2/V4-01v2_공항도착.wav', 29.0, 1.0, True),
    (V/'V4-02_지우속마음_로밍_student.wav', 32.8, 1.0, True),
    (V/'v2/V4-04v2_하은이두통.wav', 36.7, 1.0, False),
    (V/'V4-05_담임DM_지금공항_teacher.wav', 40.4, 1.0, False),
    (V/'V4-06_지우DM_교감쌤이_student.wav', 43.2, 1.08, False),
    (V/'v2/V4-07v2_서연이도두통.wav', 47.0, 1.08, False),
    (V/'v2/V4-08v2_일러바친.wav', 50.7, 1.15, False),
]
ins, fc, mixl = [], [], []
for i, (f, at, tempo, hall) in enumerate(LINES):
    ins += ['-i', str(f)]
    chain = f"[{i}:a]aresample=48000,aformat=channel_layouts=mono,loudnorm=I=-18:TP=-2:LRA=9"
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
sfx('s0', SMS, 0.3, 0.05); sfx('s1', SEND, 0.35, 6.5); sfx('s2', SMS, 0.3, 26.7)
sfx('s3', SMS, 0.3, 31.6); sfx('thud', '0.5*sin(2*PI*(90-50*t)*t)*exp(-9*t)', 0.5, 32.2)
sfx('dung', '0.35*sin(2*PI*(58+8*t)*t)*exp(-1.6*t)', 1.6, 24.7)                      # "기간제" 환기
for k, at in enumerate([36.6, 43.1, 46.95, 50.6]): sfx(f'p{k}', POP, 0.2, at)
sfx('s4', SEND, 0.35, 40.3)
# 자판 소리(N4 입력, N5 입력)
for k, at in enumerate([38.3, 44.0]):
    fc.append(f"anoisesrc=d=1.4:c=brown:a=0.6:r=48000,bandpass=f=1800:w=900,volume='0.30*lt(mod(t,0.11),0.025)':eval=frame,"
              f"aformat=channel_layouts=stereo,adelay={int(at*1000)}:all=1[ty{k}]"); mixl.append(f'[ty{k}]')
# 공간 소리: 교무실(웅성 낮게) / 교실(빈 교실 바람)
def amb(lbl, a, b, lo, hi, vol):
    fc.append(f"anoisesrc=d={b-a:.2f}:c=pink:a=0.5:r=48000,bandpass=f={(lo+hi)//2}:w={hi-lo},volume={vol},"
              f"afade=t=in:d=0.3,afade=t=out:st={b-a-0.3:.2f}:d=0.3,aformat=channel_layouts=stereo,adelay={int(a*1000)}:all=1[{lbl}]")
    mixl.append(f'[{lbl}]')
amb('am_o1', 0, ST['m3'], 300, 2800, 0.05); amb('am_o2', ST['m3'], ST['N2'], 300, 2800, 0.07)
amb('am_c1', ST['N2'], ST['N3'], 500, 2500, 0.04); amb('am_o3', ST['N3'], ST['N4'], 300, 2800, 0.05)
amb('am_c2', ST['N4'], ST['N5'], 500, 2500, 0.04); amb('am_o4', ST['N5'], ST['N2b'], 300, 2800, 0.05)
amb('am_c3', ST['N2b'], VID_END, 500, 2500, 0.04)
fc.append(''.join(mixl) + f"amix=inputs={len(mixl)}:normalize=0,apad=whole_dur={TOT},atrim=0:{TOT},"
          "loudnorm=I=-14:TP=-3.5:LRA=11,alimiter=limit=0.63:level=false[aout]")
run(['ffmpeg', '-y', '-loglevel', 'error', *ins, '-filter_complex', ';'.join(fc), '-map', '[aout]', '-ar', '48000', str(B / 'mix.wav')])

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
        ty = y - {1: 58, 2: 88, 3: 118}[nl]
        tx = 820 if side == 'R' else 260
        ev(a, b, 'Tag', rf"{{\pos({tx},{ty})}}{tagcol}{tag}", 5)
def mono(a, b, text, tag, col, style='Mono'):
    ev(a, b, style, text, 2)
    ty = 1265 if r'\N' in text else 1335
    ev(a, b, 'Tag', rf"{{\pos(540,{ty})}}{col}{tag}", 3)

ev(0.0, 6.5, 'Label', '담임과 학생, 몸이 바뀌었다', 6)
bubble(0.15, 6.4, 'DMg', 'L', 860, r'선생님, 알고 보니\N고지식하신 분이시네요.')
bubble(2.9, 6.4, 'DMg', 'L', 1160, r'우리 애 아빠가 얼마나\N무서운지 아시죠?')
bubble(6.6, 11.4, 'DMg', 'R', 1000, r'오, 그래요?\N저희 아빠도 무서운데 ㅋㅋ', '지우 영혼 · 보낸 문자', PINK)
mono(9.8, 12.6, r'근데 고지식한 분이\N무섭기까지 하다니.', '지우 영혼 · 속마음', PINK)
mono(12.6, 14.3, '서연이랑 반대네.', '지우 영혼 · 속마음', PINK)
mono(14.45, 16.5, '서연인 우리 반 꼴찐데…', '지우 영혼 · 속마음', PINK)
mono(16.6, 19.1, r'그럼 저지식이라\N해야 하나? ㅋㅋ', '지우 영혼 · 속마음', PINK)
mono(19.2, 21.95, r'김 선생, 김서연 학생은\N잘 하고 있나?', '교감', '', 'Dlg')
mono(22.4, 23.85, r'그 학생만\N잘 돌봐 주면,', '교감', '', 'Dlg')
mono(23.85, 26.5, r'다음 기간제도\N내가 잘 봐주지.', '교감', '', 'Dlg')
ev(26.6, 28.4, 'Scene', '교실 · 지우 몸에 담임 영혼', 6)
bubble(26.8, 31.4, 'DMg', 'L', 860, r'[반 단톡] 하은\N나 공항 도착 ㅋㅋ')
mono(29.0, 30.6, '…공항 도착?', '담임 영혼 · 속마음', SKY)
bubble(31.7, 36.4, 'DMg', 'L', 1160, r'[로밍발신] 선생님~\N하은이가 두통이 심해서\N오늘 집에서 쉴게요.')
ev(32.2, 33.6, 'Emph', r'{\fad(60,150)}[로밍발신]', 7)
mono(32.8, 34.5, '어? 로밍?', '지우 영혼 · 속마음', PINK)
bubble(36.7, 41.4, 'DMp', 'R', 860, r'쌤, 하은이 엄마가\N하은이 두통이래요.', '지우 영혼 · DM', PINK)
bubble(40.4, 43.1, 'DMb', 'L', 1160, '하은이 지금 공항이다.', '담임 영혼 · DM', SKY)
bubble(43.2, 46.9, 'DMp', 'R', 860, r'교감쌤이 서연이 잘 챙기면\N기간제 봐준대요.', '지우 영혼 · DM', PINK)
bubble(47.0, 50.5, 'DMp', 'R', 860, r'서연이도 두통이었는데,\N아까 안 된다고 했잖아요.', '지우 영혼 · DM', PINK)
bubble(50.7, 53.4, 'DMp', 'R', 1000, r'쌤, 그거 제 폰 단톡에서\N본 거잖아요.', '지우 영혼 · DM', PINK)
bubble(53.4, 56.8, 'DMp', 'R', 1000, r'그걸로 따지면\N제가 일러바친 게 돼요.', '지우 영혼 · DM', PINK)
for k, dots in enumerate(['•', '••', '•••', '•', '••', '•••']):
    a = 55.1 + k * 0.3
    ev(a, min(a + 0.3, VID_END), 'DMb', rf"{{\an4\pos(80,1160)}}{dots}", 4)

head = (KIT / 'soulchange_style.ass').read_text(encoding='utf-8').rstrip('\n')
(B / 'ep4.ass').write_text(head + '\n' + '\n'.join(EV) + '\n', encoding='utf-8')

# ---------- 합치기 ----------
out = HERE / 'ep4_v1.mp4'
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(B / 'joined.mp4'), '-i', str(B / 'mix.wav'),
     '-vf', f"ass={B/'ep4.ass'}:fontsdir={KIT/'fonts'}", '-map', '0:v', '-map', '1:a',
     '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-c:a', 'aac', '-b:a', '160k',
     '-t', str(TOT), '-movflags', '+faststart', str(out)])
json.dump({'cuts': ST, 'video_end': VID_END, 'total': TOT}, open(HERE / 'timeline_v1.json', 'w'), ensure_ascii=False, indent=1)
print('OK', out, TOT)
