> **v3 기준** (대본 `projects/soulchange-ep04/02_기획/대본_v3.md`, 2026-10-24). 대본 v2 기준 이전 지시서는 `dreamina_지시서_4화_대본v2기준.md`에 보관. **v2 지시서로는 생성하지 말 것**(N2·N4·N6 장면과 참조 이미지가 바뀜).

# 외부 AI 작업 지시서 — 소울체인지 4화 새 컷 N1~N6

이 지시서는 클라우드 스튜디오(편집장)가 PC 쪽 AI에게 넘기는 작업입니다. 받은 AI는 아래만 하고, 결과를 지정한 위치에 올린 뒤 보고합니다.

- 4화 공개: 10/30(금) 18:00. 컷은 **10/27(화)까지** 올려 주면 편집 일정(수 편집 → 목 예약)에 맞습니다.
- 생성은 편집장이 "진행"이라고 알릴 때 시작합니다(대본 v3 블라인드 재검수 대기 중일 수 있음).

## 0. 먼저 읽을 것
- `C:\Users\경남교육청\youtube-ops\series\_soulchange_kit\소울체인지_제작규칙.md`
- 같은 폴더 `캐릭터_음성_설정.md`

## 1. 할 일
- 도구: **Dreamina Seedance 2.5 (사장님 계정)**. Higgsfield는 쓰지 않습니다.
- 컷 수: **6개**, 컷당 5초, 세로 9:16, **480P**(m1~m4·3화와 같음), 소리 끔(배경음 금지)
- 한 컷에 한 사람만 나옵니다. 폰 화면은 빈 밝은 화면으로 둡니다(문자·단톡 말풍선과 자막은 편집에서 얹음).

### 1-1. 장소 참조 프레임 먼저 만들기 (생성 전에 한 번)
키트의 `backgrounds\교실_still_class_B.png`, `backgrounds\교무실_still_office.png`는 **쓰지 않습니다**(장면과 맞지 않음: 교실 이미지는 칠판 앞 클로즈업, 교무실 이미지는 여러 인물). 대신 이미 있는 클립에서 프레임 한 장씩 뽑습니다.

```
cd C:\Users\경남교육청\youtube-ops\series\_soulchange_kit\episodes
ffmpeg -ss 0.5 -i ep4\clips\m1.mp4 -frames:v 1 ep4\clips\ref_office_m1.png
ffmpeg -ss 3.0 -i ep3\clips\c3L.mp4 -frames:v 1 ep4\clips\ref_class_c3L.png
```
- `ref_office_m1.png` = 교무실 창가 책상의 담임 몸(m1 0.5초, 진지하게 폰 보는 얼굴)
- `ref_class_c3L.png` = 교실 뒤 창가 벽에 기대 폰 보는 지우 몸(3화 c3L 3초)
- ffmpeg가 없으면 영상 재생기에서 그 시점을 화면 캡처해도 됩니다. 두 파일은 커밋하지 않아도 됩니다.

## 2. 컷별 지시

참조 이미지 경로는 모두 `C:\Users\경남교육청\youtube-ops\series\_soulchange_kit\` 아래입니다. **첫째 = 인물(필수), 둘째 = 장소 프레임.** 장소 프레임에도 같은 인물이 들어 있어 얼굴이 흔들리지 않습니다. Dreamina가 한 장만 받으면 첫째만 넣습니다.

| 컷 | 대본 시간 | 첨부할 참조 이미지(키트 경로) | 프롬프트 | 저장 파일명 |
|---|---|---|---|---|
| N1 | 11.5–16.5 | ① `characters\담임_refT.png` ② `episodes\ep4\clips\ref_office_m1.png` | 아래 N1 | `episodes\ep4\clips\N1.mp4` |
| N2 | 26.5–31.5 | ① `characters\지우_refS.png` ② `episodes\ep4\clips\ref_class_c3L.png` | 아래 N2 | `episodes\ep4\clips\N2.mp4` |
| N3 | 31.5–36.5 | ① `characters\담임_refT.png` ② `episodes\ep4\clips\ref_office_m1.png` | 아래 N3 (실패 시 N3-B) | `episodes\ep4\clips\N3.mp4` |
| N4 | 36.5–41.5 | ① `characters\지우_refS.png` ② `episodes\ep4\clips\ref_class_c3L.png` | 아래 N4 | `episodes\ep4\clips\N4.mp4` |
| N5 | 41.5–46.5 | ① `characters\담임_refT.png` ② `episodes\ep4\clips\ref_office_m1.png` | 아래 N5 | `episodes\ep4\clips\N5.mp4` |
| N6 | 46.5–51.5 | ① `characters\지우_refS.png` ② `episodes\ep4\clips\ref_class_c3L.png` | 아래 N6 | `episodes\ep4\clips\N6.mp4` |

공통 머리말(모든 프롬프트 맨 앞, 글자 그대로):
"Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI."

### N1 — 교무실, 담임 몸, 웃음 참기
```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
High-angle three-quarter medium shot of the middle-aged male teacher at his staff-room desk by the window, chin propped on one hand, a phone with a blank bright screen held low in the other hand. His mouth stays closed, no speaking; lips stay pressed together. He reads the phone while his shoulders shake with small held-back giggles, then taps his fingertips lightly on his cheek in a playful, girlish rhythm. Continuous breathing, blinking and small shoulder motion; blurred colleagues keep moving far behind. No one looks at the camera. Soft daylight from the window. Camera: slow gentle drift to the left with soft handheld breathing.
```

### N2 — 교실 뒤 창가 벽, 지우 몸, 단톡 알림
```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
Side-profile medium shot of the high-school girl leaning against the window-side wall at the back of the classroom, phone held at chest height with a blank bright screen; empty desks and soft window light behind her. Her mouth stays closed, no speaking. The phone buzzes and she looks down at the screen, then brings the phone closer to her face and narrows her eyes. Continuous breathing and blinking; a few blurred students move far in the background. No one looks at the camera. Camera: slow lateral drift keeping her in profile.
```

### N3 — 교무실, 담임 몸 어깨 너머, 화면 확대
```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
Over-the-shoulder shot from behind the middle-aged male teacher's left shoulder at his staff-room desk by the window; the phone in his hands fills the lower third of the frame, its screen blank and bright. His mouth stays closed, no speaking. He spreads two fingers on the screen to zoom in, then tilts his head and leans his face closer to the phone. Continuous small hand motion and breathing. No one looks at the camera. Camera: slight slow push toward the phone, subtle handheld micro-movement.
```
**N3-B (N3가 두 번 다 손가락이 뭉개질 때만):** 위 프롬프트에서 "He spreads two fingers on the screen to zoom in, then tilts his head and leans his face closer to the phone." 문장을 아래로 바꿉니다.
```
He lifts the phone closer to his face with both hands, then tilts his head and squints at the screen.
```

### N4 — 교실 뒤 창가 벽, 지우 몸, 안경 올리고 빠르게 입력
```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
Low three-quarter front medium shot of the high-school girl leaning against the window-side wall at the back of the classroom, phone in both hands with a blank bright screen; empty desks and window light behind her. Her mouth stays closed, no speaking. While reading, she pushes invisible glasses up her nose with one finger, then types quickly with both thumbs. Continuous breathing and finger motion; blurred students move far in the background. No one looks at the camera. Camera: slow creeping push-in.
```

### N5 — 교무실, 담임 몸, 등 기대고 흘끗
```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
Low-angle side-profile medium shot of the middle-aged male teacher in his office chair at the staff-room desk by the window, phone in both hands with a blank bright screen. His mouth stays closed, no speaking. He leans back in the chair as he reads, his eyes widening, then glances over his shoulder toward the far end of the office and turns back to type quickly with both thumbs. Continuous breathing and finger motion; blurred colleagues move in the background. No one looks at the camera. Camera: gentle floating drift upward.
```

### N6 — 교실 뒤, 지우 몸, 엄지를 올렸다 뗐다 (마지막 컷)
```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
Tight three-quarter close-up of the high-school girl by the window-side wall at the back of the classroom, the edge of her phone at the bottom of the frame. Her mouth stays closed, no speaking, lips pressed together. Her thumb hovers over the screen, lowers toward it and lifts away again without pressing, then she slowly raises her eyes toward the front of the classroom, off to the left side of the frame. Continuous breathing and blinking. No one looks at the camera. Soft afternoon window light. Camera: slow creeping push-in toward her face.
```

## 3. 확인 기준 (생성 직후 직접 보고, 어긋나면 한 번만 다시 생성)
- 얼굴·머리·옷이 참조 이미지와 같은가
  - 담임 몸: 희끗한 머리, 남색 카디건, 흰 셔츠, 줄무늬 넥타이, **목에 건 안경 줄**(m1~m4와 같음)
  - 지우 몸: 어깨 길이 갈색 머리, **왼쪽 리본 핀**, 남색 블레이저, 회색 체크 치마
- **다른 인물의 얼굴이 주인공 자리에 들어오지 않았는가**(뒤쪽 흐린 사람은 괜찮음)
- 아무도 카메라를 보지 않는가. **6컷 모두 입이 움직이지 않는가**(모두 속마음·DM 컷)
- 화면과 폰에 글자·앱 화면·로고가 생기지 않았는가
- **종이·서류 같은 소품을 손에 들고 있지 않은가**(폰만)
- 교실 컷(N2·N4·N6)이 3화 c3L처럼 **창가 벽** 앞인가(사물함·칠판 앞이면 다시 생성)
- 교무실 컷(N1·N3·N5)의 책상·창 방향이 m1과 크게 다르지 않은가
- 행동이 2개를 넘지 않고, 5초 내내 무언가 움직이는가(정지처럼 보이는 구간이 1초 넘으면 다시 생성)
- 컷별 핵심 동작:
  - N1 어깨가 들썩이는 웃음(입은 다묾) · 볼 톡톡
  - N2 폰 울림 → 얼굴 가까이 당기며 눈 가늘게
  - N3 두 손가락 확대(손가락이 뭉개지면 N3-B)
  - N4 없는 안경 올리기 → 두 엄지 빠른 입력
  - N5 등 기대며 눈 커짐 → 어깨 너머 흘끗 → 입력
  - N6 엄지가 화면 위에서 내려갔다 올라감(누르지 않음) → 눈을 들어 화면 왼쪽 밖. **마지막 1초가 얼굴 표정으로 끝나는지**(편집에서 5초 전부 씀)
- 2번 다시 해도 안 되면 멈추고 그 사실과 원인 추측을 보고

## 4. 결과 올리기
- 저장: `C:\Users\경남교육청\youtube-ops\series\_soulchange_kit\episodes\ep4\clips\` (N1.mp4 ~ N6.mp4. 다시 뽑은 것은 덮어쓰지 말고 `N3_v2.mp4`처럼)
- 쓴 크레딧과 실제 사용 프롬프트를 `episodes\ep4\생성로그.md`에 적기 (컷, 시도 횟수, Dreamina 크레딧, 해상도, 첨부한 참조 이미지, 확인 기준 통과 여부)
- `git add series/_soulchange_kit/episodes/ep4 && git commit -m "4화 컷" && git push` (100MB 넘는 파일은 빼고 보고. 참조 프레임 png 두 장은 올리지 않아도 됨)
