# 1화 v15 → v16 (사장님 11/15): 훅 제목을 키우고 살짝 위로, 훅 구간 대사 자막은 쓰지 않음(2화와 같게). 크레딧 0
import sys,os
from PIL import ImageFont
s=open(sys.argv[1]).read()
def R(a,b):
    global s
    assert s.count(a)==1,('not unique/missing',a[:80],s.count(a)); s=s.replace(a,b)
F=ImageFont.truetype(os.path.expanduser('~/fonts/BlackHanSans-Regular.ttf'),100)
L=["야외수업 결재받으라는 교감에게","대처하는 방법"]
fs=min(52,int(660*100/max(F.getlength(x) for x in L)))
print('hook font',fs)
R(",(0.1,3.4,'교감 선생님의 결재 대상이 아닙니다.','D')])","])")
R("Style: HookT,Black Han Sans,40,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,4,3,2,24,24,352,1",
  "Style: HookT,Black Han Sans,%d,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,5,3,2,24,24,330,1"%fs)   # 1화 첫 컷은 얼굴 클로즈업이라 위로 올리면 입을 가림 → 대사 자리였던 턱·옷깃 높이 유지
for a,b in [('full_v15.mp4','full_v16.mp4'),('sub_v15.ass','sub_v16.ass'),('aud_v15_pre.wav','aud_v16_pre.wav'),('aud_v15.m4a','aud_v16.m4a')]:
    s=s.replace(a,b)
open(sys.argv[2],'w').write(s); print('ok')
