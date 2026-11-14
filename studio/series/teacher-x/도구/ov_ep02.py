# 교사X 2화 글자 카드·화면 글자 만들기 예시(반려 팝업, 최종 승인, 기안 도착, 반려 사유표, 초과근무 막대, 엔딩 포스터).
# 글자를 얹을 그림은 처음부터 정면(카메라와 평행)으로 그린다. 비스듬한 화면이면 네 모서리 원근 변형으로 얹는다.
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
F='/home/user/fonts/NanumGothicBold.ttf'; P='/home/user/fonts/NanumPen.ttf'
def f(s,p=F): return ImageFont.truetype(p,s)
def ctext(d,box,t,font,fill):
    x0,y0,x1,y1=box; w=d.textlength(t,font=font); bb=font.getbbox(t); h=bb[3]-bb[1]
    d.text(((x0+x1-w)/2,(y0+y1-h)/2-bb[1]),t,font=font,fill=fill)
I='img/'
# 01 rejection popup
im=Image.open(I+'i301.png').convert('RGB'); d=ImageDraw.Draw(im)
ctext(d,(410,903,1123,965),'에듀파인 · 결재 알림',f(40),'white')
ctext(d,(410,1000,1123,1090),'반  려',f(96),(200,30,40))
ctext(d,(410,1110,1123,1170),'공모사업 기획서(안) · 6차',f(40),(60,60,60))
ctext(d,(410,1190,1123,1250),'사유: 문맥을 다시 볼 것',f(40),(60,60,60))
ctext(d,(663,1330,878,1389),'확인',f(38),'white')
d.text((1180,620),'15:00',font=f(44),fill=(70,70,70))
im.save('ov/o01.png')
# 25 final approval on same monitor, green bar
im=Image.open(I+'i301.png').convert('RGB'); px=im.load()
for y in range(895,975):
    for x in range(400,1130):
        r,g,b=px[x,y]
        if r>150 and g<110 and b<110: px[x,y]=(40,150,80)
for y in range(1320,1400):
    for x in range(650,890):
        r,g,b=px[x,y]
        if r>150 and g<110 and b<110: px[x,y]=(40,150,80)
d=ImageDraw.Draw(im)
ctext(d,(410,903,1123,965),'에듀파인 · 결재 알림',f(40),'white')
ctext(d,(410,1000,1123,1090),'최종 승인',f(90),(30,130,60))
ctext(d,(410,1130,1123,1200),'공모사업 기획서(안)',f(42),(60,60,60))
ctext(d,(663,1330,878,1389),'확인',f(38),'white')
d.text((1180,620),'16:52',font=f(44),fill=(70,70,70))
ImageEnhance.Color(im).enhance(1.0).save('ov/o25.png')
# 13 draft arrived (vp office monitor)
im=Image.open(I+'i314.png').convert('RGB'); d=ImageDraw.Draw(im)
d.rectangle((1080,1468,1366,1568),fill='white',outline=(200,200,200))
ctext(d,(1080,1470,1366,1520),'기안 도착',f(32),(200,60,40))
ctext(d,(1080,1518,1366,1566),'독고다해 · 15:40',f(26),(80,80,80))
ctext(d,(587,1250,772,1300),'결재',f(32),'white')
im.save('ov/o13.png')
im2=Image.open(I+'i314.png').convert('RGB'); d=ImageDraw.Draw(im2)
ctext(d,(587,1250,772,1300),'승인',f(34),'white')
d.rectangle((1080,1468,1366,1568),fill='white',outline=(200,200,200))
ctext(d,(1080,1490,1366,1546),'결재 완료',f(34),(30,130,60))
im2.save('ov/o24.png')
# table card
W,H=1520,2688; im=Image.new('RGB',(W,H),(246,243,235)); d=ImageDraw.Draw(im)
ctext(d,(0,180,W,280),'공모사업 기획서 반려 사유',f(72),(20,20,20))
ctext(d,(0,290,W,350),'(극 중 설정)',f(40),(120,120,120))
rows=[('1차','목적이 불분명함'),('2차','강사료 항목 새로 만들 것'),('3차','강사료 → 운영비로 옮길 것'),('4차','문맥에 맞게 고칠 것'),('5차','왜 운영비로 옮겼나? 원래대로'),('6차','강사료 항목 지울 것')]
y=420; RH=300
for i,(a,b) in enumerate(rows):
    d.rectangle((80,y,W-80,y+RH),outline=(60,60,60),width=4)
    d.line((300,y,300,y+RH),fill=(60,60,60),width=4)
    ctext(d,(80,y,300,y+RH),a,f(64),(20,20,20)); d.text((340,y+RH/2-34),b,font=f(58),fill=(20,20,20))
    d.text((W-260,y+RH/2-40),'반려',font=f(56),fill=(200,30,40))
    y+=RH
im.save('ov/table.png')
# (c3·c5·c26 칸 카드는 표 한 칸을 큰 글씨로 다시 그리고 빨간 밑줄 — v4A에서 따로 만듦)
# overtime bar card
im=Image.new('RGB',(W,H),(24,26,34)); d=ImageDraw.Draw(im)
ctext(d,(0,260,W,360),'안정우 선생님 초과근무',f(70),'white')
ctext(d,(0,370,W,430),'(극 중 설정)',f(40),(150,150,150))
x0,x1=200,1400; t0,t1=16.5,23.5
def X(t): return x0+(t-t0)/(t1-t0)*(x1-x0)
for t in range(17,24):
    d.line((X(t),560,X(t),2000),fill=(60,62,72),width=2); ctext(d,(X(t)-60,2010,X(t)+60,2070),f'{t}시',f(36),(160,160,160))
data=[('1주',16+40/60,22.5,21+38/60,'21:38'),('2주',16+40/60,23+10/60,22+47/60,'22:47'),('3주',16+40/60,22+5/60,21+52/60,'21:52')]
y=700
for lab,s,e,r,rt in data:
    d.text((60,y+10),lab,font=f(48),fill='white')
    d.rounded_rectangle((X(s),y,X(e),y+110),radius=20,fill=(120,124,140))
    cx=X(r); d.ellipse((cx-34,y+21,cx+34,y+89),fill=(230,40,50))
    ctext(d,(cx-160,y+125,cx+160,y+185),'반려 '+rt,f(40),(255,90,90))
    y+=420
ctext(d,(0,2150,W,2230),'회색 = 초과근무   빨간 점 = 반려 시각',f(44),(200,200,200))
im.save('ov/bars.png')
# end poster
im=Image.open(I+'i127.png').convert('RGB'); ov=Image.new('RGBA',im.size,(0,0,0,0)); do=ImageDraw.Draw(ov)
do.rectangle((0,1800,W,H),fill=(0,0,0,150)); im=Image.alpha_composite(im.convert('RGBA'),ov).convert('RGB'); d=ImageDraw.Draw(im)
ctext(d,(0,1900,W,2020),'교사X',f(120),'white')
ctext(d,(0,2060,W,2140),'3화  12월 2일(수) 저녁 6시',f(64),(255,210,120))
ctext(d,(0,2500,W,2560),'@twistbite_drama',f(40),(220,220,220))
im.save('ov/poster2.png')
print('ok')
