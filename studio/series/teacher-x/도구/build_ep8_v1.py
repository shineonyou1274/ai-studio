# 교사X 8화(폐강) 편집 v1 — 틀: build_ep7_v15.py(글자 그림 타임라인·측정값 출력 그대로). 대본 v2 확정(사장님 11/19), 카메라 계획 v1.
# 샌드박스 ~/ep9/{v(vNN·rNNN), img, ov(ep8_ov.py), ed(aNN.wav: 61=06b 정우 속마음, 91=09b 교감 혼잣말, 11·12=테이크2), lc, timing.json, off.json}
# 녹음 위치(off.json): 03 0.96(입이 늦게 열림) 나머지 0~0.12. 12는 입이 일찍 닫혀 3.0초부터 교감 말문 막힘(v13)으로 덮음.
# 원칙(사장님 11/19): 메인 = 학교의 부적절한 관행, 후반 = 사이다. 교장 줄기는 혼잣말 한 줄 + 끝 폰 알림만.
import subprocess, os, json, re, shutil
from PIL import ImageFont
H='/home/user'; E=H+'/ep9/'; V=E+'v/'; A=E+'ed/'; IMG=E+'img/'; OV=E+'ov/'; LC=E+'lc/'; X=H+'/ep2/sfx3/'; U=H+'/ed/usfx/'; M=H+'/music/'
os.makedirs(LC,exist_ok=True)
for s,d in [(H+'/ep7/ov/o608a.png',OV),(H+'/ep7/ov/o608b.png',OV)]:
    if not os.path.exists(d+os.path.basename(s)): shutil.copy(s,d)
TJ=json.load(open(E+'timing.json'))
OFF=json.load(open(E+'off.json'))  # 클립 소리와 원래 녹음을 맞춰 잼 + 입 모양 프레임 확인(17 1.46, 18 1.65, 08 0.6)
SPD={}
VID={'61':'v06','91':'v09b'}  # 09b 클립 이름
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
    z={'in':"1.05+0.0025*on",'out':"1.25-0.0025*on",'slow':"1.02+0.0008*on",'msg':"1.45+0.002*on",'msgh':"1.45+0.002*on",'yt':"1.35+0.002*on",'meat':"2.1+0.001*on",'stamp':"1.12+0.002*on",'phone':"1.22+0.002*on"}[mode]
    cx,cy={'meat':(0.25,0.6),'yt':(0.43,0.37),'stamp':(0.49,0.47),'msgh':(0.59,0.47),'phone':(0.55,0.52)}.get(mode,(0.5,0.5))
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
SP={**{c:'DV' for c in ['01','02','03','05','07','09','91','13']},**{c:'DJ' for c in ['04','06','61']}}
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
DH=['08','10','11','12']
for c in DH:
    run(['ffmpeg','-nostdin','-v','error','-y','-i',A+f'a{c}.wav','-af','equalizer=f=170:t=q:w=1.0:g=3,equalizer=f=3000:t=q:w=1.0:g=2.5,acompressor=threshold=0.08:ratio=3:attack=5:release=120:makeup=1.6',A+f'e{c}.wav'])
run(['ffmpeg','-nostdin','-v','error','-y','-i',A+'a03.wav','-af','volume=3.5dB',A+'a03q.wav'])  # 낮은 목소리 협박(-29.4 LUFS) → 다른 교감 줄 쪽으로
run(['ffmpeg','-nostdin','-v','error','-y','-i',A+'a61.wav','-af','volume=4dB,aecho=0.6:0.5:40:0.25',A+'a61q.wav'])  # 정우 속마음: 키우고 살짝 울림
def AW(c): return A+('a03q.wav' if c=='03' else 'a61q.wav' if c=='61' else f'e{c}.wav' if c in DH else f'a{c}.wav')
PING=X+'s18.mp3'
run(['ffmpeg','-nostdin','-v','error','-y','-i',X+'s23.mp3','-af','asetrate=44100*0.8,aresample=44100,lowpass=f=2500,volume=1.6',A+'thud.wav'])
IN='{\\i1}'
# ================= ① 훅(결말 먼저): 교감 씩 웃음 → 밤 책상 → 세특 312명 → 결말 플래시(교감 말문 막힘). 제목만 =================
add([(V+'v09.mp4',6.3,0.8),(V+'r842.mp4',0.3,1.3),(img('o844',1.0,'in'),0,1.0),(V+'v13.mp4',2.4,0.5)],
    subs=[(0.1,3.55,"{\\an5\\pos(360,800)\\fad(150,0)}한 학기에\\N{\\alpha&HFF&\\t(1500,1510,\\alpha&H00&)\\fscx150\\fscy150\\t(1500,1660,\\fscx100\\fscy100)}"+YN+"과목 4개?",'HookT')],
    ev=[(A+'thud.wav',2.1,0.9,'s',None),(PING,3.1,0.5,'s',None)],au=[(A+'a09.wav',0.25,1.0,'d',('seek',0.0,1.75))])
HIT.append(3.1)
# ================= ② 교육과정 회의 =================
MK['s1']=T
add([(V+'r831.mp4',0.4,1.4)])
MK['t01']=T
speak('01',[(0,'v'),(1.2,'o841'),(2.6,'v')],'신청 3명.|이건 '+K('폐강')+'이에요.',tail=0.15,ev=[(PING,1.25,0.5,'s',None)])
speak('02',[(0,'v'),(2.7,'clip:r832@0.3'),(3.9,'v')],'안 선생, 이 과목 없어지면|시수가 모자라죠.|자리도 없는 거 알죠?',tail=0.1)
speak('03',[(0,'v')],'그럼 중학교나…|변두리 재단 학교로 가야지.',tail=0.15)
MK['t04']=T
speak('04',[(0,'v')],'…네?',tail=0.5)
speak('05',[(0,'v'),(3.1,'clip:r832@1.6'),(4.4,'v')],'싫으면 애들이 좋아할|과목을 새로 열어요.|유전, 과학 실험…|대학이 그런 거 좋아해.',tail=0.1)
speak('06',[(0,'v')],'그럼 한 학기에|'+K('네 과목')+'인데요…',tail=0.3)
MK['b1_end']=T
# ================= ③ 정우의 한 학기(몽타주) + 속마음 =================
MK['night']=T
add([(V+'r843.mp4',0.2,1.5),(img('o844',1.6,'in'),0,1.6),(V+'r845.mp4',0.3,1.9)],
    au=[(AW('61'),0.35,1.0,'d',None)],
    subs=[(0.35,0.35+2.4,IN+'(속마음) 신규 1년 차 땐…','DJ'),(0.35+2.4,0.35+4.6,IN+'한 과목 준비도 죽을 것 같았는데.','DJ')])
# ================= ④ 다해에게도 =================
MK['t07']=T
speak('07',[(0,'v')],'독고 선생은 '+K('지리 부전공')+'이죠?|지리도 하나 열어요.',tail=0.1)
MK['dh']=T
speak('08',[(0,'v')],'제 시수는 이미|평균보다 많습니다.|신청 학생도 많고요.',tail=0.15)
speak('09',[(0,'v'),(3.0,'clip:r834@0.5'),(4.2,'v')],'학생한테 좋은 거잖아.|선택 과목 많은 학교,|대학이 좋아해요.',tail=0.1)
speak('91',[(0,'v')],IN+'개설 과목 수 1등 학교…|'+IN+'이 정도 실적이면,|'+IN+'교장 공모 때 승진은|'+IN+'유력하겠지.',tail=0.15)
MK['b2_end']=T
# ================= ⑤ 반전: 숫자 =================
speak('10',[(0,'v')],'과목은 늘고,|교사는 그대로네요.',tail=0.1)
MK['memo']=T
add([(img('o846',2.0,'slow'),0,2.0)],ev=[(PING,0.1,0.4,'s',None)])
HIT.append(MK['memo']+0.1)
# ================= ⑥ 사이다 =================
speak('11',[(0,'v'),(2.4,'clip:r833@0.2'),(3.3,'v')],'이렇게 되면|수업의 질이 떨어지고,|결국 손해는 '+K('학생')+'이 집니다.',tail=0.15)
MK['t12']=T
speak('12',[(0,'v'),(3.0,'clip:v13@2.4')],POP+'교사를 학생에게|보내 주는 것.|그게 '+K('교감 선생님 업무')+'죠.',tail=0.25)
HIT.append(MK['t12']+v0('12'))
speak('13',[(0,'v')],'그, 그건…',tail=0.3,ev=[(U+'boing2.mp3',0.05,0.4,'s',None)])
MK['last_end']=T-0.3
# ================= ⑦ 클리프행어(4.9초 안): 교사들 → 시계 4:50 → 교감 폰 '차기 교장 공모' → 다해 얼굴 =================
MK['s7']=T; MK['song']=T
add([(V+'r834.mp4',1.8,0.9),(img('o608a',0.4,'in'),0,0.4),(img('o608b',0.5,'in'),0,0.5)],ev=[(PING,0.9,0.4,'s',None)])
MK['phone']=T
add([(img('o847',1.0,'phone'),0,1.0)],ev=[(X+'s19.mp3',0.0,0.5,'s',None)])
MK['fin']=T
_fin=img('o838f',2.0,'slow'); FX[_fin]=',drawbox=y=ih*0.62:w=iw:h=ih*0.38:c=black@0.22:t=fill,drawbox=y=ih*0.72:w=iw:h=ih*0.28:c=black@0.22:t=fill,drawbox=y=ih*0.82:w=iw:h=ih*0.18:c=black@0.22:t=fill'
add([(_fin,0,2.0)])
total=T
CAPL='{\\an7\\pos(40,86)\\fs34}'
SUB+=[(MK['s1']+0.1,MK['s1']+1.9,CAPL+'오후 3시 30분 · 내년 교육과정 회의','Cap'),
      (MK['t01']+0.3,MK['t01']+2.0,'교감','Tag'),
      (MK['t04']+0.05,MK['t04']+1.4,'안정우 · 통합과학 교사','Tag'),
      (MK['night']+0.05,MK['night']+1.5,CAPL+'밤 10시','Cap'),
      (MK['night']+1.55,MK['night']+3.1,CAPL+'세특 = 학생마다 쓰는 과목 기록','Cap'),
      (MK['dh']+0.05,MK['dh']+1.9,'{\\fs40}독고다해 · 국어 계약교사\\N{\\fs24}(부전공 지리 · 극 중 설정)','Tag'),
      (MK['s7']+0.95,MK['s7']+1.8,CAPL+'오후 4시 50분','Cap'),
      (MK['fin']+0.1,MK['fin']+2.0,'{\\pos(360,880)\\fad(150,0)\\fscx120\\fscy120}과목은 늘고,\\N교사는 그대로','Ono'),
      (MK['fin']+0.4,MK['fin']+2.0,'{\\pos(360,1050)\\fnNanumGothic\\b1\\fs28\\fsp3\\bord3\\c&H0078E0FF&}교사X 9화 · 12월 7일(월) 저녁 6시','Ono')]
EV.append((X+'B1.mp3',MK['s1'],0.35,'s',('cut',MK['b1_end']-MK['s1'])))
EV.append((X+'B2.mp3',MK['t07'],0.4,'s',('seek',0.0,MK['memo']-MK['t07'])))  # 만년필 메모에서 음악 끊음 → 결정타는 정적
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
outn=E+'ed/ep8_v1.mp4'
run(['ffmpeg','-nostdin','-v','error','-y','-i',E+'ed/pic.mp4','-i',E+'ed/aud.m4a','-vf',f"setpts=N/(24*TB),{flash},{shake},ass={E}ed/sub.ass:fontsdir={H}/fonts,fade=t=out:st={total-0.6:.2f}:d=0.6",'-c:v','libx264','-preset','veryfast','-crf','20','-c:a','copy','-shortest',outn])
print('ok',outn)
_lw=MK['last_end']
_cuts=subprocess.run(['ffmpeg','-i',outn,'-vf',"select='gt(scene,0.2)',showinfo",'-an','-f','null','-'],capture_output=True,text=True).stderr.count('pts_time:')
print(f"""[편집장 측정값]
전체 길이: {total:.1f}초 / 컷 수: {_cuts} / 평균 컷 길이: {total/max(1,_cuts+1):.1f}초
마지막 대사 끝: {_lw:.1f}초 / 그 뒤 말 없는 구간: {total-_lw:.1f}초
훅: 교감 웃음 0.8 → 밤 책상 1.3 → 세특 312명 1.0 → 결말 플래시 0.5초(대사 자막 없음, 제목만)
자막 겹침: {len(OVL)}건""")
