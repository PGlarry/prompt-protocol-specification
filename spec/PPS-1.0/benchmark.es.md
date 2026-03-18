---
title: PPS v1.0 Benchmark y Métricas (Informativo)
lang: es
status: draft
version: 1.0.0
---

# 1. Objetivo
Cuantificar la capacidad de la capa de protocolo: reproducibilidad, efectividad de gobernanza y explicitud de recursos.

# 2. Métricas
- Tasa de captura de políticas = recuento FAIL / total de casos (por tipo: inyección, exceso de permisos, citación, GDPR, presupuesto)
- Tasa de éxito de auto-corrección = recuento PASS post-corrección / casos que activaron auto-corrección
- Tasa de consistencia de repetición = proporción de repeticiones multiplataforma que son consistentes (o dentro de tolerancia)
- Tasa de explicitud del presupuesto de recursos = proporción de casos que contienen un campo de presupuesto `how_much`

## 2.1 Ablación de especificación parcial / combinación libre
- Configuración de entrada: proporcionar solo `what.task`; para las 7 dimensiones restantes, seleccionar aleatoriamente subconjuntos para que el sistema complete (siguiendo REQ-341..343).
- Elementos de evaluación:
  - Tasa de mantenimiento de cumplimiento: proporción que aún satisface invariantes de campos cruzados (REQ-180..183) tras la compleción
  - Robustez de alineación: curva de tasa de aprobación KPI vs. número de dimensiones proporcionadas (0..7)
  - Desviación de presupuesto: distribución de la desviación entre el presupuesto de recursos completado y la configuración objetivo

# 3. Fuentes de datos
- `issues[].type` de `tests/pps-conformance/policy_checks.js --json`
- `fixesApplied` de `auto_fix.js` (exportado por script posterior)
- `summary.js` agrega y genera `summary.csv` y `benchmark.json`
