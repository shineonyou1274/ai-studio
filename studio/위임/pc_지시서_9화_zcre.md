# PC 지시서 — 9화 컷을 zcre.co.kr에서 만들기 (2026-10-31)

받는 쪽: 사장님 맥에서 Aside 브라우저를 쓰는 AI
보내는 쪽: 클라우드 편집장(Claude Code) — 편집·자막·소리는 편집장이 한다.
근거: 사장님 2026-10-30 "어사이드 브라우저 이용해서 zcre.co.kr 들어가면 영상 뽑을 수 있어. 1000크레딧 있어" → 9화 컷은 zcre로.

## 0. 먼저 할 일 (생성 전에 보고)
1. 저장소 `shineonyou1274/ai-studio` 브랜치 `claude/eager-mccarthy-bcbh23`를 받는다.
2. zcre에서 쓸 수 있는 영상 모델과 기능을 확인해 `studio/projects/soulchange-ep09/04_생성물/zcre_확인.md`에 적는다:
   - 모델 이름(예: Seedance·Kling·Veo 등), 세로 9:16 되는지, 길이(5·10초 등), 해상도
   - **참조 이미지(인물 얼굴 고정) 몇 장까지**, **오디오 넣으면 입 맞추기(립싱크) 되는지**, 시작 프레임 지정 되는지
   - 컷 하나 값(크레딧)
3. 첫 컷 K1 하나만 만들어 올리고 사장님 확인을 받은 뒤 나머지를 만든다. 전체 예상 크레딧을 먼저 사장님께 말한다(1000 안).

## 1. 공통 규칙
- 세로 9:16, 소리 끔(생성 오디오 쓰지 않음 — 편집에서 녹음을 씀), 영상에 글자·자막·음악 없음.
- 참조 그림: `studio/series/요소_이미지/` — 담임 김병만 `sc_teacher.png`(+클로즈업 `sc_teacher_cu.png`), 지우 `sc_jiu.png`, 교감 `sc_vp_full.png`(가운데 인물), 최 쌤 `sc_choi.png`(뒷모습·옷), 현석 `sc_hood.png`(뒷모습만), 교실 `sc_classroom.png`, 교무실 `sc_office.png`, 벤치 `sc_bench.png`, 향수병 `sc_perfume.png`.
- 입 맞추기: 표의 "오디오"가 있는 컷은 zcre가 오디오 립싱크를 받으면 그 파일을 넣는다(`studio/projects/soulchange-ep09/04_생성물/voices/`). 안 받으면 오디오 없이 만들되, 말하는 동안 입이 자연스럽게 움직이게.
- 하지 말 것: 정지 유발어(still, freeze, static), 카메라를 보는 인물, 한 컷에 행동 3개 이상.
- 결과 파일: `studio/projects/soulchange-ep09/04_생성물/clips/K번호.mp4`, 다시 뽑으면 `K번호_v2.mp4`. 쓴 프롬프트·모델·크레딧은 `04_생성물/생성로그.md` 맨 아래에 표로.
- 다 올리면 커밋 "9화 컷 zcre" 후 푸시.

## 2. 컷 (11개)
| 컷 | 길이 | 참조 | 오디오(립싱크) | 프롬프트(영어 그대로) |
|---|---|---|---|---|
| K1 | 6초 | sc_teacher, sc_teacher_cu, sc_classroom | E9-01_jiu_teacherbody.mp3 | Vertical 9:16 realistic Korean high school drama. Morning homeroom in a bright classroom. The middle-aged male teacher from the reference (short graying hair, glasses on a cord, navy cardigan, striped tie) stands behind the teacher's desk holding an attendance book, medium shot, three-quarter front. Action 1 (0-4s): he speaks awkwardly to the class with an embarrassed smile, mouth moving naturally, eyes darting around. Action 2 (4-6s): he lifts his pinky finger and tucks his short hair behind his ear like a shy teenage girl. Blurred students in the foreground. Soft morning window light from the left. Slow push-in. He does not look into the lens. No text. |
| K2 | 5초 | sc_jiu, sc_classroom | E9-02_teacher_studentbody.mp3 | Vertical 9:16 realistic Korean high school drama. The schoolgirl from the reference (shoulder-length black hair, ribbon hair clip, navy blazer) sits in the back row, side view, arms folded like a grumpy middle-aged man. Action 1: she turns her head toward the noisy classmates behind her. Action 2: she says one short stern line in a low voice, mouth moving, eyebrows lowered. Blurred classmates around. Warm morning light. Handheld, slight push-in. No one looks at the camera. No text. |
| K3 | 5초 | sc_teacher, sc_classroom | — | Vertical 9:16 realistic Korean high school drama. Over the shoulder of the middle-aged male teacher (navy cardigan, graying hair, back of head blurred in the left foreground), a schoolgirl in a navy blazer stands in front of the teacher's desk. Action 1: she holds one hand over her lower belly and fidgets with the other hand, putting on a weak, pained face. Action 2: she speaks one short line softly, mouth moving. Morning classroom. No one looks at the camera. No text. |
| K4 | 6초 | sc_teacher_cu, sc_classroom | E9-05_jiu_teacherbody.mp3 | Vertical 9:16 realistic. Close-up of the middle-aged male teacher (graying hair, glasses on a cord, navy cardigan). Action 1 (0-3s): he narrows his eyes knowingly and nods slowly, then speaks with a sly little smile, mouth moving. Action 2 (3-6s): he picks up a smartphone from the desk and raises it to his ear. Classroom background softly blurred. Slow dolly-in. He does not look into the lens. No text. |
| K5 | 8초 | sc_teacher_cu, sc_classroom | E9-07_jiu_teacherbody.mp3 앞부분(0–3.6초) | Vertical 9:16 realistic. Medium close-up of the middle-aged male teacher holding a smartphone to his ear in the classroom. Action 1 (0-4s): he speaks into the phone in an overly polite, sweet way, smiling, mouth moving. Action 2 (4-8s): he listens, tilting his head with a knowing grin, then lowers the phone slowly. Window light from the left. Slow arc around him. No text. |
| K6 | 5초 | sc_classroom | — | Vertical 9:16 realistic. Close shot of a Korean schoolgirl in a navy blazer standing at the teacher's desk (the same girl as K3). Action 1: her eyes go wide and her body tenses as she realizes she has been caught. Action 2: in the blurred background a girl in the back row covers her mouth, shoulders shaking with held-back laughter. Crash zoom-in on her face. No text. |
| K7 | 5초 | sc_jiu, sc_classroom | — | Vertical 9:16 realistic. The schoolgirl from the reference (ribbon hair clip, navy blazer) in the back row, mouth closed, watching the front of the class with an impressed, middle-aged expression; she claps her hands softly three times and nods slowly. Low angle from the desk. No one looks at the camera. No text. |
| K8 | 6초 | sc_choi, sc_perfume, sc_office | — | Vertical 9:16 realistic insert. A teacher's desk in a teachers' office at lunchtime; a handwritten list on lined notebook paper is taped to the desk partition beside the monitor; the round glass perfume bottle with a gold cap stands next to it. Only the hand and beige striped cardigan sleeve of the woman teacher are visible. Action 1: her fingertip slides down the lines of the list and stops on one line. Action 2: she picks up the perfume bottle, puts it into the desk drawer and closes the drawer gently. Soft window light with blind stripes. Slow push-in. No readable writing. No text. |
| K9 | 8초 | sc_bench, sc_hood, sc_choi | — | Vertical 9:16 realistic. Lunchtime at the far end of a school sports field, wide shot from behind a weathered wooden bench. A boy in a light gray hoodie with the hood up sits alone on the right end, seen only from behind. Action 1 (0-4s): a woman teacher (low ponytail, beige striped cardigan) walks in from the left and sits down carefully on the left end, leaving one seat of space, seen from behind. Action 2 (4-8s): the boy slowly takes one white earphone out of his ear. Overcast noon light with soft backlight. Slow dolly-in. No faces toward the camera. No text. |
| K10 | 15초(또는 10초+5초 이어서) | sc_choi | E9-09a_choi_celine.mp3 → E9-09b_choi_celine.mp3 | Vertical 9:16 realistic. Side close-up of a Korean woman teacher in her late thirties (low ponytail, beige striped cardigan, natural makeup), sitting on a wooden bench outdoors, facing right toward a boy who is out of frame. She speaks gently and calmly, mouth moving naturally, sometimes lowering her eyes, then looking back at him with kind but firm eyes. The blurred sports field and fence behind her. Soft overcast light with a warm rim on her hair. Very slow push-in. She does not look into the lens. No text. (같은 얼굴로 2~3컷 필요: 오디오 E9-09a 15초, E9-09b 22초를 나눠서) |
| K11 | 6초 | sc_teacher, sc_jiu, sc_vp_full | — | Vertical 9:16 realistic comedy. Behind a hedge near the sports field, the middle-aged male teacher (navy cardigan) and the schoolgirl (ribbon hair clip, navy blazer) crouch side by side, peeking over the hedge. Action 1: the teacher dabs his teary eyes with a handkerchief; the girl puts a finger to her lips, "shh". Action 2: a gray-suited vice principal with metal-rimmed glasses appears standing right behind them and taps his wristwatch with one finger. Daylight. Handheld. No one looks at the camera. No text. |
| K12 | 6초 | sc_hood, sc_bench | — | Vertical 9:16 realistic. Close shot from behind of the boy in the light gray hoodie on the bench. Action 1: his fingers stop fidgeting with the earphone cord. Action 2: he slowly pulls his hood down and lifts his head toward the field. Overcast light, wind moving his hair. Slow push-in. Face not visible. No text. |

## 3. 편집장에게 넘길 것
- 올린 컷 목록과 각 컷 길이, 립싱크를 했는지(오디오를 넣었는지) 여부.
