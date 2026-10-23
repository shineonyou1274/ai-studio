# 06_reference_enhance-prompts.md — 생성 직전 로드 (상수 라이브러리)

> 이미지·영상 생성 직전 이 파일을 로드해 해당 상수를 프롬프트에 주입한다.
> 규칙0 [A][B][C]와 ENHANCE 상수는 **VERBATIM(글자 그대로)**이며 임의 수정하지 않는다. 프롬프트는 모델 입력용이라 영어로 적는다(humanizer 미적용).

---

## 어떤 상수를 언제 쓰나

| 상황 | 이미지 상수 | 영상 상수 |
|---|---|---|
| **480p 프리뷰(S16)** | `PREVIEW_DRAFT` (아래 0번 — 시트·화각·조명 확정 전 전용) | — |
| **씬 기본(모든 컷)** | 규칙0[A] + `DRAMA_IMG_ENHANCE` + `ARRI_LOOK` | 규칙0[B] + `DRAMA_VID_ENHANCE` |
| **인물 대사 컷** | + `IMG_PERSON_LOCK` | + `VID_DIALOGUE` |
| **인서트·매크로 컷** | + `IMG_INSERT_OBJECT` | + `VID_INSERT` |
| **캐릭터 시트(S19)** | `SHEET_MULTIVIEW`(정면 배제 예외) | — |
| **썸네일(S24-5)** | `THUMBNAIL_ENHANCE` | — |

## 0) PREVIEW_DRAFT — 480p 초벌 전용 (S16 — 캐릭터 시트·화각 배정·조명 레시피 확정 전)

```text
PREVIEW DRAFT 480p — storyboard direction check only (composition & art direction, not identity):
Obey the project frame (16:9 or 9:16; vertical keeps lower ~20% clean for subtitles). Shallow depth of field with FG/MG/BG separation; ARRI Alexa filmic look (soft, grainy, low-key default). Cinematic photoreal, never CGI/illustration. Characters described by text only (no reference lock at this stage); pick a deliberate non-frontal angle per shot and vary angles between adjacent cuts.
```

**우선순위:** 규칙0 [A][B][C] > DRAMA_*_ENHANCE > 유형별 확장. 충돌 시 규칙0이 이긴다.

---

## 규칙 0 (재게시 — NON-NEGOTIABLE)

**[A] 이미지 프리픽스 (모든 씬 이미지에 합침):**
```text
MANDATORY DRAMA IMAGE PREFIX (append to EVERY scene-image prompt, no exceptions):
— IDENTITY LOCK: render EXACTLY the same person(s) as the character-sheet reference — same face, age, hair, signature wardrobe. Never beautify, never average into a generic idol face. If two characters share a frame, each must match their own sheet.
— ANGLE BALANCE: pick ONE deliberate angle per shot from {high / low / side / dutch / over-the-shoulder / demai close-up / insert / object POV}, and never repeat the previous shot's angle. ZERO flat front-facing eye-level unless it is a designated peak-emotion reaction.
— DEPTH & TEXTURE: shallow depth of field (telephoto demai bokeh), clear FG/MG/BG separation; ARRI Alexa / ARRI look — filmic latitude, gentle organic softness (NOT clinical digital sharpness), fine 35mm grain, true-to-skin subsurface texture.
— LIGHTING & ART obey the shot's assigned lighting recipe and art-direction (color contrast / color balance) from STORYBOARD_PLAN; LOW-KEY by default, high-key ONLY where the recipe says so.
```

**[B] 영상 프리픽스 (모든 영상 맨 앞):**
```text
MANDATORY DRAMA VIDEO PREFIX (must be the FIRST lines of EVERY video prompt, no exceptions):
No background music. NO BGM. NO score. SFX only — diegetic sound effects (footsteps, breath, cloth, glass, door). NO musical bed whatsoever. (Music, if ever wanted, is added later in the edit — never baked into the clip.)
CHARACTER LOCK: appearance and voice must match this character's sheet and Voice Sheet exactly — do not drift the face or the voice across shots.
```

**[C]** 캐릭터 시트·Voice Sheet 락 없이는 씬 생성 금지. (→ `00_core` 규칙0-[C])

---

## 1) DRAMA_IMG_ENHANCE — 씬 이미지 공통

```text
CINEMATIC PHOTOREAL DRAMA — REQUIRED ENHANCEMENT (append to every scene image):
A real frame from a premium cinema-grade TV drama — never CGI / 3D-render / illustration / video-game render. Heightened photoreal realism with lifelike skin micro-texture (visible pores, subsurface scattering, sharp eye catchlights).
FRAME: obey the project frame (horizontal 16:9 OR vertical 9:16) from STORYBOARD_PLAN. For vertical, keep the lower ~20% as clean defocused negative space for subtitles.
ANGLE BALANCE: use the shot's assigned angle (high / low / side / dutch / OTS / demai CU / insert / object POV); rotate angles between adjacent cuts; reserve dead-on eye-level for peak-emotion reactions only.
DEPTH: telephoto shallow depth of field (demai bokeh) with clear 3-layer FG/MG/BG separation.
LIGHTING: obey the assigned lighting recipe; LOW-KEY luxurious grade by default — deep controlled shadows, restrained highlights, motivated practicals; high-key only where the recipe specifies.
ART: obey the assigned art-direction — deliberate color contrast (subject separated from background by hue) and color balance (one dominant color + one complementary accent); fill FG/MG/BG, no dead space (except the subtitle margin); place the scene's signature/setup props.
Compose so cuts connect via match-cuts; frame as a keyframe primed for the assigned pace's motion.
```

## 2) DRAMA_VID_ENHANCE — 영상화(i2v) 공통

```text
DYNAMIC DRAMA MOTION — REQUIRED (the audio line MUST be first on every video prompt):
No background music. NO BGM. NO score. SFX only — a few subtle diegetic sound effects; no musical bed.
CHARACTER & VOICE LOCK: keep the start-image character's exact face and the locked voice — no drift across shots.
MOTION by pace: TIGHT cuts carry ONE fast deliberate move (push-in, whip-pan, handheld sway, crash-zoom) with a match-cut hand-off; SLOW cuts HOLD (slow dolly / micro-orbit / near-static) letting micro-expression carry the beat.
Preserve the start image's ARRI Alexa filmic look; keep motion out of the subtitle margin (vertical). Reveal/peak-emotion shots hold on the face.
```

## 3) ARRI_LOOK — 카메라·필름 룩 상수 (질감·색감)

```text
CAMERA / FILM LOOK (ARRI): shot on ARRI Alexa (Alexa 65 for wides) with vintage anamorphic lenses; filmic latitude and highlight roll-off; gentle organic SOFTNESS — NOT clinical digital sharpness; fine-to-medium 35mm film grain (Vision3 500T feel); Black Pro-Mist halation bloom on highlights; anamorphic oval bokeh + subtle horizontal lens flare; crushed blacks, controlled low saturation, rich but not garish color; true cinematic contrast (chiaroscuro), never flat video-look.
```

## 4) IMG_PERSON_LOCK — 인물 대사 컷 확장

```text
PERSON CUT: exactly the SAME person as the character sheet (face, age, hair, wardrobe) — do not alter identity. Prefer 3/4 or over-the-shoulder framing and reaction close-ups over dead-on lip-sync framing (protects voice-lock dubbing later). Demai shallow DOF on the face; motivated key + negative fill; micro-expression readable.
```

## 5) IMG_INSERT_OBJECT — 인서트·매크로 컷 확장

```text
INSERT / MACRO: no faces (or only hands / silhouette). Extreme shallow DOF, razor-thin focus plane, creamy anamorphic bokeh. The prop/gesture carries story meaning — shoot setup props and payoff props at the SAME angle so they read as the same object across the film. Dramatic hard backlight, halation bloom, strong color contrast; end on a surface/texture filling the frame for a match-cut hand-off.
```

## 6) VID_DIALOGUE / VID_INSERT — 영상 유형 확장

```text
VID_DIALOGUE: diegetic SFX only, NO music. Subtle performance motion (breath, small gesture, weight shift); camera per pace. Do NOT bake in music or a different voice — dialogue audio is dubbed later with the locked voice_id. Reaction/peak shots hold 3-4s on the face.

VID_INSERT: diegetic SFX only, NO music. One continuous accelerating or slow-holding move per pace; heavy shallow-DOF; end as a surface/light swallows the frame (built-in match-cut out-point).
```

## 7) SHEET_MULTIVIEW — 캐릭터 시트 전용 (S19)

```text
CHARACTER SHEET — single composite image, neutral seamless background:
Show the SAME invented person in multiple views on one sheet — front, 3/4, profile, back of head/torso; one neutral expression + one signature expression; a full-body natural pose; a wardrobe close-up (fabric/texture/color); hair + hands detail inserts; a small color-palette swatch of the character's assigned colors; small name/age/keyword labels.
WARDROBE COLOR ARC: if this character has an arc, show THREE wardrobe stages side by side — stage 1 (before: muted/neutral tone), stage 2 (turning: stronger color), stage 3 (after: final color) — same person, same face, only wardrobe/color evolves; label the stages.
This is an identity reference — do NOT apply scene art or dramatic scene lighting; use clean even studio light so the face reads clearly. Give the person distinctive, identifiable features (not an averaged idol face); NEVER copy any real actor or existing character. Photoreal skin micro-texture, ARRI-grade rendering. (Front view is allowed here — this is the ONLY place the no-front-facing rule is waived.)
```

## 8) THUMBNAIL_ENHANCE — 썸네일 컷 전용 (S24-5, 숏폼 트랙)

```text
THUMBNAIL FRAME — REQUIRED (for thumbnail candidates only):
One dominant FACE in tight close-up carrying a single readable peak emotion (shock / fury / cold smile); high color contrast against the background; leave a large clean negative-space band for big bold Korean copy text (do not render the text itself); vivid but not garish; instantly readable at 200px wide. Frame variants: (a) emotion CU, (b) identity-gap two-layer composition, (c) freeze at the reversal moment, (d) confrontation two-shot (global variant only).
```

---

## ★ 화각 밸런스 카드 (S21 — 씬별 1개 배정, 인접 중복 금지)

| 화각 | 영어 키 | 용도 | 프롬프트 조각 |
|---|---|---|---|
| 하이앵글 | high-angle | 약화·조망 | `high-angle looking down, subject diminished` |
| 로우앵글 | low-angle | 위압·권력 | `low worm's-eye looking up, subject looms` |
| 사이드 | side / profile | 대치·관찰 | `clean side profile, lateral distance` |
| 더치 | dutch | 불안·붕괴 | `dutch tilt 20-40°, unstable horizon` |
| OTS | over-the-shoulder | 대화 시선 | `over-the-shoulder, foreground blurred sliver` |
| 데마이 CU | demai close-up | 감정·표정 | `telephoto demai close-up, ultra-shallow bokeh` |
| 인서트 | insert / macro | 소품·상징 | `macro insert, razor-thin focus` |
| 오브젝트 POV | object POV | "이 사물이 중요해진다" 신호 + 연출감 | `wide-angle low POV from inside/under the object looking up at the character` |

> 규칙: 정면 온-액시스 CU = 감정 피크 리액션 전용(작품당 소수). 대사 씬 = OTS·3/4·리액션 우선. 셋업/페이오프 소품 = 심기·회수를 동일 앵글 + 동일 소품 ref로.
> **가짜 리버스샷(투샷 회피):** 두 인물 대치는 각자 단독 CU를 맞교차 — `single-character close-up, eyeline matched for cross-cut with the counterpart shot (opposite look direction), consistent lens & light` × 2컷. 한 프레임 투샷은 꼭 필요할 때만.
> **프레임별 화각 예산:** 세로 9:16 = 반신~CU 위주, 와이드 막당 1컷 이하(표정이 정보의 전부). 가로 16:9 = 와이드 허용.

---

## ★ 조명 레시피북 (S22 — 룩을 프롬프트 조각으로)

| 룩 | 프롬프트 조각 |
|---|---|
| 로우키 | `low-key chiaroscuro, deep controlled shadows, single hard key, restrained highlights` |
| 하이키 | `high-key soft even light, minimal shadow, bright airy` |
| 네거티브필 | `black negative fill on shadow side, one side of the face sculpted into deep shadow` |
| 렘브란트 | `Rembrandt lighting, triangle of light on the shadow-side cheek, key from 45 degrees side-above` |
| 버터플라이 | `butterfly lighting, key from high front, small nose shadow, glamorous goddess look` |
| 스플릿 | `split lighting, key from exactly 90° side, half the face in total darkness, duality` |
| 볼류메트릭/갓레이 | `volumetric lighting, visible light shafts, god rays, dust in the air, subtle haze` |
| 하드 라이트 | `hard light, small strong source, razor-edged shadows, unforgiving texture detail` |
| 소프트 라이트 | `soft diffused light, large source, shadowless gentle falloff, dreamy flattering` |
| 실루엣 역광 | `hard rim backlight, subject as silhouette separated from background` |
| 모티베이티드 프랙티컬 | `motivated practicals in frame (window/neon/lamp) driving the key; natural high-contrast` |
| 색코드 억압 | `cold blue low-key, high contrast, oppressor side slightly high-key` |
| 색코드 해방 | `warm amber backlight, golden rim, released/liberated mood` |
| 타임라인 과거(웜) | `warm amber/sepia grade, heavy 35mm film grain, tungsten practicals — PAST timeline signature` |
| 타임라인 현재(콜드) | `cold cyan-blue grade, clean fluorescent, low grain — PRESENT timeline signature` |

> **"원하는 작품명" 처리:** 작품의 조명 **원리만**(방향·대비·색온도·질감) 언어화해 위 조각으로 변환. **특정 장면의 구도·소품·인물 복제 금지**(표절 경계 — `07`/규칙 4).
> **공간 색온도 고정(S23-2):** 공간마다 위 조각 중 하나를 배정해 `global_look.json`에 박제 — 컷만 바뀌어도 감정 좌표가 읽히게. 타임라인 색코드는 과거/현재(또는 꿈/현실)를 자막 없이 0.5초에 판별시키는 장치.
> **의상 색 아크 연동(S19·S22):** 인물 의상 색 아크와 조명 색코드는 같은 방향으로 이동해야 한다 — 씬 프롬프트에 해당 비트의 의상 단계(`wardrobe stage 1|2|3 from the sheet`)를 명시.

---

## ★ 렌즈 문법 조각 (S21-3 — 씬 심리 → mm·구도) 🎬 비전: Part 2·4

| 의도 | 프롬프트 조각 |
|---|---|
| 광각 소외·왜곡 | `shot on 16mm wide angle, edge distortion, subject dwarfed by vast space, isolation` |
| 광각 영웅화 | `low-angle wide shot, subject looms, converging verticals, dynamic power` |
| 표준 정직 | `50mm lens, eye-level, natural proportions, no distortion, honest documentary gaze` |
| 망원 압축·관음 | `200mm telephoto, background compression, voyeuristic distance, subject isolated from crowd` |
| 망원 침투 CU | `85mm telephoto extreme close-up, razor-thin focus on the eyes, psychological intimacy` |
| Z축 레이어링 | `blurred foreground object framing the shot, subject sharp in middleground, hazy background depth` |
| 프레임 속 프레임 | `viewed through a slightly open door / window / mirror, dark frame edges, trapped composition` |
| 1점 투시 | `one-point perspective, symmetrical corridor, leading lines to a single vanishing point` |
| 다다미 샷 | `camera at 70cm tatami height, locked-off static, contemplative equal gaze, quiet domestic realism` |
| 버즈아이 | `true top-down bird's-eye view, camera perpendicular to the ground, subject small in a maze-like pattern` |
| 얕은 심도 강제 | `focus falloff is very fast, only a thin plane is sharp, creamy bokeh, background melt` |
| 딥 포커스 강제 | `deep focus, everything sharp from foreground to background, f/11–16, layered readable composition` |

## ★ 그레이딩 스톡 조각 (S23 — 룩을 한 단어로) 🎬 비전: Part 3

| 룩 | 프롬프트 조각 | 어울림 |
|---|---|---|
| 웜 포트레이트 필름 | `warm natural skin tones, creamy highlight roll-off, pastel palette, soft fine grain (Portra-style)` | 인물 감성·일상 |
| 텅스텐 야경 필름 | `tungsten-balanced night look, neon halation glow, cool shadows with red bloom, grainy (800T-style)` | 도시 야경·네온 |
| 블리치 바이패스 | `bleach-bypass look, desaturated, harsh contrast, gritty metallic texture` | 전쟁·재난·거침 |
| 테크니컬러 | `saturated bold primary colors, theatrical heightened reality, glossy classic-musical vibrance` | 뮤지컬적 비현실·꿈 |
| 틸앤오렌지 | `teal and orange grade, warm skin vs cool background separation` | 인물 분리·상업 룩 |

> **한 프로젝트에 스톡은 하나**(전역 그레이드와 충돌 금지 — 씬 오버라이드는 색코드·타임라인 룰만).

## ★ 푼크툼 · Atmosphere 라인 (S23 — 필요한 씬에 추가) 🎬 비전: Part 1

```text
PUNCTUM DETAIL: include ONE small unexplained imperfection that pricks the viewer — e.g. a cracked lens of glasses, a single child's rain boot overturned in a puddle, a fingerprint on a photo's corner. It must stay incidental (never centered, never explained).
ATMOSPHERE (write HOW, not WHAT): describe the air of the space — temperature, humidity, density, tension (e.g. "the cold damp air of rain-soaked asphalt, lonely 3am stillness") — not just the objects in it.
IMPERFECT REALISM (스투디움 탈피): unretouched, visible pores, raw beauty documentation, asymmetry allowed — never an averaged flawless face.
```

## ★ 무브 동기 사전 조각 (S27-3 — 영상 프롬프트용) 🎬 비전: Part 5

| 동기 | 프롬프트 조각 |
|---|---|
| 푸시인(감정 진입) | `slow push-in toward the face, creeping closer, rising emotional intensity` |
| 풀아웃(고립·엔딩) | `slow pull-out revealing the vast empty surroundings, subject shrinking, abandonment` |
| 리빌(정보 공개) | `sliding/truck move from behind a foreground wall, revealing the hidden …` |
| 랙 포커스(주도권 이동) | `rack focus shifting from the foreground subject to … behind, silent revelation` |
| 돌리 줌(공황) | `dolly-zoom (vertigo effect), background stretching while subject stays, reality collapsing` |
| 핸드헬드(날것) | `handheld, breathing camera, urgent documentary energy` |
| 스테디캠(우아·몽환) | `smooth gimbal glide, dreamlike floating flow` |
| 슬로모(감정 확대) | `extreme slow motion, high-speed-camera feel, a split second dilated` |
| 불릿타임(전지) | `frozen moment, time stands still, camera orbiting the static subject` |
| 리버스(후회·꿈) | `reverse motion, entropy flowing backwards, dream logic` |

> 사용법: 씬 감정 → 동기 선택 → 조각을 규칙0[B] 뒤에 합침. **동기 없는 무브 금지. "Move" 대신 구체 동사(tremble/glide/soar).**

## ★ 미술·조명 정밀 질문 카드 (S18-2 · S23 — 평범한 배경 방지)

생성 전 반드시 아래를 물어 특색 있는 배경을 만든다:
1. **지배색 1 + 액센트 보색 1** — 컬러 밸런스의 축. (예: 청록 공간 + 주황 광원 / 회녹 + 핏빛 소품)
2. **컬러 콘트라스트 전략** — 인물 의상색 ↔ 배경색 대비로 인물 분리. (알버스: 인물을 튀게 하려면 배경색을 바꿔라.)
3. **색채 대비 유형(이텐)** — 이 씬의 감정에 맞는 대비는? 보색(갈등·강렬) / 한난(감성적 거리) / 명도(느와르·실루엣).
4. **전경-중경-후경 소품** — 데드스페이스 금지(자막 여백은 예외). 전경 흐림 = 훔쳐보기 몰입.
5. **질감·환경(Atmosphere)** — 빛샘·먼지·습기·반사·낡음 중 무엇으로 평범을 깨나. **What이 아니라 How로**(공간의 온도·밀도·공기).
6. **상징 소품** — SCENARIO_BIBLE의 셋업/페이오프 오브제를 어디에 심나.
7. **푼크툼 디테일** — 이 씬에서 관객을 '찌를' 설명되지 않는 작은 이물감 1개는? (완벽·매끈 금지.)
8. **공간 일관성** — 반복 장소는 공간 plate를 먼저 확정해 ref 락(S23-2).

---

## 크로스 엔진 노트

- 이미지: `nano_banana_2`(인물 일관성) · `gpt_image_2`(캐릭터 시트·텍스트·정보 구도) · `seedream-4`/Magnific NB(포토리얼 질감) · 나노바나나-라이트(480p 초벌). 호출 전 `models_explore(action='get')`/`models_list`로 resolution 라벨·medias role 확정.
- 영상: `kling3_0`(연기·모션) · `seedance_2_0`(카메라 무브·전환). 720p/1080p. start-image = 캐릭터 락 본 이미지.
- 음성: ElevenLabs voice_id 락(S26). 영상 클립은 SFX only, 대사는 후반 더빙.

## ★ MODE 파라미터 표 (S0-B 품질 모드 → 생성 호출 기본값)

| 호출 | QUALITY(최고 품질) | ECO(가성비) |
|---|---|---|
| 캐릭터 시트 | 3안 · 2k | 1안 · 1k~2k |
| 480p 프리뷰 | 전 씬(동일) | 전 씬(동일) |
| 본 이미지 | 씬당 2안(엔진 병렬 가능) · 2k | 씬당 1안 · 1k~2k |
| 업스케일 | 주요 컷 적극 | 최종 채택 컷만 |
| 영상 | 1080p 직행 · 피크 씬 2테이크 | 720p 초벌 → 컨펌 컷 `video_upscale` 1080p화(테이크 보존) · 미달 컷만 재생성 |
| 음성 샘플 | 후보 4 + 립싱크 테스트 | 후보 2 · TTS만 |

> 공통(모드 무관): 프리뷰 승인 없이는 호출 금지 · 배치 전 비용 견적 · 진단 없는 재생성 금지 · resumable · 재시도 상한(네트워크 3회, 필터 2회). — `00_core` [크레딧 절약 공통 규칙]
