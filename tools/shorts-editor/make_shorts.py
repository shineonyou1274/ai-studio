# -*- coding: utf-8 -*-
"""쇼츠 편집기 — 폴더에 넣은 영상·사진을 9:16 쇼츠 한 편으로 이어 붙입니다.
여행, 맛집, 일상 브이로그, 매장·병원 홍보처럼 '찍어 둔 장면을 이어 붙이는' 영상용입니다.

쓰는 법
    1. 이 파일 옆의 videos 폴더에 영상(mp4·mov)과 사진(jpg·png)을 넣습니다.
    2. settings.json 에서 주제와 제목 문구를 바꿉니다.
    3. python make_shorts.py   →  output/shorts.mp4

화면비율("9:16"·"16:9"·"1:1"·"4:5")과 길이(최대길이, 초)를 바꿀 수 있습니다.
"장면"에 파일과 시작·끝 초를 적으면 그 구간만 그 순서대로 씁니다(직접 고르기).
"앞영상"·"뒤영상"에 motion 폴더의 영상(Claude Motion 등으로 만든 오프닝·엔딩)을 적으면 앞뒤에 붙습니다.

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
W, H, FPS = 1080, 1920, 30            # W, H 는 settings.json 의 "화면비율"로 바뀜
RATIOS = {"9:16": (1080, 1920), "16:9": (1920, 1080), "1:1": (1080, 1080), "4:5": (1080, 1350)}
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
    "화면비율": "9:16",      # "9:16"(쇼츠·릴스) | "16:9"(유튜브·공모전) | "1:1" | "4:5"(인스타·스레드)
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
    "제목효과": "팝",        # "팝" | "슬라이드" | "펼치기" | "없음"
    "제목시작": 0,           # 제목이 나오는 시각(초)
    "글자효과": "슬라이드",  # 장면 글자가 왼쪽에서 밀려 들어옴. "없음"이면 그냥 나타남
    "글자효과음": True,      # 장면 글자가 나올 때 '딸깍'
    "장면": [],              # 직접 고르기: [{"파일": "clip3", "시작": 5, "끝": 9, "글자": "한 줄", "효과음": "whoosh"}]
    "앞영상": "",            # motion 폴더의 오프닝 영상 파일 이름
    "뒤영상": "",            # motion 폴더의 엔딩 영상 파일 이름
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


def collect(folder: Path, need: int = 2) -> list[dict]:
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
    if len(items) < need:
        fail(f"{folder} 에 쓸 수 있는 영상·사진이 {need}개 이상 있어야 합니다(지금 {len(items)}개).")
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
def scale_k() -> float:
    """글자 크기 배율: 세로 쇼츠(9:16)는 원래 크기, 다른 비율은 조금 작게."""
    return 1.0 if (W, H) == (1080, 1920) else 0.8


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


def title_png(s: dict, font: str) -> "tuple[Path, int, int] | None":
    """제목을 글자 부분만 잘라 저장. (파일, 왼쪽 위 x, y). 제목이 비었으면 None."""
    small, big = str(s["제목_작게"]), str(s["제목_크게"])
    a, b = str(s["제목_아래"]), str(s["제목_아래_강조"])
    k, y0 = scale_k(), H * 0.1365

    def draw(d, shadow):
        col = "#000000" if shadow else "#FFFFFF"
        if small:
            d.text((W / 2, y0), small, font=fit(small, font, int((40 if k == 1 else 48) * k), W - 160), fill=col, anchor="mm")
        if big:
            d.text((W / 2, y0 + 100 * k), big, font=fit(big, font, int(150 * k), W - 120), fill=col, anchor="mm")
        if a or b:
            f = fit(a + b, font, int(60 * k), W - 120)
            wa = d.textlength(a, font=f)
            x = (W - d.textlength(a + b, font=f)) / 2
            d.text((x, y0 + 214 * k), a, font=f, fill=col, anchor="lm")
            d.text((x + wa, y0 + 214 * k), b, font=f, fill="#000000" if shadow else "#FFE14D", anchor="lm")
    img = soft(draw)
    box = img.getbbox()
    if not box:
        return None
    l, t, r, btm = max(0, box[0] - 4), max(0, box[1] - 4), min(W, box[2] + 4), min(H, box[3] + 4)
    l, t = l - l % 2, t - t % 2
    r, btm = r + (r - l) % 2, btm + (btm - t) % 2
    p = WORK / "title.png"
    img.crop((l, t, r, btm)).save(p)
    return p, l, t


def label_png(key: str, head: str, place: str, font: str, pin: bool = True) -> Path:
    """왼쪽 아래 라벨: 노란 딱지(head) + 장면 글자(place). pin 이면 글자 앞에 빨간 위치 핀."""
    k = scale_k()

    def draw(d, shadow):
        y = H - 450 * k
        if head:
            f = ImageFont.truetype(font, int(64 * k))
            l, tp, r, b = d.textbbox((70 * k, y), head, font=f, anchor="lm")
            d.rounded_rectangle([l - 24 * k, tp - 14 * k, r + 24 * k, b + 18 * k], radius=18 * k,
                                fill="#000000" if shadow else "#FFD84D")
            if not shadow:
                d.text((70 * k, y), head, font=f, fill="#0B0B0E", anchor="lm")
            y += 100 * k
        if place:
            x = 52 * k
            if pin:
                col = "#000000" if shadow else "#E5453D"        # 위치 핀(빨간 물방울 + 흰 점)
                d.ellipse([48 * k, y - 30 * k, 92 * k, y + 14 * k], fill=col)
                d.polygon([(52 * k, y + 2 * k), (88 * k, y + 2 * k), (70 * k, y + 34 * k)], fill=col)
                if not shadow:
                    d.ellipse([62 * k, y - 16 * k, 78 * k, y], fill="#FFFFFF")
                x = 112 * k
            d.text((x, y), place, font=fit(place, font, int(58 * k), int(W - x - 90)),
                   fill="#000000" if shadow else "#FFFFFF", anchor="lm")
    p = WORK / f"label_{key}.png"
    soft(draw).save(p)
    return p


# ── 파일 찾기 ───────────────────────────────────────────────────────────
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


def find_clip(key: str) -> "Path | None":
    """앞영상·뒤영상: motion 폴더나 이 폴더 기준 경로. 비었으면 None."""
    want = str(key or "").strip()
    if not want or want == "없음":
        return None
    for c in (Path(want), HERE / "motion" / want, HERE / want):
        c = c if c.is_absolute() else HERE / c
        if c.exists():
            return c
    fail(f"'{want}' 을 찾지 못했습니다. motion 폴더에 넣고 파일 이름을 그대로 적어 주세요.")


def find_sfx(name: str) -> "Path | None":
    """효과음 이름(click·whoosh·pop 또는 sfx 폴더에 넣은 파일 이름)."""
    name = str(name or "").strip()
    if not name or name == "없음":
        return None
    folder = HERE / "sfx"
    for c in [folder / name] + [folder / (name + e) for e in (".wav", ".mp3", ".m4a")]:
        if c.exists():
            return c
    print(f"  (알림) 효과음 '{name}' 이 sfx 폴더에 없어 뺐습니다.")
    return None


def has_audio(path: Path) -> bool:
    out = subprocess.run([tool("ffprobe"), "-v", "error", "-select_streams", "a", "-show_entries", "stream=index",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return bool(out.stdout.strip())


# ── 컷 계획 ─────────────────────────────────────────────────────────────
def plan(items: list[dict], s: dict) -> tuple[list, list, float]:
    """자동 모드: (도입부 몽타주 컷, 본편 컷, 도입부 길이). 컷 = dict(item, ss, dur, zoom, fx, fy)"""
    beat = float(s["컷길이"])
    intro = bool(s["도입효과"]) and len(items) >= 4
    intro_len = 0.8 + 1.0 if intro else 0.0
    budget = max(4, int((float(s["최대길이"]) - intro_len) / beat))
    n = len(items)
    per = max(1, budget // n)                              # 영상이 적고 길이가 길면 한 영상에서 여러 컷
    use = items if n * per <= budget or per > 1 else [items[round(i * (n - 1) / (budget - 1))] for i in range(budget)]
    shots = []
    for it in use:
        k = per if it["photo"] else max(1, min(per, int(it["dur"] / (beat + 0.3))))
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


def plan_scenes(items: list[dict], s: dict) -> tuple[list, list, float]:
    """직접 고르기 모드: settings.json 의 "장면" 순서대로, 적은 구간만 씀."""
    shots = []
    for n, sc in enumerate(s["장면"], 1):
        if not isinstance(sc, dict) or not str(sc.get("파일", "")).strip():
            fail(f"\"장면\" {n}번째에 \"파일\"이 없습니다. 예: {{\"파일\": \"clip3\", \"시작\": 5, \"끝\": 9}}")
        key = str(sc["파일"]).strip()
        it = next((x for x in items if key in x["path"].name), None)
        if it is None:
            fail(f"\"장면\" {n}번째의 파일 '{key}' 을 videos 폴더에서 찾지 못했습니다.")
        if it["photo"]:
            ss, dur = 0.0, float(sc.get("길이", 2.0))
        else:
            ss = float(sc.get("시작", 0))
            end = float(sc.get("끝", it["dur"]))
            end = min(end, it["dur"])
            if ss >= end - 0.2:
                fail(f"\"장면\" {n}번째({it['path'].name})의 시작({ss})·끝({end}) 초를 확인해 주세요. 영상 길이는 {it['dur']:.1f}초입니다.")
            dur = end - ss
        shots.append({"item": it, "ss": ss, "dur": dur, "zoom": float(sc.get("확대", 1.0)), "fx": 0.5, "fy": 0.5,
                      "scene": n, "text": str(sc.get("글자", "")), "sfx": sc.get("효과음", "")})
    tease, intro_len = [], 0.0
    if s["도입효과"] and len(shots) >= 4:
        m = len(shots)
        for i in (m - 2, m // 2, max(1, m // 3), min(m - 1, 2)):
            c = shots[i]
            tease.append({"item": c["item"], "ss": c["ss"] + c["dur"] / 2 - 0.1 if not c["item"]["photo"] else 0.0, "dur": 0.2})
        first = shots[0]
        tease.append({**first, "dur": 1.0, "main": True})
        intro_len = 1.8
        if first["dur"] > 1.4:
            first["ss"] += 0.0 if first["item"]["photo"] else 1.0
            first["dur"] -= 1.0
        else:
            shots.pop(0)
    return tease, shots, intro_len


def src_args(it: dict, ss: float, dur: float) -> list[str]:
    if it["photo"]:
        return ["-loop", "1", "-t", f"{dur + 0.2}", "-i", str(photo_input(it))]
    return ["-ss", f"{ss:.3f}", "-t", f"{dur + 0.2}", "-i", str(it["path"])]


# ── 렌더 ────────────────────────────────────────────────────────────────
def run_ffmpeg(ffmpeg: str, ins: list, graph: list, out_args: list, name: str) -> None:
    gp = WORK / f"{name}.txt"
    gp.write_text(";\n".join(graph), encoding="utf-8")
    for opt in ("-filter_complex_script", "-/filter_complex"):     # 최신 ffmpeg: 옵션 이름이 바뀜
        r = subprocess.run([ffmpeg, "-v", "error", "-y", *ins, opt, str(gp), *out_args],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode == 0 or "filter_complex_script" not in (r.stderr or ""):
            break
    if r.returncode != 0:
        fail("ffmpeg 가 영상을 만들지 못했습니다:\n" + "\n".join((r.stderr or "").strip().splitlines()[-6:]))


def cut_filter(c: dict, i: int, d: float, look: str, tease: bool) -> str:
    cover = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"      # 가로 영상도 화면 가득
    if tease:                                             # 도입부: 번쩍임 + 색 번짐 + 당겼다 풀리는 줌
        main_cut = c.get("main")
        z = f"({1 if main_cut else 1.035}+0.06*t/{d}+{0.26 if main_cut else 0.35}*exp(-13*t))"
        sx = "+16*exp(-8*t)*sin(72*t)" if main_cut else ""
        sy = "+12*exp(-8*t)*cos(61*t)" if main_cut else ""
        cw = W if main_cut else W + 32
        f = (f"[{i}:v]fps={FPS},setpts=PTS-STARTPTS,{cover},scale=w='{W}*{z}':h=-2:eval=frame:flags=bicubic,"
             f"crop={cw}:{H}:x='(in_w-{cw})/2{sx}':y='(in_h-{H})/2{sy}',setsar=1")
        if not main_cut:
            f += f",rgbashift=rh=-16:bh=16:enable='lt(t,0.16)',crop={W}:{H}"
        return f + f",eq=brightness='0.32*exp(-17*t)':eval=frame{look},format=yuv420p,trim=0:{d},setpts=PTS-STARTPTS[v{i}]"
    # 본편: 컷 안에서 아주 조금 다가감(긴 컷은 천천히)
    zz = f"({c['zoom']}*(1+{min(0.035, 0.02 * d):.4f}*t/{d}))"
    return (f"[{i}:v]fps={FPS},setpts=PTS-STARTPTS,{cover},scale=w='{W}*{zz}':h=-2:eval=frame:flags=bicubic,"
            f"crop={W}:{H}:x='(in_w-{W})*{c['fx']}':y='(in_h-{H})*{c['fy']}',setsar=1{look},format=yuv420p,"
            f"trim=0:{d},setpts=PTS-STARTPTS[v{i}]")


def render_cuts(ffmpeg: str, cuts: list, look: str) -> list[Path]:
    """컷을 40개씩 묶어 중간 파일로 만듦(긴 영상도 메모리 걱정 없이)."""
    parts = []
    for p0 in range(0, len(cuts), 40):
        group, ins, fc = cuts[p0:p0 + 40], [], []
        for i, (c, is_tease) in enumerate(group):
            ins += src_args(c["item"], c["ss"], c["dur"])
            fc.append(cut_filter(c, i, c["dur"], look, is_tease))
        fc.append("".join(f"[v{i}]" for i in range(len(group))) + f"concat=n={len(group)}:v=1:a=0[v]")
        out = WORK / f"part_{p0 // 40:03d}.mp4"
        print(f"  컷 {p0 + 1}~{p0 + len(group)} / {len(cuts)} 만드는 중…")
        run_ffmpeg(ffmpeg, ins, fc, ["-map", "[v]", "-r", str(FPS), "-c:v", "libx264", "-preset", "fast",
                                     "-crf", "14", "-pix_fmt", "yuv420p", str(out)], f"part_{p0 // 40:03d}")
        parts.append(out)
    return parts


TITLE_FX = ("팝", "슬라이드", "펼치기", "없음")


def main() -> None:
    global W, H
    s = load_settings()
    ratio = str(s.get("화면비율", "9:16")).strip()
    if ratio not in RATIOS:
        fail(f"화면비율 '{ratio}' 은 쓸 수 없습니다. 가능: {', '.join(RATIOS)}")
    W, H = RATIOS[ratio]
    ffmpeg = tool("ffmpeg")
    if WORK.exists():
        shutil.rmtree(WORK, ignore_errors=True)
    WORK.mkdir(exist_ok=True)
    folder = Path(s["영상폴더"])
    manual = bool(s.get("장면"))
    items = collect(folder if folder.is_absolute() else HERE / folder, 1 if manual else 2)
    font = find_font()
    tease, shots, intro_len = (plan_scenes if manual else plan)(items, s)
    look = ",eq=saturation=1.22:contrast=1.07:brightness=0.01" if s["색보정"] else ""
    total = sum(c["dur"] for c in tease) + sum(c["dur"] for c in shots)

    parts = render_cuts(ffmpeg, [(c, True) for c in tease] + [(c, False) for c in shots], look)
    concat_list = WORK / "parts.txt"
    concat_list.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
    ins = ["-f", "concat", "-safe", "0", "-i", str(concat_list)]
    fc, idx, cur = [], 1, "0:v"
    sfx_events = []                                       # (파일, 시각, 크기 dB)
    use_sfx = bool(s["효과음"])
    k = scale_k()

    # 제목: 효과(팝·슬라이드·펼치기)와 함께 등장
    title = title_png(s, font)
    fx = str(s.get("제목효과", "팝")).strip()
    if fx not in TITLE_FX:
        print(f"  (알림) 제목효과 '{fx}' 는 없는 이름이라 '팝'으로 합니다. 가능: {', '.join(TITLE_FX)}")
        fx = "팝"
    if title:
        tp, tx, ty = title
        st = max(0.0, float(s.get("제목시작", 0)))
        ins += ["-loop", "1", "-t", f"{total}", "-i", str(tp)]
        tw, th = Image.open(tp).size
        T = f"(t-{st})"
        if fx == "팝":
            S = f"max(0.05,1-0.9*exp(-9*{T})*cos(13*{T}))"
            fc.append(f"[{idx}:v]format=rgba,fade=in:st={st}:d=0.12:alpha=1,"
                      f"scale=w='max(2,trunc(iw*{S}/2)*2)':h='max(2,trunc(ih*{S}/2)*2)':eval=frame[tt]")
            pos = f"x='{tx + tw / 2}-overlay_w/2':y='{ty + th / 2}-overlay_h/2'"
        elif fx == "슬라이드":
            fc.append(f"[{idx}:v]format=rgba,fade=in:st={st}:d=0.3:alpha=1[tt]")
            pos = f"x={tx}:y='{ty}-{160 * k}*exp(-9*max(0,{T}))'"
        elif fx == "펼치기":
            fc.append(f"[{idx}:v]format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':"
                      f"a='if(lt(X,W*clip((T-{st})/0.6,0,1)),alpha(X,Y),0)'[tt]")
            pos = f"x={tx}:y={ty}"
        else:
            fc.append(f"[{idx}:v]format=rgba[tt]")
            pos = f"x={tx}:y={ty}"
        fc.append(f"[{cur}][tt]overlay={pos}:eval=frame:enable='gte(t,{st})'[c1]")
        cur, idx = "c1", idx + 1
        if use_sfx and fx != "없음":
            sfx_events.append(("pop" if fx == "팝" else "whoosh", st + (0.0 if fx == "팝" else 0.05), -8))

    # 왼쪽 아래 라벨: 같은 영상(직접 고르기면 같은 장면)이 이어지는 동안 유지
    places = {str(kk): str(v) for kk, v in (s.get("장면글자") or {}).items()}

    def place_of(c):
        if c.get("text"):
            return c["text"]
        return next((v for kk, v in places.items() if kk and kk in c["item"]["path"].name), "")
    tease_ids = {id(c) for c in tease}
    timeline, t = [], 0.0
    for c in tease + shots:
        if not (id(c) in tease_ids and not c.get("main")):
            timeline.append((c, c.get("scene", id(c["item"])), t, t + c["dur"]))
        if c.get("sfx") and use_sfx and id(c) not in tease_ids:
            sfx_events.append((c["sfx"], t, -6))
        t += c["dur"]
    spans = []
    for c, key, a, b in timeline:
        if spans and spans[-1][1] == key and abs(spans[-1][3] - a) < 1e-6:
            spans[-1][3] = b
        else:
            spans.append([c, key, a, b])
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
    slide = str(s.get("글자효과", "슬라이드")).strip() != "없음"
    for n, (c, key, a, b) in enumerate(spans):
        head, place = head_of(c["item"]), place_of(c)
        if not head and not place:
            continue
        ins += ["-loop", "1", "-t", f"{b - a:.3f}", "-i", str(label_png(f"{n}", head, place, font, bool(s["핀"])))]
        if slide:
            fc.append(f"[{idx}:v]format=rgba,fade=in:st=0:d=0.18:alpha=1,setpts=PTS+{a:.3f}/TB[lb{n}]")
            fc.append(f"[{cur}][lb{n}]overlay=x='-{70 * k:.0f}*exp(-14*(t-{a:.3f}))':y=0:eval=frame:eof_action=pass[l{n}]")
            if use_sfx and s.get("글자효과음", True) and a > 0.5:
                sfx_events.append(("click", a, -14))
        else:
            fc.append(f"[{idx}:v]setpts=PTS+{a:.3f}/TB[lb{n}]")
            fc.append(f"[{cur}][lb{n}]overlay=0:0:eof_action=pass[l{n}]")
        cur, idx = f"l{n}", idx + 1
    fc.append(f"[{cur}]format=yuv420p,trim=0:{total:.3f},setpts=PTS-STARTPTS[vm]")

    # 소리: 무음 바탕 + 효과음 + 배경음악
    fc.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{total:.3f}[sil]")
    mix = ["[sil]"]
    if use_sfx and tease:
        sfx_events = [("click", i * 0.2, -9) for i in range(4)] + [("whoosh", 0.75, -9), ("pop", 0.85, -7)] + sfx_events
    for n, (name, at, vol) in enumerate(sfx_events):
        f = find_sfx(name)
        if not f or at >= total:
            continue
        ins += ["-i", str(f)]
        fc.append(f"[{idx}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={vol}dB,"
                  f"adelay={int(at * 1000)}:all=1[s{n}]")
        mix.append(f"[s{n}]"); idx += 1
    music = find_music(s)
    if music:                                             # 배경음악: 짧으면 반복, 앞뒤로 부드럽게
        ins += ["-stream_loop", "-1", "-ss", f"{float(s['음악시작']):.3f}", "-i", str(music)]
        fade_out = min(1.0, total / 3)
        fc.append(f"[{idx}:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{total:.3f},"
                  f"asetpts=PTS-STARTPTS,volume={float(s['음악크기'])}dB,afade=t=in:d=0.3,"
                  f"afade=t=out:st={total - fade_out:.3f}:d={fade_out:.3f}[bgm]")
        mix.append("[bgm]"); idx += 1
    fc.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=first[am]")

    # 앞영상·뒤영상(Claude Motion 등으로 만든 오프닝·엔딩): 화면을 자르지 않고 맞춰 붙임
    segs, full = [], total
    for role in ("앞영상", "뒤영상"):
        clip = find_clip(s.get(role, ""))
        if not clip:
            segs.append(None)
            continue
        d = probe(clip)["dur"]
        if d <= 0:
            fail(f"{role} '{clip.name}' 을 읽지 못했습니다.")
        ins += ["-i", str(clip)]
        fc.append(f"[{idx}:v]fps={FPS},scale={W}:{H}:force_original_aspect_ratio=decrease,"
                  f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,format=yuv420p,"
                  f"trim=0:{d:.3f},setpts=PTS-STARTPTS[{role}v]")
        if has_audio(clip):
            fc.append(f"[{idx}:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{d:.3f},"
                      f"apad=whole_dur={d:.3f},asetpts=PTS-STARTPTS[{role}a]")
        else:
            fc.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{d:.3f}[{role}a]")
        segs.append(role)
        idx += 1
        full += d
    order_ = [x for x in (segs[0], "main", segs[1]) if x]
    if len(order_) > 1:
        pads = "".join("[vm][am]" if x == "main" else f"[{x}v][{x}a]" for x in order_)
        fc.append(f"{pads}concat=n={len(order_)}:v=1:a=1[v][au]")
    else:
        fc += ["[vm]null[v]", "[am]anull[au]"]

    out = HERE / "output" / "shorts.mp4"
    out.parent.mkdir(exist_ok=True)
    print(f"영상·사진 {len(items)}개 → 컷 {len(tease) + len(shots)}개, {full:.1f}초({ratio})로 마무리하는 중…")
    run_ffmpeg(ffmpeg, ins, fc, ["-map", "[v]", "-map", "[au]", "-t", f"{full:.3f}", "-r", str(FPS),
                                 "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                                 "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(out)], "final")
    print(f"완성: {out}  ({full:.1f}초, {ratio} {W}x{H})")
    if not manual and total < float(s["최대길이"]) * 0.8:
        print(f"  (알림) 최대길이 {s['최대길이']}초보다 짧게 나왔습니다. 영상이 짧거나 적어서 쓸 장면이 모자랍니다."
              f" 영상을 더 넣거나 \"컷길이\"를 줄여 보세요.")
    print(f"제목효과: {fx if title else '제목 없음'}   글자효과: {'슬라이드' if slide else '없음'}")
    print(f"배경음악: {music.name if music else '없음 (music 폴더에 음악 파일을 넣으면 들어갑니다)'}")
    print(f"주제: {s.get('주제')}  (머리표 {mode}, 핀 {'있음' if s['핀'] else '없음'})")
    if manual:
        print("장면(직접 고르기):")
        for c in shots:
            print(f"  {c['scene']:>2}. {c['item']['path'].name}  {c['ss']:.1f}~{c['ss'] + c['dur']:.1f}초" +
                  (f"  → {c['text']}" if c.get("text") else ""))
    else:
        print("장면마다 글자를 넣으려면 settings.json 의 \"장면글자\"에  \"파일 이름 일부\": \"한 줄\"  을 적으세요.")
        for it in items:
            pl = next((v for kk, v in places.items() if kk and kk in it["path"].name), "")
            print(f"  {head_of(it) or '-':8s} {it['path'].name}" + (f"  → {pl}" if pl else ""))


if __name__ == "__main__":
    main()
