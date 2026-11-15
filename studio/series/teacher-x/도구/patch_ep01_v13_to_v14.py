# 1화 v13 → v14 (사장님 11/15: "(아직 조금만)"은 '훅 생각해 보자'는 메모였음 / 훅 자막 "야외수업 결재받으라는 교감에게 대처하는 방법" /
#  훅 자막(위)과 대사 자막(아래)이 화면 양끝으로 벌어져 눈이 오감 → 훅 동안 훅 자막을 대사 자막 바로 위로 붙임). 크레딧 0
import sys
s=open(sys.argv[1]).read()
def R(a,b):
    global s
    assert s.count(a)==1, ('not unique/missing', a[:80], s.count(a))
    s=s.replace(a,b)
R("'{\\\\fad(300,0)}되로 주려다 {\\\\c&H0078E0FF&}말로{\\\\r} 받는다\\\\N{\\\\fs24}(아직 조금만)','HookT'",
  "'{\\\\fad(300,0)}야외수업 결재받으라는 교감에게\\\\N{\\\\c&H0078E0FF&}대처하는 방법','HookT'")
R("Style: HookT,Black Han Sans,36,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,4,3,8,24,24,50,1",
  "Style: HookT,Black Han Sans,40,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,4,3,2,24,24,352,1")
s=s.replace('full_v13.mp4','full_v14.mp4').replace('sub_v13.ass','sub_v14.ass').replace('aud_v13_pre.wav','aud_v14_pre.wav').replace('aud_v13.m4a','aud_v14.m4a')
open(sys.argv[2],'w').write(s); print('ok')
