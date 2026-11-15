# 1화 v12 → v13 (사장님 11/15: 글자 위아래 벌어짐·가독성 "또 반복", 그날 아침 블랙 카드, 교감 대사 묻힘, 속마음 작음, 새소리는 교감 뛸 때 사라지게,
#  "사진 좀 찍어도" 안 들림, 화면 바뀌어도 자막 이어짐, 시 자막 지저분, 일기장 엔딩 빼고 차 안 장면을 엔딩으로). 크레딧 0
import sys, re
s=open(sys.argv[1]).read()
def R(a,b):
    global s
    assert s.count(a)==1, ('not unique/missing', a[:80], s.count(a))
    s=s.replace(a,b)
X="H+'/ep2/sfx3/"
# 1) '그날 아침' = 0.8초 블랙 카드(하드 컷) + 키보드 타자음 + 교감 첫 대사 0.35초 먼저(J컷). 훅 뒤 흰 번쩍임 뺌
R("mk('black.png','lc2/BLK3.mp4',0.3,'1','0','0')","mk('black.png','lc2/BLK3.mp4',0.3,'1','0','0')\nmk('black.png','lc2/BLK8.mp4',0.8,'1','0','0')")
R("FL.append(T-0.08)\nE.append((H+'/ep2/sfx3/B2.mp3',0,0.45,'b',('seek',50.0,T)))","E.append((H+'/ep2/sfx3/B2.mp3',0,0.45,'b',('seek',50.0,T)))")
R("MARK['b03']=T\nblk([(V+'v03.mp4',0,1.55),('lc/A2.mp4',0,2.0),(V+'v03.mp4',3.55,1.55)],[d('c03.mp3')]",
  "blk([('lc2/BLK8.mp4',0,0.8)],subs=[(-0.08,0.8,'그날 아침','Card')],ev=[("+X+"s26.mp3',0.05,0.5,'s',('seek',0.0,0.6))])\nMARK['b03']=T\nblk([(V+'v03.mp4',0,1.55),('lc/A2.mp4',0,2.0),(V+'v03.mp4',3.55,1.55)],[d('c03.mp3',-0.35)]")
# 2) 효과음이 대사를 덮음: 진동음 줄이고, 효과음 버스도 대사 때 자동으로 줄이기
s=s.replace("(S+'buzz2.wav',0.0,0.45,","(S+'buzz2.wav',0.0,0.2,").replace("(S+'buzz2.wav',0.2,0.45,","(S+'buzz2.wav',0.2,0.2,")
R("asplit=2[D1][D2];","asplit=3[D1][D2][D3];")
R('fl+=f"[D1][SX][BD]amix=inputs=3','fl+=f"[SX][D3]sidechaincompress=threshold=0.02:ratio=4:attack=10:release=250[SXD];[D1][SXD][BD]amix=inputs=3')
# 3) 속마음 크게(+5 dB)
for a in ("d('i04r.wav',0.7)","d('i11r.wav',0.15)","d('i14r.wav',1.8)","d('i28r.wav',1.0)"):
    R(a,a[:-1]+",1.8)")
# 4) 새소리: 교감이 뛰기 시작하면(16) 1.5초 동안 사라짐
R("('trim',MARK['birds_end']-MARK['birds'])))","('trim',MARK['t16']+1.5-MARK['birds'])))")
# 5) "사진 좀 찍어도 되겠습니까"를 덮던 승리 팡파르(B3)를 뒤로 — 교감이 사진 찍는 셔터 순간(굴복)에, 작게
R("blk([(C+'c26.mp4',0,1.8)]","MARK['c26']=T\nblk([(C+'c26.mp4',0,1.8)]")
R("E.append((H+'/ep2/sfx3/B3.mp3',MARK['t23e'],0.9,'s',None))","E.append((H+'/ep2/sfx3/B3.mp3',MARK['c26']+1.55,0.6,'s',None))")
# 6) 일기장 엔딩 빼기 → 백미러 차 안 장면이 엔딩, 엔딩곡이 차 안부터
R("blk([(C+'c33.mp4',0,3.0),(C+'c34.mp4',0,4.0),('lc2/c35f.mp4',0,3.0)],","blk([('lc2/c35f.mp4',0,3.0)],")
R("MARK['orange']=MARK['sad']+6.6","MARK['orange']=MARK['sad']")
s=re.sub(r"E\.append\(\(M\+'Dusk_Diary\.mp3'[^\n]*\n","",s)
# 7) 자막 v2(2화와 같은 규칙): 한 줄만(넘치면 시간 나눠 두 장으로), 인물 테두리 색, 속마음 명조, 시는 종이 위 손글씨, 장면 카드, 일기 자막 뺌
POST=r'''
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
EXTRA="Style: HookT,Black Han Sans,36,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,4,3,8,24,24,50,1\nStyle: Note,NanumGothic,30,&H00FFFFFF,&H00FFFFFF,&H00000000,&HA0000000,1,0,0,0,100,100,0,0,3,8,0,8,40,40,150,1\nStyle: Poem,Nanum Pen,58,&H00303A40,&H00303A40,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1\nStyle: Card,Black Han Sans,60,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,2,0,1,0,0,5,0,0,0,1"
'''
s=s.replace("def ts(x):",POST+"\ndef ts(x):",1)
lines=s.split('\n')
for k,l in enumerate(lines):
    if l.startswith("head=open('sub1.ass')"):
        lines[k]="head=open(H+'/ep2/sub_v2_header.ass').read().replace('\\n\\n[Events]','\\n'+EXTRA+'\\n\\n[Events]',1)"
s='\n'.join(lines)
# 8) 화면 밀림 막기(2화 v9와 같음): 조각을 누적 프레임 경계로 자르고, 짧은 원본은 마지막 프레임으로 채움
R("""for i,(f,s,dd) in enumerate(P):\n    o=f'segv9/s{i:03d}.mp4'\n    run(['ffmpeg','-nostdin','-v','error','-y','-ss',str(s),'-i',f,'-t',str(dd),'-vf',"crop='min(iw,ih*9/16)':'min(ih,iw*16/9)',scale=720:1280,fps=24,format=yuv420p",""",
  """CUM=0.0\nimport shutil; shutil.rmtree('segv9',ignore_errors=True); os.makedirs('segv9',exist_ok=True)\nfor i,(f,s,dd) in enumerate(P):\n    o=f'segv9/s{i:03d}.mp4'\n    n0=round(CUM*24); CUM+=dd; nf=max(1,round(CUM*24)-n0)\n    run(['ffmpeg','-nostdin','-v','error','-y','-ss',str(max(0,s)),'-i',f,'-vf',"crop='min(iw,ih*9/16)':'min(ih,iw*16/9)',scale=720:1280,fps=24,tpad=stop_mode=clone:stop_duration=1,format=yuv420p",'-frames:v',str(nf),""")
s=s.replace('full_v12.mp4','full_v13.mp4').replace('sub_v12.ass','sub_v13.ass').replace('aud_v12_pre.wav','aud_v13_pre.wav').replace('aud_v12.m4a','aud_v13.m4a')
open(sys.argv[2],'w').write(s); print('ok')
