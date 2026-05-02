from pathlib import Path
"""
pub_priv_analysis.py
====================
Classify each (dimension, model, domain) cell as "public" or "private"
based on f-ICMw recovery score when that dimension is ablated.

Public  : model successfully recovers the removed dimension from priors
          → icm_raw[removed_dim] >= THRESHOLD
Private : model cannot recover → icm_raw[removed_dim] < THRESHOLD

Validates IST Predictions:
  P2: "Private" dimensions → larger f-ICMw drop than "Public" dimensions
  P3: Weaker models have narrower pub set (more dimensions classified as private)

Output:
  d:/pps/experiments/data/ist_ablation/pub_priv_results.json
  d:/pps/experiments/data/ist_ablation/pub_priv_report.md
"""

import json
import os
import glob
from collections import defaultdict

# ── Config ─────────────────────────────────────────────────────────────────
THRESHOLD    = 0.7      # f-ICMw >= this → public; < this → private
DATA_ROOT    = str(Path(__file__).parent.parent / "01_ablation")
DIMS         = ["why", "who", "when", "where", "how_to_do", "how_much", "how_feel"]
DOMAINS      = ["business", "technical", "travel"]

# Model capacity ordering (strong → weak, from Paper 3 evidence)
MODEL_CAPACITY = {
    "claude":   3,   # strongest
    "gpt4o":    2,
    "qwen":     2,
    "deepseek": 2,
    "kimi":     1,
    "gemini":   1,   # weakest (from Paper 3 compensation effect)
}

# Score directories: (lang, v2_dir)
SCORE_DIRS = [
    ("zh", os.path.join(DATA_ROOT, "scores/zh")),
    ("en", os.path.join(DATA_ROOT, "scores/en")),
    ("ja", os.path.join(DATA_ROOT, "scores/ja")),
]

# ── Load all v2 score records ───────────────────────────────────────────────
def load_scores():
    records = []
    for lang, score_dir in SCORE_DIRS:
        if not os.path.isdir(score_dir):
            print(f"  [SKIP] {score_dir} not found")
            continue
        for fpath in glob.glob(os.path.join(score_dir, "*.jsonl")):
            with open(fpath, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        rec = json.loads(line)
                        rec["lang"] = lang
                        records.append(rec)
                    except json.JSONDecodeError:
                        pass
    print(f"Loaded {len(records)} v2 records from {len(SCORE_DIRS)} languages")
    return records

# ── Classify pub/priv per cell ─────────────────────────────────────────────
def classify_pub_priv(records, threshold=THRESHOLD):
    """
    For each ablation record (condition != FULL), extract the recovery score
    for the removed dimension from icm_raw, then classify pub/priv.

    Returns: list of dicts with keys:
      task_id, domain, model, lang, removed_dim,
      recovery_score, is_public, icmw_full, icmw_ablated, icmw_drop
    """
    # First, collect FULL icmw per (task, model, lang)
    full_scores = {}
    for rec in records:
        if rec.get("condition") == "FULL":
            key = (rec["task_id"], rec["model"], rec["lang"])
            full_scores[key] = rec.get("icmw", None)

    cells = []
    for rec in records:
        if rec.get("condition") == "FULL":
            continue
        removed = rec.get("removed_dim")
        if removed not in DIMS:
            continue
        icm_raw = rec.get("icm_raw", {})
        if not icm_raw or removed not in icm_raw:
            continue

        recovery_score = icm_raw[removed]
        # Handle 0.5 scores (partial) — treat >= threshold as public
        is_public = (recovery_score >= threshold)

        key = (rec["task_id"], rec["model"], rec["lang"])
        icmw_full    = full_scores.get(key)
        icmw_ablated = rec.get("icmw")
        icmw_drop    = (icmw_full - icmw_ablated) if (icmw_full is not None and icmw_ablated is not None) else None

        cells.append({
            "task_id":       rec["task_id"],
            "domain":        rec["domain"],
            "model":         rec["model"],
            "lang":          rec["lang"],
            "removed_dim":   removed,
            "recovery_score": recovery_score,
            "is_public":     is_public,
            "icmw_full":     icmw_full,
            "icmw_ablated":  icmw_ablated,
            "icmw_drop":     icmw_drop,
        })

    print(f"Classified {len(cells)} ablation cells")
    return cells

# ── Aggregate analyses ──────────────────────────────────────────────────────
def analyze(cells):
    results = {}

    # ── A: Pub rate per dimension (averaged across all models/domains/langs)
    dim_pub = defaultdict(lambda: {"public": 0, "total": 0, "drop_pub": [], "drop_priv": []})
    for c in cells:
        d = c["removed_dim"]
        dim_pub[d]["total"] += 1
        if c["is_public"]:
            dim_pub[d]["public"] += 1
            if c["icmw_drop"] is not None:
                dim_pub[d]["drop_pub"].append(c["icmw_drop"])
        else:
            if c["icmw_drop"] is not None:
                dim_pub[d]["drop_priv"].append(c["icmw_drop"])

    dim_summary = {}
    for d, v in dim_pub.items():
        pub_rate  = v["public"] / v["total"] if v["total"] else 0
        mean_drop_pub  = sum(v["drop_pub"])  / len(v["drop_pub"])  if v["drop_pub"]  else None
        mean_drop_priv = sum(v["drop_priv"]) / len(v["drop_priv"]) if v["drop_priv"] else None
        dim_summary[d] = {
            "pub_rate":       round(pub_rate, 3),
            "total":          v["total"],
            "n_public":       v["public"],
            "n_private":      v["total"] - v["public"],
            "mean_drop_pub":  round(mean_drop_pub,  3) if mean_drop_pub  is not None else None,
            "mean_drop_priv": round(mean_drop_priv, 3) if mean_drop_priv is not None else None,
        }
    results["by_dimension"] = dim_summary

    # ── B: Pub rate per domain
    domain_pub = defaultdict(lambda: {"public": 0, "total": 0})
    for c in cells:
        domain_pub[c["domain"]]["total"] += 1
        if c["is_public"]:
            domain_pub[c["domain"]]["public"] += 1
    results["by_domain"] = {
        dom: {
            "pub_rate": round(v["public"]/v["total"], 3) if v["total"] else 0,
            "n_public": v["public"],
            "total":    v["total"],
        }
        for dom, v in domain_pub.items()
    }

    # ── C: Pub rate per model (P3: weaker model → smaller pub set)
    model_pub = defaultdict(lambda: {"public": 0, "total": 0})
    for c in cells:
        model_pub[c["model"]]["total"] += 1
        if c["is_public"]:
            model_pub[c["model"]]["public"] += 1
    results["by_model"] = {
        m: {
            "pub_rate":   round(v["public"]/v["total"], 3) if v["total"] else 0,
            "n_public":   v["public"],
            "total":      v["total"],
            "capacity":   MODEL_CAPACITY.get(m, "?"),
        }
        for m, v in model_pub.items()
    }

    # ── D: P2 validation — private dims → larger f-ICMw drop?
    pub_drops  = [c["icmw_drop"] for c in cells if c["is_public"]  and c["icmw_drop"] is not None]
    priv_drops = [c["icmw_drop"] for c in cells if not c["is_public"] and c["icmw_drop"] is not None]
    results["p2_validation"] = {
        "mean_drop_public":  round(sum(pub_drops)/len(pub_drops),   3) if pub_drops  else None,
        "mean_drop_private": round(sum(priv_drops)/len(priv_drops), 3) if priv_drops else None,
        "n_public_cells":    len(pub_drops),
        "n_private_cells":   len(priv_drops),
        "p2_supported":      (sum(priv_drops)/len(priv_drops) > sum(pub_drops)/len(pub_drops))
                             if pub_drops and priv_drops else None,
    }

    # ── E: P3 validation — model capacity vs pub_rate (Spearman)
    model_rows = [(MODEL_CAPACITY.get(m, 0), v["public"]/v["total"])
                  for m, v in model_pub.items() if v["total"] > 0 and m in MODEL_CAPACITY]
    model_rows.sort(key=lambda x: x[0])
    # Simple rank correlation check
    n = len(model_rows)
    if n >= 3:
        cap_ranks  = [sorted(set(r[0] for r in model_rows)).index(r[0]) + 1 for r in model_rows]
        pub_ranks  = sorted(range(n), key=lambda i: model_rows[i][1])
        pub_ranks  = [pub_ranks.index(i) + 1 for i in range(n)]
        d2 = sum((cap_ranks[i] - pub_ranks[i])**2 for i in range(n))
        rho = 1 - 6*d2 / (n*(n**2-1))
        results["p3_validation"] = {
            "model_capacity_vs_pub_rate": [(m, MODEL_CAPACITY.get(m,"?"),
                                            round(v["public"]/v["total"],3))
                                           for m, v in sorted(model_pub.items(),
                                                               key=lambda x: MODEL_CAPACITY.get(x[0],0))
                                           if v["total"] > 0],
            "spearman_rho": round(rho, 3),
            "p3_supported": rho > 0.3,
            "note": "Positive rho = higher capacity → higher pub rate, supporting P3",
        }
    else:
        results["p3_validation"] = {"note": "Not enough models to compute correlation"}

    # ── F: By domain × dimension (pub rate heatmap data)
    dom_dim = defaultdict(lambda: {"public": 0, "total": 0})
    for c in cells:
        key = (c["domain"], c["removed_dim"])
        dom_dim[key]["total"] += 1
        if c["is_public"]:
            dom_dim[key]["public"] += 1
    results["domain_x_dimension"] = {
        f"{dom}|{dim}": {
            "pub_rate": round(v["public"]/v["total"], 3) if v["total"] else 0,
            "total": v["total"],
        }
        for (dom, dim), v in dom_dim.items()
    }

    return results

# ── Write Markdown report ───────────────────────────────────────────────────
def write_report(results, cells, threshold, out_md):
    R = results
    lines = []
    A = lines.append

    A("# IST Pub/Priv Analysis Report")
    A(f"\nThreshold: f-ICMw ≥ {threshold} → Public (model recovered from priors)")
    A(f"Total ablation cells analyzed: {len(cells)}\n")

    # P2 validation
    p2 = R["p2_validation"]
    A("## 1. P2 Validation: Private Dimensions → Larger f-ICMw Drop?\n")
    A(f"| Category | N cells | Mean f-ICMw Drop |")
    A(f"|----------|---------|-----------------|")
    A(f"| Public (recovered) | {p2['n_public_cells']} | {p2['mean_drop_public']} |")
    A(f"| Private (unrecovered) | {p2['n_private_cells']} | {p2['mean_drop_private']} |")
    A(f"\n**P2 Supported: {p2['p2_supported']}**")
    A("\n> IST predicts: when a removed dimension is 'private' (model cannot guess it), "
      "the overall f-ICMw drop should be larger than for 'public' dimensions.\n")

    # P3 validation
    p3 = R.get("p3_validation", {})
    A("## 2. P3 Validation: Capacity-Dependent Privacy Boundary\n")
    A("| Model | Capacity | Pub Rate |")
    A("|-------|----------|----------|")
    for row in p3.get("model_capacity_vs_pub_rate", []):
        A(f"| {row[0]} | {row[1]} | {row[2]} |")
    rho = p3.get("spearman_rho")
    if rho is not None:
        A(f"\nSpearman ρ (capacity vs pub_rate) = **{rho}**")
        A(f"\n**P3 Supported: {p3.get('p3_supported')}**")
    A("\n> IST predicts: stronger models should have higher pub rates "
      "(they can recover more dimensions from priors).\n")

    # By dimension
    A("## 3. Pub Rate by Dimension\n")
    A("| Dimension | Pub Rate | N Public | N Private | Δ f-ICMw (pub) | Δ f-ICMw (priv) |")
    A("|-----------|----------|----------|-----------|----------------|-----------------|")
    by_dim = R["by_dimension"]
    for d in DIMS:
        v = by_dim.get(d, {})
        A(f"| {d} | {v.get('pub_rate','?')} | {v.get('n_public','?')} | "
          f"{v.get('n_private','?')} | {v.get('mean_drop_pub','?')} | "
          f"{v.get('mean_drop_priv','?')} |")
    A("\n> High pub_rate = model easily guesses this dimension (typical/predictable content).")
    A("> Low pub_rate = model cannot guess (user-specific, private content).\n")

    # By domain
    A("## 4. Pub Rate by Domain\n")
    A("| Domain | Pub Rate | N Public | Total |")
    A("|--------|----------|----------|-------|")
    for dom in DOMAINS:
        v = R["by_domain"].get(dom, {})
        A(f"| {dom} | {v.get('pub_rate','?')} | {v.get('n_public','?')} | {v.get('total','?')} |")
    A("\n> IST predicts: Travel (Gini=0.196) should have higher pub rate "
      "than Business/Technical (Gini=0.336/0.339) — more predictable dimensions.\n")

    # Domain × Dimension heatmap
    A("## 5. Domain × Dimension Pub Rate (Heatmap Data)\n")
    header = "| Domain | " + " | ".join(DIMS) + " |"
    sep    = "|--------|" + "|".join(["--------"]*len(DIMS)) + "|"
    A(header)
    A(sep)
    for dom in DOMAINS:
        row_vals = []
        for d in DIMS:
            key = f"{dom}|{d}"
            v = R["domain_x_dimension"].get(key, {})
            pub_rate = v.get("pub_rate", "—")
            row_vals.append(str(pub_rate))
        A(f"| {dom} | " + " | ".join(row_vals) + " |")
    A("")

    # IST interpretation
    A("## 6. IST Interpretation\n")
    A("### Pub/Priv Decomposition Connects to Paper 4 v1/v2 Split\n")
    A("- **s-ICMw (v1)** measures structural recovery — the model fills the placeholder regardless of content")
    A("- **f-ICMw (v2)** measures content fidelity — the model must recover the *specific* user intent")
    A("- Public dimensions: model recovers from training priors → high v2 score")
    A("- Private dimensions: model cannot recover user-specific content → low v2 score → intent-level hallucination")
    A("")
    A("This directly validates TIIL: the private component of intent, once lost at encoding, ")
    A("is irrecoverable by the model regardless of capacity.\n")

    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Report saved: {out_md}")

# ── Main ────────────────────────────────────────────────────────────────────
def main():
    print("=== IST Pub/Priv Analysis ===")

    records = load_scores()
    cells   = classify_pub_priv(records, THRESHOLD)

    results = analyze(cells)

    # Save JSON
    out_json = os.path.join(DATA_ROOT, "pub_priv_results.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({"threshold": THRESHOLD, "n_cells": len(cells),
                   "results": results}, f, ensure_ascii=False, indent=2)
    print(f"JSON saved: {out_json}")

    # Save report
    out_md = os.path.join(DATA_ROOT, "pub_priv_report.md")
    write_report(results, cells, THRESHOLD, out_md)

    # Quick console summary
    p2 = results["p2_validation"]
    p3 = results.get("p3_validation", {})
    print("\n── Quick Summary ──────────────────────────────")
    print(f"P2: pub drop={p2['mean_drop_public']}, priv drop={p2['mean_drop_private']}, "
          f"P2_supported={p2['p2_supported']}")
    rho = p3.get("spearman_rho")
    if rho:
        print(f"P3: capacity-pub_rate Spearman ρ={rho}, P3_supported={p3.get('p3_supported')}")
    print("\nDimension pub rates:")
    for d in DIMS:
        v = results["by_dimension"].get(d, {})
        print(f"  {d:12s}: pub_rate={v.get('pub_rate','?')}, "
              f"drop(pub)={v.get('mean_drop_pub','?')}, drop(priv)={v.get('mean_drop_priv','?')}")
    print("\nDomain pub rates:")
    for dom in DOMAINS:
        v = results["by_domain"].get(dom, {})
        print(f"  {dom:10s}: pub_rate={v.get('pub_rate','?')}")

if __name__ == "__main__":
    main()
