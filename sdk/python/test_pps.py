"""pps-sdk self-test — run: python test_pps.py"""

import sys
import copy
import pps

MINIMAL = {
    "header": {
        "pps_version": "PPS-v1.0.0",
        "model": {"name": "gpt-4o", "digest": "sha256-test", "data_cutoff": "2024-01-01"},
        "decode": {"seed": 1, "temperature": 0, "top_p": 1},
        "locale": "en-US",
    },
    "body": {
        "what":      {"task": "Summarize the document"},
        "why":       {"goals": ["compress information"]},
        "who":       {"persona": "editor"},
        "when":      {"timeframe": "current"},
        "where":     {"environment": "local"},
        "how_to_do": {"paradigm": "CoT", "steps": ["read", "summarize"]},
        "how_much":  {"content_length": "200 words"},
        "how_feel":  {"tone": "neutral"},
    },
    "integrity": {"canonical_hash": ""},
}

passed = 0
failed = 0


def assert_ok(label, condition):
    global passed, failed
    if condition:
        print(f"  ✓ {label}")
        passed += 1
    else:
        print(f"  ✗ {label}", file=sys.stderr)
        failed += 1


print("\n=== pps-sdk test ===\n")

# validate
print("validate():")
v = pps.validate(MINIMAL)
assert_ok("valid envelope passes schema", v["valid"] is True)
assert_ok("errors list is empty", v["errors"] == [])

bad = {"header": {}, "body": {}, "integrity": {}}
v2 = pps.validate(bad)
assert_ok("invalid envelope fails schema", v2["valid"] is False)

# policy_check
print("\npolicy_check():")
p = pps.policy_check(MINIMAL)
assert_ok("minimal envelope passes policy", p["pass"] is True)
assert_ok("issues list is empty", p["issues"] == [])

gdpr_bad = copy.deepcopy(MINIMAL)
gdpr_bad["header"]["compliance"] = ["gdpr"]
p2 = pps.policy_check(gdpr_bad)
assert_ok("gdpr without no_pii fails policy", p2["pass"] is False)
assert_ok("correct violation type", p2["issues"][0]["type"] == "gdpr_missing_no_pii")

# canonicalize
print("\ncanonicalize():")
h1 = pps.canonicalize(MINIMAL)
assert_ok("hash starts with sha256:", h1.startswith("sha256:"))
env2 = copy.deepcopy(MINIMAL)
env2["integrity"]["canonical_hash"] = "anything"
h2 = pps.canonicalize(env2)
assert_ok("hash is stable regardless of existing canonical_hash field", h1 == h2)

# auto_fix
print("\nauto_fix():")
to_fix = copy.deepcopy(gdpr_bad)
original_policy = copy.deepcopy(to_fix.get("body", {}).get("who", {}).get("policy"))
fixed = pps.auto_fix(to_fix)
assert_ok("does not mutate input", original_policy == to_fix.get("body", {}).get("who", {}).get("policy"))
assert_ok("adds no_pii to fixed envelope", "no_pii" in (fixed["body"]["who"].get("policy") or []))

# check
print("\ncheck():")
c = pps.check(MINIMAL)
assert_ok("check returns schema dict", isinstance(c["schema"], dict))
assert_ok("check returns policy dict", isinstance(c["policy"], dict))
assert_ok("check returns hash string", isinstance(c["hash"], str))

print(f"\n=== {passed} passed, {failed} failed ===\n")
sys.exit(1 if failed > 0 else 0)
