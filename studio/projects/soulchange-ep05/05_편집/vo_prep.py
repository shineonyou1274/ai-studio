"""5화 v1 대사 조각 만들기: 원본 mp3 → 구간 자르기 → 줄 안 긴 쉼 줄이기 → -18 LUFS(2단계 게인) → atempo.
build_ep5_v1.py가 불러 쓴다. 결과: build/vo/<id>.wav (48kHz mono), 길이 dict.
"""
import subprocess, re, json, pathlib
import numpy as np

SR = 48000


def decode(path, ss, to):
    cmd = ['ffmpeg', '-v', 'error', '-ss', f'{ss}', '-to', f'{to}', '-i', str(path), '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-']
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).copy()


def squeeze(x, maxgap, rel_db=-34, edge=0.04):
    """10ms RMS가 최댓값보다 rel_db 아래인 구간을 쉼으로 보고, 앞뒤 쉼은 edge초만, 줄 안 쉼은 maxgap초까지만 남긴다."""
    hop = SR // 100
    n = len(x) // hop
    rms = np.sqrt(np.mean(x[:n * hop].reshape(n, hop) ** 2, axis=1) + 1e-12)
    db = 20 * np.log10(rms)
    voiced = db > db.max() + rel_db
    idx = np.nonzero(voiced)[0]
    if len(idx) == 0:
        return x
    a, b = idx[0], idx[-1] + 1
    keep = []
    i = a
    while i < b:
        if voiced[i]:
            j = i
            while j < b and voiced[j]: j += 1
            keep.append(('v', i, j)); i = j
        else:
            j = i
            while j < b and not voiced[j]: j += 1
            keep.append(('s', i, j)); i = j
    out = [x[max(0, a * hop - int(edge * SR)):a * hop]]
    fade = int(0.008 * SR)
    for kind, i, j in keep:
        seg = x[i * hop:j * hop]
        if kind == 's' and (j - i) * hop > maxgap * SR:
            h = int(maxgap * SR / 2)
            p1, p2 = seg[:h].copy(), seg[-h:].copy()
            p1[-fade:] *= np.linspace(1, 0, fade); p2[:fade] *= np.linspace(0, 1, fade)
            seg = np.concatenate([p1, p2])
        out.append(seg)
    out.append(x[b * hop:b * hop + int(edge * SR)])
    return np.concatenate(out)


def lufs(path):
    m = subprocess.run(['ffmpeg', '-i', str(path), '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', m)[-1])


def prep(spec, src_dir, out_dir):
    """spec: {id: dict(f=파일, r=[(in,out),...], tempo=1.05, gap=0.18)}"""
    out_dir.mkdir(parents=True, exist_ok=True)
    durs = {}
    for lid, s in spec.items():
        parts = [decode(src_dir / s['f'], a, b) for a, b in s['r']]
        x = np.concatenate(parts)
        x = squeeze(x, s.get('gap', 0.18))
        tmp = out_dir / f'{lid}_t.wav'
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', str(tmp)],
                       input=x.astype(np.float32).tobytes(), check=True)
        g = -18.0 - lufs(tmp)
        af = f'volume={g:.2f}dB'
        if s.get('tempo', 1.0) != 1.0: af += f",atempo={s['tempo']}"
        out = out_dir / f'{lid}.wav'
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(tmp), '-af', af, '-ar', str(SR), '-c:a', 'pcm_s16le', str(out)], check=True)
        tmp.unlink()
        d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(out)],
                                 capture_output=True, text=True).stdout)
        durs[lid] = round(d, 3)
    return durs
