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
im=Image.open(I+'i502.png').convert('RGB'); d=ImageDraw.Draw(im)
d.text((200,600),'초과근무 신청',font=f(54),fill=(30,40,70))
d.text((205,722),'신청자  독고다해',font=f(34),fill=(50,50,50))
d.text((775,722),'일시  오늘 17:00~21:00',font=f(34),fill=(50,50,50))
d.text((205,812),'결재  교감 → 교장',font=f(34),fill=(50,50,50))
d.text((225,870),'사유',font=f(44),fill=(200,30,40))
ctext(d,(240,1300,700,1390),'임시 저장',f(34),(80,80,80))
ctext(d,(820,1300,1320,1390),'결재 요청',f(34),(30,60,160))
tag(d,2480)
im.save(O+'o502.png')
# o503 결재선: 신청자 → 교감 → 교장
im=Image.open(I+'i503.png').convert('RGB'); d=ImageDraw.Draw(im)
ctext(d,(0,860,W,960),'결재선',f(64),(30,40,70))
ctext(d,(230,1080,470,1250),'신청',f(46),(60,60,60)); ctext(d,(200,1290,500,1360),'독고다해',f(40),(60,60,60))
ctext(d,(590,1100,830,1270),'교감',f(46),(60,60,60))
ctext(d,(990,1060,1370,1400),'교장',f(72),(200,30,40)); ctext(d,(940,1430,1420,1500),'최종 결재',f(40),(200,30,40))
tag(d,2480)
im.save(O+'o503.png')
# 엔딩 포스터: 다음 화 안내 (오후 5시 다해 그림 위)
im=Image.open(I+'i316.png').convert('RGBA'); ov=Image.new('RGBA',im.size,(0,0,0,0)); do=ImageDraw.Draw(ov)
do.rectangle((0,1800,W,HH),fill=(0,0,0,150)); im=Image.alpha_composite(im,ov).convert('RGB'); d=ImageDraw.Draw(im)
ctext(d,(0,1880,W,2000),'교사X',f(120),'white')
ctext(d,(0,2040,W,2120),'4화  11월 25일(수) 저녁 6시',f(64),(255,210,120))
ctext(d,(0,2500,W,2560),'@twistbite_drama',f(40),(220,220,220))
im.save(O+'poster.png')
print('ok')
