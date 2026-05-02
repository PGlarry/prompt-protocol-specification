"""
Compare Judge A and Judge B outputs for Paper B Experiment 1 clean-split pilot.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict

from ist_weighting_v3_clean_common import CONDITIONS, REPORT_DIR, SCORE_ROOT_DIR, ensure_layout


def load_scores(judge_label: str):
    score_dir = SCORE_ROOT_DIR / judge_label
    rows = {}
    for score_file in sorted(score_dir.glob("*_scores.jsonl")):
        for line in score_file.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            key = (row["task_id"], row["model"], row["condition"])
            rows[key] = row
    return rows


def mean(values):
    return round(sum(values) / len(values), 4) if values else None


def compare(judge_a: str, judge_b: str):
    ensure_layout()
    left = load_scores(judge_a)
    right = load_scores(judge_b)
    overlap_keys = sorted(set(left) & set(right))
    if not overlap_keys:
        raise ValueError(f"No overlapping scored records between {judge_a} and {judge_b}.")

    per_record = []
    summary_bucket = defaultdict(lambda: {"abs_f": [], "abs_was": [], "same_was": 0, "same_f_band": 0, "n": 0})
    for key in overlap_keys:
        a = left[key]
        b = right[key]
        f_diff = round(abs(a["f_icmw"] - b["f_icmw"]), 4)
        was_diff = abs(int(a["was"]) - int(b["was"]))
        f_band_match = (
            ("low" if a["f_icmw"] < 0.67 else "mid" if a["f_icmw"] < 0.9 else "high")
            == ("low" if b["f_icmw"] < 0.67 else "mid" if b["f_icmw"] < 0.9 else "high")
        )
        row = {
            "task_id": key[0],
            "model": key[1],
            "condition": key[2],
            "domain": a["domain"],
            "judge_a_f_icmw": a["f_icmw"],
            "judge_b_f_icmw": b["f_icmw"],
            "judge_a_was": a["was"],
            "judge_b_was": b["was"],
            "abs_f_icmw_diff": f_diff,
            "abs_was_diff": was_diff,
            "same_was": a["was"] == b["was"],
            "same_f_band": f_band_match,
        }
        per_record.append(row)
        bucket = summary_bucket[(a["domain"], a["condition"])]
        bucket["abs_f"].append(f_diff)
        bucket["abs_was"].append(was_diff)
        bucket["same_was"] += 1 if row["same_was"] else 0
        bucket["same_f_band"] += 1 if row["same_f_band"] else 0
        bucket["n"] += 1

    ranking_rows = []
    rank_bucket = defaultdict(lambda: {"same_was_ranking": 0, "same_f_ranking": 0, "n": 0})
    a_task = defaultdict(dict)
    b_task = defaultdict(dict)
    for key, row in left.items():
        a_task[(row["task_id"], row["model"])][row["condition"]] = row
    for key, row in right.items():
        b_task[(row["task_id"], row["model"])][row["condition"]] = row

    for pair_key in sorted(set(a_task) & set(b_task)):
        if not all(condition in a_task[pair_key] for condition in CONDITIONS):
            continue
        if not all(condition in b_task[pair_key] for condition in CONDITIONS):
            continue
        was_rank_a = sorted(CONDITIONS, key=lambda c: (-a_task[pair_key][c]["was"], CONDITIONS.index(c)))
        was_rank_b = sorted(CONDITIONS, key=lambda c: (-b_task[pair_key][c]["was"], CONDITIONS.index(c)))
        f_rank_a = sorted(CONDITIONS, key=lambda c: (-a_task[pair_key][c]["f_icmw"], CONDITIONS.index(c)))
        f_rank_b = sorted(CONDITIONS, key=lambda c: (-b_task[pair_key][c]["f_icmw"], CONDITIONS.index(c)))
        domain = a_task[pair_key]["matched_v2"]["domain"]
        ranking_rows.append({
            "task_id": pair_key[0],
            "model": pair_key[1],
            "domain": domain,
            "was_rank_a": was_rank_a,
            "was_rank_b": was_rank_b,
            "f_rank_a": f_rank_a,
            "f_rank_b": f_rank_b,
            "same_was_ranking": was_rank_a == was_rank_b,
            "same_f_ranking": f_rank_a == f_rank_b,
        })
        bucket = rank_bucket[domain]
        bucket["same_was_ranking"] += 1 if was_rank_a == was_rank_b else 0
        bucket["same_f_ranking"] += 1 if f_rank_a == f_rank_b else 0
        bucket["n"] += 1

    condition_summary = []
    for (domain, condition), bucket in sorted(summary_bucket.items()):
        condition_summary.append({
            "domain": domain,
            "condition": condition,
            "n": bucket["n"],
            "mean_abs_f_icmw_diff": mean(bucket["abs_f"]),
            "mean_abs_was_diff": mean(bucket["abs_was"]),
            "same_was_rate": round(bucket["same_was"] / bucket["n"], 4) if bucket["n"] else None,
            "same_f_band_rate": round(bucket["same_f_band"] / bucket["n"], 4) if bucket["n"] else None,
        })

    ranking_summary = []
    for domain, bucket in sorted(rank_bucket.items()):
        ranking_summary.append({
            "domain": domain,
            "n": bucket["n"],
            "same_was_ranking_rate": round(bucket["same_was_ranking"] / bucket["n"], 4) if bucket["n"] else None,
            "same_f_ranking_rate": round(bucket["same_f_ranking"] / bucket["n"], 4) if bucket["n"] else None,
        })

    report = {
        "judge_a": judge_a,
        "judge_b": judge_b,
        "overlap_n": len(overlap_keys),
        "condition_summary": condition_summary,
        "ranking_summary": ranking_summary,
        "per_record": per_record,
        "ranking_rows": ranking_rows,
    }
    out_file = REPORT_DIR / f"interjudge_{judge_a}_vs_{judge_b}.json"
    out_file.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Inter-judge report written: {out_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare Judge A and Judge B for weighting v3_clean")
    parser.add_argument("--judge-a", default="judge_a")
    parser.add_argument("--judge-b", default="judge_b")
    args = parser.parse_args()
    compare(judge_a=args.judge_a, judge_b=args.judge_b)
