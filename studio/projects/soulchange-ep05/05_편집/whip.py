"""5화 v5: 두 컷 사이 휩 팬(가로로 빠르게 쓸리는 번짐) 전환. 시간은 늘리지 않고 앞 컷 끝 nA프레임·뒤 컷 앞 nB프레임만 바꾼다.
K6a(책상 쾅쾅, 친구들 곁) → K6b(지우 몸 혼자 머리 감쌈): 친구들이 자리를 뜨는 동안 카메라가 휙 돌아간 것처럼 보이게(발소리·의자 소리는 build에서).
사용: python3 whip.py a.mp4 b.mp4 nA nB a_out.mp4 b_out.mp4
"""
import subprocess, sys
import numpy as np

W, H, FPS = 1080, 1920, 30


def read(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3).copy()


def write(fr, p):
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p', p], input=fr.tobytes(), check=True)


def smear(img, shift, blur):
    """가로로 shift만큼 밀고(가장자리는 늘임) blur 픽셀 가로 상자 번짐."""
    x = np.roll(img.astype(np.float32), int(shift), axis=1)
    if shift > 0: x[:, :int(shift)] = x[:, int(shift):int(shift) + 1]
    elif shift < 0: x[:, int(shift):] = x[:, int(shift) - 1:int(shift)]
    b = max(1, int(blur))
    c = np.cumsum(np.pad(x, ((0, 0), (b, b), (0, 0)), mode='edge'), axis=1)
    x = (c[:, 2 * b:] - c[:, :-2 * b]) / (2 * b)
    return np.clip(x[:, :W], 0, 255).astype(np.uint8)


def main(a, b, nA, nB, ao, bo):
    nA, nB = int(nA), int(nB)
    A, Bf = read(a), read(b)
    for k in range(nA):                     # 앞 컷: 왼쪽으로 점점 빠르게 쓸려 나감
        e = ((k + 1) / nA) ** 2
        A[-nA + k] = smear(A[-nA + k], -420 * e, 6 + 120 * e)
    for k in range(nB):                     # 뒤 컷: 오른쪽에서 쓸려 들어와 멈춤
        e = (1 - k / nB) ** 2
        Bf[k] = smear(Bf[k], 420 * e, 6 + 120 * e) if e > 0.01 else Bf[k]
    write(A, ao); write(Bf, bo)


if __name__ == '__main__':
    main(*sys.argv[1:])
