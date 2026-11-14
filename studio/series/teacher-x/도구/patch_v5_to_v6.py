# 2화 v5 → v6 고침(채점 v5A 지적, 크레딧 0). 사용: python3 patch_v5_to_v6.py <v5 스크립트> <v6 스크립트>
import sys
s=open(sys.argv[1]).read()
def R(a,b):
    global s
    assert s.count(a)==1, ('not unique/missing', a[:70], s.count(a))
    s=s.replace(a,b)
# 1) ev= 로 넘긴 효과음이 믹스에서 빠지던 버그
R("    for f,o,v,k,tr in au: EV.append((f,T+o,v,k,tr))","    for f,o,v,k,tr in list(au)+list(ev): EV.append((f,T+o,v,k,tr))")
# 2) 이름표 '극 중 설정'
R("'{\\\\fs46}독고다해 · 최저가 계약교사','Tag')","'{\\\\fs46}독고다해 · 최저가 계약교사\\\\N{\\\\fs24}(극 중 설정)','Tag')")
# 3) 기안 풀이 + 알림 상자 잘림(crash → in) + 띵 위치
R("add([(img('313',1.4,'in'),0,1.4),(img('o13',1.6,'crash'),0,1.6)],ev=[(E+'sfx2/arrive.mp3',1.4,0.5,'s',None)],subs=[(1.4,2.0,'{\\\\pos(540,700)\\\\frz-8}'+POP+'띵—','Ono')])",
  "add([(img('313',1.4,'in'),0,1.4),(img('o13',1.6,'in'),0,1.6)],ev=[(E+'sfx2/arrive.mp3',1.4,0.5,'s',None)],subs=[(1.4,2.0,'{\\\\pos(470,680)\\\\frz-8}'+POP+'띵—','Ono'),(1.5,3.0,'{\\\\fs30}기안 = 결재를 올린 문서','N')])")
R("(0.9,'o24','crash')","(0.9,'o24','in')")
# 4) 다해 등장 전 시계 인서트 두 번 → 정우 장면으로
R("(6.0,'307'),(7.4,'v')","(6.0,'clip:n601@2.4'),(7.4,'v')")
R("inner('05',[(img('305',2.0,'out'),0,2.0),(img('307',1.2,'in'),0,1.2)]","inner('05',[(img('305',2.0,'out'),0,2.0),(E+'x/r501.mp4',2.6,1.2)]")
# 5) 결정타 뒤 교감 눈(320, 교감실에서 두 번째·어두운 톤) → 표를 내려다보는 교감 영상의 안 쓴 구간
R("add([(img('320',1.8,'slow'),0,1.8)],subs=[(0.3,1.8,'[정적]','Act')])","add([(E+'x/r508.mp4',2.2,1.8)],subs=[(0.3,1.8,'[정적]','Act')])")
R("outn=E+('ed/ep2_v5A.mp4' if WITH28 else 'ed/ep2_v5B.mp4')","outn=E+('ed/ep2_v6A.mp4' if WITH28 else 'ed/ep2_v6B.mp4')")
R("# 교사X 2화 편집 스크립트 v5","# 교사X 2화 편집 스크립트 v6 (v5 + 채점 지적 고침: 효과음 누락 버그·극 중 설정·기안 풀이·알림 잘림·인서트 중복)\n# (아래는 v5 설명)")
# 6) 기안 도착·최종 승인 알림음이 대사보다 7~8 dB 큼(측정) → 낮춤
R("(E+'sfx2/arrive.mp3',1.4,0.5,'s',None)","(E+'sfx2/arrive.mp3',1.4,0.2,'s',None)")
R("(E+'sfx2/arrive.mp3',0.1,0.45,'s',None)","(E+'sfx2/arrive.mp3',0.1,0.18,'s',None)")
open(sys.argv[2],'w').write(s); print('ok')
