"""
proxy_merge.py
==============
Merge GPT-4o and Claude proxy annotation results.
Applies merge rules, flags conflicts, outputs analysis.

Merge rules (B+ protocol):
  public + public  → public
  mixed  + mixed   → mixed
  private+ private → private
  mixed  + public  → mixed
  mixed  + private → mixed
  public + private → CONFLICT (adjudication_needed=True)

Output:
  proxy_pub_priv_merged.csv     — full merged table
  proxy_pub_priv_analysis.md    — statistics & comparison with recovery-based labels

Usage:
    python scripts/proxy_merge.py --mode smoke
    python scripts/proxy_merge.py --mode full
    python scripts/proxy_merge.py --mode full --recovery-labels path/to/labels.csv
"""

import json, argparse, csv
from pathlib import Path
from collections import Counter, defaultdict

DATA_DIR = Path(__file__).parent.parent / "data" / "proxy_pub_priv"

MERGE_RULES = {
    ("public",  "public"):  "public",
    ("mixed",   "mixed"):   "mixed",
    ("private", "private"): "private",
    ("mixed",   "public"):  "mixed",
    ("public",  "mixed"):   "mixed",
    ("mixed",   "private"): "mixed",
    ("private", "mixed"):   "mixed",
    ("public",  "private"): "conflict",
    ("private", "public"):  "conflict",
}


def load_labels(path: Path) -> dict:
    labels = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            labels[r["unit_id"]] = r
    return labels


def merge_label(l1: str, l2: str) -> tuple[str, bool]:
    key = (l1, l2)
    merged = MERGE_RULES.get(key, "conflict")
    return merged, merged == "conflict"


def load_units(mode: str) -> list[dict]:
    fname = "proxy_pub_priv_smoke12.jsonl" if mode == "smoke" \
            else "proxy_pub_priv_units.jsonl"
    path = DATA_DIR / fname
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def run_merge(mode: str, recovery_path: Path | None = None):
    gpt_path    = DATA_DIR / "proxy_labels_gpt4o.jsonl"
    claude_path = DATA_DIR / "proxy_labels_claude.jsonl"

    missing = [p for p in [gpt_path, claude_path] if not p.exists()]
    if missing:
        raise FileNotFoundError(f"Missing label files: {missing}")

    units      = {u["unit_id"]: u for u in load_units(mode)}
    gpt_labels  = load_labels(gpt_path)
    claude_labels = load_labels(claude_path)

    # Filter to units that appear in both
    common_ids = set(units) & set(gpt_labels) & set(claude_labels)
    print(f"Units with both labels: {len(common_ids)}")

    rows = []
    for uid in sorted(common_ids):
        u  = units[uid]
        g  = gpt_labels[uid]
        c  = claude_labels[uid]
        final, conflict = merge_label(g["label"], c["label"])

        rows.append({
            "unit_id":           uid,
            "task_id":           u["task_id"],
            "domain":            u["domain"],
            "dimension":         u["dimension"],
            "task_title_short":  u["task_title_short"],
            "gold_dimension_value": u["gold_dimension_value"],
            "label_gpt4o":       g["label"],
            "conf_gpt4o":        g.get("confidence", ""),
            "reason_gpt4o":      g.get("reason", ""),
            "label_claude":      c["label"],
            "conf_claude":       c.get("confidence", ""),
            "reason_claude":     c.get("reason", ""),
            "proxy_final_label": final,
            "adjudication_needed": conflict,
            "adjudicator_label": "",
            "adjudicator_note":  "",
        })

    # Write CSV
    out_csv = DATA_DIR / "proxy_pub_priv_merged.csv"
    if rows:
        with open(out_csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
    print(f"Merged CSV → {out_csv}")

    # Statistics
    _print_analysis(rows, mode, out_csv)


def _print_analysis(rows: list[dict], mode: str, out_csv: Path):
    lines = []
    lines.append(f"# Proxy Pub/Priv Annotation — {mode.upper()} Analysis\n")
    lines.append(f"Total units: {len(rows)}\n")

    # Agreement
    agree = sum(1 for r in rows if r["label_gpt4o"] == r["label_claude"])
    conflict = sum(1 for r in rows if r["adjudication_needed"])
    lines.append(f"## Inter-model Agreement")
    lines.append(f"- Exact agreement: {agree}/{len(rows)} = {agree/len(rows)*100:.1f}%")
    lines.append(f"- Conflicts (public vs private): {conflict}")
    lines.append("")

    # Label distribution (proxy_final)
    final_counts = Counter(r["proxy_final_label"] for r in rows)
    lines.append(f"## Final Label Distribution")
    for lbl, n in sorted(final_counts.items()):
        lines.append(f"- {lbl}: {n} ({n/len(rows)*100:.1f}%)")
    lines.append("")

    # Domain breakdown
    lines.append(f"## Domain-Level Public Rate")
    by_domain = defaultdict(list)
    for r in rows:
        by_domain[r["domain"]].append(r["proxy_final_label"])
    for domain in ["travel", "business", "technical"]:
        lbls = by_domain[domain]
        if not lbls:
            continue
        pub = sum(1 for l in lbls if l == "public")
        lines.append(f"- {domain}: public={pub}/{len(lbls)} ({pub/len(lbls)*100:.1f}%)")
    lines.append("")

    # Dimension breakdown
    lines.append(f"## Dimension-Level Public Rate")
    by_dim = defaultdict(list)
    for r in rows:
        by_dim[r["dimension"]].append(r["proxy_final_label"])
    for dim in ["how_to_do", "where", "why", "who", "when", "how_much", "how_feel"]:
        lbls = by_dim.get(dim, [])
        if not lbls:
            continue
        pub = sum(1 for l in lbls if l == "public")
        lines.append(f"- {dim:12s}: public={pub}/{len(lbls)} ({pub/len(lbls)*100:.1f}%)")
    lines.append("")

    # Smoke12 sanity check (if in smoke mode)
    if mode == "smoke":
        lines.append(f"## Smoke12 Sanity Check")
        anchors = {
            "BZ01_how_much":  "private",
            "TC01_when":      "private",
            "BZ01_how_to_do": "public/mixed",
            "BZ01_where":     "public/mixed",
        }
        for uid, expected in anchors.items():
            r = next((x for x in rows if x["unit_id"] == uid), None)
            if r:
                ok = "✓" if r["proxy_final_label"] != ("public" if "private" in expected else "private") else "?"
                lines.append(f"- {uid}: expected≈{expected} → got {r['proxy_final_label']} {ok}")
        lines.append("")

    report = "\n".join(lines)
    out_md = DATA_DIR / f"proxy_pub_priv_analysis_{mode}.md"
    out_md.write_text(report, encoding="utf-8")
    print(report)
    print(f"Analysis → {out_md}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["smoke", "full"], default="smoke")
    parser.add_argument("--recovery-labels", metavar="CSV",
                        help="Optional: path to recovery-based pub/priv labels CSV for concordance")
    args = parser.parse_args()
    run_merge(args.mode, Path(args.recovery_labels) if args.recovery_labels else None)


if __name__ == "__main__":
    main()
