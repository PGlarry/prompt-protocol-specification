"""
analyze_ist_weighting_v3_clean.py
=================================
Aggregate analysis for Paper B Experiment 1 clean-split pilot.
"""

from __future__ import annotations

import argparse
import json
import logging
from collections import defaultdict

from ist_weighting_v3_clean_common import AUDIT_DIR, CONDITIONS, REPORT_DIR, SCORE_ROOT_DIR, ensure_layout

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


def mean(values):
    return round(sum(values) / len(values), 4) if values else None


def load_records(score_dir, domain_filter: str, model_filter: str):
    records = []
    for score_file in sorted(score_dir.glob("*_scores.jsonl")):
        for line in score_file.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            if domain_filter != "all" and record["domain"] != domain_filter:
                continue
            if model_filter != "all" and record["model"] != model_filter:
                continue
            records.append(record)
    return records


def analyze(domain_filter: str, model_filter: str, judge_label: str, lang: str = "zh"):
    if lang != "zh":
        raise ValueError("Current weighting v3_clean analysis is configured for zh only.")

    ensure_layout()
    score_dir = SCORE_ROOT_DIR / judge_label
    records = load_records(score_dir, domain_filter, model_filter)
    if not records:
        raise ValueError(f"No scored weighting v3_clean records found in {score_dir}. Run judge_ist_weighting_v3_clean.py first.")

    condition_buckets = defaultdict(lambda: defaultdict(list))
    task_condition_buckets = defaultdict(dict)

    for record in records:
        key = (record["domain"], record["model"], record["condition"])
        task_key = (record["domain"], record["model"], record["task_id"])
        condition_buckets[key]["ga"].append(record.get("ga"))
        condition_buckets[key]["s_icmw"].append(record.get("s_icmw"))
        condition_buckets[key]["f_icmw"].append(record.get("f_icmw"))
        condition_buckets[key]["was"].append(record.get("was"))
        task_condition_buckets[task_key][record["condition"]] = record

    condition_means = []
    for (domain, model, condition), metrics in sorted(condition_buckets.items()):
        condition_means.append({
            "domain": domain,
            "model": model,
            "condition": condition,
            "mean_ga": mean([value for value in metrics["ga"] if value is not None]),
            "mean_s_icmw": mean([value for value in metrics["s_icmw"] if value is not None]),
            "mean_f_icmw": mean([value for value in metrics["f_icmw"] if value is not None]),
            "mean_was": mean([value for value in metrics["was"] if value is not None]),
            "n": len(metrics["ga"]) or len(metrics["s_icmw"]),
        })

    comparisons = [
        ("matched_v2", "uniform_v2"),
        ("matched_v2", "mismatched_v2"),
        ("matched_v2", "perturbed_v2"),
        ("uniform_v2", "mismatched_v2"),
        ("uniform_v2", "perturbed_v2"),
        ("perturbed_v2", "mismatched_v2"),
    ]
    paired_diffs = []
    ranking_rows = []
    for (domain, model, task_id), rows in sorted(task_condition_buckets.items()):
        if not all(condition in rows for condition in CONDITIONS):
            continue
        ranking_rows.append({
            "domain": domain,
            "model": model,
            "task_id": task_id,
            "was_ranking": sorted(CONDITIONS, key=lambda c: (-rows[c]["was"], CONDITIONS.index(c))),
            "f_icmw_ranking": sorted(CONDITIONS, key=lambda c: (-rows[c]["f_icmw"], CONDITIONS.index(c))),
        })
        for left, right in comparisons:
            paired_diffs.append({
                "domain": domain,
                "model": model,
                "task_id": task_id,
                "comparison": f"{left}_minus_{right}",
                "delta_s_icmw": round(rows[left]["s_icmw"] - rows[right]["s_icmw"], 4),
                "delta_f_icmw": round(rows[left]["f_icmw"] - rows[right]["f_icmw"], 4),
                "delta_was": round(rows[left]["was"] - rows[right]["was"], 4),
                "delta_ga": round(rows[left]["ga"] - rows[right]["ga"], 4),
            })

    summary_buckets = defaultdict(lambda: defaultdict(list))
    for row in paired_diffs:
        key = (row["domain"], row["model"], row["comparison"])
        for metric in ["delta_s_icmw", "delta_f_icmw", "delta_was", "delta_ga"]:
            summary_buckets[key][metric].append(row[metric])

    paired_summary = []
    for (domain, model, comparison), metrics in sorted(summary_buckets.items()):
        paired_summary.append({
            "domain": domain,
            "model": model,
            "comparison": comparison,
            "mean_delta_s_icmw": mean(metrics["delta_s_icmw"]),
            "mean_delta_f_icmw": mean(metrics["delta_f_icmw"]),
            "mean_delta_was": mean(metrics["delta_was"]),
            "mean_delta_ga": mean(metrics["delta_ga"]),
            "n": len(metrics["delta_s_icmw"]),
        })

    prs_summary_path = AUDIT_DIR / "prs_condition_summary.json"
    prs_summary = json.loads(prs_summary_path.read_text(encoding="utf-8")) if prs_summary_path.exists() else None

    report = {
        "lang": lang,
        "judge_label": judge_label,
        "condition_means": condition_means,
        "paired_summary": paired_summary,
        "paired_diffs": paired_diffs,
        "ranking_rows": ranking_rows,
        "prs_summary": prs_summary,
    }
    out_file = REPORT_DIR / f"analysis_results_{judge_label}.json"
    out_file.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    log.info("\n%s", "=" * 84)
    log.info("Condition Means (%s)", judge_label)
    log.info("%-10s %-8s %-16s %-8s %-8s %-8s %-8s", "Domain", "Model", "Condition", "sICMw", "fICMw", "WAS", "GA")
    log.info("%s", "-" * 84)
    for row in condition_means:
        log.info(
            "%-10s %-8s %-16s %-8s %-8s %-8s %-8s",
            row["domain"],
            row["model"],
            row["condition"],
            str(row["mean_s_icmw"]),
            str(row["mean_f_icmw"]),
            str(row["mean_was"]),
            str(row["mean_ga"]),
        )

    log.info("\n%s", "=" * 84)
    log.info("Paired Differences (%s)", judge_label)
    log.info("%-10s %-8s %-34s %-8s %-8s %-8s %-8s", "Domain", "Model", "Comparison", "Δs", "Δf", "ΔWAS", "ΔGA")
    log.info("%s", "-" * 84)
    for row in paired_summary:
        log.info(
            "%-10s %-8s %-34s %-8s %-8s %-8s %-8s",
            row["domain"],
            row["model"],
            row["comparison"],
            str(row["mean_delta_s_icmw"]),
            str(row["mean_delta_f_icmw"]),
            str(row["mean_delta_was"]),
            str(row["mean_delta_ga"]),
        )

    log.info("\nAnalysis written: %s", out_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Paper B weighting analysis v3_clean")
    parser.add_argument("--lang", choices=["zh"], default="zh")
    parser.add_argument("--domain", choices=["business", "technical", "all"], default="all")
    parser.add_argument("--model", choices=["deepseek", "qwen", "kimi", "all"], default="all")
    parser.add_argument("--judge-label", default="judge_a")
    args = parser.parse_args()
    analyze(domain_filter=args.domain, model_filter=args.model, judge_label=args.judge_label, lang=args.lang)
