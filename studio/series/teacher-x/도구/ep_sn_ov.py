# 교사X 수능 특별편: 화면 글자 그림 만들기 (샌드박스 ~/ep3 에서 실행)
# 입력 ~/ep3/img/i*.png (1520x2688) → 출력 ~/ep3/ov/*.png
from PIL import Image, ImageDraw, ImageFont, ImageFilter
H='/home/user/'; I=H+'ep3/img/'; O=H+'ep3/ov/'
F=H+'fonts/NanumGothicBold.ttf'; P=H+'fonts/NanumPen.ttf'; BH=H+'fonts/BlackHanSans-Regular.ttf'; MJ=H+'fonts/NanumMyeongjo-Bold.ttf'
def f(s,p=F): return ImageFont.truetype(p,s)
def ctext(d,box,t,font,fill):
    x0,y0,x1,y1=box; w=d.textlength(t,font=font); bb=font.getbbox(t); h=bb[3]-bb[1]
    d.text(((x0+x1-w)/2,(y0+y1-h)/2-bb[1]),t,font=font,fill=fill)
W,HH=1520,2688

# o501 휴대폰 속 가짜 커뮤니티 글 (극 중 설정, 흐리게)
im=Image.open(I+'i501.png').convert('RGB')
lay=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(lay)
x0=520; y=700
d.text((x0,y),'익명 · 3분 전',font=f(34),fill=(120,120,120,255)); y+=80
for t,s,c in [('ㅋㅋ 절대 안 걸리는',50,(20,20,20)),('방법 알려 준다',50,(20,20,20)),('',20,0),('초소형 카메라',42,(40,40,40)),('+ 쌀알 이어폰',42,(40,40,40)),('= 11만 원',42,(200,40,40)),('',20,0),('AI가 5초마다',42,(40,40,40)),('문제 풀어 줌',42,(40,40,40)),('',20,0),('이렇게 만점 근처',40,(40,40,40)),('나온 애들 수백 명임 ㅋ',40,(40,40,40)),('',20,0),('3분 있다 삭제함',36,(120,120,120))]:
    if t: d.text((x0,y),t,font=f(s),fill=c+(255,))
    y+=s+22
lay=lay.filter(ImageFilter.GaussianBlur(1.6))
im=Image.alpha_composite(im.convert('RGBA'),lay).convert('RGB'); d=ImageDraw.Draw(im)
d.rounded_rectangle((1060,1880,1440,1960),radius=16,fill=(0,0,0))
ctext(d,(1060,1880,1440,1960),'극 중 설정',f(40),'white')
im.save(O+'o501.png')

# o502 감독 배정표
im=Image.open(I+'i502.png').convert('RGB'); d=ImageDraw.Draw(im)
ctext(d,(300,660,1150,760),'수능 감독 배정표',f(70),(20,20,20))
d.line((360,790,1090,790),fill=(60,60,60),width=4)
rows=[('1교시','안정우'),('2교시','안정우'),('3교시','안정우'),('4교시','독고다해')]
y=860
for a,b in rows:
    d.text((380,y),a,font=f(58),fill=(40,40,40)); d.text((700,y),b,font=f(58),fill=(200,30,40) if b=='안정우' else (40,40,40)); y+=150
d.text((380,y+40),'※ 부정행위 적발 책임은 감독관에게',font=f(36),fill=(90,90,90))
d.rounded_rectangle((1060,2200,1440,2280),radius=16,fill=(0,0,0)); ctext(d,(1060,2200,1440,2280),'극 중 설정',f(40),'white')
im.save(O+'o502.png')

# o504 각서 (손 위쪽과 오른쪽 아래만 글자)
im=Image.open(I+'i504.png').convert('RGB'); d=ImageDraw.Draw(im)
ctext(d,(260,670,1220,770),'감독관 책임 각서',f(76,MJ),(20,20,20))
ctext(d,(260,790,1220,850),'부정행위를 놓칠 경우',f(44,MJ),(40,40,40))
ctext(d,(260,855,1220,915),'모든 책임을 본인이 진다.',f(44,MJ),(40,40,40))
d.text((880,1790),'교감 작성',font=f(42,MJ),fill=(40,40,40))
d.rounded_rectangle((1060,2380,1440,2460),radius=16,fill=(0,0,0)); ctext(d,(1060,2380,1440,2460),'극 중 설정',f(40),'white')
im.save(O+'o504.png')

# o506 폐기함 앞면 글자 (비스듬한 이름표에 맞춰 돌림)
im=Image.open(I+'i506.png').convert('RGBA')
t=Image.new('RGBA',(520,170),(0,0,0,0)); dt=ImageDraw.Draw(t); ctext(dt,(0,0,520,170),'폐기함',f(84,BH),(40,40,40,255))
t=t.rotate(-38,expand=True,resample=Image.BICUBIC)
im.alpha_composite(t,(628-t.size[0]//2,2405-t.size[1]//2)); im.convert('RGB').save(O+'o506.png')

# 사실 카드 A
im=Image.new('RGB',(W,HH),(18,22,34)); d=ImageDraw.Draw(im)
ctext(d,(0,820,W,920),'실제로 올해 수능은',f(72),(200,200,210))
ctext(d,(0,980,W,1120),'전파탐지기 없이',f(118,BH),'white')
ctext(d,(0,1140,W,1280),'맨눈 감독',f(118,BH),(255,210,120))
ctext(d,(0,1420,W,1520),"교원 82.3% '가려내기 어렵다'",f(70),'white')
ctext(d,(0,1600,W,1660),'교원 2,716명 설문 · 2026년 11월 언론 보도',f(38),(150,150,160))
im.save(O+'factA.png')

# 응원 카드 B (빈 시험실 위)
im=Image.open(I+'i901.png').convert('RGBA'); ov=Image.new('RGBA',im.size,(0,0,0,120)); im=Image.alpha_composite(im,ov).convert('RGB'); d=ImageDraw.Draw(im)
ctext(d,(0,1080,W,1220),'성실한 수험생 여러분,',f(96,BH),'white')
ctext(d,(0,1260,W,1420),'응원합니다',f(140,BH),(255,210,120))
im.save(O+'cheerB.png')

# 엔딩 포스터: 1화 안내
im=Image.open(I+'i317.png').convert('RGBA'); ov=Image.new('RGBA',im.size,(0,0,0,0)); do=ImageDraw.Draw(ov)
do.rectangle((0,1800,W,HH),fill=(0,0,0,150)); im=Image.alpha_composite(im,ov).convert('RGB'); d=ImageDraw.Draw(im)
ctext(d,(0,1880,W,2000),'교사X',f(120),'white')
ctext(d,(0,2040,W,2120),'1화  11월 20일(금) 저녁 6시',f(64),(255,210,120))
ctext(d,(0,2160,W,2220),'수능 특별편을 봐 주셔서 고맙습니다',f(40),(220,220,220))
ctext(d,(0,2500,W,2560),'@twistbite_drama',f(40),(220,220,220))
im.save(O+'poster.png')
print('ok')
