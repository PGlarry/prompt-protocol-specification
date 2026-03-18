/**
 * pps-sdk self-test
 * Run: node test.js
 */
'use strict';

const pps = require('./index');

const minimalEnvelope = {
  header: {
    pps_version: "PPS-v1.0.0",
    model: { name: "gpt-4o", digest: "sha256-test", data_cutoff: "2024-01-01" },
    decode: { seed: 1, temperature: 0, top_p: 1 },
    locale: "en-US"
  },
  body: {
    what:     { task: "Summarize the document" },
    why:      { goals: ["compress information"] },
    who:      { persona: "editor" },
    when:     { timeframe: "current" },
    where:    { environment: "local" },
    how_to_do:{ paradigm: "CoT", steps: ["read", "summarize"] },
    how_much: { content_length: "200 words" },
    how_feel: { tone: "neutral" }
  },
  integrity: { canonical_hash: "" }
};

let pass = 0;
let fail = 0;

function assert(label, condition) {
  if (condition) { console.log('  ✓', label); pass++; }
  else           { console.error('  ✗', label); fail++; }
}

console.log('\n=== pps-sdk test ===\n');

// validate
console.log('validate():');
const v = pps.validate(minimalEnvelope);
assert('valid envelope passes schema', v.valid === true);
assert('errors array is empty', v.errors.length === 0);

const bad = { header: {}, body: {}, integrity: {} };
const v2 = pps.validate(bad);
assert('invalid envelope fails schema', v2.valid === false);

// policyCheck
console.log('\npolicyCheck():');
const p = pps.policyCheck(minimalEnvelope);
assert('minimal envelope passes policy', p.pass === true);
assert('issues array is empty', p.issues.length === 0);

// GDPR violation
const gdprBad = JSON.parse(JSON.stringify(minimalEnvelope));
gdprBad.header.compliance = ['gdpr'];
const p2 = pps.policyCheck(gdprBad);
assert('gdpr without no_pii fails policy', p2.pass === false);
assert('correct violation type', p2.issues[0].type === 'gdpr_missing_no_pii');

// canonicalize
console.log('\ncanonicalize():');
const h1 = pps.canonicalize(minimalEnvelope);
assert('hash starts with sha256:', h1.startsWith('sha256:'));
const env2 = JSON.parse(JSON.stringify(minimalEnvelope));
env2.integrity.canonical_hash = 'anything';
const h2 = pps.canonicalize(env2);
assert('hash is stable regardless of existing canonical_hash field', h1 === h2);

// autoFix
console.log('\nautoFix():');
const toFix = JSON.parse(JSON.stringify(gdprBad));
const fixed = pps.autoFix(toFix);
assert('does not mutate input', !toFix.body.who.policy || !toFix.body.who.policy.includes('no_pii'));
assert('adds no_pii to fixed envelope', fixed.body.who.policy.includes('no_pii'));

// check
console.log('\ncheck():');
const c = pps.check(minimalEnvelope);
assert('check returns schema', typeof c.schema === 'object');
assert('check returns policy', typeof c.policy === 'object');
assert('check returns hash string', typeof c.hash === 'string');

console.log(`\n=== ${pass} passed, ${fail} failed ===\n`);
if (fail > 0) process.exit(1);
