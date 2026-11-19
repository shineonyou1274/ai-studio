# 교사X 1·2·3·5·6·7화 커버 (통일 틀 cover_v2.series) — 사장님 11/19 글귀 확정 + "자동으로 골라"
# 얼굴 그림 자동 선택: 그 화 그림들 중 가장 큰 얼굴(얼굴 폭/그림 폭)이 있는 그림. 결과는 ~/cov_all/picks.json
# 샌드박스 ~/qa 에서 실행(cover_v2.py 같은 폴더) → ~/cov_all/cover{N}.png, ~/qa/feed_all.jpg
import sys, os, glob, json
sys.path.insert(0, '/home/user/qa')
from cover_v2 import series, feed, face_box, YEL
from PIL import Image
H = '/home/user/'; O = H + 'cov_all/'; os.makedirs(O, exist_ok=True); Wt = 'white'
EP = {
    1: ('ep2/img/i1*.png', '퇴근 10분 전 지시', [[('퇴근 10분 전 일 폭탄', Wt)], [('남는다 vs 퇴근한다?', YEL)]]),
    2: ('ep2/img/i[23]*.png', '반려만 6번째', [[('"반려"', YEL), ('의 뜻은', Wt)], [('알고 쓰시길', Wt)]]),
    3: ('ep4/img/i*.png', '밤 9시까지 남아', [[('야근 명령', Wt)], [('따른다 vs 거절한다?', YEL)]]),
    5: ('ep6/img/i5*.png', '1등급이 사라졌다', [[('100점을 받아도', Wt)], [('1등급', YEL), ('을 못 받는 사연', Wt)]]),
    6: ('ep7/img/i6*.png', '회식에서 빠진 사람', [[('계약직은', Wt)], [('회식도', YEL), (' 오지 마라?', Wt)]]),
    7: ('ep8/img/i7[0-1]*.png', '계약직이 하기 딱이네', [[('고기 굽는', YEL), (' 교사 업무', Wt)], [('들어는 봤나?', Wt)]]),
}
picks = {}
for n, (pat, title, lines) in EP.items():
    best = None
    for p in sorted(glob.glob(H + pat)):
        if '_old' in p: continue
        im = Image.open(p).convert('RGB'); im.thumbnail((640, 640))
        fb = face_box(im)
        if not fb: continue
        frac = fb[2] / im.width
        if best is None or frac > best[0]: best = (frac, p)
    if not best: print(n, '얼굴 못 찾음'); continue
    picks[n] = {'img': best[1].replace(H, '~/'), 'face_frac': round(best[0], 3)}
    series(best[1], n, title, lines, O + f'cover{n}.png')
    print(n, picks[n])
json.dump(picks, open(O + 'picks.json', 'w'), ensure_ascii=False, indent=1)
ks = sorted(picks)
feed([O + f'cover{k}.png' for k in ks] + ['/home/user/cov4/cover4_G.png'], [f'{k}화' for k in ks] + ['4화(확정)'], '/home/user/qa/feed_all.jpg')
print('ok')
