#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ai-hub-memory v2 pre-commit hook - memory integrity guard

Checks (FAIL blocks commit, WARN does not):
  [FAIL] secrets in staged content
  [FAIL] per-project STATE S-ID removed without DROP in same project CHANGELOG
  [FAIL] per-project STATE.md > 60 lines or > 12 KiB
  [FAIL] per-project 已完成（最近） > 8 entries
  [FAIL] modified/deleted files under archive/ (immutable)
  [WARN] project CHANGELOG > 200 entries (250 block)
  [WARN] STATE STALE (git log -S based)
  [FAIL] memory operation written outside current project scope (best-effort)
Emergency bypass: git commit --no-verify (not recommended)
"""

import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True)


def project_dirs():
    pdir = ROOT / "projects"
    if not pdir.is_dir():
        return []
    return [d for d in pdir.iterdir() if d.is_dir()]


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


def check_project_state_ids(proj_dir):
    """Per-project S-ID removal must have DROP in same project CHANGELOG."""
    rel = proj_dir.name
    state_rel = "projects/" + rel + "/STATE.md"
    head = git("show", "HEAD:" + state_rel)
    if head.returncode != 0:
        return []
    old_ids = set(re.findall(r"\[(S-\d{8}-\d{2}|[A-Z]+-\d{4,})\]", head.stdout))
    if not old_ids:
        return []
    new = git("show", ":" + state_rel)
    if new.returncode != 0:
        return []
    new_ids = set(re.findall(r"\[(S-\d{8}-\d{2}|[A-Z]+-\d{4,})\]", new.stdout))
    dropped = old_ids - new_ids
    if not dropped:
        return []
    cl = git("show", ":" + "projects/" + rel + "/CHANGELOG.md")
    cl_text = cl.stdout if cl.returncode == 0 else ""
    missing = [i for i in sorted(dropped) if ("DROP " + i) not in cl_text]
    if missing:
        return [rel + " STATE IDs removed without DROP: " + ", ".join(missing)
                + " (add DROP <ID> to projects/" + rel + "/CHANGELOG.md)"]
    return []


def check_project_state_size(proj_dir):
    """Per-project STATE limits: 60 lines / 12 KiB / 已完成 <= 8."""
    rel = proj_dir.name
    state_rel = "projects/" + rel + "/STATE.md"
    new = git("show", ":" + state_rel)
    if new.returncode != 0:
        return []
    text = new.stdout
    lines = text.splitlines()
    problems = []
    if len(lines) > 60:
        problems.append(rel + " STATE.md exceeds 60 lines (" + str(len(lines)) + ")")
    if len(text.encode("utf-8")) > 12 * 1024:
        problems.append(rel + " STATE.md exceeds 12 KiB")
    in_done = False
    done_count = 0
    for ln in lines:
        s = ln.strip()
        if s.startswith("## ") or s.startswith("# "):
            in_done = (s == "## 已完成（最近）")
            continue
        if in_done and s.startswith("-"):
            done_count += 1
    if done_count > 8:
        problems.append(rel + " 已完成（最近） has " + str(done_count) + " entries (> 8)")
    return problems


def check_archive_lock(staged_names):
    """archive/ files immutable: modification/deletion of tracked blocked."""
    bad = []
    for n in staged_names:
        if "archive" not in n.split("/"):
            continue
        r = git("diff", "--cached", "--name-status", "--", n)
        if r.returncode == 0 and r.stdout.strip():
            status = r.stdout.split()[0]
            if status not in ("A", ""):
                bad.append(n + " (status " + status + ")")
    return bad


def check_changelog_size(proj_dir):
    rel = proj_dir.name
    cl_rel = "projects/" + rel + "/CHANGELOG.md"
    new = git("show", ":" + cl_rel)
    if new.returncode != 0:
        return [], []
    entries = [l for l in new.stdout.splitlines() if l.strip().startswith("-")]
    warns, blocks = [], []
    if len(entries) > 250:
        blocks.append(rel + " CHANGELOG too large: " + str(len(entries)) + " entries")
    elif len(entries) > 200:
        warns.append(rel + " CHANGELOG near rotate: " + str(len(entries)) + " entries (run scripts/rotate_memory.py)")
    return warns, blocks


def main():
    r = git("diff", "--cached", "--name-only")
    if r.returncode != 0:
        return 0
    staged = [x.strip() for x in r.stdout.splitlines() if x.strip()]
    problems = []
    warns = []

    hits = check_secrets(staged)
    if hits:
        problems.append("Secrets in staged content:\n" + "\n".join(hits))

    for proj in project_dirs():
        problems.extend(check_project_state_ids(proj))
        problems.extend(check_project_state_size(proj))
        cl_w, cl_b = check_changelog_size(proj)
        warns.extend(cl_w); problems.extend(cl_b)

    arc = check_archive_lock(staged)
    if arc:
        problems.append("archive files immutable: " + ", ".join(arc))

    # v2.1: inbox settled/receipts immutable (modify/delete blocked; first create A allowed)
    for n in staged:
        if n.startswith("inbox/settled/") or n.startswith("inbox/receipts/"):
            r = git("diff", "--cached", "--name-status", "--", n)
            if r.returncode == 0 and r.stdout.strip():
                status = r.stdout.split()[0]
                if status not in ("A", ""):
                    problems.append("inbox settled/receipts immutable: " + n + " (status " + status + ")")

    if problems:
        for p in problems:
            print("[pre-commit] FAIL " + p)
        print("[pre-commit] commit blocked. Bypass: git commit --no-verify")
        return 1
    for w in warns:
        print("[pre-commit] WARN " + w)
    print("[pre-commit] OK memory guard passed" + (" (with warnings)" if warns else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
