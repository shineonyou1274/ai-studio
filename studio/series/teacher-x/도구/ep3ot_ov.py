# 교사X 3화(야근 강요) 화면 글자 그림 (샌드박스 ~/ep4 에서 실행) → ~/ep4/ov/*.png
from PIL import Image, ImageDraw, ImageFont
H='/home/user/'; I=H+'ep4/img/'; O=H+'ep4/ov/'
F=H+'fonts/NanumGothicBold.ttf'; BH=H+'fonts/BlackHanSans-Regular.ttf'
def f(s,p=F): return ImageFont.truetype(p,s)
def ctext(d,box,t,font,fill):
    x0,y0,x1,y1=box; w=d.textlength(t,font=font); bb=font.getbbox(t); h=bb[3]-bb[1]
    d.text(((x0+x1-w)/2,(y0+y1-h)/2-bb[1]),t,font=font,fill=fill)
def tag(d,y):
    d.rounded_rectangle((1060,y,1440,y+80),radius=16,fill=(0,0,0)); ctext(d,(1060,y,1440,y+80),'극 중 설정',f(40),'white')
W,HH=1520,2688
# o502 초과근무 신청서 화면: 사유 칸만 비어 있음
# 화면이 기울어 있음(오른쪽이 위, 기울기 -0.0606 ≈ 3.47도). 칸 테두리를 픽셀로 재서 칸 가운데에 같은 각도로 돌려 넣음 (11/16 v5)
import math
SL=-0.0606; ANG=math.degrees(math.atan(-SL))
def rtext(im,cx,cy,t,font,fill,anchor='mm'):
    w=int(font.getlength(t))+40; bb=font.getbbox(t); h=bb[3]+40
    lay=Image.new('RGBA',(w,h),(0,0,0,0)); dl=ImageDraw.Draw(lay)
    if anchor=='mm': dl.text((w/2,h/2),t,font=font,fill=fill,anchor='mm')
    else: dl.text((20,h/2),t,font=font,fill=fill,anchor='lm')
    lay=lay.rotate(ANG,expand=True,resample=Image.BICUBIC)
    if anchor=='mm': im.alpha_composite(lay,(int(cx-lay.size[0]/2),int(cy-lay.size[1]/2)))
    else: im.alpha_composite(lay,(int(cx-20),int(cy-lay.size[1]/2)))
im=Image.open(I+'i502.png').convert('RGBA')
rtext(im,760,620,'초과근무 신청',f(56),(30,40,70))
rtext(im,452,781,'신청자: 독고다해',f(30),(50,50,50))      # 왼쪽 칸 x184~720, 가운데 높이 781
rtext(im,1019,746,'일시: 오늘 17:00~21:00',f(30),(50,50,50)) # 오른쪽 칸 x754~1284
rtext(im,746,871,'결재: 교감 → 교장',f(30),(50,50,50))       # 넓은 칸 x194~1298
rtext(im,258,1032,'사유를 입력하세요',f(34),(165,165,170),anchor='lm')  # 사유 칸 안, 커서 오른쪽 자리표시 글자
rtext(im,508,1349,'임시 저장',f(34),(80,80,80))
rtext(im,1081,1297,'결재 요청',f(34),(30,60,160))
im=im.convert('RGB'); d=ImageDraw.Draw(im)
tag(d,2150)
im.save(O+'o502.png')
# o503 결재선: 신청자 → 교감 → 교장
im=Image.open(I+'i503.png').convert('RGB'); d=ImageDraw.Draw(im)
ctext(d,(0,960,W,1060),'결재선',f(64),(30,40,70))
ctext(d,(245,1160,475,1240),'신청',f(46),(60,60,60)); ctext(d,(250,1330,470,1420),'독고다해',f(38),(60,60,60))
ctext(d,(595,1175,845,1255),'교감',f(46),(60,60,60))
ctext(d,(1000,1110,1375,1215),'교장',f(66),(200,30,40)); ctext(d,(1010,1370,1365,1460),'최종 결재',f(42),(200,30,40))
tag(d,2150)
im.save(O+'o503.png')
# 엔딩 포스터: 다음 화 안내 (오후 5시 다해 그림 위)
im=Image.open(I+'i316.png').convert('RGBA'); ov=Image.new('RGBA',im.size,(0,0,0,0)); do=ImageDraw.Draw(ov)
do.rectangle((0,1800,W,HH),fill=(0,0,0,150)); im=Image.alpha_composite(im,ov).convert('RGB'); d=ImageDraw.Draw(im)
ctext(d,(0,1880,W,2000),'교사X',f(120),'white')
ctext(d,(0,2040,W,2120),'4화  11월 25일(수) 저녁 6시',f(64),(255,210,120))
ctext(d,(0,2500,W,2560),'@twistbite_drama',f(40),(220,220,220))
im.save(O+'poster.png')
print('ok')
