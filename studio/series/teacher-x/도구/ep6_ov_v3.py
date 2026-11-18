# 교사X 6화 화면 글자 그림 v3 (사장님 11/18: 명판이 비어 어색함 → 한자 '設立者' 새김 + 이름 자리는 뭉갠 글씨) / v2 (사장님 11/18: "전화 화면 글자 위치 삐뚤고, 친목회 종이 글자도 삐뚤어 / 이사장 사진 밑에 텍스트가 아무것도 없어서 끄적끄적이라도 표시해 / 마지막 다해 얼굴 뭉개짐")
# → 폰(약 7° 기울기)·종이(약 5.7°) 글자를 그 기울기대로 돌려서 얹음. 설립자 액자 명판에 읽히지 않는 새김 글씨. 마지막 얼굴은 2K 원본 그림에서 잘라 냄(o508f).
# 좌표는 1520x2688 그림에 격자를 그려 잰 값. 샌드박스 ~/ep7 에서 실행 → ~/ep7/ov/*.png
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, random
H='/home/user/'; I=H+'ep7/img/'; O=H+'ep7/ov/'; os.makedirs(O,exist_ok=True)
F=H+'fonts/NanumGothicBold.ttf'
def f(s): return ImageFont.truetype(F,s)
def tag(d,x=60,y=300):
    d.rounded_rectangle((x,y,x+340,y+76),radius=16,fill=(0,0,0)); d.text((x+170,y+38),'극 중 설정',font=f(38),fill='white',anchor='mm')
def tilted(im,center,lines,size,angle,fill=(25,25,35),bg=None,pad=14,gap=1.25,align='mm',width=None):
    """글자 묶음을 투명 판에 그린 뒤 angle(도, 반시계)만큼 돌려 center에 붙인다."""
    ft=f(size); lh=int(size*gap)
    w=width or int(max(ft.getlength(l) for l in lines))+pad*2; h=lh*len(lines)+pad*2
    L=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(L)
    if bg: d.rounded_rectangle((0,0,w-1,h-1),radius=pad,fill=bg)
    for k,l in enumerate(lines):
        y=pad+lh*k+lh/2
        if align=='lm': d.text((pad,y),l,font=ft,fill=fill,anchor='lm')
        else: d.text((w/2,y),l,font=ft,fill=fill,anchor='mm')
    R=L.rotate(angle,resample=Image.BICUBIC,expand=True)
    im.paste(R,(int(center[0]-R.width/2),int(center[1]-R.height/2)),R)
# 601 컴퓨터 메신저(모니터는 정면이라 v1 그대로)
im=Image.open(I+'i601.png').convert('RGB'); d=ImageDraw.Draw(im)
d.rectangle((415,618,700,672),fill=(244,246,252)); d.text((420,645),'교감',font=f(44),fill=(30,40,70),anchor='lm')
d.rounded_rectangle((415,755,1395,1075),radius=26,fill=(255,255,255),outline=(200,206,222),width=3)
for k,t in enumerate(['계약직은 친목회원이 아닙니다.','회식에 참여 희망하시면','별도 회비를 내세요.']):
    d.text((455,815+k*92),t,font=f(52),fill=(20,20,30),anchor='lm')
d.text((430,1115),'오후 2:58',font=f(32),fill=(120,126,140),anchor='lm')
tag(d,60,120); im.save(O+'o601.png')
# 602 교직원 단체방(폰, 약 7° 기울어짐: 말풍선 아래 변 (590,1192)→(1010,1140))
A2=7.0
im=Image.open(I+'i602.png').convert('RGB')
bb=im.getpixel((1050,745)); bb=tuple(bb)+(255,)
tilted(im,(800,752),['교직원 친목회','오늘 회식 6시!'],30,A2,fill=(30,30,40),bg=bb,pad=10,gap=1.2,align='lm',width=330)
tilted(im,(760,962),['교직원 친목회 (38)'],32,A2,fill=(255,255,255))
for c,ls in [((810,1112),['오늘 친목회 회식','6시 OO갈비']),((835,1292),['1차는 친목회비로!']),((875,1470),['다들 오시죠?']),
             ((1005,1622),['참석합니다!']),((838,1775),['저도요~']),((878,1903),['6시에 봬요'])]:
    tilted(im,c,ls,38,A2)
tag(ImageDraw.Draw(im),60,120); im.save(O+'o602.png')
# 604 설립자 액자 명판: 읽히지 않는 새김 글씨(이름은 다음 화에, 사장님 11/17)
im=Image.open(I+'i604.png').convert('RGB')
L=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(L); random.seed(6)
import glob
HZ=([p for p in glob.glob('/usr/share/fonts/**/ipam*.ttf',recursive=True)]+glob.glob('/usr/share/fonts/**/ipag.ttf',recursive=True))[0]
ImageDraw.Draw(L).text((780,1673),'設 立 者',font=ImageFont.truetype(HZ,30),fill=(58,42,20,215),anchor='mm')
for y0,x0,x1,amp in [(1706,712,850,3)]:
    x=x0
    while x<x1:
        n=random.randint(3,6); pts=[]
        for k in range(n*3): pts.append((x+k*3,y0+(amp if k%2 else -amp)*random.uniform(0.3,1.0)))
        d.line(pts,fill=(60,44,22,170),width=2); x+=n*9+random.randint(7,13)
L=L.filter(ImageFilter.GaussianBlur(1.0)); im.paste(L,(0,0),L); im.save(O+'o604.png')
# 605 교직원 친목회 회칙(종이 약 5.7° 기울어짐: 제목 줄 (412,725)→(1062,657), 형광펜 (350,887)→(1125,800))
A5=5.7
im=Image.open(I+'i605.png').convert('RGB'); d=ImageDraw.Draw(im)
paper=tuple(im.getpixel((318,930)))
tilted(im,(737,640),['교직원 친목회 회칙'],60,A5,fill=(25,25,30))
Mk=Image.new('L',im.size,0); ImageDraw.Draw(Mk).rectangle((294,862,346,922),fill=255); Mk=Mk.filter(ImageFilter.GaussianBlur(6)); im.paste(Image.new('RGB',im.size,paper),(0,0),Mk)  # '1.' 번호를 가장자리 흐리게 지움
tilted(im,(770,875),['제2조(회원) 본교 교직원은','누구나 회원이 될 수 있다.'],50,A5,fill=(20,20,25),bg=None,pad=8,gap=1.35,align='lm',width=800)
# 형광펜은 첫 줄 아래에 다시(글자 판이 덮지 않게 반투명 노랑)
L=Image.new('RGBA',im.size,(0,0,0,0)); ImageDraw.Draw(L).polygon([(372,872),(1150,795),(1152,822),(374,899)],fill=(255,236,60,110)); im.paste(L,(0,0),L)
tag(ImageDraw.Draw(im),1100,60); im.save(O+'o605.png')
# 508 마지막 프레임: 2K 원본에서 다해 얼굴 쪽을 9:16으로 잘라 냄(영상 확대로 뭉개지던 것 대신)
im=Image.open(I+'i508.png').convert('RGB'); W,Hh=im.size
cw=int(W*0.55); ch=int(cw*16/9); x0=200; y0=120; im.crop((x0,y0,x0+cw,y0+ch))  # 얼굴 가운데·빨간 만년필 보이게(x0 100·200 견줘 봄).resize((1520,2688),Image.LANCZOS).save(O+'o508f.png')
print('ok')
