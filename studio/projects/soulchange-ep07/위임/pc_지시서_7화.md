# 외부 AI 작업 지시서 — 소울체인지 7화 PC 쪽 컷 6개 (Kling 4 · Dreamina 2)

이 지시서는 클라우드 스튜디오(편집장)가 PC 쪽 AI에게 넘기는 작업입니다. 받은 AI는 아래만 하고, 결과를 지정한 위치에 올린 뒤 보고합니다.

> ## ★ 2026-10-27 바뀐 일정 (이 상자가 아래 내용보다 우선)
> - **7화 공개는 11/3(화) 18:00**으로 당겨졌습니다(사장님 정정 2026-10-27). 아래 본문의 "공개 11/6"과 "마감 11/3"은 옛 일정입니다.
> - **K3·K6은 끝났습니다**(`episodes\ep7\clips\K03.mp4`, `K06.mp4`).
> - **남은 4컷(K1·K2·K7·K10)은 Kling이 아니라 Dreamina Seedance 2.5(480P, 5초, 소리 끔)로 하루 1개씩 만듭니다**(사장님 결정 2026-10-27 "PC 드리미나 하루 1개").
>
>   | 날짜 | 컷 | 참조 | 저장 |
>   |---|---|---|---|
>   | 10/28(화) | **K1** 손바닥 '탁' + 가방 속 향수병 | `episodes\ep5\refs\office_nopeople.png` + `episodes\ep6\refs\K02_last.png` | `episodes\ep7\clips\K01.mp4` + 마지막 프레임 `episodes\ep7\refs\K01_last.png` |
>   | 10/29(수) | **K2** 손가락 콕 → 톡톡 | `episodes\ep7\refs\K01_last.png`(겉모습만) | `episodes\ep7\clips\K02.mp4` |
>   | 10/30(목) | **K7** 가방끈 비틀기 → 툭 | 〃 | `episodes\ep7\clips\K07.mp4` |
>   | 10/31(금) | **K10** 가방 낚아채고 일어남 | 〃 | `episodes\ep7\clips\K10.mp4` |
>
> - 프롬프트는 아래 3절의 K1·K2·K7·K10 글을 그대로 씁니다. **K1만 Dreamina 5초에 맞춰 Action 2를 "(3-5s)"로 바꿉니다**(10초 → 5초, 편집에서는 0–5초 전부 씀).
> - 하루가 밀리면 그대로 하루씩 미루되, **11/1(일)까지 4컷이 다 올라와야** 11/2(월) 편집으로 11/3에 맞출 수 있습니다. 밀리면 바로 보고합니다.
> - 확인 기준(4절)은 그대로입니다. 다시 뽑기는 컷마다 한 번까지 하고, 그래도 안 되면 멈추고 보고합니다.
근거 문서: 클라우드 `studio/projects/soulchange-ep07/02_기획/대본_v4.md` **5-2절**(연출 다양성 v4.4, 2026-10-26). 아래 프롬프트는 그 절과 글자 하나까지 같습니다. 5절·`대본_v3.md`의 옛 프롬프트는 쓰지 않습니다.

- **마감: 11/3(화)까지 6컷 전부.** (7화 공개 11/6(금) 18:00)
- Higgsfield 컷(K4·K12)은 클라우드에서 만듭니다(K12 완료, K4 진행 중). 재사용 컷(K5·R2)과 코드 컷(K0·K8·K11·K13)은 클라우드 편집에서 처리합니다. PC 쪽은 아래 6컷만 만듭니다.

## 0. 먼저 읽을 것
- `C:\Users\경남교육청\youtube-ops\series\_soulchange_kit\소울체인지_제작규칙.md`
- 같은 폴더 `캐릭터_음성_설정.md`
- 6화 지시서 `projects\soulchange-ep06\위임\pc_지시서_6화.md`(같은 규칙, 같은 확인 방법)

## 1. 할 일과 순서 (앞 컷에 기대는 컷이 있음)
- 도구: **Kling**(사장님 계정) 4컷 / **Dreamina Seedance 2.5**(사장님 계정, 480P) 2컷. 세로 9:16, 소리 끔.
- **기다려야 하는 것**
  1. **K1은 6화 K2가 끝난 뒤** 만듭니다. 6화 K2의 마지막 프레임 `episodes\ep6\refs\K02_last.png`(향수병 모양)를 참조로 넣어야 7화 어머니 가방 속 향수병이 6화와 같은 병이 됩니다.
  2. **K2·K7·K10은 K1이 통과한 뒤** 만듭니다. K1 마지막 프레임을 `episodes\ep7\refs\K01_last.png`로 뽑아 **겉모습 참조**(금반지·손톱·베이지 트렌치 소매·가방)로 넣습니다. **첫 프레임으로 쓰지 않습니다** — 이번 화부터 어머니 손 네 컷은 앵글을 컷마다 바꿉니다(탁자 높이 → 바로 위 → 옆 익스트림 클로즈업 → 바닥 높이). Kling 이미지→영상이 첫 프레임 구도를 그대로 따라가면, 참조(Elements) 기능으로 넣거나 글→영상으로 만들고 같은 반지·소매가 나오는지 눈으로 맞춥니다.
  3. **K6은 K3가 통과한 뒤** 만듭니다(K3 마지막 프레임 `episodes\ep7\refs\K03_last.png`가 K6 참조 ③).
- **Dreamina 하루 1개:** 10/27 = 6화 K8 → **10/28 = 7화 K3 → 10/29 = 7화 K6.** 하루가 밀리면 그대로 하루씩 미루고 보고합니다(11/3 안).
- 촬영 순서(권장): 6화 K2 끝나면 → K1 → K2 → K7 → K10 (Kling) / K3(10/28) → K6(10/29) (Dreamina).
- 이번 화부터 **장면·앵글·카메라를 다채롭게**(사장님 결정 2026-10-26). 프롬프트의 Camera·Lighting 줄(크래시 줌·탑·아크·휩 다운·바닥 로우·형광등 깜빡·역광)이 결과에 실제로 보여야 합니다.

## 2. 참조 이미지
| 쓸 그림 | 경로(키트 `C:\Users\경남교육청\youtube-ops\series\_soulchange_kit\` 아래) | 쓰는 컷 |
|---|---|---|
| 사람 없는 교무실(상담실 분위기용) | `episodes\ep5\refs\office_nopeople.png` | K1, K3 |
| 6화 K2 마지막 프레임(향수병) | `episodes\ep6\refs\K02_last.png` | K1 |
| 7화 K1 마지막 프레임(어머니 손·가방) | `episodes\ep7\refs\K01_last.png` (K1 뒤 직접 뽑기) | K2, K7, K10 |
| 담임 | `characters\담임_refT.png` | K3, K6 |
| 담임 클로즈업 | `characters\담임_클로즈업_still_A_cu.png` | K3, K6 |
| 7화 K3 마지막 프레임 | `episodes\ep7\refs\K03_last.png` (K3 뒤 직접 뽑기) | K6 |

## 3. 컷별 지시

공통 머리말(모든 프롬프트 맨 앞, 글자 그대로 — 아래 프롬프트 첫 줄에 이미 들어 있음):
"Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI."

| 순서 | 컷 | 도구 · 생성 길이 | 첨부할 참조 | 쓰는 구간 | 저장 파일명 |
|---|---|---|---|---|---|
| 1 (6화 K2 뒤) | **K1** 어머니 손 '탁' + 가방 속 향수병 | Kling 10초 | `episodes\ep5\refs\office_nopeople.png` + `episodes\ep6\refs\K02_last.png` | 0–6.8초 | `episodes\ep7\clips\K01.mp4` (+ `episodes\ep7\refs\K01_last.png`) |
| 2 | **K2** 손가락 콕(인서트, 바로 위) | Kling 5초 | `episodes\ep7\refs\K01_last.png`(겉모습만) | 0–3.6초 | `episodes\ep7\clips\K02.mp4` |
| 3 | **K7** 가방끈 비틀기 → 툭(인서트) | Kling 5초 | `episodes\ep7\refs\K01_last.png`(겉모습만) | 0–4.6초 | `episodes\ep7\clips\K07.mp4` |
| 4 | **K10** 가방 낚아채고 일어남(인서트, 구두·의자 다리) | Kling 5초 | `episodes\ep7\refs\K01_last.png`(겉모습만) | 0–5초 전부 | `episodes\ep7\clips\K10.mp4` |
| 10/28 | **K3** 담임 몸 굽신 끄덕 → 탁자 밑 엄지 타자 | Dreamina 5초 | ① 담임_refT ② 담임_클로즈업 ③ office_nopeople | 0–2.5초(K3a) + 2.5–5초(K3b) | `episodes\ep7\clips\K03.mp4` (+ `episodes\ep7\refs\K03_last.png`) |
| 10/29 | **K6** 킁킁 → 손끝으로 입 → 기침·굽신 칭찬 | Dreamina 5초 | ① 담임_refT ② 담임_클로즈업 ③ `episodes\ep7\refs\K03_last.png` | 0–5초 전부(편집 5.6초) | `episodes\ep7\clips\K06.mp4` |

Kling이 막히면(한도·로그인) 그 컷은 Dreamina로 하루 1개씩 이어서 만들고 그 사실을 보고합니다.

### K1 — Kling 10초 (쓰는 구간 0–6.8)
```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
Subject: a small table in a small Korean school counseling room. Close shot of the tabletop: a woman's hands with neatly manicured nails and a gold ring rest on a structured leather handbag with no logo; a small round glass perfume bottle with a gold cap peeks out of the open top of the bag. Across the table, a man's navy cardigan sleeve and a hand holding a pen over a notebook are blurred at the edge. No faces.
Action 1 (0-3s): the woman's right hand slaps the table flat once, firmly.
Action 2 (3-10s): she grips the handbag strap tightly with both hands and leans forward, the bag sliding a little toward the man, her fingers tapping the strap restlessly.
Lighting: cool fluorescent light that flickers once at the slap, window light from behind the bag making the perfume bottle glint.
Mood: confrontational, tense.
Camera: close shot at table height, a crash zoom in on the slap, then a slow push-in toward the bag. No one looks at the camera.
```

### K2 — Kling 5초 (인서트, 쓰는 구간 0–3.6)
```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
Subject: the small table in a school counseling room seen from directly above: a woman's manicured hands with a gold ring beside a leather handbag with no logo; a man's navy cardigan sleeve and an open notebook lie across the table. No faces.
Action 1 (0-2.5s): the woman points her index finger sharply across the table toward the man's sleeve.
Action 2 (2.5-5s): she lowers the hand and taps her fingertips on the table several times.
Lighting: cool fluorescent light from above, hard little shadows of the fingers on the table.
Mood: accusing, cold.
Camera: top-down overhead shot, slowly rotating and pushing in toward the pointing finger. No one looks at the camera.
```

### K7 — Kling 5초 (인서트, 쓰는 구간 0–4.6)
```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
Subject: an extreme close-up from the side of a woman's manicured hands with a gold ring gripping the strap of a leather handbag with no logo on the small counseling-room table; a beige trench coat cuff. No faces.
Action 1 (0-2.5s): her hands twist the strap tightly, knuckles whitening.
Action 2 (2.5-5s): she drops the bag onto the table with a flat thump and her fingers press down on it, knuckles flexing.
Lighting: hard side light from the window, deep shadows between the fingers.
Mood: bitter, sharp.
Camera: extreme close-up from the side at table height, handheld, a quick whip down following the bag as it drops. No one looks at the camera.
```

### K10 — Kling 5초 (인서트, 쓰는 구간 전부)
```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
Subject: a low view near the floor of the small counseling room: chair legs, the hem of a beige trench coat and a woman's low-heeled black shoes beside the table; above, a woman's manicured hand with a gold ring rests on a leather handbag with no logo at the table edge. No faces.
Action 1 (0-2s): her hand snatches up the handbag by its handle.
Action 2 (2-5s): she rises from the chair, the chair sliding back, the hem of her coat sweeping across the frame as her shoes step away toward the door.
Lighting: cool fluorescent light, a bright spill of hallway light from the door side.
Mood: cold, abrupt.
Camera: low angle at floor height, tilting up following the bag as she rises. No one looks at the camera.
```

### K3 — Dreamina 5초 (10/28, K3a 0–2.5 + K3b 2.5–5)
```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
Subject: the middle-aged Korean male teacher from the reference image (graying hair, navy cardigan, white shirt, striped tie, eyeglass cord) sits at a small table in a school counseling room, three-quarter view, chest up; in the left foreground the blurred back of a woman's head with dark wavy hair and a beige trench coat shoulder.
Action 1 (0-2.5s): with both hands clasped on the table and a stiff, wide smile, he nods quickly several times and says a few eager words, mouth moving with natural lip movement.
Action 2 (2.5-5s): his smile drops and his eyes go wide; he slides a smartphone under the edge of the table and types very fast with both thumbs, mouth stays closed, no speaking.
Lighting: window light from behind him rim-lighting his gray hair, cool fluorescent fill on his face.
Mood: nervously agreeable, then shocked.
Camera: over the woman's shoulder from a slightly high angle, a slow arc to the right during Action 1, then a quick tilt down toward the phone under the table edge. No one looks at the camera.
```

### K6 — Dreamina 5초 (10/29, 쓰는 구간 전부 — 편집 5.6초)
```
Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI.
Subject: the middle-aged Korean male teacher from the reference image (graying hair, navy cardigan, white shirt, striped tie, eyeglass cord) sits at the small counseling-room table, close-up from the chest up, three-quarter view; a beige coat shoulder leans in, blurred, at the left edge.
Action 1 (0-2s): he sniffs the air twice, his eyes going round, and his fingertips fly up to cover his mouth as a couple of muffled words slip out, like a surprised teenage girl.
Action 2 (2-5s): he rubs his throat and coughs several times into his fist, a bead of sweat on his forehead, then gives a small bow of the head with a stiff polite smile and stammers a short sentence, mouth moving with natural lip movement.
Lighting: the fluorescent light above flickers once as he sniffs, then steady cool light; soft window fill.
Mood: startled, then struggling and awkwardly flattering.
Camera: low-angle close-up past the blurred shoulder, a crash zoom in on the sniff, then light handheld movement. No one looks at the camera.
```

## 4. 확인 기준 (생성 직후 직접 보고, 어긋나면 한 번만 다시 생성)

모든 컷 공통
- **아무도 카메라를 보지 않는가**(눈이 렌즈를 향하는 순간이 한 번이라도 있으면 불합격).
- 화면에 글자·상표·로고가 생기지 않았는가(가방·향수병·폰에 로고 없음).
- 쓰는 구간 안에서 화면이 멈춰 보이지 않는가.
- **프롬프트의 카메라 무빙과 빛이 실제로 보이는가.** 카메라가 거의 고정이면 한 번 다시.

컷별
| 컷 | 꼭 볼 것 |
|---|---|
| K1 | **얼굴 0**(손·가방·맞은편 남색 소매만). 금반지·손톱. **가방 입구의 둥근 유리 향수병(금색 뚜껑)이 6화 K2의 병과 같은 모양**(가장 중요). 0–3초 손바닥 '탁'에 맞춰 화면이 확 다가감(크래시 줌), 형광등 한 번 깜빡은 있으면 좋음 |
| K2 | **바로 위에서 내려다본 탁자**(탑 앵글). 같은 금반지·손톱·소매. 검지로 맞은편 소매 콕 → 손끝 톡톡. 얼굴 0 |
| K7 | **옆에서 본 손마디 익스트림 클로즈업.** 가방끈 비틀기(손마디 하얘짐) → 가방 툭, 카메라가 가방을 따라 아래로 휙. 센 옆빛·짙은 그림자. 얼굴 0 |
| K10 | **바닥 높이에서 올려다봄:** 의자 다리, 트렌치 자락, 굽 낮은 검은 구두가 보임. 손이 가방을 낚아채고 일어서며 구두가 문 쪽으로 걸어 나감. 카메라가 위로 따라 올라감. 얼굴 0 |
| K3 | 담임 얼굴·희끗한 머리·남색 카디건·넥타이·안경 줄 유지. 0–2.5초 두 손 모으고 굳은 웃음으로 연신 끄덕이며 **말함**, 2.5초부터 웃음이 빠지고 탁자 밑에서 **두 엄지로 빠르게 타자, 입 다묾**. 뒤 창빛이 머리에 빛 테두리. 앞쪽 어머니 뒷머리·트렌치 어깨는 흐림(얼굴 0) |
| K6 | 같은 담임. 0–2초 코를 두 번 킁킁 → 눈이 동그래지며 **손끝으로 입을 가림**(여고생 몸짓). 2초 뒤 목을 문지르며 기침 여러 번, 이마 땀, 굳은 웃음으로 꾸벅하며 더듬더듬 말함. 아래에서 올려다본 클로즈업, 킁킁에 확 다가감. 손이 입을 안 가리면 1회 다시(목소리 섞임 입 맞춤 때문) |

- 2번 다시 해도 안 되면 멈추고 그 사실과 원인 추측을 보고합니다.

## 5. 결과 올리기
- 저장: `C:\Users\경남교육청\youtube-ops\series\_soulchange_kit\episodes\ep7\clips\` (마지막 프레임 PNG는 `episodes\ep7\refs\`)
- 쓴 크레딧, 시도 횟수, 첨부한 참조, 실제 사용 프롬프트, 확인 기준 통과 여부를 `episodes\ep7\생성로그.md`에 적기(6화와 같은 표 형식)
- `git add series/_soulchange_kit/episodes/ep7 && git commit -m "7화 PC 컷" && git push` (100MB 넘는 파일은 빼고 보고)
- 보고에 넣을 것: 만든 컷 목록, 다시 뽑은 컷과 이유, 남은 Dreamina·Kling 크레딧, 못 만든 컷, 향수병이 6화와 같아 보이는지 한 줄
