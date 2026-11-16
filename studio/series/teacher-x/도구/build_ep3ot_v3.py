# 교사X 3화(야근 강요) 편집 v3 (v2 + 사장님 11/16: 젊어 보이는 교감 컷 04·407·603 빼거나 덮음, 훅 첫 소리 잘림, Gemini 효과음 일부. v2: 12번 자막 나눔. 수능 특별편 build_sn_v3.py 틀)
# 샌드박스: ~/ep4/{v(vNN·rNNN), img, ov, ed(aNN.wav), lc, timing.json}, ~/ep2/sfx3, ~/ed/usfx, ~/music, ~/fonts
import subprocess, os, json, re
from PIL import ImageFont
H='/home/user'; E=H+'/ep4/'; V=E+'v/'; A=E+'ed/'; IMG=E+'img/'; OV=E+'ov/'; LC=E+'lc/'; X=H+'/ep2/sfx3/'; U=H+'/ed/usfx/'; M=H+'/music/'
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
SP={'01':'DV','02':'DV','04':'DV','06':'DV','09':'DV','11':'DV','13':'DV','14':'DV','03':'DJ','17':'DJ'}
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

# 세그먼트별 색 처리(회상 바랜 색)
FX={V+'r602.mp4':",eq=saturation=0.35:brightness=-0.02,curves=r='0/0.06 1/0.98':g='0/0.03 1/0.9':b='0/0 1/0.75',gblur=sigma=0.6"}
DH=['05','07','08','10','12','15','16']
for c in DH:
    run(['ffmpeg','-nostdin','-v','error','-y','-i',A+f'a{c}.wav','-af','equalizer=f=170:t=q:w=1.0:g=3,equalizer=f=3000:t=q:w=1.0:g=2.5,acompressor=threshold=0.08:ratio=3:attack=5:release=120:makeup=1.6',A+f'e{c}.wav'])
def AW(c): return A+(f'e{c}.wav' if c in DH else f'a{c}.wav')
# 훅 소리: 12번 '교장'부터 끝까지
hs=wt('12','교장',v1('12')-3.4)
run(['ffmpeg','-nostdin','-v','error','-y','-ss',str(max(0,hs-0.3)),'-to',str(v1('12')+0.15),'-i',AW('12'),'-af','afade=t=in:d=0.04',A+'h12.wav'])
hd=round(v1('12')+0.5-hs,3)
# ================= 훅: 밤 9시 혼자 문단속 (대사 자막 없음, 제목만) =================
add([(img('505',0.9,'crash'),0,0.9),(V+'r601.mp4',0.6,round(hd-0.9,3))],
    [(A+'h12.wav',0,1.0,'d',None),(X+'B2.mp3',0,0.4,'s',('seek',50.0,hd))],
    [(0,hd,"{\\fad(200,0)}야근시키려면\\N{\\alpha&HFF&\\t(430,440,\\alpha&H00&)\\fscx160\\fscy160\\t(430,600,\\fscx100\\fscy100)}"+YN+"사유부터{\\c&HFFFFFF&} 쓰시죠!",'HookT')],
    [(X+'s21.mp3',0.1,0.7,'s',None)])
FL.append(T-0.08)
# ================= 씬 1 월요일 아침 회의 08:30 =================
MK['t01']=T
speak('01',[(0,'v'),(2.6,'clip:r401@0.3'),(4.2,'v')],'올해 새로 온 선생님들,|당분간 저녁 '+K('9시')+'까지 남으세요.|문단속까지 하고 퇴근하고.')
speak('02',[(0,'v'),(2.4,'clip:r402@0.3'),(4.0,'v')],'요즘 선생들은|5시 땡 하면 사라져.|'+K('기강')+'이 없어, 기강이.')
MK['t03']=T
speak('03',[(0,'v'),(2.4,'clip:r401@2.0')],'저… 남아서|무슨 일을 하면 될까요?',tail=0.15)
speak('04',[(0,'clip:r403@0.3')],'할 일이야 찾으면 나오지.',tail=0.15)
MK['t05']=T
speak('05',[(0,'v'),(2.0,'clip:r403@2.3')],'교감 선생님.|남으라는 건, '+K('명령')+'이시죠?',tail=0.2)
HIT.append(T+0.05)
speak('06',[(0,'v')],'그래, 명령이야!',tail=0.2,ev=[(X+'s21.mp3',0.0,0.6,'s',None)])
speak('07',[(0,'v'),(2.2,'clip:r404@0.3')],'알겠습니다.|그럼 오늘 '+K('초과근무 신청')+',|미리 올리겠습니다.',tail=0.25)
MK['b1_end']=T
# ================= 씬 2 오후 5시 =================
MK['s2']=T
add([(img('501',1.5,'in'),0,1.5)],ev=[(X+'s18.mp3',-0.3,0.55,'s',None)])
MK['t08']=T
speak('08',[(0,'v'),(2.3,'o502','in'),(3.7,'clip:r405@0.3')],'초과근무 신청서입니다.|'+K('사유')+' 칸만 비워 뒀어요.|뭐라고 쓸까요?',ev=[(X+'s17b.mp3',2.2,0.5,'s',None),(X+'s26.mp3',2.4,0.5,'s',('cut',1.3))])
speak('09',[(0,'v')],'문단속이라고 써!',tail=0.15)
MK['t10']=T
speak('10',[(0,'v'),(2.3,'504','in'),(3.5,'clip:r406@0.3'),(5.0,'v')],'문단속은 선생님 업무에서|빠진 지 오래예요.|지금은 당직 기사님과|경비 시스템이 하죠.')
HIT.append(T+0.05)
speak('11',[(0,'v')],'그, 그럼…|신규 교사 '+K('기강 확립')+'!',tail=0.15)
MK['t12']=T
th=wt('12','이름',v1('12')-1.4)
speak('12',[(0,'v'),(2.4,'clip:r406@0.3'),(3.8,'clip:r408@0.3'),(5.1,'o503','in'),(6.4,'v')],
      '좋습니다.|올해 온 교사만,|기강 잡으려고,|밤 9시까지.|이 결재,|'+K('교장')+' 선생님까지 올라갑니다.|!H교감 선생님 이름으로요.',hit_at=th,
      ev=[(X+'s19.mp3',th-0.05,0.8,'s',None),(X+'s17b.mp3',5.0,0.5,'s',None),(X+'s23.mp3',5.3,0.8,'s',None)])
FL.append(T-0.05); MK['after12']=T
speak('13',[(0,'v')],'그, 그건…',tail=0.15)
MK['t14']=T
speak('14',[(0,'v'),(2.6,'clip:r409@0.3'),(3.9,'v')],'나 1년 차 땐 '+K('숙직')+'까지 섰어!|요즘 선생들은|좋은 시절 만나서…',tail=0.15)
add([(V+'r409.mp4',2.0,0.6)])
MK['t15']=T
speak('15',[(0,'v'),(2.3,'clip:r410@0.3')],'그때도 잘못이었어요.|그걸 '+K('물려주시면')+' 안 되죠.',tail=0.4)
speak('16',[(0,'v')],'안 선생님, '+K('퇴근')+'하시죠.',tail=0.2)
speak('17',[(0,'v')],'…네!',tail=1.0,ev=[(X+'B3.mp3',0.5,0.7,'s',None)])
MK['b2_end']=T
# ================= 씬 3 밤 9시 (대사 없음) =================
MK['song']=T; MK['s3']=T
add([(V+'r601.mp4',0.2,3.4)],ev=[(X+'s24.mp3',3.2,0.5,'s',None)])
add([(V+'r602.mp4',0.3,3.6)])
MK['end']=T
add([(img('poster',3.0,'crash'),0,3.0)],[(X+'s19.mp3',0.0,0.5,'s',None)])
total=T
SUB+=[(MK['t01']+0.05,MK['t01']+1.7,'월요일 아침 8시 30분','Cap'),(MK['t01']+0.5,MK['t01']+2.4,'교감','Tag'),
      (MK['t03']+0.1,MK['t03']+1.9,'안정우 · 생물 교사 (올해 전입)','Tag'),(MK['t05']+0.1,MK['t05']+1.9,'{\\fs40}독고다해 · 계약교사 (올해 부임)\\N{\\fs24}(극 중 설정)','Tag'),
      (MK['s2']+0.05,MK['s2']+1.45,'오후 5시','Cap'),(MK['s3']+0.1,MK['s3']+2.4,'밤 9시','Cap'),(MK['s3']+3.5,MK['s3']+6.4,'{\\i1}(1990년대, 교감의 1년 차){\\i0}','Cap')]
EV.append((X+'B1.mp3',MK['t01'],0.4,'s',('cut',MK['b1_end']-MK['t01'])))
EV.append((X+'B2.mp3',MK['t08'],0.42,'s',('seek',0.0,MK['t12']+th-0.6-MK['t08'])))
EV.append((M+'Orange_on_the_Floor.mp3',MK['song'],0.6,'s',('end',total-MK['song'])))

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
outn=E+'ed/ep3ot_v3.mp4'
run(['ffmpeg','-nostdin','-v','error','-y','-i',E+'ed/pic.mp4','-i',E+'ed/aud.m4a','-vf',f"setpts=N/(24*TB),{flash},{shake},ass={E}ed/sub.ass:fontsdir={H}/fonts,fade=t=out:st={total-1.5:.2f}:d=1.5",'-c:v','libx264','-preset','veryfast','-crf','20','-c:a','copy','-shortest',outn])
print('ok',outn)
