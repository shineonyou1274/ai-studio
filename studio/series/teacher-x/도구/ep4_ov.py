# 교사X 4화(쉽게 내요) 화면 글자 그림 (샌드박스 ~/ep5 에서 실행) → ~/ep5/ov/*.png
# 좌표는 그림에 100px 격자를 그려 잰 값(1520x2688). 표시는 왼쪽 위(매뉴얼 8-1).
from PIL import Image, ImageDraw, ImageFont
import os
H='/home/user/'; I=H+'ep5/img/'; O=H+'ep5/ov/'; os.makedirs(O,exist_ok=True)
F=H+'fonts/NanumGothicBold.ttf'; FR=H+'fonts/NanumGothic.ttf' if os.path.exists(H+'fonts/NanumGothic.ttf') else F
def f(s,p=F): return ImageFont.truetype(p,s)
W,HH=1520,2688
def tag(d):
    d.rounded_rectangle((60,300,400,376),radius=16,fill=(0,0,0)); d.text((230,338),'극 중 설정',font=f(38),fill='white',anchor='mm')
def bubble(d,x0,y0,lines,me,size=34,pad=22,maxw=520,x1=None):
    fnt=f(size); w=max(d.textlength(t,font=fnt) for t in lines)+pad*2; h=len(lines)*(size+12)+pad*2-12
    if me: bx1=x1; bx0=bx1-w
    else: bx0=x0; bx1=bx0+w
    d.rounded_rectangle((bx0,y0,bx1,y0+h),radius=26,fill=(70,130,240) if me else (232,232,236))
    for k,t in enumerate(lines): d.text((bx0+pad,y0+pad+k*(size+12)),t,font=fnt,fill='white' if me else (30,30,30))
    return bx0,bx1,y0+h
# 602 낮: 정우가 보낸 문자, '읽음', 답 없음
im=Image.open(I+'i602.png').convert('RGB'); d=ImageDraw.Draw(im)
d.rectangle((470,640,1070,1590),fill=(250,250,252))
d.text((760,600),'한결',font=f(30),fill=(40,40,40),anchor='mm')
bx0,bx1,yb=bubble(d,0,1180,['한결아, 오늘 4시 반','보충이야. 꼭 와.'],True,x1=1050)
d.text((bx0-12,yb),'읽음',font=f(24),fill=(150,150,150),anchor='rd')
tag(d); im.save(O+'o602.png')
# 607 밤: 한결의 답장
im=Image.open(I+'i607.png').convert('RGB'); d=ImageDraw.Draw(im)
d.rectangle((530,900,1070,1720),fill=(250,250,252))
d.text((780,862),'한결',font=f(28),fill=(40,40,40),anchor='mm')
bubble(d,555,1240,['쌤 죄송해요.','학원 가야 해서요.'],False,size=34)
tag(d); im.save(O+'o607.png')
# 605 모니터: 시험지와 7번 문항
def doc(del_=False):
    im=Image.open(I+'i605.png').convert('RGBA'); d=ImageDraw.Draw(im)
    d.text((760,764),'통합과학 기말고사 (1학년)',font=f(46),fill=(40,50,80),anchor='mm')
    d.rectangle((268,925,1300,985),fill=(238,242,250,255))
    d.text((290,955),'7. 그래프를 해석한 것으로 옳은 것은?',font=f(36),fill=(30,30,30),anchor='lm')
    if del_:
        ov=Image.new('RGBA',im.size,(0,0,0,0)); do=ImageDraw.Draw(ov)
        do.rectangle((184,888,1336,1752),fill=(220,30,40,90),outline=(220,30,40,255),width=10)
        im=Image.alpha_composite(im,ov); d=ImageDraw.Draw(im)
        d.rounded_rectangle((470,1230,1050,1410),radius=24,fill=(220,30,40))
        d.text((760,1320),'삭제',font=f(110),fill='white',anchor='mm')
    im=im.convert('RGB'); d=ImageDraw.Draw(im); tag(d); return im
doc().save(O+'o605.png'); doc(True).save(O+'o605d.png')
# 604 서류 더미: 서류 이름표
im=Image.open(I+'i604.png').convert('RGB'); d=ImageDraw.Draw(im)
for (x,y,t) in [(330,560,'출석 독려 기록'),(760,1130,'보충지도 계획서'),(1060,1950,'결과 보고서')]:
    w=d.textlength(t,font=f(44))+50
    d.rounded_rectangle((x-w/2,y-42,x+w/2,y+42),radius=14,fill=(255,236,150),outline=(120,100,40),width=3)
    d.text((x,y),t,font=f(44),fill=(40,40,40),anchor='mm')
tag(d); im.save(O+'o604.png')
# 엔딩 포스터
im=Image.open(I+'i418.png').convert('RGBA'); ov=Image.new('RGBA',im.size,(0,0,0,0)); do=ImageDraw.Draw(ov)
do.rectangle((0,1800,W,HH),fill=(0,0,0,150)); im=Image.alpha_composite(im,ov).convert('RGB'); d=ImageDraw.Draw(im)
d.text((W/2,1940),'교사X',font=f(120),fill='white',anchor='mm')
d.text((W/2,2080),'5화  11월 27일(금) 저녁 6시',font=f(64),fill=(255,210,120),anchor='mm')
d.text((W/2,2530),'@twistbite_drama',font=f(40),fill=(220,220,220),anchor='mm')
im.save(O+'poster.png')
print('ok')
