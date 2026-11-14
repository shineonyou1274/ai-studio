# 반려 사유표 다시 그리기: 줄 높이 300 → 250. 표가 화면 위쪽 71% 안에 들어와 아래 대사 자막(23% 위치)과 겹치지 않게. 샌드박스 ~/ep2 에서 실행.
from PIL import Image, ImageDraw, ImageFont
F='/home/user/fonts/NanumGothicBold.ttf'
def f(s): return ImageFont.truetype(F,s)
def ctext(d,box,t,font,fill):
    x0,y0,x1,y1=box; w=d.textlength(t,font=font); bb=font.getbbox(t); h=bb[3]-bb[1]
    d.text(((x0+x1-w)/2,(y0+y1-h)/2-bb[1]),t,font=font,fill=fill)
W,H=1520,2688; im=Image.new('RGB',(W,H),(246,243,235)); d=ImageDraw.Draw(im)
ctext(d,(0,180,W,280),'공모사업 기획서 반려 사유',f(72),(20,20,20))
ctext(d,(0,290,W,350),'(극 중 설정)',f(40),(120,120,120))
rows=[('1차','목적이 불분명함'),('2차','강사료 항목 새로 만들 것'),('3차','강사료 → 운영비로 옮길 것'),('4차','문맥에 맞게 고칠 것'),('5차','왜 운영비로 옮겼나? 원래대로'),('6차','강사료 항목 지울 것')]
y=400; RH=250
for a,b in rows:
    d.rectangle((80,y,W-80,y+RH),outline=(60,60,60),width=4); d.line((300,y,300,y+RH),fill=(60,60,60),width=4)
    ctext(d,(80,y,300,y+RH),a,f(64),(20,20,20)); d.text((340,y+RH/2-34),b,font=f(58),fill=(20,20,20))
    d.text((W-260,y+RH/2-40),'반려',font=f(56),fill=(200,30,40)); y+=RH
im.save('ov/table.png'); print('table bottom px(of 1280):', round(y/H*1280))
