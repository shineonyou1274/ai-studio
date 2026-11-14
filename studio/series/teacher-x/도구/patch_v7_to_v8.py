# 2화 v7 → v8 (사장님 외부 검수 "사이다가 고구마처럼" 반영, 크레딧 0). 사용: python3 patch_v7_to_v8.py <v7> <v8>
# 효과음 sfx3/s15~s24, 배경음악 sfx3/B1(답답)·B2(반격)·B3(통쾌) — ~/ep2/sfx3
import sys
s=open(sys.argv[1]).read()
def R(a,b):
    global s
    assert s.count(a)==1, ('not unique/missing', a[:80], s.count(a))
    s=s.replace(a,b)
X="E+'sfx3/"
# 0) 배경음악 자르기 방식 추가: seek(시작초, 길이), cut(길이, 끝 0.15초에 뚝)
R("        if tr[0]=='end':","        if tr[0]=='seek': ex=f',atrim={tr[1]:.3f}:{tr[1]+tr[2]:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.3,afade=t=out:st={max(0,tr[2]-0.6):.3f}:d=0.6'\n        if tr[0]=='cut': ex=f',atrim=0:{tr[1]:.3f},afade=t=in:d=0.6,afade=t=out:st={max(0,tr[1]-0.15):.3f}:d=0.15'\n        if tr[0]=='end':")
# 1) 다해 목소리 보정(중저음·또렷함·압축) — 입 모양은 그대로
R("# inner voice processing","DH=['09','12','15','16','17','19','21','23','27','28']\nfor c in DH:\n    run(['ffmpeg','-nostdin','-v','error','-y','-i',A+f'a{c}.wav','-af','equalizer=f=170:t=q:w=1.0:g=3,equalizer=f=3000:t=q:w=1.0:g=2.5,acompressor=threshold=0.08:ratio=3:attack=5:release=120:makeup=1.6',A+f'e{c}.wav'])\ndef AW(c): return A+(f'e{c}.wav' if c in DH else f'a{c}.wav')\n# inner voice processing")
R("    add(segs,[(A+f'a{c}.wav',0,1.0,'d',None)],chunks(text,c))","    add(segs,[(AW(c),0,1.0,'d',None)],chunks(text,c))")
R("add(segs,[(A+'a17.wav',0,1.0,'d',None)]","add(segs,[(AW('17'),0,1.0,'d',None)]")
R("add(segs,[(A+'a19.wav',0,1.0,'d',None)]","add(segs,[(AW('19'),0,1.0,'d',None)]")
# 2) 훅 = 다해 "커피 한 잔 드시고 오세요. 40분이면 됩니다." + 반격 음악 절정 부분
i=s.index("add([(E+'x/n19c.mp4',max(0,hs-0.05-9.4-0.1),1.4)"); j=s.index("FL.append(T-0.08)")
s=s[:i]+"""L12=round(v1('12')+0.12,3)
add([(V+'v12.mp4',0,1.5),(img('212',0.9),0,0.9),(V+'v12.mp4',2.4,round(L12-2.4,3))],[(AW('12'),0,1.0,'d',None),("""+X+"""B2.mp3',0,0.9,'s',('seek',50.0,L12))],
    [(0,L12,"{\\\\fs36}'고쳐 오라면서 길을 6번 바꾸면?'\\\\N3주 끌던 결재, 40분 만에 뚫린 이유",'Cap')]+chunks('커피 한 잔 드시고 오세요.|'+K('40분')+'이면 됩니다.','12'))
"""+s[j:]
# 3) 반려 화면 2.4 → 1.5초, 날카로운 비프
R("add([(img('o01',2.4,'crash'),0,2.4)],ev=[(E+'sfx2/reject.mp3',0.15,0.6,'s',None)],subs=[(0.05,1.6,'그날 오후 3시','Cap'),(0.4,2.4,","add([(img('o01',1.5,'crash'),0,1.5)],ev=[("+X+"s15.mp3',0.1,0.45,'s',None)],subs=[(0.05,1.4,'그날 오후 3시','Cap'),(0.3,1.5,")
# 4) 교감 "내가 언제 옮기랬어?"에 화면 흔들림
R("speak('04',","MK['t04']=T; HIT.extend([T+0.1,T+0.45])\nspeak('04',")
# 5) 정우 한숨 3.2 → 2.9초
R("inner('05',[(img('305',2.0,'out'),0,2.0),(E+'x/r501.mp4',2.6,1.2)]","inner('05',[(img('305',1.4,'out'),0,1.4),(E+'x/r501.mp4',2.6,1.5)]")
# 6) 서류 쿵
R("speak('06',","MK['t06']=T; EV.append(("+X+"s16.mp3',T+2.6,0.9,'s',None))\nspeak('06',")
# 7) 대사 뒤 빈 시간 줄이기
for a,b in [("'흥. 어디 한번 봅시다.',tail=0.5","'흥. 어디 한번 봅시다.',tail=0.25"),("'교감 선생님,|그건 제 업무인데…',tail=0.4","'교감 선생님,|그건 제 업무인데…',tail=0.25"),("'그, 그건 문맥이…',tail=0.4","'그, 그건 문맥이…',tail=0.2"),("'도, 독고 선생…',tail=0.3","'도, 독고 선생…',tail=0.2"),("'이면 됩니다.',tail=0.3","'이면 됩니다.',tail=0.2"),("'면 됩니다.',tail=0.3","'면 됩니다.',tail=0.2")]:
    R(a,b)
R("speak('09',","MK['t09']=T\nspeak('09',")
# 8) 3:40 시계 째깍 빨리감기 + 기안 도착 묵직한 히트 + 종이 휙·스우시(앞 장면 끝)
R("ev=[(E+'sfx2/arrive.mp3',1.4,0.2,'s',None)],subs=[(1.4,2.0,","ev=[("+X+"s18.mp3',0,0.7,'s',('cut',1.4)),("+X+"s19.mp3',1.4,0.55,'s',None),(E+'sfx2/arrive.mp3',1.4,0.2,'s',None),("+X+"s17a.mp3',-0.5,0.8,'s',None),("+X+"s17b.mp3',-0.15,0.8,'s',None)],subs=[(1.4,2.0,")
# 9) 다해 교감실 들어가는 구두 소리(교감 "벌써?" 뒤)
R("MK['drone']=T","MK['drone']=T; EV.append(("+X+"s20.mp3',T-1.3,0.8,'s',('cut',1.4)))")
# 10) 초과근무 그래프 빨간 점 3번 타격음
R("speak('21',","MK['t21']=T; EV.extend([("+X+"s21.mp3',T+4.2+k*0.55,0.25,'s',None) for k in range(3)])\nspeak('21',")
# 11) 결정타 직전 0.5초 정적용 시각 기록 + 미로 뒤 유리 깨짐
R("segs=[(V+'v19.mp4',0,2.5),","MK['t19']=T\nsegs=[(V+'v19.mp4',0,2.5),")
R("FL.append(T-0.05)\nadd([(E+'x/r508.mp4',2.2,1.8)]","FL.append(T-0.05); MK['after19']=T; EV.append(("+X+"s22.mp3',T-0.05,0.8,'s',None))\nadd([(E+'x/r508.mp4',2.2,1.8)]")
# 12) 최종 승인: 도장 + 승리 음악
R("ev=[(E+'sfx2/arrive.mp3',0.1,0.18,'s',None)])","ev=[("+X+"s23.mp3',0.15,0.9,'s',None),("+X+"B3.mp3',0.0,1.0,'s',None)])")
# 13) 다해 퇴장 문 닫힘, 엔딩 포스터 쾅
R("add([(E+'x/r513.mp4',0.3,2.6)],[(U+'g1s.wav',0.5,0.8,'d',None)])","add([(E+'x/r513.mp4',0.3,2.6)],[(U+'g1s.wav',0.5,0.8,'d',None),("+X+"s24.mp3',0.0,0.9,'s',None)])")
R("add([(img('poster2',3.0,'slow'),0,3.0)])","add([(img('poster2',3.0,'crash'),0,3.0)],[("+X+"s19.mp3',0.0,0.6,'s',None)])")
# 14) 배경음악: B1 답답(반려~09 직전, 뚝 끊음) → B2 반격(09~결정타 0.8초 전) → 정적 → B2 뒷부분(미로 뒤~승인) — 드론 대신
R("EV.append((S+'drone40.wav',MK['drone'],0.6,'s',('trim',MK['drone_end']-MK['drone'])))",
  "EV.append(("+X+"B1.mp3',MK['s1'],1.0,'s',('cut',MK['t09']-MK['s1'])))\nEV.append(("+X+"B2.mp3',MK['t09'],1.0,'s',('seek',0.0,MK['t19']+tk-0.8-MK['t09'])))\nEV.append(("+X+"B2.mp3',MK['after19'],1.0,'s',('seek',50.0,MK['drone_end']-MK['after19'])))")
# 15) 음량 맞추기를 '구간마다 자동'(loudnorm 동적)에서 '전체 한 비율'로: 섞은 소리를 재고 → 같은 비율로 −14 LUFS → 리미터. 효과음 크기 조절이 그대로 남고 최고점도 지킴
R("fl+=f\"[D1][SD]amix=inputs=2:normalize=0,atrim=0:{total},loudnorm=I=-14:TP=-1.5,alimiter=limit=0.84:level=false[out]\"",
  "fl+=f\"[D1][SD]amix=inputs=2:normalize=0,atrim=0:{total}[out]\"")
R("cmd+=['-filter_complex',fl,'-map','[out]','-c:a','aac','-b:a','192k',E+'ed/aud.m4a']; run(cmd)",
  "cmd+=['-filter_complex',fl,'-map','[out]','-c:a','pcm_s16le',E+'ed/aud_pre.wav']; run(cmd)\nimport re as _re\n_m=subprocess.run(['ffmpeg','-nostdin','-i',E+'ed/aud_pre.wav','-af','ebur128','-f','null','-'],capture_output=True,text=True).stderr\n_I=float(_re.findall(r'I:\\s+(-?[0-9.]+) LUFS',_m)[-1]); _g=-14.0-_I; print('pre I',_I,'gain',round(_g,2))\nrun(['ffmpeg','-nostdin','-v','error','-y','-i',E+'ed/aud_pre.wav','-af',f'volume={_g:.2f}dB,alimiter=limit=0.7:level=false:attack=1:release=50','-c:a','aac','-b:a','192k',E+'ed/aud.m4a'])")
R("outn=E+('ed/ep2_v7A.mp4' if WITH28 else 'ed/ep2_v7B.mp4')","outn=E+('ed/ep2_v8A.mp4' if WITH28 else 'ed/ep2_v8B.mp4')")
open(sys.argv[2],'w').write(s); print('ok')
