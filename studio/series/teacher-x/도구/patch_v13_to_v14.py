# 2화 v13 → v14 (사장님 11/15): 훅 제목이 길고 훅 같지 않음 → "반려의 뜻을 / 참교육하는 ○○교사". 크레딧 0
# 사용: python3 patch_v13_to_v14.py build14.py build15.py 계약   (또는 신규)
import sys,os
from PIL import ImageFont
s=open(sys.argv[1]).read(); who=sys.argv[3]
def R(a,b):
    global s
    assert s.count(a)==1,('not unique/missing',a[:80],s.count(a)); s=s.replace(a,b)
R("\"{\\\\fad(300,0)}'고쳐 오라면서 길을 \"+YN+\"6번{\\\\r} 바꾸면?'\\\\N\"+YN+\"3주{\\\\r} 끌던 결재, \"+YN+\"40분{\\\\r} 만에 뚫린 이유\"",
  "\"{\\\\fad(300,0)}반려의 뜻을\\\\N\"+YN+\"참교육{\\\\r}하는 "+who+"교사\"")
F=ImageFont.truetype(os.path.expanduser('~/fonts/BlackHanSans-Regular.ttf'),100)
fs=min(64,int(640*100/max(F.getlength(x) for x in ["반려의 뜻을","참교육하는 "+who+"교사"])))
print('hook font',fs)
import re
s,n=re.subn(r"Style: HookT,Black Han Sans,\d+,",f"Style: HookT,Black Han Sans,{fs},",s); assert n==1
s=s.replace("'ed/ep2_v13A.mp4' if WITH28 else 'ed/ep2_v13B.mp4'","'ed/ep2_v14%s.mp4'%('K' if '"+who+"'=='계약' else 'S')")
open(sys.argv[2],'w').write(s); print('ok')
