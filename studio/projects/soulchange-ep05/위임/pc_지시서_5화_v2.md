# 외부 AI 작업 지시서 v2 — 소울체인지 5화 PC 쪽 컷 (바뀐 것만)

v1(`pc_지시서_5화.md`)을 그대로 쓰되, **아래 두 컷만 바꿉니다.** 근거: 클라우드 `studio/projects/soulchange-ep05/02_기획/대본_v3.md`(맨 위 사장님 결정 메모가 우선).

## 0. 요약
| 컷 | v1 | v2 |
|---|---|---|
| K12b · P0 · C2 (Dreamina) | — | **그대로.** 순서 K12b → P0 → C2. 이미 만들었으면 다시 만들지 않음 |
| P1 · P2 (Kling) | — | **그대로.** 이미 만들었으면 다시 만들지 않음 |
| **P1b** (Kling, 대본 K6a) | 손가락 콕콕 + 빨간 도장 합성, 쓰는 구간 0–2.5초 | **주먹으로 책상 쾅쾅 두 번 → 친구 팔이 튕겨 나가고 폰이 빠짐.** 합성 없음. **쓰는 구간 0–5초 전부.** 아래 새 프롬프트. v1 P1b를 이미 만들었으면 버리고 다시 만듦 |
| **P3** (Kling, 대본 K10) | 선생님 3명 곁눈질 + 앞쪽 담임 뒤통수 | **앞쪽 담임 몸의 오른손이 검지로 천장 가리킴 → 손바닥 받쳐 들어 올림**(지우 대사 "지식이 높은 고지식하신 교감쌤께서…"의 손동작) + 선생님들 곁눈질. 아래 새 프롬프트. v1 P3를 이미 만들었으면 버리고 다시 만듦 |

- 클라우드에서 Higgsfield 컷 7개(A1·A2·A3·A4·A5a·C1·C3)는 모두 끝났습니다. PC 쪽 7컷이 오면 바로 편집합니다.
- 공개일: **11/1(일) 18:00.** PC 컷은 **10/29(목)까지** 올려 주세요(편집·블라인드 검수·Gemini 검수 시간).

## 1. P1b (대본 K6a) — Kling 이미지→영상 5초
- 첫 프레임: `K05_P1.mp4`의 **마지막 프레임**(`episodes\ep5\refs\P1_last.png`). P1이 통과한 뒤에 만듭니다.
- 저장: `episodes\ep5\clips\K06a_P1b.mp4` (v1의 `K06b_P1b.mp4` 이름은 쓰지 않음)
- 소리: 화면 밖으로 "으악…!"(0.2–1.6초), 쾅쾅(약 1.7·2.1초), "너네, 이런 짓까지 해?"(2.5–4.9초)가 얹힙니다.

```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
Subject: the same close shot beside a student desk in a Korean high school classroom as in the reference frame. Only hands, navy blazer sleeves and shoulders are in frame; no faces. A high school girl holds a smartphone near the desk; another girl's arm rests around the shoulder of the seated student at the right edge of the frame; the seated student's two hands rest on the desk.
Action 1 (0-1.6s): the seated student's hands clench into tight trembling fists on the desk and her shoulders hunch up.
Action 2 (1.6-5s): she slams both fists down on the desk twice, hard, like a furious middle-aged teacher; the desk jolts, the arm around her shoulder jerks away, and the hand holding the smartphone pulls it back out of the frame.
Lighting: bright daylight from the classroom windows.
Mood: explosive, busted, comic.
Camera: close-up at desk height, slight handheld movement, a small jolt of the camera on each fist slam. No faces visible. No one looks at the camera.
```

**확인 기준:** 얼굴 0개 / 주먹 두 번이 또렷이 보임 / P1과 같은 손·소매로 이어 보임 / 폰이 화면 밖으로 빠져도 됨 / 손가락 5개, 손 모양 자연스러움 / 아무도 카메라를 보지 않음.

## 2. P3 (대본 K10) — Kling 5초
- 참조: `episodes\ep5\refs\office_nopeople.png` (v1 2절에서 만든 사람 없는 교무실 그림)
- 저장: `episodes\ep5\clips\K10_P3.mp4`
- 소리: 지우(담임 몸) 대사 "하. 지식이 높은 고지식하신 교감쌤께서, 무섭기까지 하면 단가요?"가 화면 밖으로 얹힙니다. 앞쪽 남자의 얼굴은 보이지 않아야 합니다.

```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
Subject: a medium-wide view of a Korean school teachers' office in the daytime, desks with stacked papers and monitors. In the right foreground, seen from behind, the graying hair, back and navy cardigan shoulder of a seated middle-aged man are visible, his face not visible; his right hand and forearm are clearly in frame. Beyond him, three other teachers in their thirties to fifties, in cardigans and shirts, sit at their desks.
Action 1 (0-2s): the foreground man raises his right index finger high, pointing up toward the ceiling, while the three teachers glance sideways over their monitors toward him.
Action 2 (2-5s): he turns his hand palm-up and lifts it slowly as if presenting someone lofty, while one female teacher covers her mouth with her hand and leans toward the teacher next to her.
All the teachers' mouths stay closed, no speaking.
Lighting: soft daylight through window blinds, neutral fluorescent fill.
Mood: sarcastic, tension spreading through the room.
Camera: medium-wide over the foreground man's shoulder, eye level, slow lateral drift. No one looks at the camera.
```

**확인 기준:** 앞쪽 남자는 뒤통수·어깨·오른손만(얼굴 안 보임) / 오른손이 **검지 위 → 손바닥 들어 올림**으로 또렷이 / 선생님 3명 모두 입 다묾(소곤대는 사람도 손으로 입 가림) / 담임·지우·교감 얼굴이 엑스트라로 나오면 불합격 / 손가락 5개 / 아무도 카메라를 보지 않음.

## 3. 결과 올리기
v1 5절과 같습니다(`episodes\ep5\clips\`, `episodes\ep5\생성로그.md`, git push). 보고에 **P1b·P3를 v2 프롬프트로 만들었는지** 꼭 적어 주세요.
