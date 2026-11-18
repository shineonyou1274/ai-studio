# 교사X 물건 재기 (재발방지 체크리스트 관문 C) — 글자를 얹을 도장·라벨·종이·화면의 가운데·기울기·크기를 픽셀로 잰다
# 눈대중 금지(실수 기록 11/18 '반려' 잘림·봉투 글자). 7화 ep7_ov_v3.py에서 손으로 한 방법을 도구로.
# 사용: python3 measure_obj.py 그림.png --color red [--roi x0,y0,x1,y1] [--top 3] [--min-area 400] [--out 표시.png]
#   --color: red / white / dark / #RRGGBB(--tol 거리)
# 출력: 덩어리마다 가운데(x,y), 기울기, 회전 상자 가로·세로, 안쪽에 들어갈 글자 크기 어림
#   기울기 표기: '화면에서 시계 방향 +'와 'tilted()·PIL rotate에 넣을 값(반시계 +)'을 둘 다 적음 — 7화 라벨 방향 뒤집힘 재발 방지
import sys, os, argparse, math
import numpy as np, cv2
from PIL import Image
from scipy import ndimage

ap = argparse.ArgumentParser(); ap.add_argument('img'); ap.add_argument('--color', default='red')
ap.add_argument('--tol', type=int, default=60); ap.add_argument('--roi', default=None)
ap.add_argument('--top', type=int, default=3); ap.add_argument('--min-area', type=int, default=400)
ap.add_argument('--close', type=int, default=9, help='글자 획 사이를 메우는 크기(px)')
ap.add_argument('--out', default=None)
a = ap.parse_args()
im = np.asarray(Image.open(a.img).convert('RGB')); H, W = im.shape[:2]
x0, y0, x1, y1 = map(int, a.roi.split(',')) if a.roi else (0, 0, W, H)
sub = im[y0:y1, x0:x1]
hsv = cv2.cvtColor(sub, cv2.COLOR_RGB2HSV); h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
if a.color == 'red': m = ((h < 10) | (h > 168)) & (s > 90) & (v > 70)
elif a.color == 'white': m = (s < 40) & (v > 205)
elif a.color == 'dark': m = v < 60
else:
    c = np.array([int(a.color[i:i + 2], 16) for i in (1, 3, 5)]); m = np.abs(sub.astype(int) - c).sum(2) < a.tol
m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((a.close, a.close), np.uint8))
lab, n = ndimage.label(m)
areas = ndimage.sum(m, lab, range(1, n + 1))
order = [i + 1 for i in np.argsort(-areas) if areas[i] >= a.min_area][:a.top]
vis = cv2.cvtColor(im.copy(), cv2.COLOR_RGB2BGR)
print(f'{os.path.basename(a.img)} {W}x{H}, 색 {a.color}, 덩어리 {len(order)}개')
for k, i in enumerate(order):
    ys, xs = np.nonzero(lab == i); pts = np.stack([xs + x0, ys + y0], 1).astype(np.float32)
    (cx, cy), (rw, rh), _ = rect = cv2.minAreaRect(pts)
    box = cv2.boxPoints(rect)
    # 가로에 가장 가까운 변의 기울기(화면 기준, 시계 방향 +)
    best = None
    for j in range(4):
        p, q = box[j], box[(j + 1) % 4]; ang = math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))
        ang = (ang + 90) % 180 - 90
        L = math.hypot(*(q - p))
        if best is None or abs(ang) < abs(best[0]): best = (ang, L)
    ang = best[0]; wlen = best[1]; hlen = (rw * rh) / max(1, wlen)
    print(f' #{k + 1} 가운데 ({cx:.0f}, {cy:.0f}) / 기울기 화면 시계방향 {ang:+.1f}° → tilted()·PIL rotate 값 {-ang:+.1f} / 가로 {wlen:.0f} · 세로 {hlen:.0f}px / 면적 {int(areas[i - 1])}'
          f' / 글자 크기 어림: 한 줄이면 {int(hlen * 0.55)}, 가로 기준 2글자 {int(wlen * 0.8 / 2)}')
    cv2.drawContours(vis, [box.astype(np.int32)], 0, (0, 255, 0), 4); cv2.circle(vis, (int(cx), int(cy)), 10, (255, 0, 0), -1)
    cv2.putText(vis, f'#{k + 1} {-ang:+.1f}', (int(cx) + 14, int(cy) - 14), cv2.FONT_HERSHEY_SIMPLEX, 1.6, (0, 255, 0), 4)
if a.roi: cv2.rectangle(vis, (x0, y0), (x1, y1), (0, 200, 255), 3)
if a.out:
    s = 900 / max(W, H); cv2.imwrite(a.out, cv2.resize(vis, (int(W * s), int(H * s))), [cv2.IMWRITE_JPEG_QUALITY, 80]); print('표시 그림', a.out)
