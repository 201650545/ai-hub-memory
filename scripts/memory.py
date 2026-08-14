#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ai-hub-memory v2 - memory router (唯一读写入口)

Usage:
  python scripts/memory.py route --project <id> --kind state|decision
  python scripts/memory.py read --project <id> [--file state|decisions|changelog]
  python scripts/memory.py search --project <id> --query <text>
  python scripts/memory.py write --project <id> --kind state|decision --sid <S-ID> --content <text>
  python scripts/memory.py validate

Design (v2, GPT/Claude/网关三方定稿):
  - Routing before Retrieval; Multi-read/Single-write; Fail-Closed.
  - Agent 不指定文件路径，路径由本脚本决定。
  - write 自动 append CHANGELOG（R9）。
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "MEMORY.json"


def load_manifest():
    if not MANIFEST.exists():
        sys.exit("[memory] ERROR: MEMORY.json not found")
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def resolve_project(manifest, project_id):
    proj = manifest["projects"].get(project_id)
    if proj:
        return project_id, proj["path"]
    # alias match
    for pid, info in manifest["projects"].items():
        if project_id in info.get("aliases", []):
            return pid, info["path"]
    sys.exit("[memory] ERROR: unknown project_id=" + str(project_id) + " (fail closed)")


def cmd_route(args):
    manifest = load_manifest()
    pid, path = resolve_project(manifest, args.project)
    kinds = {"state": "STATE.md", "decision": "DECISIONS.md", "changelog": "CHANGELOG.md"}
    if args.kind not in kinds:
        sys.exit("[memory] ERROR: kind must be state|decision|changelog")
    print(str(ROOT / path / kinds[args.kind]))


def cmd_read(args):
    manifest = load_manifest()
    pid, path = resolve_project(manifest, args.project)
    kinds = {"state": "STATE.md", "decision": "DECISIONS.md", "changelog": "CHANGELOG.md"}
    if args.file not in kinds:
        sys.exit("[memory] ERROR: --file must be state|decision|changelog")
    f = ROOT / path / kinds[args.file]
    if not f.exists():
        sys.exit("[memory] ERROR: " + str(f) + " not found")
    print(f.read_text(encoding="utf-8"))


def cmd_search(args):
    manifest = load_manifest()
    pid, path = resolve_project(manifest, args.project)
    # 只在本项目目录内搜（物理隔离）
    proj_dir = ROOT / path
    if not proj_dir.is_dir():
        sys.exit("[memory] ERROR: project dir missing")
    hits = []
    for f in proj_dir.rglob("*"):
        if f.is_file() and f.suffix in (".md", ".json"):
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            if args.query.lower() in content.lower():
                hits.append(str(f.relative_to(ROOT)))
    print("\n".join(hits) if hits else "[memory] no hits in project " + pid)


def cmd_write(args):
    manifest = load_manifest()
    pid, path = resolve_project(manifest, args.project)
    kinds = {"state": "STATE.md", "decision": "DECISIONS.md", "changelog": "CHANGELOG.md"}
    if args.kind not in ("state", "decision"):
        sys.exit("[memory] ERROR: write kind must be state|decision")
    target = ROOT / path / kinds[args.kind]
    if not target.exists():
        sys.exit("[memory] ERROR: " + str(target) + " not found")
    today = datetime.now().strftime("%Y-%m-%d")
    if args.kind == "state":
        if not re.match(r"^S-", args.sid):
            sys.exit("[memory] ERROR: S-ID must start with S-")
        entry = "- **[" + args.sid + "]** " + args.content + "（" + today + "）"
        text = target.read_text(encoding="utf-8")
        # 追加到 已完成（最近）区
        text = text.replace("## 已完成（最近）", "## 已完成（最近）\n" + entry, 1)
        target.write_text(text, encoding="utf-8")
    else:
        if not re.match(r"^D-", args.sid):
            sys.exit("[memory] ERROR: D-ID must start with D-")
        entry = "- [" + args.sid + "] " + args.content + "（" + today + "）"
        text = target.read_text(encoding="utf-8")
        text += "\n" + entry + "\n"
        target.write_text(text, encoding="utf-8")
    # R9: 自动 append CHANGELOG
    cl = ROOT / path / "CHANGELOG.md"
    if cl.exists():
        cl_text = cl.read_text(encoding="utf-8")
        cl_text += "- " + args.sid + " " + args.content[:60] + "（" + today + "，脚本自动记录）\n"
        cl.write_text(cl_text, encoding="utf-8")
    print("[memory] wrote " + args.sid + " to " + pid + "/" + kinds[args.kind])


def cmd_register(args):
    """一键新建项目：更新 MEMORY.json + 建目录 + 骨架文件 + 更新根索引。"""
    manifest = load_manifest()
    pid = args.id
    if not re.match(r'^[a-z0-9-]+$', pid):
        sys.exit('[memory] ERROR: project id must be lowercase alnum+dash, e.g. english-teaching')
    if pid in manifest['projects']:
        sys.exit('[memory] ERROR: project ' + pid + ' already exists')
    aliases = [a.strip() for a in (args.aliases or '').split(',') if a.strip()]
    manifest['projects'][pid] = {'aliases': aliases, 'path': 'projects/' + pid, 'imports': []}
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    pdir = ROOT / 'projects' / pid
    (pdir / 'archive').mkdir(parents=True, exist_ok=True)
    (pdir / 'STATE.md').write_text('# STATE.md — ' + (args.name or pid) + ' 项目状态\n\n> 当前状态（保留式更新，S-ID 稳定标识）。\n\n## 进行中\n- 无。\n\n## 已完成（最近）\n- 无。\n\n## 卡点\n- 无。\n\n## 下一步\n- 无。\n', encoding='utf-8')
    (pdir / 'DECISIONS.md').write_text('# DECISIONS.md — ' + (args.name or pid) + ' 项目决策（append-only）\n\n> 只追加。\n', encoding='utf-8')
    (pdir / 'CHANGELOG.md').write_text('# CHANGELOG.md — ' + (args.name or pid) + ' 项目流水（append-only）\n\n> 只追加。\n', encoding='utf-8')
    # 更新根索引 STATE.md
    idx = ROOT / 'STATE.md'
    if idx.exists():
        it = idx.read_text(encoding='utf-8')
        row = '| ' + pid + '（' + (args.name or pid) + '） | projects/' + pid + ' | 进行中：无 |'
        it = it.replace('| teaching（教学）', row + '\n| teaching（教学）', 1)
        idx.write_text(it, encoding='utf-8')
    print('[memory] registered project: ' + pid + ' (path projects/' + pid + ')')
    print('[memory] next: git add -A && git commit -m "memory: register project ' + pid + '" && git push')
    return 0

def cmd_validate(args):
    manifest = load_manifest()
    problems = []
    for pid, info in manifest["projects"].items():
        pdir = ROOT / info["path"]
        if not pdir.is_dir():
            problems.append(pid + ": dir missing")
        for name in ("STATE.md", "DECISIONS.md", "CHANGELOG.md"):
            if not (pdir / name).exists():
                problems.append(pid + ": " + name + " missing")
    if problems:
        for p in problems:
            print("[memory] FAIL " + p)
        return 1
    print("[memory] OK structure valid")
    return 0


def main():
    p = argparse.ArgumentParser(description="ai-hub-memory v2 router")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("route"); r.add_argument("--project"); r.add_argument("--kind")
    rd = sub.add_parser("read"); rd.add_argument("--project"); rd.add_argument("--file", default="state")
    s = sub.add_parser("search"); s.add_argument("--project"); s.add_argument("--query")
    w = sub.add_parser("write"); w.add_argument("--project"); w.add_argument("--kind"); w.add_argument("--sid"); w.add_argument("--content")
    v = sub.add_parser("validate")
    reg = sub.add_parser("register"); reg.add_argument("--id"); reg.add_argument("--name", default=""); reg.add_argument("--aliases", default="")
    args = p.parse_args()
    if args.cmd == "route": cmd_route(args)
    elif args.cmd == "read": cmd_read(args)
    elif args.cmd == "search": cmd_search(args)
    elif args.cmd == "write": cmd_write(args)
    elif args.cmd == "validate": sys.exit(cmd_validate(args))
    elif args.cmd == "register": sys.exit(cmd_register(args))


if __name__ == "__main__":
    main()
