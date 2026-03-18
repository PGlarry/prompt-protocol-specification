---
title: PPS v1.0 제어 어휘 레지스트리
lang: ko
status: draft
version: 1.0.0
---

# 1. 제약 조건 (Constraints)
- `no_external_browse` | 외부 브라우징 금지
- `use_provided_evidence` | 제공된 증거만 사용
- `citations_required` | 인용 필수
- `no_pii` | 개인 식별 정보 금지

# 2. 역량 (Capabilities)
- `web_browse` | 외부 브라우징
- `function_call` | 함수 호출
- 기타 도구 이름은 "도구 이름 = 역량 이름" 규칙을 따릅니다

# 3. 패러다임 (Paradigms)
- `ReAct`, `CoT`, `ToT`, `Plan-Execute`, `None`

# 4. 용어 정규화 (Normalization)
- `how_many` ⇒ `how_much`로 정규화

# PPS v1.0 권장 어휘 (비규범적)

이 문서는 구현자가 다양한 장르/시나리오에서 재사용할 수 있는 "권장 어휘"를 제공합니다. 표준 스키마의 자유도와 호환성을 변경하지 않습니다. 구현은 필요에 따라 채택하거나 맞춤화할 수 있습니다.

## how_much (콘텐츠 정량화 컨테이너) 권장 필드
- 범용 (텍스트 / 보고서 / 기사)
  - content_length: 예 "800-1200자", "5-7만 자"
  - structure_elements: 예 "3-4단락", "10-12장"
  - detail_richness: 예 "단락당 3-5 핵심 포인트", "데이터 및 차트 포함"
  - quality_guidance: 예 "용어 일관성, 검증 가능, 인용 기준"
  - cultural_depth: 예 "도메인 배경 / 기준 비교 / 현지화"
- 여행 / 가이드
  - poi_count: "50개 이상 명소"
  - price_ranges: "입장료 0-15만원", "숙박 8-20만원/박"
  - itinerary_days: "1-5일 여정"
- 코드 / 개발
  - module_count: "3-5개 모듈"
  - api_count: "2-3개 API 엔드포인트"
  - test_coverage_hint: "샘플 테스트 케이스 + 기본 분기 커버리지"
- 가사 / 시
  - line_count: "16-24행"
  - stanza_count: "3-4연"
  - rhyme_scheme: "AABB / ABAB"
- 튜토리얼 / 체크리스트
  - steps_count: "5-8단계"
  - checklist_items: "10-15항목"

참고: 위 내용은 예시입니다. `how_much`는 문자열 또는 객체가 될 수 있습니다. 필드 이름과 단위는 강제되지 않으며 도메인별 맞춤화를 권장합니다.
