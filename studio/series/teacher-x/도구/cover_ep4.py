# 교사X 4화 커버 3종 (사장님 11/18 "4화 썸네일 바꾸고 싶네. 클릭하고 싶지가 않아")
# 지금 첫 화면(키보드 위 손 + '미이수 막으려고')은 얼굴·갈등이 없고 '미이수'가 낯선 말 → 얼굴 감정 + 갈등 한 줄 + 궁금증으로
# 틀은 cover_mk.py(1~2화 커버와 같음). 샌드박스 ~/ep5 에서 실행 → ~/cov4/*.png. 크레딧 0(이미 있는 그림)
import sys; sys.path.insert(0, '/home/user/qa')
from cover_mk import cover
import os
I = '/home/user/ep5/img/'; O = '/home/user/cov4/'; os.makedirs(O, exist_ok=True)
EP = '교사X 4화'
# A 긴장: 정우 어깨를 잡고 부탁하는 교감 — 부탁의 말 그대로
cover(I + 'i411.png', ['"시험, 너무', '어렵게 내지 마요"'], O + 'cover4_A.png', 0.5, EP, '미이수 나오면 소문난다는 교감')
# B 반전·숫자: 팔짱 낀 다해 — 결과를 궁금하게(5화 떡밥, 실제 보도된 일)
cover(I + 'i404.png', ['쉽게 내면', '1등급이 0명?'], O + 'cover4_B.png', 0.5, EP, '시험 쉽게 내라는 교감 vs 신규교사')
# C 공감: 밤, 모니터 앞 정우 — 결말(문제를 지움)을 먼저
cover(I + 'i418.png', ['결국, 그 문제를', '지웠다'], O + 'cover4_C.png', 0.5, EP, '학생은 안 오고 서류만 쌓이는 교사')
print('ok')
