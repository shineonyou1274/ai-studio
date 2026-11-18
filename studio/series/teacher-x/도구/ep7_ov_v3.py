# 교사X 7화 화면 글자 그림 v3 (사장님 11/18: '반려' 글자 잘림, 봉투 글자 엉망 — 원인: 눈대중 좌표·기울기 방향 반대. 이번엔 그림 픽셀로 도장·라벨의 가운데·기울기·크기를 재서 넣음: 743 도장 (764,1336) 반시계 7° 높이 155 / 744 도장 (853,1047) 반시계 7° / 744 라벨 (780,1308) 시계 12° 높이 135) / v2 (Gemini 11/18: 흰 네모가 종이·화면 질감과 따로 놂 → 덮는 칸은 그 자리 색을 재서 가장자리 흐리게, 글자는 곱하기로) / v1: (샌드박스 ~/ep8 에서 실행) → ~/ep8/ov/*.png
# 좌표는 1520x2688 그림에 격자를 그려 잰 값. 기울어진 물건은 기울기대로 돌려 붙임(실수 기록 11/18). '극 중 설정' 표시.
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import statistics
import os
H='/home/user/'; I=H+'ep8/img/'; O=H+'ep8/ov/'; os.makedirs(O,exist_ok=True)
F=H+'fonts/NanumGothicBold.ttf'; PEN=H+'fonts/NanumPen.ttf'
def f(s,p=F): return ImageFont.truetype(p,s)
def tag(d,x=60,y=120):
    d.rounded_rectangle((x,y,x+340,y+76),radius=16,fill=(0,0,0)); d.text((x+170,y+38),'극 중 설정',font=f(38),fill='white',anchor='mm')
def tilted(im,center,lines,size,angle,fill=(25,25,35),bg=None,pad=12,gap=1.3,align='mm',width=None,font=F):
    ft=f(size,font); lh=int(size*gap)
    w=width or int(max(ft.getlength(l) for l in lines))+pad*2; h=lh*len(lines)+pad*2
    L=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(L)
    if bg: d.rounded_rectangle((0,0,w-1,h-1),radius=pad,fill=bg)
    for k,l in enumerate(lines):
        y=pad+lh*k+lh/2
        d.text((pad,y) if align=='lm' else (w/2,y),l,font=ft,fill=fill,anchor='lm' if align=='lm' else 'mm')
    R=L.rotate(angle,resample=Image.BICUBIC,expand=True)
    im.paste(R,(int(center[0]-R.width/2),int(center[1]-R.height/2)),R)

def patch(im,box,feather=5):
    """box 자리를 그 둘레 색(가운데값)으로 덮되 가장자리를 흐리게 — 종이·화면 질감과 어울리게"""
    x0,y0,x1,y1=box; reg=im.crop((x0,y0,x1,y1)).convert('RGB'); px=list(reg.getdata())
    c=tuple(int(statistics.median([p[i] for p in px])) for i in range(3))
    M=Image.new('L',im.size,0); ImageDraw.Draw(M).rectangle(box,fill=255); M=M.filter(ImageFilter.GaussianBlur(feather))
    im.paste(Image.new('RGB',im.size,c),(0,0),M); return c
def mtext(im,xy,t,size,fill=(30,30,35),anchor='lm',font=None):
    """곱하기(Multiply)로 글자를 얹음 — 인쇄된 것처럼"""
    L=Image.new('RGB',im.size,(255,255,255)); ImageDraw.Draw(L).text(xy,t,font=f(size,font or F),fill=fill,anchor=anchor)
    im.paste(ImageChops.multiply(im.convert('RGB'),L))
# 741 동영상 사이트(모니터 정면): 검색줄·영상 제목·썸네일 글
im=Image.open(I+'i741.png').convert('RGB')
patch(im,(120,615,1290,670)); mtext(im,(135,642),'학맞통 우수사례',38,(40,40,50))
patch(im,(120,1305,1330,1395)); mtext(im,(130,1330),'[학맞통 우수사례] 학생 집 보일러',38); mtext(im,(130,1375),'고쳐 준 선생님',38)
patch(im,(125,1650,720,1700)); mtext(im,(130,1675),'주말마다 고기 구워 주기',34)
patch(im,(745,1650,1200,1700)); mtext(im,(750,1675),'가정 방문 보고서 30장',34)
d=ImageDraw.Draw(im)
tag(d); im.save(O+'o741.png')
# 742 화이트보드 업무분장표: 칸을 지우고 마커 글씨로 다시 씀(다른 이름은 빨간 줄로 지우고 전부 독고다해)
im=Image.open(I+'i742.png').convert('RGB'); d=ImageDraw.Draw(im)
d.rectangle((300,690,1290,1410),fill=(246,247,248))
d.text((795,735),'2학기 업무분장',font=f(64,PEN),fill=(20,20,30),anchor='mm')
d.line((320,780,1270,780),fill=(40,40,50),width=4); d.line((760,780,760,1400),fill=(40,40,50),width=4)
rows=[('학맞통(학생맞춤통합지원)','안정우'),('위원회 회의록','김○○'),('가정 방문','박○○'),('행사 준비','이○○'),('공문 취합','최○○'),('학부모 상담 기록','정○○')]
for k,(job,old) in enumerate(rows):
    y=835+k*95
    d.text((340,y),job,font=f(48,PEN),fill=(20,20,30),anchor='lm')
    d.text((790,y),old,font=f(46,PEN),fill=(90,90,100),anchor='lm'); w=f(46,PEN).getlength(old)
    d.line((785,y,795+w,y),fill=(210,30,40),width=6)
    d.text((1000,y),'독고다해',font=f(50,PEN),fill=(200,25,35),anchor='lm')
    if k<5: d.line((320,y+47,1270,y+47),fill=(170,170,180),width=2)
tag(d); im.save(O+'o742.png')
# 743 출장 신청서(위에서) + 빨간 '반려' 도장(약 -10° → 반시계 10°)
im=Image.open(I+'i743.png').convert('RGB')
patch(im,(262,590,560,620)); mtext(im,(270,605),'출장 신청서',34)
patch(im,(262,700,1150,738)); mtext(im,(272,719),'연수: 학맞통 담당자 연수',34)
patch(im,(300,830,1150,860)); mtext(im,(305,845),'신청자: 독고다해(계약)  ·  출장비: 신청',30)
d=ImageDraw.Draw(im)
tilted(im,(764,1336),['반 려'],104,7,fill=(205,25,35))
tag(d,1100,60); im.save(O+'o743.png')
# 744 재단 공문 봉투: 빨간 도장 '인사', 흰 라벨(봉투 약 -8° → 반시계 8°)
im=Image.open(I+'i744.png').convert('RGB')
tilted(im,(853,1047),['인사'],96,7,fill=(195,25,35))
tilted(im,(780,1308),['학교법인 이사회','친 전'],44,-12,fill=(40,35,30),gap=1.3)
tag(ImageDraw.Draw(im),60,120); im.save(O+'o744.png')
# 746 공문: 제목·본문 몇 줄·형광펜 두 줄(약 -4° → 반시계 4°)
im=Image.open(I+'i746.png').convert('RGB')
tilted(im,(860,575),['학생맞춤통합지원 운영 안내'],46,3,fill=(30,30,35))
tilted(im,(870,1600),['※ 담당 교사 1인이 아닌 위원회로 운영','※ 위원장: 교감'],44,4,fill=(20,20,25),align='lm',width=900,gap=1.5)
tag(ImageDraw.Draw(im),60,120); im.save(O+'o746.png')
# 736 마지막 프레임: 2K 원본에서 다해 얼굴 쪽을 9:16으로(영상 확대는 뭉개짐)
im=Image.open(I+'i736.png').convert('RGB'); W,Hh=im.size
cw=int(W*0.6); ch=int(cw*16/9); x0=int(W*0.1); y0=int(Hh*0.03); im.crop((x0,y0,x0+cw,y0+ch)).resize((1520,2688),Image.LANCZOS).save(O+'o736f.png')
print('ok')
