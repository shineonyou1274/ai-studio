# -*- coding: utf-8 -*-
"""쇼츠 편집기 — 폴더에 넣은 영상·사진을 9:16 쇼츠 한 편으로 이어 붙입니다.
여행, 맛집, 일상 브이로그, 매장·병원 홍보처럼 '찍어 둔 장면을 이어 붙이는' 영상용입니다.

쓰는 법
    1. 이 파일 옆의 videos 폴더에 영상(mp4·mov)과 사진(jpg·png)을 넣습니다.
    2. settings.json 에서 주제와 제목 문구를 바꿉니다.
    3. python make_shorts.py   →  output/shorts.mp4

만들어지는 영상
    · 도입부: 하이라이트 4장면을 0.2초씩 번쩍 넘김 → 첫 장면이 확 당겨졌다 자리 잡음
    · 본편: 0.5초씩 빠른 컷(한 영상에서 전경·확대 등 여러 컷), 컷 안에서 아주 조금 다가감
    · 위쪽에 제목 고정, 왼쪽 아래에 머리표(DAY·번호·시간)와 장면 글자(settings.json 의 "장면글자")
      "주제"를 고르면 머리표와 핀 표시가 그 주제에 맞게 정해집니다(여행·맛집·일상·홍보·없음).
    · 소리는 도입부 효과음 + 배경음악(music 폴더에 넣었을 때만). 컷 0.5초 = 분당 120박 음악과 맞음.

필요한 것: Python 3.9 이상, Pillow(pip install pillow), ffmpeg(PATH 에 있어야 함)
"""
import json
import math
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
except ImportError:
    sys.exit("Pillow 가 없습니다. 터미널에서  pip install pillow  를 실행한 뒤 다시 해 주세요.")

HERE = Path(__file__).resolve().parent
WORK = HERE / "_work"
W, H, FPS = 1080, 1920, 30
VIDEO_EXT = {".mp4", ".mov", ".m4v", ".mkv", ".webm", ".avi"}
PHOTO_EXT = {".jpg", ".jpeg", ".png"}
AUDIO_EXT = {".mp3", ".m4a", ".wav", ".aac", ".ogg", ".flac"}
# 주제별 기본값: 머리표(노란 딱지에 들어갈 것)와 핀(📍 모양) 표시
TOPICS = {
    "여행": {"머리표": "DAY", "핀": True},       # DAY 2 · 📍 자카르타 대성당
    "맛집": {"머리표": "없음", "핀": True},      # 📍 성수동 ○○ · 크림 파스타
    "일상": {"머리표": "시간", "핀": False},     # 오전 7시 · 출근길
    "홍보": {"머리표": "번호", "핀": False},     # 01 · 진료실 소개
    "없음": {"머리표": "없음", "핀": False},     # 제목만
}
DEFAULTS = {
    "영상폴더": "videos",
    "주제": "여행",
    "제목_작게": "「 오늘의 기록 」",
    "제목_크게": "MY SHORTS",
    "제목_아래": "",
    "제목_아래_강조": "",
    "컷길이": 0.5,
    "최대길이": 12,
    "도입효과": True,
    "효과음": True,
    "장면글자": {},          # "파일 이름 일부": "그 장면에 붙일 한 줄"
    "색보정": True,
    "배경음악": "",          # 비우면 music 폴더의 첫 음악 파일, "없음"이면 끔, 파일 이름을 적으면 그 파일
    "음악크기": -8,          # dB. 0 이 원래 크기, -10 이면 작게
    "음악시작": 0,           # 노래의 몇 초부터 쓸지(후렴부터 쓰고 싶을 때)
    # 아래 둘은 비워 두면 "주제"에 따라 정해짐. 직접 적으면 그 값이 우선
    "머리표": None,          # "DAY" | "번호" | "시간" | "없음"
    "핀": None,              # true | false
}


def fail(msg: str) -> None:
    sys.exit("[멈춤] " + msg)


def load_settings() -> dict:
    p = HERE / "settings.json"
    s = dict(DEFAULTS)
    if p.exists():
        try:
            s.update(json.loads(p.read_text(encoding="utf-8")))
        except json.JSONDecodeError as e:
            fail(f"settings.json 형식이 잘못됐습니다({e.lineno}번째 줄 근처). 쉼표·따옴표를 확인해 주세요.")
    if "장소" in s and not s.get("장면글자"):          # 예전(여행 전용) 설정 이름도 받아 줌
        s["장면글자"] = s["장소"]
    topic = TOPICS.get(str(s.get("주제", "여행")).strip())
    if topic is None:
        print(f"  (알림) 주제 '{s.get('주제')}' 는 없는 이름이라 '없음'으로 만듭니다. 가능: {', '.join(TOPICS)}")
        topic = TOPICS["없음"]
    if s.get("머리표") is None:
        s["머리표"] = "없음" if s.get("DAY표시") is False else topic["머리표"]
    if s.get("핀") is None:
        s["핀"] = topic["핀"]
    return s


def tool(name: str) -> str:
    p = shutil.which(name)
    if not p:
        fail(f"{name} 을 찾지 못했습니다. ffmpeg 를 설치하고 터미널을 새로 연 뒤 다시 해 주세요.")
    return p


def find_font(bold: bool = True) -> str:
    """제목용 굵은 한글 글꼴: fonts 폴더 → 윈도우 맑은 고딕 → 맥 산돌고딕 순."""
    local = sorted((HERE / "fonts").glob("*.[ot]tf")) if (HERE / "fonts").exists() else []
    pref = [f for f in local if ("Black" in f.name) == bold] or local
    cands = [str(f) for f in pref] + [
        "C:/Windows/Fonts/malgunbd.ttf", "C:/Windows/Fonts/malgun.ttf",
        "/System/Library/Fonts/AppleSDGothicNeo.ttc", "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
        "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf",
    ]
    for c in cands:
        if Path(c).exists():
            return c
    fail("한글 글꼴을 찾지 못했습니다. fonts 폴더에 굵은 한글 글꼴(ttf·otf) 하나를 넣어 주세요.")


def probe(path: Path) -> dict:
    """길이(초)와 촬영 시각. 사진은 길이 0."""
    taken = None
    if path.suffix.lower() in PHOTO_EXT:
        try:
            ex = Image.open(path).getexif()
            raw = ex.get_ifd(0x8769).get(36867) or ex.get(306)
            if raw:
                taken = datetime.strptime(str(raw)[:19], "%Y:%m:%d %H:%M:%S")
        except Exception:
            pass
        return {"dur": 0.0, "taken": taken or datetime.fromtimestamp(path.stat().st_mtime)}
    out = subprocess.run([tool("ffprobe"), "-v", "error", "-print_format", "json", "-show_format", str(path)],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    try:
        fmt = json.loads(out.stdout)["format"]
        dur = float(fmt["duration"])
    except Exception:
        return {"dur": -1.0, "taken": None}
    raw = (fmt.get("tags") or {}).get("creation_time")
    if raw:
        try:
            taken = datetime.fromisoformat(raw.replace("Z", "+00:00")).astimezone().replace(tzinfo=None)
        except ValueError:
            taken = None
    return {"dur": dur, "taken": taken or datetime.fromtimestamp(path.stat().st_mtime)}


def collect(folder: Path) -> list[dict]:
    if not folder.exists():
        fail(f"영상 폴더가 없습니다: {folder}\n      settings.json 의 \"영상폴더\"를 확인하거나 그 폴더를 만들어 영상을 넣어 주세요.")
    items = []
    for p in sorted(folder.iterdir()):
        ext = p.suffix.lower()
        if ext not in VIDEO_EXT | PHOTO_EXT:
            continue
        info = probe(p)
        if info["dur"] < 0 or (ext in VIDEO_EXT and info["dur"] < 0.6):
            print(f"  (건너뜀) {p.name} — 읽을 수 없거나 0.6초보다 짧음")
            continue
        items.append({"path": p, "photo": ext in PHOTO_EXT, **info})
    if len(items) < 2:
        fail(f"{folder} 에 쓸 수 있는 영상·사진이 2개 이상 있어야 합니다(지금 {len(items)}개).")
    items.sort(key=lambda x: x["taken"])
    d0 = items[0]["taken"].date()
    for it in items:
        it["day"] = (it["taken"].date() - d0).days + 1
    return items


def photo_input(it: dict) -> Path:
    """사진은 방향(EXIF)을 바로잡아 임시 jpg 로."""
    out = WORK / f"photo_{it['path'].stem}.jpg"
    if not out.exists():
        ImageOps.exif_transpose(Image.open(it["path"])).convert("RGB").save(out, quality=92)
    return out


# ── 글자 레이어 ──────────────────────────────────────────────────────────
def soft(draw_fn) -> Image.Image:
    """글자 뒤에 부드러운 그림자를 깔아 어떤 배경에서도 읽히게."""
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(sh), True)
    sh = sh.filter(ImageFilter.GaussianBlur(9))
    sh.putalpha(sh.getchannel("A").point(lambda v: min(255, int(v * 1.7))))
    img = Image.alpha_composite(sh, Image.new("RGBA", (W, H), (0, 0, 0, 0)))
    draw_fn(ImageDraw.Draw(img), False)
    return img


def fit(text: str, path: str, size: int, max_w: int) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(path, size)
    while size > 30 and f.getlength(text) > max_w:
        size -= 4
        f = ImageFont.truetype(path, size)
    return f


def title_png(s: dict, font: str) -> Path:
    small, big = str(s["제목_작게"]), str(s["제목_크게"])
    a, b = str(s["제목_아래"]), str(s["제목_아래_강조"])

    def draw(d, shadow):
        col = "#000000" if shadow else "#FFFFFF"
        if small:
            d.text((W / 2, 262), small, font=fit(small, font, 40, W - 160), fill=col, anchor="mm")
        if big:
            d.text((W / 2, 362), big, font=fit(big, font, 150, W - 120), fill=col, anchor="mm")
        if a or b:
            f = fit(a + b, font, 60, W - 120)
            wa = d.textlength(a, font=f)
            x = (W - d.textlength(a + b, font=f)) / 2
            d.text((x, 476), a, font=f, fill=col, anchor="lm")
            d.text((x + wa, 476), b, font=f, fill="#000000" if shadow else "#FFE14D", anchor="lm")
    p = WORK / "title.png"
    soft(draw).save(p)
    return p


def label_png(key: str, head: str, place: str, font: str, pin: bool = True) -> Path:
    """왼쪽 아래 라벨: 노란 딱지(head) + 장면 글자(place). pin 이면 글자 앞에 빨간 위치 핀."""
    def draw(d, shadow):
        y = 1470
        if head:
            f = ImageFont.truetype(font, 64)
            t = head
            l, tp, r, b = d.textbbox((70, y), t, font=f, anchor="lm")
            d.rounded_rectangle([l - 24, tp - 14, r + 24, b + 18], radius=18, fill="#000000" if shadow else "#FFD84D")
            if not shadow:
                d.text((70, y), t, font=f, fill="#0B0B0E", anchor="lm")
            y += 100
        if place:
            x = 52
            if pin:
                col = "#000000" if shadow else "#E5453D"        # 위치 핀(빨간 물방울 + 흰 점)
                d.ellipse([48, y - 30, 92, y + 14], fill=col)
                d.polygon([(52, y + 2), (88, y + 2), (70, y + 34)], fill=col)
                if not shadow:
                    d.ellipse([62, y - 16, 78, y], fill="#FFFFFF")
                x = 112
            d.text((x, y), place, font=fit(place, font, 58, W - x - 90), fill="#000000" if shadow else "#FFFFFF", anchor="lm")
    p = WORK / f"label_{key}.png"
    soft(draw).save(p)
    return p


# ── 컷 계획 ─────────────────────────────────────────────────────────────
def find_music(s: dict) -> "Path | None":
    """배경음악 파일: "없음"이면 끔, 이름을 적었으면 그 파일, 비웠으면 music 폴더의 첫 음악."""
    want = str(s.get("배경음악") or "").strip()
    if want in ("없음", "끔", "false", "False"):
        return None
    folder = HERE / "music"
    if want:
        for c in (Path(want), folder / want):
            c = c if c.is_absolute() else HERE / c
            if c.exists():
                return c
        fail(f"배경음악 '{want}' 을 찾지 못했습니다. music 폴더에 넣고 파일 이름을 그대로 적어 주세요.")
    songs = sorted(f for f in folder.glob("*") if f.suffix.lower() in AUDIO_EXT) if folder.exists() else []
    return songs[0] if songs else None


def plan(items: list[dict], s: dict) -> tuple[list, list, float]:
    """(도입부 몽타주 컷, 본편 컷, 도입부 길이). 컷 = dict(item, ss, dur, zoom, fx, fy)"""
    beat = float(s["컷길이"])
    intro = bool(s["도입효과"]) and len(items) >= 4
    intro_len = 0.8 + 1.0 if intro else 0.0
    budget = max(4, int((float(s["최대길이"]) - intro_len) / beat))
    n = len(items)
    per = max(1, min(3, budget // n))
    use = items if n * per <= budget or per > 1 else [items[round(i * (n - 1) / (budget - 1))] for i in range(budget)]
    shots = []
    for it in use:
        k = per if (it["photo"] or it["dur"] >= per * (beat + 0.3)) else 1
        for j in range(k):
            zoom = 1.5 if (k > 1 and j % 2 == 1) else 1.0
            ss = 0.0 if it["photo"] else max(0.0, min(it["dur"] - beat - 0.25, it["dur"] * (j + 1) / (k + 1) - beat / 2))
            shots.append({"item": it, "ss": ss, "dur": beat, "zoom": zoom, "fx": 0.5, "fy": 0.42 if zoom > 1 else 0.5})
    tease = []
    if intro:
        for idx in (n - 2, n // 2, max(1, n // 3), min(n - 1, 2)):          # 뒤쪽·가운데 장면을 먼저 보여 줌
            it = items[idx]
            tease.append({"item": it, "ss": 0.0 if it["photo"] else max(0.0, it["dur"] * 0.5 - 0.1), "dur": 0.2})
        first = items[0]
        tease.append({"item": first, "ss": 0.0 if first["photo"] else min(0.3, max(0.0, first["dur"] - 1.3)), "dur": 1.0, "main": True})
        if shots and shots[0]["item"] is first and len([x for x in shots if x["item"] is first]) > 1:
            shots.pop(0)                                    # 첫 영상의 전경 컷은 도입부와 겹치므로 뺌
    return tease, shots, intro_len


def src_args(it: dict, ss: float, dur: float) -> list[str]:
    if it["photo"]:
        return ["-loop", "1", "-t", f"{dur + 0.2}", "-i", str(photo_input(it))]
    return ["-ss", f"{ss:.3f}", "-t", f"{dur + 0.2}", "-i", str(it["path"])]


def main() -> None:
    s = load_settings()
    ffmpeg = tool("ffmpeg")
    WORK.mkdir(exist_ok=True)
    folder = Path(s["영상폴더"])
    items = collect(folder if folder.is_absolute() else HERE / folder)
    font = find_font()
    tease, shots, intro_len = plan(items, s)
    look = ",eq=saturation=1.22:contrast=1.07:brightness=0.01" if s["색보정"] else ""
    cover = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"      # 가로 영상도 화면 가득
    ins, fc, vs, idx = [], [], [], 0

    for k, c in enumerate(tease):                         # 도입부: 번쩍임 + 색 번짐 + 당겼다 풀리는 줌
        ins += src_args(c["item"], c["ss"], c["dur"]); d = c["dur"]
        main_cut = c.get("main")
        z = f"({1 if main_cut else 1.035}+0.06*t/{d}+{0.26 if main_cut else 0.35}*exp(-13*t))"
        sx = "+16*exp(-8*t)*sin(72*t)" if main_cut else ""
        sy = "+12*exp(-8*t)*cos(61*t)" if main_cut else ""
        cw = W if main_cut else W + 32
        f = (f"[{idx}:v]fps={FPS},setpts=PTS-STARTPTS,{cover},scale=w='{W}*{z}':h=-2:eval=frame:flags=bicubic,"
             f"crop={cw}:{H}:x='(in_w-{cw})/2{sx}':y='(in_h-{H})/2{sy}',setsar=1")
        if not main_cut:
            f += f",rgbashift=rh=-16:bh=16:enable='lt(t,0.16)',crop={W}:{H}"
        f += f",eq=brightness='0.32*exp(-17*t)':eval=frame{look},format=yuv420p,trim=0:{d},setpts=PTS-STARTPTS[v{idx}]"
        fc.append(f); vs.append(f"[v{idx}]"); idx += 1

    for c in shots:                                       # 본편: 0.5초 컷, 컷 안에서 아주 조금 다가감
        ins += src_args(c["item"], c["ss"], c["dur"]); d = c["dur"]
        zz = f"({c['zoom']}*(1+0.035*t/{d}))"
        fc.append(f"[{idx}:v]fps={FPS},setpts=PTS-STARTPTS,{cover},scale=w='{W}*{zz}':h=-2:eval=frame:flags=bicubic,"
                  f"crop={W}:{H}:x='(in_w-{W})*{c['fx']}':y='(in_h-{H})*{c['fy']}',setsar=1{look},format=yuv420p,"
                  f"trim=0:{d},setpts=PTS-STARTPTS[v{idx}]")
        vs.append(f"[v{idx}]"); idx += 1

    total = sum(c["dur"] for c in tease) + sum(c["dur"] for c in shots)
    fc.append("".join(vs) + f"concat=n={len(vs)}:v=1:a=0[c0]")
    ins += ["-loop", "1", "-t", f"{total}", "-i", str(title_png(s, font))]
    fc.append(f"[c0][{idx}:v]overlay=0:0[c1]"); cur, idx = "c1", idx + 1

    # 왼쪽 아래 라벨: 같은 영상에서 나온 컷이 이어지는 동안 유지(도입부 번쩍 구간에는 없음)
    places = {str(k): str(v) for k, v in (s.get("장면글자") or {}).items()}

    def place_of(it):
        return next((v for k, v in places.items() if k and k in it["path"].name), "")
    timeline, t = [], 0.0
    for c in tease + shots:
        if not (c in tease and not c.get("main")):
            timeline.append((c["item"], t, t + c["dur"]))
        t += c["dur"]
    spans = []
    for it, a, b in timeline:
        if spans and spans[-1][0] is it and abs(spans[-1][2] - a) < 1e-6:
            spans[-1][2] = b
        else:
            spans.append([it, a, b])
    multi_day = len({it["day"] for it in items}) > 1
    mode = str(s["머리표"]).strip()
    order = {id(it): n for n, it in enumerate(sorted(items, key=lambda x: x["taken"]), 1)}

    def head_of(it) -> str:
        if mode == "DAY":
            return f"DAY {it['day']}" if multi_day else ""     # 하루치뿐이면 DAY 는 뺌
        if mode == "번호":
            return f"{order[id(it)]:02d}"
        if mode == "시간":
            h = it["taken"].hour
            return f"{'오전' if h < 12 else '오후'} {h % 12 or 12}시"
        return ""
    for k, (it, a, b) in enumerate(spans):
        head, place = head_of(it), place_of(it)
        if not head and not place:
            continue
        ins += ["-loop", "1", "-t", f"{total}", "-i", str(label_png(f"{k}", head, place, font, bool(s["핀"])))]
        fc.append(f"[{cur}][{idx}:v]overlay=0:0:enable='between(t,{a:.3f},{b - 0.001:.3f})'[l{k}]")
        cur, idx = f"l{k}", idx + 1
    fc.append(f"[{cur}]format=yuv420p[v]")

    # 소리: 무음 바탕 + 도입부 효과음(sfx 폴더에 파일이 있을 때만)
    fc.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{total}[sil]")
    mix, sfx = ["[sil]"], HERE / "sfx"
    if s["효과음"] and tease:
        events = [("click", i * 0.2, -9) for i in range(4)] + [("whoosh", 0.75, -9), ("pop", 0.85, -7)]
        for k, (name, at, vol) in enumerate(events):
            f = sfx / f"{name}.wav"
            if not f.exists():
                continue
            ins += ["-i", str(f)]
            fc.append(f"[{idx}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={vol}dB,"
                      f"adelay={int(at * 1000)}:all=1[s{k}]")
            mix.append(f"[s{k}]"); idx += 1
    music = find_music(s)
    if music:                                             # 배경음악: 짧으면 반복, 앞뒤로 부드럽게
        ins += ["-stream_loop", "-1", "-ss", f"{float(s['음악시작']):.3f}", "-i", str(music)]
        fade_out = min(1.0, total / 3)
        fc.append(f"[{idx}:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{total:.3f},"
                  f"asetpts=PTS-STARTPTS,volume={float(s['음악크기'])}dB,afade=t=in:d=0.3,"
                  f"afade=t=out:st={total - fade_out:.3f}:d={fade_out:.3f}[bgm]")
        mix.append("[bgm]"); idx += 1
    fc.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=first[au]")

    out = HERE / "output" / "shorts.mp4"
    out.parent.mkdir(exist_ok=True)
    (WORK / "graph.txt").write_text(";\n".join(fc), encoding="utf-8")
    print(f"영상·사진 {len(items)}개 → 컷 {len(tease) + len(shots)}개, {total:.1f}초로 만드는 중…")
    r = subprocess.run([ffmpeg, "-v", "error", "-y", *ins, "-filter_complex_script", str(WORK / "graph.txt"),
                        "-map", "[v]", "-map", "[au]", "-t", f"{total:.3f}", "-r", str(FPS),
                        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(out)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0 and "filter_complex_script" in (r.stderr or ""):      # 최신 ffmpeg: 옵션 이름이 바뀜
        r = subprocess.run([ffmpeg, "-v", "error", "-y", *ins, "-/filter_complex", str(WORK / "graph.txt"),
                            "-map", "[v]", "-map", "[au]", "-t", f"{total:.3f}", "-r", str(FPS),
                            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(out)],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        fail("ffmpeg 가 영상을 만들지 못했습니다:\n" + "\n".join((r.stderr or "").strip().splitlines()[-6:]))
    print(f"완성: {out}  ({total:.1f}초)")
    print(f"배경음악: {music.name if music else '없음 (music 폴더에 음악 파일을 넣으면 들어갑니다)'}")
    print(f"주제: {s.get('주제')}  (머리표 {mode}, 핀 {'있음' if s['핀'] else '없음'})")
    print("장면마다 글자를 넣으려면 settings.json 의 \"장면글자\"에  \"파일 이름 일부\": \"한 줄\"  을 적으세요.")
    for it in items:
        print(f"  {head_of(it) or '-':8s} {it['path'].name}" + (f"  → {place_of(it)}" if place_of(it) else ""))


if __name__ == "__main__":
    main()
