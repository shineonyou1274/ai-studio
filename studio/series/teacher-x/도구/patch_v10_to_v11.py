# 2화 v10 → v11 (사장님 0:31 캡처: 다해 이름표가 정우 화면에 뜸 / 사장님이 녹음한 키보드 소리). 크레딧 0
import sys
s=open(sys.argv[1]).read()
def R(a,b):
    global s
    assert s.count(a)==1, ('not unique/missing', a[:80], s.count(a))
    s=s.replace(a,b)
# 1) 다해 이름표는 06에서 다해 듣는 화면(206, 06 시작 +3.5초)이 시작될 때 뜨고, 06이 끝나면(정우 07 전) 사라짐
R("MK['tag_dh']=T-1.65","MK['tag_dh']=MK['t06']+3.5; MK['tag_end']=T")
R("(MK['tag_dh'],MK['tag_dh']+2.2,","(MK['tag_dh'],MK['tag_end']-0.05,")
# 2) 밤에 일하는 정우 화면(02·04의 n601)에 키보드 소리(사장님 녹음, sfx3/s26.mp3)
R("speak('02',","MK['t02k']=T; EV.append((E+'sfx3/s26.mp3',T+2.7,0.8,'s',('seek',0.0,1.6)))\nspeak('02',")
R("MK['t04']=T;","MK['t04']=T; EV.append((E+'sfx3/s26.mp3',T+6.0,0.8,'s',('seek',2.0,1.6)));")
R("outn=E+('ed/ep2_v10A.mp4' if WITH28 else 'ed/ep2_v10B.mp4')","outn=E+('ed/ep2_v11A.mp4' if WITH28 else 'ed/ep2_v11B.mp4')")
open(sys.argv[2],'w').write(s); print('ok')
