# 교사X 4화 커버 v3 (사장님 11/18: "쉬운 시험과 어려운 시험 중 더 유리한 것은? 댓글 유도, 답이 있어? 이런 느낌" + "썸네일만 봐도 제목과 회차 알 수 있게 통일감")
# 틀 = cover_v2.series (위 남색 띠: 교사X · N화 · 「회차 제목」 / 아래: 댓글 부르는 질문). 답은 영상 14·17번(쉬우면 1등급이 안 나올 수 있다 → 열심히 한 학생 손해)
import sys; sys.path.insert(0, '/home/user/qa')
from cover_v2 import series, feed, YEL
import os
I = '/home/user/ep5/img/'; O = '/home/user/cov4/'; Wt = 'white'
Q = [[('쉬운 시험', Wt), (' vs ', YEL), ('어려운 시험', Wt)], [('더 ', Wt), ('유리한 건?', YEL)]]
series(I + 'i418.png', 4, '쉽게 내요', Q, O + 'cover4_G.png')                 # 고민하는 정우
series(I + 'i404.png', 4, '쉽게 내요', Q, O + 'cover4_H.png', face_frac=0.40)  # 답을 아는 다해
series(I + 'i409.png', 4, '쉽게 내요', [[('우리 아이에겐', Wt)], [('쉬운 시험? ', Wt), ('어려운 시험?', YEL)]], O + 'cover4_I.png')  # 놀란 교감, 학부모 말
feed(['/home/user/qa/c4now_full.jpg', O + 'cover4_D.png', O + 'cover4_G.png', O + 'cover4_H.png', O + 'cover4_I.png'],
     ['지금', 'D(직전)', 'G 정우', 'H 다해', 'I 교감'], '/home/user/qa/feed4b.jpg')
print('ok')
