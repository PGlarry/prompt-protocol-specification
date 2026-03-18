# PPS — 프롬프트 프로토콜 사양

<div align="center">

**[English](README.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md)**

[![License: MIT](https://img.shields.io/badge/Tools-MIT-blue.svg)](LICENSE)
[![Docs: CC BY 4.0](https://img.shields.io/badge/Docs-CC%20BY%204.0-green.svg)](spec/PPS-1.0/IP_NOTICE.md)
[![Version](https://img.shields.io/badge/PPS-v1.0.0-orange.svg)](spec/PPS-1.0/standard.md)
[![Status](https://img.shields.io/badge/Status-Community%20Specification-brightgreen.svg)](STATUS.md)

*인간-AI 상호작용을 위한 오픈 8차원 구조적 명령 프레임워크*

</div>

---

<div align="center">

### 체험하기 · 책 읽기 · 사양 탐색

| | |
|---|---|
| **5W3H 플랫폼** | [https://www.lateni.com](https://www.lateni.com) — 라이브 구현, 온라인으로 PPS 엔벨로프를 설계하세요 |
| **도서** | [*Super Prompt: 5W3H — A Comprehensive Guide to Designing Effective AI Prompts Across Domains*](https://www.amazon.com/dp/B0F3Z25CHC)<br>Gang Peng · Amazon KDP · 2025년 4월 · ASIN: B0F3Z25CHC |

</div>

---

## PPS란 무엇인가?

자연어 프롬프트는 **의도 전달 손실** 문제를 겪습니다 — 사용자가 실제로 필요로 하는 것과 AI 시스템에 전달하는 것 사이의 격차입니다. PPS(프롬프트 프로토콜 사양)는 AI 명령을 위한 구조적이고 기계 검증 가능한 엔벨로프를 제공하여 이 문제를 해결합니다.

PPS는 **5W3H 모델**을 기반으로 합니다: *What(무엇을), Why(왜), Who(누가), When(언제), Where(어디서), How-to-do(어떻게), How-much(얼마나), How-feel(어떤 느낌으로)* — 모든 AI 작업을 완전히 명세하는 8가지 차원입니다.

```json
{
  "pps_header": {
    "pps_version": "PPS-v1.0.0",
    "model": { "name": "gpt-4o", "digest": "sha256:abc123", "data_cutoff": "2025-01-01" },
    "decode": { "seed": 42, "temperature": 0.7, "top_p": 0.95 },
    "locale": "ko-KR"
  },
  "pps_body": {
    "what": { "task": "한국 EV 시장의 경쟁 분석 보고서 작성" },
    "why": { "goals": ["전략적 투자 의사결정 지원"], "constraints": ["no_pii"] },
    "who": { "persona": "시니어 산업 분석가", "audience": ["C-레벨 임원진"] },
    "when": { "timeframe": "2024년 데이터, 현재 시장 스냅샷" },
    "where": { "environment": "이사회 프레젠테이션", "jurisdiction": "KR" },
    "how_to_do": { "paradigm": "CoT", "steps": ["시장 규모 산정", "포터의 5가지 경쟁력 분석", "상위 5개 기업", "트렌드 전망"] },
    "how_much": { "content_length": "2000단어", "structure_elements": "표 포함 5개 섹션", "detail_richness": "10개 이상 데이터 포인트" },
    "how_feel": { "tone": "전문적", "style": "데이터 중심", "audience_level": "전문가" }
  },
  "pps_integrity": {
    "canonical_hash": "sha256:TO_BE_FILLED_AFTER_CANONICALIZATION"
  }
}
```

---

## 왜 PPS인가?

통제된 실험의 실증 결과 (60개 주제 × 3개 LLM × 3가지 조건, 540개 출력):

| 지표 | 단순 프롬프트 (A) | PPS 렌더링 (C) | 개선율 |
|------|:----------------:|:--------------:|:------:|
| **goal_alignment** | 4.34 | **4.61** | *p* = 0.006, *d* = 0.374 |
| 필요한 후속 프롬프트 수 | ~3.3회 | ~1.1회 | **−66%** |
| 첫 번째 시도 정확도 | — | **85%** 첫 번째 확장에서 정확 | — |

> 전체 방법론 및 결과: [논문 (arXiv)](https://arxiv.org/abs/PENDING) · [실험 데이터](experiments/)

**핵심 인사이트**: 기존 LLM 평가 지표는 *제약 조건 점수 비대칭* 으로 인해 A > C로 나타납니다 — 제약 조건이 없는 프롬프트는 제약 준수에서 완벽한 점수를 쉽게 받습니다. 사용자 의도 정렬(`goal_alignment`)으로 평가할 때, 구조화된 PPS 프롬프트는 특히 고모호성 도메인(비즈니스: *d* = 0.895)에서 단순 프롬프트를 크게 능가합니다.

---

## 저장소 구조

```
prompt-protocol-specification/
├── spec/
│   └── PPS-1.0/
│       ├── standard.md          # 규범적 사양 (중문)
│       ├── standard.en.md       # 규범적 사양 (영문)
│       ├── standard.ja.md       # 규범적 사양 (일문)
│       ├── best-practices.md    # 구현 가이드
│       ├── conformance.md       # 적합성 수준
│       ├── security-privacy.md  # 보안 및 GDPR 요구사항
│       ├── versioning.md        # 버전 정책
│       ├── benchmark.md         # 벤치마크 방법론
│       ├── registry.md          # 제어 어휘
│       └── IP_NOTICE.md         # IP 공지
├── schema/
│   ├── pps-1.0.schema.json      # JSON 스키마 (엄격)
│   └── pps.schema.json          # JSON 스키마 (기본)
├── spec/examples/               # 주석이 달린 예시 엔벨로프
├── tests/pps-conformance/       # 적합성 테스트 슈트 (Node.js)
├── tools/
│   └── pps-verify.js            # CLI 검증 도구
├── STATUS.md                    # 사양 로드맵 및 거버넌스
└── PUBLISHING.md                # 릴리즈 및 DOI 가이드
```

---

## 빠른 시작

**엔벨로프 검증:**
```bash
node tests/pps-conformance/validate.js spec/examples/minimal.json
```

**전체 적합성 검사 실행:**
```bash
node tests/pps-conformance/summary.js
```

**정규 해시 계산:**
```bash
node tools/pps-verify.js spec/examples/minimal.json
```

**요구사항:** Node.js ≥ 16

---

## 적합성 프로파일

PPS는 `header.compliance`에 선언되는 세 가지 적합성 수준을 정의합니다:

| 프로파일 | `why.goals` | `who.audience` | `how_to_do.steps` | `how_much` 필드 |
|---------|:-----------:|:--------------:|:-----------------:|:---------------:|
| `strict` | ≥ 4 | ≥ 4 | ≥ 6 | ≥ 3 |
| `balanced` | ≥ 3 | ≥ 3 | ≥ 5 | ≥ 2 |
| `permissive` | ≥ 2 | ≥ 2 | ≥ 4 | ≥ 1 |

---

## 인용

학술 연구에서 PPS를 사용하는 경우 다음과 같이 인용해 주세요:

```bibtex
@article{peng2026pps,
  title     = {PPS: Structured Intent Transmission — An Empirical Study of a
               5W3H-Based Prompt Protocol for Human-AI Interaction},
  author    = {Peng, Gang},
  year      = {2026},
  note      = {arXiv preprint, cs.HC},
  url       = {https://github.com/PGlarry/prompt-protocol-specification}
}
```

---

## 관련 자료

- **5W3H 플랫폼**: [https://www.lateni.com](https://www.lateni.com) — 라이브 구현, 온라인으로 PPS 엔벨로프를 설계하세요
- **도서**: [*Super Prompt: 5W3H — A Comprehensive Guide to Designing Effective AI Prompts Across Domains*](https://www.amazon.com/dp/B0F3Z25CHC)
  Gang Peng · Amazon KDP · 2025년 4월 · ASIN: B0F3Z25CHC

---

## 라이선스

- **사양 문서** (`spec/`): [CC BY 4.0](spec/PPS-1.0/IP_NOTICE.md) — 출처 표시 후 자유롭게 사용, 공유, 개작 가능
- **도구 및 테스트** (`tools/`, `tests/`): [MIT](LICENSE)
- **개방성**: PPS와 5W3H는 완전히 개방되어 있습니다 — 특허 출원 없음. 누구나 자유롭게 구현하고 상업화할 수 있습니다. [IP_NOTICE.md](spec/PPS-1.0/IP_NOTICE.md) 참조.

---

<div align="center">
<sub>Created by <a href="https://www.lateni.com">Gang Peng</a> · Huizhou University · Huizhou Lateni AI Technology Co., Ltd.</sub>
</div>
