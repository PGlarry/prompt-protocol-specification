---
title: PPS Política de Versiones y Compatibilidad
lang: es
status: draft
---

# 1. Versionado Semántico
- Usa `MAJOR.MINOR.PATCH`; la versión del protocolo se etiqueta como `PPS-vMAJOR.MINOR.PATCH` en `header.pps_version`.

# 2. Política de Compatibilidad
- Serie 1.0.x: los nuevos campos permanecen opcionales y son retrocompatibles.
- MAJOR se incrementa solo para cambios disruptivos (eliminación de campo o cambio semántico).

# 3. Migración
- Actualización de 1.0 a 1.x: etiquetar ejemplos y CI con la versión objetivo; si se añaden nuevas cláusulas de política, pueden detectarse mediante actualizaciones de reglas de `policy_checks`.
