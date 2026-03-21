# PPS — Especificación del Protocolo de Prompts

<div align="center">

**[English](README.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md)**

[![License: MIT](https://img.shields.io/badge/Tools-MIT-blue.svg)](LICENSE)
[![Docs: CC BY 4.0](https://img.shields.io/badge/Docs-CC%20BY%204.0-green.svg)](spec/PPS-1.0/IP_NOTICE.md)
[![Version](https://img.shields.io/badge/PPS-v1.0.0-orange.svg)](spec/PPS-1.0/standard.md)
[![Status](https://img.shields.io/badge/Status-Community%20Specification-brightgreen.svg)](STATUS.md)

*Un marco de instrucciones estructurado de 8 dimensiones para la interacción humano-IA*

</div>

---

<div align="center">

### Pruébalo · Lee el Libro · Explora la Especificación

| | |
|---|---|
| **Plataforma 5W3H** | [https://www.lateni.com](https://www.lateni.com) — implementación en vivo, diseña tus envoltorios PPS en línea |
| **Libro** | [*Super Prompt: 5W3H — A Comprehensive Guide to Designing Effective AI Prompts Across Domains*](https://www.amazon.com/dp/B0F3Z25CHC)<br>Gang Peng · Amazon KDP · Abril 2025 · ASIN: B0F3Z25CHC |

</div>

---

## ¿Qué es PPS?

Los prompts en lenguaje natural sufren de **pérdida de transmisión de intención** — la brecha entre lo que los usuarios realmente necesitan y lo que comunican a los sistemas de IA. PPS (Especificación del Protocolo de Prompts) resuelve esto proporcionando un envoltorio estructurado y verificable por máquina para las instrucciones de IA.

PPS está construido sobre el **modelo 5W3H**: *What (Qué), Why (Por qué), Who (Quién), When (Cuándo), Where (Dónde), How-to-do (Cómo hacerlo), How-much (Cuánto), How-feel (Cómo sentirlo)* — ocho dimensiones que especifican completamente cualquier tarea de IA.

```json
{
  "pps_header": {
    "pps_version": "PPS-v1.0.0",
    "model": { "name": "gpt-4o", "digest": "sha256:abc123", "data_cutoff": "2025-01-01" },
    "decode": { "seed": 42, "temperature": 0.7, "top_p": 0.95 },
    "locale": "es-ES"
  },
  "pps_body": {
    "what": { "task": "Redactar un análisis competitivo del mercado de vehículos eléctricos en América Latina" },
    "why": { "goals": ["apoyar la decisión de inversión estratégica"], "constraints": ["no_pii"] },
    "who": { "persona": "analista industrial senior", "audience": ["ejecutivos C-suite"] },
    "when": { "timeframe": "datos de 2024, instantánea del mercado actual" },
    "where": { "environment": "presentación ante el consejo directivo", "jurisdiction": "ES" },
    "how_to_do": { "paradigm": "CoT", "steps": ["dimensionamiento del mercado", "5 Fuerzas de Porter", "top 5 actores", "proyección de tendencias"] },
    "how_much": { "content_length": "2000 palabras", "structure_elements": "5 secciones con tablas", "detail_richness": "10+ puntos de datos" },
    "how_feel": { "tone": "profesional", "style": "basado en datos", "audience_level": "experto" }
  },
  "pps_integrity": {
    "canonical_hash": "sha256:TO_BE_FILLED_AFTER_CANONICALIZATION"
  }
}
```

---

## ¿Por qué PPS?

Resultados empíricos de un experimento controlado (60 temas × 3 LLMs × 3 condiciones, 540 salidas):

| Métrica | Prompt Simple (A) | PPS Renderizado (C) | Mejora |
|---------|:-----------------:|:-------------------:|:------:|
| **goal_alignment** | 4.34 | **4.61** | *p* = 0.006, *d* = 0.374 |
| Prompts de seguimiento necesarios | ~3.3 rondas | ~1.1 rondas | **−66%** |
| Precisión en primera impresión | — | **85%** preciso en primera expansión | — |

> Metodología completa y resultados: [Artículo (arXiv)](https://arxiv.org/abs/2603.18976) · [Datos experimentales](experiments/)

**Conclusión clave**: Las métricas tradicionales de evaluación LLM muestran A > C debido a la *asimetría de puntuación de restricciones* — los prompts sin restricciones obtienen puntuaciones perfectas trivialmente. Cuando se evalúa la alineación con la intención del usuario (`goal_alignment`), los prompts PPS estructurados superan significativamente a los simples, especialmente en dominios de alta ambigüedad (negocios: *d* = 0.895).

---

## Estructura del Repositorio

```
prompt-protocol-specification/
├── spec/
│   └── PPS-1.0/
│       ├── standard.md          # Especificación normativa (chino)
│       ├── standard.en.md       # Especificación normativa (inglés)
│       ├── standard.ja.md       # Especificación normativa (japonés)
│       ├── best-practices.md    # Guía de implementación
│       ├── conformance.md       # Niveles de conformidad
│       ├── security-privacy.md  # Requisitos de seguridad y GDPR
│       ├── versioning.md        # Política de versiones
│       ├── benchmark.md         # Metodología de benchmarks
│       ├── registry.md          # Vocabulario controlado
│       └── IP_NOTICE.md         # Aviso de propiedad intelectual
├── schema/
│   ├── pps-1.0.schema.json      # JSON Schema (estricto)
│   └── pps.schema.json          # JSON Schema (base)
├── spec/examples/               # Envoltorios de ejemplo anotados
├── tests/pps-conformance/       # Suite de pruebas de conformidad (Node.js)
├── tools/
│   └── pps-verify.js            # Herramienta de verificación CLI
├── STATUS.md                    # Hoja de ruta y gobernanza
└── PUBLISHING.md                # Guía de lanzamiento y DOI
```

---

## Inicio Rápido

**Validar un envoltorio:**
```bash
node tests/pps-conformance/validate.js spec/examples/minimal.json
```

**Ejecutar todas las comprobaciones de conformidad:**
```bash
node tests/pps-conformance/summary.js
```

**Calcular hash canónico:**
```bash
node tools/pps-verify.js spec/examples/minimal.json
```

**Requisitos:** Node.js ≥ 16

---

## Perfiles de Conformidad

PPS define tres niveles de conformidad declarados en `header.compliance`:

| Perfil | `why.goals` | `who.audience` | `how_to_do.steps` | Campos `how_much` |
|--------|:-----------:|:--------------:|:-----------------:|:-----------------:|
| `strict` | ≥ 4 | ≥ 4 | ≥ 6 | ≥ 3 |
| `balanced` | ≥ 3 | ≥ 3 | ≥ 5 | ≥ 2 |
| `permissive` | ≥ 2 | ≥ 2 | ≥ 4 | ≥ 1 |

---

## Citación

Si utilizas PPS en trabajos académicos, por favor cita:

```bibtex
@article{peng2026pps,
  title     = {Evaluating 5W3H Structured Prompting for Intent Alignment in
               Human-AI Interaction},
  author    = {Peng, Gang},
  year      = {2026},
  eprint    = {2603.18976},
  archivePrefix = {arXiv},
  primaryClass = {cs.AI},
  url       = {https://arxiv.org/abs/2603.18976}
}
```

---

## Recursos Relacionados

- **Plataforma 5W3H**: [https://www.lateni.com](https://www.lateni.com) — implementación en vivo, diseña tus envoltorios PPS en línea
- **Libro**: [*Super Prompt: 5W3H — A Comprehensive Guide to Designing Effective AI Prompts Across Domains*](https://www.amazon.com/dp/B0F3Z25CHC)
  Gang Peng · Amazon KDP · Abril 2025 · ASIN: B0F3Z25CHC

---

## Licencia

- **Documentos de especificación** (`spec/`): [CC BY 4.0](spec/PPS-1.0/IP_NOTICE.md) — libre para usar, compartir y adaptar con atribución
- **Herramientas y pruebas** (`tools/`, `tests/`): [MIT](LICENSE)
- **Apertura**: PPS y 5W3H son completamente abiertos — sin patentes presentadas ni reclamadas. Cualquiera puede implementar y comercializar libremente. Ver [IP_NOTICE.md](spec/PPS-1.0/IP_NOTICE.md).

---

<div align="center">
<sub>Created by <a href="https://www.lateni.com">Gang Peng</a> · Huizhou University · Huizhou Lateni AI Technology Co., Ltd.</sub>
</div>
