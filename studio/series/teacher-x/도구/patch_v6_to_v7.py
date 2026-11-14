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
R("outn=E+('ed/ep2_v6A.mp4' if WITH28 else 'ed/ep2_v6B.mp4')","outn=E+('ed/ep2_v7A.mp4' if WITH28 else 'ed/ep2_v7B.mp4')")
open(sys.argv[2],'w').write(s); print('ok')
