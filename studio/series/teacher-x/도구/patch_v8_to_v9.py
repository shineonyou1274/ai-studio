# 2화 v8 → v9 (사장님 캡처: 훅 자막이 얼굴 가림 → (가) / 제미나이 v8 감수 받은 것 / "딸깍!·[정적] 둘 다 빼"). 크레딧 0
import sys
s=open(sys.argv[1]).read()
def R(a,b):
    global s
    assert s.count(a)==1, ('not unique/missing', a[:80], s.count(a))
    s=s.replace(a,b)
# 1) 훅 자막: 화면 맨 위로 + 0.3초 서서히 (다해 얼굴 가리지 않게)
R("""[(0,L12,"{\\\\fs36}'고쳐 오라면서 길을 6번 바꾸면?'""","""[(0,L12,"{\\\\an8\\\\pos(360,28)\\\\fad(300,0)\\\\fs32}'고쳐 오라면서 길을 6번 바꾸면?'""")
# 2) "딸깍!"·"[정적]" 글자 빼기
R("SUB.append((T-L19+tk-0.25,T-L19+tk+0.45,'{\\\\pos(540,400)\\\\frz12}'+POP+'딸깍!','Ono'))\n","")
R("add([(E+'x/r508.mp4',2.2,1.8)],subs=[(0.3,1.8,'[정적]','Act')])","add([(E+'x/r508.mp4',2.2,1.8)])")
# 3) 미로 뒤 1.8초는 음악 없이 실제 정적 → 그다음 반격 음악
R("EV.append((E+'sfx3/B2.mp3',MK['after19'],1.0,'s',('seek',50.0,MK['drone_end']-MK['after19'])))","EV.append((E+'sfx3/B2.mp3',MK['after19']+1.8,1.0,'s',('seek',50.0,MK['drone_end']-MK['after19']-1.8)))")
# 4) 교감 협박(08)에서 답답 음악 끊기 → 정적 → 09 반격
R("speak('08',","MK['t08']=T\nspeak('08',")
R("EV.append((E+'sfx3/B1.mp3',MK['s1'],1.0,'s',('cut',MK['t09']-MK['s1'])))","EV.append((E+'sfx3/B1.mp3',MK['s1'],1.0,'s',('cut',MK['t08']+0.1-MK['s1'])))")
# 5) 교감 "내가 언제 옮기랬어?" 흔들림 조금 더(3번)
R("HIT.extend([T+0.1,T+0.45])","HIT.extend([T+0.1,T+0.4,T+0.75])")
# 6) 반려 사유: 5차 카드 뒤에 3차↔5차 '정반대' 카드
R("(img('c5',round(t2-t5,3),'in'),0,round(t2-t5,3))","(img('c5',round((t2-t5)*0.55,3),'in'),0,round((t2-t5)*0.55,3)),(img('c35',round((t2-t5)*0.45,3),'crash'),0,round((t2-t5)*0.45,3))")
# 7) 화면이 소리보다 점점 늦어지던 문제(채점 v8A 상): 조각마다 1/24초씩 올려 쌓이던 것을 누적 프레임 경계로 자름
R("""    run(['ffmpeg','-nostdin','-v','error','-y','-ss',str(max(0,s)),'-i',f,'-t',str(dd),'-vf',"scale=720:1280,fps=24"+cf+",format=yuv420p",'-an','-c:v','libx264','-preset','veryfast','-crf','19',o]); F.append(o)""",
  """    n0=round(CUM*24); CUM+=dd; nf=max(1,round(CUM*24)-n0)
    run(['ffmpeg','-nostdin','-v','error','-y','-ss',str(max(0,s)),'-i',f,'-vf',"scale=720:1280,fps=24"+cf+",tpad=stop_mode=clone:stop_duration=1,format=yuv420p",'-frames:v',str(nf),'-an','-c:v','libx264','-preset','veryfast','-crf','19',o]); F.append(o)""")
R("for i,(f,s,dd) in enumerate(P):","CUM=0.0\nfor i,(f,s,dd) in enumerate(P):")
# 8) 음악·효과음이 대사보다 충분히 낮지 않음(채점 상): 배경음악 −7dB, 대사 때 자동 줄임 더 세게
R("EV.append((E+'sfx3/B1.mp3',MK['s1'],1.0,","EV.append((E+'sfx3/B1.mp3',MK['s1'],0.45,")
R("EV.append((E+'sfx3/B2.mp3',MK['t09'],1.0,","EV.append((E+'sfx3/B2.mp3',MK['t09'],0.45,")
R("EV.append((E+'sfx3/B2.mp3',MK['after19']+1.8,1.0,","EV.append((E+'sfx3/B2.mp3',MK['after19']+1.8,0.45,")
R("(E+'sfx3/B2.mp3',0,0.9,'s',('seek',50.0,L12))","(E+'sfx3/B2.mp3',0,0.45,'s',('seek',50.0,L12))")
R("sidechaincompress=threshold=0.03:ratio=6:attack=30:release=400","sidechaincompress=threshold=0.015:ratio=10:attack=20:release=350")
# 9) 그래프 타격 셋째가 "공무원" 첫소리와 겹침 → 간격 0.45초
R("T+4.2+k*0.55,0.25,'s',None) for k in range(3)","T+4.1+k*0.45,0.25,'s',None) for k in range(3)")
R("outn=E+('ed/ep2_v8A.mp4' if WITH28 else 'ed/ep2_v8B.mp4')","outn=E+('ed/ep2_v9A.mp4' if WITH28 else 'ed/ep2_v9B.mp4')")
open(sys.argv[2],'w').write(s); print('ok')
