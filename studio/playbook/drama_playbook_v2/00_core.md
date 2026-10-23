# 00_core.md — AInspire 반자동화 드라마 제작 플레이북 v2.1 (진입점·라우터 + 필수 규칙)

> **드라마 한 편을, 정통 시나리오 작법에 기반한 대화형 인터뷰만으로 `시나리오 → 스토리보드 → 이미지 → 영상 → 편집`까지 반자동으로 만드는 진행 대본.**
> 근거: **AInspire 기획 강의(「AI 드라마 완성 클래스」 기초이론 + M1 시나리오의 구조 + M2 캐릭터와 줄거리 + M3 명작 3편 해부 + M4 하이브리드 — M5 제외)** + 정통 작법서 8권(시학·시드필드·맥키·에그리·Save the Cat·영웅의 여정·김사라·육상효) + 명작 드라마 심층 해부(브레이킹 배드·나의 아저씨·시그널) + 광고 스토리보드 플레이북 v2(`18_`)의 생성 파이프라인.
> 이 플레이북은 `19_shortdrama_playbook_v1`(세로 5분 막장/사이다 공식)을 **대체·상위**한다. 작법 우선·취향 반영·표절 청정의 일반 드라마 제작용이며, **숏폼(5분 하이브리드)도 트랙 옵션으로 흡수**한다.

### 📚 강의 앵커 규약 (전 파일 공통 — 두 개의 강의 소스)
- **`📚 강의: 슬라이드N·제목`** = 「AI 드라마 완성 클래스」(숏드라마 마스터클래스) 교안·대본의 해당 슬라이드. 원문: `projects/hybrid/shortdrama_masterclass/v2026-07-02/교안_숏드라마_마스터클래스_v2.html` · 같은 폴더 `text/강의대본.md`. **⛔ M5(AI 파이프라인, 슬라이드 70~)는 인용·적용 금지**(구버전 파이프라인 — 본 플레이북이 상위).
- **`🎬 비전: Part N`** = 「AI 비전 디렉팅」 8-Day 커리큘럼(인문학 연출 강의, Notion — Part 1~5 확보, 6~8 미제공). 핵심 철학: **"AI는 확률로 계산하고, 인간은 결핍으로 상상한다"** · **"AI는 캔버스를 채우려 하고, 감독은 캔버스를 비우려(Negative Space) 해야 한다."** 원문(사용자 Notion 계정 필요):
  - Part 1 기획의 본질(시간·몽타주·푼크툼): `app.notion.com/p/Part-1-2cf3970bb5e180c29013eaf79d8139d4`
  - Part 2 렌즈와 시선의 권력: `app.notion.com/p/Part-2-2cf3970bb5e180cfa4f3f3736abd8c14`
  - Part 3 빛과 색채의 심리학: `app.notion.com/p/Part3-2cf3970bb5e18009ab42fd38ce80e61d`
  - Part 4 미장센: `app.notion.com/p/Part-4-The-Power-of-Mise-en-sc-ne-2d03970bb5e180409940cacf8c0469c3`
  - Part 5 움직임의 미학: `app.notion.com/p/Part5-The-Aesthetics-of-Motion-2d03970bb5e18063a2acdcd3a6b2bb00`
- **핵심 가르침은 이미 플레이북 본문에 증류되어 있으므로, 진행 중에 원문을 열 필요가 없다**(토큰 절약). 사용자가 심층 근거를 원할 때만 해당 슬라이드/Part 하나를 연다.
- 강의의 워크드 예시(청소부·회장, 명작 장면 묘사, 특정 감독 스타일 묘사)는 **교육용 예시·원리 참조**다. 실전 산출물에 그대로 복제 금지(규칙 4·`07` 3부). 감독 이름(큐브릭·웨스 앤더슨 등)은 **원리 설명용**이며, 프롬프트에는 원리를 풀어 쓴 광학·조명 언어를 쓴다.

---

## 이 플레이북의 5대 원칙 (사용자 확정 요구사항 — 절대 훼손 금지)

1. **시나리오가 가장 중요하다.** 작법 프레임워크로 체계화하되, **대화를 통해** 만들어 간다. 표절을 엄격히 차단하고, **만드는 사람의 취향이 상세히 반영**되도록 구체적·다양한 질문으로 자연스럽게 완성한다. (→ `01_scenario`)
2. **스토리보드는 가로/세로를 먼저 고른다.** 대사 장면 ↔ 인서트 장면을 나누고, 타이트한 호흡 ↔ 천천히 흐르는 호흡을 고르게 한다. 진짜 생성 전에 **나노바나나-라이트 480p 저화질 전체 스토리보드 HTML**을 먼저 만들어 셀렉트받고, 그 결과로 **씬별 이미지 수정·모델 선택 + 전 씬 공통 미술·조명 UI**를 제공한다. (→ `02_storyboard`)
3. **이미지 생성이 두 번째로 중요하다.** 인물마다 **1장에 특징이 모두 담긴 캐릭터 시트를 gpt-image-2로 먼저** 만든다. 다양한 화각(하이·로우·사이드·더치·오버더숄더·데마이·인서트)을 밸런스 있게, **얕은 심도 + ARRI Alexa 질감·색감**으로. 조명은 **원하는 작품명을 지정해 룩을 입히고**(하이키·로우키·네거티브필), 미술은 **컬러 콘트라스트·컬러 밸런스**까지 디테일하게 물어 특색 있는 배경을 만든다. (→ `03_image`)
4. **영상은 클링3.0 / 시댄스2.0 중 선택**, 화질 720p / 1080p 중 선택. **캐릭터별 음성 특성을 샘플 영상 또는 기존 음성 첨부로 확정해 잠그고, 모든 씬에서 음성이 변하지 않게 일관성을 유지한다(음성 일관성 최우선).** **모든 영상은 BGM 절대 금지, 효과음(SFX)만.** 모든 장면에 **캐릭터 시트를 강력 적용**해 외관·음성을 동일하게 만든다. 씬별 결과는 **버전별 HTML에서 관리·미세수정**한다. (→ `04_video`)
5. **편집은 최종 컨펌 영상만 골라 프리미어로 불러와 시나리오 시간순으로 배열**한다. (→ `05_edit`)

> **이 문서를 실행하는 에이전트에게(IMPORTANT):**
> 1. 각 **STAGE / GATE**에 도착하면 그 질문을 `AskUserQuestion` 도구로 **객관식**으로 물어라. 옵션마다 쉬운 설명을 붙여라. **단, `01_scenario`의 취향 인터뷰는 객관식 + 자유서술 혼합**이다(취향은 객관식만으로 안 잡힌다 — 해당 파일 규칙을 따른다).
> 2. 사용자가 답하기 전에는 다음 단계로 넘어가지 마라. 비싼 생성(돈·시간)이 걸린 분기는 특히 먼저 묻는다.
> 3. 각 STAGE가 끝나면 **정리 시트**(SCENARIO_BIBLE / STORYBOARD_PLAN / CHARACTER_SHEETS / VIDEO_PLAN)를 텍스트로 보여주고 승인받은 뒤 다음으로 간다.
> 4. 용어가 처음 나오면 한 줄로 풀어 설명한다. (`07_reference_craft-and-taste.md` 맨 끝 [용어 사전])
> 5. **`AskUserQuestion` 호출 규칙:** 한 번의 호출에 `questions` 배열을 반드시 채운다 — 질문마다 `question`·`header`·`options`(2~4개, 각 `label`+`description`) 전부 필수. 한 번에 최대 4개 질문. (누락 시 `InputValidationError`로 멈춘다.)

---

## ★ 로딩 가이드 — 이 플레이북 어떻게 읽나

에이전트는 항상 이 파일(`00_core.md`)을 **먼저** 읽는다(필수 규칙·규칙0·상수 요약·엔진 표가 여기 있다). 그다음은 단계별로 **한 파일씩** 온디맨드 로드한다. **처음에 8개 문서를 통독하지 마라 — 컨텍스트 낭비다.**

| 단계 | 읽을 파일 | 핵심 |
|---|---|---|
| **STAGE 1 — 시나리오** ★가장 중요 | `01_scenario_S1-S12.md` | 작법 체계화 + 취향 심층 인터뷰 + 표절 차단 → SCENARIO_BIBLE |
| **STAGE 2 — 스토리보드** | `02_storyboard_S13-S18.md` | 가로/세로·대사/인서트·호흡 → 480p 프리뷰 HTML → 씬수정·미술조명 UI |
| **STAGE 3 — 이미지** ★두번째 중요 | `03_image_S19-S24.md` | 캐릭터 시트(gpt-image-2) → 화각 밸런스·ARRI 룩·작품별 조명·미술 |
| **STAGE 4 — 영상** | `04_video_S25-S30.md` | 클링/시댄스·720/1080·음성 일관성 락·No-BGM·버전 콘솔 |
| **STAGE 5 — 편집** | `05_edit_S31-S32.md` | 최종 셀렉 → 프리미어 시간순 자동 배열 |
| **이미지·영상 생성 직전(상수 풀텍스트)** | `06_reference_enhance-prompts.md` | 규칙0 · 룩 상수 · 화각 밸런스 카드 · 조명 레시피북 |
| **작법·취향·표절 관리** | `07_reference_craft-and-taste.md` | 작법 카드 A~N · 취향 질문 은행 · 표절 차단 프로토콜 · 용어 사전 |
| **강의 원문(📚 앵커의 심층 근거 — 요청 시만)** | `projects/hybrid/shortdrama_masterclass/v2026-07-02/교안_..._v2.html` · `text/강의대본.md` | **통독 금지, 앵커의 슬라이드만. ⛔ M5(슬라이드 70~) 사용 금지** |
| **강의 원문(🎬 비전 디렉팅 — 요청 시만)** | 앵커 규약의 Notion 링크(Part 1~5, 사용자 계정 필요) | 통독 금지, 해당 Part만. 핵심은 본문·`06`·`07` 카드 O에 증류됨 |
| **심층 근거(필요할 때만)** | `projects/hybrid/shortdrama_masterclass/v2026-07-02/text/masterpiece_3_digest.md` · `04_masterpiece_report.md` | 명작 해부 — 통독 금지, 해당 파트만 |

---

## 우리가 만드는 것 (최종 산출물 체인)

1. **SCENARIO_BIBLE**: 로그라인 · 3막 비트시트 · 캐릭터 아크(Want/Need/Lie/Wound) · 씬 리스트 · 대사 · **취향 프로파일** · **표절 청정 확인서**. — 텍스트 1장.
2. **STORYBOARD_PLAN**: 프레임(가로/세로) · 대사씬/인서트씬 분류 · 씬별 호흡(타이트/슬로우) · 화각·미술·조명 지정.
3. **480p 프리뷰 스토리보드 HTML**: 나노바나나-라이트로 뽑은 전 씬 저화질 + 셀렉터(OK/수정) + 씬별 모델·미술·조명 수정 패널.
4. **CHARACTER_SHEETS**: 인물별 1장 캐릭터 시트(gpt-image-2) + **Voice Sheet(음성 프로파일 락)**.
5. **본 이미지**: 씬별 고화질 이미지(캐릭터 시트 ref 락 + 화각 밸런스 + ARRI 룩 + 지정 조명·미술).
6. **씬 영상**: 클링3.0/시댄스2.0 i2v 클립(캐릭터 시트 강력 적용 · 음성 일관성 락 · No-BGM/SFX only) + **버전 관리 콘솔 HTML**.
7. **프리미어 프로젝트**: 최종 컨펌 컷을 시나리오 시간순으로 배열한 편집 타임라인.

> **BGM은 이 파이프라인에서 만들지 않는다.** 영상 트랙은 **효과음만**. 음악이 필요하면 편집 단계에서 별도로 얹는다(사용자 결정). — 규칙 0-[B].

---

## 쓰는 도구 (엔진 표)

| 단계 | 용도 | 도구·모델 | 실행 경로 |
|---|---|---|---|
| 이미지 — **캐릭터 시트** | 1장에 특징 총집합 | **gpt-image-2** | Higgsfield MCP `generate_image(gpt_image_2)` / Magnific `images_generate(gpt-2)` / 메인 repo `system/generate_gpt_image.mjs`(CometAPI) |
| 이미지 — **480p 프리뷰** | 저비용 전 씬 초벌 | **나노바나나-라이트**(nano_banana 저해상·드래프트) | Higgsfield/Magnific `nano_banana_2` 저해상 모드 (호출 전 `models_list`로 라벨 확정) |
| 이미지 — **본 생성** | 고화질 씬 | nano_banana_2 / gpt_image_2 / seedream-4 | 연결된 엔진, 캐릭터 시트 ref 락 |
| 영상 — i2v | 씬 영상 | **클링 3.0** 또는 **시댄스 2.0** | Higgsfield MCP(`kling3_0`/`seedance_2_0`) · CLI · Replicate(`system/generate_seedance.mjs`) |
| 음성 | 인물별 voice 락 | **ElevenLabs**(voice clone / voice_id) | 직접 API. Voice Sheet에 voice_id 박제 |
| 업스케일·누끼 | 후처리 | Magnific MCP | 얼굴 보호 마스크 |
| 편집 | 시간순 배열 | **Premiere**(CEP 브리지) | `reference-premiere-bridge-filedrop` 방식(temp command/response) |

### 🔌 STAGE 0 — 시작 셋업 3종 (제일 먼저: 연결 → 품질 모드 → 런타임 어댑터)

#### S0-A. 생성 엔진 연결 확인 (생성 전 필수)
**Higgsfield MCP / Magnific MCP / 메인 repo 직접 API(CometAPI·Replicate) 중 최소 하나**가 연결돼야 생성 단계로 간다.
1. 확인: Higgsfield `balance` / Magnific `account_balance` / 메인 repo `system/.env`의 `COMET_API_KEY`·`REPLICATE_API_TOKEN`.
2. 안 되어 있으면 연결부터(OAuth 또는 키 입력을 사용자에게 요청). **연결 전까지 이미지 생성(STAGE 3 이후)으로 가지 마라.**
3. **음성 일관성을 쓸 거면 `ELEVENLABS_API_KEY`도 확인**(인물별 voice 락의 핵심). 없으면 사용자에게 키 발급·입력 안내. 없이도 시나리오·스토리보드·무음영상까진 진행 가능하나, 음성 일관성은 불가함을 고지.
4. 편집(STAGE 5)은 Premiere 데스크톱 + CEP 브리지가 필요(생성 엔진과 무관 — 편집 직전에 확인).

#### S0-B. 품질 모드 선택 ★ (반드시 최초에 1회 — 객관식)
> **왜:** 크레딧을 어디에 쓸지의 철학을 먼저 정해야, 이후 모든 생성 GATE가 흔들리지 않는다. 프로젝트 중간에 모드 변경 가능(변경 시점부터 적용, PROJECT_PROFILE에 기록).

**Q0-1. 이번 프로젝트의 크레딧 철학은?** (객관식)
| 선택 | 모드 | 철학 |
|---|---|---|
| A. **최고 품질(QUALITY)** | 크레딧이 들어도 최고의 결과 | 후보 다안 생성 → 베스트 선택. 마스터 화질 직행 |
| B. **가성비(ECO)** | 크레딧을 아끼며 충분히 좋은 결과 | 저해상 초벌로 방향 확정 → 컨펌분만 고화질. 1안+수정 |

**모드별 기본값 표 (각 생성 GATE가 이 표를 읽는다 — MODE 훅):**
| 항목 | QUALITY | ECO |
|---|---|---|
| 캐릭터 시트(S19) | 인물별 **3안** → 선택, 2k | 인물별 **1안** + 수정 루프, 1k~2k |
| 480p 프리뷰(S16) | 전 씬 (동일 — 이미 최저비용 장치) | 전 씬 (동일) |
| 본 이미지(S24) | 씬당 **2안**(가능하면 엔진 병렬) → 베스트, 2k | 씬당 **1안**, 수정된 씬만 재생성, 1k~2k |
| 업스케일 | 적극 (주요 컷) | 최종 채택 컷만 |
| 영상(S25~28) | **1080p 직행**, 감정 피크 씬은 2테이크 | **2패스: 720p 초벌 전 씬 → 컨펌 컷은 1순위 `video_upscale`로 1080p화(테이크 보존), 업스케일 품질 미달 컷만 1080p 재생성+재컨펌** |
| 음성 샘플(S26) | 후보 4개 + 립싱크 테스트 영상 | 후보 2개, TTS 샘플만(립싱크 테스트 생략) |
| 수정 루프 | 자유 (단, 재생성 전 원인 진단은 동일 의무) | 씬당 재생성 2회 초과 시 → 원인 진단 후 사용자 확인 |

#### S0-C. 런타임 어댑터 — 어떤 모델·어떤 앱에서도 돌아가게 (크로스 모델 필수)
> 이 플레이북은 Claude(Opus/Sonnet/Haiku)·ChatGPT·Gemini 등 **어떤 에이전트에서도** 실행 가능해야 한다. 시작 시 아래 3가지 능력을 자가 점검하고, 없는 능력은 **폴백**으로 대체한다. 절차·질문·산출물 구조는 폴백에서도 동일하다.

| 능력 | 있으면 | 없으면 (폴백) |
|---|---|---|
| **객관식 질문 도구**(AskUserQuestion 등) | 도구로 질문 | **채팅 텍스트로 번호 객관식** 제시("1/2/3 중 답해주세요") — 질문·옵션·설명 구조는 동일 |
| **생성 도구 호출**(MCP/API/스크립트) | 직접 호출(4종 프리뷰 승인 후) | **프롬프트 패키지 모드**: 설정표(모델·해상도·비율·ref)+완성 프롬프트를 복붙 블록으로 만들어 주고, 사용자가 해당 서비스(웹 Higgsfield·Kling·Magnific 등)에서 직접 생성 → 결과 파일명을 규칙대로 저장하게 안내 |
| **파일 시스템·로컬 실행**(HTML 콘솔·스크립트) | 콘솔 HTML·selections.json 사용 | **마크다운 표 셀렉터**: 씬번호·프롬프트 요약·[OK/수정] 열이 있는 표를 채팅에 제시하고 사용자가 표로 회신. 산출물(BIBLE/PLAN)은 채팅 코드블록으로 출력해 사용자가 저장 |

- **백그라운드 에이전트가 없으면**: 배치 생성을 순차 처리하되, **체크포인트(생성 완료 목록)를 산출물 시트에 기록**해 중단돼도 빠진 것만 재개한다.
- **STAGE 5(편집)·S30(믹스)의 폴백**: 로컬 실행 불가 런타임에서는 — S30: ffmpeg 믹스 생략, 분리 스템(대사/SFX) 목록 + 클립별 배치 지시서만 산출(사용자가 프리미어에서 직접 얹음). S31~S32: `final_selects` 기반 **시간순 배열표**(씬번호→클립 파일명→V1/A1/A2 트랙·순서)를 코드블록으로 제공하는 **수동 편집 가이드 모드**로 진행.
- **컨텍스트가 작은 모델(Sonnet 등)에서는**: 각 STAGE 종료 시 요약 시트(SCENARIO_BIBLE·STORYBOARD_PLAN 등)를 **다시 출력**해 그것만 다음 STAGE의 진실 원천으로 쓴다. 이전 대화 전체를 되짚지 않는다.
- **규칙0·강화 상수는 어떤 모델에서든 VERBATIM 복사**한다. 요약·의역 금지(작은 모델일수록 요약 유혹이 크다 — 금지).

### 💳 크레딧 절약 공통 규칙 (모드 무관, 항상 적용)
1. **프리뷰 승인 없이는 호출 없다** — 4종 확인(MODEL·해상도·오디오·비율) + 프롬프트 요약 테이블 승인 후에만 크레딧을 쓴다.
2. **배치 전 비용 견적** — `get_cost`/`generate cost`/크레딧 잔액으로 "씬수×단가" 총액을 보여주고 승인받는다.
3. **싼 것으로 방향, 비싼 것으로 완성** — 구도·미술 방향은 480p 초벌에서 다 잡는다. 본 생성에서 방향을 실험하지 않는다.
4. **진단 없는 재생성 금지** — 실패하면 먼저 원인(프롬프트? ref? 모델? 화각?)을 한 줄로 진단하고 그 변수 하나만 바꿔 재시도. 같은 프롬프트 반복 제출 금지.
5. **resumable** — 디스크에 이미 있는 산출물은 건너뛴다. 실패분만 재생성.
6. **재시도 상한** — 네트워크성 오류(fetch failed) 재시도 3회, 필터 오탐 우회 2회. 초과 시 사용자에게 보고 후 결정.
7. **컨텍스트도 크레딧이다** — 문서는 한 파일씩, 생성물 Read 금지, 교안·대본 통독 금지(앵커 슬라이드만), 긴 산출물은 파일로 쓰고 채팅엔 요약만.

---

## ⛔ 규칙 0 — 이미지·영상 생성 시 무조건·강제 (NON-NEGOTIABLE, 어떤 씬도 예외 없음)

> **아래 프리픽스를 빼먹은 생성은 즉시 폐기·재생성한다. 프롬프트 프리뷰 테이블에 "MANDATORY 프리픽스 주입됨"을 반드시 표기한다.**

**[A] 이미지 — 모든 씬 이미지 프롬프트에 반드시 합친다 (캐릭터 락 · 화각 밸런스 · ARRI 룩):**
```text
MANDATORY DRAMA IMAGE PREFIX (append to EVERY scene-image prompt, no exceptions):
— IDENTITY LOCK: render EXACTLY the same person(s) as the character-sheet reference — same face, age, hair, signature wardrobe. Never beautify, never average into a generic idol face. If two characters share a frame, each must match their own sheet.
— ANGLE BALANCE: pick ONE deliberate angle per shot from {high / low / side / dutch / over-the-shoulder / demai close-up / insert / object POV}, and never repeat the previous shot's angle. ZERO flat front-facing eye-level unless it is a designated peak-emotion reaction.
— DEPTH & TEXTURE: shallow depth of field (telephoto demai bokeh), clear FG/MG/BG separation; ARRI Alexa / ARRI look — filmic latitude, gentle organic softness (NOT clinical digital sharpness), fine 35mm grain, true-to-skin subsurface texture.
— LIGHTING & ART obey the shot's assigned lighting recipe and art-direction (color contrast / color balance) from STORYBOARD_PLAN; LOW-KEY by default, high-key ONLY where the recipe says so.
```

**[B] 영상 — 모든 영상 프롬프트의 맨 앞에 반드시 둔다 (BGM 절대 금지 · 효과음만 · 음성 일관성):**
```text
MANDATORY DRAMA VIDEO PREFIX (must be the FIRST lines of EVERY video prompt, no exceptions):
No background music. NO BGM. NO score. SFX only — diegetic sound effects (footsteps, breath, cloth, glass, door). NO musical bed whatsoever. (Music, if ever wanted, is added later in the edit — never baked into the clip.)
CHARACTER LOCK: appearance and voice must match this character's sheet and Voice Sheet exactly — do not drift the face or the voice across shots.
```

**[C] 캐릭터·음성 일관성 락 — 모든 씬 생성에 강제:**
- **캐릭터 시트 없이는 씬 이미지도, 씬 영상도 생성하지 않는다.** 인물이 등장하는 모든 컷은 그 인물의 캐릭터 시트를 ref로 잠근다(STAGE 3 확정 후). **(유일한 예외: S16의 480p 나노바나나-라이트 초벌 — 구도·미술 방향 확인용이라 시트 락 없이 허용. 본 이미지(S24)·영상(S27~)부터는 예외 없음.)**
- **음성은 Voice Sheet(인물별 락된 voice_id)로만.** 씬마다 음성을 새로 정하지 않는다. 대사 오디오는 락된 voice로 생성하고, 영상 클립 자체의 오디오 트랙은 규칙 0-[B]대로 SFX only. (→ `04_video` S26 음성 일관성 워크플로우)

> [A][B][C]는 아래 강화 상수(규칙 5)보다 **상위**다. 충돌 시 규칙 0이 이긴다.

### 절대 규칙 7가지 (어기면 처음부터 다시 함)
1. **생성 직전 4종 확인 + 프리뷰 승인** — MODEL · 해상도 · 오디오 · 비율을 표로 보여주고 OK 후에만 호출. 첨부 ref는 파일명·경로·용도까지 표기. 이미지 업로드 전 해상도·용량 확인(ref 다운스케일). (CLAUDE.md 규칙 5)
2. **덮어쓰기 금지** — 수정마다 새 버전 폴더(`v{날짜}_v2`, `_v3`…)와 새 HTML로 누적. (메모리: feedback-version-never-overwrite)
3. **생성 이미지를 Read 도구로 열지 않는다** — 경로만 안내, 사용자가 브라우저/콘솔로 확인. (컨텍스트 절약 + 20MB 제한)
4. **표절·IP 침해 절대 금지 (엄격)** — 실존 배우 얼굴, 브랜드 로고, **기존 드라마·영화·소설의 캐릭터·플롯·명장면·대사 복제 금지.** 작법의 '구조·원리'만 차용하고 표면(인물·사건·대사·비주얼)은 100% 오리지널. STAGE 1의 **표절 차단 프로토콜**(`07`)을 통과하지 못한 시나리오로는 생성에 들어가지 않는다.
5. **강화 상수 기본 주입** — 모든 이미지에 `DRAMA_IMG_ENHANCE`, 모든 영상에 `DRAMA_VID_ENHANCE`(풀텍스트 `06`).
6. **캐릭터 시트·Voice Sheet 우선** — **씬 이미지(S24) = 캐릭터 시트 락 필수 / 씬 영상·대사 오디오(S27~) = 캐릭터 시트 + Voice Sheet(S26) 락 필수.** (S16 480p 초벌만 예외 · ElevenLabs 미연결 시 무음영상은 S0-A 3항 고지 후 허용)
7. **음성 일관성 최우선** — 한 인물의 목소리는 전 씬에서 동일해야 한다. 드리프트가 감지되면 그 씬을 폐기하고 락된 voice로 재생성. (사용자 강조 항목)

---

## ★ 필수 강화 프롬프트 (요약 — 풀텍스트는 06)

### DRAMA_IMG_ENHANCE — 씬 이미지 공통
의도: 시네마틱 실사(ARRI Alexa 질감·틸앤앰버/저채도 필름 룩·크러시드 블랙·아나모픽·35mm 그레인·하이퍼리얼 피부) + **화각 밸런스**(하이/로우/사이드/더치/OTS/데마이/인서트/오브젝트POV 로테이션, 정면 아이레벨 배제) + **지정 조명 레시피·미술(컬러 콘트라스트·밸런스)** 적용 + **가로/세로 프레임 준수**.

### DRAMA_VID_ENHANCE — 영상화(i2v) 공통
의도: **No-BGM·SFX only**(가장 강한 고정 규칙) / **캐릭터·음성 락**(외관·목소리 드리프트 금지) / 씬 호흡에 맞는 카메라 무브(타이트=빠른 단일 무브, 슬로우=느린 홀드·미세 무브) / 시작 이미지(캐릭터 시트 ref) 룩 유지.

> 유형별 확장(대사 CU / 대치 투샷 / 인서트 매크로 / 감정 홀드)과 조명 레시피북·화각 밸런스 카드는 `06_reference_enhance-prompts.md`.

---

## 전체 흐름 (5 STAGE)

```
[시작 전 — STAGE 0]
  S0-A 생성 엔진 연결 확인 (+ 음성 쓸 거면 ElevenLabs)
  → S0-B 품질 모드 선택 ★ (QUALITY 최고품질 / ECO 가성비)
  → S0-C 런타임 어댑터 (객관식 도구·생성 호출·파일시스템 폴백 확정)

[STAGE 1 · 시나리오 ★가장 중요 — 01_scenario]
  S1 소재·톤·취향 진입 인터뷰(+시청 계약·플랫폼) → S2 로그라인/전제 ★ → S3 캐릭터(Want/Need/Lie/Wound) →
  S4 3막·구성점 골격(25/50/75 정렬·콜드오픈) → S5 비트시트(Save the Cat/8시퀀스/7비트 v2 택1) → S6 씬 리스트 →
  S7 대사·서브텍스트 → S8 취향 정밀 반영 패스 → S9 표절 차단 프로토콜 ★ →
  S10 톤·주제 최종 점검 → S11 SCENARIO_BIBLE 승인 → S12 (선택)워크숍 루프

[STAGE 2 · 스토리보드 — 02_storyboard]
  S13 프레임(가로/세로) ★ → S14 대사씬/인서트씬 분류 → S15 호흡(타이트/슬로우) →
  S16 480p 나노바나나-라이트 전 씬 프리뷰 HTML + 셀렉터 →
  S17 씬별 수정·모델 선택 UI → S18 전 씬 공통 미술·조명 UI

[STAGE 3 · 이미지 ★두번째 중요 — 03_image]
  S19 캐릭터 시트(gpt-image-2, 1장 총집합) ★ → S20 Voice Sheet 준비 →
  S21 화각 밸런스 배정 → S22 조명 룩(작품 지정) → S23 미술(컬러 콘트라스트·밸런스) →
  S24 본 이미지 생성(캐릭터 락 + ARRI 룩)

[STAGE 4 · 영상 — 04_video]
  S25 엔진(클링3.0/시댄스2.0)·화질(720/1080) → S26 음성 일관성 락 ★ →
  S27 씬 영상 프롬프트(호흡·캐릭터·음성 락·No-BGM) → S28 씬 영상 배치 생성 →
  S29 버전 관리 콘솔·미세수정 → S30 대사·SFX 오디오 조립(No-BGM)

[STAGE 5 · 편집 — 05_edit]
  S31 최종 컷 셀렉·프리미어 임포트 → S32 시나리오 시간순 배열·export
```

★ = 가장 중요한 분기(비싼 실수가 여기서 갈린다). 시나리오(STAGE 1)에 시간을 가장 많이 쓴다.

---

## 막혔을 때의 황금 규칙

사용자가 제안을 계속 "별로"라고 하면 같은 걸 또 던지지 말고 —
① **피하고 싶은 점 한 줄**을 물어 키워드를 받거나,
② **취향 앵커를 다시 캔다**(좋아하는 장면·감정·톤을 구체적으로 되물어 `07`의 취향 질문 은행 활용),
③ 시나리오라면 **작법 원리로 되돌아가**(구성점이 약한지, 가치 변화가 없는지, Need가 안 보이는지) 진단 후 다시 제안한다.
무한 재생성은 토큰·시간 낭비다.
