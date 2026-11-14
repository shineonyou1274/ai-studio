# 2화 v9 → v10 (제미나이 2차: 훅 자막 디자인·템포·결정타 비네팅). 크레딧 0
import sys
s=open(sys.argv[1]).read()
def R(a,b):
    global s
    assert s.count(a)==1, ('not unique/missing', a[:80], s.count(a))
    s=s.replace(a,b)
# 1) 훅 자막: 검은 상자 → 상자 없이 굵은 제목체(검은고딕)+테두리·그림자, 85% 크기, 숫자만 노랑
R("""[(0,L12,"{\\\\an8\\\\pos(360,28)\\\\fad(300,0)\\\\fs32}'고쳐 오라면서 길을 6번 바꾸면?'\\\\N3주 끌던 결재, 40분 만에 뚫린 이유",'Cap')]""",
  """[(0,L12,"{\\\\fad(300,0)}'고쳐 오라면서 길을 "+YN+"6번{\\\\r} 바꾸면?'\\\\N"+YN+"3주{\\\\r} 끌던 결재, "+YN+"40분{\\\\r} 만에 뚫린 이유",'HookT')]""")
R("def K(w): return Y+w+'{\\\\r}'","def K(w): return Y+w+'{\\\\r}'\nYN='{\\\\c&H0078E0FF&}'")
R("head=open(H+'/ep2/sub_v2_header.ass').read()","head=open(H+'/ep2/sub_v2_header.ass').read().replace('\\n\\n[Events]','\\nStyle: HookT,Black Han Sans,31,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,4,3,8,24,24,26,1\\n\\n[Events]',1)")
# 2) 06 → 07 넘어가는 틈 0.25초 줄이기
R("내일 아침까지 고쳐 와요.',tail=0.6)","내일 아침까지 고쳐 와요.',tail=0.35)")
R("MK['tag_dh']=T-1.9","MK['tag_dh']=T-1.65")
# 3) "미로입니다" 동안 화면 가장자리 어둡게(비네팅)
R('f"setpts=N/(24*TB),{flash},{shake},ass=','f"setpts=N/(24*TB),{flash},{shake},vignette=angle=0.75:enable=\'between(t,{MK[\'t19\']+tk+0.5:.2f},{MK[\'after19\']:.2f})\',ass=')
R("outn=E+('ed/ep2_v9A.mp4' if WITH28 else 'ed/ep2_v9B.mp4')","outn=E+('ed/ep2_v10A.mp4' if WITH28 else 'ed/ep2_v10B.mp4')")
open(sys.argv[2],'w').write(s); print('ok')
