# 교사X 4화(쉽게 내요) 편집 v2 (v1 + 사장님 11/17: 15 '팔짜네' 다시 녹음·얼굴 다시 그림, 18 소리 키움(+6.5dB), 만화 효과(교감 놀람 '띠용', 다해 시계 반짝임). v1: build_ep3ot_v8.py 틀. 회당 2분 내외, 바이럴 기준 매뉴얼 8-1)
# 샌드박스: ~/ep5/{v(vNN·rNNN), img, ov, ed(aNN.wav), lc, timing.json}, ~/ep2/sfx3, ~/ed/usfx, ~/music, ~/fonts
import subprocess, os, json, re
from PIL import ImageFont
H='/home/user'; E=H+'/ep5/'; V=E+'v/'; A=E+'ed/'; IMG=E+'img/'; OV=E+'ov/'; LC=E+'lc/'; X=H+'/ep2/sfx3/'; U=H+'/ed/usfx/'; M=H+'/music/'
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
SP={'06':'DV','08':'DV','09':'DV','11':'DV','13':'DV','15':'DV','16':'DV','01':'DJ','03':'DJ','05':'DJ','07':'DJ','10':'DJ','18':'DJ'}
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
DH=['02','04','12','14','17']
for c in DH:
    run(['ffmpeg','-nostdin','-v','error','-y','-i',A+f'a{c}.wav','-af','equalizer=f=170:t=q:w=1.0:g=3,equalizer=f=3000:t=q:w=1.0:g=2.5,acompressor=threshold=0.08:ratio=3:attack=5:release=120:makeup=1.6',A+f'e{c}.wav'])
def AW(c): return A+(f'e{c}.wav' if c in DH else f'a{c}.wav')
# v2: 18은 다른 줄보다 약 6dB 작음(측정 -31.8 vs -25 LUFS) → 키워서 e18
run(['ffmpeg','-nostdin','-v','error','-y','-i',A+'a18.wav','-af','volume=6.5dB,acompressor=threshold=0.1:ratio=2.5:attack=5:release=120',A+'e18.wav'])
DH.append('18')
U2=H+'/ed/usfx/'  # 사장님이 준 '띠용' 효과음(boing1 낮음·boing2 높음)
LEAD=0.5
# 훅 소리: 08번 전체(훅 문장 = 08, 사장님 11/16). 0초 무음(키보드 소리 없음, v3) 뒤 0.5초에 말 시작
hs=max(0,v0('08')-0.05)
run(['ffmpeg','-nostdin','-v','error','-y','-ss',str(hs),'-to',str(v1('08')+0.15),'-i',AW('08'),'-af',f'afade=t=in:d=0.03,adelay={int(LEAD*1000)}:all=1',A+'h08.wav'])
hd=round(v1('08')+0.25-hs+LEAD,3)
# ================= 훅: 밤, 문항 삭제 → 교감의 말 (대사 자막 없음, 제목만) =================
add([(V+'r606.mp4',1.2,1.0),(img('o605d',1.3,'in'),0,1.3),(V+'v08.mp4',round(2.3-LEAD+hs,3),round(hd-2.3,3))],
    [(A+'h08.wav',0,1.0,'d',None),(X+'B2.mp3',0,0.22,'s',('seek',50.0,hd))],
    [(0,hd,"{\\fad(200,0)}미이수 막으려고\\N{\\alpha&HFF&\\t(430,440,\\alpha&H00&)\\fscx160\\fscy160\\t(430,600,\\fscx100\\fscy100)}"+YN+"시험을 쉽게?",'HookT')],
    [(X+'s23.mp3',1.0,0.5,'s',None)])  # v3: 훅 키보드 소리 뺌(사장님 11/17), [삭제] 쿵만
pass  # v4: 장면 전환 흰 번쩍임 뺌(사장님 11/17), 시계 반짝임만 남김
# ================= 1. 방과후 보충교실 =================
MK['s1']=T
add([(V+'r601.mp4',0.3,1.4)])
add([(img('o602',1.6,'in'),0,1.6)],ev=[(X+'s17b.mp3',0.1,0.5,'s',None)])
add([(img('603',0.8,'in'),0,0.8)],ev=[(X+'s18.mp3',0.0,0.5,'s',None)])
MK['t01']=T
speak('01',[(0,'v')],'하… 오늘도… 안 오네.',tail=0.2)
MK['b1_mid']=T
# ================= 2. 교무실 서류 더미 =================
add([(img('o604',1.2,'in'),0,1.2)])
MK['t02']=T
speak('02',[(0,'v')],'학생은 안 왔는데,|서류는 다 왔네요.')
speak('03',[(0,'v'),(2.2,'o604','slow'),(3.6,'v')],'안 온 것도 증명해야 해서요.|통화 기록, 문자 캡처,|사유서까지.')
speak('04',[(0,'v')],'그 서류, 누가 다 읽어요?',tail=0.15)
speak('05',[(0,'v')],'…감사 나올 때요.',tail=0.3)
MK['b1_end']=T
# ================= 3. 교감의 부탁 =================
MK['t06']=T
speak('06',[(0,'v')],'안 선생, 통합과학|기말 문제 다 냈죠?')
speak('07',[(0,'v')],'네, 내일 검토 올리겠습니다.')
MK['t08']=T
speak('08',[(0,'v'),(2.2,'clip:r501@0.2'),(3.8,'v')],'너무 어렵게 내지 마요.|'+K('미이수')+' 많이 나오면,|이 동네 소문 무서운 거 다 알죠.')
speak('09',[(0,'clip:r502@2.0'),(1.2,'v'),(2.6,'clip:r505@0.3'),(4.0,'v')],'소문나면 내년|'+K('신입생 모집')+' 어렵고,|모집 안 되면…|재단이 나를 가만 안 둬.')  # v5: 08 끝~09 앞 교감 4초 연속 → 09 첫 1.2초를 정우 반응으로(사장님 11/17)
speak('10',[(0,'v')],'그래도 평가 기준이 있는데…',tail=0.2)
speak('11',[(0,'v'),(2.0,'clip:r504@0.3'),(3.6,'v')],'기준은 지키면서, 쉽게.|안 선생은 할 수 있잖아.')
# ================= 4. 다해의 두 수 앞 =================
speak('12',[(0,'v')],'쉽게 내면,|이번엔 '+K('다른 쪽')+'에서 소문나요.')
speak('13',[(0,'v')],'다른 쪽?',tail=0.35,ev=[(U2+'boing1.mp3',0.0,0.55,'s',None)])
MK['t14']=T
h14=wt('14','등급',v1('14')-2.5)-0.25
speak('14',[(0,'v'),(2.0,'clip:r503@0.3'),(3.3,'v')],'만점자가 열 명 중|한 명을 넘으면,|!H1등급이 한 명도\\N안 나올 수 있거든요.',hit_at=h14,ev=[(X+'s19.mp3',h14-0.05,0.7,'s',None),(U2+'boing2.mp3',2.0,0.5,'s',None)])
HIT.append(MK['t14']+h14)
speak('15',[(0,'v')],'에이, 우리 애들이|그렇게 잘 봐?|걱정도 팔자네.')
speak('16',[(0,'v'),(1.7,'clip:r502@0.3')],'안 선생, 쉽게. 알죠?',tail=0.3)
FL.append(T+0.42)
add([(img('o608a',0.4,'in'),0,0.4),(img('o608b',0.5,'in'),0,0.5),(V+'r506.mp4',0.2,1.6)],ev=[(X+'s18.mp3',0.0,0.4,'s',None)])  # v2: 시계 반짝임
MK['t17']=T
h17=wt('17','열심',v1('17')-2.5)
speak('17',[(0,'v'),(2.6,'clip:r507@0.05'),(3.3,'v')],'안 선생님.|시험도 학습의 일부예요.|!H열심히 공부한 학생을\\N배신하지 말아요.',hit_at=h17,tail=0.3)
MK['b2_end_day']=T
# ================= 5. 밤 =================
MK['song']=T; MK['s5']=T
add([(V+'r508.mp4',0.2,1.6)],ev=[(X+'s18.mp3',0.0,0.45,'s',None)])
add([(img('o607',1.8,'in'),0,1.8)],ev=[(X+'s17b.mp3',0.1,0.5,'s',None)])
add([(V+'r509.mp4',0.3,1.6)])
add([(V+'r606.mp4',1.0,0.6),(img('o605d',1.0,'crash'),0,1.0)],ev=[(X+'s26.mp3',0.25,0.8,'s',None),(X+'s23.mp3',0.65,0.6,'s',None)])
pass  # v4: 흰 번쩍임 뺌
MK['t18']=T
speak('18',[(0,'v')],'…이러면 다 통과는 하겠지.',tail=0.4)
MK['b2_end']=T
add([(img('poster',1.8,'crash'),0,1.8)],[(X+'s19.mp3',0.0,0.5,'s',None)])
total=T
SUB+=[(MK['s1']+0.05,MK['s1']+2.6,'방과후 보충교실 · 오후 4시 30분','Cap'),
      (MK['t01']+0.1,MK['t01']+1.9,'안정우 · 통합과학 교사','Tag'),
      (MK['t02']+0.1,MK['t02']+1.9,'{\\fs40}독고다해 · 계약교사\\N{\\fs24}(극 중 설정)','Tag'),
      (MK['t06']+0.1,MK['t06']+1.9,'교감','Tag'),
      (MK['t14']+0.3,MK['t14']+5.2,'고1 공통과목 5등급제: 1등급 = 상위 10%','Cap'),
      (MK['s5']+0.05,MK['s5']+1.5,'밤 9시','Cap')]
EV.append((X+'B1.mp3',MK['s1'],0.35,'s',('cut',MK['b1_end']-MK['s1'])))
EV.append((X+'B2.mp3',MK['t06'],0.4,'s',('seek',0.0,MK['b2_end_day']-MK['t06'])))
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
outn=E+'ed/ep4_v5.mp4'
run(['ffmpeg','-nostdin','-v','error','-y','-i',E+'ed/pic.mp4','-i',E+'ed/aud.m4a','-vf',f"setpts=N/(24*TB),{flash},{shake},ass={E}ed/sub.ass:fontsdir={H}/fonts,fade=t=out:st={total-0.6:.2f}:d=0.6",'-c:v','libx264','-preset','veryfast','-crf','20','-c:a','copy','-shortest',outn])
print('ok',outn)
_lw=MK['b2_end']-0.4  # 18 꼬리 0.4 빼면 말 끝
_cuts=subprocess.run(['ffmpeg','-i',outn,'-vf',"select='gt(scene,0.2)',showinfo",'-an','-f','null','-'],capture_output=True,text=True).stderr.count('pts_time:')
print(f"""[편집장 측정값]
전체 길이: {total:.1f}초 / 컷 수: {_cuts} / 평균 컷 길이: {total/max(1,_cuts+1):.1f}초
마지막 대사 끝: {_lw:.1f}초 / 그 뒤 말 없는 구간: {total-_lw:.1f}초
첫 대사 시작: {LEAD:.2f}초 / 훅 첫 화면: 키 누름(소리 없음)→[삭제] 모니터+쿵
표시 위치: 극 중 설정·인물 소개 = 왼쪽 위
자막 겹침: {len(OV)}건""")
