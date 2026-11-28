# 교사X 11화 편집 v9 (사장님 11/28: 교감 민원 응대는 '네?'만, 끝 뉴스 화면이 뉴스 같지 않음 → 신문 1면으로) / v8 (Gemini v7 검수: 한 화면 4초 넘는 대사 컷은 가운데서 12% 당겨 둘로 나눔(펀치 인). 립싱크 누락 지적은 프레임으로 확인해 보니 입 움직임 있음 → 안 고침. 시계 손목은 사장님 결정(10화 '그대로 둬'), '임용고시'는 사장님(작가) 결정으로 유지) / v7 (Gemini v6 검수: 통화 중 '같은 시각 교실의 다해' 컷 끼워 다해 첫 등장 앞당김·통화 컷 2초대로, 훅 다해 컷을 23 숙여 말하는 끝(입 다묾)으로, 29 '화장실뿐' 타격음+배경음 0.3초 끊기, 창밖 오후빛이라 '2교시' → '5교시') / v6 (사장님 11/28: 13 '아까 그거 다시 설명해 주세요'는 설명 거절로 오해 → '선생님, 지금 뭐라고 하셨어요?', 다해 답 '그건 복습.' → '그건 집중력.'(사장님: '놓친 거'보다 집중력 문제)) / v5 (사장님 11/28: 03·04 빼고 08·10 살림 / 준호 19·21 목소리 차이 → 음높이 가운데로 맞춤(19 낮추고 21 올림, 길이 그대로라 입 그대로)) / v4 (Gemini v3 검수: 동료 교사 손 뒤집힘 → 그림·02 다시, 통화 중 교감 입 → 어머니 대사 영상(1.3배)과 교차, 학생 질문 ↔ 다해 '그건 허락/확인/복습' 핑퐁, 21 대사 사이 빈 2초 잘라 냄(소리·입 같이), 다해가 앉은 20 → 선 자세로 다시, 31 기자 컷 재사용 → 이사장 반응, 웅웅 배경 저음 빼고 칙칙 효과음 낮춤, 웅성 세 줄 좌우로 벌림, 先生 위치, 요약 바 위로) / v3 (Gemini v2 검수, 06_검수/v2_gemini_판정_v3.md: 통화 중 이사장 복도 컷 빼기, 인터뷰 역샷·복도 다해 그림 다시(31·26), 출석·준호·23 화면 잘라 공간 오류 숨김, 학생 3컷 구도 바꿈, 요약 바·先生 위치, 22·31 타격음+배경음 끊기, 훅에 다해 눈빛, 꼬리 4.5초 안) / v2 (사장님 11/27 '이사장 얼굴이 다르고 스타일도 바뀐 것 같다': 이사장 그림·영상 6개 다시(수염·갈색 정장은 편집장이 지어낸 묘사 → 시트대로), 화면 색을 10화처럼 덜 노랗고 덜 진하게, 말 없는 끝 5초 안) / v1 — 대본 v2(사장님 11/27 "괜찮아 시작해 가자. 묻지말고 주욱 뽑아"). 틀: build_ep10_v6.py
# 샌드박스 ~/ep12/{v(vNN 대사 = minimax, kNNN 반응 = kling), img(NNN.png), au(aNN 녹음), ed}
# 소리는 모두 코드 합성(종·전화벨·문·초침·휙·쿵·배경 저음). 외부 음원 없음.
import subprocess, os, json, re, glob
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
H='/home/user'; E=H+'/ep12/'; V=E+'v/'; AU=E+'au/'; A=E+'ed/'; IMG=E+'img/'; OV=E+'ov/'; LC=E+'lc/'; F=H+'/fonts/'
for d in (A,OV,LC): os.makedirs(d,exist_ok=True)
def run(c): subprocess.run(c,check=True)
# ---------- 1) 녹음 정리 ----------
SRC={'01':'a01.wav','02':'a02.wav','03':'a03.wav','04':'a04.wav','05':'a05.wav','06':'a061.mp3','07':'a07.wav','08':'a08.mp3','09':'a09.wav','10':'a10.mp3',
 '11':'a11.wav','12':'a12.wav','13':'a131.wav','141':'a143.mp3','14':'a14.mp3','16':'a16.mp3','171':'a171.wav','172':'a172.wav','173':'a173.wav','18':'a18.mp3','19':'a19.wav','20':'a20.mp3',
 '21':'a21c.wav','22':'a22.mp3','23':'a23.mp3','26':'a26.mp3','27':'a27.wav','28':'a28.mp3','29':'a29.mp3','30':'a30.wav','31':'a31.mp3'}
SPEED={'05':1.3}
PITCH={'19':0.95,'21':1.055}   # v5: 준호 음높이(중앙값 19=129Hz, 21=115Hz) 가운데로   # 어머니 전화: 음높이 유지 1.3배(입 없는 화면이라 길이만 줄임)
for c,s in SRC.items():
    af='aresample=44100' + (f',atempo={SPEED[c]}' if c in SPEED else '') + (f',asetrate=44100*{PITCH[c]},aresample=44100,atempo={1/PITCH[c]:.5f}' if c in PITCH else '')
    run(['ffmpeg','-nostdin','-v','error','-y','-i',AU+s,'-ac','1','-af',af,A+f'a{c}.wav'])
TJF=E+'timing.json'
if os.path.exists(TJF): TJ=json.load(open(TJF))
else: TJ={}
need=[c for c in SRC if c not in TJ]
if need:
    from faster_whisper import WhisperModel
    import wave
    m=WhisperModel('small',compute_type='int8')
    for c in need:
        f=A+f'a{c}.wav'; w=wave.open(f); a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float); sr=w.getframerate()
        h=int(sr*0.02); r=np.array([np.sqrt((a[i*h:(i+1)*h]**2).mean()) for i in range(len(a)//h)]); v=np.where(r>max(r.max()*0.05,150))[0]
        segs,_=m.transcribe(f,language='ko',word_timestamps=True)
        TJ[c]={'dur':round(len(a)/sr,2),'v0':round(v[0]*0.02,2),'v1':round((v[-1]+1)*0.02,2),'words':[(x.word.strip(),round(x.start,2),round(x.end,2)) for s in segs for x in s.words]}
    json.dump(TJ,open(TJF,'w'),ensure_ascii=False)
def env(p):
    b=subprocess.check_output(['ffmpeg','-nostdin','-v','error','-i',p,'-ac','1','-ar','16000','-f','s16le','-']); a=np.frombuffer(b,np.int16).astype(float)
    h=320; return np.array([np.sqrt((a[i*h:(i+1)*h]**2).mean()) for i in range(len(a)//h)])
OFF,VE={},{}
for p in sorted(glob.glob(V+'v[0-9][0-9].mp4')):
    c=os.path.basename(p)[1:3]
    try: r=env(p)
    except subprocess.CalledProcessError: continue
    if len(r)==0 or r.max()<50: continue
    v=np.where(r>max(r.max()*0.08,100))[0]; VE['v'+c]=round((v[-1]+1)*0.02,2)
    if c in TJ: OFF[c]=max(0.0,round(v[0]*0.02-TJ[c]['v0'],2))
print('OFF',OFF); print('VE',VE)
def v1(c): return TJ[c]['v1']
def v0(c): return TJ[c]['v0']
def W(c): return TJ[c]['words']
def wt(c,key,default,last=False):
    hits=[s for w,s,e in W(c) if key in w]
    return (hits[-1] if last else hits[0]) if hits else default
# ---------- 2) 소리 합성 ----------
def syn(name,expr,d,af=None):
    c=['ffmpeg','-nostdin','-v','error','-y','-f','lavfi','-i',f"aevalsrc='{expr}':s=44100:d={d}"]
    if af: c+=['-af',af]
    run(c+[A+name])
syn('impact.wav','0.95*sin(2*PI*(70-40*t)*t)*exp(-t*4)+0.5*sin(2*PI*140*t)*exp(-t*12)',1.0,'lowpass=f=900,volume=1.3')   # v3: 결정타 타격음
syn('tak.wav','0.9*sin(2*PI*900*t)*exp(-t*60)+0.6*sin(2*PI*180*t)*exp(-t*30)',0.15)   # v4: 핑퐁 탁
syn('heart.wav','0.9*sin(2*PI*50*t)*(exp(-t*14)+exp(-(t-0.28)*14)*gt(t\\,0.28))',0.8,'lowpass=f=200')   # v4: 훅 심장
syn('ping.wav','0.45*sin(2*PI*1320*t)*exp(-t*28)',0.25)
syn('thud.wav','0.9*sin(2*PI*55*t)*exp(-t*9)+0.3*sin(2*PI*110*t)*exp(-t*14)',0.6,'lowpass=f=300')
# 학교 종(딩-동-댕-동): 네 음
syn('bell.wav',"0.35*(sin(2*PI*659*t)*exp(-t*2.2)*lt(t\\,0.9)+sin(2*PI*523*(t-0.8))*exp(-(t-0.8)*2.2)*gt(t\\,0.8)*lt(t\\,1.7)+sin(2*PI*587*(t-1.6))*exp(-(t-1.6)*2.2)*gt(t\\,1.6)*lt(t\\,2.5)+sin(2*PI*392*(t-2.4))*exp(-(t-2.4)*1.6)*gt(t\\,2.4))",3.6,'aecho=0.8:0.6:60:0.25')
# 사무실 전화벨 두 번
syn('ring.wav',"0.3*sin(2*PI*480*t)*sin(2*PI*20*t)*lt(mod(t\\,1.4)\\,0.6)",1.9,'highpass=f=300')
# 초침 째깍
syn('tick.wav',"0.5*sin(2*PI*2500*t)*exp(-mod(t\\,0.25)*120)",1.4,'highpass=f=1200')
# 휙
run(['ffmpeg','-nostdin','-v','error','-y','-f','lavfi','-i',"anoisesrc=d=0.45:c=pink:a=0.8,highpass=f=300,lowpass=f=1800,volume='0.6*sin(PI*t/0.45)':eval=frame",A+'whoosh.wav'])
# 미닫이문 드르륵
run(['ffmpeg','-nostdin','-v','error','-y','-f','lavfi','-i',"anoisesrc=d=0.8:c=brown:a=0.9,bandpass=f=900:w=600,volume='0.6*abs(sin(2*PI*t*18))*(1-t/0.8)':eval=frame",A+'door.wav'])
# 수첩 사각사각
run(['ffmpeg','-nostdin','-v','error','-y','-f','lavfi','-i',"anoisesrc=d=1.2:c=white:a=0.5,highpass=f=3000,volume='0.5*gt(sin(2*PI*t*7)\\,0.2)':eval=frame",A+'scribble.wav'])
# 배경: 가벼운 수업 배경(낮은 현+맥박), 긴장 저음
syn('bedA.wav',"0.10*sin(2*PI*220*t)*(0.6+0.4*sin(2*PI*0.25*t))+0.07*sin(2*PI*277*t)+0.05*sin(2*PI*330*t)*(0.5+0.5*sin(2*PI*0.5*t))",40,'highpass=f=150,lowpass=f=1500,volume=0.7,afade=t=in:d=1.0')   # v4: 65Hz 맥박(웅웅) 뺌
syn('dark.wav',"0.22*sin(2*PI*55*t)*(0.65+0.35*sin(2*PI*0.5*t))+0.12*sin(2*PI*82.4*t)+0.5*sin(2*PI*48*t)*exp(-mod(t\\,1.1)*9)",40,'lowpass=f=400,afade=t=in:d=1.5')
syn('warm.wav',"0.09*sin(2*PI*261.6*t)+0.07*sin(2*PI*329.6*t)*(0.6+0.4*sin(2*PI*0.3*t))+0.06*sin(2*PI*392*t)+0.04*sin(2*PI*523.2*t)*(0.5+0.5*sin(2*PI*0.2*t))",20,'lowpass=f=2000,afade=t=in:d=0.8')
# 어머니 전화 목소리: 전화 대역
run(['ffmpeg','-nostdin','-v','error','-y','-i',A+'a05.wav','-af','highpass=f=350,lowpass=f=3200,acompressor=threshold=0.1:ratio=4,volume=1.4',A+'a05p.wav'])
# 웅성: 세 줄 겹치기
run(['ffmpeg','-nostdin','-v','error','-y','-i',A+'a171.wav','-i',A+'a172.wav','-i',A+'a173.wav','-filter_complex','[0]pan=stereo|c0=0.9*c0|c1=0.35*c0,volume=0.9[a];[1]adelay=900|900,pan=stereo|c0=0.35*c0|c1=0.9*c0,volume=0.75[b];[2]adelay=1900|1900,pan=stereo|c0=0.6*c0|c1=0.6*c0,volume=0.65[c];[a][b][c]amix=inputs=3:normalize=0',A+'murmur.wav'])
# ---------- 3) 글자 그림(뉴스) ----------
def news():   # v9: 신문 1면(다음 날 아침)
    W_,H_=1440,2560; P_=(244,240,230); INK=(25,25,25)
    im=Image.new('RGB',(W_,H_),(40,38,36)); pw,ph=1240,1900; x0,y0=100,330
    paper=Image.new('RGB',(pw,ph),P_); d=ImageDraw.Draw(paper)
    MJ=ImageFont.truetype(F+'NanumMyeongjoBold.ttf',150); BH=ImageFont.truetype(F+'BlackHanSans.ttf',118); NG=ImageFont.truetype(F+'NanumGothicBold.ttf',46); NS=ImageFont.truetype(F+'NanumGothic.ttf',34)
    d.text((pw//2,120),'한입일보',font=MJ,fill=INK,anchor='mm')
    d.line([60,215,pw-60,215],fill=INK,width=6); d.line([60,268,pw-60,268],fill=INK,width=2)
    d.text((70,242),'제1면',font=NS,fill=INK,anchor='lm'); d.text((pw-70,242),'교육',font=NS,fill=INK,anchor='rm')
    d.text((pw//2,370),'가르칠 것을',font=BH,fill=INK,anchor='mm'); d.text((pw//2,500),'가르치는 교실',font=BH,fill=INK,anchor='mm')
    d.text((pw//2,610),'선생: 먼저 살아 본 사람의 진짜 가르침이 시작됐다',font=NG,fill=(60,60,60),anchor='mm')
    ph_=Image.open(IMG+'3131.png').convert('L').resize((640,1138)).crop((0,180,640,780))
    ph_=ph_.point(lambda v:int(v*0.9+20)).convert('RGB'); paper.paste(ph_,(60,680))
    d.rectangle([60,680,700,1280],outline=INK,width=3); d.text((60,1300),'수업 중인 교장(사진=한입일보)',font=NS,fill=(70,70,70))
    for k in range(16):   # 본문 줄(글자 대신 회색 줄)
        y=700+k*36; d.line([740,y,pw-60,y],fill=(150,150,150),width=12)
    for col in range(3):
        for k in range(12):
            y=1380+k*36; xa=60+col*380; d.line([xa,y,xa+340,y],fill=(160,160,160),width=12)
    paper=paper.rotate(-2.5,expand=True,fillcolor=(40,38,36))
    im.paste(paper,(x0-20,y0-20)); im.save(OV+'o_news.png')
news()
# ---------- 4) 편집 틀 ----------
cache={}
def img(name,d,mode='in'):
    key=(name,round(d,2),mode)
    if key in cache: return cache[key]
    src=OV+name+'.png' if os.path.exists(OV+name+'.png') else IMG+name+'.png'
    out=LC+f"{name}_{mode}_{int(d*100)}.mp4"; n=int(round(d*24))
    z={'in':"1.05+0.0025*on",'out':"1.25-0.0025*on",'slow':"1.02+0.0008*on",'news':"1.0+0.0012*on",'face':"1.45+0.003*on"}[mode]
    cy=0.36 if mode=='face' else 0.5
    vf=f"scale=1440:2560,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih*{cy}-(ih/zoom/2)':d={n}:s=720x1280:fps=24,format=yuv420p"
    run(['ffmpeg','-nostdin','-v','error','-y','-loop','1','-i',src,'-vf',vf,'-t',str(d),'-c:v','libx264','-preset','veryfast','-crf','19',out])
    cache[key]=out; return out
P=[]; EV=[]; SUB=[]; HIT=[]; WARN=[]; T=0.0; MK={}
def add(segs,au=(),subs=(),ev=()):
    global T
    for f,o,v,k,tr in list(au)+list(ev): EV.append((f,T+o,v,k,tr))
    for s in segs: P.append(s)
    for a,b,txt,st in subs:
        SUB.append((T+a,T+b,txt,st))
    T+=sum(s[2] for s in segs)
SP={**{c:'DV' for c in ['06','08','10','28']},**{c:'N' for c in ['01','02','03','04','05','07','09','11','12','13','19','21','27','30']}}
Y='{\\c&H0078E0FF&\\fscx120\\fscy120}'
def K(w): return Y+w+'{\\r}'
POP='{\\fscx170\\fscy170\\t(0,150,\\fscx100\\fscy100)}'
BIGP='{\\an5\\pos(360,990)\\fscx190\\fscy190\\t(0,160,\\fscx130\\fscy130)\\bord7\\c&H0000E6FF&}'
_fw=ImageFont.truetype(F+'NanumGothicBold.ttf',40)
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
    if what=='v': return (V+f'v{c}.mp4',t+OFF.get(c,0.0),d)
    if what.startswith('clip:'):
        nm=what[5:]; o=0.3
        if '@' in nm: nm,o=nm.split('@'); o=float(o)
        if nm in VE and o < VE[nm]-0.05: raise SystemExit(f'듣는 화면 {nm}@{o}: 이 클립은 {VE[nm]}초까지 입이 움직임')
        return (V+nm+'.mp4',o,d)
    return None
def AW(c): return A+f'n{c}.wav'
def speak(c,plan,text,tail=0.12,ev=(),lead=0.0):
    L=v1(c)+tail; segs=[]; pts=plan+[(L,None)]
    for i in range(len(pts)-1):
        t,what=pts[i][0],pts[i][1]; d=round(pts[i+1][0]-t,3)
        if d<=0.05: continue
        s=seg(c,what,t,d)
        if s and what=='v' and d>3.6:   # v8: 4초 넘는 한 화면 → 둘로, 뒤쪽 12% 펀치 인
            pf=V+f'v{c}p.mp4'
            if not os.path.exists(pf): os.symlink(V+f'v{c}.mp4',pf)
            FX[pf]=FX.get(s[0],'')+',crop=643:1143:38:40,scale=720:1280'
            h=round(d/2,3); segs+= [(s[0],s[1],h),(pf,s[1]+h,round(d-h,3))]; continue
        segs.append(s if s else (img(what,d,pts[i][2] if len(pts[i])>2 else 'in'),0,d))
    add(segs,[(AW(c),0,1.0,'d',None)],chunks(text,c),ev)
def ve(n,plus=0.1): return 'clip:%s@%.2f'%(n,VE[n]+plus)
def lufs(p):
    m=subprocess.run(['ffmpeg','-nostdin','-i',p,'-af','ebur128','-f','null','-'],capture_output=True,text=True).stderr
    return float(re.findall(r'I:\s+(-?[0-9.]+) LUFS',m)[-1])
DH=['14','141','16','18','20','22','23','26','29','31']
for c in TJ:
    src=A+('a05p.wav' if c=='05' else f'a{c}.wav')
    g=max(-6,min(10,-24.0-lufs(src))); af=f'highpass=f=90,volume={g:.2f}dB'
    if c in DH: af+=',equalizer=f=3000:t=q:w=1.0:g=2.5,acompressor=threshold=0.08:ratio=3:attack=5:release=120:makeup=1.6'
    run(['ffmpeg','-nostdin','-v','error','-y','-i',src,'-af',af,A+f'n{c}.wav'])
FX={}
for _n,_c in (('v14a','crop=686:1219:17:30'),('v14b','crop=643:1143:38:60'),('v141c','crop=600:1067:60:90')):
    if not os.path.exists(V+_n+'.mp4'): os.symlink(V+('v141.mp4' if _n=='v141c' else 'v14.mp4'),V+_n+'.mp4')
    FX[V+_n+'.mp4']=','+_c+',scale=720:1280'   # v4: 핑퐁 105·112·120%
FX[V+'v12.mp4']=',hflip'   # v3: 학생 3컷 같은 구도 → 둘째 좌우 뒤집기
FX[V+'v13.mp4']=',crop=504:896:108:110,scale=720:1280'   # 셋째 얼굴 쪽
FX[V+'v16.mp4']=',crop=336:597:200:200,scale=720:1280'   # v3: 출석 컷 뒤 학생들 숨김
FX[V+'v21.mp4']=',crop=540:960:30:180,scale=720:1280'   # v3: 앞쪽 다른 학생 잘라 냄(시선)
FX[V+'v23.mp4']=',crop=576:1024:110:0,scale=720:1280'   # v3: 앞 학생 필기 손 숨김
GRADE=',eq=saturation=0.86:gamma=0.98,colorbalance=rm=-0.04:bm=0.04:rh=-0.03:bh=0.03'   # v2: 10화처럼 덜 노랗고 덜 진하게
CAPL='{\\an7\\pos(40,86)\\fs34}'
# ================= 훅: "선생님이 뭔데요?" → 말 잃은 준호 → 창밖 이사장·기자 (대사 자막 없음, 큰 제목만) =================
_h=wt('21','뭔데',1.4)+0.55
add([(V+'v21.mp4',OFF.get('21',0)+v0('21'),round(_h-v0('21'),2)),(V+'k324.mp4',1.6,1.1),(V+'v23.mp4',VE['v23']+0.05,0.55),(V+'k325.mp4',1.0,1.0)],
    au=[(AW('21'),-v0('21'),1.0,'d',('cut',_h))],
    subs=[(0.1,_h-v0('21')+2.7,"{\\an5\\pos(360,800)\\fad(150,0)}선생님이\\N{\\c&H0078E0FF&\\fscx130\\fscy130}뭔데요?",'HookT')],
    ev=[(A+'thud.wav',_h-v0('21')+0.02,0.9,'s',None),(A+'heart.wav',_h-v0('21')+1.2,0.8,'s',None),(A+'heart.wav',_h-v0('21')+2.0,0.8,'s',None)])
HIT.append(_h-v0('21')+0.02)
# ================= ① 교무실: 이사장 도착 =================
MK['s1']=T
speak('01',[(0,'v')],'교장 선생님,|계십니까?',tail=0.05)
MK['t02']=T
speak('02',[(0,'v'),(2.6,ve('v01')),(3.6,'v')],'지금 수업 중이십니다.|수업 중엔,|아무도 안 부릅니다.',tail=0.1)
MK['walk']=T
add([(V+'k305.mp4',0.4,1.1)],ev=[(A+'whoosh.wav',0.0,0.4,'s',None)])
# ================= ② 교감 자리: 민원 전화 → 기자 =================
MK['s2']=T
_m=v1('05')+0.1
add([(V+'k306.mp4',0.2,0.9)],ev=[(A+'ring.wav',0.0,0.5,'s',None)])
MK['t05']=T
_c1=wt('05','청소',3.0)-0.1; _c2=wt('05','제가',6.5)-0.1
add([seg('05','v',0,_c1),(img('306',1.0,'face'),0,1.0),(V+'k313.mp4',0.4,1.2),seg('05','v',_c1+2.2,round(_c2-_c1-2.2,2)),(img('306',1.0,'in'),0,1.0),seg('05','v',_c2+1.0,round(_m-_c2-1.0,2))],
    au=[(AW('05'),0,1.0,'d',None)],subs=chunks('신입생 엄마인데요…|우리 애가|화장실 청소를 한다니|마음이 아파서요.|제가 대신 하면|안 될까요?','05'))   # v4: 어머니 입(1.3배)과 교감 듣는 얼굴(입 다문 그림) 교차
SUB.append((MK['t05']+0.1,MK['t05']+2.0,'신입생 어머니(전화)','Tag'))
SUB.append((MK['t05']+_c1+1.05,MK['t05']+_c1+2.15,'같은 시각 · 교장은 수업 중','Tag'))
MK['t06']=T
speak('06',[(0,'v')],'네?',tail=0.25)   # v9: 사장님 '네? 정도로만'
MK['t07']=T
speak('07',[(0,'v'),(2.2,ve('v06')),(3.0,'v')],'민원 건으로|취재 왔습니다.|교장 선생님은요?',tail=0.1,ev=[(A+'whoosh.wav',0.0,0.4,'s',None)])
SUB.append((MK['t07']+0.1,MK['t07']+2.0,'방송 기자','Tag'))
speak('08',[(0,'v')],'…수업 중이십니다.',tail=0.1)
MK['t09']=T
speak('09',[(0,'v')],POP+'교장이…|'+K('수업')+'을요?',tail=0.3)
HIT.append(MK['t09']+wt('09','수업',1.0))
speak('10',[(0,'v')],'민원은…|제가 받습니다.',tail=0.12,ev=[(A+'thud.wav',0.0,0.4,'s',None)])
MK['peek']=T
add([(V+'k312.mp4',0.0,1.5)],ev=[(A+'whoosh.wav',0.0,0.4,'s',None)])
# ================= ③ 교실: 질문 =================
MK['s3']=T
add([(V+'k313.mp4',0.4,1.4)])
def piece(c,a,b,sub,f=None,ev=(),st=None):
    add([(f or V+f'v{c}.mp4',a+OFF.get(c,0.0),round(b-a,3))],au=[(AW(c),0,1.0,'d',('part',a,b))],subs=[(0.02,b-a-0.02,sub,st or SP.get(c,'DD'))],ev=ev)
TK=[(A+'tak.wav',0.0,0.6,'s',None)]
piece('11',max(0,v0('11')-0.05),v1('11')+0.08,'쌤, 화장실 가도 돼요?')
MK['t14']=T
piece('14',0.0,1.1,'그건 허락.',V+'v14a.mp4',TK)
piece('12',max(0,v0('12')-0.05),v1('12')+0.08,'숙제 있어요?')
piece('14',1.1,2.15,'그건 확인.',V+'v14b.mp4',TK)
piece('13',max(0,v0('13')-0.05),v1('13')+0.08,'선생님, 지금 뭐라고 하셨어요?')
piece('141',max(0,v0('141')-0.05),v1('141')+0.1,'그건 집중력.',V+'v141c.mp4',TK)
MK['t14r']=T; _r0=3.27; _L=v1('14')+0.15
_k2=wt('14','막힌',5.76)
_parts=[('그런 건,',3.3),('짝한테 물어.',4.0),('나한텐,',5.08),(K('막힌 생각')+'을 가져와.',5.76),('네 생각의 구멍이 어딘지,',7.1),('그런 거.',8.82)]
_subs=[(a-_r0,(_parts[k+1][1] if k+1<len(_parts) else _L)-_r0-0.02,t,'DD') for k,(t,a) in enumerate(_parts)]
_subs+=[(0.0,_k2-_r0-0.1,'{\\an8\\pos(360,150)\\fs44}친구에게 → 허락 · 확인 · 놓친 말','Act'),(_k2-_r0,_L-_r0,'{\\an8\\pos(360,150)\\fs44}선생님에게 → 막힌 생각','Act')]
add([(V+'v14.mp4',_r0,round(_k2-0.1-_r0,3)),(V+'v13.mp4',VE['v13']+0.2,0.9),(V+'v14.mp4',_k2+0.8,round(_L-_k2-0.8,3))],au=[(AW('14'),0,1.0,'d',('part',_r0,_L))],subs=_subs)
# ================= ④ 지각 → 결정타 =================
MK['t16']=T
speak('16',[(0,'v')],'이준호.|어딨지?',tail=0.2)
MK['mur']=T
add([(V+'k315.mp4',0.4,2.6)],au=[(A+'murmur.wav',0.0,1.0,'d',None)],subs=[(0.1,0.9,'몰라요…','N'),(0.9,1.8,'어? 아까 있었는데…','N'),(1.8,2.6,'화장실 간 것 같던데…','N')])
MK['clock']=T
add([(V+'k3161.mp4',0.3,1.3)],ev=[(A+'tick.wav',0.0,0.7,'s',None)],subs=[(0.1,1.3,'{\\an5\\pos(360,1000)\\fscx150\\fscy150\\bord7\\c&H0000E6FF&}15분 뒤','Ono')])
MK['enter']=T
add([(V+'k317.mp4',0.3,1.9)],ev=[(A+'door.wav',0.1,0.8,'s',None)])
SUB.append((MK['enter']+0.3,MK['enter']+1.9,'이준호 · 해당 학생','Tag'))
MK['t18']=T
speak('18',[(0,'v')],'준호,|지금 '+K('15분')+' 지각이야.',tail=0.15)
speak('19',[(0,'v'),(2.0,ve('v18')),(2.9,'v')],'친구한테,|화장실 다녀온다고 말했어요.',tail=0.15)
MK['t20']=T
speak('20',[(0,'v'),(wt('20','니',1.6)-0.05,ve('v19',0.1)),(wt('20','니',1.6)+0.8,'v')],'이 수업의 선생님은 나야.|니 친구가 아니고.',tail=0.2)
MK['t21']=T
speak('21',[(0,'v')],'…선생님이 뭔데요.|우리 엄마도|저 안 혼내는데요.',tail=0.25,ev=[(A+'thud.wav',0.0,0.3,'s',None)])
MK['t22']=T
_s1=wt('22','먼저',1.0)
speak('22',[(0,'v'),(v1('22')-1.6,ve('v21',0.1)),(v1('22')-0.6,'v')],POP+'선생.|먼저 선, 날 생.|너보다 먼저|살아 본 사람이야.',tail=0.35,ev=[(A+'impact.wav',v0('22')-0.02,1.0,'s',None)])
SUB.append((MK['t22']+v0('22'),MK['t22']+v1('22')+0.3,'{\\an5\\pos(170,250)\\fnNanumMyeongjo\\b1\\fs110\\bord6\\3c&H202020&\\c&HF0F0F0&\\fad(120,0)}先生','Ono'))
HIT.append(MK['t22']+v0('22'))
MK['t23']=T
_a=wt('23','밖에서',5.6); _b=wt('23','그러니까',8.8)
speak('23',[(0,'v'),(_a-1.2,'clip:k324@0.3'),(_a+0.6,'v'),(_b-1.5,'clip:k325@0.4'),(_b-0.1,'v')],'그리고 나도 보니까,|너희 어머님 훌륭하시더라.|그래서 자식을|잘 키우셨을 것 같아.|밖에서 이러는데,|뭐라고 안 하셨을 리가 없지.|그러니까|'+K('부모님 욕보이지 말고')+',|잘하자.',tail=0.2,
      ev=[(A+'scribble.wav',_b-1.4,0.5,'s',None)])
MK['sit']=T
add([(V+'k324.mp4',2.4,1.4)])
# ================= ⑤ 복도: 종 친 뒤 =================
MK['s5']=T
add([(V+'k325.mp4',2.2,1.2)],ev=[(A+'bell.wav',0.0,0.7,'s',None)])
MK['t26']=T
speak('26',[(0,'v')],'수업 중이었습니다.|무슨 일이십니까?',tail=0.15)
speak('27',[(0,'v')],'아, 아닙니다.|그냥… 지나가다가.',tail=0.2)
MK['t28']=T
speak('28',[(0,'v')],'교장 선생님,|신입생 어머님이…|화장실 청소를|대신 하시겠다고…',tail=0.1)
MK['t29']=T
speak('29',[(0,'v'),(wt('29','대신',2.0)-0.1,ve('v28')),(wt('29','대신',2.0)+0.9,'v')],'어머님께 전해 주십시오.|대신 해 주시면,|깨끗해지는 건|'+POP+K('화장실뿐')+'이라고요.',tail=0.2,ev=[(A+'impact.wav',wt('29','화장실',3.6)-0.02,0.8,'s',None)])
HIT.append(MK['t29']+wt('29','화장실',3.6))
speak('30',[(0,'v')],'교장 선생님,|한 말씀만 해 주시죠.',tail=0.1,ev=[(A+'scribble.wav',0.0,0.5,'s',None)])
MK['t31']=T
speak('31',[(0,'v'),(wt('31','화장실',3.2)-0.1,ve('v27',0.2)),(wt('31','화장실',3.2)+0.8,'v')],POP+'선생님들은,|'+K('임용고시')+'를 통과한|전문가입니다.|화장실 민원이나|상대하라고 뽑은|분들 아닙니다.',tail=0.25,ev=[(A+'impact.wav',v0('31')-0.02,0.9,'s',None)])
HIT.append(MK['t31']+v0('31'))
MK['last_end']=T-0.2
# ================= ⑥ 끝: 뉴스 → 서랍 → 만년필 → 다해 얼굴 =================
MK['news']=T
add([(img('o_news',1.5,'in'),0,1.5)],ev=[(A+'whoosh.wav',0.0,0.4,'s',None)])   # v9: 신문 넘기는 소리 대신 휙
MK['drawer']=T
add([(V+'k332.mp4',1.0,1.0)],ev=[(A+'thud.wav',1.0,0.35,'s',None)])
MK['pen']=T
add([(V+'k333.mp4',0.6,0.75)])
MK['fin']=T
add([(V+'k334.mp4',0.6,1.2)])
total=T
SUB+=[(MK['s1']+0.05,MK['walk']-0.05,CAPL+'5교시 · 교무실','Cap'),
      (MK['s1']+0.1,MK['s1']+1.9,'재단 이사장','Tag'),
      (MK['t02']+0.1,MK['t02']+1.7,'동료 교사','Tag'),
      (MK['s2']+0.05,MK['t06']-0.05,CAPL+'같은 시각 · 교감 자리','Cap'),
      (MK['s3']+0.05,MK['s3']+1.4,CAPL+'5교시 · 국어 시간','Cap'),
      (MK['s3']+0.1,MK['s3']+1.4,'독고다해 · 교장(수업 중)','Tag'),
      (MK['s5']+0.05,MK['t26']+1.0,CAPL+'쉬는 시간 · 복도','Cap'),
      (MK['news']+0.05,MK['drawer']-0.05,CAPL+'다음 날 아침 · 신문','Cap'),
      (MK['fin']+0.05,MK['fin']+1.2,'{\\pos(360,780)\\fad(150,0)\\fscx110\\fscy110}손님이 온다, 바다 건너서','Ono'),
      (MK['fin']+0.25,MK['fin']+1.2,'{\\pos(360,900)\\fnNanumGothic\\b1\\fs28\\fsp3\\bord3\\c&H0078E0FF&}교사X 12화 · 12월 14일(월) 저녁 6시','Ono')]
# 배경음: 교무실·복도 가벼운 바탕 → 교실 긴장 저음(결정타 0.5초 전 끊음 = 정적) → 끝은 따뜻한 화음
EV.append((A+'bedA.wav',MK['s1'],0.35,'s',('end',MK['s3']-MK['s1'])))
EV.append((A+'dark.wav',MK['t16'],0.5,'s',('cut',MK['t22']-MK['t16']-0.5)))
_b29=MK['t29']+wt('29','화장실',3.6)-0.3
EV.append((A+'bedA.wav',MK['s5'],0.3,'s',('cut',_b29-MK['s5'])))   # v7: 29 '화장실뿐' 직전 0.3초 정적
EV.append((A+'bedA.wav',_b29+0.9,0.3,'s',('cut',MK['t31']+v0('31')-0.3-_b29-0.9)))   # 31 직전 0.3초 정적   # v3: 31 직전 0.3초 정적
EV.append((A+'warm.wav',MK['news'],0.5,'s',('end',total-MK['news'])))
print('total',round(total,2),{k:round(v,2) for k,v in MK.items()})
# ---------- 5) 렌더 ----------
os.makedirs(A+'seg',exist_ok=True); FL=[]; CUM=0.0
for i,(f,s,dd) in enumerate(P):
    o=A+f'seg/s{i:03d}.mp4'; n0=round(CUM*24); CUM+=dd; nf=max(1,round(CUM*24)-n0)
    run(['ffmpeg','-nostdin','-v','error','-y','-ss',str(max(0,s)),'-i',f,'-vf',"scale=720:1280,fps=24"+FX.get(f,"")+("" if "/lc/o_" in f else GRADE)+",tpad=stop_mode=clone:stop_duration=2,format=yuv420p",'-frames:v',str(nf),'-an','-c:v','libx264','-preset','veryfast','-crf','19',o]); FL.append(o)
open(A+'seg/l.txt','w').write(''.join(f"file '{x}'\n" for x in FL))
run(['ffmpeg','-nostdin','-v','error','-y','-f','concat','-safe','0','-i',A+'seg/l.txt','-c','copy',A+'pic.mp4'])
cmd=['ffmpeg','-nostdin','-v','error','-y']
for e in EV: cmd+=['-i',e[0]]
fl=''; dl=[]; sl=[]
for i,(f,at,v,k,tr) in enumerate(EV):
    ex=''
    if tr:
        if tr[0]=='seek': ex=f',atrim={tr[1]:.3f}:{tr[1]+tr[2]:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.3,afade=t=out:st={max(0,tr[2]-0.6):.3f}:d=0.6'
        if tr[0]=='cut': ex=f',atrim=0:{tr[1]:.3f},afade=t=in:d=0.05,afade=t=out:st={max(0,tr[1]-0.15):.3f}:d=0.15'
        if tr[0]=='part': ex=f',atrim={tr[1]:.3f}:{tr[2]:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={max(0,tr[2]-tr[1]-0.03):.3f}:d=0.03'
        if tr[0]=='end': ex=f',atrim=0:{tr[1]:.3f},afade=t=in:d=1.0,afade=t=out:st={max(0,tr[1]-1.5):.3f}:d=1.5'
    if at<0: ex+=f',atrim=start={-at:.3f},asetpts=PTS-STARTPTS'; at=0
    ms=max(0,int(round(at*1000)))
    fl+=f"[{i}:a]aformat=sample_rates=44100:channel_layouts=stereo{ex},volume={v},adelay={ms}|{ms},apad=whole_dur={total}[a{i}];"
    (dl if k=='d' else sl).append(f'[a{i}]')
fl+=''.join(dl)+f"amix=inputs={len(dl)}:normalize=0,asplit=2[D1][D2];"
fl+=''.join(sl)+f"amix=inputs={len(sl)}:normalize=0[SX];[SX][D2]sidechaincompress=threshold=0.015:ratio=10:attack=20:release=350[SD];"
fl+=f"[D1][SD]amix=inputs=2:normalize=0,atrim=0:{total}[out]"
cmd+=['-filter_complex',fl,'-map','[out]','-c:a','pcm_s16le',A+'aud_pre.wav']; run(cmd)
_I=lufs(A+'aud_pre.wav'); _g=-14.0-_I; print('pre I',_I,'gain',round(_g,2))
run(['ffmpeg','-nostdin','-v','error','-y','-i',A+'aud_pre.wav','-af',f'volume={_g:.2f}dB,alimiter=limit=0.6:level=false:attack=1:release=50','-c:a','aac','-b:a','192k',A+'aud.m4a'])
def ts(x): x=max(0,x); h=int(x//3600); m=int(x%3600//60); s=x%60; return f"{h}:{m:02d}:{s:05.2f}"
head=open(E+'sub_v2_header.ass').read().replace(',1,5,1,2,40,100,295,1',',1,7,3,2,40,100,295,1').replace(',1,4,1,2,40,100,295,1',',1,7,3,2,40,100,295,1').replace('\n\n[Events]','\nStyle: HookT,Black Han Sans,58,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,5,3,2,24,24,150,1\n\n[Events]',1)
for a,b,txt,st in sorted(SUB): head+=f"Dialogue: 0,{ts(a)},{ts(b)},{st},,0,0,0,,{txt}\n"
open(A+'sub.ass','w').write(head)
SH='+'.join(f"between(t,{x:.2f},{x+0.25:.2f})" for x in HIT) or '0'
shake=f"crop=w=696:h=1256:x='12+11*sin(2*PI*t*26)*({SH})':y='12+11*cos(2*PI*t*21)*({SH})',scale=720:1280"
_B=sorted([x for x in SUB if x[3] in ('DV','DD','N')])
OVL=[(round(_B[i][0],2),vis(_B[i][2]),vis(_B[i+1][2])) for i in range(len(_B)-1) if _B[i][1]>_B[i+1][0]+0.01]
print('SUB OVERLAP',OVL); print('WARN long lines',WARN)
outn=A+'ep11_v9.mp4'
run(['ffmpeg','-nostdin','-v','error','-y','-i',A+'pic.mp4','-i',A+'aud.m4a','-vf',f"setpts=N/(24*TB),{shake},ass={A}sub.ass:fontsdir={F},fade=t=out:st={total-0.4:.2f}:d=0.4",'-c:v','libx264','-preset','veryfast','-crf','20','-c:a','copy','-shortest',outn])
_cuts=subprocess.run(['ffmpeg','-i',outn,'-vf',"select='gt(scene,0.2)',showinfo",'-an','-f','null','-'],capture_output=True,text=True).stderr.count('pts_time:')
_lw=MK['last_end']
print(f"""[편집장 측정값]
전체 길이: {total:.1f}초 / 컷 수: {_cuts} / 평균 컷 길이: {total/max(1,_cuts+1):.1f}초
마지막 대사 끝: {_lw:.1f}초 / 그 뒤 말 없는 구간: {total-_lw:.1f}초
자막 겹침: {len(OVL)}건""")
print('ok',outn)
