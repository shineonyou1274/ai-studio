# 교사X 2화 편집 스크립트 v6 (v5 + 채점 지적 고침: 효과음 누락 버그·극 중 설정·기안 풀이·알림 잘림·인서트 중복)
# (아래는 v5 설명) (자막 v2: 인물 색·핵심어 노랑·속마음 명조·결정타 팝인+흔들림·의성어·행동 자막·안전 영역). 새 화는 복사해 "회차 부분"만 바꾼다.
# 샌드박스 폴더 구조: ~/ep2/{v,x,img,ov,ed,sfx2,timing.json}, ~/fonts, ~/music, ~/ed/sfx, ~/ed/usfx
# 사용: python3 build_ep02_v4.py A   (A = 컷28 포함)
# 주의: 파이썬 문자열 안 ASS 덮어쓰기는 반드시 '{\\fs46}'처럼 역슬래시 두 개(또는 r'' 문자열). '{\fs46}'는 \f가 다른 문자로 바뀌어 효과가 사라진다.
import subprocess, os, json, sys, re
from PIL import ImageFont
H='/home/user'; E=H+'/ep2/'; V=E+'v/'; A=E+'ed/'; IMG=E+'img/'; OV=E+'ov/'; LC=E+'ed/lc/'; S=H+'/ed/sfx/'; U=H+'/ed/usfx/'; M=H+'/music/'
WITH28 = (sys.argv[1] if len(sys.argv)>1 else 'A')=='A'
TJ=json.load(open(E+'timing.json'))
def run(c): subprocess.run(c,check=True)
def v1(c): return TJ[c]['v1']
def v0(c): return TJ[c]['v0']
cache={}
def img(name,d,mode='in',tint=None):
    key=(name,round(d,2),mode,tint)
    if key in cache: return cache[key]
    src = OV+name+'.png' if os.path.exists(OV+name+'.png') else IMG+'i'+name+'.png'
    out=LC+f"{name}_{mode}_{int(d*100)}{'_t' if tint else ''}.mp4"
    n=int(round(d*24))
    z={'in':"1.05+0.0025*on",'out':"1.25-0.0025*on",'crash':"if(lt(on,6),1.0+0.08*on,1.5)",'slow':"1.02+0.0008*on",'up':"1.1"}[mode]
    yexp="ih*0.5-(ih/zoom/2)" if mode!='up' else f"(ih-ih/zoom)*(1-on/{n})"
    vf=f"scale=1440:2560,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='{yexp}':d={n}:s=720x1280:fps=24"
    if tint: vf+=",curves=r='0/0.08 1/1':g='0/0.02 1/0.82':b='0/0 1/0.55',eq=brightness=-0.04"
    vf+=",format=yuv420p"
    run(['ffmpeg','-nostdin','-v','error','-y','-loop','1','-i',src,'-vf',vf,'-t',str(d),'-c:v','libx264','-preset','veryfast','-crf','19',out])
    cache[key]=out; return out
def zoomrow(name,d,fy,out):
    n=int(round(d*24))
    run(['ffmpeg','-nostdin','-v','error','-y','-loop','1','-i',OV+name+'.png','-vf',f"scale=1440:2560,zoompan=z='1.0+min(on,12)*0.0125':x='iw/2-(iw/zoom/2)':y='max(0,min(ih*{fy}-(ih/zoom/2),ih-ih/zoom))':d={n}:s=720x1280:fps=24,format=yuv420p",'-t',str(d),'-c:v','libx264','-preset','veryfast','-crf','19',out]); return out
P=[]; EV=[]; SUB=[]; FL=[]; T=0.0; MK={}
def add(segs,au=(),subs=(),ev=()):
    global T
    for f,o,v,k,tr in list(au)+list(ev): EV.append((f,T+o,v,k,tr))
    for s in segs: P.append(s)
    for a,b,txt,st in subs:
        SUB.append((T+a,T+b,txt,st))
        if st=='Hit': HIT.append(T+a)
    T+=sum(s[2] for s in segs)
# ---- 자막 v2 ----
SP={'02':'DV','04':'DV','06':'DV','08':'DV','10':'DV','18':'DV','22':'DV','24':'DV','03':'DJ','07':'DJ','11':'DJ','26':'DJ'}  # 나머지 = 다해 DD
Y='{\\c&H0078E0FF&\\fscx120\\fscy120}'   # 핵심어 노랑 120%
def K(w): return Y+w+'{\\r}'
POP='{\\fscx170\\fscy170\\t(0,150,\\fscx100\\fscy100)}'
HIT=[]; WARN=[]
_fw=ImageFont.truetype(H+'/fonts/NanumGothicBold.ttf',40)
def vis(p): return re.sub(r'\{[^}]*\}','',p)
def chunks(text,c,off=0.0,hit_at=None):
    parts=[p.strip() for p in text.split('|') if p.strip()]
    hit=None
    if parts[-1].startswith('!H'): hit=parts.pop()[2:]
    a,b=v0(c),v1(c); e=hit_at if hit else b
    tot=sum(len(vis(p)) for p in parts); t=a; out=[]; st=SP.get(c,'DD')
    for p in parts:
        if _fw.getlength(vis(p))>540: WARN.append((c,vis(p)))
        d=(e-a)*len(vis(p))/tot; out.append((off+t,off+t+d,p,st)); t+=d
    if hit: out.append((off+e,off+b+0.35,POP+hit,'Hit'))
    return out
def speak(c,vid,plan,text,tail=0.12,extra=()):
    """plan: list of switch points [(t,'v') or (t,img,mode)] in audio time; last video seg ends at v1+tail"""
    L=v1(c)+tail; segs=[]
    pts=plan+[(L,None)]
    for i in range(len(pts)-1):
        t,what=pts[i][0],pts[i][1]; d=round(pts[i+1][0]-t,3)
        if d<=0.05: continue
        if what=='v': segs.append((vid,t,d))
        elif what.startswith('clip:'):
            nm=what[5:]; off=0.3
            if '@' in nm: nm,off=nm.split('@'); off=float(off)
            segs.append((E+'x/'+nm+'.mp4',off,d))
        else: segs.append((img(what,d,pts[i][2] if len(pts[i])>2 else 'in'),0,d))
    for x in extra: segs.append(x)
    add(segs,[(AW(c),0,1.0,'d',None)],chunks(text,c))
def inner(c,segs,text,off=0.2):
    add(segs,[(A+f'i{c}.wav',off,1.0,'d',None)],[(off,off+TJ[c]['v1']+0.2,'{\\blur6}'+text,'In')])
DH=['09','12','15','16','17','19','21','23','27','28']
for c in DH:
    run(['ffmpeg','-nostdin','-v','error','-y','-i',A+f'a{c}.wav','-af','equalizer=f=170:t=q:w=1.0:g=3,equalizer=f=3000:t=q:w=1.0:g=2.5,acompressor=threshold=0.08:ratio=3:attack=5:release=120:makeup=1.6',A+f'e{c}.wav'])
def AW(c): return A+(f'e{c}.wav' if c in DH else f'a{c}.wav')
# inner voice processing
for c in ('05','14'):
    run(['ffmpeg','-nostdin','-v','error','-y','-i',A+f'a{c}.wav','-af','highpass=f=180,lowpass=f=3800,aecho=0.8:0.75:60|140:0.45|0.3,volume=1.1',A+f'i{c}.wav'])
# hook audio: last phrase of 19
w19=TJ['19']['words']; hs=[s for (w,s,e) in w19 if w.startswith('그건')]; hs=hs[-1] if hs else v1('19')-2.6
run(['ffmpeg','-nostdin','-v','error','-y','-ss',str(max(0,hs-0.05)),'-to',str(v1('19')+0.1),'-i',A+'a19.wav',A+'h19.wav'])
hd=v1('19')+0.15-hs
# ================= HOOK =================
L12=round(v1('12')+0.12,3)
add([(V+'v12.mp4',0,1.5),(img('212',0.9),0,0.9),(V+'v12.mp4',2.4,round(L12-2.4,3))],[(AW('12'),0,1.0,'d',None),(E+'sfx3/B2.mp3',0,0.45,'s',('seek',50.0,L12))],
    [(0,L12,"{\\an8\\pos(360,28)\\fad(300,0)\\fs32}'고쳐 오라면서 길을 6번 바꾸면?'\\N3주 끌던 결재, 40분 만에 뚫린 이유",'Cap')]+chunks('커피 한 잔 드시고 오세요.|'+K('40분')+'이면 됩니다.','12'))
FL.append(T-0.08)
# ================= S1 15:00 =================
MK['s1']=T
add([(img('o01',1.5,'crash'),0,1.5)],ev=[(E+'sfx3/s15.mp3',0.1,0.45,'s',None)],subs=[(0.05,1.4,'그날 오후 3시','Cap'),(0.3,1.5,'{\\fs30}에듀파인 = 학교 전자 결재 시스템','N')])
MK['t02']=T
speak('02',V+'v02.mp4',[(0,'v'),(1.6,'clip:r501'),(2.7,'clip:n601'),(4.3,'v')],'안 선생, 이번에도 '+K('반려')+'야.|기획서 하나를 3주째|붙들고 있으면 어떡해.')
MK['t03']=T
speak('03',V+'v03.mp4',[(0,'v'),(2.4,'o01','slow'),(3.4,'v')],'어제 말씀하신 대로…|강사료, 운영비로|옮겨서 올렸는데요.')
MK['t04']=T; HIT.extend([T+0.1,T+0.4,T+0.75])
speak('04',V+'v04.mp4',[(0,'v'),(2.4,'204'),(3.9,'v'),(6.0,'clip:n601@2.4'),(7.6,'clip:r504@2.2')],'내가 언제 옮기랬어?|문맥을 봐야지.|마감 놓치면 나도|교장 선생님 뵐 낯이 없어.|책임감이 없어, 책임감이.|쯧쯧쯧')
inner('05',[(img('305',1.4,'out'),0,1.4),(E+'x/r501.mp4',2.6,1.5)],'하… 규정대로 했는데.')
# ================= S2 =================
MK['t06']=T; EV.append((E+'sfx3/s16.mp3',T+2.6,0.9,'s',None))
speak('06',V+'v06.mp4',[(0,'v'),(2.6,'306','crash'),(3.5,'206')],'독고 선생. 마침 잘됐네.|이 기획서 넘겨받아서|내일 아침까지 고쳐 와요.',tail=0.6)
MK['tag_dh']=T-1.9
speak('07',V+'v07.mp4',[(0,'v'),(1.9,'clip:r504')],'교감 선생님,|그건 제 업무인데…',tail=0.25)
MK['t08']=T
speak('08',V+'v08.mp4',[(0,'v'),(2.0,'208'),(3.0,'v')],'계약직이 재계약하려면,|이런 것도 해 봐야지.|못 하겠어요?')
MK['t09']=T
speak('09',V+'v09.mp4',[(0,'v'),(1.8,'209'),(2.8,'v')],'네. 알겠습니다.|말씀하신 규정대로.|오늘 '+K('5시')+' 전에 올리겠습니다.')
speak('10',V+'v10.mp4',[(0,'v')],'흥. 어디 한번 봅시다.',tail=0.25)
speak('11',V+'v11.mp4',[(0,'v')],'다해쌤, 그거 절대|통과 안 시켜 줘요…',tail=0.2)
speak('12',V+'v12.mp4',[(0,'v'),(1.5,'212'),(2.4,'v')],'커피 한 잔 드시고 오세요.|'+K('40분')+'이면 됩니다.',tail=0.2)
# ================= S3 15:40 =================
MK['s3']=T; I3a=len(P)
add([(img('313',1.4,'in'),0,1.4),(img('o13',1.6,'in'),0,1.6)],ev=[(E+'sfx3/s18.mp3',0,0.7,'s',('cut',1.4)),(E+'sfx3/s19.mp3',1.4,0.55,'s',None),(E+'sfx2/arrive.mp3',1.4,0.2,'s',None),(E+'sfx3/s17a.mp3',-0.5,0.8,'s',None),(E+'sfx3/s17b.mp3',-0.15,0.8,'s',None)],subs=[(1.4,2.0,'{\\pos(470,680)\\frz-8}'+POP+'띵—','Ono'),(1.5,3.0,'{\\fs30}기안 = 결재를 올린 문서','N')])
inner('14',[(E+'x/r507.mp4',0.6,2.0)],'벌써?',off=0.3)
MK['drone']=T; EV.append((E+'sfx3/s20.mp3',T-1.3,0.8,'s',('cut',1.4)))
speak('15',V+'v15.mp4',[(0,'v'),(v0('15')+1.2,'215'),(v0('15')+2.2,'v')],'기안 올렸습니다.|직접 설명도|같이 드리겠습니다.')
speak('16',V+'v16.mp4',[(0,'v'),(1.8,'table','slow'),(3.3,'clip:r508')],'1차부터 6차까지,|교감 선생님 반려 사유를|한 장에 모았습니다.',tail=0.4)
# 17 with zoom rows: find word times
w17=TJ['17']['words']
def wt(words,key,default):
    for w,s,e in words:
        if key in w: return s
    return default
t5=wt(w17,'5',wt(w17,'오',3.8)); t2=wt(w17,'2',wt(w17,'이',6.5))
zoomrow('t3',t5,0.435,LC+'z3.mp4'); zoomrow('t5',t2-t5,0.66,LC+'z5.mp4')
segs=[(img('table',0.8,'in'),0,0.8),(img('c3',round(t5-0.8,3),'in'),0,round(t5-0.8,3)),(img('c5',round((t2-t5)*0.55,3),'in'),0,round((t2-t5)*0.55,3)),(img('c35',round((t2-t5)*0.45,3),'in'),0,round((t2-t5)*0.45,3)),(img('c26',1.0,'in'),0,1.0),(V+'v17.mp4',t2+1.0,round(v1('17')+0.12-t2-1.0,3))]
add(segs,[(AW('17'),0,1.0,'d',None)],chunks('3차엔 강사료를|운영비로 옮기라 하셨고,|5차엔 왜 옮겼냐며|반려하셨어요.|2차와 6차도,|서로 반대입니다.','17'),[(E+'sfx2/pen.mp3',0.15,0.7,'s',None),(E+'sfx2/pen.mp3',t5+0.05,0.7,'s',None)])
speak('18',V+'v18.mp4',[(0,'v')],'그, 그건 문맥이…',tail=0.2)
# 19 climax
w19=TJ['19']['words']; tg=wt(w19,'그런데',4.0); tk=hs
L19=v1('19')+0.12
B0,C0=3.45,9.4
MK['t19']=T
segs=[(V+'v19.mp4',0,2.5),(img('222',0.9),0,0.9),(E+'x/n19b.mp4',3.4-B0,1.9),(E+'x/r509.mp4',1.8,1.2),(E+'x/n19b.mp4',6.5-B0,round(tk-0.3-6.5,3)),(img('319',0.8,'crash'),0,0.8),(E+'x/n19c.mp4',tk+0.5-C0,round(L19-tk-0.5,3))]
add(segs,[(AW('19'),0,1.0,'d',None)],chunks("'반려'는|돌려보낸다는 뜻이죠.|고칠 길을 알려 주고요.|그런데 길을|여섯 번 바꿔 놓고,|왜 못 오냐고 하시면…|그건 반려가 아니라,|!H미로입니다.",'19',hit_at=wt(w19,'미로',v1('19')-1.0)),[(E+'sfx2/cap.mp3',tk-0.25,1.8,'d',None)])
FL.append(T-0.05); MK['after19']=T; EV.append((E+'sfx3/s22.mp3',T-0.05,0.8,'s',None))
add([(E+'x/r508.mp4',2.2,1.8)])
# 21
w21=TJ['21']['words']; tc=wt(w21,'공무원',5.0)
MK['t21']=T; EV.extend([(E+'sfx3/s21.mp3',T+4.1+k*0.45,0.25,'s',None) for k in range(3)])
speak('21',V+'v21.mp4',[(0,'v'),(0.9,'clip:n603'),(2.4,'clip:n604'),(3.9,'bars','slow'),(tc,'v'),(tc+1.4,'clip:r510'),(tc+2.6,'222'),(tc+3.4,'v')],'안 선생님 3주|초과근무 기록이,|반려 시각이랑|딱 겹치더라고요.|공무원 행동강령에|직무권한을 이용한|부당한 행위를|금지하는 조항이 있던데요.')
speak('22',V+'v22.mp4',[(0,'v')],'도, 독고 선생…',tail=0.2)
speak('23',V+'v23.mp4',[(0,'323'),(1.3,'v')],'5시 전에 결재해 주시면,|이 자료는 바로|파쇄하겠습니다.',tail=0.3)
t24=T
speak('24',V+'v24.mp4',[(0,'v'),(0.9,'o24','in'),(1.5,'v')],'승, 승인! '+K('승인')+'했어!',tail=0.2)
EV.extend([(E+'sfx2/click.mp3',t24+0.02+i*0.45,0.6,'s',None) for i in range(4)])
SUB.append((t24+0.02,t24+1.6,'{\\pos(500,860)\\frz-10}탁 탁 탁','Ono'))
MK['drone_end']=T; I3b=len(P)
# ================= S4 17:00 =================
add([(img('o25',1.8,'crash',tint=True),0,1.8),(img('225',1.3),0,1.3)],ev=[(E+'sfx3/s23.mp3',0.15,0.9,'s',None),(E+'sfx3/B3.mp3',0.0,1.0,'s',None)])
speak('26',V+'v26b.mp4',[(0,'v')],'다해쌤…|저녁은 제가 살게요.',tail=0.2)
add([(img('327',1.0,'in'),0,1.0)])
speak('27',V+'v27.mp4',[(0,'v')],'전 '+K('칼퇴')+'면 됩니다.',tail=0.2)
if WITH28:
    w28=TJ['28']['words']; tq=wt(w28,'끝까지',2.2)
    speak('28',V+'v28.mp4',[(0,'v'),(tq-0.1,'228'),(tq+1.3,'v')],'규정이 지켜 주는 게 아니에요.|끝까지 읽은 사람이|지키는 거지.',tail=0.3,extra=[(V+'v28.mp4',v1('28')+0.3,0.6)])
MK['song']=T
add([(E+'x/r513.mp4',0.3,2.6)],[(U+'g1s.wav',0.5,0.8,'d',None),(E+'sfx3/s24.mp3',0.0,0.9,'s',None)])
MK['end']=T
add([(img('poster2',3.0,'crash'),0,3.0)],[(E+'sfx3/s19.mp3',0.0,0.6,'s',None)])
total=T
SUB+=[(MK['t02']+0.1,MK['t02']+1.7,'교감','Tag'),(MK['t03']+0.1,MK['t03']+1.7,'안정우 · 생물 교사','Tag'),(MK['tag_dh'],MK['tag_dh']+2.2,'{\\fs46}독고다해 · 최저가 계약교사\\N{\\fs24}(극 중 설정)','Tag'),(MK['s3']+0.05,MK['s3']+1.4,'오후 3시 40분','Cap')]
EV.append((E+'sfx3/B1.mp3',MK['s1'],0.45,'s',('cut',MK['t08']+0.1-MK['s1'])))
EV.append((E+'sfx3/B2.mp3',MK['t09'],0.45,'s',('seek',0.0,MK['t19']+tk-0.8-MK['t09'])))
EV.append((E+'sfx3/B2.mp3',MK['after19']+1.8,0.45,'s',('seek',50.0,MK['drone_end']-MK['after19']-1.8)))
EV.append((M+'Orange_on_the_Floor.mp3',MK['song'],0.7,'s',('end',total-MK['song'])))
print('total',round(total,2),MK)
os.makedirs(E+'ed/seg',exist_ok=True); F=[]
CUM=0.0
for i,(f,s,dd) in enumerate(P):
    o=E+f'ed/seg/s{i:03d}.mp4'
    cf=",colorbalance=rs=-0.12:gs=-0.02:bs=0.1:rm=-0.08:bm=0.06,eq=saturation=0.88" if I3a<=i<I3b else ""
    n0=round(CUM*24); CUM+=dd; nf=max(1,round(CUM*24)-n0)
    run(['ffmpeg','-nostdin','-v','error','-y','-ss',str(max(0,s)),'-i',f,'-vf',"scale=720:1280,fps=24"+cf+",tpad=stop_mode=clone:stop_duration=1,format=yuv420p",'-frames:v',str(nf),'-an','-c:v','libx264','-preset','veryfast','-crf','19',o]); F.append(o)
open(E+'ed/seg/l.txt','w').write(''.join(f"file '{x}'\n" for x in F))
run(['ffmpeg','-nostdin','-v','error','-y','-f','concat','-safe','0','-i',E+'ed/seg/l.txt','-c','copy',E+'ed/pic.mp4'])
cmd=['ffmpeg','-nostdin','-v','error','-y']
for e in EV: cmd+=['-i',e[0]]
fl=''; dl=[]; sl=[]
for i,(f,at,v,k,tr) in enumerate(EV):
    ex=''
    if tr:
        if tr[0]=='trim': ex=f',atrim=0:{tr[1]:.3f},afade=t=in:d=0.8,afade=t=out:st={max(0,tr[1]-0.8):.3f}:d=0.8'
        if tr[0]=='seek': ex=f',atrim={tr[1]:.3f}:{tr[1]+tr[2]:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.3,afade=t=out:st={max(0,tr[2]-0.6):.3f}:d=0.6'
        if tr[0]=='cut': ex=f',atrim=0:{tr[1]:.3f},afade=t=in:d=0.6,afade=t=out:st={max(0,tr[1]-0.15):.3f}:d=0.15'
        if tr[0]=='end': ex=f',atrim=0:{tr[1]:.3f},afade=t=in:d=1.0,afade=t=out:st={tr[1]-2.5:.3f}:d=2.5'
    ms=max(0,int(round(at*1000)))
    fl+=f"[{i}:a]aformat=sample_rates=44100:channel_layouts=stereo{ex},volume={v},adelay={ms}|{ms},apad=whole_dur={total}[a{i}];"
    (dl if k=='d' else sl).append(f'[a{i}]')
fl+=''.join(dl)+f"amix=inputs={len(dl)}:normalize=0,asplit=2[D1][D2];"
fl+=''.join(sl)+f"amix=inputs={len(sl)}:normalize=0[SX];[SX][D2]sidechaincompress=threshold=0.015:ratio=10:attack=20:release=350[SD];"
fl+=f"[D1][SD]amix=inputs=2:normalize=0,atrim=0:{total}[out]"
cmd+=['-filter_complex',fl,'-map','[out]','-c:a','pcm_s16le',E+'ed/aud_pre.wav']; run(cmd)
import re as _re
_m=subprocess.run(['ffmpeg','-nostdin','-i',E+'ed/aud_pre.wav','-af','ebur128','-f','null','-'],capture_output=True,text=True).stderr
_I=float(_re.findall(r'I:\s+(-?[0-9.]+) LUFS',_m)[-1]); _g=-14.0-_I; print('pre I',_I,'gain',round(_g,2))
run(['ffmpeg','-nostdin','-v','error','-y','-i',E+'ed/aud_pre.wav','-af',f'volume={_g:.2f}dB,alimiter=limit=0.7:level=false:attack=1:release=50','-c:a','aac','-b:a','192k',E+'ed/aud.m4a'])
def ts(x): x=max(0,x); h=int(x//3600); m=int(x%3600//60); s=x%60; return f"{h}:{m:02d}:{s:05.2f}"
head=open(H+'/ep2/sub_v2_header.ass').read()
for a,b,txt,st in SUB: head+=f"Dialogue: 0,{ts(a)},{ts(b)},{st},,0,0,0,,{txt}\n"
open(E+'ed/sub.ass','w').write(head)
flash=','.join(f"drawbox=c=white@0.85:t=fill:enable='between(t,{x:.2f},{x+0.08:.2f})'" for x in FL)
SH='+'.join(f"between(t,{x:.2f},{x+0.25:.2f})" for x in HIT) or '0'
shake=f"crop=w=696:h=1256:x='12+11*sin(2*PI*t*26)*({SH})':y='12+11*cos(2*PI*t*21)*({SH})',scale=720:1280"
print('WARN long lines',WARN); print('HIT',HIT)
outn=E+('ed/ep2_v9A.mp4' if WITH28 else 'ed/ep2_v9B.mp4')
run(['ffmpeg','-nostdin','-v','error','-y','-i',E+'ed/pic.mp4','-i',E+'ed/aud.m4a','-vf',f"setpts=N/(24*TB),{flash},{shake},ass={E}ed/sub.ass:fontsdir={H}/fonts,fade=t=out:st={total-1.5:.2f}:d=1.5",'-c:v','libx264','-preset','veryfast','-crf','20','-c:a','copy','-shortest',outn])
print('ok',outn)
