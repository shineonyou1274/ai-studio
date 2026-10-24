# 외부 AI 작업 지시서 — 소울체인지 <N>화 <컷/작업 이름>

이 지시서는 클라우드 스튜디오(편집장)가 PC 쪽 AI에게 넘기는 작업입니다. 받은 AI는 아래만 하고, 결과를 지정한 위치에 올린 뒤 보고합니다.

## 0. 먼저 읽을 것
- `C:\Users\경남교육청\youtube-ops\series\_soulchange_kit\소울체인지_제작규칙.md`
- 같은 폴더 `캐릭터_음성_설정.md`

## 1. 할 일
- 도구: <Dreamina Seedance 2.5 / Kling (사장님 계정)>
- 컷 수: <n>개, 컷당 5초, 세로 9:16, 소리 끔(배경음 금지)

## 2. 컷별 지시
| 컷 | 첨부할 참조 이미지(키트 경로) | 프롬프트(그대로 붙여 넣기) | 저장 파일명 |
|---|---|---|---|
| c1 | `characters\담임_refT.png` | (공통 머리말 + 본문) | `ep<N>\clips\c1.mp4` |

공통 머리말(모든 프롬프트 맨 앞, 글자 그대로):
"Keep the exact face, hair and clothing from the reference image; no identity drift. Vertical 9:16 realistic Korean school drama. No background music, no music, no score. No text, no captions, no on-screen UI."

## 3. 확인 기준 (생성 직후 직접 보고, 어긋나면 한 번만 다시 생성)
- 얼굴·머리·옷이 참조 이미지와 같은가
- 아무도 카메라를 보지 않는가, 입을 다물어야 하는 컷에서 입이 움직이지 않는가
- 화면에 글자가 생기지 않았는가
- 2번 다시 해도 안 되면 멈추고 그 사실과 원인 추측을 보고

## 4. 결과 올리기
- 저장: `C:\Users\경남교육청\youtube-ops\series\_soulchange_kit\episodes\ep<N>\clips\`
- 쓴 크레딧과 실제 사용 프롬프트를 `episodes\ep<N>\생성로그.md`에 적기
- `git add series/_soulchange_kit/episodes/ep<N> && git commit -m "<N>화 컷" && git push` (100MB 넘는 파일은 빼고 보고)
