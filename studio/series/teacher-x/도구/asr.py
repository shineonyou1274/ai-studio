# 녹음 받아쓰기 확인: 폴더 안 r*.mp3를 받아써서 확정 대사와 대조. 사용: python3 asr.py ~/ep2/rec
import sys,glob,subprocess
from faster_whisper import WhisperModel
m=WhisperModel("small",compute_type="int8")
for f in sorted(glob.glob(sys.argv[1]+"/r*.mp3")):
    d=float(subprocess.check_output(["ffprobe","-v","0","-show_entries","format=duration","-of","csv=p=0",f]))
    segs,_=m.transcribe(f,language="ko")
    print(f.split("/")[-1],round(d,2),"|"," ".join(s.text.strip() for s in segs))
