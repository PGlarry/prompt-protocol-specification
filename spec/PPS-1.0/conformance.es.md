---
title: PPS v1.0 Conformidad y Especificación de Pruebas
lang: es
status: draft
version: 1.0.0
---

# 1. Alcance
Define las pruebas mínimas de conformidad para PPS v1.0: validación de esquema, comprobaciones de políticas, reproducibilidad y consistencia de hash. La salida está destinada a revisión humana y CI.

# 2. Validaciones Requeridas
1) JSON Schema (REQ-001): `spec/pps-1.0.schema.json`
2) Comprobaciones de políticas (REQ-050/051/052/053, 180..183, 320..323)
3) Consistencia de hash canónico (REQ-300)
4) Determinismo de decodificación (REQ-012/302) y repetición multiplataforma (dentro de tolerancia)

# 3. Herramientas y Comandos
- Canonicalización / hash: `node tests/pps-conformance/canonicalize.js <file> --write`
- Validación de esquema: `node tests/pps-conformance/validate.js <file>`
- Comprobaciones de políticas: `node tests/pps-conformance/policy_checks.js <file> --json`
- Auto-corrección: `node tests/pps-conformance/auto_fix.js <file> --write`

# 4. Formato de Salida (Recomendado)
Comprobación de políticas `--json`:
```json
{ "pass": true, "warnings": [], "issues": [{ "type": "tool_capability_missing", "message": "..." }] }
```

# 5. Integración CI (Recomendada)
En CI, para cada archivo en `spec/examples/*.json`: canonicalizar → esquema → política → (si es necesario) auto-corrección → resumen. El fallo bloquea el pipeline.
