# 2화 v11 → v12: 훅 자막(위)과 대사 자막(아래)이 벌어짐 → 훅 자막을 대사 자막 바로 위로(1화와 같은 규칙). 크레딧 0
import sys
s=open(sys.argv[1]).read()
a="Style: HookT,Black Han Sans,31,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,4,3,8,24,24,26,1"
assert s.count(a)==1
s=s.replace(a,"Style: HookT,Black Han Sans,34,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,4,3,2,24,24,352,1")
s=s.replace("outn=E+('ed/ep2_v11A.mp4' if WITH28 else 'ed/ep2_v11B.mp4')","outn=E+('ed/ep2_v12A.mp4' if WITH28 else 'ed/ep2_v12B.mp4')")
s=s.replace("alimiter=limit=0.7:level=false","alimiter=limit=0.6:level=false")
open(sys.argv[2],'w').write(s); print('ok')
