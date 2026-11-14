# 2화 v6 → v7 (사장님 11/14 청취 지적). 사용: python3 patch_v6_to_v7.py <v6> <v7>
import sys
s=open(sys.argv[1]).read()
def R(a,b):
    global s
    assert s.count(a)==1, ('not unique/missing', a[:70], s.count(a))
    s=s.replace(a,b)
# 1) "쯧쯧쯧"(04, 7.62~8.28초) 입이 안 맞음 → 그 구간을 교감 눈 굴리는 반응 영상(r504의 안 쓴 뒤쪽)으로 덮음
R("(6.0,'clip:n601@2.4'),(7.4,'v')],","(6.0,'clip:n601@2.4'),(7.6,'clip:r504@2.2')],")
# 2) 마지막 대사 자막: "아니에요."를 앞 문장에 붙임
R("'규정이 지켜 주는 게|아니에요.|끝까지 읽은 사람이|지키는 거지.'","'규정이 지켜 주는 게 아니에요.|끝까지 읽은 사람이|지키는 거지.'")
# 3) 컷19 뒷부분을 다시 찍은 두 영상으로(19b = 녹음 3.45~9.4초, 19c = 9.4~12.1초). 교차는 1~3초
R("segs=[(V+'v19.mp4',0,2.5),(img('222',0.9),0,0.9),(V+'v19.mp4',3.4,round(tg-0.2-3.4,3)),(E+'x/r509.mp4',1.8,1.2),(V+'v19.mp4',tg+1.0,round(tk-0.3-(tg+1.0),3)),(img('319',0.8,'crash'),0,0.8),(V+'v19.mp4',tk+0.5,round(L19-tk-0.5,3))]",
  "B0,C0=3.45,9.4\nsegs=[(V+'v19.mp4',0,2.5),(img('222',0.9),0,0.9),(E+'x/n19b.mp4',3.4-B0,1.9),(E+'x/r509.mp4',1.8,1.2),(E+'x/n19b.mp4',6.5-B0,round(tk-0.3-6.5,3)),(img('319',0.8,'crash'),0,0.8),(E+'x/n19c.mp4',tk+0.5-C0,round(L19-tk-0.5,3))]")
# 4) 훅 첫 화면도 다시 찍은 19c로(입 맞음)
R("add([(V+'v19.mp4',hs-0.15,1.4),","add([(E+'x/n19c.mp4',max(0,hs-0.05-9.4-0.1),1.4),")
R("outn=E+('ed/ep2_v6A.mp4' if WITH28 else 'ed/ep2_v6B.mp4')","outn=E+('ed/ep2_v7A.mp4' if WITH28 else 'ed/ep2_v7B.mp4')")
open(sys.argv[2],'w').write(s); print('ok')
