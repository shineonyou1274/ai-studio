# 외부 AI 작업 지시서 — 소울체인지 6화 PC 쪽 컷 7개 (Kling 6 · Dreamina 1)

이 지시서는 클라우드 스튜디오(편집장)가 PC 쪽 AI에게 넘기는 작업입니다. 받은 AI는 아래만 하고, 결과를 지정한 위치에 올린 뒤 보고합니다.
근거 문서: 클라우드 `studio/projects/soulchange-ep06/02_기획/대본_v4.md` **5-2절**(연출 다양성 v4.4, 2026-10-26). 아래 프롬프트는 그 절과 글자 하나까지 같습니다. 5절·`대본_v3.md`의 옛 프롬프트는 쓰지 않습니다.

- **마감: 10/31(토)까지 7컷 전부.** (6화 공개 11/3(화) 18:00)
- Higgsfield 컷(H1·H2·H3)은 클라우드에서 이미 만들었습니다. PC 쪽은 아래 K·D 컷만 만듭니다.

## 0. 먼저 읽을 것
- `C:\Users\경남교육청\youtube-ops\series\_soulchange_kit\소울체인지_제작규칙.md`
- 같은 폴더 `캐릭터_음성_설정.md`
- 5화 지시서 2절(사람 없는 참조 그림 만들기). 5화 때 만든 `episodes\ep5\refs\office_nopeople.png`를 그대로 씁니다. 없으면 5화 지시서 2절대로 먼저 만듭니다.

## 1. 할 일
- 도구: **Kling**(사장님 계정) 6컷 / **Dreamina Seedance 2.5**(사장님 계정, 480P) 1컷
- 세로 9:16, 소리 끔(배경음 금지). 길이는 컷마다 다릅니다(아래 표 "생성 길이").
- **Dreamina는 하루 1개.** 6화 몫은 K8 하나이고, **10/27(화)** 에 만듭니다(5화 Dreamina 몫이 남아 있으면 그 다음 날). 10/28·10/29 Dreamina는 7화 지시서 차례입니다.
- Kling은 언제든 만들어도 되지만, **K2를 먼저 만듭니다.** K2의 마지막 프레임(향수병)을 7화 K1과 8화 K7이 참조로 씁니다.
- 이번 화부터 **장면·앵글·카메라를 다채롭게**(사장님 결정 2026-10-26). 프롬프트의 Camera·Lighting 줄(아크·돌리 인·탑·역광·블라인드 줄무늬·형광등 깜빡임)이 결과에 실제로 보여야 합니다(4절 확인 기준).

## 2. 참조 이미지
| 쓸 그림 | 경로 | 쓰는 컷 |
|---|---|---|
| 사람 없는 교무실 | `C:\Users\경남교육청\youtube-ops\series\_soulchange_kit\episodes\ep5\refs\office_nopeople.png` | K2, K7, K8 |
| 담임 | `...\_soulchange_kit\characters\담임_refT.png` | K8 |
| 담임 클로즈업 | `...\_soulchange_kit\characters\담임_클로즈업_still_A_cu.png` | K8 |
- 키트의 교실 그림(`backgrounds\교실_still_class_B.png`)에는 지우 얼굴이 크게 들어 있습니다. **교실 컷(K3·K4·K5·K11)은 참조 없이 글→영상**으로 만듭니다.
- 원본 그림은 고치지 않습니다.

## 3. 컷별 지시

공통 머리말(모든 프롬프트 맨 앞, 글자 그대로 — 아래 프롬프트 첫 줄에 이미 들어 있음):
"Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI."

| 순서 | 컷 | 도구 · 생성 길이 | 첨부할 참조 | 쓰는 구간 | 저장 파일명 |
|---|---|---|---|---|---|
| 1 | **K2** 최 쌤 뒷모습 + 문 닫는 팔 | Kling 5초 | `episodes\ep5\refs\office_nopeople.png` | 1.2–5.0초 | `episodes\ep6\clips\K02.mp4` (+ 마지막 프레임 `episodes\ep6\refs\K02_last.png`) |
| 2 | **K3** 텀블러(인서트) | Kling 5초 | 없음(글→영상) | 0–3.5초 | `episodes\ep6\clips\K03.mp4` |
| 3 | **K4** 쪽지 줍는 손(인서트) | Kling 5초 | 없음 | 2.2–5.0초 | `episodes\ep6\clips\K04.mp4` |
| 4 | **K5** 회상, 컵 마시는 시늉 | Kling 5초 | 없음 | 0–3.8초 | `episodes\ep6\clips\K05.mp4` |
| 5 | **K7** 옆자리 선생님 뒷모습 | Kling 10초 | `episodes\ep5\refs\office_nopeople.png` | 0–1.8초(K7a) + 2.6–7.2초(K7b) | `episodes\ep6\clips\K07.mp4` |
| 6 | **K11** 창밖 벤치 + 허리 짚는 손 | Kling 10초 | 없음 | 0–10초 전부 | `episodes\ep6\clips\K11.mp4` (+ 마지막 프레임 `episodes\ep6\refs\K11_last.png`) |
| 10/27 | **K8** 담임 몸 아는 척 끄덕 → 폰 | Dreamina 5초 | ① 담임_refT ② 담임_클로즈업 ③ office_nopeople | 0–5초 전부(편집에서 5.3초) | `episodes\ep6\clips\K08.mp4` |

Kling이 막히면(한도·로그인) 그 컷은 Dreamina로 하루 1개씩 이어서 만들고 그 사실을 보고합니다(7화 Dreamina 순서가 하루씩 밀림 — 보고에 적기).

### K2 — Kling 5초 (쓰는 구간 1.2–5.0)
```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
Subject: a corner desk in a Korean school teachers' office in the daytime. A female teacher in her thirties with a low ponytail and a beige cardigan sits at the desk with her back to the camera, her face not visible, her forehead lowered onto one hand. On the desk beside the monitor stand a small round glass perfume bottle with a gold cap and no logo, and a tissue box. Behind her, a glass-paneled door to the hallway is half open.
Action 1 (0-2.5s): the seated teacher's shoulders shake with quiet sobs and her back rises and falls unevenly.
Action 2 (2.5-5s): an older man's arm in a gray suit sleeve reaches in from the edge of the frame and quickly slides the hallway door shut; his face is out of frame.
No faces visible.
Lighting: afternoon light through window blinds lays slanted stripes across her back and the desk; a small glint on the perfume bottle; cool fluorescent fill.
Mood: heavy, hushed.
Camera: medium-wide from behind, lower than her seated shoulder height, slow arc from behind her back toward the hallway door so the closing door ends up in frame. No one looks at the camera.
```

### K3 (인서트) — Kling 5초 (쓰는 구간 0–3.5)
```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
Subject: an open stainless steel tumbler stands on the teacher's desk at the front of an empty Korean high school classroom, its lid lying on its side next to it; a folded attendance book and a whiteboard marker rest nearby. Rows of empty student desks recede behind it. No people.
Action 1 (0-2.5s): a window curtain in the background lifts slowly in a breeze and falls back.
Action 2 (2.5-5s): dust drifts slowly through the beam of light behind the tumbler.
Lighting: backlit by low late-afternoon sun from the windows behind the tumbler, a bright edge of light along the steel rim, floating dust in the light beam, cool shadows in front.
Mood: quiet, uneasy.
Camera: extreme close-up at desk height, low angle, slow dolly-in with a rack focus from the curtain to the tumbler rim. No one looks at the camera.
```

### K4 (인서트) — Kling 5초 (쓰는 구간 2.2–5.0)
```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
Subject: the floor between student desks in an empty Korean high school classroom in the afternoon. A crumpled piece of lined notebook paper lies on the floor. Only a woman's hands and beige cardigan sleeves enter the frame; no faces.
Action 1 (0-2s): one hand reaches down and picks up the crumpled paper.
Action 2 (2-5s): both hands unfold the paper and hold it flat toward the camera at chest height, the fingers trembling slightly; the side of the paper facing the camera is blank.
Lighting: an overhead fluorescent tube flickers once or twice, cool flat afternoon light from the windows.
Mood: cold, shaken.
Camera: top-down shot looking straight down at the floor, then the camera tilts up following the paper to chest height. No one looks at the camera.
```

### K5 (회상) — Kling 5초 (쓰는 구간 0–3.8)
```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
Subject: the view into a Korean high school classroom during a break, seen from just behind a female teacher standing in the doorway; only her beige cardigan shoulder and low ponytail are visible at the left edge, her face not visible. About ten students in navy blazer uniforms sit and stand in the room, all softly out of focus; the nearest boy in the second row is seen from the side.
Action 1 (0-2.5s): the boy in the second row lifts an empty hand to his mouth as if drinking from a cup, and two students near him smile and glance at each other.
Action 2 (2.5-5s): the teacher's hand at the left edge tightens around an attendance book and slowly lowers it to her side.
Lighting: hazy, slightly overexposed afternoon light flooding in from the windows, washed-out colors like a memory.
Mood: uncomfortable, mocking, cold.
Camera: handheld over the teacher's shoulder from the doorway, slight dutch tilt, a quick small push-in on the boy's gesture. No one looks at the camera.
```

### K7 (K7a + K7b) — Kling 10초 (쓰는 구간 0–1.8 / 2.6–7.2)
```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
Subject: a Korean school teachers' office in the daytime. In the foreground, a female teacher in her forties with short permed hair and a gray cardigan is seen from behind and slightly to the side, her face turned away from the camera. Beyond her shoulder sits a middle-aged man in a navy cardigan and white shirt, blurred.
Action 1 (0-2.5s): she half-turns her head toward the man for a moment, then turns it back, her face still turned away from the camera.
Action 2 (2.5-6s): she lays her hand on the man's forearm and gives it a small knowing pat.
Action 3 (6-10s): she tilts her head toward the far corner of the office and slowly pulls her hand back, her shoulders dropping with a sigh.
Lighting: slanted stripes of daylight through window blinds across her shoulder and the desk, neutral fluorescent fill.
Mood: briefly puzzled, then hushed and knowing.
Camera: starts close over her shoulder from behind at eye level, then a slow arc around her shoulder rising to a slightly high angle. No one looks at the camera.
```

### K8 — Dreamina 5초 (10/27, 쓰는 구간 전부)
(0.1–1.6초 짧게 말하는 입 / 1.8초부터 입 다묾)
```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
Subject: the middle-aged Korean male teacher from the reference image (graying hair, navy cardigan, white shirt, striped tie, eyeglass cord) sits at his desk in a teachers' office, close-up from the chest up, three-quarter view; a gray cardigan shoulder is blurred at the right edge.
Action 1 (0-1.8s): he gives several quick small nods with an awkward stiff smile and says a couple of words, while his fingers fiddle with the ends of his cardigan sleeves like a nervous teenage girl.
Action 2 (1.8-5s): his smile drops; his mouth stays closed, no speaking; his eyes drift sideways and he slides a smartphone out from under the edge of the desk and looks down at it, breathing slowly.
Lighting: a cool bluish glow from the computer monitor lights his face from below, soft window daylight from the left.
Mood: flustered, then uneasy.
Camera: low-angle close-up past the blurred shoulder, a quick dolly-in on the nods, then the camera tilts down with his eyes toward the phone. No one looks at the camera.
```

### K11 — Kling 10초 (쓰는 구간 전부)
```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
Subject: a view through a Korean high school classroom window toward the far edge of a dirt sports field in the late afternoon. On a bench by the fence at the far end, a lone student in a navy blazer with a gray hood pulled up sits with his back to the camera, small in the frame. In the foreground, the blurred window frame, a navy blazer sleeve and a girl's hand rest on the windowsill.
Action 1 (0-3s): the distant student sits hunched with his hands in his pockets and scuffs the dirt with one shoe.
Action 2 (3-5.5s): the hand on the windowsill slowly closes into a fist.
Action 3 (5.5-10s): the hand opens, leaves the windowsill and presses against the lower back, the blazer shoulder stretching backward like a stiff middle-aged man; a few dry leaves drift across the field.
Lighting: backlit by a low orange sunset sun beyond the field, the distant bench figure a small silhouette, a warm orange rim of light on the hand and sleeve at the window.
Mood: worried, then wry.
Camera: starts focused on the blurred hand at the window, racks focus to the distant bench and slowly dollies in; on Action 3 a small tilt up following the hand. No one looks at the camera.
```

## 4. 확인 기준 (생성 직후 직접 보고, 어긋나면 한 번만 다시 생성)

모든 컷 공통
- **아무도 카메라를 보지 않는가**(눈이 렌즈를 향하는 순간이 한 번이라도 있으면 불합격).
- 화면에 글자·상표가 생기지 않았는가(쪽지·폰 화면은 비어 있어야 함, 글씨는 클라우드에서 코드로 얹음).
- 쓰는 구간 안에서 화면이 멈춰 보이지 않는가(사람·카메라가 계속 조금씩 움직임).
- **프롬프트의 카메라 무빙과 빛이 실제로 보이는가**(아크·돌리 인·탑 틸트·역광 등). 카메라가 거의 고정이면 불합격 사유로 적고 한 번 다시.

컷별
| 컷 | 꼭 볼 것 |
|---|---|
| K2 | 최 쌤 **얼굴 0**(뒷모습·낮은 포니테일·베이지 카디건). 모니터 옆 **둥근 유리 향수병(금색 뚜껑)이 끝까지 보임** — 7화 K1·8화 K7 참조라 가장 중요. 2.5초 뒤 회색 정장 팔이 복도 문을 닫음(얼굴 밖). 블라인드 줄무늬가 등에 보임. 카메라가 등 뒤에서 문 쪽으로 돎 |
| K3 | 사람 0. 텀블러 뚜껑이 옆에 놓임. 뒤에서 오는 햇빛으로 텀블러 테두리가 밝게 빛남(역광), 먼지. 침·액체를 보여 주는 장면이 생기면 불합격 |
| K4 | 손·베이지 소매만, **얼굴 0**. 쪽지 앞면(카메라 쪽)이 비어 있음. 위에서 내려다보다 가슴 높이로 따라 올라옴. 형광등 깜빡임은 있으면 좋고 없어도 통과 |
| K5 | 문간 선생님은 어깨·포니테일만(얼굴 0). 학생들 흐림, 둘째 줄 남학생이 빈손으로 컵 마시는 시늉(옆모습). **학생 얼굴이 또렷하게 카메라를 보면 불합격.** 뿌옇고 바랜 색 |
| K7 | 여교사 **얼굴 0**(뒤·옆모습, 짧은 파마, 회색 카디건). 0–2.5초 고개를 반쯤 돌렸다 돌아감(크게 홱 돌리면 불합격 — 6화는 '거의 못 알아챔'). 팔뚝 토닥 → 구석 쪽으로 고개. 담임은 흐림 |
| K8 | 담임 얼굴·희끗한 머리·남색 카디건·넥타이·안경 줄 유지. 0–1.8초 끄덕이며 짧게 말하고 소매 끝 만지작, **1.8초부터 입 다묾**(입이 계속 움직이면 불합격 — 속마음이 얹힘). 아래에서 오는 모니터 빛. 웃는 얼굴이 끝까지 가면 불합격 |
| K11 | 먼 벤치 학생은 **작은 뒷모습만**(얼굴·몸을 흔드는 동작 없음 — 그 학생은 증상처럼 보이는 몸짓 금지). 앞쪽 손이 주먹 → 허리 짚기. 노을 역광, 벤치 실루엣 |

- 2번 다시 해도 안 되면 멈추고 그 사실과 원인 추측을 보고합니다.

## 5. 결과 올리기
- 저장: `C:\Users\경남교육청\youtube-ops\series\_soulchange_kit\episodes\ep6\clips\` (마지막 프레임 PNG는 `episodes\ep6\refs\`)
- 쓴 크레딧, 시도 횟수, 첨부한 참조, 실제 사용 프롬프트, 확인 기준 통과 여부를 `episodes\ep6\생성로그.md`에 적기(5화 `episodes\ep5\생성로그.md`와 같은 표 형식)
- `git add series/_soulchange_kit/episodes/ep6 && git commit -m "6화 PC 컷" && git push` (100MB 넘는 파일은 빼고 보고)
- 보고에 넣을 것: 만든 컷 목록, 다시 뽑은 컷과 이유, 남은 Dreamina·Kling 크레딧, 못 만든 컷, **K2_last.png를 올렸는지**(7화 K1이 기다림)
