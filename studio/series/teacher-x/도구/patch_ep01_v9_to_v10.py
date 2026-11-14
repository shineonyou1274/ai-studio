# 1화 v9 → v10 (사장님 11/14: "1화에 사로잡게 배경음악 넣고" / 훅 자막 "되로 주려다 말로 받는다 (아직 조금만)" / 결재판 숨긴 걸 몰랐다 → 누구 결재판인지 표시). 크레딧 0
# 2화에서 고친 것 같이: 음량 전체 한 비율, 이어 붙인 뒤 setpts, 배경음악은 대사 때 자동 줄임 버스로
import sys
s=open(sys.argv[1]).read()
def R(a,b):
    global s
    assert s.count(a)==1, ('not unique/missing', a[:80], s.count(a))
    s=s.replace(a,b)
X="H+'/ep2/sfx3/"
# 1) 훅 자막 바꾸기 + 반격 음악 절정
R("[(0.0,3.4,'결재판 숨긴 교감,\\\\N계약교사 한마디에 얼어붙은 이유','Cap'),","[(-0.08,3.4,'{\\\\fad(300,0)}되로 주려다 {\\\\c&H0078E0FF&}말로{\\\\r} 받는다\\\\N{\\\\fs24}(아직 조금만)','HookT'),")
R("FL.append(T-0.08)\nMARK['b03']=T","FL.append(T-0.08)\nE.append(("+X+"B2.mp3',0,0.45,'b',('seek',50.0,T)))\nMARK['b03']=T")
# 2) 결재판이 누구 것인지: 서랍 장면 위에 표시
R("blk([(C+'c11.mp4',0,4.0)],[d('i11r.wav',0.15)],[(0.15,3.85,'결재판은 서랍에. 3교시 전엔 절대 못 나가.','In')]","blk([(C+'c11.mp4',0,4.0)],[d('i11r.wav',0.15)],[(0.15,3.85,'결재판은 서랍에. 3교시 전엔 절대 못 나가.','In'),(0.0,3.9,'{\\\\an8\\\\pos(360,150)\\\\fad(200,200)}다해가 올린 「야외 수업」 결재판','Note')]")
# 3) 배경음악: B1(답답) 그날 아침~종 쳤네 / B2(반격) 꽃밭 반박~'우수' 결정타 / B3(통쾌) 우수 결정타 뒤 / B2 뒷부분 4:50 칼퇴 장면. 코드 드론 뺌
R("E.append((S+'drone40.wav',MARK['drone'],1,'s',('trim',T-0.15-MARK['drone'])))\n","")
R(" [(S+'drone40.wav',0,1,'s',('trim',10.45))])"," [])")
R("MARK['birds']=T\nblk([(C+'c15.mp4',0,1.5)])","MARK['birds']=T\nblk([(C+'c15.mp4',0,1.5)])\nMARK['t16']=T")
R("FL.append(t23+8.8)","FL.append(t23+8.8); MARK['t23e']=t23+8.8")
R("MARK['b29']=T","MARK['b29']=T")
R("E.append((S+'birds2.wav',","E.append(("+X+"B1.mp3',MARK['b03'],0.45,'b',('cut',MARK['birds']-MARK['b03'])))\nE.append(("+X+"B2.mp3',t17,0.45,'b',('seek',0.0,MARK['t23e']-t17)))\nE.append(("+X+"B3.mp3',MARK['t23e'],0.9,'s',None))\nE.append(("+X+"s19.mp3',t17+10.45,0.55,'s',None)); E.append(("+X+"s19.mp3',MARK['t23e']-0.05,0.55,'s',None))\nE.append(("+X+"B2.mp3',MARK['b29'],0.45,'b',('seek',50.0,MARK['sad']-MARK['b29'])))\nE.append((S+'birds2.wav',")
R("        if tr[0]=='end':","        if tr[0]=='seek': ex=f',atrim={tr[1]:.3f}:{tr[1]+tr[2]:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.3,afade=t=out:st={max(0,tr[2]-0.6):.3f}:d=0.6'\n        if tr[0]=='cut': ex=f',atrim=0:{tr[1]:.3f},afade=t=in:d=0.6,afade=t=out:st={max(0,tr[1]-0.15):.3f}:d=0.15'\n        if tr[0]=='end':")
# 4) 대사 때 배경음악 더 세게 줄이기
R("sidechaincompress=threshold=0.03:ratio=8:attack=30:release=400[BD]","sidechaincompress=threshold=0.015:ratio=10:attack=20:release=350[BD]")
# 5) 음량: 전체 한 비율 + 리미터(2화와 같음)
R("loudnorm=I=-14:TP=-1.5[out]\"\ncmd+=['-filter_complex',fl,'-map','[out]','-c:a','aac','-b:a','192k','aud_v9.m4a']; run(cmd)",
  "[out]\"\ncmd+=['-filter_complex',fl,'-map','[out]','-c:a','pcm_s16le','aud_v10_pre.wav']; run(cmd)\nimport re as _re\n_m=subprocess.run(['ffmpeg','-nostdin','-i','aud_v10_pre.wav','-af','ebur128','-f','null','-'],capture_output=True,text=True).stderr\n_I=float(_re.findall(r'I:\\s+(-?[0-9.]+) LUFS',_m)[-1]); _g=-14.0-_I; print('pre I',_I,'gain',round(_g,2))\nrun(['ffmpeg','-nostdin','-v','error','-y','-i','aud_v10_pre.wav','-af',f'volume={_g:.2f}dB,alimiter=limit=0.6:level=false:attack=1:release=50','-c:a','aac','-b:a','192k','aud_v10.m4a'])")
# 6) 자막 스타일 추가(HookT, Note), 파일 이름 v10
R("Style: Poem,Gaegu,50,&H00FFFFFF,&H00FFFFFF,&H00000000,&HA0000000,0,0,0,0,100,100,0,0,3,14,0,2,60,60,160,1\\n\\n[Events]","Style: Poem,Gaegu,50,&H00FFFFFF,&H00FFFFFF,&H00000000,&HA0000000,0,0,0,0,100,100,0,0,3,14,0,2,60,60,160,1\\nStyle: HookT,Black Han Sans,36,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,4,3,8,24,24,26,1\\nStyle: Note,NanumGothic,30,&H00FFFFFF,&H00FFFFFF,&H00000000,&HA0000000,1,0,0,0,100,100,0,0,3,8,0,8,40,40,150,1\\n\\n[Events]")
R("open('sub_v9.ass','w').write(head)","open('sub_v10.ass','w').write(head)")
# 7) 이어 붙인 뒤 시간 다시 매기기(밀림 방지) + 출력 v10
R("'-i','pic_v9.mp4','-i','aud_v9.m4a','-vf',f\"{flash},ass=sub_v9.ass:","'-i','pic_v9.mp4','-i','aud_v10.m4a','-vf',f\"setpts=N/(24*TB),{flash},ass=sub_v10.ass:")
R("'-shortest','full_v9.mp4'])","'-shortest','full_v10.mp4'])")
open(sys.argv[2],'w').write(s); print('ok')
