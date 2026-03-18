"""Canonical SHA-256 hash for PPS envelopes (JCS-like, keys sorted lexicographically)."""

import copy
import hashlib
import json
import base64
from typing import Any


def _stringify(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return json.dumps(value)
    if isinstance(value, str):
        return json.dumps(value)
    if isinstance(value, list):
        return "[" + ",".join(_stringify(v) for v in value) + "]"
    if isinstance(value, dict):
        parts = [json.dumps(k) + ":" + _stringify(value[k]) for k in sorted(value.keys())]
        return "{" + ",".join(parts) + "}"
    raise TypeError(f"Unsupported type: {type(value)}")


def canonicalize(envelope: dict) -> str:
    """
    Compute the canonical SHA-256 hash of a PPS envelope.
    The integrity.canonical_hash field is excluded before hashing.

    Returns:
        "sha256:<base64url>"
    """
    obj = copy.deepcopy(envelope)
    if isinstance(obj.get("integrity"), dict) and "canonical_hash" in obj["integrity"]:
        del obj["integrity"]["canonical_hash"]
    canonical = _stringify(obj)
    digest = hashlib.sha256(canonical.encode("utf-8")).digest()
    b64 = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
    return "sha256:" + b64
