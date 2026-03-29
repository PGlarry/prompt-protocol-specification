# PPS-Bench: Conjunto de Datos de Prompts Paralelos Multilingüe para Investigación de Alineación de Intención

**[English](README.md) | [中文](README.zh.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Español](README.es.md)**

---

## Descripción General

PPS-Bench es un conjunto de datos de referencia multilingüe y abierto para investigar la **transmisión estructurada de intención en la interacción humano-IA**. Proporciona prompts paralelos en 3 idiomas, 6 formatos de prompt, 3 modelos de IA y 3 dominios de tareas, con puntuaciones de alineación de objetivos (GA) para cada registro.

---

## Estadísticas del Conjunto de Datos

| Dimensión | Detalles |
|-----------|---------|
| Total de Registros | **4,440** |
| Idiomas | ZH (Chino), EN (Inglés), JA (Japonés) |
| Condiciones de Prompt | 6 (A / B / C / D / E / F) |
| Modelos de IA | Claude (claude-sonnet-4-20250514), GPT-4o, Gemini 2.5 Pro |
| Dominios de Tarea | Viajes, Negocios, Técnico |
| Tareas por Dominio | 20 |
| Métrica de Evaluación | Puntuación de Alineación de Objetivos (1-5, evaluado por DeepSeek-V3) |

---

## Las 6 Condiciones de Prompt

| ID | Nombre | Descripción |
|----|--------|-------------|
| **A** | Prompt Simple | Descripción de tarea en una oración (línea base) |
| **B** | JSON Estructurado (PPS Crudo) | JSON PPS sin renderizar |
| **C** | 5W3H Manual (Lenguaje Natural) | 5W3H escrito manualmente en lenguaje natural |
| **D** | 5W3H Expandido por IA (PPS Completo) | Prompt PPS completo de 8 dimensiones generado por expansión de intención IA en [lateni.com](https://lateni.com) |
| **E** | CO-STAR | Prompt estructurado con el marco CO-STAR |
| **F** | RISEN | Prompt estructurado con el marco RISEN |

---

## Estructura de Archivos

```
dataset/
├── data/
│   ├── pps_bench_zh.jsonl      ← 1,080 registros en chino
│   ├── pps_bench_en.jsonl      ← 1,080 registros en inglés
│   ├── pps_bench_ja.jsonl      ← 1,080 registros en japonés
│   └── pps_bench_full.jsonl    ← 3,240 registros completos
└── statistics/
    └── summary.json
```

---

## Resultados Principales

| Condición | GA Media Global |
|-----------|----------------|
| A (línea base) | 4.463 |
| B (JSON crudo) | 4.141 |
| C (5W3H manual) | 4.683 |
| D (5W3H IA) | 4.930 |
| E (CO-STAR) | 4.978 |
| F (RISEN) | 4.983 |

**Hallazgo notable**: Los prompts estructurados (D/E/F) reducen la varianza de puntuación entre idiomas hasta 24× (σ: 0.470 → 0.020).

---

## Cita

```bibtex
@dataset{pps_bench_2026,
  title     = {PPS-Bench: A Multilingual Parallel Prompt Dataset for Intent Alignment Research},
  author    = {[Autor]},
  year      = {2026},
  url       = {https://github.com/PGlarry/prompt-protocol-specification}
}
```

---

## Licencia

Publicado bajo [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
