# Korean Word-Order MT Robustness — Evaluation Scripts

한국어 어순 변형에 대한 LLM 번역 강건성 실증 연구의 평가 스크립트입니다.
데이터셋: https://huggingface.co/datasets/YMmim/korean-word-order-mt-robustness

## Scripts

| 파일 | 역할 |
|---|---|
| `split_dataset.py` | 데이터셋을 dev/test로 층화 분할 (seed=42, dev 0.3) |
| `make_label.py` | 대상 모델로 원문·변형문을 번역해 라벨링용 CSV 생성 |
| `apply_label.py` | 사람이 입력한 gold 라벨을 데이터셋에 반영 |
| `analyze.py` | 카테고리별 변형 관계 위반율 집계 |
| `extract_fails.py` | 위반 사례 추출 (어순 vs 오역 분류용) |
| `run_eval.py` | (참고) 지표별 위반 판정 성능 비교 |

## Requirements# korean-word-order-mt-robustness
korean-word-order-mt-robustness


## Target Model

평가에 사용한 대상 모델: `Qwen/Qwen2.5-1.5B-Instruct` (그리디 디코딩)

## Pipeline

1. `split_dataset.py` — dev/test 분할
2. `make_label.py` — 번역 생성 → CSV
3. (사람이 CSV에 gold 라벨 입력)
4. `apply_label.py` — 라벨 반영
5. `analyze.py` / `extract_fails.py` — 결과 분석

## Citation

데이터셋 및 논문 인용 정보는 Hugging Face 데이터셋 카드를 참조하십시오.

## License

MIT
