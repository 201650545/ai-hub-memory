import { execFileSync } from 'child_process';
import fs from 'fs';

// 把文件内容以 execCommand('insertText') 注入镜像站 contenteditable
// usage: node inject.mjs --file <txt> --tab <id> [--check]
const CLI = 'D:/opencli-app/dist/src/main.js';
const SESSION = 'gptreview';
const a = (k) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : ''; };
const file = a('file'), tab = a('tab');
const text = fs.readFileSync(file, 'utf8');
const js = '(()=>{const el=document.querySelector(\'[contenteditable="true"]\');'
  + 'if(!el) return JSON.stringify({ok:false,why:\'no editor\'});'
  + 'el.focus();'
  + `document.execCommand('insertText', false, ${JSON.stringify(text)});`
  + 'const t=(el.innerText||\'\');'
  + 'return JSON.stringify({ok:true,len:t.length,head:t.slice(0,30),tail:t.slice(-40)});})()';
const out = execFileSync(process.execPath, [CLI, 'browser', SESSION, 'eval', js].concat(tab ? ['--tab', tab] : []),
  { encoding: 'utf8', maxBuffer: 1 << 25 });
process.stdout.write(out);
