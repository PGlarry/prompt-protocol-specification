"""
pps-sdk — Official Python SDK for PPS v1.0.0
Prompt Protocol Specification (5W3H)

API:
    validate(envelope)     → {"valid": bool, "errors": list}
    policy_check(envelope) → {"pass": bool, "warnings": list, "issues": list}
    canonicalize(envelope) → "sha256:..."
    auto_fix(envelope)     → fixed envelope dict (new object)
    check(envelope)        → {"schema": ..., "policy": ..., "hash": ...}

https://github.com/PGlarry/prompt-protocol-specification/releases/tag/v1.0.0
"""

from ._validate import validate
from ._policy import policy_check
from ._canonical import canonicalize
from ._autofix import auto_fix
from ._schema import PPS_SCHEMA


def check(envelope: dict) -> dict:
    """
    Run the full PPS check pipeline: schema + policy + hash.

    Returns:
        {
            "schema":  {"valid": bool, "errors": list},
            "policy":  {"pass": bool, "warnings": list, "issues": list},
            "hash":    "sha256:...",
        }
    """
    return {
        "schema": validate(envelope),
        "policy": policy_check(envelope),
        "hash":   canonicalize(envelope),
    }


__all__ = ["validate", "policy_check", "canonicalize", "auto_fix", "check", "PPS_SCHEMA"]
__version__ = "1.0.0"
