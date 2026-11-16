# 교사X 수능 특별편 편집 v3 (14번 다시 녹음 14b·엔딩 1화 11/18 + v2: v1 + 사장님 순서 교감→다해→정우 + Gemini 지적 중 싼 것)
# 샌드박스: ~/ep3/{v(대사 vNN·반응 rNNN), img, ov, ed(aNN.wav), lc, timing.json}, ~/ep2/sfx3, ~/ed/usfx, ~/music, ~/fonts
import subprocess, os, json, re
from PIL import ImageFont
H='/home/user'; E=H+'/ep3/'; V=E+'v/'; A=E+'ed/'; IMG=E+'img/'; OV=E+'ov/'; LC=E+'lc/'; X=H+'/ep2/sfx3/'; U=H+'/ed/usfx/'; M=H+'/music/'
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
SP={'01':'DV','02':'DV','03':'DV','04':'DV','07':'DV','10':'DV','05':'DJ','16':'DJ'}
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
    if hit: out.append((off+e,off+b+0.35,POP+hit,'Hit'))
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
DH=['06','08','09','11','12','13','14','15','17']
for c in DH:
    run(['ffmpeg','-nostdin','-v','error','-y','-i',A+f'a{c}.wav','-af','equalizer=f=170:t=q:w=1.0:g=3,equalizer=f=3000:t=q:w=1.0:g=2.5,acompressor=threshold=0.08:ratio=3:attack=5:release=120:makeup=1.6',A+f'e{c}.wav'])
def AW(c): return A+(f'e{c}.wav' if c in DH else f'a{c}.wav')
# 훅 소리: 11번 '그런데'부터 끝까지
hs=wt('11','그런데',v1('11')-3.4)
run(['ffmpeg','-nostdin','-v','error','-y','-ss',str(max(0,hs-0.05)),'-to',str(v1('11')+0.15),'-i',AW('11'),A+'h11.wav'])
hd=round(v1('11')+0.2-hs,3)
# ================= 훅 (대사 자막 없음, 제목만) =================
add([(img('o506',0.7,'crash'),0,0.7),(V+'r409.mp4',0.5,1.0),(V+'v11.mp4',hs-0.05+1.7,round(hd-1.7,3))],
    [(A+'h11.wav',0,1.0,'d',None),(X+'B2.mp3',0,0.45,'s',('seek',50.0,hd))],
    [(0,hd,"{\\fad(200,0)}수능 감독은 이제\\N{\\alpha&HFF&\\t(430,440,\\alpha&H00&)\\fscx160\\fscy160\\t(430,600,\\fscx100\\fscy100)}"+YN+"대학에서{\\c&HFFFFFF&} 하시죠!",'HookT')],
    [(X+'s21.mp3',0.15,0.8,'s',None),(X+'s17b.mp3',0.65,0.6,'s',None)])
FL.append(T-0.08)
# ================= 교무실, 수능 전날 16:00 =================
MK['t01']=T
speak('01',[(0,'v'),(2.4,'o501'),(4.4,'v'),(6.2,'clip:r401@0.3'),(7.8,'v')],
      '봤지? 인터넷에|이런 썰까지 돈다.|단추 구멍에 카메라 달고|쌀알만 한 이어폰 끼면,|단돈 '+K('11만 원')+'에|AI가 수능을 대신 풀어 준대!',ev=[(X+'s17b.mp3',2.3,0.6,'s',None)])
speak('02',[(0,'v'),(2.5,'clip:r402@0.3'),(4.2,'v'),(6.4,'clip:r401@2.0'),(7.8,'v')],
      '얼마 전엔 국가 시험 수석이|AI로 커닝했다고|자수까지 했어.|내일 AI 안경, 블루투스 렌즈|하나라도 뚫리면|감독관이 '+K('독박')+' 쓰는 거야.')
t03=T; HIT.append(t03+wt('03','눈',4.6))
speak('03',[(0,'v'),(1.9,'507','crash'),(3.0,'v'),(4.3,'clip:r403@0.3'),(5.8,'v')],ev=[(X+'s16.mp3',1.9,0.8,'s',None)],text=
      '학부모 소송 들어오면|학교는 안 지켜 줘.|의자 생겼다고|앉아 졸 생각 말고,|매의 눈으로 서서 봐!')
speak('04',[(0,'v')],'우린 의자도 없었어.|요즘 선생들은…',tail=0.2)
MK['t06']=T
speak('06',[(0,'v'),(1.9,'503'),(3.1,'clip:r405@0.3'),(4.7,'v')],
      '네, 명심하겠습니다.|AI 스마트 기기 적발,|완벽하게 통제하죠.|매뉴얼대로.',tail=0.25)
MK['t05']=T
speak('05',[(0,'v'),(2.0,'o502'),(3.1,'v'),(5.4,'clip:r404@0.3'),(7.0,'v')],
      '3년 내내 입시 지도하느라|진 다 뺐는데…|내일은 '+K('8시간')+'씩 서서|감옥 간수를 해야 하네요…')
MK['b1_end']=T
# ================= 감독관실, 수능 날 07:40 =================
MK['s2']=T
add([(img('900',1.6,'in'),0,1.6)],ev=[(X+'s18.mp3',-0.4,0.6,'s',None)])
MK['t07']=T
add([(V+'v07.mp4',0,1.9),(img('o504',1.7,'in'),0,1.7),(V+'r406.mp4',0.3,1.5)],
    [(AW('07'),0.45,1.0,'d',None)],[(0.45,1.6,'다들 '+K('사인')+'해.','DV')],[(X+'s16.mp3',0.2,0.9,'s',None),(X+'s21.mp3',0.22,0.6,'s',None)])
FL.append(MK['t07']+0.22)
MK['t08']=T
speak('08',[(0,'v'),(2.4,'clip:r407@0.3'),(3.8,'505','crash'),(5.0,'v')],ev=[(X+'s21.mp3',3.8,0.5,'s',None)],text=
      '교감 선생님.|금속 탐지기 하나 들려 주고|2mm 카메라를|맨눈으로 잡아내라는 건,|'+"'감독'이 아니라|'"+K('기술 수사')+"'입니다.")
MK['t09']=T
speak('09',[(0,'v'),(2.2,'clip:r408@0.3'),(3.7,'v')],
      '교사 한 명에게|무한 책임을 지우는 이 각서는,|'+K('직권남용')+' 소지가 있죠.')
t10=T; HIT.extend([t10+0.05,t10+0.35])
speak('10',[(0,'v'),(2.6,'311','slow'),(3.6,'v')],'뭐, 뭐? 독고 선생,|수능이 장난이야?|대입이 걸렸어!',ev=[(X+'s21.mp3',0.0,0.8,'s',None)])
MK['t11']=T
th=wt('11','다',v1('11')-0.9,last=True)
speak('11',[(0,'v'),(2.0,'clip:r409@0.3'),(3.4,'v')],
      '대입이 걸렸죠.|국가가 치르는 시험입니다.|그런데 책임은 왜|교사 한 명한테|!H다 옵니까?',hit_at=th,ev=[(X+'s19.mp3',th-0.05,0.8,'s',None)])
FL.append(T-0.05); MK['after11']=T
t12=T
speak('12',[(0,'v')],'이 각서는 '+K('폐기')+'하시죠.',tail=0.1,
      extra=[(V+'v12.mp4',v1('12')+0.4,1.1),(img('o506',1.0,'in'),0,1.0),(V+'r409.mp4',2.2,1.2)],
      ev=[(X+'s17a.mp3',0.4,0.7,'s',None)])
tdrop=t12+v1('12')+0.1+1.1
EV.append((X+'s21.mp3',tdrop,0.9,'s',None)); EV.append((X+'B3.mp3',tdrop+0.1,0.8,'s',None))
MK['t13']=T
speak('13',[(0,'v'),(2.3,'clip:r410@0.3'),(3.8,'903','in'),(4.8,'v')],
      '감독 중 실수의 배상은|'+K('국가')+'가 합니다.|교사 개인이 지는 건|고의나 중대한 과실뿐이고요.')
speak('14',[(0,'v'),(2.2,'clip:r411@0.3'),(3.7,'v')],
      '안 선생님, 쫄지 마세요.|우리 교실로 가죠.|가서 떳떳하게|'+"'"+K('의자')+"'에 앉아서 감독합시다.")
speak('15',[(0,'v'),(2.3,'clip:r412@0.3'),(3.6,'v')],
      '안경은 기계가 못 잡아도,|애들 떠는 건|우리 눈에 보이니까.',tail=0.6,ev=[(X+'s20.mp3',v1('15')-0.2,0.6,'s',None)])
EV.append((X+'s24.mp3',T-0.1,0.8,'s',None)); MK['b2_end']=T
# ================= 시험실, 수능 날 17:45 =================
MK['s3']=T
add([(V+'r413.mp4',0.2,3.0)],[(U+'bell.mp3',0.0,0.5,'s',None)])
speak('16',[(0,'v'),(1.6,'clip:r414@0.3'),(2.7,'v')],'다해 선생님…|처음으로 앉아서 감독했어요.',tail=0.2)
a17=wt('17','퇴근',0.6)
speak('17',[(0,'5082','in'),(max(0.6,a17-0.2),'v')],K('퇴근')+' 시간 지났네요.',tail=0.25,a=a17)
MK['song']=T
add([(V+'r415.mp4',0.3,2.2)])
add([(img('factA',2.8,'slow'),0,2.8)],ev=[(X+'s17b.mp3',0.0,0.6,'s',None)])
add([(img('cheerB',2.4,'slow'),0,2.4)],ev=[(X+'s23.mp3',0.1,0.5,'s',None)])
MK['end']=T
add([(img('poster',3.0,'crash'),0,3.0)],[(X+'s19.mp3',0.0,0.5,'s',None)])
total=T
SUB+=[(MK['t01']+0.05,MK['t01']+1.7,'수능 전날 오후 4시','Cap'),(MK['t01']+4.5,MK['t01']+6.1,'교감','Tag'),
      (MK['t05']+0.1,MK['t05']+1.9,'안정우 · 생물 교사','Tag'),(MK['t06']+0.1,MK['t06']+1.85,'{\\fs40}독고다해 · 계약교사\\N{\\fs24}(극 중 설정)','Tag'),
      (MK['s2']+0.05,MK['s2']+1.55,'수능 날 아침 7시 40분','Cap'),(MK['s3']+0.1,MK['s3']+2.9,'수능 날 오후 5시 45분','Cap')]
EV.append((X+'B1.mp3',MK['t01'],0.4,'s',('cut',MK['b1_end']-MK['t01'])))
EV.append((X+'B2.mp3',MK['t09'],0.42,'s',('seek',0.0,MK['t11']+th-0.6-MK['t09'])))
EV.append((X+'B2.mp3',MK['t13'],0.4,'s',('seek',50.0,MK['b2_end']-MK['t13'])))
EV.append((M+'Orange_on_the_Floor.mp3',MK['song'],0.7,'s',('end',total-MK['song'])))
print('total',round(total,2),{k:round(v,2) for k,v in MK.items()})
os.makedirs(E+'ed/seg',exist_ok=True); F=[]; CUM=0.0
for i,(f,s,dd) in enumerate(P):
    o=E+f'ed/seg/s{i:03d}.mp4'
    n0=round(CUM*24); CUM+=dd; nf=max(1,round(CUM*24)-n0)
    run(['ffmpeg','-nostdin','-v','error','-y','-ss',str(max(0,s)),'-i',f,'-vf',"scale=720:1280,fps=24,tpad=stop_mode=clone:stop_duration=2,format=yuv420p",'-frames:v',str(nf),'-an','-c:v','libx264','-preset','veryfast','-crf','19',o]); F.append(o)
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
        if tr[0]=='end': ex=f',atrim=0:{tr[1]:.3f},afade=t=in:d=1.0,afade=t=out:st={tr[1]-2.5:.3f}:d=2.5'
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
head=open(H+'/ep2/sub_v2_header.ass').read().replace('\n\n[Events]','\nStyle: HookT,Black Han Sans,64,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,5,3,2,24,24,540,1\n\n[Events]',1)
for a,b,txt,st in SUB: head+=f"Dialogue: 0,{ts(a)},{ts(b)},{st},,0,0,0,,{txt}\n"
open(E+'ed/sub.ass','w').write(head)
flash=','.join(f"drawbox=c=white@0.85:t=fill:enable='between(t,{x:.2f},{x+0.08:.2f})'" for x in FL)
SH='+'.join(f"between(t,{x:.2f},{x+0.25:.2f})" for x in HIT) or '0'
shake=f"crop=w=696:h=1256:x='12+11*sin(2*PI*t*26)*({SH})':y='12+11*cos(2*PI*t*21)*({SH})',scale=720:1280"
print('WARN long lines',WARN); print('HIT',[round(h,2) for h in HIT])
outn=E+'ed/sn_v3.mp4'
run(['ffmpeg','-nostdin','-v','error','-y','-i',E+'ed/pic.mp4','-i',E+'ed/aud.m4a','-vf',f"setpts=N/(24*TB),{flash},{shake},ass={E}ed/sub.ass:fontsdir={H}/fonts,fade=t=out:st={total-1.5:.2f}:d=1.5",'-c:v','libx264','-preset','veryfast','-crf','20','-c:a','copy','-shortest',outn])
print('ok',outn)
