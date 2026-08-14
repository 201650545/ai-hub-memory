#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ai-hub-memory pre-commit hook - memory integrity guard (GPT force-read 2026-08-14)"""

import re
import subprocess
import sys


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True)


def check_secrets(staged_names):
    patterns = [
        (r"sk-[A-Za-z0-9]{16,}", "sk- key"),
        (r"AIza[A-Za-z0-9_-]{20,}", "Google API key"),
        (r"Bearer [A-Za-z0-9._-]{20,}", "Bearer token"),
        (r"app_token[\"']?\s*[:=]\s*[\"']?[A-Za-z0-9]{15,}", "app_token"),
        (r"app_secret[\"']?\s*[:=]\s*[\"']?[A-Za-z0-9]{15,}", "app_secret"),
    ]
    hits = []
    for name in staged_names:
        low = name.lower()
        if ".example" in low or "your-" in low or "xxx" in low:
            continue
        r = git("show", ":" + name)
        if r.returncode != 0:
            continue
        for pat, desc in patterns:
            for m in re.finditer(pat, r.stdout, re.IGNORECASE):
                hits.append(name + ": " + desc + " -> " + m.group(0)[:24])
    return hits


def check_state_ids():
    head = git("show", "HEAD:STATE.md")
    if head.returncode != 0:
        return []
    old_ids = set(re.findall(r"\[(S-\d{8}-\d{2})\]", head.stdout))
    if not old_ids:
        return []
    new = git("show", ":STATE.md")
    if new.returncode != 0:
        return []
    new_ids = set(re.findall(r"\[(S-\d{8}-\d{2})\]", new.stdout))
    dropped = old_ids - new_ids
    if not dropped:
        return []
    cl = git("show", ":CHANGELOG.md")
    cl_text = cl.stdout if cl.returncode == 0 else ""
    missing = [i for i in sorted(dropped) if ("DROP " + i) not in cl_text]
    if missing:
        return ["STATE IDs removed without DROP: " + ", ".join(missing)
                + " (add 'DROP <ID> - reason' to CHANGELOG.md first)"]
    return []


def main():
    r = git("diff", "--cached", "--name-only")
    if r.returncode != 0:
        return 0
    staged = [x.strip() for x in r.stdout.splitlines() if x.strip()]
    problems = []

    hits = check_secrets(staged)
    if hits:
        problems.append("Secrets in staged content:\n" + "\n".join(hits))

    problems.extend(check_state_ids())

    if problems:
        for p in problems:
            print("[pre-commit] FAIL " + p)
        print("[pre-commit] commit blocked. Bypass: git commit --no-verify")
        return 1
    print("[pre-commit] OK memory guard passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
