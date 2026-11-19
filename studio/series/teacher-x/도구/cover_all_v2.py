# 교사X 1~7화 커버 v2 — cover_all_v1 결과(자동 선택 그림) 그대로 + 글자 뒤 어두운 띠(cover_v2 고침)
# 11/19 확인: 흰 셔츠 위에서 3화 '야'·6화 '약'이 사라짐 → 띠 추가 후 7화 모두 다시. 4화(G)도 같은 틀로 다시
import sys; sys.path.insert(0, '/home/user/qa')
from cover_v2 import series, feed, YEL
H = '/home/user/'; O = H + 'cov_all/'; Wt = 'white'
C = {
    1: ('ep2/img/i104.png', '퇴근 10분 전 지시', [[('퇴근 10분 전 일 폭탄', Wt)], [('남는다 vs 퇴근한다?', YEL)]]),
    2: ('ep2/img/i217.png', '반려만 6번째', [[('"반려"', YEL), ('의 뜻은', Wt)], [('알고 쓰시길', Wt)]]),
    3: ('ep4/img/i407.png', '밤 9시까지 남아', [[('야근 명령', Wt)], [('따른다 vs 거절한다?', YEL)]]),
    4: ('ep5/img/i418.png', '시험 쉽게 내요', [[('쉬운 시험', Wt), (' vs ', YEL), ('어려운 시험', Wt)], [('더 ', Wt), ('유리한 건?', YEL)]]),
    5: ('ep6/img/i501.png', '1등급이 사라졌다', [[('100점을 받아도', Wt)], [('1등급', YEL), ('을 못 받는 사연', Wt)]]),
    6: ('ep7/img/i414c.png', '회식에서 빠진 사람', [[('계약직은', Wt)], [('회식도', YEL), (' 오지 마라?', Wt)]]),
    7: ('ep8/img/i702.png', '계약직이 하기 딱이네', [[('고기 굽는', YEL), (' 교사 업무', Wt)], [('들어는 봤나?', Wt)]]),
}
for n, (src, title, lines) in C.items():
    series(H + src, n, title, lines, O + f'cover{n}_v2.png')
feed([O + f'cover{n}_v2.png' for n in C], [f'{n}화' for n in C], H + 'qa/feed_all2.jpg')
print('ok')
