import { execFileSync } from 'child_process';
import fs from 'fs';

// 零点击轮询（不用 gpt_wait_extract 的滚动/点"跳到底部"，那会刷下载）
// usage: node poll.mjs --tab <id> --out <path> [--first 30] [--fast 15] [--max 40] [--min 120]
const CLI = 'D:/opencli-app/dist/src/main.js';
const SESSION = 'gptreview';
const g = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const TAB = g('tab', ''), OUT = g('out', '');
const FIRST = +g('first', 30), FAST = +g('fast', 15), MAX = +g('max', 40), MIN = +g('min', 120);

const PROBE = '(()=>{const stop=!!document.querySelector(\'[data-testid=stop-button],button[aria-label*="Stop"]\');'
  + 'const m=document.querySelectorAll(\'[data-message-author-role=assistant]\');let txt=\'\',idx=-1;'
  + 'for(let i=m.length-1;i>=0;i--){const t=(m[i].innerText||m[i].textContent||\'\').trim();if(t){txt=t;idx=i;break;}}'
  + 'return JSON.stringify({stop,count:m.length,len:txt.length,tail:txt.slice(-120).replace(/\\s+/g,\' \')});})()';
const FULL = '(()=>{const a=document.querySelectorAll(\'[data-message-author-role=assistant]\');let best=\'\';'
  + 'for(let i=a.length-1;i>=0;i--){const t=(a[i].innerText||a[i].textContent||\'\').trim();if(t){best=t;break;}}'
  + 'return JSON.stringify({text:best});})()';

const run = (js) => execFileSync(process.execPath, [CLI, 'browser', SESSION, 'eval', js]
  .concat(TAB ? ['--tab', TAB] : []), { encoding: 'utf8', maxBuffer: 1 << 25 });
const parse = (raw) => {
  const m = String(raw).match(/\{[\s\S]*\}\s*$/);
  if (!m) return null;
  try {
    let o = JSON.parse(m[0]);
    if (typeof o === 'string') o = JSON.parse(o);
    return o;
  } catch (e) { return null; }
};
const sleep = (ms) => Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms);

let prev = -1, same = 0;
for (let i = 0; i < MAX; i++) {
  sleep((i === 0 ? FIRST : FAST) * 1000);
  const p = parse(run(PROBE));
  if (!p) { console.log(`[${i}] unparsable`); continue; }
  const done = p.len >= MIN && !p.stop && p.len === prev;
  console.log(`[${i}] stop=${p.stop} count=${p.count} len=${p.len}${p.len === prev ? ' =prev' : ''}`);
  prev = p.len;
  if (done) {
    const f = parse(run(FULL));
    const txt = (f && f.text) || '';
    if (OUT) { fs.writeFileSync(OUT, txt, 'utf8'); console.log('SAVED ' + OUT + ' chars=' + txt.length); }
    else console.log(txt);
    console.log('STABLE & DONE');
    process.exit(0);
  }
}
console.log('TIMEOUT-未收敛（不判故障，人工复核）');
process.exit(2);
