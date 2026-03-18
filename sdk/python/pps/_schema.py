# Embedded PPS v1.0 JSON Schema (Draft 2020-12)
PPS_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "PPS Envelope (5W3H Prompt Protocol Specification)",
    "type": "object",
    "additionalProperties": False,
    "required": ["header", "body", "integrity"],
    "properties": {
        "header": {
            "type": "object", "additionalProperties": False,
            "required": ["pps_version", "model", "decode", "locale"],
            "properties": {
                "pps_version": {"type": "string", "pattern": r"^PPS-v\d+\.\d+\.\d+$"},
                "model": {
                    "type": "object", "additionalProperties": False,
                    "required": ["name", "digest", "data_cutoff"],
                    "properties": {
                        "name": {"type": "string"},
                        "digest": {"type": "string"},
                        "data_cutoff": {"type": "string"},
                        "modality": {"type": "string"},
                    },
                },
                "decode": {
                    "type": "object", "additionalProperties": False,
                    "required": ["seed", "temperature", "top_p"],
                    "properties": {
                        "seed": {"type": "integer"},
                        "temperature": {"type": "number", "minimum": 0, "maximum": 1},
                        "top_p": {"type": "number", "minimum": 0, "maximum": 1},
                        "top_k": {"type": "integer", "minimum": 0},
                        "beam_width": {"type": "integer", "minimum": 1},
                        "stop": {"type": "array", "items": {"type": "string"}},
                    },
                },
                "locale": {"type": "string"},
                "compliance": {"type": "array", "items": {"type": "string"}},
                "created_at": {"type": "string"},
                "implementation": {
                    "type": "object", "additionalProperties": True,
                    "properties": {
                        "vendor": {"type": "string"},
                        "version": {"type": "string"},
                        "origins": {"type": "array", "items": {"type": "string"}},
                    },
                },
            },
        },
        "body": {
            "type": "object", "additionalProperties": False,
            "required": ["what", "why", "who", "when", "where", "how_to_do", "how_much", "how_feel"],
            "properties": {
                "what": {
                    "type": "object", "additionalProperties": False, "required": ["task"],
                    "properties": {
                        "task": {"type": "string"},
                        "input_schema": {"type": "object"},
                        "output_schema": {"type": "object"},
                        "kpi": {"type": "array", "items": {"type": "string"}},
                    },
                },
                "why": {
                    "type": "object", "additionalProperties": False,
                    "properties": {
                        "goals": {"type": "array", "items": {"type": "string"}},
                        "constraints": {"type": "array", "items": {"type": "string"}},
                    },
                },
                "who": {
                    "type": "object", "additionalProperties": False,
                    "properties": {
                        "persona": {"type": "string"},
                        "audience": {"type": "array", "items": {"type": "string"}},
                        "roles": {"type": "array", "items": {"type": "string"}},
                        "capabilities": {"type": "array", "items": {"type": "string"}},
                        "policy": {"type": "array", "items": {"type": "string"}},
                    },
                },
                "when": {
                    "type": "object", "additionalProperties": False,
                    "properties": {
                        "timeframe": {"type": "string"},
                        "validity_window": {"type": "string"},
                        "staleness_policy": {"type": "string"},
                    },
                },
                "where": {
                    "type": "object", "additionalProperties": False,
                    "properties": {
                        "environment": {"type": "string"},
                        "evidence": {
                            "type": "array",
                            "items": {
                                "type": "object", "additionalProperties": False, "required": ["uri"],
                                "properties": {
                                    "uri": {"type": "string"},
                                    "digest": {"type": "string"},
                                    "title": {"type": "string"},
                                },
                            },
                        },
                        "jurisdiction": {"type": "array", "items": {"type": "string"}},
                        "citations_required": {"type": "boolean"},
                    },
                },
                "how_to_do": {
                    "oneOf": [
                        {"type": "string"},
                        {
                            "type": "object", "additionalProperties": True,
                            "properties": {
                                "paradigm": {"type": "string"},
                                "steps": {"type": "array", "items": {"type": "string"}},
                                "tools": {"type": "array", "items": {"type": "string"}},
                            },
                        },
                    ]
                },
                "how_much": {
                    "oneOf": [
                        {"type": "string"},
                        {"type": "object", "additionalProperties": True, "minProperties": 1},
                    ]
                },
                "how_feel": {
                    "oneOf": [
                        {"type": "string"},
                        {
                            "type": "object", "additionalProperties": True,
                            "properties": {
                                "tone": {"type": "string"},
                                "style": {"type": "string"},
                                "audience_level": {"type": "string"},
                            },
                        },
                    ]
                },
                "how_interface": {
                    "type": "object", "additionalProperties": True,
                    "properties": {
                        "format": {"type": "string", "enum": ["json", "function_call", "markdown", "text"]},
                        "schema": {"type": "object"},
                        "error_recovery": {"type": "string"},
                    },
                },
                "how_meta": {
                    "type": "object", "additionalProperties": True,
                    "properties": {
                        "governance": {
                            "type": "object",
                            "properties": {
                                "safety": {"type": "array", "items": {"type": "string"}},
                                "verification": {"type": "array", "items": {"type": "string"}},
                                "citations": {"type": "boolean"},
                                "locks": {"type": "array", "items": {"type": "string"}},
                            },
                        }
                    },
                },
            },
        },
        "integrity": {
            "type": "object", "additionalProperties": False, "required": ["canonical_hash"],
            "properties": {
                "canonical_hash": {"type": "string"},
                "signature": {"type": "string"},
                "public_key_id": {"type": "string"},
            },
        },
    },
}
