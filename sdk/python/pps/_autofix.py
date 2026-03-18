"""Automatic repair of common PPS policy violations."""

import copy
import re


def auto_fix(envelope: dict) -> dict:
    """
    Automatically repair common policy violations in a PPS envelope.
    Returns a new deep-copied envelope — does not mutate the input.

    Repairs applied (in order):
    1. Remove web_browse from tools if no_external_browse constraint present
    2. Strip injected URLs from task if browsing is forbidden
    3. Inject placeholder evidence if citations_required=true and evidence is empty
    4. Add function_call capability if fn: tools are declared but capability is missing
    5. Copy what.output_schema to how_interface.schema if format=json and schema missing
    6. Add no_pii to who.policy if gdpr is declared but no_pii is missing
    """
    env = copy.deepcopy(envelope)
    b: dict = env.setdefault("body", {})

    constraints: list = (b.get("why") or {}).get("constraints") or []
    forbid_browse = "no_external_browse" in constraints or any(
        re.search(r"禁止外部浏览|不允许外部链接|仅使用提供的证据", str(c)) for c in constraints
    )

    # Fix 1: remove web_browse from tools
    how_to_do = b.get("how_to_do")
    if forbid_browse and isinstance(how_to_do, dict) and isinstance(how_to_do.get("tools"), list):
        how_to_do["tools"] = [t for t in how_to_do["tools"] if t != "web_browse"]

    # Fix 2: strip URLs from task
    what = b.get("what") or {}
    if forbid_browse and isinstance(what.get("task"), str):
        what["task"] = re.sub(r"https?://\S+", "[URL_REMOVED]", what["task"], flags=re.I)
        b["what"] = what

    # Fix 3: inject placeholder evidence
    where = b.setdefault("where", {})
    if where.get("citations_required") is True:
        if not isinstance(where.get("evidence"), list):
            where["evidence"] = []
        if len(where["evidence"]) == 0:
            where["evidence"].append({
                "uri": "content://placeholder",
                "digest": "sha256-PLACEHOLDER",
                "title": "Placeholder Evidence",
            })

    # Fix 4: add function_call capability
    if isinstance(how_to_do, dict) and isinstance(how_to_do.get("tools"), list):
        has_fn = any(str(t).startswith("fn:") for t in how_to_do["tools"])
        if has_fn:
            who = b.setdefault("who", {})
            if not isinstance(who.get("capabilities"), list):
                who["capabilities"] = []
            if "function_call" not in who["capabilities"]:
                who["capabilities"].append("function_call")

    # Fix 5: copy output_schema to how_interface.schema
    iface = b.get("how_interface") or {}
    if iface.get("format") == "json" and not isinstance(iface.get("schema"), dict):
        output_schema = (b.get("what") or {}).get("output_schema")
        if isinstance(output_schema, dict):
            iface["schema"] = output_schema
            b["how_interface"] = iface

    # Fix 6: add no_pii policy if gdpr declared
    header_compliance = [str(x).lower() for x in (env.get("header") or {}).get("compliance") or []]
    if "gdpr" in header_compliance:
        who = b.setdefault("who", {})
        if not isinstance(who.get("policy"), list):
            who["policy"] = []
        has_no_pii = any(re.search(r"no[_-]?pii|不包含个人信息|禁止个人敏感信息", str(x), re.I)
                         for x in who["policy"])
        if not has_no_pii:
            who["policy"].append("no_pii")

    return env
