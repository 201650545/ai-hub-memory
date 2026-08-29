import { execFileSync } from 'child_process';
import fs from 'fs';

const PINNED_NODE = 'C:/Users/郭永涛/.workbuddy/binaries/node/versions/22.22.2/node.exe';
const NODE = fs.existsSync(PINNED_NODE) ? PINNED_NODE : process.execPath;
const CLI = 'D:/opencli-app/dist/src/main.js';

const args = process.argv.slice(2);
const get = (k, d) => {
  const i = args.indexOf('--' + k);
  return i >= 0 && args[i + 1] ? args[i + 1] : d;
};

const SESSION = get('session', 'gptreview');
const OUT = get('out', '');
const FIRST = parseInt(get('first', '30'), 10);
const FAST = parseInt(get('fast', '10'), 10);
const MAX = parseInt(get('max', '14'), 10);

const PROBE = `(()=>{const stop=document.querySelector('[data-testid=stop-button],button[aria-label*=Stop]');const msgs=document.querySelectorAll('[data-message-author-role=assistant]');const last=msgs[msgs.length-1];const txt=last?(last.innerText||last.textContent||'').trim():'';return JSON.stringify({stop:!!stop,count:msgs.length,len:txt.length})})()`;
const EXTRACT = `(()=>{const msgs=document.querySelectorAll('[data-message-author-role=assistant]');const last=msgs[msgs.length-1];return JSON.stringify({text:(last?(last.innerText||last.textContent||'').trim():'')})})()`;

const run = js => execFileSync(NODE, [CLI, 'browser', SESSION, 'eval', js], { encoding: 'utf8', maxBuffer: 1024 * 1024 * 30 });

const parse = raw => {
  for (const l of raw.split('\n')) {
    const t = l.trim();
    if (!t || t.includes('Update available') || t.includes('npm install') || t.includes('Download:') || t.includes('Warning') || t.includes('Extension update')) continue;
    const i = t.indexOf('{'), j = t.lastIndexOf('}');
    if (i >= 0 && j > i) { try { return JSON.parse(t.slice(i, j + 1)); } catch (e) {} }
  }
  return null;
};

const sleep = s => Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, s * 1000);

let lastLen = -1;
let stable = 0;
let elapsed = 0;
let emptyStreak = 0;

for (let i = 1; i <= MAX; i++) {
  const gap = (lastLen > 0) ? FAST : FIRST;
  sleep(gap);
  elapsed += gap;

  const s = parse(run(PROBE));
  if (!s) { console.log(`[${elapsed}s] probe failed, retry`); continue; }
  console.log(`[${elapsed}s] stop=${s.stop} count=${s.count} len=${s.len}`);

  if (s.len > 0) {
    emptyStreak = 0;
    if (s.len === lastLen && !s.stop) {
      stable++;
      if (stable >= 1) {
        console.log(`STABLE & DONE in ~${elapsed}s (len=${s.len}, 连续两次一致且已停止生成)`);
        if (OUT) {
          const p = parse(run(EXTRACT));
          if (p && p.text) {
            fs.writeFileSync(OUT, p.text + '\n', { encoding: 'utf8' });
            console.log('SAVED:', OUT, 'LEN:', p.text.length);
          } else { console.log('EXTRACT_FAILED'); process.exit(3); }
        }
        process.exit(0);
      }
    } else {
      stable = 0;
    }
    lastLen = s.len;
  } else {
    emptyStreak++;
    if (emptyStreak >= 6) {
      console.log(`EMPTY_REPLY after ${elapsed}s — assistant 连续 6 次探测（约180s）均为 0 字`);
      console.log('ACTION: 按 SOP 故障处置上报用户（实例故障疑似），不自动换模型兜底');
      process.exit(4);
    }
  }
}
console.log(`TIMEOUT after ${elapsed}s — 未满足稳定判据，按 SOP 故障处置上报用户`);
process.exit(1);
