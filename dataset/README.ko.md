# PPS-Bench：의도 정렬 연구를 위한 다국어 병렬 프롬프트 데이터셋

**[English](README.md) | [中文](README.zh.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Español](README.es.md)**

---

## 개요

PPS-Bench는 **인간-AI 상호작용에서의 구조화된 의도 전달**을 연구하기 위한 오픈 다국어 벤치마크 데이터셋입니다. 3가지 언어, 6가지 프롬프트 형식, 3개의 AI 모델, 3개의 작업 도메인에 걸친 병렬 프롬프트를 제공하며, 각 레코드에는 목표 정렬(GA) 평가 점수가 포함되어 있습니다.

---

## 데이터셋 통계

| 차원 | 세부 정보 |
|------|----------|
| 총 레코드 수 | **4,440건** |
| 언어 | ZH(중국어), EN(영어), JA(일본어) |
| 프롬프트 조건 | 6가지 (A / B / C / D / E / F) |
| AI 모델 | Claude (claude-sonnet-4-20250514), GPT-4o, Gemini 2.5 Pro |
| 작업 도메인 | 여행, 비즈니스, 기술 |
| 도메인당 작업 수 | 20건 |
| 평가 지표 | 목표 정렬 점수 (1~5점, DeepSeek-V3 평가) |

---

## 6가지 프롬프트 조건

| ID | 이름 | 설명 |
|----|------|------|
| **A** | 단순 프롬프트 | 한 문장 작업 설명 (기준선) |
| **B** | 구조화 JSON (PPS 원시) | 렌더링 없는 원시 PPS JSON |
| **C** | 수동 5W3H (자연어) | 수동 작성된 5W3H 자연어 버전 |
| **D** | AI 확장 5W3H (PPS 완전판) | [lateni.com](https://lateni.com)의 AI 의도 확장으로 생성한 8차원 완전 PPS 프롬프트 |
| **E** | CO-STAR | CO-STAR 프레임워크로 구조화된 프롬프트 |
| **F** | RISEN | RISEN 프레임워크로 구조화된 프롬프트 |

---

## 파일 구조

```
dataset/
├── data/
│   ├── pps_bench_zh.jsonl      ← 중국어 1,080건
│   ├── pps_bench_en.jsonl      ← 영어 1,080건
│   ├── pps_bench_ja.jsonl      ← 일본어 1,080건
│   └── pps_bench_full.jsonl    ← 전체 3,240건
└── statistics/
    └── summary.json
```

---

## 주요 결과

| 조건 | 전체 평균 GA |
|------|------------|
| A (기준선) | 4.463 |
| B (원시 JSON) | 4.141 |
| C (수동 5W3H) | 4.683 |
| D (AI 확장 5W3H) | 4.930 |
| E (CO-STAR) | 4.978 |
| F (RISEN) | 4.983 |

**핵심 발견**: 구조화 프롬프트(D/E/F)는 언어 간 점수 분산을 최대 24배 감소시켜(σ: 0.470 → 0.020) 언어 독립적 의도 전달을 입증했습니다.

---

## 인용

```bibtex
@dataset{pps_bench_2026,
  title     = {PPS-Bench: A Multilingual Parallel Prompt Dataset for Intent Alignment Research},
  author    = {[저자]},
  year      = {2026},
  url       = {https://github.com/PGlarry/prompt-protocol-specification}
}
```

---

## 라이선스

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 라이선스로 공개됩니다.
