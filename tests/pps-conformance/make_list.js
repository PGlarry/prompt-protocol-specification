const fs = require('fs');

function esc(s){ return String(s||'').replace(/[\\{}%_#]/g, '\\$&'); }

const csv = fs.readFileSync('tests/pps-conformance/summary.csv','utf8').replace(/^\uFEFF/,'');
const lines = csv.trim().split(/\r?\n/).slice(1).filter(Boolean);
const items = lines.map(l => {
  const [c,s,p] = l.split(',');
  return '  \\item ' + esc(c) + ': Schema=' + esc(s) + ', Policy=' + esc(p);
}).join('\n');

const out = '\\section*{Conformance Summary (from CSV)}\n\\begin{itemize}\n' + items + '\n\\end{itemize}\n';
fs.writeFileSync('papers/PPS/conformance_table.tex', out, 'utf8');
console.log('Wrote plain list to papers/PPS/conformance_table.tex');
