"""
analyze_ist_ablation.py
=======================
IST Validation Experiment 1: Statistical Analysis
--------------------------------------------------
Reads scored outputs and tests three hypotheses:

  H1: High-weight dimension removal → greater GA drop than low-weight removal
  H2: High-weight dimension removal → greater ICMw drop than low-weight removal
  H3: Removing dim X → deficiency signature for X is present in output

Key output:
  - Spearman ρ between predicted weight rank and observed severity rank
  - Effect sizes (Cohen's d) for high- vs. low-weight contrasts
  - DS match rate per domain × dimension

Usage:
    python scripts/analyze_ist_ablation.py
    python scripts/analyze_ist_ablation.py --domain travel --model claude
"""

import json, argparse, logging
from pathlib import Path
from collections import defaultdict

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s",
                    datefmt="%H:%M:%S")
log = logging.getLogger(__name__)

BASE_DIR   = Path(__file__).parent.parent
IST_DIR    = BASE_DIR / "01_ablation"

def get_task_file(lang: str) -> Path:
    if lang == "zh":
        return IST_DIR / "tasks" / "tasks.json"
    return IST_DIR / "tasks" / f"tasks_{lang}.json"

# Version-aware score/report dirs — set by --version and --lang args
def get_dirs(version: str, lang: str = "zh"):
    lang_suffix = "" if lang == "zh" else f"_{lang}"
    if version == "v1":
        score_dir  = IST_DIR / f"scores_v1{lang_suffix}"
        report_dir = IST_DIR / f"reports_v1{lang_suffix}"
    elif version == "v2":
        score_dir  = IST_DIR / "scores" / ("zh" if lang == "zh" else lang)
        report_dir = IST_DIR / f"reports_v2{lang_suffix}"
    else:
        score_dir  = IST_DIR / "scores" / ("zh" if lang == "zh" else lang)
        report_dir = IST_DIR / f"reports{lang_suffix}"
    report_dir.mkdir(parents=True, exist_ok=True)
    return score_dir, report_dir

ABLATION_DIMS = ["why", "who", "when", "where", "how_to_do", "how_much", "how_feel"]


def load_scores(domain_filter="all", model_filter="all", score_dir=None):
    records = []
    for f in sorted(score_dir.glob("*_scores.jsonl")):
        for line in f.read_text(encoding="utf-8").strip().split("\n"):
            if not line.strip():
                continue
            try:
                r = json.loads(line)
                if domain_filter != "all" and r.get("domain") != domain_filter:
                    continue
                if model_filter != "all" and r.get("model") != model_filter:
                    continue
                records.append(r)
            except:
                pass
    return records


def spearman_r(x, y):
    """Compute Spearman rank correlation."""
    n = len(x)
    if n < 2:
        return None, None
    def ranks(seq):
        s = sorted(enumerate(seq), key=lambda t: t[1])
        r = [0] * n
        for rank, (idx, _) in enumerate(s, 1):
            r[idx] = rank
        return r
    rx, ry = ranks(x), ranks(y)
    d2 = sum((rx[i] - ry[i])**2 for i in range(n))
    rho = 1 - 6 * d2 / (n * (n**2 - 1))
    # Approximate p-value (t-distribution, df=n-2)
    import math
    if abs(rho) == 1.0:
        return rho, 0.0
    t_stat = rho * math.sqrt(n - 2) / math.sqrt(1 - rho**2)
    # Simple two-tailed approximation
    return rho, t_stat


def cohen_d(group1, group2):
    """Cohen's d effect size."""
    import math, statistics
    if not group1 or not group2:
        return None
    m1, m2 = statistics.mean(group1), statistics.mean(group2)
    s1 = statistics.stdev(group1) if len(group1) > 1 else 0
    s2 = statistics.stdev(group2) if len(group2) > 1 else 0
    pooled = math.sqrt((s1**2 + s2**2) / 2) if (s1 or s2) else 1e-9
    return (m1 - m2) / pooled


def analyze(domain_filter="all", model_filter="all", version="v1", lang="zh"):
    score_dir, report_dir = get_dirs(version, lang)
    records = load_scores(domain_filter, model_filter, score_dir=score_dir)
    if not records:
        log.error("No scored records found. Run judge_ist_ablation.py first.")
        return

    log.info(f"Loaded {len(records)} scored records (lang={lang})")

    task_file     = get_task_file(lang)
    tasks_data    = json.loads(task_file.read_text(encoding="utf-8"))
    prior_weights = tasks_data["prior_weights"]

    # ── Build per-task GA/ICMw for FULL and each ablation ─────────────────
    # Structure: {(task_id, model): {condition: {ga, icmw}}}
    task_model_data: dict = defaultdict(lambda: defaultdict(dict))
    for r in records:
        task_model_data[(r["task_id"], r["model"])][r["condition"]] = {
            "domain":    r["domain"],
            "ga":        r.get("ga"),
            "icmw":      r.get("icmw"),
            "ds":        r.get("ds"),
            "removed_dim": r.get("removed_dim"),
        }

    # ── Compute drops per (task_id, model, removed_dim) ───────────────────
    drops = []  # list of dicts
    for (task_id, model), cond_map in task_model_data.items():
        full = cond_map.get("FULL", {})
        if not full.get("ga"):
            continue
        domain = full.get("domain") or next(
            (v.get("domain") for v in cond_map.values() if v.get("domain")), "")

        for dim in ABLATION_DIMS:
            abl = cond_map.get(f"-{dim}", {})
            if abl.get("ga") is None:
                continue
            weight = prior_weights.get(domain, {}).get(dim, 0.0)
            drops.append({
                "task_id":     task_id,
                "domain":      domain,
                "model":       model,
                "dim":         dim,
                "weight":      weight,
                "ga_full":     full.get("ga"),
                "ga_abl":      abl.get("ga"),
                "ga_drop":     (full.get("ga") or 0) - (abl.get("ga") or 0),
                "icmw_full":   full.get("icmw"),
                "icmw_abl":    abl.get("icmw"),
                "icmw_drop":   (full.get("icmw") or 0) - (abl.get("icmw") or 0),
                "ds":          abl.get("ds"),
            })

    if not drops:
        log.error("No ablation drops computable (need FULL + ablated conditions scored).")
        return

    log.info(f"Computed {len(drops)} ablation drops")

    # ── H1 / H2: Spearman ρ between weight rank and severity rank ─────────
    report_rows = []

    for domain in (["travel", "business", "technical"]
                   if domain_filter == "all" else [domain_filter]):
        d_drops = [d for d in drops if d["domain"] == domain]
        if not d_drops:
            continue

        for model in (set(d["model"] for d in d_drops)):
            m_drops = [d for d in d_drops if d["model"] == model]
            if not m_drops:
                continue

            # Mean GA drop and ICMw drop per dim (across tasks)
            dim_stats: dict = defaultdict(lambda: {"ga_drops": [], "icmw_drops": [], "weights": []})
            for d in m_drops:
                dim_stats[d["dim"]]["ga_drops"].append(d["ga_drop"])
                dim_stats[d["dim"]]["icmw_drops"].append(d["icmw_drop"])
                dim_stats[d["dim"]]["weights"].append(d["weight"])

            dims = sorted(dim_stats.keys())
            weights   = [dim_stats[d]["weights"][0] for d in dims]  # same per domain
            mean_ga   = [sum(dim_stats[d]["ga_drops"]) / len(dim_stats[d]["ga_drops"]) for d in dims]
            mean_icmw = [sum(dim_stats[d]["icmw_drops"]) / len(dim_stats[d]["icmw_drops"]) for d in dims]

            rho_ga,   t_ga   = spearman_r(weights, mean_ga)
            rho_icmw, t_icmw = spearman_r(weights, mean_icmw)

            # High-weight dims (top 3 by weight) vs low-weight (bottom 3)
            sorted_dims = sorted(dims, key=lambda d: dim_stats[d]["weights"][0], reverse=True)
            hi = sorted_dims[:3]
            lo = sorted_dims[-3:]
            hi_ga_drops = [d2["ga_drop"] for d in drops if d["domain"] == domain
                           and d["model"] == model and d["dim"] in hi for d2 in [d]]
            lo_ga_drops = [d2["ga_drop"] for d in drops if d["domain"] == domain
                           and d["model"] == model and d["dim"] in lo for d2 in [d]]
            cd = cohen_d(hi_ga_drops, lo_ga_drops)

            row = {
                "domain": domain,
                "model":  model,
                "n_tasks": len(set(d["task_id"] for d in m_drops)),
                "rho_ga":   round(rho_ga, 3)   if rho_ga   else None,
                "t_ga":     round(t_ga, 3)     if t_ga     else None,
                "rho_icmw": round(rho_icmw, 3) if rho_icmw else None,
                "t_icmw":   round(t_icmw, 3)   if t_icmw   else None,
                "cohen_d_ga": round(cd, 3)     if cd       else None,
                "hi_dims": hi,
                "lo_dims": lo,
                "dim_mean_ga_drop":   {d: round(mean_ga[i], 3)   for i, d in enumerate(dims)},
                "dim_mean_icmw_drop": {d: round(mean_icmw[i], 3) for i, d in enumerate(dims)},
                "dim_weights":        {d: weights[i] for i, d in enumerate(dims)},
            }
            report_rows.append(row)

            log.info(f"\n{'─'*55}")
            log.info(f"Domain={domain}, Model={model}, N_tasks={row['n_tasks']}")
            log.info(f"  H1 (Spearman ρ weight vs GA drop):   ρ={row['rho_ga']}, t={row['t_ga']}")
            log.info(f"  H2 (Spearman ρ weight vs ICMw drop): ρ={row['rho_icmw']}, t={row['t_icmw']}")
            log.info(f"  Cohen's d (hi-w vs lo-w GA drop):    d={row['cohen_d_ga']}")
            log.info(f"  Dim GA drops (desc):")
            for d in sorted(dims, key=lambda d2: -dim_stats[d2]["ga_drops"][0] if dim_stats[d2]["ga_drops"] else 0):
                log.info(f"    {d:<12} w={dim_stats[d]['weights'][0]:.2f}  "
                         f"mean_GA_drop={row['dim_mean_ga_drop'][d]:+.3f}  "
                         f"mean_ICMw_drop={row['dim_mean_icmw_drop'][d]:+.3f}")

    # ── H3: Deficiency Signature match rate ───────────────────────────────
    log.info(f"\n{'─'*55}")
    log.info("H3: Deficiency Signature match rates")
    ds_stats: dict = defaultdict(lambda: {"scores": [], "n": 0})
    for d in drops:
        if d["ds"] is not None:
            key = (d["domain"], d["dim"], d["model"])
            ds_stats[key]["scores"].append(d["ds"])
            ds_stats[key]["n"] += 1

    for (domain, dim, model), vals in sorted(ds_stats.items()):
        mean_ds = sum(vals["scores"]) / len(vals["scores"]) if vals["scores"] else None
        log.info(f"  {domain:<10} -{dim:<12} {model:<8} mean_DS={mean_ds:.3f}  n={vals['n']}")

    # ── Save report ────────────────────────────────────────────────────────
    report = {
        "hypotheses": report_rows,
        "drops": drops,
    }
    out = report_dir / "analysis_results.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info(f"\nFull report saved: {out}")

    # Print final summary table for the paper
    log.info("\n" + "="*70)
    log.info("KEY RESULTS TABLE (for paper)")
    log.info(f"{'Domain':<10} {'Model':<8} {'ρ_GA':>6} {'ρ_ICMw':>7} {'d':>6} {'Verdict'}")
    log.info("-" * 70)
    for r in report_rows:
        verdict = ("✓ H1+H2 supported" if (r["rho_ga"] or 0) > 0.5 else
                   "~ partial" if (r["rho_ga"] or 0) > 0 else "✗ not supported")
        log.info(f"{r['domain']:<10} {r['model']:<8} {str(r['rho_ga']):>6} "
                 f"{str(r['rho_icmw']):>7} {str(r['cohen_d_ga']):>6}  {verdict}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IST Ablation Analysis")
    parser.add_argument("--lang", choices=["zh", "en", "ja"], default="zh",
                        help="Task language (zh=default Chinese, en=English, ja=Japanese)")
    parser.add_argument("--domain", choices=["travel", "business", "technical", "all"],
                        default="all")
    parser.add_argument("--model", choices=["claude", "gemini", "gpt4o", "deepseek", "qwen", "kimi", "all"],
                        default="all")
    parser.add_argument("--version", choices=["v1", "v2"], default="v1",
                        help="v1=Structural ICMw (s-ICMw), v2=Fidelity ICMw (f-ICMw)")
    args = parser.parse_args()

    analyze(domain_filter=args.domain, model_filter=args.model,
            version=args.version, lang=args.lang)
