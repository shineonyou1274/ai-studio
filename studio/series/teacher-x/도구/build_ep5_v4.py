# 교사X 5화(1등급 0명) 편집 v4 (v3 + 사장님 11/17: 훅 제목 '시험 쉽게 내라던', 이사장 컷 빨간 만년필로 다시(v14·r5072·r5082), 만년필 CU(n607), 퇴장 뒷모습(n609)) / v3 (v2 + 사장님 11/17: 진짜 전화벨, 이사장 퇴장을 분명히, Gemini P0 결재판 타점(쿵 + 음악 1초 끊김)) / v2 (v1 + 긴 자막 줄 나눔, 다해 이름표를 다해 화면으로, 끝 꼬리 5초 이내) / v1 — 7비트 순서(매뉴얼 2-1, 사장님 11/17 "7비트 순서로 편집해"). 틀: build_ep4_v5.py
# 샌드박스: ~/ep6/{v(vNN·rNNN·nNNN), img, ov, ed(aNN.wav), lc, timing.json}, ~/ep2/sfx3, ~/ed/usfx, ~/music, ~/fonts. 4화 시계 그림·반짝임·코트 컷은 ~/ep5에서 복사(i608, o608a/b, r406)
import subprocess, os, json, re
from PIL import ImageFont
H='/home/user'; E=H+'/ep6/'; V=E+'v/'; A=E+'ed/'; IMG=E+'img/'; OV=E+'ov/'; LC=E+'lc/'; X=H+'/ep2/sfx3/'; U=H+'/ed/usfx/'; M=H+'/music/'
os.makedirs(LC,exist_ok=True)
TJ=json.load(open(E+'timing.json'))
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
    z={'in':"1.05+0.0025*on",'out':"1.25-0.0025*on",'crash':"if(lt(on,6),1.0+0.08*on,1.5)",'slow':"1.02+0.0008*on"}[mode]
    vf=f"scale=1440:2560,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih*0.5-(ih/zoom/2)':d={n}:s=720x1280:fps=24,format=yuv420p"
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
# 자막: 교감 DV, 정우 DJ, 나머지 다해 DD
SP={**{c:'DV' for c in ['03','04','05','07','09','12','15','16','17','18','19','20']},**{c:'DJ' for c in ['01','02','06','21','24']},'14':'N'}
Y='{\\c&H0078E0FF&\\fscx120\\fscy120}'
def K(w): return Y+w+'{\\r}'
YN='{\\c&H0078E0FF&}'
POP='{\\fscx170\\fscy170\\t(0,150,\\fscx100\\fscy100)}'
_fw=ImageFont.truetype(H+'/fonts/NanumGothicBold.ttf',40)
def vis(p): return re.sub(r'\{[^}]*\}','',p)
def chunks(text,c,off=0.0,hit_at=None,a=None):
    parts=[p.strip() for p in text.split('|') if p.strip()]
    hit=None
    if parts[-1].startswith('!H'): hit=parts.pop()[2:]
    a=v0(c) if a is None else a; b=v1(c); e=hit_at if hit else b
    tot=sum(len(vis(p)) for p in parts); t=a; out=[]; st=SP.get(c,'DD')
    for p in parts:
        if _fw.getlength(vis(p))>560: WARN.append((c,vis(p)))
        d=(e-a)*len(vis(p))/tot; out.append((off+t,off+t+d,p,st)); t+=d
    if hit: out.append((off+e,off+b+0.1,POP+hit,'Hit'))  # v5: 다음 줄 자막과 겹치지 않게(말이 끝나고 0.1초)
    return out
def seg(what,t,d,vid):
    if what=='v': return (vid,t,d)
    if what.startswith('clip:'):
        nm=what[5:]; o=0.3
        if '@' in nm: nm,o=nm.split('@'); o=float(o)
        return (V+nm+'.mp4',o,d)
    return None
def speak(c,plan,text,tail=0.12,extra=(),hit_at=None,a=None,ev=()):
    vid=V+f'v{c}.mp4'; L=v1(c)+tail; segs=[]; pts=plan+[(L,None)]
    for i in range(len(pts)-1):
        t,what=pts[i][0],pts[i][1]; d=round(pts[i+1][0]-t,3)
        if d<=0.05: continue
        s=seg(what,t,d,vid)
        segs.append(s if s else (img(what,d,pts[i][2] if len(pts[i])>2 else 'in'),0,d))
    for x in extra: segs.append(x)
    add(segs,[(AW(c),0,1.0,'d',None)],chunks(text,c,hit_at=hit_at,a=a),ev)



FX={}
DH=['08','10','11','13','22','23']
for c in DH:
    run(['ffmpeg','-nostdin','-v','error','-y','-i',A+f'a{c}.wav','-af','equalizer=f=170:t=q:w=1.0:g=3,equalizer=f=3000:t=q:w=1.0:g=2.5,acompressor=threshold=0.08:ratio=3:attack=5:release=120:makeup=1.6',A+f'e{c}.wav'])
def AW(c): return A+(f'e{c}.wav' if c in DH else f'a{c}.wav')
U2=H+'/ed/usfx/'
# 13 뒤 교감이 마지못해 받는 "네, 어머님"(03 녹음 앞쪽 중복분 0~1.74초)
run(['ffmpeg','-nostdin','-v','error','-y','-t','1.74','-i',E+'au/a03.mp3','-ar','44100','-ac','1','-af','afade=t=out:st=1.5:d=0.24',A+'h03.wav'])
RING=U2+'phone_ring.mp3'  # 사장님 11/17 준 전화벨(0~1.9초가 한 번 울림)
# ================= ① 굴욕/위기 (훅): 전화 → 굳은 교감 → 버럭. 대사 자막 없이 제목만 =================
HS=1.8
add([(V+'n603.mp4',0.2,0.8),(V+'n604.mp4',0.3,1.0),(V+'v05.mp4',0,round(v1('05')+0.45,3))],
    [(AW('05'),HS,1.0,'d',None)],
    [(0,HS+v1('05')+0.45,"{\\fad(200,0)}시험 쉽게 내라던 교감,\\N{\\alpha&HFF&\\t(780,790,\\alpha&H00&)\\fscx160\\fscy160\\t(780,950,\\fscx100\\fscy100)}"+YN+"1등급 0명 나오자…",'HookT')],
    [(RING,0.0,0.45,'s',('cut',1.85)),(X+'s19.mp3',HS+v0('05')-0.03,0.6,'s',None)])
HIT.append(HS+v0('05'))
# ================= ② 세계 제시: 성적 화면, 정우, 학부모 전화 =================
MK['s1']=T
add([(img('o601',1.8,'crash'),0,1.8)],ev=[(X+'s18.mp3',0.0,0.5,'s',None)])
MK['t01']=T
speak('01',[(0,'v')],'만점이… 스물여덟 명?',tail=0.15)
speak('02',[(0,'v'),(2.0,'clip:r501@0.5'),(3.2,'v')],'1등급이… 한 명도 없어.',tail=0.2)
add([(V+'n603.mp4',0.4,0.9)],ev=[(RING,0.0,0.45,'s',('cut',1.0))])
MK['t03']=T
speak('03',[(0,'v')],'네, 어머님. 백 점인데|'+K('1등급')+'이 아니라고요?|네, 네… 바로 확인하겠습니다.',tail=0.2)
MK['b1_end']=T
# ================= ③ 정체 떡밥: 이사장 방문, 다해만 인사 안 함, 은색 시계 =================
add([(V+'n605.mp4',0.3,1.4)],ev=[(X+'s18.mp3',0.2,0.3,'s',None)])
add([(V+'r5072.mp4',0.3,1.6)])
MK['t14']=T
speak('14',[(0,'v')],'학교에 별일 없지요?',tail=0.3)
add([(V+'n607.mp4',0.3,1.8)],ev=[(X+'s18.mp3',0.2,0.3,'s',None)])  # v4: 이사장 가슴의 빨간 만년필(가문의 증표, 말없이)
speak('15',[(0,'v')],'그럼요, 이사장님!|아무 일 없습니다.',tail=0.1)
add([(V+'n603.mp4',0.4,0.8)],ev=[(RING,0.0,0.45,'s',('cut',0.9))])  # 전화는 울리는데 "아무 일 없다"
MK['dh']=T
add([(V+'r505.mp4',0.4,1.8)])
MK['t16']=T
speak('16',[(0,'v'),(2.4,'clip:r506@0.5'),(3.8,'v')],'독고 선생! 귀가 먹었어요?|이사장님 오셨는데|당장 인사 안 합니까?')
add([(img('608',2.0,'slow'),0,2.0)],ev=[(X+'s18.mp3',0.0,0.5,'s',None)])  # 단서 오브제: 은색 시계 매크로 CU
speak('17',[(0,'v')],'에휴, 요즘 젊은 선생들이|예의가 없어요.|제가 그렇게|교육을 시켰는데도 말이죠.',tail=0.2)
add([(V+'r5082.mp4',0.2,3.0)])  # 이사장이 말없이 다해를 보다 돌아섬
MK['exit']=T
add([(V+'n609.mp4',0.2,3.0)])  # v4: 등 돌려 문 열고 나감  # v3: 문간 실루엣 = 이사장이 나감(사장님 "계속 있는 건지 나간 건지 헷갈려")
MK['b2_start']=T
# ================= ④ 압박 상승: 교감의 갑질 → 정우에게 책임 전가 =================
speak('18',[(0,'v')],'그리고 '+K('가족관계증명서')+'|아직도 안 냈죠?|내일까지 안 내면|계약 다시 봅니다.')
speak('19',[(0,'v'),(2.0,'606','in'),(3.4,'v')],'복사기에 종이 낀 거,|업체에 전화 넣어요.|지금 당장.')
add([(V+'r509.mp4',0.3,1.8)])
speak('20',[(0,'v')],'그동안 내가 당한 거 생각하면…|분이 안 풀려.',tail=0.3)
MK['t04']=T
speak('04',[(0,'v')],'안 선생! 통합과학 시험,|이게 뭐예요?',tail=0.1)
speak('05',[(0,'v')],'누가 이렇게 쉽게 내랬어!',tail=0.1,ev=[(X+'s19.mp3',v0('05')-0.03,0.5,'s',None)])
add([(V+'r503.mp4',0.3,1.0)])
speak('06',[(0,'v')],'교감 선생님이…|너무 어렵게 내지 말라고…',tail=0.15)
speak('07',[(0,'v')],'내가 언제?|난 '+K('기준은 지키면서')+'라고 했지.',tail=0.1)
MK['t08']=T
speak('08',[(0,'v'),(2.6,'clip:v07@4.0'),(3.7,'v')],'그날 저도 옆에 있었어요.|"미이수 많이 나오면,|이 동네 소문 무서운 거 다 알죠."')
speak('09',[(0,'v'),(2.6,'clip:r502@0.5'),(3.9,'v')],'독고 선생은 빠져요.|'+K('최저가')+'로 들어온 계약 교사가|뭘 안다고.')
MK['b2_end']=T
# ================= ⑤ 1차 반전: 결재판 =================
MK['t10']=T
speak('10',[(0,'v'),(1.0,'o602','slow'),(3.0,'v')],'이 시험지,|교감 선생님 '+K('결재')+'|받고 나간 겁니다.',ev=[(X+'s23.mp3',0.25,1.0,'s',None)])  # v3: 결재판 내려놓는 '쿵'
HIT.append(MK['t10']+0.25)
h11=wt('11','보셨',v1('11')-1.0)-0.2
speak('11',[(0,'v'),(1.8,'clip:r504@0.3'),(2.9,'v')],'쉽다는 것도,|!H그때 다 보셨겠죠.',hit_at=h11,ev=[(X+'s19.mp3',h11-0.05,0.6,'s',None)])
HIT.append(MK['t10']+0)  # (흔들림은 아래 HIT 계산 때 11에서)
HIT.pop()
b12=wt('12','사회',2.0)
speak('12',[(0,'v')],'그, 그건…|난 '+K('사회과')+'야,|내가 과학을 어떻게 알아?',ev=[(U2+'boing2.mp3',b12-0.05,0.5,'s',None)])
# ================= ⑥ 카타르시스: 1초 정적 → 전화벨 → 한 문장 → 교감이 받음 =================
MK['s6']=T
add([(V+'n603.mp4',0.2,1.4)],ev=[(RING,0.3,0.5,'s',('cut',1.2))])
MK['t13']=T
h13=wt('13','이번',1.0)-0.05
speak('13',[(0,'v')],'받으세요.|!H이번 전화는\\N교감 선생님 몫이에요.',hit_at=h13,tail=0.2)
HIT.append(MK['t13']+h13)
add([(V+'r510.mp4',0.2,2.0)],[(A+'h03.wav',0.1,0.8,'d',None)],[(0.1,1.9,'(작게) 네, 어머님…','DV')])
MK['b3_end']=T
# ================= ⑦ 클리프행어: 퇴근길 → 시계 반짝 → 다해 표정 CU + 떡밥 글자 =================
MK['s7']=T; MK['song']=T
speak('21',[(0,'v')],'다해 쌤… 죄송해요.|제가 어려운 문제들을 지웠어요.',tail=0.15)
speak('22',[(0,'v')],'만점 받고도 학생들이|'+K('1등급')+'을 못 받았어요.',tail=0.15)
speak('23',[(0,'v'),(2.4,'clip:v24@1.5'),(3.9,'v')],'다음 시험은,|안 선생님 기준대로 내요.|그게 학생을 지키는 거예요.',tail=0.1)
speak('24',[(0,'v')],'…네.',tail=0.35)
MK['last_end']=T-0.35
FL.append(T+0.42)
add([(img('o608a',0.4,'in'),0,0.4),(img('o608b',0.5,'in'),0,0.5),(V+'r406.mp4',0.2,1.4)],ev=[(X+'s18.mp3',0.0,0.4,'s',None)])
MK['fin']=T
add([(V+'v22.mp4',3.9,2.3)])
total=T
SUB+=[(MK['s1']+0.05,MK['s1']+2.4,'기말 성적 나온 날 · 아침 8시','Cap'),
      (MK['s1']+0.3,MK['s1']+3.6,'고1 5등급제: 1등급 = 상위 10%','Act'),
      (MK['t01']+0.1,MK['t01']+1.9,'안정우 · 통합과학 교사','Tag'),
      (MK['t03']+0.1,MK['t03']+1.9,'교감','Tag'),
      (MK['t14']+0.1,MK['t14']+2.2,'재단 이사장','Tag'),
      (MK['dh']+0.1,MK['dh']+1.9,'{\\fs40}독고다해 · 계약교사\\N{\\fs24}(극 중 설정)','Tag'),
      (MK['s7']+0.05,MK['s7']+1.6,'오후 4시 50분','Cap'),
      (MK['fin']+0.2,MK['fin']+2.3,'{\\pos(360,330)\\fad(150,0)}가족관계증명서, 내일까지?','Ono'),
      (MK['fin']+0.7,MK['fin']+2.3,'{\\pos(360,1010)\\fs34}교사X 6화 · 11월 30일(월) 저녁 6시','Ono')]
EV.append((X+'B1.mp3',MK['s1'],0.35,'s',('cut',MK['b1_end']-MK['s1'])))
EV.append((X+'B2.mp3',MK['b1_end'],0.4,'s',('seek',0.0,MK['t10']+0.3-MK['b1_end'])))  # v3: 결재판 '쿵'에서 음악 끊음
EV.append((X+'B2.mp3',MK['t10']+1.5,0.4,'s',('seek',40.0,MK['s6']-MK['t10']-1.5)))  # 1초 정적 뒤 다시, ⑥ 앞에서 다시 끊음
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
        if tr[0]=='end': ex=f',atrim=0:{tr[1]:.3f},afade=t=in:d=1.0,afade=t=out:st={tr[1]-4.0:.3f}:d=4.0'  # v4: 끝 음악 4초 페이드
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
head=open(H+'/ep2/sub_v2_header.ass').read().replace('\n\n[Events]','\nStyle: HookT,Black Han Sans,64,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,5,3,2,24,24,330,1\n\n[Events]',1)
for a,b,txt,st in SUB: head+=f"Dialogue: 0,{ts(a)},{ts(b)},{st},,0,0,0,,{txt}\n"
open(E+'ed/sub.ass','w').write(head)
flash=','.join(f"drawbox=c=white@0.85:t=fill:enable='between(t,{x:.2f},{x+0.08:.2f})'" for x in FL)
SH='+'.join(f"between(t,{x:.2f},{x+0.25:.2f})" for x in HIT) or '0'
shake=f"crop=w=696:h=1256:x='12+11*sin(2*PI*t*26)*({SH})':y='12+11*cos(2*PI*t*21)*({SH})',scale=720:1280"
_B=sorted([x for x in SUB if x[3] in ('DV','DJ','DD','Hit')])
OV=[(round(_B[i][0],2),vis(_B[i][2]),vis(_B[i+1][2])) for i in range(len(_B)-1) if _B[i][1]>_B[i+1][0]+0.01]
print('SUB OVERLAP',OV)
print('WARN long lines',WARN); print('HIT',[round(h,2) for h in HIT])
outn=E+'ed/ep5_v4.mp4'
run(['ffmpeg','-nostdin','-v','error','-y','-i',E+'ed/pic.mp4','-i',E+'ed/aud.m4a','-vf',f"setpts=N/(24*TB),{flash},{shake},ass={E}ed/sub.ass:fontsdir={H}/fonts,fade=t=out:st={total-0.6:.2f}:d=0.6",'-c:v','libx264','-preset','veryfast','-crf','20','-c:a','copy','-shortest',outn])
print('ok',outn)
_lw=MK['last_end']  # 24 말 끝
_cuts=subprocess.run(['ffmpeg','-i',outn,'-vf',"select='gt(scene,0.2)',showinfo",'-an','-f','null','-'],capture_output=True,text=True).stderr.count('pts_time:')
print(f"""[편집장 측정값]
전체 길이: {total:.1f}초 / 컷 수: {_cuts} / 평균 컷 길이: {total/max(1,_cuts+1):.1f}초
마지막 대사 끝: {_lw:.1f}초 / 그 뒤 말 없는 구간: {total-_lw:.1f}초
첫 대사 시작: {HS+v0('05'):.2f}초 / 훅 첫 화면: 울리는 전화 → 굳은 교감 → 버럭(대사 05, 1.8초)
표시 위치: 극 중 설정·인물 소개 = 왼쪽 위
자막 겹침: {len(OV)}건""")
