/**
 * pps-sdk — Official JavaScript SDK for PPS v1.0.0
 * Prompt Protocol Specification (5W3H)
 *
 * API:
 *   validate(envelope)    → { valid, errors }
 *   policyCheck(envelope) → { pass, warnings, issues }
 *   canonicalize(envelope)→ "sha256:..."
 *   autoFix(envelope)     → fixed envelope (new object)
 *   check(envelope)       → { schema, policy, hash }
 *
 * https://github.com/PGlarry/prompt-protocol-specification/releases/tag/v1.0.0
 */

'use strict';

const crypto = require('crypto');
const Ajv = require('ajv/dist/2020');

// ─── Embedded PPS v1.0 JSON Schema ───────────────────────────────────────────
const PPS_SCHEMA = {
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "PPS Envelope (5W3H Prompt Protocol Specification)",
  "type": "object",
  "additionalProperties": false,
  "required": ["header", "body", "integrity"],
  "properties": {
    "header": {
      "type": "object", "additionalProperties": false,
      "required": ["pps_version", "model", "decode", "locale"],
      "properties": {
        "pps_version": { "type": "string", "pattern": "^PPS-v\\d+\\.\\d+\\.\\d+$" },
        "model": {
          "type": "object", "additionalProperties": false,
          "required": ["name", "digest", "data_cutoff"],
          "properties": {
            "name": { "type": "string" },
            "digest": { "type": "string" },
            "data_cutoff": { "type": "string" },
            "modality": { "type": "string" }
          }
        },
        "decode": {
          "type": "object", "additionalProperties": false,
          "required": ["seed", "temperature", "top_p"],
          "properties": {
            "seed": { "type": "integer" },
            "temperature": { "type": "number", "minimum": 0, "maximum": 1 },
            "top_p": { "type": "number", "minimum": 0, "maximum": 1 },
            "top_k": { "type": "integer", "minimum": 0 },
            "beam_width": { "type": "integer", "minimum": 1 },
            "stop": { "type": "array", "items": { "type": "string" } }
          }
        },
        "locale": { "type": "string" },
        "compliance": { "type": "array", "items": { "type": "string" } },
        "created_at": { "type": "string" },
        "implementation": {
          "type": "object", "additionalProperties": true,
          "properties": {
            "vendor": { "type": "string" },
            "version": { "type": "string" },
            "origins": { "type": "array", "items": { "type": "string" } }
          }
        }
      }
    },
    "body": {
      "type": "object", "additionalProperties": false,
      "required": ["what", "why", "who", "when", "where", "how_to_do", "how_much", "how_feel"],
      "properties": {
        "what": {
          "type": "object", "additionalProperties": false, "required": ["task"],
          "properties": {
            "task": { "type": "string" },
            "input_schema": { "type": "object" },
            "output_schema": { "type": "object" },
            "kpi": { "type": "array", "items": { "type": "string" } }
          }
        },
        "why": {
          "type": "object", "additionalProperties": false,
          "properties": {
            "goals": { "type": "array", "items": { "type": "string" } },
            "constraints": { "type": "array", "items": { "type": "string" } }
          }
        },
        "who": {
          "type": "object", "additionalProperties": false,
          "properties": {
            "persona": { "type": "string" },
            "audience": { "type": "array", "items": { "type": "string" } },
            "roles": { "type": "array", "items": { "type": "string" } },
            "capabilities": { "type": "array", "items": { "type": "string" } },
            "policy": { "type": "array", "items": { "type": "string" } }
          }
        },
        "when": {
          "type": "object", "additionalProperties": false,
          "properties": {
            "timeframe": { "type": "string" },
            "validity_window": { "type": "string" },
            "staleness_policy": { "type": "string" }
          }
        },
        "where": {
          "type": "object", "additionalProperties": false,
          "properties": {
            "environment": { "type": "string" },
            "evidence": {
              "type": "array",
              "items": {
                "type": "object", "additionalProperties": false, "required": ["uri"],
                "properties": {
                  "uri": { "type": "string" },
                  "digest": { "type": "string", "pattern": "^(sha256:)?[A-Za-z0-9_=-]{20,}$" },
                  "title": { "type": "string" }
                }
              }
            },
            "jurisdiction": { "type": "array", "items": { "type": "string" } },
            "citations_required": { "type": "boolean" }
          }
        },
        "how_to_do": {
          "oneOf": [
            { "type": "string" },
            {
              "type": "object", "additionalProperties": true,
              "properties": {
                "paradigm": { "type": "string" },
                "steps": { "type": "array", "items": { "type": "string" } },
                "tools": { "type": "array", "items": { "type": "string" } }
              }
            }
          ]
        },
        "how_much": {
          "oneOf": [
            { "type": "string" },
            {
              "type": "object",
              "additionalProperties": { "type": ["string", "number", "object", "array", "boolean", "null"] },
              "minProperties": 1
            }
          ]
        },
        "how_feel": {
          "oneOf": [
            { "type": "string" },
            {
              "type": "object", "additionalProperties": true,
              "properties": {
                "tone": { "type": "string" },
                "style": { "type": "string" },
                "audience_level": { "type": "string" }
              }
            }
          ]
        },
        "how_interface": {
          "type": "object", "additionalProperties": true,
          "properties": {
            "format": { "type": "string", "enum": ["json", "function_call", "markdown", "text"] },
            "schema": { "type": "object" },
            "error_recovery": { "type": "string" }
          }
        },
        "how_meta": {
          "type": "object", "additionalProperties": true,
          "properties": {
            "governance": {
              "type": "object",
              "properties": {
                "safety": { "type": "array", "items": { "type": "string" } },
                "verification": { "type": "array", "items": { "type": "string" } },
                "citations": { "type": "boolean" },
                "locks": { "type": "array", "items": { "type": "string" } }
              }
            }
          }
        }
      }
    },
    "integrity": {
      "type": "object", "additionalProperties": false, "required": ["canonical_hash"],
      "properties": {
        "canonical_hash": { "type": "string" },
        "signature": { "type": "string" },
        "public_key_id": { "type": "string" }
      }
    }
  }
};

// ─── AJV instance (singleton) ────────────────────────────────────────────────
const _ajv = new Ajv({ allErrors: true, strict: false, validateFormats: false });
const _validateSchema = _ajv.compile(PPS_SCHEMA);

// ─── validate ─────────────────────────────────────────────────────────────────
/**
 * Validate a PPS envelope against the JSON Schema.
 * @param {object} envelope
 * @returns {{ valid: boolean, errors: Array }}
 */
function validate(envelope) {
  const ok = _validateSchema(envelope);
  return { valid: ok, errors: ok ? [] : (_validateSchema.errors || []) };
}

// ─── policyCheck ─────────────────────────────────────────────────────────────
/**
 * Run the 8 cross-field policy checks on a PPS envelope.
 * @param {object} envelope
 * @returns {{ pass: boolean, warnings: string[], issues: Array<{type:string, message:string}> }}
 */
function policyCheck(envelope) {
  const issues = [];
  const warnings = [];
  const b = envelope.body || {};
  const governance = (b.how_meta && b.how_meta.governance) ? b.how_meta.governance : {};
  const locks = Array.isArray(governance.locks) ? governance.locks : [];

  // REQ-180: citations_required → evidence ≥ 1
  const citationsRequired = b.where && b.where.citations_required === true;
  const evidence = (b.where && Array.isArray(b.where.evidence)) ? b.where.evidence : [];
  if (citationsRequired && evidence.length === 0) {
    const msg = 'citations_required=true but evidence is empty';
    issues.push({ type: 'citations_missing_evidence', message: msg });
  }

  // REQ-344: lock pointers must be valid JSON Pointers (start with /)
  for (const p of locks) {
    if (typeof p !== 'string' || !p.startsWith('/')) {
      issues.push({ type: 'lock_pointer_invalid', message: 'invalid lock pointer (must start with /): ' + String(p) });
    }
  }

  // REQ-175: format=json → how_interface.schema required
  const iface = b.how_interface || null;
  if (iface && iface.format === 'json' && (typeof iface.schema !== 'object' || iface.schema === null)) {
    issues.push({ type: 'interface_json_missing_schema', message: 'json interface requires how_interface.schema' });
  }

  // REQ-181: tools ⊆ capabilities
  const tools = (b.how_to_do && Array.isArray(b.how_to_do.tools)) ? b.how_to_do.tools : [];
  const caps = (b.who && Array.isArray(b.who.capabilities)) ? b.who.capabilities : [];
  for (const t of tools) {
    if (t === 'web_browse' && !caps.includes('web_browse')) {
      issues.push({ type: 'tool_capability_missing', message: 'tool web_browse requires capability web_browse' });
    } else if (String(t).startsWith('fn:') && !caps.some(c => /function_call|函数调用/i.test(c))) {
      issues.push({ type: 'tool_capability_missing', message: 'function-like tool requires capability function_call' });
    } else if (!String(t).startsWith('fn:') && t !== 'web_browse' && !caps.includes(t)) {
      issues.push({ type: 'tool_capability_missing', message: `tool ${t} requires capability ${t}` });
    }
  }

  // REQ-183: no_external_browse constraint → web_browse tool forbidden
  const constraints = (b.why && Array.isArray(b.why.constraints)) ? b.why.constraints : [];
  const forbidBrowse = constraints.includes('no_external_browse') ||
    constraints.some(x => /禁止外部浏览|不允许外部链接|仅使用提供的证据/.test(String(x)));
  if (forbidBrowse && tools.includes('web_browse')) {
    issues.push({ type: 'policy_forbid_browse_tool_present', message: 'no_external_browse constraint conflicts with web_browse tool' });
  }
  const taskStr = b.what && typeof b.what.task === 'string' ? b.what.task : '';
  if (forbidBrowse && /(https?:\/\/|www\.)/i.test(taskStr)) {
    issues.push({ type: 'policy_forbid_browse_url_present', message: 'no_external_browse constraint but task contains external URL' });
  }

  // REQ-182: gdpr compliance → no_pii policy
  const headerCompliance = (envelope.header && Array.isArray(envelope.header.compliance))
    ? envelope.header.compliance.map(x => String(x).toLowerCase()) : [];
  if (headerCompliance.includes('gdpr')) {
    const hasNoPii = b.who && Array.isArray(b.who.policy) &&
      b.who.policy.some(x => /no[_-]?pii|不包含个人信息|禁止个人敏感信息/i.test(String(x)));
    if (!hasNoPii) {
      issues.push({ type: 'gdpr_missing_no_pii', message: 'gdpr compliance requires no_pii in who.policy' });
    }
  }

  // REQ-160: how_much quantification (warning)
  const hm = (b.how_much && typeof b.how_much === 'object') ? b.how_much : {};
  const nonEmpty = Object.values(hm).filter(v => v !== null && v !== undefined && v !== '').length;
  if (nonEmpty === 0) {
    warnings.push('how_much has no quantification items (REQ-160)');
  }

  // REQ-040: determinism (warning)
  const dec = envelope.header && envelope.header.decode ? envelope.header.decode : {};
  if (!(dec.temperature === 0 && dec.top_p === 1)) {
    warnings.push('decode is not strictly deterministic (temperature≠0 or top_p≠1)');
  }

  return { pass: issues.length === 0, warnings, issues };
}

// ─── canonicalize ─────────────────────────────────────────────────────────────
/**
 * Compute the canonical SHA-256 hash of a PPS envelope.
 * The integrity.canonical_hash field is excluded before hashing.
 * @param {object} envelope
 * @returns {string} "sha256:..."
 */
function canonicalize(envelope) {
  function stringify(value) {
    if (value === null) return 'null';
    const t = typeof value;
    if (t === 'number' || t === 'boolean' || t === 'string') return JSON.stringify(value);
    if (Array.isArray(value)) return '[' + value.map(stringify).join(',') + ']';
    if (t === 'object') {
      const parts = Object.keys(value).sort().map(k => JSON.stringify(k) + ':' + stringify(value[k]));
      return '{' + parts.join(',') + '}';
    }
    throw new Error('Unsupported type: ' + t);
  }

  const obj = JSON.parse(JSON.stringify(envelope));
  if (obj.integrity && 'canonical_hash' in obj.integrity) delete obj.integrity.canonical_hash;
  const canonical = stringify(obj);
  const hash = crypto.createHash('sha256').update(Buffer.from(canonical, 'utf8')).digest();
  const b64 = hash.toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
  return 'sha256:' + b64;
}

// ─── autoFix ──────────────────────────────────────────────────────────────────
/**
 * Automatically repair common policy violations in a PPS envelope.
 * Returns a new (deep-copied) envelope — does not mutate the input.
 * @param {object} envelope
 * @returns {object} fixed envelope
 */
function autoFix(envelope) {
  const env = JSON.parse(JSON.stringify(envelope));
  const b = env.body || {};

  const constraints = (b.why && Array.isArray(b.why.constraints)) ? b.why.constraints : [];
  const forbidBrowse = constraints.includes('no_external_browse') ||
    constraints.some(x => /禁止外部浏览|不允许外部链接|仅使用提供的证据/.test(String(x)));

  // Fix 1: remove web_browse from tools if browsing is forbidden
  if (forbidBrowse && b.how_to_do && Array.isArray(b.how_to_do.tools)) {
    b.how_to_do.tools = b.how_to_do.tools.filter(t => t !== 'web_browse');
  }

  // Fix 2: strip injected URLs if browsing is forbidden
  if (forbidBrowse && b.what && typeof b.what.task === 'string') {
    b.what.task = b.what.task.replace(/https?:\/\/\S+/ig, '[URL_REMOVED]');
  }

  // Fix 3: inject placeholder evidence if citations_required but empty
  if (!b.where) b.where = {};
  if (b.where.citations_required === true) {
    if (!Array.isArray(b.where.evidence)) b.where.evidence = [];
    if (b.where.evidence.length === 0) {
      b.where.evidence.push({ uri: 'content://placeholder', digest: 'sha256-PLACEHOLDER', title: 'Placeholder Evidence' });
    }
  }

  // Fix 4: add function_call capability if fn: tools declared
  if (b.how_to_do && Array.isArray(b.how_to_do.tools) && b.who) {
    const hasFn = b.how_to_do.tools.some(t => String(t).startsWith('fn:'));
    if (hasFn) {
      if (!Array.isArray(b.who.capabilities)) b.who.capabilities = [];
      if (!b.who.capabilities.includes('function_call')) b.who.capabilities.push('function_call');
    }
  }

  // Fix 5: copy output_schema to how_interface.schema if format=json and schema missing
  if (b.how_interface && b.how_interface.format === 'json') {
    if (typeof b.how_interface.schema !== 'object' || b.how_interface.schema === null) {
      if (b.what && typeof b.what.output_schema === 'object') {
        b.how_interface.schema = b.what.output_schema;
      }
    }
  }

  // Fix 6: add no_pii policy if gdpr declared
  const headerCompliance = (env.header && Array.isArray(env.header.compliance))
    ? env.header.compliance.map(x => String(x).toLowerCase()) : [];
  if (headerCompliance.includes('gdpr')) {
    if (!b.who) b.who = {};
    if (!Array.isArray(b.who.policy)) b.who.policy = [];
    if (!b.who.policy.some(x => /no[_-]?pii|不包含个人信息|禁止个人敏感信息/i.test(String(x)))) {
      b.who.policy.push('no_pii');
    }
  }

  env.body = b;
  return env;
}

// ─── check (full pipeline) ────────────────────────────────────────────────────
/**
 * Run the full PPS check pipeline: schema validation + policy checks + hash.
 * @param {object} envelope
 * @returns {{ schema: {valid, errors}, policy: {pass, warnings, issues}, hash: string }}
 */
function check(envelope) {
  return {
    schema: validate(envelope),
    policy: policyCheck(envelope),
    hash: canonicalize(envelope),
  };
}

// ─── Exports ──────────────────────────────────────────────────────────────────
module.exports = { validate, policyCheck, canonicalize, autoFix, check, PPS_SCHEMA };
