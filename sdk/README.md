# PPS SDK

Official SDK for **PPS v1.0.0** (Prompt Protocol Specification / 5W3H).

Available in JavaScript (Node.js) and Python.

---

## JavaScript SDK

### Install

```bash
# From npm (once published)
npm install pps-sdk

# From GitHub directly
npm install github:PGlarry/prompt-protocol-specification#path:sdk/js
```

### Usage

```js
const pps = require('pps-sdk');

const envelope = {
  header: {
    pps_version: "PPS-v1.0.0",
    model: { name: "gpt-4o", digest: "sha256-...", data_cutoff: "2024-01-01" },
    decode: { seed: 1, temperature: 0, top_p: 1 },
    locale: "zh-CN"
  },
  body: {
    what:      { task: "将以下内容总结为200字摘要" },
    why:       { goals: ["信息压缩"] },
    who:       { persona: "编辑" },
    when:      { timeframe: "当前会话" },
    where:     { environment: "local" },
    how_to_do: { paradigm: "CoT", steps: ["阅读", "提取要点", "生成摘要"] },
    how_much:  { content_length: "200字" },
    how_feel:  { tone: "客观" }
  },
  integrity: { canonical_hash: "" }
};

// 1. Schema validation
const { valid, errors } = pps.validate(envelope);

// 2. Policy checks (8 cross-field rules)
const { pass, warnings, issues } = pps.policyCheck(envelope);

// 3. Compute canonical hash
const hash = pps.canonicalize(envelope);

// 4. Auto-fix policy violations
const fixed = pps.autoFix(envelope);

// 5. Full pipeline at once
const result = pps.check(envelope);
// => { schema: {...}, policy: {...}, hash: "sha256:..." }
```

---

## Python SDK

### Install

```bash
# From PyPI (once published)
pip install pps-sdk

# From GitHub directly
pip install "git+https://github.com/PGlarry/prompt-protocol-specification.git#subdirectory=sdk/python"
```

### Usage

```python
import pps

envelope = {
    "header": {
        "pps_version": "PPS-v1.0.0",
        "model": {"name": "gpt-4o", "digest": "sha256-...", "data_cutoff": "2024-01-01"},
        "decode": {"seed": 1, "temperature": 0, "top_p": 1},
        "locale": "zh-CN",
    },
    "body": {
        "what":      {"task": "将以下内容总结为200字摘要"},
        "why":       {"goals": ["信息压缩"]},
        "who":       {"persona": "编辑"},
        "when":      {"timeframe": "当前会话"},
        "where":     {"environment": "local"},
        "how_to_do": {"paradigm": "CoT", "steps": ["阅读", "提取要点", "生成摘要"]},
        "how_much":  {"content_length": "200字"},
        "how_feel":  {"tone": "客观"},
    },
    "integrity": {"canonical_hash": ""},
}

# 1. Schema validation
result = pps.validate(envelope)
# => {"valid": True, "errors": []}

# 2. Policy checks (8 cross-field rules)
result = pps.policy_check(envelope)
# => {"pass": True, "warnings": [...], "issues": [...]}

# 3. Compute canonical hash
hash_str = pps.canonicalize(envelope)
# => "sha256:..."

# 4. Auto-fix policy violations
fixed = pps.auto_fix(envelope)

# 5. Full pipeline at once
result = pps.check(envelope)
# => {"schema": {...}, "policy": {...}, "hash": "sha256:..."}
```

---

## API Reference

| Function | JS | Python | Description |
|----------|----|--------|-------------|
| Schema validation | `validate(env)` | `validate(env)` | Check against PPS JSON Schema |
| Policy checks | `policyCheck(env)` | `policy_check(env)` | 8 cross-field rules (REQ-040/160/175/180-183/344) |
| Canonical hash | `canonicalize(env)` | `canonicalize(env)` | SHA-256 of sorted compact JSON |
| Auto-fix | `autoFix(env)` | `auto_fix(env)` | Repair 6 common violations |
| Full pipeline | `check(env)` | `check(env)` | Schema + policy + hash in one call |

---

## License

MIT — see [../../LICENSE](../../LICENSE)
