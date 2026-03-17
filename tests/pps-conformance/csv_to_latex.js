// Render CSV (CASE,SCHEMA,POLICY) to LaTeX table
// Usage: node tests/pps-conformance/csv_to_latex.js <input.csv> <output.tex>

const fs = require('fs');
const path = require('path');

function loadCsv(fp) {
  // Force UTF-8 and strip BOM if any
  let text = fs.readFileSync(fp, 'utf8');
  text = text.replace(/^\uFEFF/, '');
  const s = text.trim().split(/\r?\n/);
  const header = s.shift();
  const rows = s.map(line => line.split(','));
  return { header, rows };
}

function escapeLatex(str) {
  return String(str)
    .replace(/_/g, '\\_')
    .replace(/%/g, '\\%')
    .replace(/&/g, '\\&')
    .replace(/#/g, '\\#')
    .replace(/\{/g, '\\{')
    .replace(/\}/g, '\\}')
    .replace(/\^/g, '\\^{}')
    .replace(/~/g, '\\~{}');
}

function renderLatex(rows) {
  const lines = [];
  lines.push('\\begin{table}[t]');
  lines.push('  \\centering');
  lines.push('  \\small');
  lines.push('  \\begin{tabular}{lcc}');
  // Minimal markup: no hlines to avoid noalign issues across TeX setups
  lines.push('    Case & Schema & Policy \\');
  for (const r of rows) {
    const [c, s, p] = r.map(x => (x || '').replace(/[^\x20-\x7E]/g, '')); // strip non-ASCII control chars
    lines.push(`    ${escapeLatex(c)} & ${escapeLatex(s)} & ${escapeLatex(p)} \\`);
  }
  // end rows
  lines.push('  \\end{tabular}');
  lines.push('  \\caption{Conformance summary generated from CSV.}');
  lines.push('  \\label{tab:conformance-csv}');
  lines.push('\\end{table}');
  lines.push('');
  return lines.join('\n');
}

function main() {
  const input = process.argv[2];
  const output = process.argv[3];
  if (!input || !output) {
    console.error('Usage: csv_to_latex.js <input.csv> <output.tex>');
    process.exit(2);
  }
  const { rows } = loadCsv(input);
  // Remove header row if present "CASE,SCHEMA,POLICY"
  const filtered = rows.filter(r => r[0] && r[0] !== 'CASE');
  const tex = renderLatex(filtered);
  fs.writeFileSync(output, tex + '\n', 'utf8');
  console.log('Wrote LaTeX table to', output);
}

main();


