---
title: Prompt Protocol Specification (PPS) v1.0 — 규범적 사양 (한국어)
status: community-specification
version: 1.0.0
lang: ko
---

**Language / 语言 / 言語 / 언어 / Idioma**：[中文](standard.md) · [English](standard.en.md) · [日本語](standard.ja.md) · [한국어](standard.ko.md) · [Español](standard.es.md)

---

## 목차

| 섹션 | 내용 |
|------|------|
| [§1](#1-범위) | 범위 |
| [§2](#2-용어) | 용어 |
| [§3](#3-데이터-모델-규범적-스키마) | 데이터 모델 (8차원) |
| [§4](#4-헤더-필수) | 헤더 |
| [§5](#5-바디-필수) | 바디 |
| [§6](#6-무결성-필수) | 무결성 |
| [§7](#7-결정론--재생) | 결정론 & 재생 |
| [§8](#8-보안--컴플라이언스) | 보안 & 컴플라이언스 |
| [§9](#9-적합성) | 적합성 |
| [§10](#10-버전-관리) | 버전 관리 |
| [§11](#11-상호운용성-프로파일) | 상호운용성 프로파일 |
| [§12](#12-참조-구현-참고-정보) | 참조 구현 |
| [부록 A](#부록-a-참고-정보-제어-제약-어휘) | 제약 어휘 |
| [부록 B](#부록-b-참고-정보-pps-콘텐츠-프로파일--엄격성-임계값) | 적합성 임계값 |
| [부록 C](#부록-c-참고-정보-최소-상호운용-가능-예시) | 최소 예시 |
| [부록 D](#부록-d-참고-정보-검증-체크리스트) | 검증 체크리스트 |
| [부록 E](#부록-e-참고-정보-pps-qr-선택적-바인딩-사양) | PPS-QR 바인딩 |

---

# 1. 범위

이 사양은 인간-AI 상호작용 명령 프로토콜인 PPS(프롬프트 프로토콜 사양)의 최소 상호운용 가능한 구현을 정의합니다. 규범적 요구사항은 MUST / SHOULD / MAY (RFC 2119에 따름)로 표현되며 REQ 식별자를 가집니다.

# 2. 용어

- **엔벨로프**: 단일 상호작용을 위한 프로토콜 캐리어로 `header`, `body`, `integrity`로 구성됩니다.
- **정규화**: 안정적인 해시를 생성하기 위한 JSON의 결정론적 순서 지정 및 직렬화.
- **결정론적 디코딩**: 재현 가능한 재생을 가능하게 하는 고정된 디코딩 매개변수.

# 3. 데이터 모델 (규범적 스키마)

구현자는 `schema/pps-1.0.schema.json`을 준수하는 엔벨로프를 수락하고 생성해야 합니다 (REQ-001).

## 3.1 8차원 및 JSON 경로 (규범적 매핑)

- **REQ-100 (What)**: `body.what.task`를 MUST 제공해야 합니다. 출력이 구조화된 JSON인 경우 `body.what.output_schema`를 SHOULD 제공해야 합니다.
  - JSON 경로: `/body/what/{task, input_schema?, output_schema?}`

- **REQ-110 (Why)**: `body.why.goals`를 SHOULD 나열해야 합니다. 제약 조건은 제어 어휘 (부록 A)에서 SHOULD 가져와야 합니다. 예: `no_external_browse`, `citations_required`, `use_provided_evidence`.
  - JSON 경로: `/body/why/{goals?, constraints?}`

- **REQ-120 (Who)**: `persona`를 SHOULD 지정해야 합니다. 도구를 사용할 경우 `who.capabilities`에 MUST 허용 목록에 추가해야 합니다.
  - JSON 경로: `/body/who/{persona?, capabilities?, policy?}`

- **REQ-130 (When)**: `timeframe` 또는 `validity_window` 중 하나 이상을 MUST 제공해야 합니다.
  - JSON 경로: `/body/when/{timeframe?, validity_window?, staleness_policy?}`

- **REQ-140 (Where)**: `citations_required=true`인 경우 하나 이상의 `evidence` 항목을 MUST 제공해야 합니다. 증거는 `digest`와 `title`을 SHOULD 포함해야 합니다.
  - JSON 경로: `/body/where/{environment?, evidence[], jurisdiction?, citations_required?}`

- **REQ-150 (How-to-do)**: `paradigm`과 `steps`를 SHOULD 지정해야 합니다. 사용되는 `tools`는 REQ-181 (역량 제약)을 MUST 충족해야 합니다.
  - JSON 경로: `/body/how_to_do/{paradigm?, steps?, tools?}`

- **REQ-160 (How-much)**: 생성된 콘텐츠 자체를 대상으로 하는 정량적 요소를 SHOULD 지정해야 합니다 (예: 길이, 구조, 세부 밀도, 품질 지침, 문화적 깊이). 필드 이름은 개방형 집합이며 도메인별 키와 단위가 허용됩니다.
  - JSON 경로: `/body/how_much/{content_length?, structure_elements?, detail_richness?, quality_guidance?, cultural_depth?}`

- **REQ-161 (통합 정량화 컨테이너로서의 How-much)**: 이 사양은 *how much*와 *how many*를 별도의 차원으로 구분하지 않습니다. 모든 수량 및 리소스 관련 정량화는 `how_much`로 통합됩니다. 구현은 동의어 필드 (예: `how_many`)를 `how_much`로 매핑하여 MUST 정규화해야 합니다.

- **REQ-170 (How-feel)**: `tone`과 `style`을 SHOULD 지정해야 합니다. 특정 청중을 대상으로 하는 경우 `audience_level`은 열거형에서 MUST 가져와야 합니다.
  - JSON 경로: `/body/how_feel/{tone?, style?, audience_level?}`

- **REQ-175 (인터페이스 / 거버넌스)**: 출력 인터페이스가 JSON인 경우 스키마는 `what.output_schema` 또는 `how_interface.schema` 중 하나 이상에 MUST 나타나야 합니다.

## 3.2 부분 사양 및 자동 완성

- **REQ-340**: `what.task`는 사용자가 MUST 제공해야 하는 최소 입력입니다.
- **REQ-341**: 나머지 7개 차원은 생략하거나 부분적으로 생략 MAY 할 수 있습니다. 구현은 기본 정책, 검색 결과 또는 추론을 사용하여 채웁니다.
- **REQ-342**: 자동 완성이 발생하면 시스템은 완성되거나 덮어쓴 필드를 `header.implementation.filled_fields` (JSON 포인터 배열로)에 MUST 기록해야 하며, 사용된 기본 구성을 `header.implementation.defaults_profile`에 MAY 주석으로 달 수 있습니다.
- **REQ-343**: 자동 완성은 거버넌스 제약을 MUST NOT 위반해서는 안 됩니다.

---

# 4. 헤더 (필수)

- **REQ-010**: `PPS-vMAJOR.MINOR.PATCH` 형식의 `pps_version`을 MUST 포함해야 합니다.
- **REQ-011**: `model.name`, `model.digest`, `model.data_cutoff`를 MUST 지정해야 합니다.
- **REQ-012**: `decode.seed`, `decode.temperature`, `decode.top_p`를 MUST 지정해야 합니다. 결정론적 재생에는 `temperature=0`과 `top_p=1`을 사용합니다.
- **REQ-013**: `locale`을 MUST 지정해야 합니다. `header.created_at`은 생성 타임스탬프를 SHOULD 기록해야 합니다.

---

# 5. 바디 (필수)

- **REQ-020**: 8개의 평면 차원 모두를 MUST 포함해야 합니다: `what`, `why`, `who`, `when`, `where`, `how_to_do`, `how_much`, `how_feel`.
- **REQ-021**: `how_to_do`, `how_much`, `how_feel`은 형제 필드입니다. 도구는 해당 역량이 선언된 경우에만 사용 가능합니다.
- **REQ-022**: `where.citations_required=true`인 경우 하나 이상의 `evidence` 항목을 MUST 제공해야 합니다 (URI + digest 또는 title).

---

# 6. 무결성 (필수)

- **REQ-030**: `integrity.canonical_hash`를 MUST 채워야 합니다. 값은 엔벨로프를 정규 직렬화하고 SHA-256을 적용한 후 `sha256:`을 접두사로 붙여 계산합니다.

---

# 7. 결정론 & 재생

- **REQ-040**: 재생 시 헤더에서 `model.digest`와 `decode` 매개변수를 MUST 고정해야 합니다.
- **REQ-041**: 안정적인 잘라내기를 위해 `stop`을 SHOULD 지정해야 합니다.

## 7.1 재현성

- **REQ-300**: 엔벨로프는 MUST 정규화 가능해야 합니다. `body`, `header`, `integrity`에 대한 모든 변경은 해시를 변경합니다.
- **REQ-301**: 증거 재현성: `where.evidence[].uri`가 변경 가능한 리소스를 가리킬 때 `digest`와 `title` 스냅샷 필드도 SHOULD 제공해야 합니다.
- **REQ-302**: 디코드 재현성: `decode.seed`, `temperature`, `top_p`는 MUST 고정해야 합니다 (REQ-012 참조).
- **REQ-303**: 모델 재현성: `model.digest`는 MUST 특정 버전을 식별해야 합니다 (모델 가중치, 매개변수, 툴체인).
- **REQ-304**: 구현자는 재생 단계를 MUST 문서화해야 합니다: 정규화 → 검증 → 정책 검사 → 결정론적 디코드.

## 7.2 해시 안정성

- **REQ-305**: 동일한 엔벨로프의 여러 정규화는 MUST 동일한 `canonical_hash`를 생성해야 합니다 (멱등성).
- **REQ-306**: 정규화 알고리즘이 변경되면 `pps_version`을 MUST 올려야 합니다 (MAJOR 또는 MINOR).

## 7.3 정규화 알고리즘

크로스 플랫폼 일관성을 보장하기 위해 구현은 RFC 8785 (JCS — JSON 정규화 체계)와 호환되는 최소 구현을 SHOULD 채택해야 합니다:

- **입력**: 전체 엔벨로프. 정규화 전에 `integrity.canonical_hash`를 임시로 제거합니다.
- **문자열**: 표준 JSON 이스케이핑을 사용한 UTF-8 인코딩.
- **객체**: 사전 순서로 키를 정렬합니다.
- **배열**: 원래 순서를 유지합니다.
- **숫자**: 표준 JSON 표현 (후행 0 없음).
- **출력**: 정규화된 바이트 문자열의 SHA-256에 `sha256:` 접두사를 붙입니다.
- **쓰기 복귀**: 결과를 `integrity.canonical_hash`에 저장합니다.

참조 구현: `tests/pps-conformance/canonicalize.js`

## 7.4 재생 아티팩트

- **REQ-310**: 생성 시스템은 재생 기록 (타임스탬프, 호스트, 구현 버전)을 `header.implementation` 또는 외부 감사 로그에 SHOULD 기록해야 합니다.

---

# 8. 보안 & 컴플라이언스

- **REQ-050**: `header.compliance`에 `gdpr`이 있는 경우 `who.policy`에 `no_pii`를 MUST 명시적으로 포함해야 합니다.
- **REQ-051**: `why.constraints`가 외부 브라우징을 금지하는 경우 `web_browse` 또는 다른 외부 네트워크 도구를 MUST NOT 포함해서는 안 됩니다.
- **REQ-052**: `why.constraints`가 외부 브라우징을 금지하고 `what.task`에 `http(s)://` URL이 포함된 경우 이를 MUST 대체하거나 플래그 표시해야 합니다 (예: `[URL_REMOVED]`).
- **REQ-053**: `how_to_do.tools`의 모든 도구는 MUST `who.capabilities`에 나타나야 합니다 (역량 샌드박스).

## 8.1 교차 필드 불변 조건

- **REQ-180**: `where.citations_required=true` ⇒ 증거 항목 수 ≥ 1.
- **REQ-181**: `how_to_do.tools ⊆ who.capabilities`.
- **REQ-182**: `gdpr ∈ header.compliance` ⇒ `no_pii ∈ who.policy`.
- **REQ-183**: `no_external_browse ∈ why.constraints` ⇒ `web_browse ∉ how_to_do.tools`.

## 8.2 필드 잠금 및 반복적 개선

- **REQ-344**: 구현자는 `body.how_meta.governance.locks`에 JSON 포인터 목록을 MAY 제공하여 경로를 "쓰기 보호"로 표시할 수 있습니다.
- **REQ-345**: 구현자는 감사 목적으로 `header.implementation.origins`에 주요 필드의 출처를 SHOULD 기록해야 합니다.

## 8.3 AI 컴플라이언스 테스트 및 앵커링

- **REQ-346 (앵커 우선순위)**: 사용자 입력이 있거나 명시적 `locks`가 존재하는 경우 AI 재생성은 해당 경로를 앵커로 MUST 처리해야 하며 MUST NOT 덮어써서는 안 됩니다.
- **REQ-347 (잠금 운용 의미론)**:
  - 잠금 세분성: 모든 JSON 포인터 (스칼라, 객체 또는 배열).
  - 우선순위: `locks` > `origins` > 다른 개선 정책.
  - 잠금 해제 메커니즘: 사용자가 포인터를 명시적으로 제거하거나 UI 또는 API를 통해 `unlock=[...]`을 전달할 때만 경로를 덮어쓸 수 있습니다.
- **REQ-348 (일관성 제약)**: `why.constraints`가 외부 브라우징을 금지하는 경우 `how_to_do.tools`는 MUST NOT `web_browse`를 포함해서는 안 됩니다.
- **REQ-349 (교차 턴 검증)**: 구현자는 `locks` 지정 경로의 값이 변경되지 않았는지 확인하는 전/후 비교 도구를 SHOULD 제공해야 합니다.
- **REQ-350 (실패 처리)**: `locks` 또는 일관성 제약이 위반되면 시스템은 MUST 이전 값으로 롤백하고 위반 및 교정 이벤트를 기록해야 합니다.

---

# 9. 적합성

구현자는 다음 테스트를 MUST 통과해야 합니다:
1. JSON 스키마 검증 통과 (REQ-001).
2. 정책 검사 통과 (REQ-050/051 등).
3. 정규 해시 일관성: 동일한 엔벨로프는 항상 동일한 `canonical_hash`를 생성합니다.
4. 재현성 테스트: 동일한 입력과 디코드 전략이 플랫폼 전반에 걸쳐 일관된 출력을 생성합니다 (또는 정의된 허용 범위 내에서).

## 9.1 인간-AI 정렬

- **REQ-320**: `body.what.kpi`는 SHOULD 측정 가능한 지표 또는 수락 기준을 제공해야 합니다.
- **REQ-321**: `body.why.goals`와 `body.what.kpi`는 SHOULD 매핑 가능해야 합니다 (목표 → 지표).
- **REQ-322**: `how_much.quality_guidance` 또는 다른 측정 가능한 기준이 지정된 경우 정렬을 검증할 수 있도록 `what.output_schema` 또는 외부 평가 스크립트를 SHOULD 제공해야 합니다.
- **REQ-323**: `how_meta.governance.verification`은 SHOULD `schema_validate`와 `policy_check`를 포함해야 합니다.

---

# 10. 버전 관리

- **REQ-060**: `pps_version`은 시맨틱 버전 관리를 따릅니다. v1.0은 향후 v1.x 릴리즈에서 추가된 새 선택적 필드와 하위 호환됩니다.

---

# 11. 상호운용성 프로파일

- **REQ-070**: 최소 하위 집합은 위에 설명된 헤더 + 바디 + 무결성의 필수 필드로 구성됩니다. `how_meta`는 선택 사항입니다.

---

# 12. 참조 구현 (참고 정보)

이 사양 패키지에는 스크립트가 번들로 포함되어 있지 않습니다. 구현자는 엔지니어링 수준의 검증 및 벤치마킹을 위해 별도로 게시된 참조 구현 및 적합성 슈트를 MAY 사용할 수 있습니다. 권위 있는 링크와 버전 번호는 릴리즈 페이지를 참조하십시오.

---

# 부록 A (참고 정보): 제어 제약 어휘

| 설명 | 영어 키 |
|------|---------|
| 외부 브라우징 금지 | `no_external_browse` |
| 제공된 증거만 사용 | `use_provided_evidence` |
| 인용 필수 | `citations_required` |
| 개인 식별 정보 금지 | `no_pii` |

---

# 부록 B (참고 정보): PPS-콘텐츠 프로파일 & 엄격성 임계값

이 부록은 크로스 모델 재현성 향상을 위한 도메인 무관 콘텐츠 생성 임계값을 제공합니다. 주 사양을 수정하지 않으며 선택적 상호운용성 프로파일입니다.

## B.1 프로파일 선언

`header.compliance`에 선언:
- 프로파일: `pps-content` (또는 `pps-core`, `pps-analysis`, `pps-code`, `custom`)
- 엄격성: `strict` | `balanced` (기본값) | `permissive`
- 예시: `["pps-content", "balanced"]`

## B.2 구조 및 유형 요구사항 (이 프로파일 하에서)

- `body.what.task`는 MUST 비어있지 않은 문자열이어야 합니다.
- `body.who.audience`가 있는 경우 MUST 배열이어야 합니다.
- `body.how_to_do.steps`가 있는 경우 MUST 배열이어야 합니다.
- `body.how_much`는 5가지 정량화 요소를 SHOULD 채택해야 합니다:
  - `content_length` — 길이 / 규모
  - `structure_elements` — 구조 / 섹션 / 모듈
  - `detail_richness` — 세부 / 요소 밀도
  - `quality_guidance` — 품질 기준
  - `cultural_depth` — 문화적 맥락 / 참여 깊이

## B.3 최소 임계값 (엄격성별)

| 수준 | `why.goals` | `who.audience` | `how_to_do.steps` | `how_much` 요소 |
|------|:-----------:|:--------------:|:-----------------:|:---------------:|
| `strict` | ≥ 4 | ≥ 4 | ≥ 6 | 5 / 5 |
| `balanced` (기본값) | ≥ 3 | ≥ 3 | ≥ 5 | ≥ 3 / 5 |
| `permissive` | ≥ 2 | ≥ 2 | ≥ 4 | ≥ 2 / 5 |

`strict` 하에서 임계값 미충족은 SHOULD 오류로 보고되어야 합니다. `balanced` / `permissive` 하에서는 경고로 보고됩니다.

---

# 부록 C (참고 정보): 최소 상호운용 가능 예시 (balanced)

```json
{
  "header": {
    "pps_version": "PPS-v1.0.0",
    "model": {
      "name": "example-model",
      "digest": "sha256-model-xyz",
      "data_cutoff": "2025-01-01"
    },
    "decode": { "seed": 0, "temperature": 0, "top_p": 1 },
    "locale": "ko-KR",
    "compliance": ["pps-content", "balanced"],
    "created_at": "2025-10-01T12:00:00Z"
  },
  "body": {
    "what": { "task": "주제에 대한 구조화된 소개 작성" },
    "why": {
      "goals": [
        "핵심 개념 전달",
        "실행 가능한 정보 제공",
        "이해와 적용 촉진"
      ]
    },
    "who": {
      "persona": "전문 어시스턴트",
      "audience": ["초보자", "실무자", "의사결정자"]
    },
    "when": { "timeframe": "현재 주기, 단계적 제공" },
    "where": { "environment": "온라인 문서 및 일반 업무 환경" },
    "how_to_do": {
      "paradigm": "CoT",
      "steps": [
        "핵심 포인트 파악",
        "구조 정리",
        "내용 초안 작성",
        "검토 및 게시",
        "피드백 수집"
      ]
    },
    "how_much": {
      "content_length": "1000-1500자",
      "structure_elements": "제목과 요약이 있는 3-4개의 주요 섹션",
      "detail_richness": "필요한 경우 예시와 데이터가 있는 5-8개의 핵심 포인트",
      "quality_guidance": "논리적 흐름, 일관된 용어, 높은 가독성",
      "cultural_depth": "권위 있는 또는 업계 맥락에 대한 적절한 참조"
    },
    "how_feel": {
      "tone": "전문적이고 접근하기 쉬운",
      "style": "명확한",
      "audience_level": "intermediate"
    }
  },
  "integrity": {
    "canonical_hash": "sha256:TO_BE_FILLED_AFTER_CANONICALIZATION"
  }
}
```

---

# 부록 D (참고 정보): 검증 체크리스트

## D.1 구조 및 일관성

- [ ] JSON 스키마 검증 통과 (REQ-001)
- [ ] `body.what.task`가 비어있지 않음 (REQ-100)
- [ ] 있는 경우 `who.audience`가 배열임
- [ ] 있는 경우 `how_to_do.steps`가 배열임
- [ ] `where.citations_required=true` ⇒ `evidence` ≥ 1 (REQ-180)
- [ ] `how_to_do.tools ⊆ who.capabilities` (REQ-181)
- [ ] 제약 충돌: `no_external_browse` ⇒ `web_browse` 허용되지 않음 (REQ-183)

## D.2 품질 임계값 (엄격성별)

- **strict**:
  - [ ] `why.goals` ≥ 4
  - [ ] `who.audience` ≥ 4
  - [ ] `how_to_do.steps` ≥ 6
  - [ ] 5개의 `how_much` 요소 모두 채워짐 (5/5)
- **balanced** (기본값): 3 / 3 / 5 / 3
- **permissive**: 2 / 2 / 4 / 2

## D.3 재현성

- [ ] `decode.temperature=0`이고 `top_p=1` (결정론적, REQ-012)
- [ ] `integrity.canonical_hash`가 계산되어 저장됨 (REQ-030 / REQ-300)
- [ ] 재생 일관성을 위해 모델과 디코드 매개변수가 기록됨 (REQ-040 / REQ-302 / REQ-303)

## D.4 선택적 인터페이스 / 출력 구조

- [ ] `how_interface.schema`가 출력 형태를 제한하는 경우 값이 객체임
- [ ] 스키마가 `what.output_schema`에만 제공된 경우 런타임에 검증을 위해 `how_interface.schema`에 복사 MAY 할 수 있음 (REQ-175)

---

# 부록 E (참고 정보): PPS-QR 선택적 바인딩 사양 (바인딩 v1)

이 부록은 QR 코드를 통해 PPS 명령을 전달하기 위한 선택적 바인딩을 정의합니다. 주 사양을 수정하지 않습니다.

## E.1 목적

- 스캔 후 5W3H 명령 요약을 직접 읽을 수 있으며 무결성 검증에 필요한 정보와 함께 제공됩니다.
- 개인 식별 정보나 민감한 데이터가 포함되지 않습니다. `integrity.canonical_hash`가 유일한 무결성 앵커 역할을 합니다.

## E.2 페이로드 (UTF-8 일반 텍스트)

**MUST 포함:**
- `pps_version` (`header.pps_version`에서)
- `created_at` (`header.created_at`에서)
- `task` (`body.what.task`에서)
- `canonical_hash` (전체 값 `sha256:…`)
- `verification_hint` (예: "명령 무결성을 확인하기 위해 해시를 비교하세요")
- `instruction` (5W3H로 정리된 인간 읽기 가능한 명령 텍스트)

**SHOULD 포함:**
- `id_short`: `canonical_hash`의 고정 길이 잘라내기 (마지막 12-16자 권장)
- `provider_note`: 인간 읽기 가능한 노트

**MAY 포함:**
- `signature` / `public_key_id`: 구현이 서명을 사용하는 경우
- `retrieval_uri`: JSON 엔벨로프 검색을 위한 선택적 URI

권장 텍스트 레이아웃:
```
PPS 명령 인증서
작업: <task>
생성: <created_at>
명령 ID: <id_short>
검증: 명령 무결성을 확인하기 위해 해시를 비교하세요
PPS 버전: <pps_version>
전체 해시: <sha256:...>

=== 전체 명령 ===

What(무엇을):    ...
Why(왜):         ...
Who(누가):       ...
When(언제):      ...
Where(어디서):   ...
How-to-do(어떻게): ...
How-much(얼마나): ...
How-feel(어떤 느낌으로): ...

=== 사용 지침 ===
위 내용에 따라 작업을 완료해 주세요.
```

## E.3 인코딩 및 오류 수정

- 문자 인코딩: UTF-8 일반 텍스트.
- 오류 수정 수준: L 또는 M. 콘텐츠가 너무 긴 경우 인간 읽기 가능한 설명은 적당히 압축 MAY 할 수 있지만 5W3H 제목 키는 MUST NOT 제거해서는 안 됩니다.

## E.4 보안 및 프라이버시

- 개인 식별 정보, 키, 액세스 토큰 또는 기타 민감한 데이터를 MUST NOT 포함해서는 안 됩니다.
- `id_short`는 비민감 식별자입니다. 엄격한 검증은 `canonical_hash`를 재계산하고 비교하는 것에 의존합니다.

## E.5 검증 흐름 (스캐너 측)

1. `canonical_hash`와 5W3H 명령을 읽습니다.
2. 명령에서 최소 엔벨로프를 재구성합니다 (또는 `retrieval_uri`를 통해 JSON 엔벨로프를 검색합니다).
3. 정규 직렬화를 수행합니다 (`integrity` 제거, 객체 키를 사전순으로 정렬, JSON 압축).
4. SHA-256을 계산하고 `canonical_hash`와 비교합니다.
5. 일치 → 검증 통과.

## E.6 버전 관리

- 바인딩 버전: `PPS-QR 바인딩 v1`.
- 바인딩 형식에 선택적 필드를 추가하는 것은 기존 구현과 하위 호환됩니다. MUST 필드는 변경되지 않습니다.
