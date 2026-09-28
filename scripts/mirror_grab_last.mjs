import { execFileSync } from 'child_process';
import fs from 'fs';

const CLI = 'D:/opencli-app/dist/src/main.js';
const TAB = 'C0F33693CFFC5F334EC252A58725236B';
const OUT = 'D:/临时文件夹/_auto_orch_R1.txt';

const FULL = '(()=>{const a=document.querySelectorAll(\'[data-message-author-role=assistant]\');let best=\'\';'
  + 'for(let i=a.length-1;i>=0;i--){const t=(a[i].innerText||a[i].textContent||\'\').trim();if(t){best=t;break;}}'
  + 'const u=document.querySelectorAll(\'[data-message-author-role=user]\').length;'
  + 'return JSON.stringify({text:best,userMsgs:u});})()';

const raw = execFileSync(process.execPath, [CLI, 'browser', 'gptreview', 'eval', FULL, '--tab', TAB],
  { encoding: 'utf8', maxBuffer: 1 << 25 });
const m = raw.match(/\{[\s\S]*\}\s*$/);
if (!m) { console.log('UNPARSABLE', raw.slice(-400)); process.exit(1); }
let o = JSON.parse(m[0]);
if (typeof o === 'string') o = JSON.parse(o);
fs.writeFileSync(OUT, o.text, 'utf8');
console.log('userMsgs=' + o.userMsgs, 'saved chars=' + o.text.length);
console.log('HEAD>>>', JSON.stringify(o.text.slice(0, 260)));
console.log('TAIL>>>', JSON.stringify(o.text.slice(-260)));
