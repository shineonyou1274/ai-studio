# 교사X 6화(회비 안 낸 사람) 화면 글자 그림 (샌드박스 ~/ep7 에서 실행) → ~/ep7/ov/*.png
# 좌표는 그림에 100px 격자를 그려 잰 값(1520x2688). '극 중 설정' 표시는 왼쪽 위. 자막 띠(y 약 1900~2100)는 비운다(실수 기록 11/17).
from PIL import Image, ImageDraw, ImageFont
import os
H='/home/user/'; I=H+'ep7/img/'; O=H+'ep7/ov/'; os.makedirs(O,exist_ok=True)
F=H+'fonts/NanumGothicBold.ttf'
def f(s): return ImageFont.truetype(F,s)
def tag(d,x=60,y=300):
    d.rounded_rectangle((x,y,x+340,y+76),radius=16,fill=(0,0,0)); d.text((x+170,y+38),'극 중 설정',font=f(38),fill='white',anchor='mm')
# 601 컴퓨터 메신저: 교감 → 다해 1:1 쪽지 (훅 제목과 같은 문구)
im=Image.open(I+'i601.png').convert('RGB'); d=ImageDraw.Draw(im)
d.rectangle((415,618,700,672),fill=(244,246,252)); d.text((420,645),'교감',font=f(44),fill=(30,40,70),anchor='lm')
d.rounded_rectangle((415,755,1395,1075),radius=26,fill=(255,255,255),outline=(200,206,222),width=3)
for k,t in enumerate(['계약직은 친목회원이 아닙니다.','회식에 참여 희망하시면','별도 회비를 내세요.']):
    d.text((455,815+k*92),t,font=f(52),fill=(20,20,30),anchor='lm')
d.text((430,1115),'오후 2:58',font=f(32),fill=(120,126,140),anchor='lm')
tag(d,60,120); im.save(O+'o601.png')
# 602 교직원 단체방(폰): 회식 공지에 들뜬 교사들
im=Image.open(I+'i602.png').convert('RGB'); d=ImageDraw.Draw(im)
d.rectangle((598,720,1090,800),fill=(236,238,244)); d.text((605,742),'교직원 친목회',font=f(32),fill=(30,30,40),anchor='lm'); d.text((605,782),'오늘 회식 6시!',font=f(30),fill=(80,80,90),anchor='lm')
d.text((610,975),'교직원 친목회 (38)',font=f(34),fill='white',anchor='lm')
for (x0,y0,x1,y1,t) in [(600,1040,1015,1180,'오늘 친목회 회식|6시 OO갈비'),(615,1215,1045,1350,'1차는 친목회비로!'),(640,1395,1095,1530,'다들 오시죠?')]:
    ls=t.split('|'); cy=(y0+y1)/2-(len(ls)-1)*24
    for k,l in enumerate(ls): d.text((x0+30,cy+k*48),l,font=f(38),fill=(25,25,35),anchor='lm')
d.text((1000,1615),'참석합니다!',font=f(38),fill=(25,25,35),anchor='mm')
d.text((700,1775),'저도요~',font=f(38),fill=(25,25,35),anchor='lm')
d.text((710,1905),'6시에 봬요',font=f(38),fill=(25,25,35),anchor='lm')
tag(d,60,120); im.save(O+'o602.png')
# 605 교직원 친목회 회칙: 제2조 형광펜 줄
im=Image.open(I+'i605.png').convert('RGB'); d=ImageDraw.Draw(im)
d.text((740,600),'교직원 친목회 회칙',font=f(60),fill=(25,25,30),anchor='mm')
d.rectangle((292,850,348,920),fill=(238,234,228))
d.text((350,845),'제2조(회원) 본교 교직원은',font=f(50),fill=(20,20,25),anchor='lm')
d.rectangle((345,885,1190,965),fill=(238,234,228)); d.text((350,925),'누구나 회원이 될 수 있다.',font=f(50),fill=(20,20,25),anchor='lm')
tag(d,1100,60); im.save(O+'o605.png')
print('ok')
