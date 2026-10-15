# 모션 인트로 (코드로 렌더)

videointro 스킬로 만든 인트로 영상의 소스입니다. 사진 없이 캔버스 코드로 그리고, 음악도 코드로 합성했습니다.

| 폴더 | 내용 | 결과 |
|---|---|---|
| `autumn/` | 가을 여행 세로 쇼츠 인트로, 15초, 하우스(밝게), 128 BPM | `autumn/build/autumn-trip-shorts.mp4` |

## 다시 만들기
```bash
cd motion/autumn
python3 <스킬>/scripts/compose.py --genre house --mood bright --structure classic --length 15 \
  --texture vinyl --breaker ding --seed 1015 --out build --history ../intro_history.json
HTML=shorts.html node ../render.mjs build/autumn-trip-shorts.mp4
```

## 쇼츠 편집기에 붙이기
`autumn-trip-shorts.mp4`를 `tools/shorts-editor/motion/`에 복사하고 `settings.json`의 `"앞영상"`에 파일 이름을 적습니다.

글꼴: Pretendard(SIL OFL), Archivo, JetBrains Mono.
