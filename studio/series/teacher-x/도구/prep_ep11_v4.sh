# 교사X 11화 v4 준비 (샌드박스 ~/ep12): 21 대사 빈 곳 잘라 냄(녹음·입 같이), 05 어머니 대사 영상 1.3배, 02·20 새 영상 자리
set -e; cd ~/ep12
# 21: 녹음 시각 1.72~3.27, 4.40~4.73 를 뺌 (영상은 같은 구간 + OFF 0.1)
K="between(t,1.72,3.27)+between(t,4.40,4.73)"; KV="between(t,1.82,3.37)+between(t,4.50,4.83)"
[ -f v/v21raw.mp4 ] || cp v/v21.mp4 v/v21raw.mp4
ffmpeg -nostdin -v error -y -i au/a21.wav -af "aselect='not($K)',asetpts=N/SR/TB" au/a21c.wav
ffmpeg -nostdin -v error -y -i v/v21raw.mp4 -vf "select='not($KV)',setpts=N/FRAME_RATE/TB" -af "aselect='not($KV)',asetpts=N/SR/TB" v/v21.mp4
# 05: 어머니 대사 영상 1.3배(소리도 같이) → v05.mp4
ffmpeg -nostdin -v error -y -i v/v05raw.mp4 -vf "setpts=PTS/1.3" -af "atempo=1.3" v/v05.mp4
python3 - <<'P'
import json; T=json.load(open('timing.json')); T.pop('21',None); json.dump(T,open('timing.json','w'),ensure_ascii=False)
P
echo prep ok
