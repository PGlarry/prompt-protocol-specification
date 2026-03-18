---
title: PPS v1.0 Registro de Vocabulario Controlado
lang: es
status: draft
version: 1.0.0
---

# 1. Restricciones (Constraints)
- `no_external_browse` | Prohibir navegación externa
- `use_provided_evidence` | Usar solo la evidencia proporcionada
- `citations_required` | Citaciones requeridas
- `no_pii` | Prohibir información de identificación personal

# 2. Capacidades (Capabilities)
- `web_browse` | Navegación externa
- `function_call` | Llamada a función
- Otros nombres de herramientas siguen la regla "nombre de herramienta = nombre de capacidad"

# 3. Paradigmas (Paradigms)
- `ReAct`, `CoT`, `ToT`, `Plan-Execute`, `None`

# 4. Normalización de Términos (Normalization)
- `how_many` ⇒ normalizar a `how_much`

# PPS v1.0 Vocabulario Recomendado (No normativo)

Este documento proporciona vocabulario sugerido que los implementadores pueden reutilizar en diferentes géneros y escenarios. No cambia la libertad o compatibilidad del Schema estándar. Las implementaciones pueden adoptar o personalizar según sea necesario.

## how_much (Contenedor de Cuantificación de Contenido) — Campos Recomendados
- General (texto / informes / artículos)
  - content_length: ej. "800-1200 palabras", "50.000-70.000 palabras"
  - structure_elements: ej. "3-4 párrafos", "10-12 capítulos"
  - detail_richness: ej. "3-5 puntos clave por párrafo", "incluir datos y gráficos"
  - quality_guidance: ej. "terminología consistente, verificable, estándares de citación"
  - cultural_depth: ej. "contexto de dominio / comparación de estándares / localización"
- Viajes / Guía
  - poi_count: "50+ atracciones"
  - price_ranges: "entradas €0-15", "alojamiento €80-200/noche"
  - itinerary_days: "itinerario de 1-5 días"
- Código / Desarrollo
  - module_count: "3-5 módulos"
  - api_count: "2-3 endpoints API"
  - test_coverage_hint: "casos de prueba de ejemplo + cobertura básica de ramas"
- Letras / Poesía
  - line_count: "16-24 líneas"
  - stanza_count: "3-4 estrofas"
  - rhyme_scheme: "AABB / ABAB"
- Tutorial / Lista de verificación
  - steps_count: "5-8 pasos"
  - checklist_items: "10-15 elementos"

Nota: Lo anterior son solo ejemplos. `how_much` puede ser una cadena o un objeto; los nombres de campo y las unidades no están mandatados — se recomienda la personalización específica del dominio.
