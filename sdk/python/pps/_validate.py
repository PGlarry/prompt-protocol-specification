"""JSON Schema validation for PPS envelopes."""

import jsonschema
from ._schema import PPS_SCHEMA


def validate(envelope: dict) -> dict:
    """
    Validate a PPS envelope against the JSON Schema.

    Returns:
        {"valid": True, "errors": []}
        {"valid": False, "errors": [{"path": ..., "message": ...}, ...]}
    """
    validator = jsonschema.Draft202012Validator(PPS_SCHEMA)
    errors = list(validator.iter_errors(envelope))
    if not errors:
        return {"valid": True, "errors": []}
    return {
        "valid": False,
        "errors": [
            {
                "path": "/" + "/".join(str(p) for p in e.absolute_path) if e.absolute_path else "/",
                "message": e.message,
                "schema_path": list(e.absolute_schema_path),
            }
            for e in errors
        ],
    }
