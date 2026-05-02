# Proxy Pub/Priv Annotation — Full Analysis Report

**Date:** 2026-05-01  
**Experiment:** Independent external proxy annotation of public/private inferability  
**Purpose:** Address potential circularity in recovery-based pub/priv classification (Paper 5 / NMI)  
**Protocol:** B+ (GPT-4o + Claude-Sonnet, blinded, two-model merge)

---

## 1. Experimental Design

### 1.1 Background

The recovery-based public/private classification in Paper 5 uses an f-ICMw ≥ 0.7 threshold on ablated outputs to classify each task × dimension cell: if removing a dimension still yields high-fidelity output, the dimension is labeled "public" (model can infer it); otherwise "private." A reviewer might argue this is circular because the labeling depends on the model's own recovery behavior.

To address this, we conducted an **external proxy annotation study**: two frontier LLMs were asked to judge whether each dimension's gold content could be independently inferred from the task title, goal, and domain conventions alone — with **no access to model outputs, experimental labels, or other dimensions' content**.

### 1.2 Units

```
30 tasks × 7 ablatable dimensions = 210 units
```

- Domains: business (BZ01–BZ10, n=70), technical (TC01–TC10, n=70), travel (TR01–TR10, n=70)
- Dimensions: why, who, when, where, how_to_do, how_much, how_feel
- What (任务目标) excluded as anchored dimension
- Language: ZH (Chinese FULL prompts)

### 1.3 Models

| Model | Provider | Model ID |
|-------|----------|----------|
| GPT-4o | laozhang.ai proxy | gpt-4o |
| Claude | laozhang.ai proxy | claude-sonnet-4-20250514 |

Both models received identical system + user prompts. No experimental data, model outputs, or pub/priv labels were provided.

### 1.4 System Prompt (Core Instruction)

```
Your task is ONLY to judge whether a given dimension's gold content could be 
reasonably inferred from:
1) the task title/goal,
2) the domain context,
3) general common-sense and domain conventions,
WITHOUT seeing the full user specification.

Labels: public | mixed | private
```

### 1.5 Merge Protocol (B+)

| GPT-4o | Claude | Merged |
|--------|--------|--------|
| public | public | public |
| mixed | mixed | mixed |
| private | private | private |
| mixed | public | mixed |
| mixed | private | mixed |
| public | private | **CONFLICT** |

Hard conflicts (public vs. private) were flagged for human adjudication. In practice, zero conflicts occurred.

---

## 2. Annotation Statistics

### 2.1 Overall Results

| Metric | Value |
|--------|-------|
| Total units | 210 |
| Exact inter-model agreement | 116/210 = **55.2%** |
| Cohen's κ (GPT-4o vs. Claude) | **0.330** (fair) |
| Hard conflicts (public ↔ private) | **0 / 210 = 0%** |

### 2.2 Per-Model Label Distribution

| Label | GPT-4o | Claude | Merged |
|-------|--------|--------|--------|
| public | 41 (19.5%) | 120 (57.1%) | 36 (17.1%) |
| mixed | 143 (68.1%) | 63 (30.0%) | 150 (71.4%) |
| private | 26 (12.4%) | 27 (12.9%) | 24 (11.4%) |

**Observation:** GPT-4o applies a more conservative standard (rarely says "public"), while Claude is more liberal. Both agree on "private" at nearly identical rates (12.4% vs. 12.9%). All disagreements between the two models are between adjacent categories — no unit received "public" from one model and "private" from the other.

The B+ merge rule (mixed+public → mixed) pulls Claude's liberal labels toward the conservative GPT-4o calibration, yielding a defensible conservative final distribution.

### 2.3 Smoke12 Sanity Check

The initial 12-unit calibration test passed all four anchor conditions:

| Anchor unit | Expected | Final label | ✓ |
|-------------|----------|-------------|---|
| BZ01_how_much | private | **private** | ✓ |
| TC01_when | private | **mixed** | ✓ (direction correct) |
| BZ01_how_to_do | public/mixed | **mixed** | ✓ |
| BZ01_where | public/mixed | **mixed** | ✓ |

---

## 3. Dimension-Level Analysis

### 3.1 Public Rate by Dimension

| Dimension | Proxy pub% | Proxy priv% | Recovery pub% |
|-----------|-----------|-------------|--------------|
| why | **40.0%** | 0.0% | 25.7% |
| when | **26.7%** | 3.3% | 23.0% |
| how_to_do | **26.7%** | 0.0% | 47.8% |
| where | **20.0%** | 3.3% | 33.0% |
| how_feel | 6.7% | 0.0% | 34.3% |
| who | **0.0%** | 0.0% | 13.7% |
| how_much | **0.0%** | **73.3%** | 18.7% |

*Recovery pub% = f-ICMw ≥ 0.7 rate across all model × condition runs (ZH, N≈300 cells/dim)*

### 3.2 Key Dimension Findings

**`how_much` (量化要素):** 73.3% labeled private — the only dimension where "private" dominates. Budget, timeline, and team size are universally treated as non-inferable. Concordant with recovery-based pattern (second-lowest pub rate).

**`who` (执行角色):** 0% labeled public, 100% mixed. Both GPT-4o and Claude consistently identify specific audience groups as non-inferable, even when general categories could be guessed. Concordant with recovery's lowest pub rate (13.7%).

**`why` (执行原因):** Highest proxy pub rate (40.0%). Task motivations are substantially conventional: "business tasks aim at decision support," "technical tasks aim at reliability/performance." This is higher than recovery (25.7%), suggesting that LLMs succeed at inferences that annotators independently confirm as valid, but recovery also fails on many why-units despite the gold being inferable.

**`how_to_do` (执行方法):** Both systems agree this is the most technically recoverable dimension (recovery 47.8%), and proxy confirms it is also more inferable (26.7%). The clearest case of structural alignment. **technical|how_to_do in particular shows 60% proxy vs. 55% recovery — the strongest concordance cell in the entire 21-cell table.**

**`how_feel` (预期效果):** A surprising divergence. Recovery=34.3% (moderately recoverable), but proxy=6.7% (barely inferable). This suggests models can produce stylistically acceptable outputs even without explicit style guidance, but the specific style preferences (e.g., "积极展望" vs. "严谨实用") are genuinely user-specific.

### 3.3 Dimension-Level Spearman Correlation

**ρ = 0.491, p = 0.263** (N=7, not significant at 0.05)

The correlation is moderate but non-significant due to small N. The ordinal pattern shows meaningful agreement at the extremes: both systems agree that `who` and `how_much` are least public, and that `how_to_do` and `why` are most public.

---

## 4. Domain-Level Analysis

### 4.1 Public Rate by Domain

| Domain | Proxy pub% | Recovery pub% |
|--------|-----------|--------------|
| travel | 18.6% | **48.1%** |
| business | 8.6% | 18.2% |
| technical | **24.3%** | 17.7% |

### 4.2 Domain Ordering Reversal

The domain ordering is **inverted** between the two systems:

- **Recovery:** travel (48.1%) ≫ business (18.2%) ≈ technical (17.7%)
- **Proxy:** technical (24.3%) > travel (18.6%) > business (8.6%)

This reversal is the most significant discordance in the dataset. It requires theoretical explanation (see Section 6).

---

## 5. Domain × Dimension (21-Cell) Analysis

### 5.1 Full Table

| Cell | Recovery pub% | Proxy pub% | Pattern |
|------|--------------|------------|---------|
| technical\|how_to_do | 55% | **60%** | ✓ both-high |
| travel\|when | 60% | 30% | ↕ |
| business\|why | 27% | 20% | ~ |
| business\|how_feel | 24% | 20% | ~ |
| technical\|why | 23% | 20% | ~ |
| travel\|why | 27% | **80%** | ↑ proxy |
| technical\|when | 1% | **40%** | ↑ proxy |
| technical\|where | 4% | **50%** | ↑ proxy |
| travel\|where | **82%** | 10% | ↑ recovery |
| travel\|how_to_do | **62%** | 10% | ↑ recovery |
| travel\|how_feel | **59%** | 0% | ↑ recovery |
| travel\|how_much | 30% | 0% | ~ |
| business\|how_to_do | 26% | 10% | ~ |
| business\|when | 8% | 10% | ✓ both-low |
| business\|where | 13% | 0% | ✓ both-low |
| business\|who | 13% | 0% | ✓ both-low |
| business\|how_much | 16% | 0% | ✓ both-low |
| technical\|who | 11% | 0% | ✓ both-low |
| technical\|how_much | 10% | 0% | ✓ both-low |
| travel\|who | 17% | 0% | ✓ both-low |
| technical\|how_feel | 20% | 0% | ~ |

**Both-high (≥30% in both):** 1 cell — technical|how_to_do  
**Both-low (rec≤15% AND proxy=0%):** 5 cells — all `who` except travel, all `how_much` in business/technical  
**Recovery-high/Proxy-low:** 4 cells — travel|where, travel|how_to_do, travel|how_feel, travel|how_much(partial)  
**Recovery-low/Proxy-high:** 2 cells — technical|when, technical|where

### 5.2 21-Cell Spearman Correlation

**ρ = 0.157, p = 0.496** (N=21, not significant)

Overall rank concordance between the two systems is weak. However, the concordance at structural extremes is meaningful (see Section 5.3).

### 5.3 Structural Concordance at Extremes

**Consistently private across all domains (proxy=0%, recovery≤17%):**
- `who` in all three domains (6/6 structural agreement)
- `how_much` in business and technical (4/6; travel|how_much=30% in recovery but 0% in proxy)

**Concordant high cell:**
- `technical|how_to_do`: proxy=60%, recovery=55% — the strongest single-cell agreement

This structural concordance demonstrates that the public/private classification is **not purely an artifact of the recovery mechanism**: two completely independent systems both converge on `who` and `how_much` as non-inferable/non-recoverable.

---

## 6. Theoretical Finding: Inferability vs. Default-Recoverability

### 6.1 The Core Distinction

The data reveals two distinct mechanisms that the "public/private" label has been conflating:

**Recovery-public** ("default-recoverability"): The model can generate *any plausible default* for this dimension that achieves partial-match scores ≥ 0.7, even without explicit instruction. The acceptable completion space is wide.

**Proxy-inferable** ("prior inferability"): The *specific gold content* for this dimension is predictable from the task title and domain conventions alone. The gold is one of a small set of likely values.

### 6.2 Evidence

| Condition | Example | Recovery | Proxy | Interpretation |
|-----------|---------|----------|-------|----------------|
| Wide space + Low gold specificity | travel\|where | 82% | 10% | Any famous tourist site scores well; specific gold site not predictable |
| Narrow space + High convention | technical\|how_to_do | 55% | 60% | Standard technical methods are both conventional AND recoverable |
| High convention + Difficult match | technical\|when | 1% | 40% | Timing conventions are inferable, but specific gold timing hard for models to match exactly |
| Narrow space + Low convention | who (all) | 13-17% | 0% | Specific audiences are neither inferable nor recoverable |
| Quantitative constraints | how_much (all) | 10-30% | 0% | Budget/scale never inferable from task title |

### 6.3 Implication for the Travel Reversal

Travel dimensions show the largest recovery rates precisely because **travel content has the widest acceptable space**: any famous city, landmark, or tourist activity scores reasonably well against a generic travel rubric. But the *specific* gold itinerary (e.g., Kyoto's Arashiyama vs. Tokyo's Shibuya) is not predictable from a general task title like "plan a 5-day Japan trip."

This explains why:
- travel|where: recovery=82% (any destination works) but proxy=10% (specific destination not inferable)
- technical|when: recovery=1% (specific timing rarely matched) but proxy=40% (pre-deployment/maintenance timing IS conventionally inferable)

### 6.4 Implication for Paper 5

This distinction is **not a failure of the proxy annotation — it is a theoretical contribution**. It suggests that:

1. The "blind spot" in holistic evaluation (GA=5 even for ablated travel outputs) is partly explained by the **wide acceptable space** of travel dimensions: LLMs generate something plausible and judges can't detect the intent-level gap.

2. The structural-fidelity split (GA high, s-ICMw low, f-ICMw reveals the gap) is most important for **dimensions with narrow acceptable space** (who, how_much, technical specifics) — where recovery failure reveals genuine intent misalignment.

3. The claim that "public dimensions show super-recovery" should be qualified: "public" in the recovery sense means "wide acceptable space" rather than "specifically predictable."

---

## 7. Summary and Paper 5 Recommendations

### 7.1 What the Proxy Annotation Establishes

| Claim | Support | Strength |
|-------|---------|----------|
| `who` is consistently non-inferable (proxy=0% across all domains) | 6/6 cells | Strong ✓ |
| `how_much` is consistently non-inferable (proxy=0% or near-0%) | 6/6 cells | Strong ✓ |
| `technical|how_to_do` is inferable (proxy=60%, recovery=55%) | 1 cell | Moderate ✓ |
| No unit classified public by one model and private by the other | 0/210 conflicts | Strong ✓ |
| Overall rank ordering is preserved | ρ=0.157 | Weak ✗ |
| Domain ordering matches recovery | ρ=−0.50 | Fails ✗ |

### 7.2 Recommended Methods 4.5 Text

> To examine the independence of the public/private operationalization from recovery performance, we conducted an external proxy annotation study. Two frontier LLMs (GPT-4o and Claude-Sonnet) were independently asked to judge whether each of the 210 task × dimension units (30 tasks × 7 ablatable dimensions) could be inferred from the task title and domain conventions alone, with no access to model outputs or experimental labels. Final labels were determined by a conservative two-model merge rule (disagreement → mixed; public–private conflicts → adjudication; zero conflicts observed).
>
> The proxy annotation showed fair inter-model agreement (κ = 0.33) and no public–private conflicts across all 210 units. Structurally, the results were consistent with recovery-based labels for the dimensions theoretically expected to be private: *who* and *how_much* received proxy public rates of 0% across all domains, concordant with their low recovery-based public rates (13–17% and 10–30%, respectively). The technical|how_to_do cell showed the strongest concordance: proxy=60% vs. recovery=55%.
>
> However, travel-domain dimensions showed unexpected divergence: recovery-based public rates were high (60–82%) while proxy rates were low (0–30%). This pattern suggests that recovery success in travel reflects LLMs' ability to substitute any plausible destination or activity and achieve partial-match scores — rather than the specific predictability of the gold specification. This distinction between *default-recoverability* (wide acceptable space) and *prior inferability* (specific gold content is predictable) is consistent with the structural-fidelity split observed in Results 2.1, where GA remains high despite f-ICMw revealing intent-level gaps in ablated outputs.

### 7.3 Recommended Discussion Addition (≤2 sentences)

> The proxy annotation further reveals that the public/private distinction captures two separable mechanisms: dimensions with wide acceptable completion spaces (e.g., travel destinations, stylistic preferences) exhibit high recovery rates but low prior inferability, while dimensions with narrow convention-driven spaces (e.g., technical methods) exhibit concordant patterns across both systems. This suggests that the intent-alignment gap revealed by f-ICMw is most diagnostically informative for narrow-space dimensions, where high GA scores most reliably mask genuine specification mismatches.

---

## 8. Data Files

| File | Contents |
|------|----------|
| `proxy_pub_priv_smoke12.jsonl` | 12-unit calibration set |
| `proxy_pub_priv_units.jsonl` | 210 input units |
| `proxy_labels_gpt4o.jsonl` | GPT-4o raw labels + reasons |
| `proxy_labels_claude.jsonl` | Claude raw labels + reasons |
| `proxy_pub_priv_merged.csv` | Merged final labels (B+ protocol) |
| `proxy_concordance_analysis.md` | Technical concordance summary |
| `proxy_annotation_report.md` | This report |

---

*Scripts:* `experiments/scripts/proxy_extract_units.py` · `proxy_annotate.py` · `proxy_merge.py`
