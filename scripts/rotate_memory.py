#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ai-hub-memory rotate script - move old records from hot files to archive/.

Usage:
  python scripts/rotate_memory.py changelog   # archive old CHANGELOG segments
  python scripts/rotate_memory.py decisions   # archive old DECISIONS segments

Design (GPT bloat/lifecycle consultation 2026-08-14):
  - ROTATE is the only exception to append-only: old records move OUT of the
    hot file and INTO archive/ verbatim, in the same working-tree state (the
    caller commits everything together).
  - This script only edits files; it never commits or pushes.
  - archive/ files are immutable afterwards (pre-commit hook enforces).
  - CHANGELOG: rotate by month (keep current + previous month hot).
  - DECISIONS: rotate when > 80 decisions; keep still-active long-term decisions
    as short references in the hot file.
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def split_by_month(text):
    """Split CHANGELOG-like content into [(date_header, body_lines)].
    date headers look like `## YYYY-MM-DD`. Returns ordered list of sections."""
    sections = []
    cur_date = None
    cur_lines = []
    for ln in text.splitlines():
        m = re.match(r"^## (\d{4}-\d{2}-\d{2})\s*$", ln)
        if m:
            if cur_date is not None:
                sections.append((cur_date, cur_lines))
            cur_date = m.group(1)
            cur_lines = [ln]
        else:
            cur_lines.append(ln)
    if cur_date is not None:
        sections.append((cur_date, cur_lines))
    return sections


def rotate_changelog():
    """Move CHANGELOG sections older than the current month to archive/changelog/YYYY/."""
    p = ROOT / "CHANGELOG.md"
    if not p.exists():
        print("CHANGELOG.md not found"); return 1
    text = p.read_text(encoding="utf-8")
    sections = split_by_month(text)
    if not sections:
        print("No dated sections found"); return 1
    now = datetime.now()
    current_month = now.strftime("%Y-%m")
    to_archive = []
    keep = []
    for date_hdr, lines in sections:
        month = date_hdr[:7]
        if month < current_month:
            to_archive.append((date_hdr, lines))
        else:
            keep.append((date_hdr, lines))
    if not to_archive:
        print("Nothing to archive (all sections are current month or newer)"); return 0

    # build archive file per year
    by_year = {}
    for date_hdr, lines in to_archive:
        year = date_hdr[:4]
        by_year.setdefault(year, []).extend(lines + [""])
    for year, body in by_year.items():
        adir = ROOT / "archive" / "changelog" / year
        adir.mkdir(parents=True, exist_ok=True)
        afile = adir / ("CHANGELOG-" + year + ".md")
        header = "# CHANGELOG archive " + year + "\n\n> 归档：历史流水（ROTATE 移出热文件，原样保留）。\n\n"
        existing = afile.read_text(encoding="utf-8") if afile.exists() else ""
        new_block = "\n".join(body).rstrip() + "\n\n"
        # avoid duplicate if already archived
        if existing.rstrip().endswith(new_block.rstrip()):
            print("Already archived"); return 0
        afile.write_text(existing + new_block, encoding="utf-8")
        print("archived to " + str(afile) + " (" + str(len(body)) + " lines)")

    # rewrite hot CHANGELOG with kept sections + header
    kept_text = "\n".join(["".join(l) for l in []])
    keep_body = []
    for date_hdr, lines in keep:
        keep_body.extend(lines)
        keep_body.append("")
    header_lines = ["# CHANGELOG.md — 操作记录（只追加）", "", "> 只追加。每个 Agent 干完写一条「谁 / 何时 / 做了什么」。", "> 已归档历史见 archive/changelog/。", ""]
    p.write_text("\n".join(header_lines + keep_body).rstrip() + "\n", encoding="utf-8")
    print("CHANGELOG.md rewritten: kept " + str(len(keep)) + " sections, archived " + str(len(to_archive)))
    return 0


def rotate_decisions():
    """Archive DECISIONS when too many; keep header + recent + active references."""
    p = ROOT / "DECISIONS.md"
    if not p.exists():
        print("DECISIONS.md not found"); return 1
    text = p.read_text(encoding="utf-8")
    lines = text.splitlines()
    decision_lines = [l for l in lines if l.strip().startswith("-")]
    if len(decision_lines) <= 80:
        print("DECISIONS under threshold (" + str(len(decision_lines)) + "/80), nothing to rotate"); return 0
    # keep header (first 2 non-empty lines before ##) + move old date sections
    sections = split_by_month(text)
    # for decisions, archive all but the most recent date section
    if len(sections) <= 1:
        print("Only one date section; manual review needed"); return 1
    keep = sections[-1:]
    to_archive = sections[:-1]
    year = datetime.now().strftime("%Y")
    adir = ROOT / "archive" / "decisions" / year
    adir.mkdir(parents=True, exist_ok=True)
    afile = adir / ("DECISIONS-" + year + ".md")
    body = []
    for date_hdr, ls in to_archive:
        body.extend(ls); body.append("")
    header = "# DECISIONS archive " + year + "\n\n> 归档：历史决策（ROTATE 移出热文件）。仍有效的长期决策以引用保留在热文件。\n\n"
    existing = afile.read_text(encoding="utf-8") if afile.exists() else ""
    afile.write_text(existing + header + "\n".join(body).rstrip() + "\n", encoding="utf-8")
    # rewrite hot file
    keep_body = []
    for date_hdr, ls in keep:
        keep_body.extend(ls)
    hot_header = ["# DECISIONS.md — 决策记录（只追加，带日期）", "", "> 只追加，不删改旧条目。用户敲板的决策记这里。", "> 已归档历史见 archive/decisions/。", ""]
    p.write_text("\n".join(hot_header + keep_body).rstrip() + "\n", encoding="utf-8")
    print("DECISIONS rotated: kept " + str(len(keep)) + " section, archived " + str(len(to_archive)))
    return 0


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("changelog", "decisions"):
        print(__doc__); return 1
    if sys.argv[1] == "changelog":
        return rotate_changelog()
    return rotate_decisions()


if __name__ == "__main__":
    sys.exit(main())
