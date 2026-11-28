# 11/28 커버 띠만 새 제목(2줄)으로 덮어 그림 — 확정 커버 PNG 위 남색 띠(0~230px) 다시 그림. 샌드박스 ~/cov2 에서 실행
from PIL import Image, ImageDraw, ImageFont
F='/home/user/fonts/BlackHanSans-Regular.ttf'; NAVY=(16,28,58); YEL=(255,214,0); W=1080
T={'6':['이 정도면','직장 내 괴롭힘 인정?'],'7':['고기 굽고 보일러','놔주는 업무도 있다?'],'8':['선택과목 수 많아지면','좋은 거 맞나?'],
'9':['AI가 쓴 과제 제출에','대처하는 법'],'10':['계획서, 보고서는','누구를 위해 작성하는가'],'11':['화장실 청소를','엄마가 대신?']}
for k in ['6','7','8','9','10','11A','11B','11C']:
    n=k.rstrip('ABC'); im=Image.open(f'src{k}.png').convert('RGB'); d=ImageDraw.Draw(im)
    d.rectangle((0,0,W,230),fill=NAVY)
    fl=ImageFont.truetype(F,92); d.text((50,62),'교사X',font=fl,fill='white'); x=50+fl.getlength('교사X')+26
    fn=ImageFont.truetype(F,80); s=f'{n}화'; nw=fn.getlength(s)
    d.rounded_rectangle((x,56,x+nw+40,176),18,fill=YEL); d.text((x+20,70),s,font=fn,fill=NAVY); x+=nw+40+28
    L=T[n]; ft=72
    while max(ImageFont.truetype(F,ft).getlength(l) for l in L)>W-x-36: ft-=2
    f=ImageFont.truetype(F,ft); gap=int(ft*1.12); y0=116-gap//2
    for i,l in enumerate(L): d.text((x,y0+i*gap),l,font=f,fill='white',anchor='lm')
    im.save(f'cover{k}_t2.png')
