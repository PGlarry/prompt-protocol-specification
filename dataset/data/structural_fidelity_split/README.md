# Dataset: Structural Recovery Without Intent Fidelity

This directory contains all data and analysis scripts for the paper:

> **Structural Recovery Without Intent Fidelity: A Blind Spot in Holistic
> Evaluation of Large Language Models**
> Gang Peng — submitted to *Nature Machine Intelligence* (2026)

The study quantifies the **structural-fidelity split** — a systematic pattern
in which LLM outputs achieve near-perfect holistic alignment scores (GA=5)
while failing to reproduce the user's specific dimensional intent.

---

## Directory Structure

```
structural_fidelity_split/
  01_ablation/         Dimensional ablation experiment (§2.1–2.2, Methods §4.1–4.4)
  02_human_evaluation/ Independent human validation (§2.1, Methods §4.8)
  03_proxy_annotation/ Prior-inferability proxy study (§2.3, Methods §4.5)
  04_weight_experiment/ Weight-perturbation experiment (§2.4, Methods §4.6)
  analysis_scripts/    Reproducible analysis code
```

---

## Experiments Overview

### 01 · Dimensional Ablation (§2.1–2.2)

- **Design**: 30 tasks × 3 domains × 8 conditions (FULL + 7 single-dimension ablations)
  × 6 models (ZH) / 3 models (EN, JA) = 2,880 outputs evaluated
- **Models**: Claude Sonnet 4 (`claude-sonnet-4-20250514`), GPT-4o (`gpt-4o`),
  DeepSeek-V3 (`deepseek-chat`), Qwen-Max (`qwen-max`),
  Gemini 2.5 Pro (`gemini-2.5-pro`), Kimi (`moonshot-v1-32k`)
- **Metrics**: GA (holistic, 1–5), f-ICMw (dimensional fidelity), s-ICMw (structural coverage)
- **Key finding**: 22.5% ZH / 60.3% EN outputs score GA=5 with measurable dimensional deficits

| File | Description |
|---|---|
| `tasks/tasks_zh.json` | 30 tasks used for ZH experiment |
| `tasks/tasks_en.json` | Tasks for EN subset |
| `tasks/tasks_ja.json` | Tasks for JA subset |
| `data/ablation_zh.jsonl` | All ZH outputs with GA + f-ICMw scores (1,440 records) |
| `data/ablation_en.jsonl` | EN outputs (720 records, 3 models) |
| `data/ablation_ja.jsonl` | JA outputs (720 records, 3 models) |
| `data/ablation_full.jsonl` | All languages combined (2,880 records) |
| `scores/zh/` | Per-task per-model detailed score files (ZH) |
| `scores/en/` | Per-task per-model detailed score files (EN) |
| `scores/ja/` | Per-task per-model detailed score files (JA) |

### 02 · Human Evaluation (§2.1, Methods §4.8)

- **Design**: N=60 stratified sample (25 split-zone, 15 agree-high, 10 full-baseline, 10 agree-low)
- **Raters**: Two independent raters (A: familiar with 5W3H; B: no prior framework exposure)
- **Outputs**: Anonymized — no user or model identifying information retained

| File | Description |
|---|---|
| `answer_key.json` | Sampling frame, zone labels, gold references for 60 outputs |
| `annotation_sheet.xlsx` | Combined scoring rubric and instructions |
| `analysis_summary.xlsx` | Rater scores + LLM scores + Spearman ρ computations |
| `outputs/1–60.docx` | Anonymized model outputs shown to raters |

### 03 · Proxy Annotation (§2.3, Methods §4.5)

- **Design**: 210 task × dimension units (30 tasks × 7 ablatable dimensions)
- **Annotators**: GPT-4o (`gpt-4o`) and Claude Sonnet 4 (`claude-sonnet-4-20250514`)
- **Task**: Label each unit as public / private / mixed based on prior inferability
- **Key finding**: Global rank concordance with recovery rates is weak (ρ=0.157),
  demonstrating that prior inferability ≠ default recoverability

| File | Description |
|---|---|
| `units.jsonl` | 210 task × dimension units with gold content |
| `labels_gpt4o.jsonl` | GPT-4o inferability labels (public/private/mixed) |
| `labels_claude.jsonl` | Claude Sonnet 4 inferability labels |
| `merged.csv` | B+ consensus labels with adjudication flags |

### 04 · Weight-Perturbation Experiment (§2.4, Methods §4.6)

- **Design**: 2 domains × 3 models × 4 weight conditions (matched/uniform/perturbed/mismatched)
  × 10 tasks/domain = 240 outputs, dual-judge scored (v3_clean leakage-audited subset)
- **Models**: DeepSeek-V3, Qwen-Max, Kimi
- **Key finding**: Plateau-cliff structure — moderate misalignment absorbed; severe inversion
  consistently degrades WAS across 100% of domain × model cells

| File | Description |
|---|---|
| `tasks/tasks_v3_clean.json` | Task definitions for weight experiment |
| `scores/judge_a/` | Judge A (primary) per-task scores |
| `scores/judge_b/` | Judge B (independent) per-task scores |
| `scores/judge_a/summary.json` | Condition-level summary, Judge A |
| `scores/judge_b/summary.json` | Condition-level summary, Judge B |

---

## Reproducing Key Results

```bash
# Table 1 (human evaluation): requires annotation_sheet.xlsx + answer_key.json
python analysis_scripts/human_eval_analysis.py

# Table 2 (weight experiment): requires scores/judge_a/ + scores/judge_b/
python analysis_scripts/analyze_weight_experiment.py

# Results §2.1–2.2 (split rates, s/f-ICMw divergence): requires scores/zh/ etc.
python analysis_scripts/analyze_ablation.py

# Results §2.3 (proxy annotation): requires merged.csv
python analysis_scripts/pub_priv_analysis.py
```

> **Note**: API credentials are required to re-run model inference
> (`run_*.py` scripts). Analysis scripts operate on the pre-computed score
> files and do not require API access.

---

## Relationship to Prior Work

This dataset supersedes the separately released `paper4` dataset.
Papers 1–3 data remains in `dataset/data/paper1/`, `paper2/`, `paper3/`
respectively (corresponding to arXiv refs 2603.18976, 2603.25379, 2603.29953).

---

## Citation

*Citation information will be added upon publication.*

## License

Data and code are released under CC BY 4.0.
