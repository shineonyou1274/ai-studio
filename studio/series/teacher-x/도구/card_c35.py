# 3차·5차 '정반대' 카드(1520x2688, 반려 사유표와 같은 종이색). 샌드박스 ~/ep2 에서 실행 → ov/c35.png
from PIL import Image, ImageDraw, ImageFont
F='/home/user/fonts/NanumGothicBold.ttf'; BH='/home/user/fonts/BlackHanSans-Regular.ttf'
def f(s,p=F): return ImageFont.truetype(p,s)
W,H=1520,2688; im=Image.new('RGB',(W,H),(246,243,235)); d=ImageDraw.Draw(im)
def ct(y,t,fn,fill):
    w=d.textlength(t,font=fn); d.text(((W-w)/2,y),t,font=fn,fill=fill)
ct(330,'같은 강사료, 두 번의 반려',f(76),(20,20,20)); ct(440,'(극 중 설정)',f(40),(120,120,120))
RED=(210,30,40)
for y0,lab,txt in ((640,'3차','강사료 → 운영비로 옮길 것'),(1420,'5차','왜 운영비로 옮겼나? 원래대로')):
    d.rounded_rectangle((90,y0,W-90,y0+420),40,fill='white',outline=(60,60,60),width=4)
    d.text((150,y0+50),lab,font=f(110),fill=RED)
    d.text((150,y0+220),txt,font=f(64),fill=(20,20,20))
    d.ellipse((110,y0+190,W-110,y0+330),outline=RED,width=12)
# 두 칸을 잇는 화살표 + 정반대
x=W//2; d.line((x,1080,x,1400),fill=RED,width=16); d.polygon([(x-50,1350),(x+50,1350),(x,1410)],fill=RED); d.polygon([(x-50,1130),(x+50,1130),(x,1070)],fill=RED)
d.rounded_rectangle((x+60,1170,x+520,1310),30,fill=RED); ct_w=d.textlength('정반대',font=f(96,BH)); d.text((x+60+(460-ct_w)/2,1180),'정반대',font=f(96,BH),fill='white')
im.save('ov/c35.png'); print('ok')
