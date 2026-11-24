# 교사X 9화(AI가 쓴 숙제) 편집 v6 (사장님 11/24 "7초 전후의 똑딱이는 부분이 편집 실수처럼 느껴져": 강조음 PING이 '빠른 시계 째깍(s18)'이었음 → 짧은 '띡' 합성음으로 바꿈, 키보드(4.2초)가 다음 컷까지 이어짐 → 정우 컷 1.3초만·학생 붙여 넣기 0.5초만) / v5 (v4 점검: 함정·붙여 넣기 큰 자막이 문서 글자 위 → 아래(y1170), 학부모 자막이 폰 알림 가림 → 위로, 학부모 +5.8dB → 줄임, 03 -3.9dB → +6, '다른 학생 방'·'금요일 밤' 캡션 0.25초 겹침, 꼬리 5.0 → 4.9) / v4 — 사장님 11/23 v3 지적 8개 + 다른 AI 분석 중 맞는 것(06_검수/v3_지적_판정_v4계획.md): 화분 장면 뺌, 22·11·교감 6줄·다해 17·21 새 영상, 다해 17~21 차갑게 다시 녹음, 학부모 목소리 2개(전화 음질)+진동, 함정·붙여 넣기·손글씨 가운데 큰 자막, 정면 화면 그림(ep9_ov4), 7장 넘김 점점 빠르게, 키워드 쾅, 발령 2초+형광펜, 마지막 입 다문 얼굴, 듣는 화면 말소리 끝 자동 확인 / v3
# 틀: build_ep8_v8.py. 샌드박스 ~/ep10/{v(vNN·rNNN), img, ov(ep9_ov.py), ed(aNN.wav·timing은 prep_ep9.py), lc}
# 정우 화면(교무실 낮·남색 조끼) vs 학생 화면(집 밤·초록 교복) 구분 + 캡션 '과제 내던 날 · 교무실' / '그날 밤 · 학생 방'
# 녹음 위치(off.json): 상호상관 대신 말소리 시작 차이(04 0.56, 16 0.18, 17 0.16, 나머지 0~0.04)
import subprocess, os, json, re, shutil
from PIL import ImageFont
H='/home/user'; E=H+'/ep10/'; V=E+'v/'; A=E+'ed/'; IMG=E+'img/'; OV=E+'ov/'; LC=E+'lc/'; X=H+'/ep2/sfx3/'; U=H+'/ed/usfx/'; M=H+'/music/'
os.makedirs(LC,exist_ok=True)
TJ=json.load(open(E+'timing.json'))
OFF=json.load(open(E+'off.json')); VE=json.load(open(E+'voice_end.json'))  # v4: prep_ep9_v4.py가 잼(말소리 시작 차이, 클립 말소리 끝)
SPD={}
VID={}
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
    z={'ribbon':"1.8+0.002*on",'screen':"1.55+0.002*on",'form':"1.2+0.0015*on",'notif9':"2.0+0.0015*on",'chart':"1.25+0.002*on",'notice':"1.25+0.002*on",'in':"1.05+0.0025*on",'out':"1.25-0.0025*on",'slow':"1.02+0.0008*on",'msg':"1.45+0.002*on",'msgh':"1.45+0.002*on",'yt':"1.35+0.002*on",'meat':"2.1+0.001*on",'stamp':"1.12+0.002*on",'phone':"1.22+0.002*on",'memo':"1.7+0.001*on",'notif':"2.3+0.001*on"}[mode]
    cx,cy={'ribbon':(0.76,0.69),'screen':(0.69,0.43),'form':(0.5,0.62),'notif9':(0.668,0.339),'chart':(0.5,0.42),'notice':(0.5,0.42),'meat':(0.25,0.6),'yt':(0.43,0.37),'stamp':(0.49,0.47),'msgh':(0.59,0.47),'phone':(0.55,0.52),'memo':(0.62,0.70),'notif':(0.665,0.376)}.get(mode,(0.5,0.5))
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
SP={**{c:'DV' for c in ['01','05','06','08','10','14','16']},**{c:'DJ' for c in ['02','03','04','07','22']},'09':'N','p1':'N','p2':'N'}
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
        if nm in VE and o < VE[nm]-0.05: raise SystemExit(f'듣는 화면 {nm}@{o}: 이 클립은 {VE[nm]}초까지 입이 움직임')  # v4: 사장님 11/23 지적
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
# 줄마다 -24 LUFS로 맞춘 뒤(n), 다해 줄은 EQ·압축(e), 정우 속마음 02·03은 울림
def lufs(p):
    m=subprocess.run(['ffmpeg','-nostdin','-i',p,'-af','ebur128','-f','null','-'],capture_output=True,text=True).stderr
    return float(re.findall(r'I:\s+(-?[0-9.]+) LUFS',m)[-1])
DH=['11','12','13','15','17','18','19','20','21','23','24']
GAIN={}
for c in [f'{i:02d}' for i in range(2,25)]+['p1','p2']:
    g=max(-6,min(10,-24.0-lufs(A+f'a{c}.wav')))+{'02':7.0,'03':6.0}.get(c,0.0); GAIN[c]=round(g,1)  # v2: 속마음 울림·배경음에 묻혀 더 키움
    af=f'volume={g:.2f}dB'
    if c in DH: af+=',equalizer=f=170:t=q:w=1.0:g=3,equalizer=f=3000:t=q:w=1.0:g=2.5,acompressor=threshold=0.08:ratio=3:attack=5:release=120:makeup=1.6'
    if c in ('02','03'): af+=',aecho=0.6:0.5:40:0.25,alimiter=limit=0.9'
    if c in ('p1','p2'): af+=',highpass=f=320,lowpass=f=3300,acompressor=threshold=0.1:ratio=4,volume=0.9'  # 전화 음질
    run(['ffmpeg','-nostdin','-v','error','-y','-i',A+f'a{c}.wav','-af',af,A+f'n{c}.wav'])
print('GAIN',GAIN)
def AW(c): return A+f'n{c}.wav'
run(['ffmpeg','-nostdin','-v','error','-y','-f','lavfi','-i',"aevalsrc='0.45*sin(2*PI*1320*t)*exp(-t*28)':s=44100:d=0.25",A+'blip.wav'])
PING=A+'blip.wav'  # v6: s18은 '빠른 시계 째깍' 소리라 강조음으로 쓰면 똑딱거림(사장님 지적)
run(['ffmpeg','-nostdin','-v','error','-y','-f','lavfi','-i',"aevalsrc='0.5*sin(2*PI*165*t)*sin(2*PI*30*t)*lt(mod(t\\,0.55)\\,0.38)':s=44100:d=1.2",A+'vib.wav'])  # 휴대폰 진동(코드 합성)
VIB=A+'vib.wav'
run(['ffmpeg','-nostdin','-v','error','-y','-i',X+'s23.mp3','-af','asetrate=44100*0.8,aresample=44100,lowpass=f=2500,volume=1.6',A+'thud.wav'])
IN='{\\i1}'
BIG='{\\an5\\pos(360,1170)\\fad(80,0)\\fscx130\\fscy130\\bord7\\c&H0000E6FF&}'   # 가운데 큰 노란 자막
RED='{\\an5\\pos(360,640)\\fad(80,0)\\fscx125\\fscy125\\bord7\\c&H3030FF&}'      # 가운데 큰 붉은 자막
def KW(t,w): return (t,t+0.9,'{\\an5\\pos(360,560)\\fscx260\\fscy260\\t(0,140,\\fscx200\\fscy200)\\bord8\\c&H0000E6FF&}'+w,'Ono')
# ================= 훅(결말 먼저, 제목만): 첫 프레임부터 '그게 바로 역차별입니다' + 쿵 =================
add([(V+'v21.mp4',0.2,1.1),(V+'v16.mp4',2.0,0.8),(img('o906p7',0.8,'in'),0,0.8),(V+'r930.mp4',0.5,0.8)],
    subs=[(0.1,3.45,"{\\an5\\pos(360,800)\\fad(150,0)}AI가 쓴 숙제,\\N{\\alpha&HFF&\\t(1500,1510,\\alpha&H00&)\\fscx150\\fscy150\\t(1500,1660,\\fscx100\\fscy100)}"+YN+"점수 줘야 할까?",'HookT')],
    au=[(AW('21'),0.0,1.0,'d',None)],ev=[(A+'thud.wav',0.0,0.9,'s',None),(A+'thud.wav',1.9,0.7,'s',None),(PING,3.0,0.5,'s',None)])
HIT.append(0.05); HIT.append(1.9)
# ================= ② 함정(교사) → 붙여 넣기(학생) → 손글씨(다른 학생) =================
MK['s1']=T; MK['trap']=T
add([(V+'r902.mp4',0.4,1.3),(img('o902a',1.1,'in'),0,1.1),(img('o902b',1.2,'in'),0,1.2)],ev=[(X+'s26.mp3',0.0,0.5,'s',('cut',1.3)),(PING,2.45,0.5,'s',None)],
    subs=[(0.2,3.5,BIG+'정우 선생님이\\N과제에 숨긴 함정','Ono')])
MK['stu']=T
add([(V+'r903.mp4',0.3,1.3),(img('o903f',2.1,'in'),0,2.1)],ev=[(X+'s26.mp3',0.5,0.4,'s',('cut',0.5)),(PING,1.4,0.4,'s',None),(PING,2.6,0.4,'s',None)],
    subs=[(0.1,1.3,BIG+'학생은 과제를 통째로\\NAI에 붙여 넣음','Ono')])
MK['hand']=T
add([(V+'r904.mp4',0.3,2.1)],subs=[(0.1,2.1,RED+'AI 없이 밤새\\N직접 쓴 학생','Ono')])
# ================= 금요일 밤 채점: 02·03 속마음(7장 점점 빠르게 + 쿵) =================
MK['night']=T
speak('02',[(0,'clip:r905@0.2'),(2.3,'o906p1','in')],IN+'(속마음) 통합과학 보고서…|'+IN+'이상하게 문장이 다 똑같네.',tail=0.1)
_pp=[0,1.0,1.9,2.6,3.1,3.5]
speak('03',[(t,f'o906p{k+2}','in') for k,t in enumerate(_pp)],IN+K('초록 고양이')+'…|'+IN+'이것도, 이것도.|'+IN+'일곱 장이 다.',tail=0.1,ev=[(A+'thud.wav',t+0.02,0.55+0.07*k,'s',None) for k,t in enumerate(_pp)])
# ================= ③ 주말: 학부모 전화(목소리 2개) → 민원 접수 =================
MK['phone']=T
add([(img('o907b',3.95,'in'),0,3.95)],au=[(AW('p1'),0.35,1.0,'d',None)],ev=[(VIB,0.0,0.9,'s',None)],
    subs=[(0.35+v0('p1'),0.35+v1('p1'),'(학부모 전화) 선생님, AI 쓰지 말라는 말이|'.split('|')[0],'N')])
SUB[-1]=(SUB[-1][0],SUB[-1][0]+(v1('p1')-v0('p1'))*0.55,'{\\pos(360,1150)}(학부모 전화) 선생님,\\NAI 쓰지 말라는 말이','N'); SUB.append((SUB[-1][1],MK['phone']+0.35+v1('p1'),'{\\pos(360,1150)}어디 있었나요?','N'))
MK['p2']=T
add([(img('o908',4.0,'form'),0,4.0)],au=[(AW('p2'),0.2,1.0,'d',None)],ev=[(VIB,0.0,0.7,'s',None),(X+'s15.mp3',3.6,0.5,'s',None)],
    subs=[(0.2+v0('p2'),0.2+v0('p2')+(v1('p2')-v0('p2'))*0.5,'{\\pos(360,1150)}(학부모 전화) 애들한테\\N함정을 판 거예요?','N'),(0.2+v0('p2')+(v1('p2')-v0('p2'))*0.5,0.2+v1('p2'),'{\\pos(360,1150)}내일 학교로 찾아가겠습니다.','N')])
MK['t04']=T
speak('04',[(0,'v')],'…주말에 개인 번호로|이렇게까지.',tail=0.3)
# ================= ④ 교감 떠넘기기(현실 톤 다시) =================
MK['t05']=T
speak('05',[(0,'v')],'안 선생,|민원 들어온 거 알죠?',tail=0.1,ev=[(X+'s16.mp3',0.3,0.6,'s',None)])
speak('06',[(0,'v'),(2.6,'clip:v07@3.0'),(3.6,'v')],'애들이 AI 좀|참고한 거 가지고 뭘.|점수 그냥 주고 끝내요.',tail=0.1)
speak('07',[(0,'v')],'그럼…|직접 쓴 애들은요?',tail=0.15)
speak('08',[(0,'v'),(2.4,'clip:v07@3.6'),(3.4,'v')],'학부모님께 사과 전화도 드리고.|선생님 선에서 끝내요.|일 키우지 말고.',tail=0.1)
MK['t09']=T
speak('09',[(0,'v'),(2.8,'clip:r923@0.2'),(3.9,'v')],'교감 선생님, 그건 아니죠.|이건 범죄를 키우는 거라|생각해요.',tail=0.1)
speak('10',[(0,'v'),(2.6,'clip:v07@3.2'),(3.6,'v')],'들었죠.|애들 범죄자 만들 건가요?|일 커지면 학교만 시끄러워요.',tail=0.1)
# ================= ⑤ 다해: 국어로 누르기(키워드 쾅) → 책임 =================
MK['dh']=T
speak('11',[(0,'v')],K('참고')+'는, 남의 글을 읽고|제 생각을 쓰는 겁니다.',tail=0.1)
MK['t12']=T
speak('12',[(0,'v'),(2.2,'clip:v14@%.2f'%(VE['v14']+0.05)),(3.0,'v')],'남이 쓴 문장을|제 이름으로 내는 건,|'+K('표절')+'이라고 합니다.',tail=0.1)
SUB.append(KW(MK['t12']+wt('12','표절',2.6),'표절')); HIT.append(MK['t12']+wt('12','표절',2.6))
MK['t13']=T
speak('13',[(0,'v'),(2.0,'clip:v16@%.2f'%(VE['v16']+0.1)),(2.8,'v')],'이건 부정행위고,|'+K('공정성')+'을 무너뜨리는 일입니다.',tail=0.1)
SUB.append(KW(MK['t13']+wt('13','부정',0.4),'부정행위')); SUB.append(KW(MK['t13']+wt('13','공정',1.6),'공정성'))
speak('14',[(0,'v')],'그래서, 민원 커지면|누가 책임져요?|독고 선생이 져요?',tail=0.1)
speak('15',[(0,'v'),(2.5,'o920','chart'),(3.9,'v')],'민원은 학교|민원대응팀이 받습니다.|그 팀장,|'+K('교감 선생님')+'이시죠.',tail=0.1,ev=[(PING,2.55,0.4,'s',None)])
speak('16',[(0,'v')],'그, 그건…',tail=0.3,ev=[(U+'boing2.mp3',0.05,0.4,'s',None)])
# ================= ⑥ 결정타(사장님 확정 17~21, 차갑게 다시 녹음): 음악 끊고 정적 =================
MK['t17']=T
speak('17',[(0,'v'),(2.6,'clip:r923@0.5'),(3.8,'v'),(5.4,'clip:v16@%.2f'%(VE['v16']+0.6)),(6.2,'v')],POP+'교육기본법 제2조.|교육은 인격을 도야하고,|자주적 생활능력을|갖추게 하는 겁니다.',tail=0.1)
HIT.append(MK['t17']+v0('17'))
speak('18',[(0,'clip:r930@0.3'),(1.8,'clip:v16@%.2f'%(VE['v16']+1.4))],'AI가 대신 쓴 글로는,|둘 다 배울 수가 없습니다.',tail=0.1)
speak('19',[(0,'clip:r904@0.3'),(2.4,'clip:v07@3.0')],'점수를 그냥 주면,|밤새 제 손으로 쓴 학생은|뭐가 됩니까.',tail=0.1)
speak('20',[(0,'o924','in'),(2.6,'clip:r930@2.0')],'그 학생이 배우는 건 하나예요.|공부는 바보나 하는 거구나.',tail=0.1)
MK['t21']=T
speak('21',[(0,'v')],POP+'그게 바로 '+K('역차별')+'입니다.',tail=0.4)
HIT.append(MK['t21']+v0('21'))
# ================= ⑥-2 퇴근길: 정우에게(정우는 창가에 멈춰 섬) =================
MK['t22']=T
speak('22',[(0,'v')],'함정까지 판 제가…|잘못한 걸까요.',tail=0.15)
speak('23',[(0,'v'),(2.8,'clip:v22@%.2f'%(VE['v22']+0.1)),(3.6,'v')],'잘 잡긴 했어요.|그런데 아이들은 거기서,|다음엔 안 들키는 법을|생각해야겠다, 할 거예요.',tail=0.1)
speak('24',[(0,'v')],'속이는 걸 잡는 수업 말고,|'+K('속일 필요가 없는 수업')+'을 하세요.',tail=0.15)
MK['last_end']=T-0.15
# ================= ⑦ 인사 발표(5초 안): 발령 화면 2초(형광펜) → 교감 굳음 → 다해 결연한 얼굴 =================
MK['s7']=T; MK['song']=T
add([(img('o927h',2.0,'notice'),0,2.0)],ev=[(X+'s19.mp3',0.3,0.5,'s',None)])
add([(V+'v16.mp4',VE['v16']+0.3,1.0)])
MK['fin']=T
add([(img('929',1.7,'slow'),0,1.7)])
total=T
CAPL='{\\an7\\pos(40,86)\\fs34}'
SUB+=[(MK['trap']+0.05,MK['trap']+3.5,CAPL+'과제 내던 날 · 교무실','Cap'),
      (MK['stu']+0.05,MK['stu']+3.3,CAPL+'그날 밤 · 학생 방','Cap'),
      (MK['hand']+0.05,MK['hand']+2.05,CAPL+'같은 밤 · 다른 학생 방','Cap'),
      (MK['night']+0.05,MK['night']+2.2,CAPL+'금요일 밤 10시 · 교무실','Cap'),
      (MK['phone']+0.05,MK['phone']+3.9,CAPL+'주말 · 정우 개인 휴대폰','Cap'),
      (MK['t04']+0.05,MK['t05']-0.05,'안정우 · 통합과학 교사','Tag'),
      (MK['t05']+0.1,MK['t05']+1.8,'교감','Tag'),
      (MK['t09']+0.1,MK['t09']+1.9,'동료 교사','Tag'),
      (MK['dh']+0.05,MK['dh']+1.9,'독고다해 · 국어 계약교사','Tag'),
      (MK['t22']+0.05,MK['t22']+1.6,CAPL+'퇴근길','Cap'),
      (MK['s7']+0.05,MK['s7']+1.95,CAPL+'오후 5시 · 인사 발표','Cap'),
      (MK['fin']+0.05,MK['fin']+1.7,'{\\pos(360,880)\\fad(150,0)\\fscx120\\fscy120}새 교장,\\N독고다해?','Ono'),
      (MK['fin']+0.3,MK['fin']+1.7,'{\\pos(360,1050)\\fnNanumGothic\\b1\\fs28\\fsp3\\bord3\\c&H0078E0FF&}교사X 10화 · 12월 9일(수) 저녁 6시','Ono')]
EV.append((X+'B1.mp3',MK['trap'],0.35,'s',('cut',MK['t05']-MK['trap'])))
EV.append((X+'B2.mp3',MK['t05'],0.4,'s',('seek',0.0,MK['t17']-MK['t05'])))  # 결정타(17)에서 음악 끊음 → 정적
EV.append((M+'Orange_on_the_Floor.mp3',MK['song'],0.38,'s',('end',total-MK['song'])))

print('total',round(total,2),{k:round(v,2) for k,v in MK.items()})
# v15: 그림 속 글자 컷 타임라인(qa_text.py --tl) — o로 시작하는 글자 그림 클립만
_TL=[]; _c=0.0
for f,s,dd in P:
    _n=os.path.basename(f)
    if _n.startswith('o') and '_' in _n: _TL.append([round(_c,3),round(_c+dd,3),_n.split('_')[0]])
    _c+=dd
json.dump(_TL,open(E+'ed/timeline.json','w'),ensure_ascii=False)
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
head=open(H+'/ep2/sub_v2_header.ass').read().replace(',1,5,1,2,40,100,295,1',',1,7,3,2,40,100,295,1').replace(',1,4,1,2,40,100,295,1',',1,7,3,2,40,100,295,1').replace('\n\n[Events]','\nStyle: HookT,Black Han Sans,58,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,5,3,2,24,24,150,1\n\n[Events]',1)
for a,b,txt,st in SUB: head+=f"Dialogue: 0,{ts(a)},{ts(b)},{st},,0,0,0,,{txt}\n"
open(E+'ed/sub.ass','w').write(head)
flash=','.join(f"drawbox=c=white@0.85:t=fill:enable='between(t,{x:.2f},{x+0.08:.2f})'" for x in FL) or 'null'  # 8화: 흰 번쩍임 없음 → 빈 필터 대신 null
SH='+'.join(f"between(t,{x:.2f},{x+0.25:.2f})" for x in HIT) or '0'
shake=f"crop=w=696:h=1256:x='12+11*sin(2*PI*t*26)*({SH})':y='12+11*cos(2*PI*t*21)*({SH})',scale=720:1280"
_B=sorted([x for x in SUB if x[3] in ('DV','DJ','DD','N','Hit')])
OVL=[(round(_B[i][0],2),vis(_B[i][2]),vis(_B[i+1][2])) for i in range(len(_B)-1) if _B[i][1]>_B[i+1][0]+0.01]
print('SUB OVERLAP',OVL)
print('WARN long lines',WARN); print('HIT',[round(h,2) for h in HIT])
outn=E+'ed/ep9_v6.mp4'
run(['ffmpeg','-nostdin','-v','error','-y','-i',E+'ed/pic.mp4','-i',E+'ed/aud.m4a','-vf',f"setpts=N/(24*TB),{flash},{shake},ass={E}ed/sub.ass:fontsdir={H}/fonts,fade=t=out:st={total-0.6:.2f}:d=0.6",'-c:v','libx264','-preset','veryfast','-crf','20','-c:a','copy','-shortest',outn])
print('ok',outn)
_lw=MK['last_end']
_cuts=subprocess.run(['ffmpeg','-i',outn,'-vf',"select='gt(scene,0.2)',showinfo",'-an','-f','null','-'],capture_output=True,text=True).stderr.count('pts_time:')
print(f"""[편집장 측정값]
전체 길이: {total:.1f}초 / 컷 수: {_cuts} / 평균 컷 길이: {total/max(1,_cuts+1):.1f}초
마지막 대사 끝: {_lw:.1f}초 / 그 뒤 말 없는 구간: {total-_lw:.1f}초
훅: 첫 프레임부터 '그게 바로 역차별입니다'+쿵 / 다해 1.1 → 교감 0.8 → 초록 고양이 7장 0.8 → 교감 0.8초(대사 자막 없음, 제목만)
자막 겹침: {len(OVL)}건""")
