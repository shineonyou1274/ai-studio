# 교사X 5화(1등급 0명) 화면 글자 그림 (샌드박스 ~/ep6 에서 실행) → ~/ep6/ov/*.png
# 좌표는 그림에 100px 격자를 그려 잰 값(1520x2688). 표시는 왼쪽 위. 자막 띠(y 약 1900~2100)는 비운다(실수 기록 11/17).
from PIL import Image, ImageDraw, ImageFont
import os
H='/home/user/'; I=H+'ep6/img/'; O=H+'ep6/ov/'; os.makedirs(O,exist_ok=True)
F=H+'fonts/NanumGothicBold.ttf'
def f(s): return ImageFont.truetype(F,s)
def tag(d):
    d.rounded_rectangle((60,300,400,376),radius=16,fill=(0,0,0)); d.text((230,338),'극 중 설정',font=f(38),fill='white',anchor='mm')
# 601 성적 처리 화면: 위 막대 = 과목, 강조 칸 = 1등급 0명
im=Image.open(I+'i601.png').convert('RGB'); d=ImageDraw.Draw(im)
d.rectangle((240,790,1440,850),fill=(232,238,248))
d.text((260,820),'통합과학(1학년) 기말고사 · 등급 산출',font=f(40),fill=(40,50,80),anchor='lm')
d.rectangle((440,885,1080,1035),fill=(255,244,236),outline=(220,30,40),width=6)
d.text((760,925),'만점자 28명',font=f(46),fill=(60,60,60),anchor='mm')
d.text((760,995),'1등급 0명',font=f(72),fill=(220,30,40),anchor='mm')
for k,(g,n) in enumerate([('1등급','0'),('2등급','35'),('3등급','49')]):
    y=1130+k*90; d.text((300,y),g,font=f(40),fill=(50,50,50),anchor='lm'); d.text((700,y),n+'명',font=f(40),fill=(220,30,40) if n=='0' else (50,50,50),anchor='lm')
d.text((260,1560),'※ 고1 5등급제: 1등급 = 상위 10%',font=f(40),fill=(200,30,40),anchor='lm')  # v9: 위쪽 자막과 겹쳐서 화면 안으로 옮김
tag(d); im.save(O+'o601.png')
# 602 결재판: 출제 원안 검토, 결재란 3칸(담당 안정우 / 교감 서명 / 교장)
im=Image.open(I+'i602.png').convert('RGB'); d=ImageDraw.Draw(im)
d.text((560,670),'출제 원안 검토',font=f(54),fill=(30,30,30),anchor='mm')
for (x0,x1,lab) in [(412,628,'담당'),(648,860,'교감'),(888,1100,'교장')]:
    d.text(((x0+x1)/2,760),lab,font=f(34),fill=(60,60,60),anchor='mm')
d.text((520,860),'안정우',font=f(38),fill=(40,40,40),anchor='mm')
d.line((690,880,720,840,745,885,775,835,815,880),fill=(200,20,30),width=7)  # 교감 서명(빨간 사인)
for k,t in enumerate(['과목: 통합과학 (1학년)','시험: 2학기 기말고사','문항 수: 25','난이도 하 문항: 20 / 25']):
    d.text((420,1060+k*90),t,font=f(40),fill=(220,30,40) if '난이도' in t else (40,40,40),anchor='lm')
tag(d); im.save(O+'o602.png')
print('ok')
