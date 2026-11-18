# 교사X 4화 커버 v2 (사장님 11/18 "궁금하지도 않고 시청자층도 없어지게 하고 있어") — 썸네일_판단기준_v1.md로 다시
# 샌드박스 ~/qa 에서 실행(cover_v2.py 같은 폴더) → ~/cov4/*.png, 피드 비교판 ~/qa/feed4.jpg
import sys; sys.path.insert(0, '/home/user/qa')
from cover_v2 import cover, feed
import os
I = '/home/user/ep5/img/'; O = '/home/user/cov4/'; os.makedirs(O, exist_ok=True)
# D: 상식과 반대(쉬우면 좋은 거 아냐?) + 학부모가 반응하는 말 '손해'. 답(열심히 공부한 상위권 학생)은 4화 14·17번에 있음
cover(I + 'i418.png', ['시험이 쉬우면', '손해 보는 건?'], O + 'cover4_D.png', key='손해', face_frac=0.42)
# E: 몰래 한 부탁 — 내용은 숨김. 답(어렵게 내지 마요)은 4화 08번
cover(I + 'i411.png', ['교감이 몰래', '한 부탁'], O + 'cover4_E.png', key='몰래', face_frac=0.42)
# F: 이유를 숨김. 답(소문 → 신입생 모집 → 재단)은 4화 08·09번
cover(I + 'i409.png', ['시험 쉽게 내라는', '진짜 이유'], O + 'cover4_F.png', key='진짜 이유', face_frac=0.45)
feed(['/home/user/qa/c4now_full.jpg', O + 'cover4_B.png', O + 'cover4_D.png', O + 'cover4_E.png', O + 'cover4_F.png'],
     ['지금', '아까 B', 'D 손해', 'E 몰래', 'F 진짜 이유'], '/home/user/qa/feed4.jpg')
print('ok')
