import os, re, sys, subprocess, json, argparse

RULES = {
    'openai_key':     r'sk-[A-Za-z0-9]{20,}',
    'anthropic_key':  r'sk-ant-[A-Za-z0-9\-_]{20,}',
    'jwt':            r'eyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}',
    'aws_akid':       r'AKIA[0-9A-Z]{16}',
    'bearer':         r'Bearer\s+[A-Za-z0-9\-_\.]{24,}',
    'private_key':    r'-----BEGIN [A-Z ]*PRIVATE KEY-----',
    'env_assign':     r'(?i)(?:api[_-]?key|auth[_-]?token|secret|password|access[_-]?token)\s*[:=]\s*["\']([^"\']{16,})["\']',
}

WHITELIST = re.compile(r'(?:P3PASS|P11-TOKEN|CAP\d|V3R1F1ED|QM05|S-2026|D-GLOBAL|GATEWAY-BASELINE)', re.I)
TEXT_EXT = {'.py', '.md', '.json', '.jsonc', '.toml', '.yaml', '.yml', '.txt', '.cfg', '.ini', '.sh', '.mjs', '.js', '.ts'}
SKIP_DIR = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', '.pytest_cache', '.mypy_cache', 'dist', 'build', '.idea'}

COMPILED = {k: re.compile(v) for k, v in RULES.items()}


def scan_text(text, label, findings):
    for name, rx in COMPILED.items():
        for m in rx.finditer(text):
            hit = m.group(0)
            if WHITELIST.search(hit):
                continue
            findings.append({'rule': name, 'source': label})


def scan_path(root, findings, files_scanned, counter):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIR]
        for fn in filenames:
            if os.path.splitext(fn)[1].lower() not in TEXT_EXT:
                continue
            p = os.path.join(dirpath, fn)
            try:
                if os.path.getsize(p) > 2 * 1024 * 1024:
                    continue
                with open(p, 'r', encoding='utf-8', errors='ignore') as f:
                    scan_text(f.read(), os.path.relpath(p, root), findings)
                files_scanned[0] += 1
            except Exception:
                pass
            counter[0] += 1


def scan_tracked(root, findings, files_scanned, counter):
    try:
        out = subprocess.run(['git', 'ls-files', '-z'], cwd=root, capture_output=True, timeout=120)
        names = [n for n in out.stdout.decode('utf-8', 'ignore').split('\0') if n]
    except Exception:
        return False
    for n in names:
        p = os.path.join(root, n)
        if not os.path.isfile(p):
            continue
        if os.path.splitext(p)[1].lower() not in TEXT_EXT:
            continue
        try:
            if os.path.getsize(p) > 2 * 1024 * 1024:
                continue
            with open(p, 'r', encoding='utf-8', errors='ignore') as f:
                scan_text(f.read(), n, findings)
            files_scanned[0] += 1
        except Exception:
            pass
        counter[0] += 1
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', default='D:/项目')
    ap.add_argument('--state', default='D:/ai-hub-memory/projects/devel-tools/STATE.md')
    ap.add_argument('--ccswitch-log', default=os.path.expanduser('~/.cc-switch/logs/cc-switch.log'))
    ap.add_argument('--range', default='8ec04de1..HEAD')
    ap.add_argument('--out', default='')
    ap.add_argument('--tracked-only', action='store_true')
    args = ap.parse_args()

    findings = []
    files_scanned = [0]
    counter = [0]

    if args.tracked_only:
        scan_tracked(args.repo, findings, files_scanned, counter)
    else:
        scan_path(args.repo, findings, files_scanned, counter)

    if os.path.isfile(args.state):
        with open(args.state, 'r', encoding='utf-8', errors='ignore') as f:
            scan_text(f.read(), 'STATE.md', findings)
        files_scanned[0] += 1

    if os.path.isfile(args.ccswitch_log):
        with open(args.ccswitch_log, 'r', encoding='utf-8', errors='ignore') as f:
            scan_text(f.read(), 'cc-switch.log', findings)
        files_scanned[0] += 1

    git_scanned = False
    try:
        diff = subprocess.run(['git', 'log', '-p', args.range], cwd=args.repo,
                              capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=120)
        if diff.returncode == 0 and diff.stdout:
            scan_text(diff.stdout, 'git-history:%s' % args.range, findings)
            git_scanned = True
    except Exception:
        pass

    by_rule = {}
    by_src = {}
    for f in findings:
        by_rule[f['rule']] = by_rule.get(f['rule'], 0) + 1
        by_src[f['source']] = by_src.get(f['source'], 0) + 1

    by_src_sorted = sorted(by_src.items(), key=lambda x: -x[1])[:10]

    report = {
        'scan_scope': {
            'worktree': args.repo,
            'files_scanned': files_scanned[0],
            'git_history_range': args.range if git_scanned else 'NOT_SCANNED',
            'state_md': os.path.isfile(args.state),
            'ccswitch_log': os.path.isfile(args.ccswitch_log),
        },
        'rules': sorted(RULES.keys()),
        'whitelist_project_tokens': 'P3PASS|P11-TOKEN|CAPn|V3R1F1ED|QM05|S-2026|D-GLOBAL|GATEWAY-BASELINE',
        'finding_count': len(findings),
        'by_rule': by_rule,
        'top_sources_count_only': [{'source': s, 'count': c} for s, c in by_src_sorted],
        'exit_code': 0 if len(findings) == 0 else 1,
        'note': 'REDACTED — only counts are reported; no matched secret content is stored or displayed.',
    }

    txt = json.dumps(report, ensure_ascii=False, indent=2)
    print(txt)
    if args.out:
        with open(args.out, 'w', encoding='utf-8') as f:
            f.write(txt + '\n')
    sys.exit(report['exit_code'])


if __name__ == '__main__':
    main()
