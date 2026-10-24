"""4화 v11 화면 겹침 이미지: 반 단톡 폰 화면, 해외로밍 전화 수신 화면 (Jua 폰트만)"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
HERE = Path(__file__).resolve().parent
IMG = HERE.parent / '04_생성물/images'
F = '/home/user/youtube-ops/series/_soulchange_kit/fonts/Jua-Regular.ttf'
f = lambda s: ImageFont.truetype(F, s)
W, H = 1080, 1920
def phone(screen):
    pw, ph = 760, 1400; x0, y0 = (W - pw) // 2, 190
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([x0 + 10, y0 + 20, x0 + pw + 10, y0 + ph + 20], 80, fill=(0, 0, 0, 150))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(20)))
    ImageDraw.Draw(im).rounded_rectangle([x0, y0, x0 + pw, y0 + ph], 80, fill=(22, 22, 26, 255))
    sx0, sy0, sx1, sy1 = x0 + 24, y0 + 24, x0 + pw - 24, y0 + ph - 24
    scr = Image.new('RGBA', (sx1 - sx0, sy1 - sy0)); screen(scr)
    mask = Image.new('L', scr.size, 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, *scr.size], 58, fill=255)
    im.paste(scr, (sx0, sy0), mask)
    ImageDraw.Draw(im).rounded_rectangle([W // 2 - 80, y0 + 38, W // 2 + 80, y0 + 74], 18, fill=(22, 22, 26, 255))
    return im
def chat(s):
    w, h = s.size; d = ImageDraw.Draw(s)
    d.rectangle([0, 0, w, h], fill=(186, 206, 224, 255)); d.rectangle([0, 0, w, 160], fill=(170, 192, 212, 255))
    d.text((44, 112), '<  3학년 2반 단톡  28', font=f(44), fill=(30, 30, 30), anchor='lm')
    def other(name, text, y, col):
        d.ellipse([30, y, 104, y + 74], fill=col); d.text((122, y + 4), name, font=f(32), fill=(60, 60, 60))
        tw = d.textlength(text, font=f(42)); d.rounded_rectangle([122, y + 48, 122 + tw + 44, y + 122], 24, fill=(255, 255, 255))
        d.text((144, y + 85), text, font=f(42), fill=(20, 20, 20), anchor='lm'); return y + 150
    y = other('민준', '오늘 하은이 결석?', 200, (230, 170, 150))
    d.ellipse([30, y, 104, y + 74], fill=(240, 190, 200)); d.text((122, y + 4), '하은', font=f(32), fill=(60, 60, 60))
    ph = Image.open(IMG / '단톡_일본거리.png').convert('RGB'); pw = w - 170; ph = ph.resize((pw, int(pw * ph.height / ph.width)))
    m = Image.new('L', ph.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, *ph.size], 26, fill=255)
    s.paste(ph, (122, y + 48), m); y = y + 48 + ph.size[1] + 18
    t = '나 일본 도착 ㅋㅋ'; tw = d.textlength(t, font=f(52))
    d.rounded_rectangle([122, y, 122 + tw + 48, y + 88], 26, fill=(255, 255, 255)); d.text((146, y + 44), t, font=f(52), fill=(20, 20, 20), anchor='lm')
    y += 112; d.text((122, y), '오후 1:12', font=f(28), fill=(90, 100, 110)); y += 54
    other('서준', '?? 두통이라며 ㅋㅋ', y, (160, 200, 170))
def call(s):
    w, h = s.size; d = ImageDraw.Draw(s)
    for i in range(h): d.line([(0, i), (w, i)], fill=(40 + i // 45, 48 + i // 40, 70 + i // 30, 255))
    d.rounded_rectangle([w // 2 - 130, 170, w // 2 + 130, 240], 35, fill=(255, 214, 90))
    d.text((w // 2, 205), '해외로밍', font=f(46), fill=(40, 40, 50), anchor='mm')
    d.ellipse([w // 2 - 120, 320, w // 2 + 120, 560], fill=(120, 130, 150))
    d.text((w // 2, 440), '학부모', font=f(60), fill=(240, 240, 240), anchor='mm')
    d.text((w // 2, 660), '하은이 어머니', font=f(76), fill=(255, 255, 255), anchor='mm')
    d.text((w // 2, 745), '+81 국제전화 (일본)', font=f(38), fill=(200, 205, 220), anchor='mm')
    d.ellipse([100, h - 290, 280, h - 110], fill=(230, 70, 70)); d.ellipse([w - 280, h - 290, w - 100, h - 110], fill=(60, 190, 110))
    d.text((190, h - 200), '거절', font=f(40), fill=(255, 255, 255), anchor='mm'); d.text((w - 190, h - 200), '받기', font=f(40), fill=(255, 255, 255), anchor='mm')
def talking(s):
    """통화 중 화면: 어머니 목소리가 나오는 동안 화면 속 인물 표정과 겹치지 않게 덮음"""
    w, h = s.size; d = ImageDraw.Draw(s)
    for i in range(h): d.line([(0, i), (w, i)], fill=(30 + i // 50, 36 + i // 45, 56 + i // 34, 255))
    d.rounded_rectangle([w // 2 - 130, 170, w // 2 + 130, 240], 35, fill=(255, 214, 90))
    d.text((w // 2, 205), '해외로밍', font=f(46), fill=(40, 40, 50), anchor='mm')
    d.ellipse([w // 2 - 120, 320, w // 2 + 120, 560], fill=(120, 130, 150))
    d.text((w // 2, 440), '학부모', font=f(60), fill=(240, 240, 240), anchor='mm')
    d.text((w // 2, 660), '하은이 어머니', font=f(76), fill=(255, 255, 255), anchor='mm')
    d.text((w // 2, 745), '통화 중 00:04', font=f(42), fill=(120, 230, 150), anchor='mm')
    for k, hh in enumerate([30, 70, 110, 60, 140, 90, 40, 120, 80, 50, 100, 35]):
        x = 110 + k * 42; d.rounded_rectangle([x, 900 - hh // 2, x + 22, 900 + hh // 2], 10, fill=(255, 120, 120))
    d.ellipse([w // 2 - 90, h - 290, w // 2 + 90, h - 110], fill=(230, 70, 70))
    d.text((w // 2, h - 200), '종료', font=f(40), fill=(255, 255, 255), anchor='mm')
def sent(s):
    """보낸 문자 화면: 담임 몸(지우 영혼)이 들고 있는 폰이 하얗게 비어 보이던 0:33~0:35 구간을 덮음"""
    w, h = s.size; d = ImageDraw.Draw(s)
    d.rectangle([0, 0, w, h], fill=(242, 242, 247, 255)); d.rectangle([0, 0, w, 160], fill=(228, 228, 236, 255))
    d.text((44, 112), '<  하은이 어머니', font=f(46), fill=(30, 30, 30), anchor='lm')
    d.rounded_rectangle([w - 230, 88, w - 40, 134], 22, fill=(255, 214, 90)); d.text((w - 135, 111), '해외로밍', font=f(30), fill=(40, 40, 50), anchor='mm')
    y = 200
    for line in ['선생님~ 하은이가', '두통이 심해서', '오늘 집에서 쉴게요.']:
        pass
    lines = ['선생님~ 하은이가', '두통이 심해서', '오늘 집에서 쉴게요.']
    bw = max(d.textlength(t, font=f(40)) for t in lines) + 48
    d.rounded_rectangle([30, y, 30 + bw, y + 40 + 52 * len(lines)], 26, fill=(255, 255, 255))
    for i, t in enumerate(lines): d.text((54, y + 24 + 52 * i), t, font=f(40), fill=(20, 20, 20))
    y += 40 + 52 * len(lines) + 16; d.text((40, y), '오전 8:02', font=f(26), fill=(120, 120, 130)); y += 70
    lines = ['어머님~ 하은이 두통', '얼른 나아야 할 텐데요.', '근데 단톡 사진 보니까', '일본에선 다 나은 것', '같던데요?^^']
    bw = max(d.textlength(t, font=f(42)) for t in lines) + 52
    x0 = w - 30 - bw
    d.rounded_rectangle([x0, y, w - 30, y + 44 + 56 * len(lines)], 26, fill=(255, 223, 90))
    for i, t in enumerate(lines): d.text((x0 + 26, y + 24 + 56 * i), t, font=f(42), fill=(20, 20, 20))
    y += 44 + 56 * len(lines) + 14
    d.text((w - 40, y), '읽음  오전 8:41', font=f(30), fill=(120, 120, 130), anchor='ra')
    d.rounded_rectangle([24, h - 130, w - 24, h - 40], 40, fill=(255, 255, 255)); d.text((60, h - 85), '메시지 입력', font=f(34), fill=(170, 170, 180), anchor='lm')
if __name__ == '__main__':
    phone(sent).save(IMG / 'ovl_보낸문자.png')
    phone(talking).save(IMG / 'ovl_통화중.png')
    phone(chat).save(IMG / 'ovl_단톡.png'); phone(call).save(IMG / 'ovl_전화.png')
    print('ok')
