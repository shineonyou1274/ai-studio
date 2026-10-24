"""4화 v14: N3b 컷(담임 몸이 문자 보내는 0:33~0:35)의 하얀 폰 화면 안에만 문자 화면을 입힌다.
화면 = 밝고 색이 없는 픽셀만 바꾸므로, 화면을 덮은 엄지손가락·베젤은 그대로 위에 남는다.
사용: python3 phone_ui.py 입력.mp4 출력.mp4
"""
import subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
ROI = (700, 560, 1080, 1250)   # x0, y0, x1, y1: 폰이 움직이는 범위(영혼 원 아래)
F = '/home/user/youtube-ops/series/_soulchange_kit/fonts/Jua-Regular.ttf'
f = lambda s: ImageFont.truetype(F, s)


def screen_image():
    """폰 화면에 들어갈 문자 화면(세로 9:19). 작게 보이므로 굵은 덩어리 위주."""
    w, h = 450, 950
    s = Image.new('RGB', (w, h), (242, 242, 247)); d = ImageDraw.Draw(s)
    d.rectangle([0, 0, w, 110], fill=(228, 228, 236))
    d.text((24, 70), '< 하은이 어머니', font=f(36), fill=(30, 30, 30), anchor='lm')
    d.rounded_rectangle([20, 150, 330, 300], 22, fill=(255, 255, 255))
    for i, t in enumerate(['선생님~ 하은이가', '두통이 심해서', '집에서 쉴게요.']):
        d.text((38, 168 + 42 * i), t, font=f(32), fill=(40, 40, 40))
    d.rounded_rectangle([90, 360, w - 20, 660], 24, fill=(255, 223, 90))
    for i, t in enumerate(['어머님~ 하은이 두통', '얼른 나아야 할 텐데요.', '근데 단톡 사진 보니까', '일본에선 다 나은 것', '같던데요?^^']):
        d.text((110, 380 + 54 * i), t, font=f(34), fill=(20, 20, 20))
    d.text((w - 24, 690), '읽음', font=f(28), fill=(120, 120, 130), anchor='ra')
    d.rounded_rectangle([16, h - 90, w - 16, h - 24], 30, fill=(255, 255, 255))
    return s


def persp_coeffs(src, dst):
    """PIL PERSPECTIVE용 계수: 출력 좌표(dst) → 입력 좌표(src)."""
    A, b = [], []
    for (x, y), (u, v) in zip(dst, src):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]
        b += [u, v]
    return np.linalg.solve(np.array(A, float), np.array(b, float))


def screen_mask(fr):
    x0, y0, x1, y1 = ROI
    roi = fr[y0:y1, x0:x1].astype(int)
    mx, mn = roi.max(axis=2), roi.min(axis=2)
    m = (mn > 205) & (mx - mn < 28)
    full = np.zeros(fr.shape[:2], bool); full[y0:y1, x0:x1] = m
    return full


def corners(m):
    ys, xs = np.nonzero(m)
    if len(xs) < 2000: return None
    s, dd = xs + ys, xs - ys
    tl = (xs[s.argmin()], ys[s.argmin()]); br = (xs[s.argmax()], ys[s.argmax()])
    tr = (xs[dd.argmax()], ys[dd.argmax()]); bl = (xs[dd.argmin()], ys[dd.argmin()])
    return np.array([tl, tr, br, bl], float)


def in_quad(q, shrink=3):
    """사각형 q 안쪽 픽셀(가장자리 shrink 픽셀 안쪽)."""
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
    masks = [screen_mask(fr) for fr in frames]
    cs = [corners(m) for m in masks]
    # 모서리를 앞뒤 2프레임 평균으로 다듬어 떨림을 줄임(못 찾은 프레임은 이웃 값)
    # v14b: 한 프레임 사이 모서리가 크게 튀면(손가락이 화면을 많이 가려 밝은 부분이 줄 때) 앞 프레임 모서리를 쓴다
    last = next(c for c in cs if c is not None); out = []
    for c in cs:
        if c is None or np.abs(c - last).max() > 18: c = last + np.clip((c if c is not None else last) - last, -4, 4)
        out.append(c); last = c
    cs = out
    sm = [np.mean(cs[max(0, i - 2):i + 3], axis=0) for i in range(len(cs))]
    ui = screen_image(); uw, uh = ui.size
    for i, fr in enumerate(frames):
        q = sm[i]
        coef = persp_coeffs([(0, 0), (uw, 0), (uw, uh), (0, uh)], [tuple(p) for p in q])
        warped = np.asarray(ui.transform((W, H), Image.PERSPECTIVE, tuple(coef), Image.BICUBIC, fillcolor=(242, 242, 247)))
        m = in_quad(q, shrink=8) & ~skin(fr) & ~(fr.max(axis=2) < 70)   # v14b: 사각형 안쪽 전체(회색 얼룩 포함)에서 손가락(살색)만 뺌
        a = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
        a = np.asarray(a, float)[..., None] / 255
        frames[i] = (fr * (1 - a) + warped * a).astype(np.uint8)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', dst], input=frames.tobytes(), check=True)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
