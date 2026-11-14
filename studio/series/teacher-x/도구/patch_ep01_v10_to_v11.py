# 1화 v10 → v11 (사장님: "결재판은 보통 하나씩 다 있어. 나는 이게 교감이 다해 책상 보는 건 줄 알았네")
# → 누구 서랍인지 먼저 보여 줌: 서랍 안에서 올려다본 교감의 비웃는 얼굴(c14 앞부분) → 에듀파인 '상신 대기' 모니터 + 결재판을 서랍에 넣는 손(c11)
#   표시 글자도 '결재판'이 아니라 '교감 책상 서랍 속 = 다해의 야외 수업 계획서(결재 안 함)'로. 크레딧 0
import sys
s=open(sys.argv[1]).read()
def R(a,b):
    global s
    assert s.count(a)==1, ('not unique/missing', a[:80], s.count(a))
    s=s.replace(a,b)
R("blk([(C+'c11.mp4',0,4.0)],[d('i11r.wav',0.15)],[(0.15,3.85,'결재판은 서랍에. 3교시 전엔 절대 못 나가.','In'),(0.0,3.9,'{\\\\an8\\\\pos(360,150)\\\\fad(200,200)}다해가 올린 「야외 수업」 결재판','Note')]",
  "blk([(C+'c14.mp4',0,1.2),(C+'c11.mp4',0.4,2.8)],[d('i11r.wav',0.15)],[(0.15,3.85,'결재판은 서랍에. 3교시 전엔 절대 못 나가.','In'),(1.2,3.95,'{\\\\an8\\\\pos(360,400)\\\\fad(150,150)}교감 책상 서랍 속\\\\N다해의 야외 수업 계획서 (결재 안 함)','Note')]")
R("'-shortest','full_v10.mp4'])","'-shortest','full_v11.mp4'])")
R("open('sub_v10.ass','w').write(head)","open('sub_v11.ass','w').write(head)")
R("ass=sub_v10.ass:","ass=sub_v11.ass:")
s=s.replace('aud_v10_pre.wav','aud_v11_pre.wav').replace('aud_v10.m4a','aud_v11.m4a')
R("f'volume={_g:.2f}dB,alimiter=limit=0.6","f'volume={_g+1.6:.2f}dB,alimiter=limit=0.6")
open(sys.argv[2],'w').write(s); print('ok')
