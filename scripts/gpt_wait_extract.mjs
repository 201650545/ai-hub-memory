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
const TAB = get('tab', '');
const FIRST = parseInt(get('first', '30'), 10);
const FAST = parseInt(get('fast', '10'), 10);
const MAX = parseInt(get('max', '36'), 10);
// 正文长度下限：Extended 思考期会先稳定停在极少字符（实测 4），低于下限一律不算答完
const MIN = parseInt(get('min', '120'), 10);
// 可选尾令牌：提示词要求首末行原样输出令牌时传本参数，判据从「长度稳定」升级为「令牌已收尾」
const TOKEN = get('token', '');

const PROBE = `(()=>{const stop=document.querySelector('[data-testid=stop-button],button[aria-label*=Stop]');const msgs=document.querySelectorAll('[data-message-author-role=assistant]');const last=msgs[msgs.length-1];const txt=last?(last.innerText||last.textContent||'').trim():'';return JSON.stringify({stop:!!stop,count:msgs.length,len:txt.length,tail:txt.slice(-200).replace(/\\s+/g,' ')})})()`;
const EXTRACT = `(()=>{const msgs=document.querySelectorAll('[data-message-author-role=assistant]');const last=msgs[msgs.length-1];return JSON.stringify({text:(last?(last.innerText||last.textContent||'').trim():'')})})()`;

const run = js => execFileSync(NODE, [CLI, 'browser', SESSION, 'eval', js].concat(TAB ? ['--tab', TAB] : []), { encoding: 'utf8', maxBuffer: 1024 * 1024 * 30 });

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
let lowStreak = 0;

const save = () => {
  const p = parse(run(EXTRACT));
  if (!p || !p.text) { console.log('EXTRACT_FAILED'); process.exit(3); }
  if (OUT) {
    fs.writeFileSync(OUT, p.text + '\n', { encoding: 'utf8' });
    console.log('SAVED:', OUT, 'LEN:', p.text.length);
  }
  if (TOKEN && !p.text.includes(TOKEN)) {
    console.log(`TOKEN_MISSING: 存档已写入，但正文不含尾令牌 ${TOKEN} —— 回复可能被截断，按 SOP 上报用户，勿当作完整裁定`);
    process.exit(5);
  }
  process.exit(0);
};

for (let i = 1; i <= MAX; i++) {
  const gap = (lastLen > 0) ? FAST : FIRST;
  sleep(gap);
  elapsed += gap;

  const s = parse(run(PROBE));
  if (!s) { console.log(`[${elapsed}s] probe failed, retry`); continue; }
  const tokOk = !TOKEN || (s.tail || '').includes(TOKEN);
  console.log(`[${elapsed}s] stop=${s.stop} count=${s.count} len=${s.len} tail="${(s.tail || '').slice(-24)}"`);

  if (s.len > 0) {
    emptyStreak = 0;
    if (s.len < MIN) {
      // 思考期占位/开头残片：绝不判完成
      lowStreak++;
      stable = 0;
      lastLen = s.len;
      if (lowStreak >= 12) {
        console.log(`LOW_REPLY after ${elapsed}s — 正文始终仅 ${s.len} 字（< min=${MIN}），最后尾部："${s.tail || ''}"`);
        console.log('ACTION: 疑似实例退化/中途截断，按 SOP 上报用户；同实例重试无收益，勿自动换模型兜底');
        process.exit(4);
      }
      continue;
    }
    if (s.len === lastLen && !s.stop) {
      stable++;
      if (tokOk) {
        console.log(`STABLE & DONE in ~${elapsed}s (len=${s.len} ≥ min=${MIN}，连续两次一致、已停止生成${TOKEN ? '、尾令牌已出现' : ''})`);
        save();
      }
      console.log(`[${elapsed}s] 正文已稳定但末行令牌未出现，继续等待`);
      if (stable >= 3) {
        console.log('FALLBACK: 正文连续 3 次稳定却仍无尾令牌，按「可能漏写令牌」存档并上报');
        save();
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
console.log(`TIMEOUT after ${elapsed}s — 未满足稳定判据（min=${MIN}${TOKEN ? ', token=' + TOKEN : ''}），按 SOP 故障处置上报用户`);
process.exit(1);
