#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ai-hub-memory pre-commit hook - memory integrity guard

GPT force-read 2026-08-14 (backup/rollback) + 2026-08-14 (bloat/lifecycle)

Checks (FAIL blocks commit, WARN does not):
  [FAIL] secrets in staged content
  [FAIL] STATE S-ID removed without DROP in CHANGELOG
  [FAIL] STATE.md > 60 lines or > 12 KiB
  [FAIL] STATE 已完成（最近） section > 8 entries
  [FAIL] modified/deleted files under archive/ (immutable)
  [WARN] CHANGELOG > 200 entries or > 200 KiB (250 block)
  [WARN] DECISIONS > 80 decisions or > 100 KiB (100 block)
  [WARN] STATE 进行中/下一步/卡点 STALE (no modification in N days)

Emergency bypass: git commit --no-verify (not recommended)
"""

import datetime
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
                + " (add DROP <ID> - reason to CHANGELOG.md first)"]
    return []


def check_state_size():
    """STATE hard limits: 60 lines / 12 KiB / 已完成 <= 8 entries."""
    new = git("show", ":STATE.md")
    if new.returncode != 0:
        return []
    text = new.stdout
    lines = text.splitlines()
    problems = []
    if len(lines) > 60:
        problems.append("STATE.md exceeds 60 lines (" + str(len(lines)) + ")")
    if len(text.encode("utf-8")) > 12 * 1024:
        problems.append("STATE.md exceeds 12 KiB")
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
        problems.append("STATE 已完成（最近） has " + str(done_count) + " entries (> 8)")
    return problems


def check_archive_lock(staged_names):
    """archive/ files are immutable: block modification/deletion of TRACKED archive files.
    New archive files (first creation by rotate_memory.py) are allowed; subsequent
    modification/deletion is blocked."""
    bad = []
    for n in staged_names:
        if not (n.startswith("archive/") or "/archive/" in n):
            continue
        # status XY: X=index status, Y=worktree status; track if not 'A' (added new)
        r = git("diff", "--cached", "--name-status", "--", n)
        if r.returncode == 0 and r.stdout.strip():
            status = r.stdout.split()[0]
            if status not in ("A", ""):
                bad.append(n + " (status " + status + ")")
    return bad


def check_changelog_size():
    """CHANGELOG rotate threshold: 200 warn / 250 block; 200 KiB warn / 250 KiB block."""
    new = git("show", ":CHANGELOG.md")
    if new.returncode != 0:
        return [], []
    text = new.stdout
    entries = [l for l in text.splitlines() if l.strip().startswith("-")]
    kb = len(text.encode("utf-8")) / 1024.0
    warns, blocks = [], []
    if len(entries) > 250 or kb > 250:
        blocks.append("CHANGELOG too large: " + str(len(entries)) + " entries, " + str(round(kb)) + " KiB")
    elif len(entries) > 200 or kb > 200:
        warns.append("CHANGELOG near rotate: " + str(len(entries)) + " entries, " + str(round(kb)) + " KiB (run scripts/rotate_memory.py)")
    return warns, blocks


def check_decisions_size():
    """DECISIONS threshold: 80 warn / 100 block; 100 KiB warn / 125 KiB block."""
    new = git("show", ":DECISIONS.md")
    if new.returncode != 0:
        return [], []
    text = new.stdout
    decisions = [l for l in text.splitlines() if l.strip().startswith("-")]
    kb = len(text.encode("utf-8")) / 1024.0
    warns, blocks = [], []
    if len(decisions) > 100 or kb > 125:
        blocks.append("DECISIONS too large: " + str(len(decisions)) + " decisions, " + str(round(kb)) + " KiB")
    elif len(decisions) > 80 or kb > 100:
        warns.append("DECISIONS near threshold: " + str(len(decisions)) + " decisions, " + str(round(kb)) + " KiB")
    return warns, blocks


def check_stale(new_state_text):
    """STALE warning: S-ID last touched via git log -S; 进行中 14d / 下一步/卡点 30d."""
    warns = []
    now = datetime.datetime.now(datetime.timezone.utc)
    thresholds = {"## 进行中": 14, "## 下一步": 30, "## 卡点": 30}
    current_section = None
    for ln in new_state_text.splitlines():
        s = ln.strip()
        if s.startswith("## "):
            current_section = s
            continue
        m = re.match(r"- \*\*\[(S-\d{8}-\d{2})\]", s)
        if not m or current_section not in thresholds:
            continue
        sid = m.group(1)
        r2 = git("log", "-1", "--format=%ct", "-S", sid, "--", "STATE.md")
        ts = r2.stdout.strip()
        if not ts.isdigit():
            continue
        last = datetime.datetime.fromtimestamp(int(ts), datetime.timezone.utc)
        days = (now - last).days
        if days > thresholds[current_section]:
            warns.append(sid + " in " + current_section + " unchanged " + str(days) + "d (STALE, review or keep)")
    return warns


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

    problems.extend(check_state_ids())
    problems.extend(check_state_size())

    arc = check_archive_lock(staged)
    if arc:
        problems.append("archive/ files immutable (cannot modify/delete): " + ", ".join(arc))

    cl_w, cl_b = check_changelog_size()
    warns.extend(cl_w); problems.extend(cl_b)

    dc_w, dc_b = check_decisions_size()
    warns.extend(dc_w); problems.extend(dc_b)

    new_state = git("show", ":STATE.md")
    if new_state.returncode == 0:
        warns.extend(check_stale(new_state.stdout))

    if problems:
        for p in problems:
            print("[pre-commit] FAIL " + p)
        print("[pre-commit] commit blocked. Bypass: git commit --no-verify (not recommended)")
        return 1
    for w in warns:
        print("[pre-commit] WARN " + w)
    print("[pre-commit] OK memory guard passed" + (" (with warnings)" if warns else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
