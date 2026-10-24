# 시리즈 바이블 — 소울체인지

채널: 한입극장 [@twistbite_drama](https://www.youtube.com/@twistbite_drama) · "짧게 보고, 끝에서 뒤집히는 이야기."

## 올라간 회차 (2026-10-23 확인)

| 회차 | 제목 | 주소 | 조회수 |
|---|---|---|---|
| 1화 | 생결 쓰고 PC방 간 날, 담임샘과 몸이 바뀌었다 | https://www.youtube.com/shorts/chXehj3O4CI | 406 |
| 2화 | 담임 몸으로 등교한 날, 친구들이 날 못 알아봤다 | https://www.youtube.com/shorts/Uvafh7ob50g | 1.4천 |
| 3화 | (10/27 화 18:00 예약 공개, 최종본 v14 44초 — **다시 만들지 않음**) | — | — |

두 편 모두 쇼츠(세로 9:16)입니다. 영상 길이, 설명란, 각 회차의 시나리오 원본은 이 환경에서 확인하지 못했습니다.

## 시리즈 확정값 (회차마다 다시 묻지 않음)

| 항목 | 값 | 근거 |
|---|---|---|
| 시청 계약·트랙 | 모바일 피드, 숏폼 | 1·2화 쇼츠 |
| 프레임 | 세로 9:16 | 1·2화 |
| 제목 형식 | `<훅> \| 소울체인지 N화` | 1·2화 |
| 영상 엔진 | Dreamina Seedance 2.5, 컷당 5초, 행동 2개까지 | 제작 규칙 v1 2절 |
| 음성 | Higgsfield Audio(ElevenLabs v3) 커스텀 목소리 | 캐릭터·음성 설정 2절 |
| 캐릭터 참조 이미지 | 담임 `담임_refT.png`(+클로즈업), 지우 `지우_refS.png`, 교감 `교감_still_vp.png` | 키트 `characters/` |
| 반복 장소 | 교무실 `교무실_still_office.png`, 교실 `교실_still_class_B.png` | 키트 `backgrounds/` |
| 자막 | `soulchange_style.ass`(Jua 한 가지), 견본 `자막스타일_견본.png` | 제작 규칙 v1 4절 |
| 공개 일정 | 화·금·일 18:00 KST (주 3회) | 사장님 결정 2026-10-24 (제작 규칙 v1 1절의 주 2회를 바꿈) |
| 품질 모드 | **확인 필요** | — |

## 제작 키트 (가장 우선하는 기준)

`youtube-ops/series/_soulchange_kit/` (커밋 8445b7d). 클라우드 `/home/user/youtube-ops/series/_soulchange_kit/`, PC `C:\Users\경남교육청\youtube-ops\series\_soulchange_kit\`.

| 파일 | 내용 |
|---|---|
| `소울체인지_제작규칙.md` | 제작 규칙 v1(2026-10-24): 일정, 루틴, 목소리, 자막, 연출, 업로드 |
| `캐릭터_음성_설정.md` | 인물별 참조 이미지, 영상 프롬프트 공통 머리말, 인물별 목소리 |
| `soulchange_style.ass` | 고정 자막 스타일 헤더 |
| `characters/`, `backgrounds/`, `voices/`, `pip.png`, `pip_t.png`, `fonts/` | 참조 이미지, 참조 음성(+원문 .txt), 영혼 원, 폰트 |
| `gen_episode_ep3_reference.js` | 3화 빌드 스크립트 v7(참고용, PowerShell + ffmpeg) |
| `episodes/ep3/` (04cf0c3) | `README_3화.md`(최종 대사표·컷 목록, 먼저 읽기), `clips/` 컷 원본 8개, `voices/` 최종 대사 음성 10개, `cover.png`, `ep3v14.ass`, `ep3_timeline_v14.json`, `gen_ep3.js` |
| `episodes/ep4/` (04cf0c3) | 4화 시작 자료: `clips/m1~m4`, `voices/E4A1·E4I1·E4V1`, `soulchange-ep4-script-v1.md` |

인물: [담임](원래 몸, 40대 후반 남자) ↔ [지우](여고생)가 1화에서 몸이 바뀜. 표기는 "지우 영혼(담임 몸)"처럼 영혼과 몸을 함께 씁니다.

## 이야기의 바탕 자료

| 자료 | 위치 |
|---|---|
| 작가 규칙(초안) | `teacher-swap/작가규칙.md` |
| 기획서·원고·고증 | `youtube-ops` 저장소 `series/teacher-swap*.md`, `sources/` |
| 오디션 때 확정한 배역 이미지 8명 | `movie01` 저장소 `series/teacher-swap/cast/` |

**주의: 위 자료와 실제로 올라간 영상이 다릅니다.**
- `youtube-ops`의 원고(첫 아크 v3)는 가로 16:9 약 2분 롱폼이고, 몸이 3화 끝에 바뀝니다. 실제 영상은 쇼츠이고, **1화에서 이미 몸이 바뀝니다.** 2화는 담임 몸으로 등교하는 이야기입니다.
- 그래서 작가 규칙의 "한 화 약 2분, 가로 16:9" 같은 항목은 지금 시리즈와 맞지 않습니다. 고증·말투·금지 사항은 그대로 쓰되, 길이·화면 비율·회차 구성은 실제 1·2화를 기준으로 삼습니다.
- 실제 영상의 캐릭터는 제작 키트의 참조 이미지(담임 `refT`, 지우 `refS`)입니다. `movie01`의 오디션 배역 이미지는 쓰지 않습니다.

## 회차에서 새로 정해진 설정 (사장님 확정)
- 3화: 학부모는 얼굴 없이 문자로만, 목소리 `Ainsley`. 3화 공개 주소 https://youtube.com/shorts/ifNcRf0L57E
- 4화 구술(10/23): 두통 문자 학생 = **김서연**(우리 반 꼴찌). 담임 = **기간제 교사**(교감이 재계약을 쥠).
