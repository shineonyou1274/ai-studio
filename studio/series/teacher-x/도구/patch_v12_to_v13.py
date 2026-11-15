# 2화 v12 → v13 (사장님 11/15): 훅 제목을 키우고 살짝 위로(가슴 높이), 훅 구간 대사 자막은 쓰지 않음. 크레딧 0
import sys,os
from PIL import ImageFont
s=open(sys.argv[1]).read()
def R(a,b):
    global s
    assert s.count(a)==1,('not unique/missing',a[:80],s.count(a)); s=s.replace(a,b)
F=ImageFont.truetype(os.path.expanduser('~/fonts/BlackHanSans-Regular.ttf'),100)
L=["'고쳐 오라면서 길을 6번 바꾸면?'","3주 끌던 결재, 40분 만에 뚫린 이유"]
fs=min(50,int(660*100/max(F.getlength(x) for x in L)))   # 한 줄 660px(화면 720)까지 가장 크게
print('hook font',fs)
# 1) 훅 구간 대사 자막 빼기
R("+chunks('커피 한 잔 드시고 오세요.|'+K('40분')+'이면 됩니다.','12'))",")")
# 2) 크기 키우고 위로: 아래 여백 352 → 540 (사장님이 표시한 가슴 높이)
R("Style: HookT,Black Han Sans,34,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,4,3,2,24,24,352,1",
  "Style: HookT,Black Han Sans,%d,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,5,3,2,24,24,540,1"%fs)
s=s.replace("'ed/ep2_v12A.mp4' if WITH28 else 'ed/ep2_v12B.mp4'","'ed/ep2_v13A.mp4' if WITH28 else 'ed/ep2_v13B.mp4'")
open(sys.argv[2],'w').write(s); print('ok')
