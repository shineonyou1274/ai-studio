"""6화 v4: K11 벤치 학생이 고개를 깊이 숙여 '머리 없는 사람'처럼 보임(Gemini P1) → 숙인 머리 윤곽(어두운 머리+후드 둥근 테)을 코드로 살짝 얹는다.
웃음 장치 아님 — 실루엣만 사람답게. 프레임마다 남색 몸 덩어리를 찾아 따라감.
사용: python3 bench_hood.py K11.mp4 out.mp4
"""
import subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

def main(src, dst):
    w, h = map(int, subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', src],
                                   capture_output=True, text=True).stdout.strip().split(','))
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3).copy()
    last = None; out = []
    for a in fr:
        r = a[:int(h * 0.4), 150:].astype(int)
        m = (r[..., 2] > r[..., 0] + 8) & (r.sum(2) < 230)
        cols = np.nonzero(m.sum(0) >= 10)[0]
        if len(cols) > 8:
            # 가장 긴 연속 열 묶음 = 몸
            runs = np.split(cols, np.nonzero(np.diff(cols) > 3)[0] + 1); body = max(runs, key=len)
            x0, x1 = body[0] + 150, body[-1] + 150
            rows = np.nonzero(m[:, x0 - 150:x1 - 150 + 1].mean(1) > 0.55)[0]
            if not len(rows): out.append(a); continue
            # 몸 위끝 위의 회색 후드 안감까지 올라감(밝고 색 없는 픽셀)
            g = a[:, x0:x1 + 1].astype(int); gm = (g.min(2) > 120) & (g.max(2) - g.min(2) < 30)
            top = rows[0]
            while top > 2 and gm[top - 1].mean() > 0.25: top -= 1
            cur = np.array([x0, x1, top], float)
            last = cur if last is None else last * 0.7 + cur * 0.3
        im = Image.fromarray(a)
        if last is not None:
            x0, x1, top = last; bw = x1 - x0; cx = (x0 + x1) / 2
            lay = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
            hw, hh = bw * 0.24, bw * 0.24
            # 숙인 머리(검은 머리) + 그 둘레 후드 테(회색 안감)
            d.ellipse([cx - hw * 1.05, top - hh * 1.2, cx + hw * 1.05, top + hh * 0.5], fill=(128, 130, 140, 220))
            d.ellipse([cx - hw * 0.70, top - hh * 1.0, cx + hw * 0.70, top + hh * 0.25], fill=(38, 32, 34, 245))
            lay = lay.filter(ImageFilter.GaussianBlur(1.3))
            im = Image.alpha_composite(im.convert('RGBA'), lay).convert('RGB')
        out.append(np.asarray(im))
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{w}x{h}', '-r', '24', '-i', '-',
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '15', '-pix_fmt', 'yuv420p', dst], input=np.stack(out).tobytes(), check=True)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
