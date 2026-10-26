"""5화 v1: K5(P1)·K6a(P1b) 친구 폰의 하얀 화면에 연락처 카드 "대리 엄마 ☎"만 입힌다 (4화 phone_ui.py 방식).
화면 = 밝고 색이 없는 픽셀 중 가장 큰 덩어리(책상 반사광은 따로 떨어진 덩어리라 빠짐). 손가락(살색)은 위에 남긴다.
화면을 못 찾는 프레임(폰이 흔들려 빠질 때)은 그대로 둔다.
사용: python3 phone_card.py 입력.mp4 출력.mp4
"""
import subprocess, sys
from collections import deque
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
F = '/home/user/youtube-ops/series/_soulchange_kit/fonts/Jua-Regular.ttf'
f = lambda s: ImageFont.truetype(F, s)
S = 8   # 덩어리 찾기용 축소 배율


def card():
    w, h = 450, 950
    s = Image.new('RGB', (w, h), (246, 246, 250)); d = ImageDraw.Draw(s)
    d.ellipse([w // 2 - 95, 170, w // 2 + 95, 360], fill=(255, 196, 120))
    d.text((w // 2, 265), '엄', font=f(110), fill=(255, 255, 255), anchor='mm')
    d.text((w // 2, 470), '대리 엄마', font=f(92), fill=(25, 25, 30), anchor='mm')
    d.rounded_rectangle([w // 2 - 120, 580, w // 2 + 120, 720], 36, fill=(76, 200, 110))
    # Jua에는 ☎ 글자가 없어 DejaVu Sans로 그림(폰 화면 그림 안의 아이콘, 자막 아님)
    d.text((w // 2, 652), '☎', font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 100), fill=(255, 255, 255), anchor='mm')
    return s


def largest(mask):
    h, w = mask.shape
    lab = np.zeros((h, w), int); best, bl = 0, 0; n = 0
    for y0, x0 in zip(*np.nonzero(mask)):
        if lab[y0, x0]: continue
        n += 1; q = deque([(y0, x0)]); lab[y0, x0] = n; c = 0
        while q:
            y, x = q.popleft(); c += 1
            for yy, xx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                if 0 <= yy < h and 0 <= xx < w and mask[yy, xx] and not lab[yy, xx]:
                    lab[yy, xx] = n; q.append((yy, xx))
        if c > best: best, bl = c, n
    return lab == bl, best


def screen(fr):
    small = fr[::S, ::S].astype(int)
    mx, mn = small.max(axis=2), small.min(axis=2)
    m = (mn > 200) & (mx - mn < 30)
    comp, n = largest(m)
    if n < 300: return None   # 화면이 충분히 크게 보일 때만
    ys, xs = np.nonzero(comp); xs = xs * S + S // 2; ys = ys * S + S // 2
    s, dd = xs + ys, xs - ys
    q = np.array([(xs[s.argmin()], ys[s.argmin()]), (xs[dd.argmax()], ys[dd.argmax()]),
                  (xs[s.argmax()], ys[s.argmax()]), (xs[dd.argmin()], ys[dd.argmin()])], float)
    # 가로 세로 비율이 폰 화면 같지 않으면(흔들림) 버림
    wq = np.linalg.norm(q[1] - q[0]); hq = np.linalg.norm(q[3] - q[0])
    if not (1.4 < hq / max(wq, 1) < 2.8): return None
    return q


def persp(src, dst):
    A, b = [], []
    for (x, y), (u, v) in zip(dst, src):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]; b += [u, v]
    return np.linalg.solve(np.array(A, float), np.array(b, float))


def in_quad(q, shrink=10):
    yy, xx = np.mgrid[0:H, 0:W]
    c = q.mean(axis=0); q = c + (q - c) * (1 - shrink / max(1, np.linalg.norm(q[0] - c)))
    m = np.ones((H, W), bool)
    for i in range(4):
        (x1, y1), (x2, y2) = q[i], q[(i + 1) % 4]
        m &= (x2 - x1) * (yy - y1) - (y2 - y1) * (xx - x1) >= 0
    return m


def skin(fr):
    r, g, b = fr[..., 0].astype(int), fr[..., 1].astype(int), fr[..., 2].astype(int)
    return (r > 90) & (r - b > 18) & (r >= g) & (np.maximum(r, np.maximum(g, b)) - np.minimum(r, np.minimum(g, b)) > 15)


def main(src, dst):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    frames = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3).copy()
    qs = [screen(fr) for fr in frames]
    # 찾은 프레임끼리 앞뒤 2프레임 평균(떨림 줄이기)
    sm = []
    for i, q in enumerate(qs):
        if q is None: sm.append(None); continue
        nb = [qs[j] for j in range(max(0, i - 2), min(len(qs), i + 3)) if qs[j] is not None and np.abs(qs[j] - q).max() < 40]
        sm.append(np.mean(nb, axis=0))
    ui = card(); uw, uh = ui.size; hit = 0
    for i, fr in enumerate(frames):
        q = sm[i]
        if q is None: continue
        hit += 1
        coef = persp([(0, 0), (uw, 0), (uw, uh), (0, uh)], [tuple(p) for p in q])
        warped = np.asarray(ui.transform((W, H), Image.PERSPECTIVE, tuple(coef), Image.BICUBIC, fillcolor=(246, 246, 250)))
        m = in_quad(q) & ~skin(fr) & ~(fr.max(axis=2) < 70)
        a = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
        a = np.asarray(a, float)[..., None] / 255
        frames[i] = (fr * (1 - a) + warped * a).astype(np.uint8)
    print(f'phone_card: {hit}/{len(frames)} frames', file=sys.stderr)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', dst], input=frames.tobytes(), check=True)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
