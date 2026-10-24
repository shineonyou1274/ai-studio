# 외부 AI 작업 지시서 — 소울체인지 5화 PC 쪽 컷 7개 (Dreamina 3 · Kling 4)

이 지시서는 클라우드 스튜디오(편집장)가 PC 쪽 AI에게 넘기는 작업입니다. 받은 AI는 아래만 하고, 결과를 지정한 위치에 올린 뒤 보고합니다.
근거 문서: 클라우드 `studio/projects/soulchange-ep05/02_기획/대본_v2.md`(3절 컷 표, 8절 프롬프트). 프롬프트는 그 문서와 글자 하나까지 같습니다.

## 0. 먼저 읽을 것
- `C:\Users\경남교육청\youtube-ops\series\_soulchange_kit\소울체인지_제작규칙.md`
- 같은 폴더 `캐릭터_음성_설정.md`

## 1. 할 일
- 도구: **Dreamina Seedance 2.5**(사장님 계정, 480P) 3컷 / **Kling**(사장님 계정) 4컷
- 컷 수: 7개, 컷당 5초, 세로 9:16, 소리 끔(배경음 금지)
- 순서와 일정: Dreamina는 하루 무료 120 = 하루 1개(85)입니다. **1일차 K12b → 2일차 P0 → 3일차 C2.** Kling 4컷은 언제든 하되 **P1b는 P1이 통과한 뒤** P1의 마지막 프레임으로 만듭니다.
- 화면에서 실제로 쓰는 길이는 컷마다 다릅니다(아래 "쓰는 구간"). 쓰는 구간 안에서 확인 기준을 지키면 됩니다.

## 2. 참조 이미지 준비 (먼저 한 번만) — 사람 없는 부분만 잘라 쓰기 (검수 P1-5)

키트 배경 그림 두 장에는 주인공이 크게 들어 있습니다(`backgrounds\교무실_still_office.png` 가운데에 담임, `backgrounds\교실_still_class_B.png`는 지우 얼굴 클로즈업). 그대로 넣으면 엑스트라·손 컷에 담임·지우 얼굴이 나옵니다. **원본은 고치지 말고** 잘라서 새 파일로 저장합니다.

| 만들 파일 | 원본 | 자를 영역(왼쪽 위 x,y → 오른쪽 아래 x,y, 원본 1080×1916 기준) | 처리 |
|---|---|---|---|
| `C:\Users\경남교육청\youtube-ops\series\_soulchange_kit\episodes\ep5\refs\office_nopeople.png` | `backgrounds\교무실_still_office.png` | (790, 440) → (1080, 1010): 오른쪽 책상·책·스탠드·컵만 있는 부분 | 잘라서 **2배로 키워** 저장(580×1140). 자른 그림 왼쪽 끝에 담임 손·폰이 조금이라도 보이면 x를 더 오른쪽(820)으로 |
| (만들지 않음) 교실 | `backgrounds\교실_still_class_B.png`, 3화 `c3L.mp4`, 4화 `m1.mp4` | 사람 없는 부분이 너무 작음(300px 미만) | 교실 손 컷(P1)은 **배경 참조 없이** 글로만 생성. P1b는 P1 결과의 마지막 프레임 사용 |

- 잘라 만든 그림을 열어 **사람(얼굴·손·몸)이 하나도 없는지** 눈으로 확인하고 쓰세요.
- 주인공이 나오는 컷(K12b 담임, P0·C2 지우)은 그 인물의 캐릭터 그림을 넣습니다. 이때도 **다른 사람이 든 배경 그림은 넣지 않습니다**(친구가 지우 얼굴로 나오는 것을 막기 위해 C2에는 `지우_refS.png` 하나만).

## 3. 컷별 지시

공통 머리말(모든 프롬프트 맨 앞, 글자 그대로 — 아래 프롬프트 첫 줄에 이미 들어 있음):
"Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI."

| 순서 | 컷(대본 K번호) | 도구 | 첨부할 참조 이미지(키트 경로) | 쓰는 구간 | 저장 파일명 |
|---|---|---|---|---|---|
| 1일차 | **K12b** 담임 몸 "헉" 반응 | Dreamina | ① `characters\담임_refT.png` ② `characters\담임_클로즈업_still_A_cu.png` ③ `episodes\ep5\refs\office_nopeople.png` | 0–3.5초 | `episodes\ep5\clips\K12b.mp4` |
| 2일차 | **P0** (K2) 교실 뒷모습 | Dreamina | ① `characters\지우_refS.png` | 0–2.8초 | `episodes\ep5\clips\K02_P0.mp4` |
| 3일차 | **C2** (K4) 친구 등 + 헛기침 | Dreamina | ① `characters\지우_refS.png` | 0–5초 전부 | `episodes\ep5\clips\K04_C2.mp4` |
| Kling | **P1** (K5) 친구 손 + 폰 | Kling 글→영상 | 없음 | 0–5초 전부 | `episodes\ep5\clips\K05_P1.mp4` |
| Kling(P1 다음) | **P1b** (K6b) 손가락 콕콕 | Kling 이미지→영상 | `K05_P1.mp4`의 **마지막 프레임**을 PNG로 뽑아 첫 프레임으로 (`episodes\ep5\refs\P1_last.png`로 저장) | 0–2.5초 | `episodes\ep5\clips\K06b_P1b.mp4` |
| Kling | **P2** (K8) 교감 손 + 서류철 | Kling | ① `episodes\ep5\refs\office_nopeople.png` | 0–5초 전부 | `episodes\ep5\clips\K08_P2.mp4` |
| Kling | **P3** (K10) 선생님들 곁눈질 | Kling | ① `episodes\ep5\refs\office_nopeople.png` | 0–4.6초 | `episodes\ep5\clips\K10_P3.mp4` |

Kling이 막히면(한도·로그인) 그 컷은 Dreamina 무료로 하루 1개씩 이어서 만들고 그 사실을 보고합니다.

### K12b — Dreamina 5초 (끝 장면: 교감 말을 듣고 "헉" → 손으로 입 막기, 입은 끝까지 다묾)
```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
Subject: the middle-aged Korean male teacher from the reference image (graying hair, navy cardigan, white shirt, striped tie, eyeglass cord) stands beside his desk in a teachers' office, close-up, three-quarter view; the gray suit shoulder of the vice principal is blurred in the left foreground.
Action 1 (0-1.8s): his eyes go wide and his eyebrows shoot up, and a sharp gasp lifts his shoulders.
Action 2 (1.8-5s): he slaps one hand over his own mouth and his eyes dart sideways toward the foreground shoulder.
Mouth stays closed, no speaking.
Lighting: daylight through blinds, cool side light.
Mood: shocked, comic.
Camera: over-the-shoulder close-up past the blurred foreground shoulder, eye level, quick small push-in on the gasp. No one looks at the camera.
```

### P0 (K2) — Dreamina 5초 (교실 뒷모습, 팔꿈치 넓게 퍼질러 앉기 → 머리 벅벅)
```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
Subject: the Korean high school girl from the reference image (shoulder-length brown hair, ribbon hair pin on the left side, navy blazer school uniform), seen from behind and slightly above, sitting on a chair at a student desk in the back row of a Korean high school classroom during break time; other students chat in the blurred background. She sprawls on the chair like a worn-out middle-aged man, slumped low, both elbows planted wide apart on her knees; the chair back and her own back fill the lower part of the frame.
Action 1 (0-1.6s): she sinks even lower into the chair and lets her head hang, her shoulders rising and falling with a long, heavy sigh.
Action 2 (1.6-5s): she rakes both hands roughly through the back of her hair, scratching her head hard in frustration.
Lighting: bright daylight from the classroom windows on the left, soft fill.
Mood: defeated, comic.
Camera: medium shot from behind, framed from the top of her head down to the chair back, slight high angle, slow push-in. Her face is not visible. No one looks at the camera. No hair flipping, no head tilting, no cute or pretty poses.
```

### C2 (K4) — Dreamina 5초 (친구 둘은 등만, 지우 몸은 헛기침·꾸벅, 입 다묾)
```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
Subject: in a Korean high school classroom during break time, two other high school girls in the same navy blazer uniform stand in the foreground seen from behind, out of focus; one has a high ponytail, the other has short bob-cut black hair; one of them leans a hand on the desk; their faces are not visible. Between them, the girl from the reference image (shoulder-length brown hair, ribbon hair pin on the left side) sits at her desk, framed from the chest up, the desk edge hiding everything below her chest, looking up at them. Her body language is that of a timid middle-aged man: shoulders hunched, slightly bowing at the waist.
Action 1 (0-1.6s): she blinks and looks up from one girl to the other.
Action 2 (1.6-5s): she clears her throat with a fist held to her mouth, then gives small, quick, apologetic nods.
Mouth stays closed, no speaking.
Lighting: daylight from the classroom windows, soft fill.
Mood: awkward, comic.
Camera: over-the-shoulder shot between the two blurred girls, chest-up on the seated girl, eye level. No one looks at the camera. No hair flipping, no head tilting, no cute or pretty poses.
```

### P1 (K5) — Kling 5초 (손·소매·어깨만, 얼굴 없음. 2.4초 뒤 폰 화면이 카메라 쪽 — 나중에 연락처 카드를 합성함)
```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
Subject: a close shot beside a student desk in a Korean high school classroom during break time. Only the hands, navy blazer sleeves and shoulders of two high school girls are in frame; their faces are outside the frame. One girl's arm rests around the shoulder of a seated student in a navy blazer at the right edge of the frame, who is visible only from the shoulder down; the other girl holds a smartphone with a plain, evenly lit blank white screen.
Action 1 (0-2.4s): the arm pulls the seated student in by the shoulder, and the seated student hunches her shoulders and presses both hands together on the desk like a nervous middle-aged man.
Action 2 (2.4-5s): the other girl holds the smartphone out toward the seated student with the blank screen facing the camera, giving it a small, playful shake.
Lighting: bright daylight from the classroom windows.
Mood: mischievous, playful.
Camera: close-up at desk height, slight handheld movement. No faces visible. No one looks at the camera.
```

### P1b (K6b) — Kling 5초, P1 마지막 프레임에서 이어서 (0.15–2.5초 동안 폰 화면이 카메라 쪽 — 빨간 도장 합성)
```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
Subject: the same close shot beside a student desk in a Korean high school classroom as in the reference frame. Only hands, navy blazer sleeves and shoulders are in frame; no faces. A high school girl holds a smartphone with a plain, evenly lit blank white screen facing the camera; another girl's arm rests around the shoulder of the seated student at the right edge of the frame.
Action 1 (0-1.2s): the seated student's hand shoots out and jabs an index finger at the phone screen twice, like a scolding middle-aged teacher, while the phone stays where it is.
Action 2 (1.2-5s): the arm around the seated student's shoulder slowly slides away, and the hand holding the phone slowly lowers it.
Lighting: bright daylight from the classroom windows.
Mood: busted, awkward, comic.
Camera: close-up at desk height, slight handheld movement. No faces visible. No one looks at the camera.
```

### P2 (K8) — Kling 5초 (교감 손만)
```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
Subject: a close-up of an older man's hand in a gray suit sleeve with a white shirt cuff, resting on a teacher's wooden desk in a Korean school teachers' office, next to a closed plain beige document folder with no writing on it. No face is visible.
Action 1 (0-1.8s): his index finger taps slowly and deliberately on the folder.
Action 2 (1.8-5s): his hand slides the folder a few centimeters toward the edge of the desk.
Lighting: soft daylight through window blinds, slanted stripes of light across the desk.
Mood: quiet pressure, menace.
Camera: close-up, slight high angle, slow push-in on the hand. No one looks at the camera.
```

### P3 (K10) — Kling 5초 (앞쪽 흐린 담임 뒤통수 + 선생님 3명, 모두 입 다묾)
```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
Subject: a medium-wide view of a Korean school teachers' office in the daytime, desks with stacked papers and monitors. In the blurred right foreground, the graying hair, back and navy cardigan shoulder of a seated middle-aged man are visible; his face is not visible. Beyond him, three other teachers in their thirties to fifties, in cardigans and shirts, sit at their desks.
Action 1 (0-2.5s): one after another, the three teachers glance sideways over their monitors toward the man in the foreground.
Action 2 (2.5-5s): one female teacher covers her mouth with her hand and leans toward the teacher next to her.
All the teachers' mouths stay closed, no speaking.
Lighting: soft daylight through window blinds, neutral fluorescent fill.
Mood: tension spreading through the room.
Camera: medium-wide over the foreground man's shoulder, eye level, slow lateral drift. No one looks at the camera.
```

## 4. 확인 기준 (생성 직후 직접 보고, 어긋나면 한 번만 다시 생성)

모든 컷 공통
- **아무도 카메라를 보지 않는가**(눈이 렌즈를 향하는 순간이 한 번이라도 있으면 불합격).
- 화면에 글자가 생기지 않았는가(폰·서류철 화면은 글자 없이 하얗거나 비어 있어야 함).
- 쓰는 구간 안에서 화면이 멈춰 보이지 않는가(사람·카메라가 계속 조금씩 움직임).
- 얼굴이 보이는 컷은 얼굴·머리·옷이 참조 그림과 같은가.

컷별
| 컷 | 꼭 볼 것 |
|---|---|
| K12b | 담임 얼굴·희끗한 머리·남색 카디건·넥타이·안경 줄 유지. 0–1.8초 눈 휘둥그레 + 숨 들이켜 어깨 들썩, 그 뒤 **손바닥으로 입을 막음**. **입이 말하듯 움직이면 불합격**(이 컷 위에 교감 화면 밖 대사와 지우 속마음이 얹힘). 웃거나 장난스러운 표정이면 불합격 |
| P0 | **얼굴이 안 보이는 뒷모습**, 프레임은 머리~의자 등받이. 팔꿈치가 양옆으로 넓게 벌어져 아저씨처럼 퍼질러 앉은 몸짓이 뒤에서 읽힘. **치마·다리·하반신이 화면에 보이면 불합격(품위).** 머리를 우아하게 넘기거나 고개를 갸웃하면 불합격 |
| C2 | 친구 두 명은 **등과 뒷머리만**(높은 포니테일 / 짧은 단발), 얼굴이 생기면 불합격. 지우 몸은 가슴 위 프레임(책상이 아래를 가림), 주먹 헛기침 + 꾸벅꾸벅, **입 다묾**. 예쁜 포즈·머리 넘기기·고개 갸웃이면 불합격 |
| P1 | **얼굴 0개.** 앉은 학생은 어깨 아래만, 어깨 움츠리고 두 손 모음. 2.4초 뒤 폰 화면이 카메라 쪽으로 2초 넘게 보임(흔드는 폭이 작아야 합성 가능) |
| P1b | P1과 이어져 보임(같은 손·소매·폰). **얼굴 0개.** 손가락으로 폰 화면 콕콕(0–1.2초) 동안 폰이 크게 움직이지 않음 |
| P2 | 회색 소매·흰 셔츠 소매 끝, **얼굴 0개**, 서류철에 글자 없음. 톡톡 → 슥 밀기 |
| P3 | 앞쪽 오른쪽 흐린 뒤통수·어깨(얼굴 안 보임), 선생님 3명 **모두 입 다묾**(소곤대는 사람도 손으로 입을 가림). **담임·지우·교감 얼굴이 엑스트라로 나오면 불합격** |

- 2번 다시 해도 안 되면 멈추고 그 사실과 원인 추측을 보고합니다.

## 5. 결과 올리기
- 저장: `C:\Users\경남교육청\youtube-ops\series\_soulchange_kit\episodes\ep5\clips\` (잘라 만든 참조 그림은 `episodes\ep5\refs\`)
- 쓴 크레딧, 시도 횟수, 첨부한 참조, 실제 사용 프롬프트, 확인 기준 통과 여부를 `episodes\ep5\생성로그.md`에 적기(4화 `episodes\ep4\생성로그.md`와 같은 표 형식)
- `git add series/_soulchange_kit/episodes/ep5 && git commit -m "5화 PC 컷" && git push` (100MB 넘는 파일은 빼고 보고)
- 보고에 넣을 것: 만든 컷 목록, 다시 뽑은 컷과 이유, 남은 Dreamina·Kling 크레딧, 못 만든 컷
