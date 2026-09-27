import { execFileSync } from 'child_process';
import fs from 'fs';

// 零引号风险的 opencli eval 载体：node mr.mjs <js文件> [--tab <id>]
const CLI = 'D:/opencli-app/dist/src/main.js';
const SESSION = 'gptreview';
const js = fs.readFileSync(process.argv[2], 'utf8');
const i = process.argv.indexOf('--tab');
const extra = i > 0 ? ['--tab', process.argv[i + 1]] : [];
process.stdout.write(
  execFileSync(process.execPath, [CLI, 'browser', SESSION, 'eval', js, ...extra],
               { encoding: 'utf8', maxBuffer: 1 << 25 }));
