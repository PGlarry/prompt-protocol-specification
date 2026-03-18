---
title: Prompt Protocol Standard (PPS) v1.0 — 모범 사례 (참고 정보)
lang: ko
status: draft
version: 1.0.0
---

# 1. 설계 가이드라인
- **What**을 기반으로: 한 문장 작업 + 구조화된 KPI.
- **Why**를 제약 열거로: 기계 판독 가능한 짧은 구문 ("외부 브라우징 금지", "인용 필수", "개인정보 보호 정책" 등).
- **Who** 역량 허용 목록: 사용 가능한 도구 이름만 선언하고, 미선언 역량은 기본적으로 거부됩니다.
- **When** 시간 정책: `timeframe` 또는 `validity_window`를 제공하고 `staleness_policy`를 선언합니다 (예: "만료 시 거부 / 품질 저하 처리").
- **Where** 증거 & 환경: `environment`를 고정합니다. `citations_required=true`일 때 `evidence` (uri, digest, title)를 제공하고 관리 자료를 우선합니다. 필요시 `jurisdiction`을 명시합니다. 외부 링크 콘텐츠는 주입 방지를 위해 인라인화하거나 플레이스홀더로 대체합니다.
- **How-to-do** 투명성: 단계별 또는 패러다임 레이블 (ReAct / CoT / ToT).
- **How-much** 콘텐츠 중심 정량화: `content_length` (분량), `structure_elements` (단락/장/모듈), `detail_richness` (세부 밀도), `quality_guidance` (품질 기준), `cultural_depth` (문화/깊이). 토큰/시간/비용과 같은 시스템 계층 의미론은 피합니다.
- **How-feel** 스타일: 레지스터, 청중 수준.

팁: `how_many`는 사용하지 말고 모든 정량화를 `how_much` 안에서 표현합니다.

## 1.1 최소 8차원 템플릿 (복사 가능)
```json
{
  "header": {
    "pps_version": "PPS-v1.0.0",
    "model": { "name": "<model>", "digest": "sha256-<digest>", "data_cutoff": "2024-01-01" },
    "decode": { "seed": 1, "temperature": 0, "top_p": 1 },
    "locale": "ko-KR",
    "implementation": { "vendor": "local", "version": "1.0.0", "filled_fields": [], "defaults_profile": "strict" }
  },
  "body": {
    "what": { "task": "<핵심 작업>", "output_schema": { } },
    "why": { "goals": ["<목표>"], "constraints": ["use_provided_evidence", "no_external_browse"] },
    "who": { "persona": "<역할>", "capabilities": ["json_output"] },
    "when": { "timeframe": "이번 주" },
    "where": { "environment": "prod", "citations_required": true, "evidence": [] },
    "how_to_do": { "paradigm": "ReAct", "steps": ["증거 읽기", "출력 통합"], "tools": [] },
    "how_much": { "content_length": "800-1200자", "structure_elements": "3-4단락", "detail_richness": "5-8 핵심 포인트" },
    "how_feel": { "tone": "공식적", "style": "간결한", "audience_level": "mixed" },
    "how_interface": { "format": "json", "schema": {} }
  },
  "integrity": { "canonical_hash": "" }
}
```

# 2. 재현성
- `seed/temperature/top_p/stop`을 고정하고 입력 증거를 정규화합니다. 외부 검색의 경우 URI + 다이제스트로 앵커합니다.

# 3. 보안 & 준수
- URL 주입: 실행 가능한 외부 링크가 아닌 인용 지향 콘텐츠를 생성합니다. `http(s)`를 명시적으로 제거하거나 플레이스홀더로 대체합니다.
- 도구 초과 권한: 역량과 도구를 분리하고 먼저 선언한 후 사용합니다. CI에 초과 권한 테스트 케이스를 추가합니다.
- GDPR: `who.policy`에 `no_pii`를 표시하고 출력 측에서 익명화 규칙을 적용합니다.

# 4. 자가 점검 & 자동 수정
- 자가 점검기: 생성 후 스키마 / 정책 / 자가 점검을 실행합니다. 실패 시 자동 수정으로 진입합니다 (충돌 도구 비활성화, 증거 보충, 정책 주입).
  - 규칙 예: `gdpr ⇒ no_pii`, `citations_required ⇒ evidence≥1`, `no_external_browse ⇒ url_removed + tools-{web_browse}`.

## 4.1 반복적 개선 및 잠금 (실습)
- `how_meta.governance.locks`에 잠금 경로를 표시합니다 (예: `/body/where`). 턴/모델에 걸쳐 변경하지 않고 잠금 해제된 필드에만 개선적 재작성을 적용합니다.
- `header.implementation.origins`에 출처를 기록합니다: `user`는 최고 우선순위로 기본 잠금됩니다. `ai:*`는 모델 기여를 추적합니다.

# 5. 구성 & 파이프라인
- 다단계는 `P2 ∘ P1`로 연결합니다. 각 단계는 자체 `canonical_hash`와 예산을 유지하고 집계 전에 중복 제거 및 버전 잠금을 수행합니다.

# 6. 버전 관리
- `PPS-vMAJOR.MINOR.PATCH`를 사용합니다. MAJOR는 파괴적 변경의 경우에만 증가합니다. 예제와 CI는 대상 버전을 태그합니다.
