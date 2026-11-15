# 1화 v11 → v12 (사장님 "새소리 너무 자극적이야, 다른 게 안 들릴 정도" + 캡처: "그날 아침"이 교감 얼굴 가림 + 제미나이: 훅 자막이 너무 위). 크레딧 0
import sys
s=open(sys.argv[1]).read()
def R(a,b):
    global s
    assert s.count(a)==1, ('not unique/missing', a[:80], s.count(a))
    s=s.replace(a,b)
# 1) 새소리 1.0 → 0.25 (약 −12 dB). 음량 맞추기를 '전체 한 비율'로 바꾼 뒤 새소리가 같이 커졌던 것
R("E.append((S+'birds2.wav',MARK['birds'],1.0,'b',","E.append((S+'birds2.wav',MARK['birds'],0.25,'b',")
# 2) 장면 카드(Cap: 그날 아침·그날 오후 4:50)를 화면 맨 위(위 60px)로 — 얼굴 가림 방지
R("for a,b,txt,st in SUB: head+=","import re as _r\nhead=_r.sub(r'(Style: Cap,(?:[^,\\n]*,){20})[^,\\n]*', lambda m: m.group(1)+'60', head)\nfor a,b,txt,st in SUB: head+=")
# 3) 훅 자막 26 → 50px (폰 상단 상태바 안전 영역)
R("Style: HookT,Black Han Sans,36,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,4,3,8,24,24,26,1","Style: HookT,Black Han Sans,36,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,4,3,8,24,24,50,1")
s=s.replace('full_v11.mp4','full_v12.mp4').replace('sub_v11.ass','sub_v12.ass').replace('aud_v11_pre.wav','aud_v12_pre.wav').replace('aud_v11.m4a','aud_v12.m4a')
open(sys.argv[2],'w').write(s); print('ok')
