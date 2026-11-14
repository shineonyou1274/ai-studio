# 커버 3종(1080x1920): 생성 그림 + 왼쪽 위 회차 띠 + 노란 큰 글씨 2줄 + 빨간 상황 띠 + 채널명.
# 큰 글씨 한 줄은 92px 기준 약 850px(12~13자) 안. 넘치면 문구를 줄인다(폰 크기 확인 필수).
from PIL import Image,ImageDraw,ImageFont
F='/home/user/fonts/NanumGothicBold.ttf'
W,H=1080,1920
def cover(src,lines,out,focus=0.5,ep='교사X 2화',band='반려만 6번 한 교감 vs 40분 만에 뚫은 계약교사'):
    im=Image.open(src).convert('RGB')
    r=max(W/im.width,H/im.height); im=im.resize((int(im.width*r)+1,int(im.height*r)+1),Image.LANCZOS)
    x=int((im.width-W)*focus); im=im.crop((x,0,x+W,H))
    g=Image.new('L',(1,H))
    for y in range(H): g.putpixel((0,y),int(max(0,(y-H*0.45)/(H*0.55))*235))
    im.paste(Image.new('RGB',(W,H),(8,10,20)),(0,0),g.resize((W,H)))
    d=ImageDraw.Draw(im)
    f=ImageFont.truetype(F,46); d.rounded_rectangle((40,60,300,140),12,fill=(20,30,60)); d.text((62,74),ep,font=f,fill='white')
    fb=ImageFont.truetype(F,92); y=1180
    for t in lines:
        w=d.textlength(t,font=fb); d.text(((W-w)/2,y),t,font=fb,fill=(255,224,120),stroke_width=6,stroke_fill=(0,0,0)); y+=122
    fr=ImageFont.truetype(F,40)
    w=d.textlength(band,font=fr); y+=30
    d.rounded_rectangle(((W-w)/2-30,y,(W+w)/2+30,y+80),10,fill=(200,40,40)); d.text(((W-w)/2,y+14),band,font=fr,fill='white')
    fh=ImageFont.truetype(F,34); t='@twistbite_drama'; w=d.textlength(t,font=fh); d.text(((W-w)/2,H-110),t,font=fh,fill=(220,220,220))
    im.save(out)
if __name__=='__main__':
    I='/home/user/ep2/img/'
    cover(I+'i320.png',['"그건 반려가 아니라,','미로입니다"'],'/home/user/cov2/cover_A.png')
    cover(I+'i204.png',['같은 기획서,','반려만 6번째'],'/home/user/cov2/cover_B.png',0.6)
    cover(I+'i116.png',['커피 한 잔 할 시간,','"40분이면 됩니다"'],'/home/user/cov2/cover_C.png',0.5)
