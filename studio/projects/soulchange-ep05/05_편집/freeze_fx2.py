"""5화 v5: freeze_fx.py(v4)에서 — 정지를 얼굴이 늘어나기 시작하는 프레임(원본 70)에서 깨끗한 프레임 80으로 건너뛰며 시작(번쩍임·펀치 인으로 가림),
큰 흔들림과 두 번째 펀치 인은 고함("갑질이잖아요!" 큰 소리) 순간에. 마지막 인자 shout = 정지 시작부터 고함까지 초.
(v4 설명) K11(A4 v2) 고함 순간 정지 화면 + 만화 효과 (코드만, 크레딧 0).
A4 v2의 고함 얼굴이 원본 약 3.4초부터 늘어나고 뭉개져서(Gemini 지적), 그 전 마지막 깨끗한 프레임(이 드러낸 찡그림)에서 멈춘다.
효과: 흰 번쩍임 1–2프레임, 빠른 펀치 인(1.0→1.15, 0.15초) 뒤 천천히 더 다가감, 0.5초 카메라 흔들림, 첫 프레임 움직임 번짐,
얼굴을 피한 만화 집중선.
사용: python3 freeze_fx2.py live.mp4 원본.mp4 프레임번호 정지프레임수 얼굴x 얼굴y 얼굴반지름 out.mp4 shout초
  live.mp4 = 1080x1920 30fps 앞부분(정지 전), 얼굴 좌표는 1080x1920 기준.
"""
import subprocess, sys, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

W, H, FPS = 1080, 1920, 30


def grab(src, n):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-vf',
                          f"select='eq(n\\,{n})',scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920",
                          '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    return Image.frombytes('RGB', (W, H), raw[:W * H * 3])


def zoom(im, z, cx, cy, dx=0, dy=0):
    """(cx,cy)를 중심으로 z배 확대하고 (dx,dy)만큼 흔듦."""
    w, h = W / z, H / z
    x0 = min(max(cx - w / 2, 0), W - w); y0 = min(max(cy - h / 2, 0), H - h)
    return im.transform((W, H), Image.EXTENT, (x0 - dx / z, y0 - dy / z, x0 + w - dx / z, y0 + h - dy / z), Image.BICUBIC)


def speed_lines(fx, fy, r, seed, n=70):
    """얼굴 둘레(r) 밖에서 화면 끝으로 뻗는 쐐기 모양 집중선(검정·흰색 섞음)."""
    rnd = random.Random(seed)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    R = math.hypot(W, H)
    for i in range(n):
        a = 2 * math.pi * i / n + rnd.uniform(-0.03, 0.03)
        r0 = r * rnd.uniform(1.25, 1.9)
        wdt = rnd.uniform(0.004, 0.012)
        p0 = (fx + r0 * math.cos(a), fy + r0 * math.sin(a))
        p1 = (fx + R * math.cos(a - wdt), fy + R * math.sin(a - wdt))
        p2 = (fx + R * math.cos(a + wdt), fy + R * math.sin(a + wdt))
        col = (255, 255, 255, 150) if i % 3 else (20, 20, 30, 150)
        d.polygon([p0, p1, p2], fill=col)
    return lay.filter(ImageFilter.GaussianBlur(1.2))


def main(live, src, n, nf, fx, fy, fr, out, shout='0.4'):
    shout = float(shout)
    base = grab(src, int(n))
    nf, fx, fy, fr = int(nf), float(fx), float(fy), float(fr)
    rnd = random.Random(5)
    frames = []
    prev = None
    for i in range(nf):
        t = i / FPS
        z = 1.0 + 0.15 * min(t / 0.15, 1.0) + 0.03 * max(0.0, t - 0.15)          # 건너뛰는 순간 빠른 펀치 인 → 천천히
        ts = t - shout
        if ts >= 0: z += 0.08 * min(ts / 0.1, 1.0)                                 # 고함 순간 두 번째 펀치 인
        amp = 8 * max(0.0, 1 - t / 0.15)                                           # 건너뛸 때 짧게 살짝
        if 0 <= ts < 0.5: amp = 24 * (1 - ts / 0.5)                                # 고함에 0.5초 큰 흔들림
        dx, dy = rnd.uniform(-amp, amp), rnd.uniform(-amp, amp)
        im = zoom(base, z, fx, fy, dx, dy)
        if i < 3 or 0 <= ts < 0.1:   # 첫 프레임·고함 순간 움직임 번짐: 조금 덜 확대한 그림을 겹침
            z0 = max(1.0, z - 0.06)
            im = Image.blend(im, zoom(base, z0, fx, fy, dx, dy), 0.35)
        # 집중선: 얼굴 위치도 같이 확대된 자리로
        w, h = W / z, H / z
        x0 = min(max(fx - w / 2, 0), W - w); y0 = min(max(fy - h / 2, 0), H - h)
        sfx, sfy = (fx - x0) * z + dx, (fy - y0) * z + dy
        lines = speed_lines(sfx, sfy, fr * z, seed=i // 2)
        im = Image.alpha_composite(im.convert('RGBA'), lines).convert('RGB')
        if i == 0: im = Image.blend(im, Image.new('RGB', (W, H), (255, 255, 255)), 0.85)   # 흰 번쩍임
        elif i == 1: im = Image.blend(im, Image.new('RGB', (W, H), (255, 255, 255)), 0.4)
        frames.append(np.asarray(im, np.uint8))
    fz = out + '.freeze.mp4'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p', fz],
                   input=np.stack(frames).tobytes(), check=True)
    lst = out + '.txt'
    open(lst, 'w').write(f"file '{live}'\nfile '{fz}'\n")
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', out], check=True)


if __name__ == '__main__':
    main(*sys.argv[1:])
