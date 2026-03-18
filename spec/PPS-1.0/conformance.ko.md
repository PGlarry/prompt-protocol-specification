---
title: PPS v1.0 적합성 & 테스트 사양
lang: ko
status: draft
version: 1.0.0
---

# 1. 범위
PPS v1.0의 최소 적합성 테스트를 정의합니다: 스키마 검증, 정책 검사, 재현성, 해시 일관성. 출력은 인간 검토 및 CI를 위한 것입니다.

# 2. 필수 검증 항목
1) JSON 스키마 (REQ-001): `spec/pps-1.0.schema.json`
2) 정책 검사 (REQ-050/051/052/053, 180..183, 320..323)
3) 정규 해시 일관성 (REQ-300)
4) 디코드 결정론 (REQ-012/302) 및 교차 플랫폼 재생 (허용 범위 내)

# 3. 도구 & 명령어
- 정규화 / 해시: `node tests/pps-conformance/canonicalize.js <file> --write`
- 스키마 검증: `node tests/pps-conformance/validate.js <file>`
- 정책 검사: `node tests/pps-conformance/policy_checks.js <file> --json`
- 자동 수정: `node tests/pps-conformance/auto_fix.js <file> --write`

# 4. 출력 형식 (권장)
정책 검사 `--json`:
```json
{ "pass": true, "warnings": [], "issues": [{ "type": "tool_capability_missing", "message": "..." }] }
```

# 5. CI 통합 (권장)
CI에서 `spec/examples/*.json`의 각 파일에 대해 순서대로 실행합니다: 정규화 → 스키마 → 정책 → (필요시) 자동 수정 → 집계. 실패 시 파이프라인이 차단됩니다.
