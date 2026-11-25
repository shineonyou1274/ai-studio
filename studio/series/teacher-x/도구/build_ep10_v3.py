# 교사X 10화 편집 v3 (사장님 11/25 효과음 직접 고름: 박수·환호, 파쇄기, 웃음 — Pixabay, ~/ed/usfx) / v2 (사장님 11/25 Gemini·다른 AI 검수 '대부분 동의': 훅 '집니—' 잘림, 박수 무음, 엔딩 경쾌한 BGM, 예고 글자 아래 17%, AI 카드-자막 닿음, 뉴스·단체 사진 맥락 끊김, 교감 순간이동·탁자 모양) / v1 — 대본 v9 확정, 카메라 계획 v2. 틀: build_ep9_v8.py
# 샌드박스 ~/ep11/{v(vNN 대사·k2NN 반응), img, ov(ep10_ov.py), ed(aNN.wav — prep_ep10.py)}
# 05 = 05~07 묶음 녹음(한 클립), 09 = 09~10 묶음 녹음. 듣는 화면은 VE(말소리 끝) 뒤만.
# 녹음 위치(off.json): 상호상관 대신 말소리 시작 차이(04 0.56, 16 0.18, 17 0.16, 나머지 0~0.04)
import subprocess, os, json, re, shutil
from PIL import ImageFont
H='/home/user'; E=H+'/ep11/'; V=E+'v/'; A=E+'ed/'; IMG=E+'img/'; OV=E+'ov/'; LC=E+'lc/'; X=H+'/ep2/sfx3/'; U=H+'/ed/usfx/'; M=H+'/music/'
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
    z={'ribbon':"1.8+0.002*on",'screen':"1.55+0.002*on",'form':"1.2+0.0015*on",'notif9':"2.0+0.0015*on",'chart':"1.25+0.002*on",'notice':"1.25+0.002*on",'in':"1.05+0.0025*on",'out':"1.25-0.0025*on",'slow':"1.02+0.0008*on",'msg':"1.45+0.002*on",'msgh':"1.45+0.002*on",'yt':"1.35+0.002*on",'meat':"2.1+0.001*on",'stamp':"1.12+0.002*on",'card1':"1.6+0.002*on",'stamp9':"1.8+0.002*on",'phone':"1.22+0.002*on",'memo':"1.7+0.001*on",'notif':"2.3+0.001*on",'stampS':"1.3+0.002*on",'dutyH':"1.5+0.002*on"}[mode]
    cx,cy={'ribbon':(0.76,0.69),'screen':(0.69,0.43),'form':(0.5,0.62),'notif9':(0.668,0.339),'chart':(0.5,0.42),'notice':(0.5,0.42),'meat':(0.25,0.6),'yt':(0.43,0.37),'stamp':(0.49,0.47),'card1':(0.5,0.33),'stamp9':(0.56,0.683),'msgh':(0.59,0.47),'phone':(0.55,0.52),'stampS':(0.5,0.62),'dutyH':(0.6,0.36),'memo':(0.62,0.70),'notif':(0.665,0.376)}.get(mode,(0.5,0.5))
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
SP={**{c:'DV' for c in ['02','03','08','11','15','17','19']},'13':'DJ','01':'N','20':'N'}
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
DH=['04','05','09','12','14','16','18']
GAIN={}
for c in sorted(TJ):
    g=max(-6,min(10,-24.0-lufs(A+f'a{c}.wav'))); GAIN[c]=round(g,1)
    af=f'volume={g:.2f}dB'
    if c in DH: af+=',equalizer=f=170:t=q:w=1.0:g=3,equalizer=f=3000:t=q:w=1.0:g=2.5,acompressor=threshold=0.08:ratio=3:attack=5:release=120:makeup=1.6'
    run(['ffmpeg','-nostdin','-v','error','-y','-i',A+f'a{c}.wav','-af',af,A+f'n{c}.wav'])
print('GAIN',GAIN)
def AW(c): return A+f'n{c}.wav'
run(['ffmpeg','-nostdin','-v','error','-y','-f','lavfi','-i',"aevalsrc='0.45*sin(2*PI*1320*t)*exp(-t*28)':s=44100:d=0.25",A+'blip.wav'])
PING=A+'blip.wav'  # v6: s18은 '빠른 시계 째깍' 소리라 강조음으로 쓰면 똑딱거림(사장님 지적)
run(['ffmpeg','-nostdin','-v','error','-y','-f','lavfi','-i',"aevalsrc='0.5*sin(2*PI*165*t)*sin(2*PI*30*t)*lt(mod(t\\,0.55)\\,0.38)':s=44100:d=1.2",A+'vib.wav'])  # 휴대폰 진동(코드 합성)
VIB=A+'vib.wav'
run(['ffmpeg','-nostdin','-v','error','-y','-i',X+'s23.mp3','-af','asetrate=44100*0.8,aresample=44100,lowpass=f=2500,volume=1.6',A+'thud.wav'])
IN='{\\i1}'
BIG='{\\an5\\pos(360,990)\\fad(80,0)\\fscx130\\fscy130\\bord7\\c&H0000E6FF&}'   # 가운데 큰 노란 자막
RED='{\\an5\\pos(360,640)\\fad(80,0)\\fscx125\\fscy125\\bord7\\c&H3030FF&}'      # 가운데 큰 붉은 자막
def KW(t,w): return (t,t+0.9,'{\\an5\\pos(360,560)\\fscx260\\fscy260\\t(0,140,\\fscx200\\fscy200)\\bord8\\c&H0000E6FF&}'+w,'Ono')

def wsubs(c,parts):
    # parts: [(텍스트('|'로 나눔), 시작 낱말 키 또는 None, 기본 시작)] — 각 덩이는 낱말 시각에서 시작
    st=SP.get(c,'DD'); starts=[]
    for txt,key,dflt in parts: starts.append(v0(c) if key is None else wt(c,key,dflt))
    out=[]
    for i,(txt,key,dflt) in enumerate(parts):
        a=starts[i]; b=(starts[i+1]-0.05) if i+1<len(parts) else v1(c)
        ps=[p.strip() for p in txt.split('|') if p.strip()]; tot=sum(len(vis(p)) for p in ps); t=a
        for p in ps:
            if _fw.getlength(vis(p))>560: WARN.append((c,vis(p)))
            d=(b-a)*len(vis(p))/tot; out.append((t,t+d,p,st)); t+=d
    return out
def speakw(c,plan,parts,tail=0.12,ev=()):
    L=v1(c)+tail; segs=[]; pts=plan+[(L,None)]
    for i in range(len(pts)-1):
        t,what=pts[i][0],pts[i][1]; d=round(pts[i+1][0]-t,3)
        if d<=0.05: continue
        s=seg(c,what,t,d); segs.append(s if s else (img(what,d,pts[i][2] if len(pts[i])>2 else 'in'),0,d))
    add(segs,[(AW(c),0,1.0,'d',None)],wsubs(c,parts),ev)
FX[V+'k201.mp4']=',crop=540:960:90:320,scale=720:1280'   # 벽시계(8시로 그려짐) 화면 밖으로 → 자막 '밤 11시 40분'
FX[V+'k203.mp4']=',crop=432:768:20:60,scale=720:1280'   # v2: 교감이 상석이 아닌 자리로 보임 → 얼굴만
for _c in ('v12','v13','v16','v18'): FX[V+_c+'.mp4']=',crop=576:1024:72:40,scale=720:1280'   # v2: 원탁·사각 탁자 섞임 → 얼굴 쪽으로 당겨 탁자 가림
run(['ffmpeg','-nostdin','-v','error','-y','-f','lavfi','-i',"anoisesrc=d=3.2:c=pink:a=0.9,highpass=f=700,lowpass=f=6000,volume='0.35+0.65*abs(sin(2*PI*t*9.3))*abs(sin(2*PI*t*6.1+1))':eval=frame,afade=t=in:d=0.25,afade=t=out:st=2.4:d=0.8",A+'clap.wav'])  # v2: 박수(코드 합성)
run(['ffmpeg','-nostdin','-v','error','-y','-f','lavfi','-i',"aevalsrc='0.22*sin(2*PI*55*t)*(0.65+0.35*sin(2*PI*0.5*t))+0.12*sin(2*PI*82.4*t)+0.5*sin(2*PI*48*t)*exp(-mod(t\\,1.1)*9)':s=44100:d=16",'-af','lowpass=f=400,afade=t=in:d=1.5',A+'dark.wav'])  # v2: 엔딩 긴장 저음(심장 박동)

# ================= 훅(결말 먼저, 제목만): 파쇄기 → 웃는 교사들 → 굳은 교감 → "교장이 집니다." =================
_e9=max([e for w,s_,e in W('09') if '집니' in w] or [1.2])+0.15  # v2: '집니다'의 '다'까지(낱말 끝 +0.15)
add([(V+'k206.mp4',0.2,0.9),(V+'k209.mp4',0.6,0.9),(V+'k203.mp4',1.2,0.8),(V+'v09.mp4',OFF.get('09',0.0),round(_e9+0.25,2))],
    subs=[(0.1,2.6+_e9,"{\\an5\\pos(360,800)\\fad(150,0)}형식적인 보고서가\\N{\\alpha&HFF&\\t(1500,1510,\\alpha&H00&)\\fscx150\\fscy150\\t(1500,1660,\\fscx100\\fscy100)}"+YN+"없어진다면?",'HookT')],
    au=[(AW('09'),2.6,1.0,'d',('cut',_e9))],ev=[(A+'thud.wav',0.0,0.8,'s',None),(A+'thud.wav',2.6+v0('09'),0.9,'s',None),(U+'shred.mp3',0.0,0.9,'s',('seek',1.5,0.9)),(U+'laugh.mp3',0.9,0.7,'s',('seek',0.5,0.9))])
HIT.append(0.05); HIT.append(2.6+v0('09'))
# ================= ① 다음 날 아침 =================
MK['s1']=T
add([(img('o927h',1.2,'notice'),0,1.2)],ev=[(PING,0.3,0.4,'s',None)])
MK['t01']=T
speak('01',[(0,'v'),(2.8,'o927h','in'),(3.9,'v')],'계약교사가 교장이라니…|서류 실수 아니에요?',tail=0.1)
MK['t02']=T
speak('02',[(0,'v'),(1.7,'o_inbox','in')],'실수예요.|곧 정정 공문 올 겁니다.',tail=0.25,ev=[(PING,2.2,0.4,'s',None)])
# ================= ② 첫 교직원 회의 =================
MK['meet']=T
speak('03',[(0,'v'),(2.4,'clip:k202@0.3'),(3.4,'v')],'아이고, 요즘 심심해서…|회의는 짧게 하시죠.',tail=0.1,ev=[(U+'boing2.mp3',0.1,0.25,'s',None)])
MK['t04']=T
speak('04',[(0,'v'),(2.2,'clip:k202@1.6'),(3.4,'v'),(5.8,'clip:k203@0.3'),(6.9,'v')],'당황스럽긴 하지만,|어차피 계약직 교사라는|설정 자체가|말이 안 되긴 하니…|오늘부터 아무튼,|제가 교장을 맡겠습니다.',tail=0.15)
# ================= ③ 종이: 원인(전날 밤 꾸미기) → 누가 읽습니까 → 책임자 칸 → 파쇄기 =================
MK['night']=T
add([(V+'k201.mp4',0.2,1.9)],ev=[(X+'s26.mp3',0.0,0.45,'s',('cut',1.4))],subs=[(0.15,1.9,BIG+'보고서 표지만\\N세 시간째','Ono')])
MK['t05']=T
speakw('05',[(0,'v'),(2.45,'clip:k205@0.2'),(3.3,'o_resp1','in'),(4.25,'o_resp2','in'),(5.15,'o_resp3','in'),(6.5,'v'),(7.7,'clip:k206@0.2'),(8.7,'clip:k207@0.3')],
    [('이 보고서,|누가 읽습니까?',None,0),('이 종이들, 다|누구 책임인지|적는 칸만 있네요.','종이들',2.7),('없앨 종이는,|선생님들이 고르세요.','없앨',6.9)],tail=0.1,
    ev=[(A+'thud.wav',3.3,0.5,'s',None),(A+'thud.wav',4.25,0.55,'s',None),(A+'thud.wav',5.15,0.6,'s',None),(U+'shred.mp3',7.7,0.8,'s',('seek',1.5,v1('05')+0.1-7.7))])
SUB.append(KW(MK['t05']+wt('05','책임',4.0),'책임')); HIT.append(MK['t05']+wt('05','책임',4.0))
MK['one']=T
add([(img('o_one',1.4,'in'),0,1.4)],ev=[(PING,0.2,0.45,'s',None)],subs=[(0.1,1.4,BIG+'남은 건, 한 장','Ono')])
MK['t08']=T
speak('08',[(0,'v')],'감사 나오면,|누가 책임져요?',tail=0.2)
MK['t09']=T
speakw('09',[(0,'v'),(2.15,'o_safety_b','stampS'),(3.0,'o_duty_a','in'),(3.45,'o_duty_b','in'),(4.3,'clip:k208@0.3')],
    [(POP+'교장이 집니다.',None,0),('학맞통은,|교감 선생님이.','통은',2.33)],tail=0.15,ev=[(A+'thud.wav',2.15,0.8,'s',None),(PING,3.45,0.5,'s',None)])
HIT.append(MK['t09']+v0('09')); HIT.append(MK['t09']+2.15)
MK['t11']=T
speak('11',[(0,'v'),(1.6,'clip:k202@2.4'),(2.5,'v'),(3.45,'clip:v09@%.2f'%(VE['v09']+0.1))],'내가? 아… 아니, 제…|하… 제가요?',tail=0.15,ev=[(U+'boing2.mp3',0.05,0.35,'s',None)])
# ================= ④ 수요일 오후: 사진 보며 소감 → 뉴스 → AI 보고서 → 수업 이야기 =================
MK['wed']=T
add([(V+'k209.mp4',0.2,1.7),(img('o_tv',1.5,'in'),0,1.5),(img('o906p7',1.4,'in'),0,1.4)],ev=[(U+'laugh.mp3',0.0,0.75,'s',('seek',0.5,1.75)),(PING,1.75,0.45,'s',None),(A+'thud.wav',3.25,0.6,'s',None)])  # v2: 단체 사진(k210) 빼고 9화 AI 보고서(초록 고양이) 그림으로
MK['t12']=T
speak('12',[(0,'v'),(2.8,'o906p7','in'),(3.8,'v')],'제 수업이|제일 별로였습니다.|AI가 대신 써도|모를 과제였으니까요.',tail=0.1)
MK['t13']=T
speak('13',[(0,'v'),(3.0,'o_ai','in'),(4.4,'clip:k211@0.3')],'…AI한테 광합성을|설명하게 하고,|틀린 데를 애들이|찾게 하면 어떨까요?',tail=0.15)
MK['t14']=T
speak('14',[(0,'v'),(2.8,'clip:v13@%.2f'%(VE['v13']+0.1)),(3.8,'v')],'선생님이 하고 싶은 수업이|아이들을 키운다면,|그걸 지키는 게|제 일입니다.',tail=0.1)
# ================= ⑤ 결정타 =================
MK['vpin']=T
add([(V+'k216.mp4',0.2,1.3)])  # v2: 교감이 의자 끌고 둥근 자리로(순간이동 막기)
MK['t15']=T
speak('15',[(0,'v')],'이러면 학교가|어떻게 돌아갑니까?',tail=0.1)
speak('16',[(0,'v'),(2.3,'clip:v13@%.2f'%(VE['v13']+0.6)),(3.3,'v')],'돌아갑니다.|지금까지 선생님들이|대신 돌리고 있었을 뿐이죠.',tail=0.1)
speak('17',[(0,'v')],'아이고, 그럼 저는…',tail=0.25,ev=[(U+'boing2.mp3',0.05,0.35,'s',None)])
MK['t18']=T
speak('18',[(0,'v'),(2.3,'clip:v17@%.2f'%(VE['v17']+0.1)),(3.0,'v')],POP+'심심하실 틈|없으실 겁니다.|그 시간에,|'+K('교감 역할')+' 하세요.',tail=0.3)
HIT.append(MK['t18']+v0('18'))
MK['clap']=T
add([(V+'k212.mp4',0.3,1.3),(V+'k213.mp4',0.3,1.2),(V+'v16.mp4',VE['v16']+0.15,0.6)],ev=[(U+'clap_cheer.mp3',0.0,0.85,'s',('seek',1.0,3.1))])  # v2: 2.5초 남짓 + 박수 소리
# ================= ⑦ 저녁: 교감 몰래 전화 → 이사장 =================
MK['s7']=T; MK['song']=T
speak('19',[(0,'v')],'이사장님,|교장이 보고를 다 없앴습니다.',tail=0.15)
MK['ch']=T
add([(V+'k214.mp4',0.3,1.3),(img('o_memo',1.4,'in'),0,1.4)],ev=[(PING,1.5,0.4,'s',None)])
MK['t20']=T
speak('20',[(0,'v')],'…조만간,|한번 들르겠습니다.',tail=0.1)
MK['last_end']=T-0.1
add([(V+'k215.mp4',0.5,1.0),(V+'k204.mp4',0.5,1.0)],ev=[(X+'s19.mp3',0.0,0.45,'s',None)])
MK['fin']=T
add([(V+'v16.mp4',VE['v16']+0.15,1.4)])
total=T
CAPL='{\\an7\\pos(40,86)\\fs34}'
SUB+=[(MK['s1']+0.05,MK['t02']-0.05,CAPL+'다음 날 아침 · 교무실','Cap'),
      (MK['t01']+0.1,MK['t01']+1.9,'동료 교사','Tag'),
      (MK['t02']+0.1,MK['t02']+1.7,'교감','Tag'),
      (MK['meet']+0.05,MK['meet']+2.4,CAPL+'오전 8시 · 첫 교직원 회의','Cap'),
      (MK['t04']+0.1,MK['t04']+2.2,'독고다해 · 새 교장','Tag'),
      (MK['night']+0.05,MK['night']+1.85,CAPL+'전날 밤 11시 40분','Cap'),
      (MK['wed']+0.05,MK['wed']+1.65,CAPL+'수요일 오후 · 수업 이야기 시간','Cap'),
      (MK['wed']+1.75,MK['wed']+3.15,CAPL+'그때 · 교무실 TV','Cap'),
      (MK['wed']+3.25,MK['t12']+3.8,CAPL+'지난주 · AI가 대신 쓴 보고서','Cap'),
      (MK['t13']+0.1,MK['t13']+1.9,'안정우 · 통합과학 교사','Tag'),
      (MK['s7']+0.05,MK['s7']+2.0,CAPL+'그날 저녁 · 복도','Cap'),
      (MK['ch']+0.05,MK['ch']+2.6,CAPL+'같은 시각 · 이사장실','Cap'),
      (MK['fin']+0.05,MK['fin']+1.5,'{\\pos(360,780)\\fad(150,0)\\fscx120\\fscy120}이사장이 온다','Ono'),
      (MK['fin']+0.3,MK['fin']+1.5,'{\\pos(360,900)\\fnNanumGothic\\b1\\fs28\\fsp3\\bord3\\c&H0078E0FF&}교사X 11화 · 12월 11일(금) 저녁 6시','Ono')]
EV.append((X+'B1.mp3',MK['s1'],0.35,'s',('cut',MK['t08']+v1('08')+0.05-MK['s1'])))  # v2: '교장이 집니다' 앞 음악 뚝(정적 드롭)
EV.append((X+'B1.mp3',MK['t09']+2.15,0.35,'s',('seek',30.0,MK['wed']-MK['t09']-2.15)))
EV.append((A+'thud.wav',MK['t09']+v0('09'),1.0,'s',None))
EV.append((X+'B2.mp3',MK['wed'],0.4,'s',('seek',0.0,MK['t18']-MK['wed'])))  # 결정타(18)에서 음악 끊음 → 정적
EV.append((A+'dark.wav',MK['song'],0.5,'s',('end',total-MK['song'])))  # v2: 경쾌한 노래 → 긴장 저음

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
outn=E+'ed/ep10_v3.mp4'
run(['ffmpeg','-nostdin','-v','error','-y','-i',E+'ed/pic.mp4','-i',E+'ed/aud.m4a','-vf',f"setpts=N/(24*TB),{flash},{shake},ass={E}ed/sub.ass:fontsdir={H}/fonts,fade=t=out:st={total-0.6:.2f}:d=0.6",'-c:v','libx264','-preset','veryfast','-crf','20','-c:a','copy','-shortest',outn])
print('ok',outn)
_lw=MK['last_end']
_cuts=subprocess.run(['ffmpeg','-i',outn,'-vf',"select='gt(scene,0.2)',showinfo",'-an','-f','null','-'],capture_output=True,text=True).stderr.count('pts_time:')
print(f"""[편집장 측정값]
전체 길이: {total:.1f}초 / 컷 수: {_cuts} / 평균 컷 길이: {total/max(1,_cuts+1):.1f}초
마지막 대사 끝: {_lw:.1f}초 / 그 뒤 말 없는 구간: {total-_lw:.1f}초
훅: 파쇄기 0.9 → 웃는 교사들 0.9 → 굳은 교감 0.8 → '교장이 집니다' (대사 자막 없음, 제목만)
자막 겹침: {len(OVL)}건""")
