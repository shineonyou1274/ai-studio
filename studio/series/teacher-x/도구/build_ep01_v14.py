# 교사X 1화 최종본 v9 편집 스크립트 (샌드박스 ~/ed 에서 실행, 2026-11-13). 2026-11-14 저장소로 옮김(샌드박스 24시간 삭제 대비).
# 주의(2화에서 찾은 것): 조각 concat copy 뒤 시간 표시 밀림 가능 → 다시 쓸 때 마지막 단계에 setpts=N/(24*TB). loudnorm 동적 대신 전체 한 비율 권장(2화 patch_v7_to_v8 15번).
import subprocess, os
H=os.path.expanduser('~'); C=H+'/ins/clips/'; V=H+'/ed/v/'; A=H+'/ed/a/'; S=H+'/ed/sfx/'; L=H+'/ed/l/'; M=H+'/music/'
def run(c): subprocess.run(c,check=True)
def mk(img,out,d,z,x,y):
    run(['ffmpeg','-nostdin','-v','error','-y','-loop','1','-i',img,'-vf',f"scale=1440:2560,zoompan=z='{z}':x='{x}':y='{y}':d={int(round(d*24))}:s=720x1280:fps=24,format=yuv420p",'-t',str(d),'-c:v','libx264','-preset','veryfast','-crf','19',out])
mk(L+'A.png','lc/A2.mp4',2.0,'1.05+0.002*on','iw*0.5-(iw/zoom/2)','ih*0.45-(ih/zoom/2)')
mk(H+'/ins/o04.png','lc/C04M.mp4',4.1,'1.25','iw/2-(iw/zoom/2)+6*sin(on*2.2)','ih*0.55-(ih/zoom/2)+4*sin(on*3.1)')
mk('black.png','lc2/BLK3.mp4',0.3,'1','0','0')
mk('black.png','lc2/BLK8.mp4',0.8,'1','0','0')
for n in ('E2','E3'): run(['ffmpeg','-nostdin','-v','error','-y','-i',f'lc2/{n}.mp4','-vf','setpts=2.0*PTS','-c:v','libx264','-preset','veryfast','-crf','19',f'lc2/{n}s.mp4'])
run(['ffmpeg','-nostdin','-v','error','-y','-i',C+'c35.mp4','-vf','fade=t=out:st=2.5:d=0.5','-c:v','libx264','-preset','veryfast','-crf','19','lc2/c35f.mp4'])
mk(L+'B.png','lc/B4.mp4',1.5,'1.2+0.003*on','iw*0.5-(iw/zoom/2)','ih*0.27-(ih/zoom/2)')
mk(H+'/ins/p32.png','lc2/K32.mp4',2.6,'1.1+0.002*on','iw/2-(iw/zoom/2)+3*sin(on*5)','ih/2-(ih/zoom/2)+2*sin(on*6.3)')
mk('poster.png','lc2/POSTER3.mp4',3.0,'1+0.0005*on','iw/2-(iw/zoom/2)','ih/2-(ih/zoom/2)')
# split audio for breath pauses
run(['ffmpeg','-nostdin','-v','error','-y','-i',A+'c17.mp3','-t','7.20',A+'c17a.wav']); run(['ffmpeg','-nostdin','-v','error','-y','-ss','7.20','-i',A+'c17.mp3',A+'c17b.wav'])
run(['ffmpeg','-nostdin','-v','error','-y','-i',A+'c31.mp3','-t','9.95',A+'c31a.wav']); run(['ffmpeg','-nostdin','-v','error','-y','-ss','9.95','-i',A+'c31.mp3',A+'c31b.wav'])
P=[]; E=[]; SUB=[]; FL=[]; T=0.0; MARK={}
def blk(segs,au=(),subs=(),ev=()):
    # au: (file, offset, vol, kind)  kind d=dialogue s=sfx
    global T
    for f,o,v,k in au: E.append((f,T+o,v,k,None))
    for s in segs: P.append(s)
    for a,b,txt,st in subs: SUB.append((T+a+0.08,T+b,txt,st))
    for f,o,v,k,trim in ev: E.append((f,T+o,v,k,trim))
    T+=sum(s[2] for s in segs)
d=lambda f,o=0,v=1: (A+f,o,v,'d')
# ---------- part 1 ----------
hk0=T
blk([('lc2/E2s.mp4',0,1.83),('lc2/E3s.mp4',0,1.58)],[d('c17b.wav',0.1)],[(-0.08,3.4,'{\\fad(300,0)}야외수업 결재받으라는 교감에게\\N{\\c&H0078E0FF&}대처하는 방법','HookT'),(0.1,3.4,'교감 선생님의 결재 대상이 아닙니다.','D')])
E.append((H+'/ep2/sfx3/B2.mp3',0,0.45,'b',('seek',50.0,T)))
blk([('lc2/BLK8.mp4',0,0.8)],subs=[(-0.08,0.8,'그날 아침','Card')],ev=[(H+'/ep2/sfx3/s26.mp3',0.05,0.5,'s',('seek',0.0,0.6))])
MARK['b03']=T
blk([(V+'v03.mp4',0,1.55),('lc/A2.mp4',0,2.0),(V+'v03.mp4',3.55,1.55)],[d('c03.mp3',-0.35)],[(0,1.4,'정서교육 우수사례,','D'),(1.58,4.55,'오늘 5시까지 교장 결재까지 받아서 내세요.','D')])
blk([('lc/C04M.mp4',0,4.1)],[d('i04r.wav',0.7,1.8)],[(0.7,4.0,'실적 미달 명단…? 이번엔 무조건 우수사례다.','In')],[(S+'buzz2.wav',0.0,0.2,'s',None)])
MARK['office']=T
blk([(C+'c05.mp4',0,2.9),('lc/D05.mp4',0,1.1)],[(A+'c05t.wav',0,1.6,'d')],[(0,1.7,'(수군) 저 사람이 그 최저가래.','D'),(1.74,2.9,'(수군) 최저가?','D')])
MARK['b06']=T
blk([(V+'v06.mp4',0.3,1.5)],[d('c06.mp3',-0.3)],[(-0.3,1.25,'…다해쌤?','D')])
blk([(C+'c07.mp4',0,2.0)],ev=[(S+'click.wav',0.2,0.4,'s',None)])
MARK['drone']=T
blk([(V+'v08.mp4',0,1.6),('lc/B1.mp4',0,1.4),(V+'v08.mp4',3.0,1.6),(V+'v08.mp4',4.6,1.3),('lc/B2.mp4',0,0.6)],[d('c08.mp3')],[(0,2.8,'밖에서? 애들 데리고 놀러 가는 거 아닙니까?','D'),(2.97,5.81,'계획서, 안전점검표, 결재 세 단계 받아 오세요.','D')])
blk([(V+'v09.mp4',0,2.6)],[d('c09.mp3')],[(0,2.04,'(속삭이며) 에듀파인으로 올리시면 되는데…','D')])
blk([(V+'v10.mp4',0,2.4),('lc/B4.mp4',0,1.5)],[d('c10.mp3')],[(0,2.38,'올리기 전에 출력해서 먼저 들고 와요.','D'),(2.68,3.46,'그게 순서지.','D')])
blk([(C+'c14.mp4',0,1.2),(C+'c11.mp4',0.4,2.8)],[d('i11r.wav',0.15,1.8)],[(0.15,3.85,'결재판은 서랍에. 3교시 전엔 절대 못 나가.','In'),(1.2,3.95,'{\\an8\\pos(360,400)\\fad(150,150)}교감 책상 서랍 속\\N다해의 야외 수업 계획서 (결재 안 함)','Note')],[(S+'thud.wav',3.85,0.5,'s',None)])
MARK['office_end']=T
blk([(V+'v12.mp4',0,1.9),('lc/C1.mp4',0,1.2),(V+'v12.mp4',3.1,1.8),('lc/C2.mp4',0,1.0),(V+'v12.mp4',5.9,0.7)],[d('c12.mp3')],[(0,2.93,'3교시 전까지 결재 안 나면 무단 수업이에요.','D'),(3.23,6.18,'최저가로 들어오신 분이, 재계약 생각은 하셔야지.','D')])
blk([(C+'c13.mp4',0,2.5)])
blk([(C+'c14.mp4',0,3.7),(C+'c11.mp4',2.5,1.2),('lc/K14.mp4',0,2.0)],[d('i14r.wav',1.8,1.8)],[(1.8,6.8,'흐흐… 종 쳤네. 결재판은 여기 있고… 밖에서 수업은 무슨.','In')],[(H+'/ed/usfx/bell.mp3',0,0.25,'s',None)])
MARK['birds']=T
blk([(C+'c15.mp4',0,1.5)])
MARK['t16']=T
# ---------- part 2 ----------
blk([(V+'v16.mp4',0,1.3),('lc2/D1.mp4',0,0.9),(V+'v16.mp4',2.2,1.2)],[d('c16.mp3')],[(0,0.86,'독고 선생!','D'),(1.3,3.1,'이건 무단 야외 수업이에요!','D')],[(H+'/ed/usfx/run_cut.wav',0,0.5,'s',None)])
t17=T
blk([(V+'v17.mp4',0,1.9),('lc2/E1.mp4',0,1.2),(V+'v17.mp4',3.1,1.9),('lc2/E2.mp4',0,0.9),(V+'v17.mp4',5.9,1.3),('lc2/D1.mp4',0,0.9),(V+'v17.mp4',7.7,0.9),('lc2/E3.mp4',0,0.8),(V+'v17.mp4',9.4,1.4)],
 [d('c17a.wav'),d('c17b.wav',7.6)],
 [(0,1.85,'안 나갔습니다. 지적도상, 여기는.','D'),(1.86,4.0,'학교 담장 안. 교내 부지입니다.','D'),(4.1,5.3,'교실 밖일 뿐이죠.','D'),(5.5,7.2,"'교문 밖 야외 수업'이 아니니,",'D'),(7.6,10.5,'교감 선생님의 결재 대상이 아닙니다.','D')],
 [])
FL.append(t17+10.5)
blk([(C+'c18.mp4',0,2.0)],ev=[(S+'comicdown.wav',0.1,0.7,'s',None)])
blk([(V+'v19.mp4',0,1.6),('lc2/D2.mp4',0,0.8),(V+'v19.mp4',2.4,1.5)],[d('c19.mp3')],[(0,3.5,'쌤, 이 꽃은 왜 가운데가 노란색이에요?','D')])
blk([(V+'v20.mp4',0,1.8),('lc2/D1.mp4',0,0.6),(V+'v20.mp4',2.4,1.6)],[d('c20.mp3')],[(0,3.55,'어? 어… 그건 수술이라고, 꽃가루를…','D')])
blk([(C+'c21.mp4',0,2.5)],ev=[(S+'buzz2.wav',0.2,0.2,'s',None)])
blk([(V+'v22.mp4',0,2.4)],[d('c22.mp3')],[(0,1.7,'(작게) …사진이 하나도 없는데.','D')])
t23=T
blk([(V+'v23.mp4',0,2.7),('lc2/F1.mp4',0,1.0),(V+'v23.mp4',3.7,1.7),('lc2/F2.mp4',0,0.9),(V+'v23.mp4',6.3,2.5),('lc2/E3.mp4',0,0.8)],[d('c23.mp3')],
 [(0,2.7,"'우수(優秀)'는 여럿 중에 뛰어나다는 뜻입니다.",'D'),(2.76,6.6,'사방이 벽으로 막힌 교실 안에서 한 발짝도 못 나간 수업이,','D'),(6.68,8.8,'뛰어난 사례가 될 수는 없죠.','D')],
 [(S+'click.wav',0.4,0.4,'s',None)])
FL.append(t23+8.8); MARK['t23e']=t23+8.8
blk([(V+'v24.mp4',0,1.5),('lc2/N25.mp4',0,0.8),(V+'v24.mp4',2.3,0.9)],[d('c24.mp3')],[(0,2.65,'사진… 좀 찍어도 되겠습니까.','D')])
blk([(V+'v25.mp4',0,1.7),(V+'v24.mp4',3.3,0.7),(V+'v25.mp4',2.4,1.2)],[d('c25.mp3')],[(0,1.64,'아이들 얼굴은 안 됩니다.','D'),(1.94,3.0,'시(詩)만 찍으세요.','D')])
MARK['c26']=T
blk([(C+'c26.mp4',0,1.8)],ev=[(H+'/ed/usfx/camera.mp3',1.55,0.6,'s',None)])
blk([('lc/C27N.mp4',0,4.0)],subs=[(0.2,4.0,'교실에선 숨이 막혔는데,\\N꽃 앞에선 말이 나왔다.','Poem')])
blk([('lc2/c28f.mp4',0,3.0)],[d('i28r.wav',1.0,1.8)],[(1.0,2.6,'…언니.','In')],[(S+'wind.wav',0,0.8,'s',None)])
MARK['birds_end']=T
MARK['b29']=T
blk([(V+'v29.mp4',0,1.8),('lc2/G1.mp4',0,1.0),(V+'v29.mp4',2.8,1.2)],[d('c29.mp3')],[(0,1.83,'보고서는 독고 선생이 써서','D'),(2.07,3.4,'시간 안에 접수하도록 하세요.','D')])
blk([(V+'v30.mp4',0,2.0),(C+'c01.mp4',0,0.8),(V+'v30.mp4',2.8,1.4),('lc2/H1.mp4',0,1.0),(V+'v30.mp4',5.2,2.7),('lc2/H3.mp4',0,1.0),(V+'v30.mp4',8.9,1.1),(C+'c01.mp4',1.0,1.2),(V+'v30.mp4',11.2,1.2)],[d('c30.mp3')],
 [(0,1.8,'지금 4시 50분인데요.','D'),(1.94,4.1,'보고서 쓰고 교장 결재까지 나려면','D'),(4.12,5.6,'5시가 넘겠는데요.','D'),(5.9,7.7,'교장 선생님이 오늘 출장이시라…','D'),(7.74,9.7,'교무실까지 걸어가는 동안에','D'),(9.78,12.0,'5시가 다 되겠어요.','D')])
blk([(V+'v31.mp4',0,2.5),('lc2/H4.mp4',0,0.9),(V+'v31.mp4',3.4,1.6),(C+'c11.mp4',1.5,0.9),(V+'v31.mp4',5.9,2.0),('lc2/H5.mp4',0,1.0),(V+'v31.mp4',8.9,1.05),('lc2/H6.mp4',0,0.9),(V+'v31.mp4',10.45,1.55)],
 [d('c31a.wav'),d('c31b.wav',10.35)],
 [(0,2.5,'교감 선생님이 오전에 종이로 한 번,','D'),(2.56,3.9,'에듀파인으로 한 번,','D'),(3.92,5.8,'결재를 두 번만 안 받으셨어도,','D'),(5.82,7.85,'제가 점심때 써 드렸을 텐데요.','D'),(7.9,9.7,'오늘 분리수거 지도 담당이라,','D'),(10.35,11.7,'그럼 이만…','D')],
 [(S+'thud.wav',5.0,0.4,'s',None)])
blk([('lc2/K32.mp4',0,2.6)],[(H+'/ed/usfx/g1s.wav',0.35,0.9,'d')],ev=[(H+'/ed/usfx/door_cut.wav',0.0,0.6,'s',None)])
MARK['sad']=T
blk([('lc2/c35f.mp4',0,3.0)],ev=[(S+'engine.wav',0,0.6,'s',None)])
MARK['orange']=MARK['sad']
MARK['sad_end']=T
blk([('lc2/BLK3.mp4',0,0.3)])
MARK['end']=T
blk([('lc2/POSTER3.mp4',0,3.0)],ev=[(S+'ding.wav',0,0.6,'s',None)])
SUB+=[(MARK['b03']+0.05,MARK['b03']+1.5,'그날 아침','Cap'),(MARK['b03']+1.6,MARK['b03']+3.2,'교감','Tag'),(MARK['office']+0.4,MARK['office']+2.6,'독고다해 · 국어 교사','Tag'),(MARK['b06']-0.1,MARK['b06']+1.5,'안정우 · 생물 교사','Tag'),(MARK['b29']+0.0,MARK['b29']+1.6,'그날 오후 4:50','Cap'),(MARK['sad']+3.3,MARK['sad']+6.9,'결국 누구든 한 사람이 끝장나야\\N해결이 되는 식이었다.\\N그리고 그게 나였다.','Diary')]
total=T; print('total',total,MARK)
E.append((H+'/ep2/sfx3/B1.mp3',MARK['b03'],0.45,'b',('cut',MARK['birds']-MARK['b03'])))
E.append((H+'/ep2/sfx3/B2.mp3',t17,0.45,'b',('seek',0.0,MARK['t23e']-t17)))
E.append((H+'/ep2/sfx3/B3.mp3',MARK['c26']+1.55,0.6,'s',None))
E.append((H+'/ep2/sfx3/s19.mp3',t17+10.45,0.55,'s',None)); E.append((H+'/ep2/sfx3/s19.mp3',MARK['t23e']-0.05,0.55,'s',None))
E.append((H+'/ep2/sfx3/B2.mp3',MARK['b29'],0.45,'b',('seek',50.0,MARK['sad']-MARK['b29'])))
E.append((S+'birds2.wav',MARK['birds'],0.25,'b',('trim',MARK['t16']+1.5-MARK['birds'])))
E.append((M+'Orange_on_the_Floor.mp3',MARK['orange'],0.7,'s',('end',total-MARK['orange'])))
# picture
os.makedirs('segv9',exist_ok=True); F=[]
CUM=0.0
import shutil; shutil.rmtree('segv9',ignore_errors=True); os.makedirs('segv9',exist_ok=True)
for i,(f,s,dd) in enumerate(P):
    o=f'segv9/s{i:03d}.mp4'
    n0=round(CUM*24); CUM+=dd; nf=max(1,round(CUM*24)-n0)
    run(['ffmpeg','-nostdin','-v','error','-y','-ss',str(max(0,s)),'-i',f,'-vf',"crop='min(iw,ih*9/16)':'min(ih,iw*16/9)',scale=720:1280,fps=24,tpad=stop_mode=clone:stop_duration=1,format=yuv420p",'-frames:v',str(nf),'-an','-c:v','libx264','-preset','veryfast','-crf','19',o]); F.append(o)
open('segv9/l.txt','w').write(''.join(f"file '{os.path.basename(x)}'\n" for x in F))
run(['ffmpeg','-nostdin','-v','error','-y','-f','concat','-safe','0','-i','segv9/l.txt','-c','copy','pic_v9.mp4'])
# audio with ducking for birds
cmd=['ffmpeg','-nostdin','-v','error','-y']
for e in E: cmd+=['-i',e[0]]
fl=''; dl=[];sl=[];bl=[]
for i,(f,at,v,k,tr) in enumerate(E):
    ex=''
    if tr:
        if tr[0]=='trim': ex=f',atrim=0:{tr[1]:.3f},afade=t=out:st={max(0,tr[1]-0.6):.3f}:d=0.6'
        if tr[0]=='sad': ex=f',atrim=0:{tr[1]:.3f},afade=t=in:d=0.6'
        if tr[0]=='seek': ex=f',atrim={tr[1]:.3f}:{tr[1]+tr[2]:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.3,afade=t=out:st={max(0,tr[2]-0.6):.3f}:d=0.6'
        if tr[0]=='cut': ex=f',atrim=0:{tr[1]:.3f},afade=t=in:d=0.6,afade=t=out:st={max(0,tr[1]-0.15):.3f}:d=0.15'
        if tr[0]=='end': ex=f',atrim=0:{tr[1]:.3f},afade=t=in:d=1.0,afade=t=out:st={tr[1]-2.5:.3f}:d=2.5'
    ms=max(0,int(round(at*1000)))
    fl+=f"[{i}:a]aformat=sample_rates=44100:channel_layouts=stereo{ex},volume={v},adelay={ms}|{ms},apad=whole_dur={total}[a{i}];"
    {'d':dl,'s':sl,'b':bl}[k].append(f'[a{i}]')
fl+=''.join(dl)+f"amix=inputs={len(dl)}:normalize=0,asplit=3[D1][D2][D3];"
fl+=''.join(sl)+f"amix=inputs={len(sl)}:normalize=0[SX];"
fl+=''.join(bl)+f"amix=inputs={len(bl)}:normalize=0[B];[B][D2]sidechaincompress=threshold=0.015:ratio=10:attack=20:release=350[BD];"
fl+=f"[SX][D3]sidechaincompress=threshold=0.02:ratio=4:attack=10:release=250[SXD];[D1][SXD][BD]amix=inputs=3:normalize=0,atrim=0:{total}[out]"
cmd+=['-filter_complex',fl,'-map','[out]','-c:a','pcm_s16le','aud_v14_pre.wav']; run(cmd)
import re as _re
_m=subprocess.run(['ffmpeg','-nostdin','-i','aud_v14_pre.wav','-af','ebur128','-f','null','-'],capture_output=True,text=True).stderr
_I=float(_re.findall(r'I:\s+(-?[0-9.]+) LUFS',_m)[-1]); _g=-14.0-_I; print('pre I',_I,'gain',round(_g,2))
run(['ffmpeg','-nostdin','-v','error','-y','-i','aud_v14_pre.wav','-af',f'volume={_g+1.6:.2f}dB,alimiter=limit=0.6:level=false:attack=1:release=50','-c:a','aac','-b:a','192k','aud_v14.m4a'])

SPK=[('DV',['정서교육','오늘 5시까지','밖에서?','계획서, 안전','올리기 전에','그게 순서지','3교시 전까지','최저가로 들어오신','독고 선생!','이건 무단','(작게)','사진… 좀','보고서는 독고','시간 안에 접수']),('DJ',['…다해쌤?','(속삭이며)','어? 어…']),('N',['(수군)','쌤, 이 꽃은'])]
def _spk(t):
    for st,ps in SPK:
        if any(t.startswith(p) for p in ps): return st
    return 'DD'
from PIL import ImageFont as _IF
_FW=_IF.truetype(H+'/fonts/NanumGothicBold.ttf',40)
def _w(t): return _FW.getlength(re.sub(r'\{[^}]*\}','',t))
def _split(a,b,t):
    if _w(t)<=540 or ' ' not in t: return [(a,b,t)]
    sp=[i for i,c in enumerate(t) if c==' ']
    i=min(sp,key=lambda i:max(_w(t[:i]),_w(t[i+1:])))
    L,Rt=t[:i],t[i+1:]; m=a+(b-a)*len(L)/(len(L)+len(Rt))
    return _split(a,m,L)+_split(m,b,Rt)
import re
_S=[]
for a,b,t,st in SUB:
    if st=='Diary' or (st=='Cap' and t=='그날 아침'): continue
    if st in ('D','In'):
        for a2,b2,t2 in _split(a,b,t): _S.append((a2,b2,t2,_spk(t) if st=='D' else 'In'))
    elif st=='In': _S.append((a,b,t,st))
    elif st=='Poem': _S.append((a,b,'{\\pos(372,610)\\frz-5\\fad(300,200)}'+t,st))
    else: _S.append((a,b,t,st))
SUB=_S
EXTRA="Style: HookT,Black Han Sans,40,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,4,3,2,24,24,352,1\nStyle: Note,NanumGothic,30,&H00FFFFFF,&H00FFFFFF,&H00000000,&HA0000000,1,0,0,0,100,100,0,0,3,8,0,8,40,40,150,1\nStyle: Poem,Nanum Pen,58,&H00303A40,&H00303A40,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1\nStyle: Card,Black Han Sans,60,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,2,0,1,0,0,5,0,0,0,1"

def ts(x): x=max(0,x); h=int(x//3600); m=int(x%3600//60); s=x%60; return f"{h}:{m:02d}:{s:05.2f}"
head=open(H+'/ep2/sub_v2_header.ass').read().replace('\n\n[Events]','\n'+EXTRA+'\n\n[Events]',1)
import re as _r
head=_r.sub(r'(Style: Cap,(?:[^,\n]*,){20})[^,\n]*', lambda m: m.group(1)+'60', head)
for a,b,txt,st in SUB: head+=f"Dialogue: 0,{ts(a)},{ts(b)},{st},,0,0,0,,{txt}\n"
open('sub_v14.ass','w').write(head)
flash=','.join(f"drawbox=c=white@0.85:t=fill:enable='between(t,{x:.2f},{x+0.08:.2f})'" for x in FL)
run(['ffmpeg','-nostdin','-v','error','-y','-i','pic_v9.mp4','-i','aud_v14.m4a','-vf',f"setpts=N/(24*TB),{flash},ass=sub_v14.ass:fontsdir={H}/fonts,fade=t=out:st={total-2.0:.2f}:d=2.0",'-c:v','libx264','-preset','veryfast','-crf','20','-c:a','copy','-shortest','full_v14.mp4'])
print('ok')
