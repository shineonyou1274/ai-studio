#!/usr/bin/env python3
"""소울체인지 12화(마지막 화) 편집 v10 (사장님 11/2: 배경음 0초부터, 지우 고백 때 담임 몸 말하는 얼굴 대신 그동안 지우 몸(김병만 영혼) 장면 회상 — 5화 교실 머리 긁기·머리 감싸기, 8화 벤치, 11화 딸기우유, 1분 9초 눈 천천히 뜨는 컷 뺌, 엄마 "…지우…니?"에서 "니" 뺌, 고양이 뒤 번쩍 아래 김병만 얼굴 뺌).
v9 (사장님 11/2 "일단 가보자": 이마끼리 칙 자막 뺌, 첫 1초는 복도 아이들 컷, 손 컷 느린 배속 줄이고 넓은 컷 섞기, 지우 몸 리액션 컷에 "(김병만 영혼: 듣는 중)", 아이콘 바뀌는 시각을 실제 프레임 기준으로(늦던 0.2초), 이어지는 자막은 사라짐 효과 없이 바로 이어 붙임).
v8 (Gemini v7 검수: 끝 고양이 노트북 1화 글자 첫 프레임부터 덮기, 반 아이들 컷 왼쪽 김병만 닮은 학생 잘라냄, 교차 지우 얼굴은 멈춘 화면 + 파란 아이콘(김병만 영혼), 야옹은 BigSoundBank #0390 진짜 고양이 소리(CC0)).
v7 (사장님 v6 지적: 고양이 입 움직이는 부분 뺌(1화 39.5~40.1초 입 다문 구간만), 이마 소리는 무료 효과음 "칙"(BigSoundBank #0044 Short spray, CC0), "교감샘도 저처럼 살아 봐라" 입 맞춤(말하는 구간 2.8~4.3초에 맞춰 1.4배 느리게), 엄마 "죄…" 뺌, "엄마, 내가 부탁한 거잖아"부터 지우 얼굴과 담임 몸 우는 얼굴 번갈아).
v6 (사장님 11/2 v5 지적: 이마 빡 소리·교감 "아얏! 거 똑바로 좀 보고 다녀요!", 엄마 "죄…" 바로 지우 "엄마, 그만", 그 컷은 담임 몸만, "지우니?" 이름표 안 보이게, 복귀 승인 고양이 야옹, 귀 넘기기는 상담 장면에 끼워 넣고 "이건 좀 남았네" 뺌, 남학생 앞 비웃음·배경음 바꿈, 잔소리는 학생과 번갈아, 학생 손 컷 뺌, 추가 촬영 5컷(PC방·복도·반 아이들·남학생 2), 퉁퉁 효과음 뺌).
v5 (사장님 11/2: 지우 끝 대사 "엄마, 나 이제 힘들면 힘들다고 말하고, 뭐든 피하지 않고 씩씩하게 해 볼게."로 바꿈 + Gemini v4 검수: 1화 다음 편 화면 겹침 뺌, 고양이 "접수했어" 끝까지, 배경음 두 번 깔리던 것·끝 실로폰 뺌, 남았네 컷 웃는 데서 자름, 교실 들어갈 때·복도 무음 채움(발소리), 엄마 "…지우…니?"는 엄마 손, 포옹은 엄마 등·손만, 손 컷 소파 배경 잘라냄, 걷는 컷 흔들림 줄임, 학생 손 컷 소매 잘라냄, 이마 꽝 해설).
v4 (v3 + Gemini v2 검수: 복귀 전 지우 몸 입 움직이는 컷 빼기(엄마 손으로 확대), 종이 컷은 손만, "죄…" 끝까지, "에헴" 뺌, 고양이 "접수했어" 끝까지, 교실 걸어오는 컷 위쪽만(책상 뚫는 다리 빼기), 뒤 복제 학생 잘라냄, 복도 표지판·바지 무늬 확대로 뺌).
v3: (사장님 v2: "지우 얼굴이 바뀌고 버릇없어 보임, 담임과 지우가 같이 있는 것도 어색" → 크레딧 0으로: 상담실 넓은 컷은 확대해 지우 빼기, 다리 벌린 컷·웃는 컷 빼고 엄마 손으로, 포옹은 엄마 등 쪽으로 확대).
v2: (자체 점검: 긴 자막 줄을 19자 안으로 나눔, 끝 고양이 컷 1화 라벨 덮기·고양이 대사 노트북 아래로).
v1: (대본 v1.1 「자, 선택해라」).
상담실: 엄마가 털어놓음 → 지우 본색 고백 → 1화 고양이 "복귀 승인" → 번쩍, 몸 복귀 → 김병만 잔소리 → 교감과 꽝 "교감샘도 저처럼 살아 봐라" → 번쩍 → 고양이 "접수했어"
사용: python3 build_ep12_v1.py [--plan]
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
ENDING = B / 'ending_ep12.mp4'      # make_ending_final.py (시즌 1 끝)
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
    'J01': dict(f='E12-01_jiu_inner_student.mp3', r=[(0, 2.9)], tempo=1.0),
    'M02': dict(f='E12-02_mom_helena.mp3', r=[(0, 24.5)], tempo=1.1),
    'M04': dict(f='E12-04_mom_helena.mp3', r=[(0, 19.0)], tempo=1.1),
    'J05': dict(f='E12-05_jiu_slip_student.mp3', r=[(0, 3.4)], tempo=1.0),
    'J06': dict(f='ls/E12-06_jiu_student_x1.1.mp3', r=[(0, 8.55)], tempo=1.0),
    'M07': dict(f='E12-07_mom_helena.mp3', r=[(0, 1.25)], tempo=1.0),
    'J08': dict(f='ls/E12-08_jiu_student_x1.1.mp3', r=[(0, 11.35)], tempo=1.0),
    'J09': dict(f='E12-09_jiu_student.mp3', r=[(0, 9.6)], tempo=1.1),
    'J12': dict(f='E12-12b_jiu_student.mp3', r=[(0, 7.15)], tempo=1.1),
    'B13': dict(f='E12-13s_boy_benji.mp3', r=[(0, 1.6)], tempo=1.0),
    'CHIK': dict(f='SFX_chik_bigsoundbank0044.wav', r=[(0, 0.55)], tempo=1.0),
    'MEOW': dict(f='SFX_meow_bigsoundbank0390.wav', r=[(0, 0.78)], tempo=1.0),
    'B14': dict(f='E12-14_boy_benji.mp3', r=[(0, 2.1)], tempo=1.0),
    'T15': dict(f='ls/E12-15_teacher_teacher_x1.1.mp3', r=[(0, 11.9)], tempo=1.0),
    'T16': dict(f='ls/E12-16_teacher_teacher_x1.1.mp3', r=[(0, 15.0)], tempo=1.0),
    'V18': dict(f='E12-18c_vp_arthur.mp3', r=[(0, 2.95)], tempo=1.0),
    'T18': dict(f='E12-18b_teacher_teacher.mp3', r=[(0, 2.8)], tempo=1.0),
    'CAT': dict(f='CAT_ep1_접수했어_v2.wav', r=[(0, 3.35)], tempo=1.0),
}
D = vp.prep(SPEC, V, VO)
INNER = {'J01'}
PHONE = set(); WHISPER = set(); MEMORY = set(); BEEP = ('', 0, 0)
LS_OFF = {'C5': 0.0, 'C7': 0.05, 'C11': 0.1, 'C12': 0.0, 'C13': 0.7, 'C14': 0.0, 'C15': 0.0, 'C19': -0.13}   # 립싱크: 영상 입이 녹음보다 늦은 만큼(잼)

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
PP = P
FBV = "hue=s=0.45,eq=brightness=0.03:contrast=1.03,"   # 회상(그동안) 색
FB = "hue=s=0.30,eq=brightness=0.04:contrast=1.05,fade=t=in:d=0.12:color=white,"

EP1 = P / 'soulchange-ep01/05_편집/ep1_공개본_720p.mp4'
CATV = "delogo=x=250:y=118:w=225:h=70,delogo=x=110:y=958:w=440:h=95,"   # 1화 고양이: 위 라벨·아래 자막 지움
cut('K0', K('H1'), 3.0, 1.0, note='첫 1초: 복도 아이들(제목 띠)')
c0 = t; e = at('J01', c0 + 1.0)
cut('C1', K('C1'), 4.6, max(e + 0.4 - c0, 4.6), stretch=3.3, hold=True, pip='pip', zoom=(1.15, 0.0, 0.3), note='상담실 넓게: 담임 몸·엄마 뒷모습')
c0 = t; e = at('M02', c0 + 0.3); M02E = e
cut('C2', K('C2'), 0, 3.6, stretch=1.0, hold=True, zoom=(1.5, 0.5, 1.0), note='엄마 손수건')
cut('C1w', K('C1'), 4.6, 2.9, stretch=2.0, hold=True, pip='pip', zoom=(1.15, 0.0, 0.3), note='상담실 넓게(담임 몸·엄마)')
cut('C12e', K('C12'), 0.0, 2.6, stretch=1.3, hold=True, pip='pip', zoom=(1.15, 0.3, 0.2), note='담임 몸(지우) 머리를 귀 뒤로 넘김 — 지우 버릇')
cut('C4h', K('C7'), 0.0, 3.5, stretch=12.0, hold=True, pip='pip', note='담임 몸 얼굴 — 엄마 말 듣는 중')
cut('C1x', K('C1'), 4.4, 2.5, stretch=2.0, hold=True, pip='pip', zoom=(1.5, 0.15, 0.25), note='담임 몸 굳은 채 듣기')
cut('C2b', K('C2'), 0.2, max(M02E + 0.4 - t, 2.0), stretch=1.4, hold=True, zoom=(1.5, 0.5, 1.0), note='엄마 손 — 말 끝까지')
c0 = t; e = at('M04', c0 + 0.3); M04E = e
cut('C4', K('C4'), 0, 6.5, stretch=1.3, hold=True, zoom=(1.7, 0.0, 1.0), note='(손·종이만) 생결 확인서')
cut('C1c', K('C1'), 5.0, 2.6, stretch=4.5, hold=True, pip='pip', zoom=(1.15, 0.0, 0.3), note='담임 몸 안절부절(넥타이)')
cut('C12f', K('C12'), 0.2, 2.2, stretch=1.3, hold=True, pip='pip', zoom=(1.3, 0.3, 0.2), note='또 귀 뒤로 넘김')
cut('C2c', K('C2'), 0.3, max(M04E + 0.05 - t, 2.0), stretch=1.2, hold=True, zoom=(1.5, 0.5, 1.0), note='엄마 손 꽉 쥠 — "죄…"')
c0 = t; e = at('J05', c0 - 0.05)
cut('C1j', K('C1'), 4.8, e + 0.2 - c0, stretch=3.0, hold=True, pip='pip', zoom=(1.5, 0.15, 0.25), note='"엄마, 그만…" 바로 — 담임 몸만')
c0 = t; e = at('J06', c0 + LS_OFF['C5'])
cut('FB1', PP / 'soulchange-ep05/04_생성물/clips/C1_K3.mp4', 0.3, 2.7, hold=True, pip='pip_t', vfx=FBV, note='회상: 5화 교실, 지우 몸(김병만 영혼) 씩씩대며 머리 긁기')
cut('JF1', K('C6'), 3.4, 1.3, hold=True, pip='pip_t', zoom=(2.3, 0.68, 0.10), note='지우 얼굴(김병만 영혼) 놀람')
cut('FB2', PP / 'soulchange-ep08/04_생성물/clips/K8.mp4', 0.8, max(e + 0.3 - t, 2.0), hold=True, pip='pip_t', vfx=FBV, note='회상: 8화 벤치')
c0 = t; e = at('M07', c0 + 0.2)
cut('C6b', K('C2'), 3.0, e + 0.5 - c0, stretch=1.5, hold=True, zoom=(1.6, 0.5, 1.0), note='엄마 손 멈춤 "…지우…니?" (이름표 안 보이게)')
c0 = t; e = at('J08', c0 + LS_OFF['C7']); J8 = L['J08']
cut('FB3', PP / 'soulchange-ep05/04_생성물/clips/C3_K6b.mp4', 0.3, 2.6, hold=True, pip='pip_t', vfx=FBV, note='회상: 5화 교실, 머리 감싸기')
cut('JF2', K('C8'), 1.2, 1.4, hold=True, pip='pip_t', note='지우 얼굴(김병만 영혼) 고개 숙임')
cut('PC1', K('P1'), 0.3, D['J08'] * 0.36, stretch=1.0, hold=True, note='회상: 지우가 PC방에서 게임 — "게임하면 잊혀서"')
cut('FB4', PP / 'soulchange-ep11/04_생성물/clips/K5.mp4', 0.3, max(e + 0.3 - t, 2.0), hold=True, pip='pip_t', vfx=FBV, note='회상: 11화 딸기우유 툭')
c1 = t; e = at('J09', c1 + 0.3)
cut('C7c', K('C7'), 8.6, 2.6, stretch=3.0, hold=True, pip='pip', note='담임 몸 우는 얼굴')
cut('C8', K('C2'), 0.5, max(e + 0.4 - t, 1.5), stretch=2.2, hold=True, zoom=(1.5, 0.5, 1.0), note='엄마 손 — "미안해, 엄마."')
c0 = t; at('MEOW', c0 + 1.0)
cut('CATa', EP1, 39.52, 2.6, stretch=4.2, vfx=CATV, hold=True, note='1화 고양이(입 다문 0.6초만 느리게): 노트북 "복귀 승인" + 야옹')
cut('FL1', EP1, 39.9, 0.5, stretch=4.0, vfx=CATV, note='번쩍(흰 화면은 자막에서) — 고양이 화면 위')
c0 = t; e = at('J12', c0 + LS_OFF['C11'] + 0.3)
cut('C11', K('C11'), 0, max(e + 0.4 - c0, 4.6), stretch=1.4, hold=True, zoom=(1.9, 0.0, 1.0), note='(엄마 등·손만) 지우가 엄마를 안음')
cut('HW', K('H1'), 0.5, 2.6, note='다음 날 복도: 아이들 지나감')
c0 = t; e = at('B13', c0 + 0.6)
cut('BS', K('B1'), 0.3, max(e + 0.3 - c0, 2.4), hold=True, note='남학생 "참 내… 하." 비웃음')
c0 = t; e = at('B14', c0 + LS_OFF['C13'] + 0.4)
cut('C13', K('C13'), 0, max(e + 0.4 - c0, 3.4), hold=True, note='남학생 "샘이 뭔데 그러세요?"')
# 잔소리 1: 김병만 ↔ 남학생 번갈아(김병만 컷은 원래 시간 그대로 이어서 립싱크 유지)
c0 = t; e = at('T15', c0 + LS_OFF['C14']); T15S = L['T15']
def seg_teacher(cid, src, st_off, dur, **kw):
    cut(cid, src, st_off, dur, hold=True, **kw)
cut('C14a', K('C14'), 0, D['T15'] * 0.30, hold=True, zoom=(1.7, 0.5, 0.05), vfx='deshake=rx=32:ry=48,', note='김병만 "그래. 나 암것도…"')
cut('BR1', K('B2'), 0.0, D['T15'] * 0.17, hold=True, note='남학생 듣는 얼굴(비웃음 사라짐)')
_o = t - c0
cut('C14b', K('C14'), _o, D['T15'] * 0.13, hold=True, zoom=(1.7, 0.5, 0.05), vfx='deshake=rx=32:ry=48,', note='김병만 "너 지금 나 아니면"')
cut('RC1', K('R1'), 0.5, max(e + 0.3 - t, 2.0), hold=True, zoom=(1.4, 1.0, 0.5), note='반 아이들 폰 내려놓고 듣기 — "말해 줄 사람을 못 만날까 봐"')
c0 = t; e = at('T16', c0 + LS_OFF['C15'])
cut('C15a', K('C15'), 0, D['T16'] * 0.45, hold=True, zoom=(1.55, 0.3, 0.2), note='김병만 "한 번쯤…" "원하지 않으면…"')
cut('RC2', K('R1'), 2.6, D['T16'] * 0.20, stretch=1.2, hold=True, zoom=(1.4, 1.0, 0.5), note='반 아이들 — "잔소리는 아주 귀해서"')
_o = t - c0
cut('C15b', K('C15'), _o, D['T16'] * 0.13, hold=True, zoom=(1.55, 0.3, 0.2), note='김병만 "아무에게나 나눠 주는 건 아니거든"')
cut('BR2', K('B2'), 1.8, max(e + 0.6 - t, 2.6), hold=True, note='남학생 의자 내리고 바로 앉음 — "자. 선택해라. 어떻게 할래?"')
c0 = t; at('CHIK', c0 + 2.3); at('V18', c0 + 2.6)
cut('C18', K('C18'), 0, 2.6 + D['V18'] + 0.2, hold=True, zoom=(1.3, 0.2, 0.55), note='복도 교감과 이마 빡 + "아얏! 거 똑바로 좀 보고 다녀요!"')
c0 = t; e = at('T18', c0 + 0.7)
cut('C19', K('C19'), 2.3, max(e + 0.5 - c0, 3.4), stretch=1.4, hold=True, note='"교감샘도 저처럼 살아 봐라" — 말하는 구간(2.8~4.3초)을 1.4배 느리게 해서 입 맞춤')
cut('FL2', K('C19'), 4.5, 0.5, note='번쩍')
c0 = t; e = at('CAT', c0 + 0.3)
CATV2 = "delogo=x=175:y=122:w=380:h=62,delogo=x=100:y=945:w=460:h=110,"
_d = max(e + 1.3 - c0, 3.4)
cut('CATb', EP1, 16.7, _d, stretch=_d / 1.9, vfx=CATV2, hold=True, note='1화 고양이 재사용: "소원 접수: 교감 ↔ 김병만" + "접수했어."')
MAIN = round(t, 3); TOT = round(MAIN + END_LEN, 3)
print('본편', MAIN, '합계', TOT)
for c in CUTS:
    avail = (dur_of(c['src']) - c['ss']) * c['stretch']
    print(f"  {c['id']:5s} {c['start']:6.2f} +{c['dur']:.2f}  x{c['stretch']:.2f}" + (f"  멈춤 {c['dur'] - avail:.2f}" if c['dur'] > avail + 0.02 and not c['fx'] else ''))
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
cs = lambda i: k[i]['start']; ce = lambda i: k[i]['start'] + k[i]['dur']
FLASH = "anoisesrc=d=0.6:c=white:a=0.5:r=48000,highpass=f=1500,afade=t=in:d=0.05,afade=t=out:st=0.15:d=0.45,volume=0.25"
for j, cid in enumerate(['FL1', 'FL2']):
    fc.append(f"{FLASH},aformat=channel_layouts=stereo,adelay={int(cs(cid) * 1000)}:all=1[fl{j}]"); mixl.append(f'[fl{j}]')
for j, cid in enumerate(['CATa', 'CATb']):
    for q in range(3): sfx(f'key{j}{q}', '0.25*sin(2*PI*2600*t)*exp(-60*t)', 0.08, cs(cid) + 0.6 + q * 0.18, 0.6)   # 고양이 키보드 톡톡
def amb(lbl, a, b, lo, hi, vol):
    a0 = max(0, a - 0.3)
    fc.append(f"anoisesrc=d={b - a0:.2f}:c=pink:a=0.5:r=48000,bandpass=f={(lo + hi) // 2}:w={hi - lo},volume={vol},"
              f"afade=t=in:d=0.3,afade=t=out:st={b - a0 - 0.3:.2f}:d=0.3,aformat=channel_layouts=stereo,adelay={int(a0 * 1000)}:all=1[{lbl}]"); mixl.append(f'[{lbl}]')
for c in CUTS:
    a, b = c['start'], c['start'] + c['dur']
    if c['id'].startswith(('CAT', 'FL')): continue
    amb(f"am_{c['id']}", a, b, 150, 900, 0.012)
fc.append(f"anoisesrc=d={MAIN}:c=brown:a=0.5:r=48000,lowpass=f=350,volume=0.0105,afade=t=in:d=0.5,afade=t=out:st={MAIN - 0.4}:d=0.4,aformat=channel_layouts=stereo[room]"); mixl.append('[room]')
# 배경음: 상담실 앞(가벼운 class) → 엄마 털어놓기부터 고백까지 따뜻한 곡(warm) 하나로 → 복귀 뒤 밝게(class) → 잔소리(warm) → 교감 꽝 직전 뚝 → 끝 pulse
BGM_SECT = [('class', 0.0, cs('C2') + 0.2, 0.5), ('warm', cs('C4') - 0.5, cs('CATa'), 1.2, 1.5),
            ('class', cs('C11') + 2.0, cs('BS'), 0.5), ('tense2', cs('BS'), cs('C14a'), 0.3), ('warm', cs('C14a'), cs('C18') + 2.3, 1.2, 1.0)]
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
    fi, fo = (0 if x.get('cont_in') else 60), (0 if x.get('cont_out') else 100)
    ev(x['a'], x['b'], x['style'] + 'B', r'{\an2\pos(540,' + str(x['y']) + rf')\fad({fi},{fo})}}' + x['text'], 2)
    if x['tag']:
        ty = x['y'] - (149 if r'\N' in x['text'] else 87)
        ev(x['a'], x['b'], TAGSTYLE[(x['col'], x['style'] == 'Mono')], rf"{{\an2\pos(540,{ty})\fad({fi},{fo})}}{x['tag']}", 3)
def narr(a, b, text, x=40, y=430): ev(a, b, 'Narr', rf'{{\an7\pos({x},{y})\frz5\fad(120,150)}}{text}', 8)
def scene(a, b, text): ev(a, b, 'Scene', r'{\an7\pos(40,240)}' + text, 6)
cs = lambda i: k[i]['start']; ce = lambda i: k[i]['start'] + k[i]['dur']

for _a, _b in [(0.62, cs('C11'))]:
    ev(_a, _b, 'Label', r'{\an7\pos(40,140)\fs50}교사와 학생, 몸이 바뀌었다', 6)
ev(cs('C11'), cs('C11') + 2.5, 'Label', r'{\an7\pos(40,140)\fs50}돌아왔다', 6)
ev(0.0, 0.62, 'Label', r'{\an5\pos(540,640)\bord0\shad0\1c&H000000&\1a&H28&\p1\fad(0,120)}m 0 0 l 1080 0 1080 420 0 420{\p0}', 9)
ev(0.0, 0.62, 'Label', r'{\an5\pos(540,500)\fs50\bord0\fad(0,120)}소울체인지 12화 · 마지막 화', 10)
ev(0.0, 0.62, 'Label', r'{\an5\pos(540,610)\fs62\1c&HFFFFFF&\3c&H2020D0&\4c&H2020D0&\bord12\fad(0,120)}담임 몸으로 우리 엄마를 상담한다', 10)
ev(0.0, 0.62, 'Emph', r'{\an5\pos(540,750)\fs96\bord6\3c&H000000&\fad(0,120)}엄마, 그날 저…', 10)
scene(cs('C1'), cs('C1') + 2.4, '다음 날 16:00 · 상담실')
say('J01', '...엄마 앞에서 담임인 척이라니.', '(속마음) 지우 영혼', PINK, 'Mono')
M02T = [r'선생님, 요즘 애가\N방에서 잘 나오지도 않고요,', r'제가 옆에 가기만 해도\N질색을 하질 않나...', r'계속 눈을 찡그리고 머리를 긁으면서\N한숨 쉬고 씩씩거리고,', r'다리를 쩍쩍 아무 데서나\N막 벌리고 있길래 한 소리 했더니,', r'그 뒤로 밥도 같이\N안 먹으려고 하더라고요.', r'학교는 또 새벽같이 나가서\N얼굴 보기도 힘들고요.']
M02W = [0.0, 0.14, 0.28, 0.47, 0.70, 0.83, 1.0]
for j, s in enumerate(M02T):
    say('M02', s, '지우 엄마', start=L['M02'] + D['M02'] * M02W[j], end=L['M02'] + D['M02'] * M02W[j + 1], grp=f'M02_{j}')
M04T = [r'사실 애가 너무 힘들어하길래, 제가\N하루 학교 쉬라며', r'생결 확인서를 써 줬거든요.', r'죄송합니다, 선생님.', r'그러면 안 된다는 걸 알면서\N딱 한 번만... 하면서 써 줬는데,', r'저도 그렇고 우리 지우도\N그게 너무 죄책감이 들어서', r'마음이 계속 힘드네요.']
M04W = [0.0, 0.14, 0.29, 0.38, 0.60, 0.81, 1.0]
for j, s in enumerate(M04T):
    say('M04', s, '지우 엄마', start=L['M04'] + D['M04'] * M04W[j], end=L['M04'] + D['M04'] * M04W[j + 1], grp=f'M04_{j}')
narr(cs('C1c'), ce('C2c'), r'(엄마가 털어놓을 때부터 안절부절)', 40, 360)
say('J05', '엄마, 그만... 내가 잘못했어.', '지우 (본색)', PINK)
J06T = [r'엄마, 내가...\N내가 부탁한 거잖아.', r'다 내가 잘못한 거야.', r'나 그날 학교 째고\NPC방도 갔어.']
J06W = [0.0, 0.40, 0.62, 1.0]
for j, s_ in enumerate(J06T):
    say('J06', s_, '지우 (본색)', PINK, start=L['J06'] + D['J06'] * J06W[j], end=L['J06'] + D['J06'] * J06W[j + 1], grp=f'J06_{j}')
say('M07', '...지우...?', '지우 엄마')
say('J08', r'그냥 나도 몰라, 왜 그랬는지...\N아프고 싶었어.', '지우', PINK, end=L['J08'] + D['J08'] * 0.42)
say('J08', r'뭘 정해야 할 때마다 무서워서,\N게임하면 잊혀서.', '지우', PINK, start=L['J08'] + D['J08'] * 0.42, end=L['J08'] + D['J08'] * 0.75, grp='J08b')
say('J08', r'다들 그러니까\N괜찮은 줄 알았어.', '지우', PINK, start=L['J08'] + D['J08'] * 0.75, grp='J08c')
say('J09', r'마약도 도박도 아닌데\N이 정도면 정상이라고...', '지우', PINK, end=L['J09'] + D['J09'] * 0.55)
say('J09', r'근데 그냥, 비겁했던 거야.\N미안해, 엄마.', '지우', PINK, start=L['J09'] + D['J09'] * 0.55, grp='J09b')
# 고양이 노트북 화면(1화 노트북 위를 덮음)
def laptop(cid, l1, l2, l3, col3='&H5AE3FF&'):
    a, b = cs(cid), ce(cid)
    ev(a, b, 'Label', r'{\an7\pos(0,0)\bord0\shad0\1c&H4A2414&\p1}m 400 1000 l 1060 960 l 1075 1395 l 400 1395{\p0}', 9)
    ev(a, b, 'Label', r'{\an7\pos(470,1040)\fs34\bord0\1c&HE0C8A0&}SOUL CHANGE / RETURN DESK', 10)
    ev(a, b, 'Label', r'{\an7\pos(470,1100)\fs66\bord0\1c&HFFFFFF&}' + l1, 10)
    ev(a, b, 'Label', r'{\an7\pos(470,1190)\fs60\bord0\1c&H5AE3FF&}' + l2, 10)
    ev(a + 0.9, b, 'Label', r'{\an7\pos(470,1285)\fs58\bord0\1c' + col3 + r'\fad(150,0)}' + l3, 10)
laptop('CATa', '소원 성취', '서로의 자리 되어 보기', '복귀 승인 ✔', '&H7CF0A0&')
laptop('CATb', '소원 접수', '교감 ↔ 김병만', '복귀 일정: 추후 공지')
narr(cs('CATa'), ce('CATa'), '(1화 그 고양이)', 40, 300)
for cid in ('FL1', 'FL2'):
    ev(cs(cid), ce(cid), 'Label', r'{\an7\pos(0,0)\bord0\shad0\1c&HFFFFFF&\fad(30,300)\p1}m 0 0 l 1080 0 1080 1920 0 1920{\p0}', 12)
say('J12', r'...엄마, 나 이제 힘들면\N힘들다고 말하고,', '지우', PINK, end=L['J12'] + D['J12'] * 0.56)
say('J12', r'뭐든 피하지 않고\N씩씩하게 해 볼게.', '지우', PINK, start=L['J12'] + D['J12'] * 0.56, grp='J12b')
narr(cs('C12e') + 0.3, ce('C12e'), r'(지우 버릇: 머리 넘기기)', 40, 360)
scene(cs('HW'), cs('BS') + 1.5, '다음 날 · 교실')
narr(cs('PC1'), ce('PC1'), '(그날 PC방)', 40, 360)
for _j in ('JF1', 'JF2'): narr(cs(_j), ce(_j), r'(김병만 영혼: 듣는 중)', 40, 360)
for _j in ('FB1', 'FB2', 'FB3', 'FB4'): narr(cs(_j), ce(_j), r'(그동안 내 몸으로 지낸 쌤)', 40, 360)
say('B13', '참 내... 하.', '반 학생')
say('B14', '샘이 뭔데 그러세요?', '반 학생')
T15T = [r'그래. 나 암것도 아니야.\N아무 힘도 없어.', r'그런데 너가 가여워서 그래.', r'너 지금 나 아니면,', r'너한테 그렇게 살지 말라고 말해 줄\N사람을 앞으로 못 만날까 봐 그래.']
T15W = [0.0, 0.30, 0.47, 0.60, 1.0]
for j, s in enumerate(T15T):
    say('T15', s, '김병만 쌤', SKY, start=L['T15'] + D['T15'] * T15W[j], end=L['T15'] + D['T15'] * T15W[j + 1], grp=f'T15_{j}')
T16T = [r'한 번쯤 제대로 네 삶에\N참견하는 사람이 있어도 괜찮지 않을까.', r'하지만 너가 원하지 않으면,\N하지 않을 거야.', r'내가 하는 잔소리들은 아주 귀해서,\N아무에게나 나눠 주는 건 아니거든.', r'...자. 선택해라.\N어떻게 할래?']
T16W = [0.0, 0.27, 0.45, 0.78, 1.0]
for j, s in enumerate(T16T):
    say('T16', s, '김병만 쌤', SKY, start=L['T16'] + D['T16'] * T16W[j], end=L['T16'] + D['T16'] * T16W[j + 1], grp=f'T16_{j}')
say('V18', '아얏! 거, 똑바로 좀 보고 다녀요!', '교감')
say('T18', '교감샘도 저처럼 살아 봐라.', '김병만 쌤', SKY)
narr(cs('C19'), ce('C19'), '(1화 데자뷰... 씨익)', 480, 360)
say('CAT', r'서로 돼 보는 게 소원이야?\N...접수했어.', '고양이', y=1700)

PEND.sort(key=lambda x: x['a'])
for i, x in enumerate(PEND):
    nxt = next((y for y in PEND[i + 1:] if y['grp'] != x['grp'] and y['y'] == x['y']), None)
    if nxt and x['b'] > nxt['a'] - 0.03: x['b'] = nxt['a'] - 0.03
    if nxt and nxt['a'] - x['b'] < 0.1 and nxt['tag'] == x['tag']: x['b'] = nxt['a']; x['cont_out'] = True; nxt['cont_in'] = True
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
(B / 'ep12.ass').write_text(head + '\n' + '\n'.join(EV) + '\n', encoding='utf-8')

# ---------- 6. 합치기 ----------
_fs, _acc = {}, 0
for c in CUTS: _fs[c['id']] = _acc / FPS; _acc += round(c['dur'] * FPS)
for c in CUTS: c['fstart'] = _fs[c['id']]; c['fend'] = _fs[c['id']] + round(c['dur'] * FPS) / FPS
en_j = '+'.join(f"between(t,{c['fstart']:.3f},{c['fend'] - 0.001:.3f})" for c in CUTS if c['pip'] == 'pip') or '0'
en_t = '+'.join(f"between(t,{c['fstart']:.3f},{c['fend'] - 0.001:.3f})" for c in CUTS if c['pip'] == 'pip_t') or '0'
vf = (f"[1:v]scale=300:300[pj];[2:v]scale=300:300[pt];"
      f"[0:v][pj]overlay=x=750:y=130:enable='{en_j}'[a];[a][pt]overlay=x=750:y=130:enable='{en_t}'[b];"
      f"[b]ass={B / 'ep12.ass'}:fontsdir={KIT / 'fonts'},format=yuv420p[vout]")
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', B / 'joined.mp4', '-i', KIT / 'pip.png', '-i', KIT / 'pip_t.png',
     '-filter_complex', vf, '-map', '[vout]', '-t', MAIN, '-r', FPS, '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', B / 'main_v.mp4'])
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', ENDING, '-an', '-vf', f'fps={FPS},format=yuv420p,setsar=1', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', B / 'ending_v.mp4'])
(B / 'vlist.txt').write_text(f"file '{B / 'main_v.mp4'}'\nfile '{B / 'ending_v.mp4'}'\n")
out = HERE / 'ep12_v10.mp4'
run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', B / 'vlist.txt', '-i', B / 'mix.wav',
     '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-t', TOT, '-movflags', '+faststart', out])
json.dump({'main': MAIN, 'total': TOT, 'loudness_LUFS': I2, 'true_peak_dBTP': TP2,
           'cuts': [{kk: (str(vv) if isinstance(vv, pathlib.Path) else vv) for kk, vv in c.items()} for c in CUTS],
           'lines': {lid: {'start': L[lid], 'end': round(end_(lid), 3), 'file': SPEC[lid]['f'], 'range': SPEC[lid]['r']} for lid in sorted(L, key=L.get)},
           'subs': SUBS, 'bgm': BGM_SECT}, open(HERE / 'timeline_v10.json', 'w'), ensure_ascii=False, indent=1)
print('OK', out, TOT)

