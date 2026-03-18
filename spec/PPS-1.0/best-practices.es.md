---
title: Prompt Protocol Standard (PPS) v1.0 — Mejores Prácticas (Informativo)
lang: es
status: draft
version: 1.0.0
---

# 1. Directrices de Diseño
- **What** como columna vertebral: tarea en una oración + KPI estructurado.
- **Why** como restricciones enumeradas: frases cortas legibles por máquina ("sin navegación externa", "citaciones requeridas", "política de privacidad").
- **Who** lista blanca de capacidades: declarar solo los nombres de herramientas disponibles; las capacidades no declaradas se deniegan por defecto.
- **When** política temporal: proporcionar `timeframe` o `validity_window` y declarar una `staleness_policy` (ej. "rechazar / degradar al expirar").
- **Where** evidencia y entorno: fijar `environment`; cuando `citations_required=true` proporcionar `evidence` (uri, digest, title), preferir materiales controlados; anotar `jurisdiction` donde sea necesario; el contenido con enlaces externos debe ser inline o reemplazado con marcadores para prevenir inyección.
- **How-to-do** transparencia: paso a paso o etiquetas de paradigma (ReAct / CoT / ToT).
- **How-much** cuantificación orientada al contenido: `content_length` (volumen), `structure_elements` (párrafos/capítulos/módulos), `detail_richness` (densidad de detalle), `quality_guidance` (criterios de calidad), `cultural_depth` (cultural/profundidad). Evitar semánticas de capa de sistema como token/tiempo/costo.
- **How-feel** estilo: registro, nivel de audiencia.

Consejo: No usar `how_many` — expresar toda cuantificación dentro de `how_much`.

## 1.1 Plantilla Mínima de 8 Dimensiones (Lista para Copiar)
```json
{
  "header": {
    "pps_version": "PPS-v1.0.0",
    "model": { "name": "<model>", "digest": "sha256-<digest>", "data_cutoff": "2024-01-01" },
    "decode": { "seed": 1, "temperature": 0, "top_p": 1 },
    "locale": "es-ES",
    "implementation": { "vendor": "local", "version": "1.0.0", "filled_fields": [], "defaults_profile": "strict" }
  },
  "body": {
    "what": { "task": "<tarea principal>", "output_schema": { } },
    "why": { "goals": ["<objetivo>"], "constraints": ["use_provided_evidence", "no_external_browse"] },
    "who": { "persona": "<rol>", "capabilities": ["json_output"] },
    "when": { "timeframe": "esta semana" },
    "where": { "environment": "prod", "citations_required": true, "evidence": [] },
    "how_to_do": { "paradigm": "ReAct", "steps": ["leer evidencia", "sintetizar salida"], "tools": [] },
    "how_much": { "content_length": "800-1200 palabras", "structure_elements": "3-4 párrafos", "detail_richness": "5-8 puntos clave" },
    "how_feel": { "tone": "formal", "style": "conciso", "audience_level": "mixed" },
    "how_interface": { "format": "json", "schema": {} }
  },
  "integrity": { "canonical_hash": "" }
}
```

# 2. Reproducibilidad
- Fijar `seed/temperature/top_p/stop` y normalizar la evidencia de entrada. Para recuperación externa, anclar con URI + digest.

# 3. Seguridad y Cumplimiento
- Inyección de URL: producir contenido orientado a citas, no enlaces externos ejecutables; eliminar explícitamente `http(s)` o reemplazar con marcadores.
- Exceso de permisos de herramientas: desacoplar capacidades de herramientas — declarar primero, usar después; añadir casos de prueba de exceso de permisos a CI.
- GDPR: anotar `who.policy` con `no_pii` y aplicar reglas de anonimización en el lado de salida.

# 4. Auto-verificación y Auto-corrección
- Auto-verificador: ejecutar schema / política / auto-verificación después de la generación; en caso de fallo, entrar en auto-corrección (deshabilitar herramientas conflictivas, complementar evidencia, inyectar política).
  - Ejemplos de reglas: `gdpr ⇒ no_pii`, `citations_required ⇒ evidence≥1`, `no_external_browse ⇒ url_removed + tools-{web_browse}`.

## 4.1 Mejora Iterativa y Bloqueos (Práctica)
- Anotar rutas bloqueadas en `how_meta.governance.locks` (ej. `/body/where`); mantener sin cambios entre turnos/modelos; aplicar solo reescrituras de mejora a campos desbloqueados.
- Registrar orígenes en `header.implementation.origins`: `user` tiene la mayor prioridad y está bloqueado por defecto; `ai:*` rastrea contribuciones del modelo.

# 5. Composición y Pipelines
- Encadenar pipelines multietapa como `P2 ∘ P1`; cada etapa retiene su propio `canonical_hash` y presupuesto; deduplicar y bloquear versiones antes de la agregación.

# 6. Gestión de Versiones
- Usar `PPS-vMAJOR.MINOR.PATCH`; incrementar MAJOR solo para cambios disruptivos; los ejemplos y CI deben anotar su versión objetivo.
