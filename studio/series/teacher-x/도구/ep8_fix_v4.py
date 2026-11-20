# 교사X 8화 v4 소스 손질(크레딧 0) — 샌드박스 ~/ep9 에서 실행
# 1) v10p: 다해가 손에 만년필을 든 컷(v10)에서 가슴 포켓의 빨간 만년필을 프레임마다 찾아 지움(Gemini 11/20 '만년필 2개')
#    빨강 덩어리를 가슴 쪽 상자(y260~380, x290~420, 480x832 원본)에서 찾고, 사각형+여백 7·8px을 cv2.inpaint
# 2) v09bz: 교감 혼잣말 6초 한 컷 → 2.6초부터 85% 잘라 키운 같은 클립(펀치인)
import cv2, numpy as np, subprocess
cap = cv2.VideoCapture('v/v10.mp4'); fps = cap.get(5)
out = cv2.VideoWriter('/tmp/v10p_noa.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (480, 832)); last = None
while True:
    ok, f = cap.read()
    if not ok: break
    b, g, r = [f[..., k].astype(int) for k in range(3)]
    m = ((r > 110) & (r - g > 55) & (r - b > 45)).astype(np.uint8); roi = np.zeros_like(m); roi[260:380, 290:420] = 1; m *= roi
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    if n > 1:
        k = 1 + np.argmax(st[1:, 4]); x, y, w, h, a = st[k]
        if h < 30: last = (x, y, w, h)
        elif last: y, w, h = last[1], last[2], last[3]
    if last or n > 1:
        mm = np.zeros(f.shape[:2], np.uint8); cv2.rectangle(mm, (int(x) - 7, int(y) - 8), (int(x + w) + 7, int(y + h) + 8), 255, -1)
        f = cv2.inpaint(f, mm, 7, cv2.INPAINT_TELEA)
    out.write(f)
out.release()
subprocess.run(['ffmpeg','-v','error','-y','-i','/tmp/v10p_noa.mp4','-i','v/v10.mp4','-map','0:v','-map','1:a?','-c:v','libx264','-crf','17','-preset','veryfast','-c:a','copy','v/v10p.mp4'], check=True)
subprocess.run(['ffmpeg','-v','error','-y','-i','v/v09b.mp4','-vf','crop=iw*0.85:ih*0.85:iw*0.075:ih*0.06,scale=480:832,setsar=1','-c:v','libx264','-crf','17','-preset','veryfast','-c:a','copy','v/v09bz.mp4'], check=True)
print('ok')
