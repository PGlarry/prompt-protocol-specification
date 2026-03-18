---
title: PPS 버전 관리 & 호환성 정책
lang: ko
status: draft
---

# 1. 시맨틱 버전 관리
- `MAJOR.MINOR.PATCH`를 사용합니다. 프로토콜 버전은 `header.pps_version`에 `PPS-vMAJOR.MINOR.PATCH`로 태그됩니다.

# 2. 호환성 정책
- 1.0.x 시리즈: 새 필드는 선택 사항으로 유지되며 하위 호환성을 보장합니다.
- MAJOR는 파괴적 변경 (필드 삭제 또는 의미 변경)의 경우에만 증가합니다.

# 3. 마이그레이션
- 1.0에서 1.x로 업그레이드: 예제와 CI에 대상 버전을 태그합니다. 새 정책 조항이 추가된 경우 `policy_checks` 규칙 업그레이드를 통해 감지할 수 있습니다.
