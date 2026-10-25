"""소울체인지 고정 엔딩 영상 만들기 (코드 렌더, 크레딧 0)
사용: python3 make_ending.py <회차번호> <다음화 요일> <음원.wav> <출력.mp4>
예:   python3 make_ending.py 5 화 엔딩_후보A_17.2-22.9.wav ending_ep5.mp4
화면: 노을빛 그라데이션 → 두 영혼 원(지우 분홍·담임 하늘)이 양쪽에서 들어와 가운데서 자리를 바꿈 →
      한입극장 명판 + 민트 리본 "소울체인지 N화" + "다음 화 ○요일 18시" + @twistbite_drama
"""
import subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

KIT = '/home/user/youtube-ops/series/_soulchange_kit'
F = KIT + '/fonts/Jua-Regular.ttf'
W, H, FPS = 1080, 1920, 30
OUTL, RED, MINT, CREAM, YEL = (11, 16, 48), (216, 35, 42), (45, 190, 156), (255, 246, 227), (255, 226, 90)
f = lambda s: ImageFont.truetype(F, s)


def bg():
    top, bot = np.array([250, 160, 110]), np.array([20, 28, 62])   # 노을 주황 → 남색
    t = np.linspace(0, 1, H)[:, None, None] ** 0.8
    return Image.fromarray((top * (1 - t) + bot * t).repeat(W, axis=1).astype(np.uint8))


def circle(path, d):
    im = Image.open(path).convert('RGBA').resize((d, d), Image.LANCZOS)
    m = Image.new('L', (d, d), 0); ImageDraw.Draw(m).ellipse([0, 0, d - 1, d - 1], fill=255)
    im.putalpha(m); return im


def ease(x):
    x = min(max(x, 0), 1); return x * x * (3 - 2 * x)


def main(ep, day, wav, out):
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', wav],
                               capture_output=True, text=True).stdout)
    n = int(round(dur * FPS))
    base = bg(); d = 300
    jiwoo, teacher = circle(KIT + '/pip.png', d), circle(KIT + '/pip_t.png', d)
    proc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                             '-i', wav, '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
                             '-c:a', 'aac', '-b:a', '160k', '-shortest', out], stdin=subprocess.PIPE)
    for i in range(n):
        t = i / FPS
        fr = base.copy(); dr = ImageDraw.Draw(fr)
        # 0~0.6초 양쪽에서 들어옴, 0.6~1.4초 가운데서 원을 그리며 자리 바꿈, 그 뒤 살짝 떠 있음
        cy = 640
        if t < 0.6:
            k = ease(t / 0.6)
            xa = -d + (240 + d) * k
            xb = W - (d + 240) * k
            ya = yb = cy
        else:
            k = ease((t - 0.6) / 0.8)
            ang = np.pi * k
            cx, r = W / 2 - d / 2, (W / 2 - d / 2) - 240
            xa, ya = cx - r * np.cos(ang), cy - 120 * np.sin(ang)
            xb, yb = cx + r * np.cos(ang), cy + 120 * np.sin(ang)
            bob = 8 * np.sin(2 * np.pi * (t - 1.4) / 1.6) if t > 1.4 else 0
            ya += bob; yb -= bob
        fr.paste(jiwoo, (int(xa), int(ya)), jiwoo); fr.paste(teacher, (int(xb), int(yb)), teacher)
        a = ease((t - 1.2) / 0.5)   # 글자는 1.2초부터 서서히
        if a > 0:
            txt = Image.new('RGBA', (W, H), (0, 0, 0, 0)); td = ImageDraw.Draw(txt)
            td.rounded_rectangle([325, 1050, 755, 1182], radius=18, fill=RED + (255,), outline=OUTL + (255,), width=6)
            td.text((540, 1116), '한입극장', font=f(104), fill=CREAM, stroke_width=8, stroke_fill=OUTL, anchor='mm')
            td.rounded_rectangle([330, 1205, 750, 1281], radius=8, fill=MINT + (255,), outline=OUTL + (255,), width=5)
            td.text((540, 1243), f'소울체인지 {ep}화 끝', font=f(54), fill=CREAM, stroke_width=5, stroke_fill=OUTL, anchor='mm')
            td.text((540, 1400), f'다음 화 {day}요일 18시', font=f(76), fill=YEL, stroke_width=7, stroke_fill=OUTL, anchor='mm')
            td.text((540, 1760), '@twistbite_drama', font=f(40), fill=(220, 224, 240), anchor='mm')
            al = np.asarray(txt).copy(); al[..., 3] = (al[..., 3] * a).astype(np.uint8)
            fr = Image.alpha_composite(fr.convert('RGBA'), Image.fromarray(al)).convert('RGB')
        proc.stdin.write(np.asarray(fr).tobytes())
    proc.stdin.close(); proc.wait()


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
