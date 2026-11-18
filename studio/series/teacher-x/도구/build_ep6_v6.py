# 교사X 6화(회비 안 낸 사람) 편집 v6 (사장님 캡처 11/18: 명판이 여전히 비어 있음 — 원인: 글자 넣은 그림(o604) 대신 원본(604)을 불러옴 → o604로) / v5 (사장님 11/18: 41초쯤 '오후 4시 40분'·이름표가 정우 얼굴을 가림 → 시간 글자는 앞에 넣은 노을 교무실 컷(r507)에, 이름표는 가슴 옆 아래로 / Gemini P2: 마지막 교감 컷 꼬리 0.3→0.1초 / 명판 한자(ep6_ov_v3.py)) / v4 (v3 측정: 동료 교사 녹음이 앞뒤 대사보다 약 5dB 작음(-30.2 vs 05 -25.4 LUFS) → 3.8배 + 리미터) / v3 (사장님 11/18: 폰·회칙 글자 삐뚤어짐 → ep6_ov_v2.py로 기울기 맞춤, 설립자 명판 새김 글씨, 마지막 다해 얼굴 뭉개짐 → 2K 원본 그림에서 자른 o508f, '심심해' 교감 팔 하나 없어 보임 → 얼굴·올린 팔만 보이게 확대, 동료 교사 말 느리고 작음 → 1.2배 빠르게·+7dB) / v2 (v1 프레임 확인: 훅 제목이 메신저 글자 위에 겹침 → 훅 메신저를 화면 위쪽으로, '오후 3시' 글자가 폰 화면을 가림 → 다음 컷으로) / v1 — 7비트 순서(매뉴얼 2-1). 틀: build_ep5_v9.py
# 샌드박스: ~/ep7/{v(vNN·rNNN), img, ov, ed(aNN.wav), lc, timing.json}, ~/ep2/sfx3, ~/ed/usfx, ~/music, ~/fonts. 시계 반짝임·코트 컷은 5화 것(~/ep6: o608a/b, r406)을 복사
# 대사 클립은 모델이 말을 늦게 시작한 것이 있어(클립 소리와 원래 녹음을 맞춰 잼) OFF만큼 뒤에서 자름: 03 1.01 / 05 0.97 / 11 1.11 / 13 0.47
import subprocess, os, json, re, shutil
from PIL import ImageFont
H='/home/user'; E=H+'/ep7/'; V=E+'v/'; A=E+'ed/'; IMG=E+'img/'; OV=E+'ov/'; LC=E+'lc/'; X=H+'/ep2/sfx3/'; U=H+'/ed/usfx/'; M=H+'/music/'
os.makedirs(LC,exist_ok=True)
for s,d in [(H+'/ep6/ov/o608a.png',OV),(H+'/ep6/ov/o608b.png',OV),(H+'/ep6/v/r406.mp4',V)]:
    if not os.path.exists(d+os.path.basename(s)): shutil.copy(s,d)
TJ=json.load(open(E+'timing.json'))
OFF={'03':1.01,'05':0.97,'09':0.1,'11':1.11,'13':0.47}
SPD={'06':1.2}  # v3: 동료 교사 말을 1.2배 빠르게(녹음·입 영상 함께)
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
    z={'in':"1.05+0.0025*on",'out':"1.25-0.0025*on",'slow':"1.02+0.0008*on",'msg':"1.45+0.002*on",'msgh':"1.45+0.002*on",'phone':"1.22+0.002*on"}[mode]
    cx,cy={'msg':(0.59,0.335),'msgh':(0.59,0.47),'phone':(0.55,0.52)}.get(mode,(0.5,0.5))
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
SP={**{c:'DV' for c in ['01','02','03','05','07','13','15']},**{c:'DJ' for c in ['08','10']},'06':'N'}
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
    if what=='v': return (V+f'v{c}.mp4',t*SPD.get(c,1.0)+OFF.get(c,0.0),d)
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
DH=['04','09','11','12','14']
for c in DH:
    run(['ffmpeg','-nostdin','-v','error','-y','-i',A+f'a{c}.wav','-af','equalizer=f=170:t=q:w=1.0:g=3,equalizer=f=3000:t=q:w=1.0:g=2.5,acompressor=threshold=0.08:ratio=3:attack=5:release=120:makeup=1.6',A+f'e{c}.wav'])
def AW(c): return A+('a06f.wav' if c=='06' else f'e{c}.wav' if c in DH else f'a{c}.wav')
run(['ffmpeg','-nostdin','-v','error','-y','-i',A+'a06.wav','-af','atempo=1.2,volume=3.8,alimiter=limit=0.9:level=false',A+'a06f.wav'])
for k in ('v0','v1','dur'): TJ['06'][k]=round(TJ['06'][k]/1.2,3)
FX[V+'v06.mp4']=',setpts=PTS/1.2'
FX[V+'v01.mp4']=',crop=iw*0.6:ih*0.6:iw*0.05:ih*0.06,scale=720:1280:flags=lanczos'  # v3: 팔 하나 안 보이는 쪽을 화면 밖으로
PING=X+'s18.mp3'
# ================= ① 굴욕/위기 (훅): 다해 모니터의 메신저 쪽지 → 다해 눈. 대사 자막 없이 제목만 =================
add([(img('o601',2.7,'msgh'),0,2.7),(V+'r503.mp4',0.4,2.0)],
    subs=[(0.15,4.7,"{\\fad(200,0)}계약직은 친목회원이 아닙니다.\\N{\\alpha&HFF&\\t(900,910,\\alpha&H00&)\\fscx150\\fscy150\\t(900,1060,\\fscx100\\fscy100)}"+YN+"회식에 참여 희망하시면\\N"+YN+"별도 회비를 내세요",'HookT')],
    ev=[(PING,0.15,0.6,'s',None),(X+'s19.mp3',2.7,0.5,'s',None)])
HIT.append(2.7)
# ================= ② 세계 제시: 단체방 회식 공지, 심심한 교감 vs 서류에 파묻힌 교사들 =================
MK['s1']=T
add([(img('o602',1.9,'phone'),0,1.9),(V+'r502.mp4',0.3,1.5)],ev=[(PING,0.1,0.5,'s',None)])
MK['t01']=T
speak('01',[(0,'v'),(2.2,'clip:r501@0.4'),(3.5,'v')],'아이고, 심심해.|오늘따라 할 일이 없네.',tail=0.15)
# ================= ③ 정체 떡밥: 다해 책상의 빨간 만년필 → 복도의 설립자 액자(명판 안 보임) =================
add([(img('603',1.7,'slow'),0,1.7),(img('o604',1.9,'in'),0,1.9)],ev=[(PING,0.2,0.35,'s',None)])
MK['b1_end']=T
# ================= ④ 압박 상승 =================
speak('02',[(0,'v'),(1.7,'clip:r504@0.4'),(2.9,'v')],'자, 오늘 다들 오죠?|1차는 '+K('친목회비')+'로 쏩니다!',tail=0.1)
speak('03',[(0,'v')],'독고 선생은|'+K('메신저')+' 봤죠?',tail=0.1)
MK['dh']=T
speak('04',[(0,'v')],'네.',tail=1.0)
speak('05',[(0,'v'),(1.9,'clip:v04@2.2'),(3.1,'v')],'회비 안 내는 사람이|먹으면, 다른 선생님들|'+K('손해')+'잖아. 이해하죠?',tail=0.1)
MK['t06']=T
speak('06',[(0,'v'),(1.7,'clip:r503@1.6'),(2.8,'v')],'…계약직은 원래|친목회 안 들긴 하죠.',tail=0.1)
speak('07',[(0,'v'),(2.4,'clip:v04@3.9')],'그리고 '+K('가족관계증명서')+'.|아직이죠?',tail=0.1)
MK['b2_end']=T
# ================= ⑤ 1차 반전: 정우가 메신저를 우연히 봄 =================
MK['s5']=T
add([(V+'r507.mp4',2.4,1.1)])  # v5: 4시 40분 알리는 노을 교무실 컷(시간 글자를 정우 얼굴 위에서 뺌)
MK['t08']=T
speak('08',[(0,'v')],'다해 쌤, 회식 같이 가요.|제가 차 태워 드릴게요.',tail=0.1)
speak('09',[(0,'v')],'저는 괜찮아요.|먼저 가세요.',tail=0.1)
MK['reveal']=T
add([(img('o601',1.9,'msg'),0,1.9)],ev=[(X+'s19.mp3',0.0,0.55,'s',None)])
HIT.append(MK['reveal'])
speak('10',[(0,'v')],'…이걸,|쌤한테만 보낸 거예요?',tail=0.15)
# ================= ⑥ 카타르시스: 회칙 한 장 → 제2조 → "심심하시다면서요" =================
MK['t11']=T
add([(img('o605',1.7,'in'),0,1.7)],ev=[(X+'s23.mp3',0.15,0.9,'s',None)])
HIT.append(MK['t11']+0.15)
speak('11',[(0,'v'),(1.7,'clip:r506@0.3'),(3.0,'v')],'친목회 회칙 '+K('제2조')+'.|"본교 교직원은|누구나 회원이 될 수 있다."',tail=0.1)
speak('12',[(0,'v'),(1.9,'clip:v13@2.6'),(3.1,'v')],'제 가입 신청서,|3월에 냈는데요.|아직 '+K('결재')+' 안 하셨더라고요.',tail=0.1)
MK['t13']=T
speak('13',[(0,'v')],'그, 그건…|바빠서…',tail=0.15,ev=[(U+'boing2.mp3',0.05,0.4,'s',None)])
MK['t14']=T
speak('14',[(0,'v')],POP+K('심심하시다면서요.'),tail=0.25)
HIT.append(MK['t14']+v0('14'))
add([(V+'r507.mp4',0.4,1.4),(V+'r505.mp4',0.3,1.7)])
FX[V+'r507.mp4']=',colorbalance=rs=0.14:gs=0.04:bs=-0.14,eq=brightness=-0.02:saturation=1.05'  # 낮 빛 → 4시 45분 노을 색
FL.append(T+0.42)
add([(img('o608a',0.4,'in'),0,0.4),(img('o608b',0.5,'in'),0,0.5),(V+'r406.mp4',0.2,1.0)],ev=[(PING,0.0,0.4,'s',None)])
MK['b3_end']=T
# ================= ⑦ 클리프행어: 혼자 남은 교감 → 퇴근길 다해 표정 CU + 떡밥 글자 =================
MK['s7']=T; MK['song']=T
speak('15',[(0,'v')],'두고 봐…|다음 달이면 '+K('내가 교장')+'이야.',tail=0.1)
MK['last_end']=T-0.1
add([(V+'r508.mp4',0.2,1.6)])
MK['fin']=T
add([(img('o508f',2.2,'slow'),0,2.2)])  # v3: 마지막 프레임 = 다해 얼굴 CU, 2K 원본에서 자름(영상 확대는 뭉개짐)
total=T
SUB+=[(MK['s1']+1.95,MK['s1']+3.9,'친목회 회식 날 · 오후 3시','Cap'),
      (MK['t01']+0.1,MK['t01']+1.9,'교감','Tag'),
      (MK['dh']+0.05,MK['dh']+1.75,'{\\fs40}독고다해 · 계약교사\\N{\\fs24}(극 중 설정)','Tag'),
      (MK['t06']+0.1,MK['t06']+1.9,'동료 교사','Tag'),
      (MK['s5']+0.05,MK['s5']+1.1,'오후 4시 40분','Cap'),
      (MK['t08']+0.3,MK['t08']+2.2,'{\\an7\\pos(24,700)}안정우 · 통합과학 교사','Tag'),
      (MK['fin']+0.2,MK['fin']+2.2,'{\\pos(360,880)\\fad(150,0)}다음 달, 교장 인사 발표','Ono'),
      (MK['fin']+0.7,MK['fin']+2.2,'{\\pos(360,1010)\\fs34}교사X 7화 · 12월 2일(수) 저녁 6시','Ono')]
EV.append((X+'B1.mp3',MK['s1'],0.35,'s',('cut',MK['b1_end']-MK['s1'])))
EV.append((X+'B2.mp3',MK['b1_end'],0.4,'s',('seek',0.0,MK['reveal']-MK['b1_end'])))  # 메신저를 보는 순간 음악 끊음
EV.append((X+'B2.mp3',MK['t11']+0.2,0.4,'s',('seek',40.0,MK['t14']-MK['t11']-0.2)))  # '심심하시다면서요' 앞에서 끊고 정적
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
head=open(H+'/ep2/sub_v2_header.ass').read().replace('\n\n[Events]','\nStyle: HookT,Black Han Sans,58,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,5,3,2,24,24,300,1\n\n[Events]',1)
for a,b,txt,st in SUB: head+=f"Dialogue: 0,{ts(a)},{ts(b)},{st},,0,0,0,,{txt}\n"
open(E+'ed/sub.ass','w').write(head)
flash=','.join(f"drawbox=c=white@0.85:t=fill:enable='between(t,{x:.2f},{x+0.08:.2f})'" for x in FL)
SH='+'.join(f"between(t,{x:.2f},{x+0.25:.2f})" for x in HIT) or '0'
shake=f"crop=w=696:h=1256:x='12+11*sin(2*PI*t*26)*({SH})':y='12+11*cos(2*PI*t*21)*({SH})',scale=720:1280"
_B=sorted([x for x in SUB if x[3] in ('DV','DJ','DD','N','Hit')])
OVL=[(round(_B[i][0],2),vis(_B[i][2]),vis(_B[i+1][2])) for i in range(len(_B)-1) if _B[i][1]>_B[i+1][0]+0.01]
print('SUB OVERLAP',OVL)
print('WARN long lines',WARN); print('HIT',[round(h,2) for h in HIT])
outn=E+'ed/ep6_v6.mp4'
run(['ffmpeg','-nostdin','-v','error','-y','-i',E+'ed/pic.mp4','-i',E+'ed/aud.m4a','-vf',f"setpts=N/(24*TB),{flash},{shake},ass={E}ed/sub.ass:fontsdir={H}/fonts,fade=t=out:st={total-0.6:.2f}:d=0.6",'-c:v','libx264','-preset','veryfast','-crf','20','-c:a','copy','-shortest',outn])
print('ok',outn)
_lw=MK['last_end']
_cuts=subprocess.run(['ffmpeg','-i',outn,'-vf',"select='gt(scene,0.2)',showinfo",'-an','-f','null','-'],capture_output=True,text=True).stderr.count('pts_time:')
print(f"""[편집장 측정값]
전체 길이: {total:.1f}초 / 컷 수: {_cuts} / 평균 컷 길이: {total/max(1,_cuts+1):.1f}초
마지막 대사 끝: {_lw:.1f}초 / 그 뒤 말 없는 구간: {total-_lw:.1f}초
훅: 메신저 쪽지 2.7초 → 다해 눈 2.0초(대사 없음, 제목만)
자막 겹침: {len(OVL)}건""")
