# 1화 v14 → v15 (사장님 11/15: "안전점검표" 씹힘 / (수군) 같은 괄호 빼기 / 자막은 문맥 단위로(3교시가 다음 말과 같이) /
#  시 글자 삐뚤어짐 / 마지막 '띵' 빼기). 크레딧 0
import sys
s=open(sys.argv[1]).read()
def R(a,b):
    global s
    assert s.count(a)==1, ('not unique/missing', a[:80], s.count(a))
    s=s.replace(a,b)
# 1) 08 녹음 '안전점검|표' 사이 0.15초 끊김(받아쓰기 3.42~4.26초 낱말 안, 무음 4.02~4.17초) → 그 끊김만 이어 붙임
R("# split audio for breath pauses","run(['ffmpeg','-nostdin','-v','error','-y','-i',A+'c08.mp3','-filter_complex','[0]atrim=0:4.04,asetpts=PTS-STARTPTS[a];[0]atrim=4.15,asetpts=PTS-STARTPTS[b];[a][b]acrossfade=d=0.02[o]','-map','[o]',A+'c08f.wav'])\n# split audio for breath pauses")
R("[d('c08.mp3')]","[d('c08f.wav')]")
# 2) 마지막 포스터 '띵' 빼기
R("blk([('lc2/POSTER3.mp4',0,3.0)],ev=[(S+'ding.wav',0,0.6,'s',None)])","blk([('lc2/POSTER3.mp4',0,3.0)])")
# 3) 시: 기울이지 않음
R("'{\\\\pos(372,610)\\\\frz-5\\\\fad(300,200)}'","'{\\\\pos(372,610)\\\\fad(300,200)}'")
# 4) 자막 문맥 단위: 긴 줄은 편집장이 뜻 덩어리로 '|' 끊음(자동 끊기 대신), 한 줄 폭 600px까지. 괄호 지문 (수군)(속삭이며)(작게) 빼기
MAN='''
MAN={'교감 선생님의 결재 대상이 아닙니다.':'교감 선생님의|결재 대상이 아닙니다.',
'오늘 5시까지 교장 결재까지 받아서 내세요.':'오늘 5시까지|교장 결재까지 받아서 내세요.',
'실적 미달 명단…? 이번엔 무조건 우수사례다.':'실적 미달 명단…?|이번엔 무조건 우수사례다.',
'밖에서? 애들 데리고 놀러 가는 거 아닙니까?':'밖에서?|애들 데리고 놀러 가는 거 아닙니까?',
'계획서, 안전점검표, 결재 세 단계 받아 오세요.':'계획서, 안전점검표,|결재 세 단계 받아 오세요.',
'올리기 전에 출력해서 먼저 들고 와요.':'올리기 전에 출력해서|먼저 들고 와요.',
'결재판은 서랍에. 3교시 전엔 절대 못 나가.':'결재판은 서랍에.|3교시 전엔 절대 못 나가.',
'3교시 전까지 결재 안 나면 무단 수업이에요.':'3교시 전까지 결재 안 나면|무단 수업이에요.',
'최저가로 들어오신 분이, 재계약 생각은 하셔야지.':'최저가로 들어오신 분이,|재계약 생각은 하셔야지.',
'흐흐… 종 쳤네. 결재판은 여기 있고… 밖에서 수업은 무슨.':'흐흐… 종 쳤네.|결재판은 여기 있고…|밖에서 수업은 무슨.',
'쌤, 이 꽃은 왜 가운데가 노란색이에요?':'쌤, 이 꽃은|왜 가운데가 노란색이에요?',
'어? 어… 그건 수술이라고, 꽃가루를…':'어? 어…|그건 수술이라고, 꽃가루를…',
'사방이 벽으로 막힌 교실 안에서 한 발짝도 못 나간 수업이,':'사방이 벽으로 막힌 교실 안에서|한 발짝도 못 나간 수업이,'}
def _split(a,b,t):
    t=MAN.get(t,t)
    for p in ('(수군) ','(속삭이며) ','(작게) '):
        if t.startswith(p): t=t[len(p):]
    if '|' in t:
        ps=t.split('|'); tot=sum(len(p) for p in ps); out=[]; x=a
        for p in ps:
            y=x+(b-a)*len(p)/tot; out.append((x,y,p)); x=y
        return out
    if _w(t)<=600 or ' ' not in t: return [(a,b,t)]
    sp=[i for i,c in enumerate(t) if c==' ']
    i=min(sp,key=lambda i:max(_w(t[:i]),_w(t[i+1:])))
    L,Rt=t[:i],t[i+1:]; m=a+(b-a)*len(L)/(len(L)+len(Rt))
    return _split(a,m,L)+_split(m,b,Rt)
'''
a=s.index("def _split(a,b,t):"); b=s.index("import re\n_S=[]")
s=s[:a]+MAN.strip()+"\n"+s[b:]
s=s.replace('full_v14.mp4','full_v15.mp4').replace('sub_v14.ass','sub_v15.ass').replace('aud_v14_pre.wav','aud_v15_pre.wav').replace('aud_v14.m4a','aud_v15.m4a')
open(sys.argv[2],'w').write(s); print('ok')
