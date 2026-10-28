"""(6화: 5화 v8 bgm.py에 'sad' 추가) 코드로 합성한 배경음(저작권 없음 — 사인파·소음만 씀). 대사가 나오는 동안 자동으로 줄인다(덕킹).
구간 종류:
  class  — 교실: 가볍게 튕기는 장난스러운 펄스(작게)
  tense  — 교감 압박: 시계 똑딱 + 낮은 드론 + 피치카토 펄스
  tense2 — AI 빙의 의심·"헐… 설마": 더 높은 드론 + 빠른 똑딱 + 조금씩 올라가는 음
구간 끝은 바로 끊는다(5ms) — 웃음 박자용 정적.
사용(모듈): make(sections, voices, total, out_wav, target_lufs=-28.0)
  sections = [(종류, 시작, 끝)], voices = [(wav 경로, 시작초)]  (대사 파일, 덕킹 기준)
"""
import re, subprocess
import numpy as np

SR = 48000


def _pluck(f, d=0.35, a=1.0):
    t = np.arange(int(d * SR)) / SR
    return a * np.sin(2 * np.pi * f * t) * np.exp(-t * 14) * (1 - np.exp(-t * 400))


def _tick(f, a=1.0):
    t = np.arange(int(0.03 * SR)) / SR
    return a * np.sin(2 * np.pi * f * t) * np.exp(-t * 160)


def _add(buf, x, at):
    i = int(at * SR)
    if i >= len(buf): return
    n = min(len(x), len(buf) - i); buf[i:i + n] += x[:n]


def _section(kind, dur, seed):
    n = int(dur * SR); t = np.arange(n) / SR; y = np.zeros(n)
    rnd = np.random.default_rng(seed)
    if kind == 'class':
        notes = [523.3, 659.3, 784.0, 659.3, 587.3, 698.5, 880.0, 698.5]   # C E G E / D F A F
        for k, at in enumerate(np.arange(0, dur, 0.25)):
            _add(y, _pluck(notes[k % 8], 0.25, 0.35), at)
        return y
    if kind == 'tense':
        y += 0.20 * np.sin(2 * np.pi * 55 * t) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.3 * t))
        y += 0.10 * np.sin(2 * np.pi * 82.4 * t)
        noise = rnd.standard_normal(n); k = np.ones(400) / 400
        y += 0.05 * np.convolve(noise, k, mode='same') * 8
        for j, at in enumerate(np.arange(0, dur, 0.5)):
            _add(y, _tick(2400 if j % 2 == 0 else 1800, 0.35), at)                   # 똑, 딱
            _add(y, _pluck(110 if j % 4 < 2 else 103.8, 0.4, 0.45), at)              # 피치카토
        return y
    if kind == 'tense2':
        # 낮은 드론을 쓰지 않음(v8: 73Hz 드론이 "헐… 설마"(여학생 속마음)를 남자 목소리처럼 들리게 함) → 높은 현 떨림
        f0 = 440 * (1 + 0.06 * t / max(dur, 0.1))                                    # 조금씩 올라감
        ph = 2 * np.pi * np.cumsum(f0) / SR
        trem = 0.6 + 0.4 * np.sin(2 * np.pi * 9 * t)
        y += 0.10 * trem * (np.sin(ph) + 0.6 * np.sin(1.5 * ph))
        y += 0.06 * np.sin(2 * np.pi * 7 * t) * np.sin(2 * np.pi * 220 * t)         # 떨리는 높은 음
        for j, at in enumerate(np.arange(0, dur, 0.25)):
            _add(y, _tick(2600 if j % 2 == 0 else 2000, 0.30), at)
            if j % 2 == 0: _add(y, _pluck(587.3, 0.2, 0.25), at)   # v8: 낮은 피치카토(146.8Hz)는 "헐… 설마" 음높이를 낮춰 보이게 해서 높은 음으로
        return y
    if kind == 'sad':   # 6화: 무게 구간 — 느린 단조 화음(A단조), 낮은 드론 없음
        for k, at in enumerate(np.arange(0, dur, 2.0)):
            ch = [(220.0, 261.6, 329.6), (196.0, 246.9, 293.7)][k % 2]
            m = int(min(2.4, dur - at) * SR)
            if m <= 0: continue
            tt = np.arange(m) / SR; env = np.minimum(1, tt / 0.6) * np.exp(-tt * 0.5)
            x = sum(np.sin(2 * np.pi * f * tt) for f in ch) * env * 0.12
            _add(y, x, at)
        return y
    if kind == 'mystery':   # 7화 v3: 추리 구간 — 낮은 현 떨림(D·A, 7Hz 트레몰로) + 부드러운 초침 + 가끔 낮은 퉁김
        trem = 0.55 + 0.45 * np.sin(2 * np.pi * 7 * t)
        # 6화 v8 교훈: 낮은 음(<200Hz)은 여학생 속마음 음높이를 낮춰 보이게 함 → 현 떨림을 한 옥타브 위(D4·A4)에 둠
        # 두 음이 정수비(3:2 등)면 공통 기본음(146Hz)이 생겨 같은 문제 → 반음 부딪침(A4·A#4)만 씀(공통 기본음 26Hz, 음높이 측정 범위 밖)
        for fq, a_ in ((440.0, 0.09), (466.2, 0.06), (441.5, 0.04)):
            y += a_ * trem * np.sin(2 * np.pi * fq * t)
        y *= np.minimum(1, t / 0.8)
        for j, at in enumerate(np.arange(0, dur, 0.5)):
            _add(y, _tick(3000 if j % 2 == 0 else 2200, 0.22), at)
            if j % 8 == 0: _add(y, _pluck(587.3, 0.6, 0.18), at)
        return y
    if kind == 'pulse':     # 7화 v3: 웃음 구간 — 가벼운 스타카토 펄스(펜타토닉) + 통통 튀는 베이스
        notes = [659.3, 784.0, 880.0, 784.0, 659.3, 587.3, 523.3, 587.3]
        for k, at in enumerate(np.arange(0, dur, 0.18)):
            _add(y, _pluck(notes[k % 8], 0.15, 0.28), at)
            if k % 4 == 0: _add(y, _pluck(261.6 if (k // 4) % 2 == 0 else 329.6, 0.25, 0.40), at)
        return y
    if kind == 'confront':  # 7화 v4: 어머니와 대치 — 빠른 현 떨림(E4·F4 반음 부딪침, 11Hz) + 낮은 맥박(쿵-쿵, 1초에 1.2번)
        trem = 0.5 + 0.5 * np.sin(2 * np.pi * 11 * t)
        swell = 0.75 + 0.25 * np.sin(2 * np.pi * 0.25 * t)
        for fq, a_ in ((329.6, 0.08), (349.2, 0.06), (659.3, 0.025)):
            y += a_ * trem * swell * np.sin(2 * np.pi * fq * t)
        y *= np.minimum(1, t / 0.5)
        for at in np.arange(0.0, dur, 0.83):
            for dt, aa in ((0.0, 0.55), (0.16, 0.35)):
                m = int(0.18 * SR); tt = np.arange(m) / SR
                _add(y, aa * np.sin(2 * np.pi * (58 - 20 * tt) * tt) * np.exp(-tt * 22) * (1 - np.exp(-tt * 300)), at + dt)
        return y
    raise ValueError(kind)


def _lufs(path):
    m = subprocess.run(['ffmpeg', '-i', str(path), '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', m)[-1])


def _read(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.float32)


def _write(x, path):
    st = np.repeat(x[:, None], 2, axis=1).astype(np.float32)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', '-c:a', 'pcm_s16le', str(path)],
                   input=st.tobytes(), check=True)


def make(sections, voices, total, out_wav, target_lufs=-28.0, duck_db=-10.0, class_db=-4.0, release=0.35):
    n = int(total * SR); bed = np.zeros(n)
    for k, (kind, a, b) in enumerate(sections):
        if b <= a: continue
        y = _section(kind, b - a, k)
        fin = min(int(0.3 * SR), len(y)); y[:fin] *= np.linspace(0, 1, fin)                     # 들어올 때 0.3초 페이드
        fo = int(0.005 * SR); y[-fo:] *= np.linspace(1, 0, fo)                    # 나갈 때는 바로 끊음
        if kind == 'class': y *= 10 ** (class_db / 20)
        _add(bed, y, a)
    # 크기 맞추기(덕킹 전, 소리 있는 곳 기준 통합 음량)
    tmp = str(out_wav) + '.pre.wav'; _write(bed, tmp)
    bed *= 10 ** ((target_lufs - _lufs(tmp)) / 20)
    # 덕킹: 대사 소리(20ms RMS)가 있는 곳에서 duck_db만큼, 줄 때 0.05초 / 돌아올 때 0.35초
    act = np.zeros(n)
    for path, at in voices:
        v = _read(path); h = SR // 50
        m = len(v) // h
        if m == 0: continue
        r = np.sqrt((v[:m * h].reshape(m, h) ** 2).mean(1))
        on = np.repeat((r > 10 ** (-40 / 20)).astype(float), h)
        _add(act, on, at)
    act = np.clip(act, 0, 1)
    g = np.empty(n); cur = 0.0
    att, rel = 1 - np.exp(-1 / (0.05 * SR)), 1 - np.exp(-1 / (release * SR))
    for i in range(0, n, 48):                                                      # 1ms 단위로 계산
        tgt = act[i]
        cur += (tgt - cur) * (1 - (1 - (att if tgt > cur else rel)) ** 48)
        g[i:i + 48] = cur
    bed *= 10 ** (duck_db * g / 20)
    _write(bed, out_wav)
    return _lufs(out_wav)
