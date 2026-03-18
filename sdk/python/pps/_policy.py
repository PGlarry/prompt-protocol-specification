"""Cross-field policy checks for PPS envelopes (8 rules, REQ-040/160/175/180-183/344)."""

import re
from typing import Any


def _has_cap(caps: list, key: str) -> bool:
    if key in caps:
        return True
    if key == "web_browse":
        return any(re.search(r"浏览|web", str(c), re.I) for c in caps)
    if key == "function_call":
        return any(re.search(r"函数调用|function", str(c), re.I) for c in caps)
    return False


def policy_check(envelope: dict) -> dict:
    """
    Run the 8 cross-field policy checks.

    Returns:
        {
            "pass": bool,
            "warnings": ["..."],
            "issues": [{"type": "...", "message": "..."}],
        }
    """
    issues = []
    warnings = []

    b: dict = envelope.get("body") or {}
    governance: dict = ((b.get("how_meta") or {}).get("governance") or {})
    locks: list = governance.get("locks") or []

    # REQ-180: citations_required → evidence ≥ 1
    where: dict = b.get("where") or {}
    citations_required: bool = where.get("citations_required") is True
    evidence: list = where.get("evidence") or []
    if citations_required and len(evidence) == 0:
        issues.append({"type": "citations_missing_evidence",
                        "message": "citations_required=true but evidence is empty"})

    # REQ-344: lock pointers must start with /
    for p in locks:
        if not (isinstance(p, str) and p.startswith("/")):
            issues.append({"type": "lock_pointer_invalid",
                            "message": f"invalid lock pointer (must start with /): {p}"})

    # REQ-175: format=json → how_interface.schema required
    iface: dict = b.get("how_interface") or {}
    if iface.get("format") == "json" and not isinstance(iface.get("schema"), dict):
        issues.append({"type": "interface_json_missing_schema",
                        "message": "json interface requires how_interface.schema"})

    # REQ-181: tools ⊆ capabilities
    how_to_do: Any = b.get("how_to_do") or {}
    tools: list = (how_to_do.get("tools") or []) if isinstance(how_to_do, dict) else []
    who: dict = b.get("who") or {}
    caps: list = who.get("capabilities") or []

    for t in tools:
        t_str = str(t)
        if t_str == "web_browse" and not _has_cap(caps, "web_browse"):
            issues.append({"type": "tool_capability_missing",
                            "message": "tool web_browse requires capability web_browse"})
        elif t_str.startswith("fn:") and not _has_cap(caps, "function_call"):
            issues.append({"type": "tool_capability_missing",
                            "message": "function-like tool requires capability function_call"})
        elif not t_str.startswith("fn:") and t_str != "web_browse" and t_str not in caps:
            issues.append({"type": "tool_capability_missing",
                            "message": f"tool {t} requires capability {t}"})

    # REQ-183: no_external_browse → web_browse forbidden
    constraints: list = (b.get("why") or {}).get("constraints") or []
    forbid_browse = "no_external_browse" in constraints or any(
        re.search(r"禁止外部浏览|不允许外部链接|仅使用提供的证据", str(c)) for c in constraints
    )
    if forbid_browse and "web_browse" in tools:
        issues.append({"type": "policy_forbid_browse_tool_present",
                        "message": "no_external_browse constraint conflicts with web_browse tool"})
    task_str: str = (b.get("what") or {}).get("task") or ""
    if forbid_browse and re.search(r"https?://|www\.", task_str, re.I):
        issues.append({"type": "policy_forbid_browse_url_present",
                        "message": "no_external_browse constraint but task contains external URL"})

    # REQ-182: gdpr → no_pii
    header_compliance = [str(x).lower() for x in (envelope.get("header") or {}).get("compliance") or []]
    if "gdpr" in header_compliance:
        policy_list: list = who.get("policy") or []
        has_no_pii = any(re.search(r"no[_-]?pii|不包含个人信息|禁止个人敏感信息", str(x), re.I)
                         for x in policy_list)
        if not has_no_pii:
            issues.append({"type": "gdpr_missing_no_pii",
                            "message": "gdpr compliance requires no_pii in who.policy"})

    # REQ-160: how_much quantification (warning)
    how_much: Any = b.get("how_much") or {}
    if isinstance(how_much, dict):
        non_empty = sum(1 for v in how_much.values() if v not in (None, "", [], {}))
        if non_empty == 0:
            warnings.append("how_much has no quantification items (REQ-160)")

    # REQ-040: determinism (warning)
    decode: dict = (envelope.get("header") or {}).get("decode") or {}
    if not (decode.get("temperature") == 0 and decode.get("top_p") == 1):
        warnings.append("decode is not strictly deterministic (temperature≠0 or top_p≠1)")

    return {"pass": len(issues) == 0, "warnings": warnings, "issues": issues}
