---
title: PPS v1.0 Seguridad y Privacidad (Modelo de Amenazas)
lang: es
status: draft
version: 1.0.0
---

# 1. Modelo de Amenazas
- Inyección (prompt / URL / envenenamiento de evidencia)
- Exceso de permisos (herramientas no declaradas o canales externos)
- Riesgo de cumplimiento (PII, citaciones faltantes, restricciones entre jurisdicciones)

# 2. Contramedidas (Referencias Normativas)
- Lista blanca de interfaz y sandbox de capacidades: `how_to_do.tools ⊆ who.capabilities` (REQ-181)
- Restricción de no navegación: `no_external_browse` ⇒ deshabilitar `web_browse` y eliminar URLs (REQ-052/183)
- Consistencia de citaciones: `citations_required` ⇒ `evidence` no vacío (REQ-180)
- GDPR: `gdpr` ⇒ `no_pii` (REQ-182)
- No interferencia causal: las entradas no autorizadas no deben alterar la distribución de salida de las entradas autorizadas (alineado con el cuerpo del artículo y la especificación normativa)

# 3. Riesgos Residuales y Límites
- Deriva menor por actualizaciones no controladas de modelos de terceros o fuentes de recuperación (mitigado por decodificación determinista y capturas de evidencia)
- Subjetividad en anotación manual o puntuación externa (reducida por umbrales KPI y validación de esquema)
