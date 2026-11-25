# 교사X 10화 화면 글자 그림 — 정면 평면 화면(코드로 그림, 삐뚤어짐 없음). 왼쪽 위 캡션(y<230)·아래 자막 자리(y>2230) 비움
# 샌드박스 ~/ep11 에서 실행 → ~/ep11/ov/
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
H='/home/user/'; I=H+'ep11/img/'; O=H+'ep11/ov/'; os.makedirs(O,exist_ok=True)
F=H+'fonts/NanumGothicBold.ttf'; FR=H+'fonts/NanumGothic.ttf'; PEN=H+'fonts/NanumPen.ttf'
W,HH=1520,2688
def f(s,p=F): return ImageFont.truetype(p,s)
def bg(name,dark=0.45,blur=18):
    b=Image.open(I+name).convert('RGB').resize((W,HH)).filter(ImageFilter.GaussianBlur(blur)).convert('RGBA')
    b.alpha_composite(Image.new('RGBA',(W,HH),(0,0,0,int(255*dark)))); return b
def box(im,b,r,fill,sh=24):
    s=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(s); d.rounded_rectangle((b[0]+12,b[1]+18,b[2]+12,b[3]+18),r,fill=(0,0,0,110))
    im.alpha_composite(s.filter(ImageFilter.GaussianBlur(sh))); ImageDraw.Draw(im).rounded_rectangle(b,r,fill=fill)
def tag(im,x=1080,y=300):
    d=ImageDraw.Draw(im); d.rounded_rectangle((x,y,x+340,y+76),16,fill=(0,0,0)); d.text((x+170,y+38),'극 중 설정',font=f(38),fill='white',anchor='mm')
def stamp(im,cx,cy,lines,ang=-12,col=(215,30,30)):
    L=Image.new('RGBA',(980,330),(0,0,0,0)); d=ImageDraw.Draw(L)
    d.rounded_rectangle((10,10,970,320),30,outline=col+(255,),width=14)
    for k,t in enumerate(lines): d.text((490,100+k*120),t,font=f(78),fill=col+(255,),anchor='mm')
    R=L.rotate(ang,resample=Image.BICUBIC,expand=True); im.alpha_composite(R,(int(cx-R.width/2),int(cy-R.height/2)))
def strike(im,x0,x1,y,col=(215,25,25),w=12):
    ImageDraw.Draw(im).line((x0,y,x1,y+6),fill=col,width=w)
# 1 공문함 — 새 공문 없음
im=bg('i102.png',0.5,24); box(im,(260,300,1260,2180),100,(16,18,26,255),30); d=ImageDraw.Draw(im)
d.rounded_rectangle((292,332,1228,2148),80,fill=(245,246,250))
d.text((760,470),'07:52',font=f(70),fill=(40,40,55),anchor='mm')
d.text((360,640),'업무 메일 · 공문함',font=f(56),fill=(30,40,80),anchor='lm'); d.line((340,720,1180,720),fill=(210,212,220),width=4)
d.text((760,1180),'↻',font=f(200,FR),fill=(150,155,170),anchor='mm')
d.text((760,1430),'새 공문 없음',font=f(96),fill=(30,30,40),anchor='mm')
d.text((760,1560),'(정정 공문 0건)',font=f(52,FR),fill=(200,40,40),anchor='mm')
im.convert('RGB').save(O+'o_inbox.png')
# 2 책임자 칸만 있는 서류 3장
docs=[('현장체험학습 운영 계획서',['일시 · 장소','인솔 교사','이동 경로','비상 연락망'],'책임자: 담임 안정우'),
      ('교내 상장 공적조서',['수상자','공적 요지','추천 사유','심사 의견'],'작성 책임: 담임'),
      ('학부모 참가 동의서 회수 대장',['학년 · 반','회수 수','미회수 사유','확인'],'회수 책임: 담임 교사')]
for k,(title,rows,resp) in enumerate(docs):
    im=bg('i105.png',0.4,20); box(im,(120,330,1400,2120),30,(252,252,248,255)); d=ImageDraw.Draw(im)
    d.text((760,470),title,font=f(66),fill=(25,25,35),anchor='mm'); d.line((200,560,1320,560),fill=(60,60,70),width=5)
    y=640
    for r in rows:
        d.rectangle((200,y,1320,y+150),outline=(120,120,130),width=4); d.text((240,y+75),r,font=f(50,FR),fill=(60,60,70),anchor='lm')
        d.rounded_rectangle((660,y+60,660+[520,440,560,480][rows.index(r)],y+90),10,fill=(215,218,225)); y+=170
    d.rectangle((190,y+60,1330,y+250),fill=(255,232,232)); d.rectangle((190,y+60,1330,y+250),outline=(215,25,25),width=10)
    d.text((240,y+155),resp,font=f(70),fill=(200,20,20),anchor='lm')
    im.convert('RGB').save(O+f'o_resp{k+1}.png')
# 3 다음을 위한 한 장
im=bg('i105.png',0.4,20); box(im,(120,330,1400,2150),30,(252,252,248,255)); d=ImageDraw.Draw(im)
d.text((760,480),'다음을 위한 한 장',font=f(84),fill=(25,25,35),anchor='mm'); d.line((200,580,1320,580),fill=(60,60,70),width=5)
for k,(t,c) in enumerate([('좋았던 것',(40,120,70)),('바꿀 것',(40,70,160))]):
    y=650+k*420; d.rectangle((200,y,1320,y+360),outline=(120,120,130),width=4); d.text((240,y+60),t,font=f(60),fill=c,anchor='lm')
    for j in range(2): d.rounded_rectangle((240,y+150+j*90,240+[900,700][j],y+180+j*90),10,fill=(215,218,225))
y=1500; d.text((240,y+30),'사진 3장',font=f(60),fill=(150,80,20),anchor='lm')
for j in range(3):
    x=220+j*370; d.rectangle((x,y+100,x+330,y+480),fill=(222,228,236),outline=(150,155,170),width=4); d.text((x+165,y+290),'📷' if False else '사진',font=f(46,FR),fill=(150,155,170),anchor='mm')
tag(im,1060,250); im.convert('RGB').save(O+'o_one.png')
# 4 안전점검표 a/b
def safety(b):
    im=bg('i105.png',0.45,20); box(im,(120,330,1400,2120),30,(252,252,248,255)); d=ImageDraw.Draw(im)
    d.text((760,470),'체험학습 안전점검표',font=f(72),fill=(25,25,35),anchor='mm'); d.line((200,560,1320,560),fill=(60,60,70),width=5)
    y=630
    for r in ['차량 · 기사 확인','이동 경로 위험 요소','숙소 · 시설 점검','비상 의료 대책']:
        d.rectangle((200,y,1320,y+140),outline=(120,120,130),width=4); d.text((240,y+70),r,font=f(50,FR),fill=(60,60,70),anchor='lm')
        d.rectangle((1180,y+40,1240,y+100),outline=(90,90,100),width=5); y+=160
    d.text((240,y+110),'작성: 담임',font=f(72),fill=(30,30,40),anchor='lm')
    if b:
        strike(im,230,640,y+110); stamp(im,760,y+430,['전문업체 위탁','안전 보험 가입'])
    tag(im,1060,250); return im.convert('RGB')
safety(False).save(O+'o_safety_a.png'); safety(True).save(O+'o_safety_b.png')
# 5 업무분장표 a/b
def duty(b):
    im=bg('i105.png',0.45,20); box(im,(100,330,1420,2120),30,(252,252,248,255)); d=ImageDraw.Draw(im)
    d.text((760,470),'업무분장표 (공개)',font=f(72),fill=(25,25,35),anchor='mm')
    d.rectangle((160,580,1360,680),fill=(52,92,160)); d.text((420,630),'업무',font=f(52),fill='white',anchor='mm'); d.text((1000,630),'담당',font=f(52),fill='white',anchor='mm')
    rows=[('교육과정','교과협의회'),('학맞통','독고다해(계약)'),('생활지도','학년부'),('수업 결손 보강','교장 · 교감')]; y=680
    for k,(a,c) in enumerate(rows):
        d.rectangle((160,y,1360,y+190),outline=(140,140,150),width=4); d.line((680,y,680,y+190),fill=(140,140,150),width=4)
        hl=(k==1)
        if hl and not b: d.rectangle((684,y+4,1356,y+186),fill=(255,243,190))
        d.text((420,y+95),a,font=f(58 if hl else 52,F if hl else FR),fill=(30,30,40),anchor='mm'); d.text((1020,y+95),c,font=f(56 if hl else 50,F if hl else FR),fill=(30,30,40),anchor='mm')
        if hl and b:
            strike(im,760,1280,y+95,w=14); d=ImageDraw.Draw(im); d.text((1020,y+28),'교감',font=f(120,PEN),fill=(210,20,20),anchor='mm')
        y+=190
    tag(im,1060,250); return im.convert('RGB')
duty(False).save(O+'o_duty_a.png'); duty(True).save(O+'o_duty_b.png')
# 6 교무실 TV 뉴스 자막
im=bg('i1261.png',0.35,16); d=ImageDraw.Draw(im)
box(im,(60,640,1460,1560),24,(20,20,24,255),20); d=ImageDraw.Draw(im)
g=Image.new('RGB',(1340,860),(60,70,90)); gd=ImageDraw.Draw(g)
for yy in range(860): gd.line((0,yy,1340,yy),fill=(40+yy//30,55+yy//40,80+yy//25))
im.paste(g,(90,670)); d=ImageDraw.Draw(im)
d.rectangle((90,1240,1430,1530),fill=(250,250,250)); d.rectangle((90,1240,330,1530),fill=(200,20,20))
d.text((210,1385),'뉴스',font=f(70),fill='white',anchor='mm')
d.text((370,1330),'AI 부정행위 적발 시',font=f(66),fill=(20,20,30),anchor='lm'); d.text((370,1440),'당일 전 과목 0점 권고',font=f(66),fill=(200,20,20),anchor='lm')
im.convert('RGB').save(O+'o_tv.png')
# 7 이사장 책상 메모
im=Image.open(I+'i131.png').convert('RGB').resize((W,HH)).filter(ImageFilter.GaussianBlur(10)).convert('RGBA')
im.alpha_composite(Image.new('RGBA',(W,HH),(40,15,0,90)))
card=Image.new('RGBA',(1100,700),(250,244,228,255)); cd=ImageDraw.Draw(card)
for yy in range(160,700,110): cd.line((60,yy,1040,yy),fill=(210,200,180),width=3)
cd.text((90,140),'설립자 손녀',font=f(110,PEN),fill=(30,40,90),anchor='lm'); cd.text((90,330),'— 해외 체류 중',font=f(110,PEN),fill=(30,40,90),anchor='lm'); cd.text((90,520),'(귀국 미정)',font=f(90,PEN),fill=(170,40,40),anchor='lm')
R=card.rotate(-5,resample=Image.BICUBIC,expand=True); box(im,(220,1000,1300,1680),20,(0,0,0,0),30); im.alpha_composite(R,(int(760-R.width/2),int(1340-R.height/2)))
im.convert('RGB').save(O+'o_memo.png')
# 8 AI 답(틀린 문장에 빨간 동그라미)
im=bg('i128.png',0.3,14); box(im,(110,500,1410,1900),30,(255,255,255,255)); d=ImageDraw.Draw(im)
d.text((170,600),'AI의 답',font=f(56),fill=(60,70,120),anchor='lm')
for k,t in enumerate(['광합성은 빛 에너지를','화학 에너지로 바꾸는 과정이다.','광합성은 밤에 더 활발하다.','잎의 엽록체에서 일어난다.']):
    d.text((180,780+k*230),t,font=f(64,FR),fill=(30,30,40),anchor='lm')
d.ellipse((140,1170,1330,1350),outline=(215,25,25),width=12)
d.text((1350,1440),'틀렸다!',font=f(96,PEN),fill=(215,25,25),anchor='rm')
im.convert('RGB').save(O+'o_ai.png')
print('ok',sorted(os.listdir(O)))
