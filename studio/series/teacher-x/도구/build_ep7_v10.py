# 교사X 7화(계약직이 하기 딱이네) 편집 v10 (글자 전수 확인: 훅 유튜브 화면 캡션이 큰 제목과 겹침 → 영상 칸 쪽으로 확대(캡션은 제목 아래로), 공문 제목이 인쇄 줄과 겹침 → 위로) / v9 (사장님 11/18: '반려' 잘림·봉투 글자 엉망 → ep7_ov_v3(픽셀로 잰 자리), 훅 도장 줌을 고정에 가깝게(키우다 잘리던 것), 엔딩 문구 '차기 교장은 누가 될 것인가?', 봉투 컷에 사장님 종이 소리(papercrackle)) / v8 (사장님 11/18: 18초 파일은 잘못 보낸 것 → 봉투 컷의 '종이 바스락' 뺌. 마우스 딸깍은 그대로) / v7 (v6 프레임: 첫 0.7초 교감 얼굴이 낮아 제목이 입을 가림 → 얼굴이 위에 있는 02 끝(말 끝난 뒤 씩 웃음)으로, 제목은 얼굴 아래 y 800·도장은 가운데로 되돌림) / v6 (v5 프레임: 훅 제목이 '반려' 도장을 가림 → 제목 y 640→560, 도장은 화면 아래쪽으로(cy 0.47→0.36)) / v5 (Gemini 2차 11/18: 훅 첫 화면을 인물 표정(교감 씩 웃음)으로·제목은 화면 가운데 크게 / 엔딩 카드: 아래 30% 어둡게 + 큰 문구·작은 노란 예고로 위계 / 시간 글자는 왼쪽 위 한곳 / 글자 그림 v2(ep7_ov_v2: 덮는 칸 색 맞춤·곱하기) / 효과음: 사장님 마우스 딸깍(01 뒤)·종이 바스락(봉투), 훅 도장은 묵직한 '쿵'(s23 낮춤), 플래시 boing 뺌) / v4 (Gemini 11/18: P0 훅에 결말(교감 당황 16) 0.5초 플래시, P1 08 교감 고함 4dB 큼(-21.3 vs -25 LUFS) → -3.5dB, P1 정우 이름표 왼쪽 위로, P2 09에 다해 무표정 끼움(교감 단독 연속 줄임), P2 꼬리 줄임) / v3 (17·18을 Seedance 2.5 Flash로 다시 뽑은 클립(s17·s18, 첫 프레임부터 말함)으로 바꿈, 녹음 위치 0) / v2 (v1 프레임 확인: 훅 큰 제목이 유튜브 화면 글자 위에 겹침 → 화면을 덜 확대하고 제목을 아래(키보드 쪽)로, 마지막 대사 뒤 5.7초 → 5초 안, 15 자막 줄 나눔) / v1 — 7비트 + 카메라 계획(03_스토리보드/7화_카메라계획_v1.md, 매치컷 5). 틀: build_ep6_v6.py
# 샌드박스: ~/ep8/{v, img, ov(ep7_ov.py), ed(aNN.wav), lc, timing.json}. 6화 정우 웃음(r505)·4화 시계(o608a/b)·코트(r406)는 복사
# 샌드박스: ~/ep7/{v(vNN·rNNN), img, ov, ed(aNN.wav), lc, timing.json}, ~/ep2/sfx3, ~/ed/usfx, ~/music, ~/fonts. 시계 반짝임·코트 컷은 5화 것(~/ep6: o608a/b, r406)을 복사
# 대사 클립은 모델이 말을 늦게 시작한 것이 있어(클립 소리와 원래 녹음을 맞춰 잼) OFF만큼 뒤에서 자름: 03 1.01 / 05 0.97 / 11 1.11 / 13 0.47
import subprocess, os, json, re, shutil
from PIL import ImageFont
H='/home/user'; E=H+'/ep8/'; V=E+'v/'; A=E+'ed/'; IMG=E+'img/'; OV=E+'ov/'; LC=E+'lc/'; X=H+'/ep2/sfx3/'; U=H+'/ed/usfx/'; M=H+'/music/'
os.makedirs(LC,exist_ok=True)
for s,d in [(H+'/ep7/ov/o608a.png',OV),(H+'/ep7/ov/o608b.png',OV),(H+'/ep7/v/r406.mp4',V),(H+'/ep7/v/r505.mp4',V)]:
    if not os.path.exists(d+os.path.basename(s)): shutil.copy(s,d)
TJ=json.load(open(E+'timing.json'))
OFF=json.load(open(E+'off.json'))  # 클립 소리와 원래 녹음을 맞춰 잼 + 입 모양 프레임 확인(17 1.46, 18 1.65, 08 0.6)
SPD={}
VID={'17':'s17','18':'s18'}  # v3: Seedance 다시
for k in VID: OFF[k]=0.0
def run(c): subprocess.run(c,check=True)
def v1(c): return TJ[c]['v1']
def v0(c): return TJ[c]['v0']
def W(c): return TJ[c]['words']
def wt(c,key,default,last=False):
    hits=[s for w,s,e in W(c) if key in w]
    return (hits[-1] if last else hits[0]) if hits else default
cache={}
def img(name,d,mode='in'):
    key=(name,round(d,2),mode)
    if key in cache: return cache[key]
    src=OV+name+'.png' if os.path.exists(OV+name+'.png') else IMG+'i'+name+'.png'
    out=LC+f"{name}_{mode}_{int(d*100)}.mp4"; n=int(round(d*24))
    z={'in':"1.05+0.0025*on",'out':"1.25-0.0025*on",'slow':"1.02+0.0008*on",'msg':"1.45+0.002*on",'msgh':"1.45+0.002*on",'yt':"1.6+0.002*on",'stamp':"1.12+0.002*on",'phone':"1.22+0.002*on"}[mode]
    cx,cy={'yt':(0.40,0.37),'stamp':(0.49,0.47),'msgh':(0.59,0.47),'phone':(0.55,0.52)}.get(mode,(0.5,0.5))
    vf=f"scale=1440:2560,zoompan=z='{z}':x='iw*{cx}-(iw/zoom/2)':y='ih*{cy}-(ih/zoom/2)':d={n}:s=720x1280:fps=24,format=yuv420p"
    run(['ffmpeg','-nostdin','-v','error','-y','-loop','1','-i',src,'-vf',vf,'-t',str(d),'-c:v','libx264','-preset','veryfast','-crf','19',out])
    cache[key]=out; return out
P=[]; EV=[]; SUB=[]; FL=[]; HIT=[]; WARN=[]; T=0.0; MK={}
def add(segs,au=(),subs=(),ev=()):
    global T
    for f,o,v,k,tr in list(au)+list(ev): EV.append((f,T+o,v,k,tr))
    for s in segs: P.append(s)
    for a,b,txt,st in subs:
        SUB.append((T+a,T+b,txt,st))
        if st=='Hit': HIT.append(T+a)
    T+=sum(s[2] for s in segs)
# 자막: 교감 DV, 정우 DJ, 동료 교사 A N, 나머지 다해 DD
SP={**{c:'DV' for c in ['01','02','03','04','05','08','09','10','11','16','17','19']},'07':'DJ'}
Y='{\\c&H0078E0FF&\\fscx120\\fscy120}'
def K(w): return Y+w+'{\\r}'
YN='{\\c&H0078E0FF&}'
POP='{\\fscx170\\fscy170\\t(0,150,\\fscx100\\fscy100)}'
_fw=ImageFont.truetype(H+'/fonts/NanumGothicBold.ttf',40)
def vis(p): return re.sub(r'\{[^}]*\}','',p)
def chunks(text,c,a=None):
    parts=[p.strip() for p in text.split('|') if p.strip()]
    a=v0(c) if a is None else a; b=v1(c)
    tot=sum(len(vis(p)) for p in parts); t=a; out=[]; st=SP.get(c,'DD')
    for p in parts:
        if _fw.getlength(vis(p))>560: WARN.append((c,vis(p)))
        d=(b-a)*len(vis(p))/tot; out.append((t,t+d,p,st)); t+=d
    return out
def seg(c,what,t,d):
    if what=='v': return (V+VID.get(c,f'v{c}')+'.mp4',t*SPD.get(c,1.0)+OFF.get(c,0.0),d)
    if what.startswith('clip:'):
        nm=what[5:]; o=0.3
        if '@' in nm: nm,o=nm.split('@'); o=float(o)
        return (V+nm+'.mp4',o,d)
    return None
def speak(c,plan,text,tail=0.12,ev=(),sub_style=None):
    L=v1(c)+tail; segs=[]; pts=plan+[(L,None)]
    for i in range(len(pts)-1):
        t,what=pts[i][0],pts[i][1]; d=round(pts[i+1][0]-t,3)
        if d<=0.05: continue
        s=seg(c,what,t,d)
        segs.append(s if s else (img(what,d,pts[i][2] if len(pts[i])>2 else 'in'),0,d))
    add(segs,[(AW(c),0,1.0,'d',None)],chunks(text,c),ev)
FX={}
DH=['06','12','13','14','15','18']
for c in DH:
    run(['ffmpeg','-nostdin','-v','error','-y','-i',A+f'a{c}.wav','-af','equalizer=f=170:t=q:w=1.0:g=3,equalizer=f=3000:t=q:w=1.0:g=2.5,acompressor=threshold=0.08:ratio=3:attack=5:release=120:makeup=1.6',A+f'e{c}.wav'])
def AW(c): return A+('a08q.wav' if c=='08' else f'e{c}.wav' if c in DH else f'a{c}.wav')
run(['ffmpeg','-nostdin','-v','error','-y','-i',A+'a08.wav','-af','volume=-3.5dB',A+'a08q.wav'])  # v4: 고함이 다른 교감 줄보다 4dB 큼
PING=X+'s18.mp3'
# ================= ① 굴욕/위기 (훅): 유튜브 '학맞통 우수사례' → 업무분장표 → 반려 도장. 대사 자막 없이 제목만 =================
run(['ffmpeg','-nostdin','-v','error','-y','-ss','0.22','-t','0.25','-i',U+'mouse_click.mp3','-af','afade=t=out:st=0.18:d=0.07',A+'click.wav'])
run(['ffmpeg','-nostdin','-v','error','-y','-i',X+'s23.mp3','-af','asetrate=44100*0.8,aresample=44100,lowpass=f=2500,volume=1.6',A+'thud.wav'])  # 묵직한 도장 '쿵'
add([(V+'v02.mp4',3.9,0.7),(img('o741',1.1,'yt'),0,1.1),(img('o742',0.9,'in'),0,0.9),(V+'v16.mp4',0.5,0.5),(img('o743',1.5,'stamp'),0,1.5)],
    subs=[(0.1,4.7,"{\\an5\\pos(360,800)\\fad(150,0)}학맞통 우수사례 보더니\\N{\\alpha&HFF&\\t(1400,1410,\\alpha&H00&)\\fscx150\\fscy150\\t(1400,1560,\\fscx100\\fscy100)}"+YN+"\"계약직이 하기 딱이네\"",'HookT')],
    ev=[(PING,0.75,0.6,'s',None),(A+'thud.wav',3.5,1.0,'s',None)])
HIT.append(3.5)
# ================= ② 세계 제시: 심심한 교감, 유튜브 =================
MK['s1']=T; MK['t01']=T
speak('01',[(0,'v')],'아이고, 심심해…|유튜브나 볼까.',tail=0.35,ev=[(A+'click.wav',v1('01')+0.08,1.0,'s',None),(A+'click.wav',v1('01')+0.3,0.8,'s',None)])
speak('02',[(0,'v'),(1.4,'clip:r741@2.2'),(2.5,'v')],'보일러를 고쳐 줘?|고기도 구워 주고?',tail=0.15)
speak('03',[(0,'v'),(2.1,'clip:v06@3.2'),(3.1,'v')],'이거…|'+K('계약직이 하기 딱이네')+'.',tail=0.2)
# ================= ③ 정체 떡밥: 재단 봉투 '인사' → 다해 만년필 서명 =================
add([(img('o744',1.6,'slow'),0,1.6),(V+'r745.mp4',0.4,1.6)],ev=[(PING,0.2,0.35,'s',None)])
MK['b1_end']=T
# ================= ④ 압박 상승 =================
speak('04',[(0,'v'),(2.6,'clip:r731@0.5')],'업무 경감 공문 왔어요.|다들 일 좀 줄여 드릴게요.',tail=0.6)
add([(img('o742',1.5,'in'),0,1.5)],ev=[(X+'s19.mp3',0.3,0.45,'s',None)])
MK['t05']=T
g05=wt('05','고기',3.4)
speak('05',[(0,'v'),(g05-0.1,'clip:r741@0.3'),(g05+1.1,'v'),(6.0,'clip:v06@3.6'),(7.0,'v')],'학맞통은 독고 선생이 맡아요.|제일 쉬운 걸로.|애들 고기나 구워 주고,|보일러 잘 돌아가나|봐 주면 되겠네.',tail=0.1)
MK['dh']=T
speak('06',[(0,'v')],'알겠습니다.',tail=1.0)
MK['t07']=T
speak('07',[(0,'v')],'그거 혼자 하는 거|아니지 않아요? 위원회로…',tail=0.1)
speak('08',[(0,'v')],'안 선생은 빠져요.|자기 일이나 해요.',tail=0.1)
add([(V+'r733.mp4',0.3,1.2)])
MK['day2']=T
add([(V+'r732.mp4',0.2,1.8)])
speak('09',[(0,'v'),(2.2,'clip:v14@3.6'),(3.2,'v')],'학맞통 담당자 연수?|출장비 없어요.',tail=0.1)
MK['t10']=T
speak('10',[(0,'v'),(2.6,'clip:r733@2.2'),(3.7,'v')],'이게 학교에 도움 되는 건지,|'+K('개인에게 도움')+' 되는 건지|구분해요.',tail=0.1)
speak('11',[(0,'v'),(2.7,'clip:v12@3.4'),(3.8,'v')],'고기 굽는 데 무슨 연수야.|그런 것도 배워야 하나?|뭐 하나 제대로 하는 게 없어.',tail=0.15)
MK['b2_end']=T
# ================= ⑤ 반전: 공문 마지막 줄 =================
speak('12',[(0,'v')],'학교에 도움 되라고|맡기신 업무요.',tail=0.15)
speak('13',[(0,'v')],'이 공문,|끝까지 보셨어요?',tail=0.1)
MK['reveal']=T
add([(img('o746',1.9,'in'),0,1.9)],ev=[(X+'s23.mp3',0.1,0.9,'s',None)])
HIT.append(MK['reveal']+0.1)
# ================= ⑥ 카타르시스 =================
MK['t14']=T
speak('14',[(0,'v')],POP+K('위원장')+', 교감 선생님이세요.',tail=0.2)
HIT.append(MK['t14']+v0('14'))
speak('15',[(0,'v'),(1.3,'clip:r741@3.0'),(2.2,'v')],'보일러는…|위원장님이|먼저 배우셔야겠네요.',tail=0.2)
MK['t16']=T
speak('16',[(0,'v')],'아니, 그건…|공문이…',tail=0.15,ev=[(U+'boing2.mp3',0.05,0.4,'s',None)])
add([(V+'r505.mp4',0.3,1.4)])
MK['stamp']=T
add([(V+'r734.mp4',0.6,1.4)],ev=[(X+'s23.mp3',0.25,1.0,'s',None)])
HIT.append(MK['stamp']+0.25)
speak('17',[(0,'v')],'…다녀와요.|출장비는 없어요.',tail=0.1)
speak('18',[(0,'v')],'네.|결재 감사합니다.',tail=0.4)
FL.append(T+0.42)
add([(img('o608a',0.4,'in'),0,0.4),(img('o608b',0.5,'in'),0,0.5),(V+'r406.mp4',0.2,1.0)],ev=[(PING,0.0,0.4,'s',None)])
MK['b3_end']=T
# ================= ⑦ 클리프행어: 봉투 → 멈칫 → 퇴근길 다해 얼굴 =================
MK['s7']=T; MK['song']=T
speak('19',[(0,'v')],'차기 교장… 내정…?|역시 나지.',tail=0.1)
MK['last_end']=T-0.1
run(['ffmpeg','-nostdin','-v','error','-y','-t','1.3','-i',U+'papercrackle.mp3','-af','afade=t=out:st=0.9:d=0.4',A+'crackle.wav'])
add([(V+'r735.mp4',0.4,1.3),(V+'r736.mp4',0.3,1.0)],ev=[(A+'crackle.wav',0.05,0.8,'s',None)])
MK['fin']=T
_fin=img('o736f',2.0,'slow'); FX[_fin]=',drawbox=y=ih*0.62:w=iw:h=ih*0.38:c=black@0.22:t=fill,drawbox=y=ih*0.72:w=iw:h=ih*0.28:c=black@0.22:t=fill,drawbox=y=ih*0.82:w=iw:h=ih*0.18:c=black@0.22:t=fill'  # 아래 30% 어둡게
add([(_fin,0,2.0)])
total=T
CAPL='{\\an7\\pos(40,86)\\fs34}'  # 시간 글자는 왼쪽 위 한곳(이름표 바로 위)
SUB+=[(MK['s1']+0.1,MK['s1']+1.9,CAPL+'오후 3시','Cap'),
      (MK['t01']+0.3,MK['t01']+2.0,'교감','Tag'),
      (MK['t05']+0.2,MK['t05']+2.6,CAPL+'학맞통 = 학생맞춤통합지원','Cap'),
      (MK['dh']+0.05,MK['dh']+1.9,'{\\fs40}독고다해 · 계약교사\\N{\\fs24}(극 중 설정)','Tag'),
      (MK['t07']+0.3,MK['t07']+2.2,'안정우 · 통합과학 교사','Tag'),
      (MK['day2']+0.05,MK['day2']+1.75,CAPL+'다음 날 · 오후 4시 30분','Cap'),
      (MK['s7']+0.05,MK['s7']+1.5,CAPL+'오후 5시','Cap'),
      (MK['fin']+0.15,MK['fin']+2.0,'{\\pos(360,880)\\fad(150,0)\\fscx120\\fscy120}차기 교장은\\N누가 될 것인가?','Ono'),
      (MK['fin']+0.6,MK['fin']+2.0,'{\\pos(360,1050)\\fnNanumGothic\\b1\\fs28\\fsp3\\bord3\\c&H0078E0FF&}교사X 8화 · 12월 4일(금) 저녁 6시','Ono')]
EV.append((X+'B1.mp3',MK['s1'],0.35,'s',('cut',MK['b1_end']-MK['s1'])))
EV.append((X+'B2.mp3',MK['b1_end'],0.4,'s',('seek',0.0,MK['reveal']-MK['b1_end'])))  # 공문 인서트 '쿵'에서 음악 끊음
EV.append((X+'B2.mp3',MK['t16'],0.4,'s',('seek',40.0,MK['b3_end']-MK['t16'])))  # '위원장'·'보일러'는 정적, 교감 말문 막히는 데서 다시
EV.append((M+'Orange_on_the_Floor.mp3',MK['song'],0.38,'s',('end',total-MK['song'])))

print('total',round(total,2),{k:round(v,2) for k,v in MK.items()})
os.makedirs(E+'ed/seg',exist_ok=True); F=[]; CUM=0.0
for i,(f,s,dd) in enumerate(P):
    o=E+f'ed/seg/s{i:03d}.mp4'
    n0=round(CUM*24); CUM+=dd; nf=max(1,round(CUM*24)-n0)
    run(['ffmpeg','-nostdin','-v','error','-y','-ss',str(max(0,s)),'-i',f,'-vf',"scale=720:1280,fps=24"+FX.get(f,"")+",tpad=stop_mode=clone:stop_duration=2,format=yuv420p",'-frames:v',str(nf),'-an','-c:v','libx264','-preset','veryfast','-crf','19',o]); F.append(o)
open(E+'ed/seg/l.txt','w').write(''.join(f"file '{x}'\n" for x in F))
run(['ffmpeg','-nostdin','-v','error','-y','-f','concat','-safe','0','-i',E+'ed/seg/l.txt','-c','copy',E+'ed/pic.mp4'])
cmd=['ffmpeg','-nostdin','-v','error','-y']
for e in EV: cmd+=['-i',e[0]]
fl=''; dl=[]; sl=[]
for i,(f,at,v,k,tr) in enumerate(EV):
    ex=''
    if tr:
        if tr[0]=='seek': ex=f',atrim={tr[1]:.3f}:{tr[1]+tr[2]:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.3,afade=t=out:st={max(0,tr[2]-0.6):.3f}:d=0.6'
        if tr[0]=='cut': ex=f',atrim=0:{tr[1]:.3f},afade=t=in:d=0.6,afade=t=out:st={max(0,tr[1]-0.4):.3f}:d=0.4'
        if tr[0]=='end': ex=f',atrim=0:{tr[1]:.3f},afade=t=in:d=1.0,afade=t=out:st={tr[1]-4.0:.3f}:d=4.0'
    ms=max(0,int(round(at*1000)))
    fl+=f"[{i}:a]aformat=sample_rates=44100:channel_layouts=stereo{ex},volume={v},adelay={ms}|{ms},apad=whole_dur={total}[a{i}];"
    (dl if k=='d' else sl).append(f'[a{i}]')
fl+=''.join(dl)+f"amix=inputs={len(dl)}:normalize=0,asplit=2[D1][D2];"
fl+=''.join(sl)+f"amix=inputs={len(sl)}:normalize=0[SX];[SX][D2]sidechaincompress=threshold=0.015:ratio=10:attack=20:release=350[SD];"
fl+=f"[D1][SD]amix=inputs=2:normalize=0,atrim=0:{total}[out]"
cmd+=['-filter_complex',fl,'-map','[out]','-c:a','pcm_s16le',E+'ed/aud_pre.wav']; run(cmd)
_m=subprocess.run(['ffmpeg','-nostdin','-i',E+'ed/aud_pre.wav','-af','ebur128','-f','null','-'],capture_output=True,text=True).stderr
_I=float(re.findall(r'I:\s+(-?[0-9.]+) LUFS',_m)[-1]); _g=-14.0-_I; print('pre I',_I,'gain',round(_g,2))
run(['ffmpeg','-nostdin','-v','error','-y','-i',E+'ed/aud_pre.wav','-af',f'volume={_g:.2f}dB,alimiter=limit=0.6:level=false:attack=1:release=50','-c:a','aac','-b:a','192k',E+'ed/aud.m4a'])
def ts(x): x=max(0,x); h=int(x//3600); m=int(x%3600//60); s=x%60; return f"{h}:{m:02d}:{s:05.2f}"
head=open(H+'/ep2/sub_v2_header.ass').read().replace('\n\n[Events]','\nStyle: HookT,Black Han Sans,58,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,5,3,2,24,24,150,1\n\n[Events]',1)
for a,b,txt,st in SUB: head+=f"Dialogue: 0,{ts(a)},{ts(b)},{st},,0,0,0,,{txt}\n"
open(E+'ed/sub.ass','w').write(head)
flash=','.join(f"drawbox=c=white@0.85:t=fill:enable='between(t,{x:.2f},{x+0.08:.2f})'" for x in FL)
SH='+'.join(f"between(t,{x:.2f},{x+0.25:.2f})" for x in HIT) or '0'
shake=f"crop=w=696:h=1256:x='12+11*sin(2*PI*t*26)*({SH})':y='12+11*cos(2*PI*t*21)*({SH})',scale=720:1280"
_B=sorted([x for x in SUB if x[3] in ('DV','DJ','DD','N','Hit')])
OVL=[(round(_B[i][0],2),vis(_B[i][2]),vis(_B[i+1][2])) for i in range(len(_B)-1) if _B[i][1]>_B[i+1][0]+0.01]
print('SUB OVERLAP',OVL)
print('WARN long lines',WARN); print('HIT',[round(h,2) for h in HIT])
outn=E+'ed/ep7_v10.mp4'
run(['ffmpeg','-nostdin','-v','error','-y','-i',E+'ed/pic.mp4','-i',E+'ed/aud.m4a','-vf',f"setpts=N/(24*TB),{flash},{shake},ass={E}ed/sub.ass:fontsdir={H}/fonts,fade=t=out:st={total-0.6:.2f}:d=0.6",'-c:v','libx264','-preset','veryfast','-crf','20','-c:a','copy','-shortest',outn])
print('ok',outn)
_lw=MK['last_end']
_cuts=subprocess.run(['ffmpeg','-i',outn,'-vf',"select='gt(scene,0.2)',showinfo",'-an','-f','null','-'],capture_output=True,text=True).stderr.count('pts_time:')
print(f"""[편집장 측정값]
전체 길이: {total:.1f}초 / 컷 수: {_cuts} / 평균 컷 길이: {total/max(1,_cuts+1):.1f}초
마지막 대사 끝: {_lw:.1f}초 / 그 뒤 말 없는 구간: {total-_lw:.1f}초
훅: 유튜브 우수사례 1.7 → 업무분장표 1.4 → 반려 도장 1.6초(대사 없음, 제목만)
자막 겹침: {len(OVL)}건""")
