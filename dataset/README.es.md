# PPS-Bench: Conjunto de Datos de Prompts Paralelos Multilingüe para Investigación de Alineación de Intención

**[English](README.md) | [中文](README.zh.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Español](README.es.md)**

---

## Descripción General

PPS-Bench es un conjunto de datos de referencia multilingüe y abierto para investigar la **transmisión estructurada de intención en la interacción humano-IA**. Proporciona prompts paralelos en 3 idiomas, múltiples condiciones de prompt y configuraciones de ablación, 6 modelos de IA y 3 dominios de tarea, con puntuaciones de alineación de objetivos (GA) para cada registro. Paper 4 también incluye s-ICMw y DS.

---

## Estadísticas del Conjunto de Datos

| Dimensión | Detalles |
|-----------|---------|
| Total de Registros (con solapamientos) | **8,820** |
| Registros Experimentales Únicos | **8,280** |
| Idiomas | ZH (Chino), EN (Inglés), JA (Japonés) |
| Condiciones de Prompt | 6 (A / B / C / D / E / F) + condiciones de ablación de Paper 4 |
| Modelos de IA | Claude, GPT-4o, Gemini 2.5 Pro, DeepSeek, Qwen, Kimi |
| Dominios de Tarea | Viajes, Negocios, Técnico |
| Tareas por Dominio | 20 |
| Métrica de Evaluación | Puntuación de Alineación de Objetivos (1-5, evaluado por DeepSeek-V3); Paper 4 también incluye s-ICMw y DS |

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

## Condiciones de Ablación de Paper 4

Paper 4 se publica como un paquete independiente e incluye `FULL` y 7 condiciones de eliminación de dimensión:
`-why`, `-who`, `-when`, `-where`, `-how_to_do`, `-how_much` y `-how_feel`.
Solo se publican los datos usados directamente en Paper 4; los artefactos `v2` y los análisis reservados para el futuro paper teórico IST quedan excluidos por ahora.

---

## Estructura de Archivos

```
dataset/
├── data/
│   ├── paper1/
│   ├── paper2/
│   ├── paper3/
│   ├── paper4/
│   │   ├── pps_bench_paper4_zh.jsonl  ← 1,440 registros en chino
│   │   ├── pps_bench_paper4_en.jsonl  ← 720 registros en inglés
│   │   ├── pps_bench_paper4_ja.jsonl  ← 720 registros en japonés
│   │   └── pps_bench_paper4.jsonl     ← 2,880 registros
│   └── pps_bench_full.jsonl           ← 8,820 registros completos
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
  url       = {https://github.com/PGlarry/prompt-protocol-specification},
  note      = {8,820 registros (8,280 únicos) en 4 artículos}
}
```

---

## Licencia

Publicado bajo [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
