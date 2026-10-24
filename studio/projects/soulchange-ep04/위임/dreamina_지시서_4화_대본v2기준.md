# 외부 AI 작업 지시서 — 소울체인지 4화 새 컷 N1~N6

이 지시서는 클라우드 스튜디오(편집장)가 PC 쪽 AI에게 넘기는 작업입니다. 받은 AI는 아래만 하고, 결과를 지정한 위치에 올린 뒤 보고합니다.

- 근거 대본: 스튜디오 `projects/soulchange-ep04/02_기획/대본_v2.md` (2026-10-24, 사장님 결정 반영)
- 4화 공개: 10/30(금) 18:00. 컷은 **10/27(화)까지** 올려 주면 편집 일정(수 편집 → 목 예약)에 맞습니다.

## 0. 먼저 읽을 것
- `C:\Users\경남교육청\youtube-ops\series\_soulchange_kit\소울체인지_제작규칙.md`
- 같은 폴더 `캐릭터_음성_설정.md`
- (같은 장면 확인용) 이미 있는 4화 컷 `C:\Users\경남교육청\youtube-ops\series\_soulchange_kit\episodes\ep4\clips\m1.mp4`~`m4.mp4`, 3화 교실 컷 `episodes\ep3\clips\c3L.mp4`

## 1. 할 일
- 도구: **Dreamina Seedance 2.5 (사장님 계정)**. Higgsfield는 쓰지 않습니다.
- 컷 수: **6개**, 컷당 5초, 세로 9:16, **480P**(m1~m4·3화와 같음), 소리 끔(배경음 금지)
- 폰 화면은 빈 밝은 화면으로 둡니다. 문자 말풍선·자막은 편집에서 얹습니다.
- 인물: 담임 몸 컷 = 교무실(m1과 같은 창가 책상), 지우 몸 컷 = 교실 뒤 창가 사물함(3화 c3L과 같은 벽). 한 컷에 한 사람만 나옵니다.

## 2. 컷별 지시

참조 이미지 경로는 모두 `C:\Users\경남교육청\youtube-ops\series\_soulchange_kit\` 아래입니다. 첫째 이미지가 인물(필수), 둘째가 장소(Dreamina가 여러 장을 받으면 함께 첨부, 한 장만 받으면 인물만)입니다.

| 컷 | 첨부할 참조 이미지(키트 경로) | 프롬프트(그대로 붙여 넣기) | 저장 파일명 |
|---|---|---|---|
| N1 (10–15초) 담임 몸, 소리 없이 킥킥 | `characters\담임_refT.png`, `backgrounds\교무실_still_office.png` | 아래 N1 | `episodes\ep4\clips\N1.mp4` |
| N2 (25–30초) 담임 몸, 손 흔들고 문자 받음 | `characters\담임_클로즈업_still_A_cu.png`, `backgrounds\교무실_still_office.png` | 아래 N2 | `episodes\ep4\clips\N2.mp4` |
| N3 (30–35초) 담임 몸 어깨 너머, 화면 확대 | `characters\담임_refT.png`, `backgrounds\교무실_still_office.png` | 아래 N3 | `episodes\ep4\clips\N3.mp4` |
| N4 (35–40초) 지우 몸, 안경 올리고 한숨 | `characters\지우_refS.png`, `backgrounds\교실_still_class_B.png` | 아래 N4 | `episodes\ep4\clips\N4.mp4` |
| N5 (40–45초) 담임 몸, 빠르게 입력하고 흘끗 | `characters\담임_refT.png`, `backgrounds\교무실_still_office.png` | 아래 N5 | `episodes\ep4\clips\N5.mp4` |
| N6 (45–49.5초) 지우 몸, 썼다 지웠다 | `characters\지우_refS.png`, `backgrounds\교실_still_class_B.png` | 아래 N6 | `episodes\ep4\clips\N6.mp4` |

공통 머리말(모든 프롬프트 맨 앞, 글자 그대로):
"Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI."

### N1
```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
High-angle three-quarter medium shot of the middle-aged male teacher at his staff-room desk by the window, chin propped on one hand, a phone with a blank bright screen held low in the other hand. His mouth stays closed, no speaking. He reads the phone while his shoulders shake in small silent giggles, then taps his fingertips lightly on his cheek in a playful, girlish rhythm. Continuous breathing, blinking and small shoulder motion; two blurred colleagues keep moving far behind. No one looks at the camera. Soft daylight from the window. Camera: slow gentle drift to the left with soft handheld breathing.
```

### N2
```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
Three-quarter side close-up of the middle-aged male teacher seated at his staff-room desk, phone in one hand. His mouth stays closed, no speaking. He gives a small, light wave toward someone walking away off-screen to his right, then the phone buzzes in his hand and he lowers his eyes to the screen, his eyebrows lifting slightly. Continuous breathing and blinking; blurred colleagues move in the background. No one looks at the camera. Soft daylight. Camera: slow creeping push-in.
```

### N3
```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
Over-the-shoulder shot from behind the middle-aged male teacher's left shoulder at his staff-room desk; the phone in his hands fills the lower third of the frame, its screen blank and bright. His mouth stays closed, no speaking. He spreads two fingers on the screen to zoom in, then tilts his head and leans his face closer to the phone. Continuous small hand motion and breathing. No one looks at the camera. Camera: slight slow push toward the phone, subtle handheld micro-movement.
```

### N4
```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
Side-profile medium shot of the high-school girl standing by the window-side lockers at the back of the classroom during a break, phone at chest height. Her mouth stays closed, no speaking. She reads the phone and pushes invisible glasses up her nose with one finger, then lets out a long silent sigh, her shoulders rising and slowly dropping. Continuous breathing; a few blurred students move far in the background. No one looks at the camera. Afternoon window light. Camera: slow lateral drift keeping her in profile.
```

### N5
```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
Low-angle side-profile medium shot of the middle-aged male teacher leaning forward at his staff-room desk, elbows on the desk, phone in both hands with a blank bright screen. His mouth stays closed, no speaking. He types quickly with both thumbs, then glances over his shoulder toward the far end of the office and turns back to the phone. Continuous breathing and finger motion; blurred colleagues move in the background. No one looks at the camera. Camera: gentle floating drift upward.
```

### N6
```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
Tight three-quarter close-up of the high-school girl at the back of the classroom, the edge of her phone at the bottom of the frame. Her mouth stays closed, no speaking, lips pressed together. Her thumb types and deletes in short bursts, then she slowly lifts her eyes toward the front of the classroom, off to the left side of the frame. Continuous breathing and blinking. No one looks at the camera. Soft afternoon light. Camera: slow creeping push-in toward her face.
```

## 3. 확인 기준 (생성 직후 직접 보고, 어긋나면 한 번만 다시 생성)
- 얼굴·머리·옷이 참조 이미지와 같은가
  - 담임 몸: 희끗한 머리, 남색 카디건, 흰 셔츠, 줄무늬 넥타이, **목에 건 안경 줄**(m1~m4와 같음)
  - 지우 몸: 어깨 길이 갈색 머리, **왼쪽 리본 핀**, 남색 블레이저, 회색 체크 치마
- 아무도 카메라를 보지 않는가, **6컷 모두 입이 움직이지 않는가**(모두 속마음·DM 컷)
- 화면에 글자가 생기지 않았는가(폰 화면에 글자·앱 화면이 생기면 다시 생성)
- 행동이 2개를 넘지 않고, 5초 내내 무언가 움직이는가(정지처럼 보이는 구간이 1초 넘으면 다시 생성)
- 컷별 핵심 동작이 보이는가
  - N1: 어깨가 들썩이는 웃음(입은 다묾) / N2: 손 흔들기 → 폰 보기 / N3: 두 손가락 확대(손가락 모양이 뭉개지지 않는가) / N4: 없는 안경 올리기 → 한숨 / N5: 빠른 입력 → 어깨 너머 흘끗 / N6: 입술 다문 채 엄지 움직임 → 눈을 들어 화면 왼쪽 밖
- 교무실 컷(N1·N2·N3·N5)의 책상·창 방향이 m1과 크게 다르지 않은가
- 2번 다시 해도 안 되면 멈추고 그 사실과 원인 추측을 보고

## 4. 결과 올리기
- 저장: `C:\Users\경남교육청\youtube-ops\series\_soulchange_kit\episodes\ep4\clips\` (N1.mp4 ~ N6.mp4. 다시 뽑은 것은 덮어쓰지 말고 `N3_v2.mp4`처럼)
- 쓴 크레딧과 실제 사용 프롬프트를 `episodes\ep4\생성로그.md`에 적기 (컷, 시도 횟수, Dreamina 크레딧, 해상도, 참조 이미지, 확인 기준 통과 여부)
- `git add series/_soulchange_kit/episodes/ep4 && git commit -m "4화 컷" && git push` (100MB 넘는 파일은 빼고 보고)
