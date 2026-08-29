#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ai-hub-memory v2.1 - memory router (唯一读写入口 + 隔离记忆 staging)

Formal memory:
  route / read / search / write / validate / register
Staging (v2.1):
  capture / status / settle-plan / resolve / settle

Design (v2.1, GPT 3-round finalized 2026-08-14):
  Quarantined Ingress + Project-scoped Consolidation
  Routing before Retrieval; Multi-read/Single-write; Fail Closed; R1'-R16
"""

import argparse
import hashlib
import json
import os
import re
import secrets
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "MEMORY.json"
INBOX = ROOT / "inbox"
INBOX_META = INBOX / "META.json"

SECRET_PATTERNS = [
    (r"sk-[A-Za-z0-9]{16,}", "sk- key"),
    (r"AIza[A-Za-z0-9_-]{20,}", "Google API key"),
    (r"Bearer [A-Za-z0-9._-]{20,}", "Bearer token"),
    (r"app_token[\"']?\s*[:=]\s*[\"']?[A-Za-z0-9]{15,}", "app_token"),
    (r"app_secret[\"']?\s*[:=]\s*[\"']?[A-Za-z0-9]{15,}", "app_secret"),
]


def git(*args):
    """Run git in repo root; inject the current python dir into PATH so pre-commit
    hooks that call python/python3 resolve even when the caller PATH lacks it."""
    env = os.environ.copy()
    py_dir = os.path.dirname(sys.executable)
    if py_dir and py_dir not in env.get("PATH", "").split(os.pathsep):
        env["PATH"] = py_dir + os.pathsep + env.get("PATH", "")
    return subprocess.run(["git", *args], capture_output=True, text=True, cwd=str(ROOT), env=env)


def load_manifest():
    if not MANIFEST.exists():
        sys.exit("[memory] ERROR: MEMORY.json not found")
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def resolve_project(manifest, project_id):
    proj = manifest["projects"].get(project_id)
    if proj:
        return project_id, proj["path"]
    for pid, info in manifest["projects"].items():
        if project_id in info.get("aliases", []):
            return pid, info["path"]
    sys.exit("[memory] ERROR: unknown project_id=" + str(project_id) + " (fail closed)")


def secret_hits(text):
    hits = []
    for pat, desc in SECRET_PATTERNS:
        for m in re.finditer(pat, text, re.IGNORECASE):
            hits.append(desc + " -> " + m.group(0)[:16])
    return hits


def load_inbox_meta():
    if not INBOX_META.exists():
        return {"schema": "inbox-meta-v1", "last_settle_date": None, "last_settle_at": None}
    try:
        return json.loads(INBOX_META.read_text(encoding="utf-8"))
    except Exception:
        return {"schema": "inbox-meta-v1", "last_settle_date": None, "last_settle_at": None}


def save_inbox_meta(meta):
    INBOX_META.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def make_inbox_id():
    now = datetime.now(timezone.utc)
    ts = now.strftime("%Y%m%dT%H%M%S")
    return "I-" + ts + "-" + secrets.token_hex(4).upper()


def inbox_item_path(item_id):
    """Find item file under inbox/pending by id (search all date dirs)."""
    pdir = INBOX / "pending"
    if not pdir.is_dir():
        return None
    for d in pdir.iterdir():
        if d.is_dir():
            f = d / (item_id + ".md")
            if f.exists():
                return f
    return None


def parse_inbox_item(path):
    text = path.read_text(encoding="utf-8")
    meta = {}
    m = re.search(r"^---\n(.*?)\n---", text, re.DOTALL)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
    body = text[m.end():].strip() if m else text.strip()
    return meta, body


def visible_staging(project_id, capture_scope=None):
    """R11: return list of (path, meta, body) visible to a project agent."""
    pdir = INBOX / "pending"
    if not pdir.is_dir():
        return []
    out = []
    for d in sorted(pdir.iterdir()):
        if not d.is_dir():
            continue
        for f in sorted(d.glob("*.md")):
            meta, body = parse_inbox_item(f)
            hint = meta.get("project_hint", "UNKNOWN")
            scope = meta.get("capture_scope", "")
            if hint == project_id:
                out.append((f, meta, body))
            elif hint == "UNKNOWN" and capture_scope and scope == capture_scope:
                out.append((f, meta, body))
    return out


def write_inbox_item(content, project_hint, routing_basis, kind_hint, capture_scope):
    # R16: secret preflight BEFORE writing file
    hits = secret_hits(content)
    if hits:
        sys.exit("[memory] ERROR: credential-like content rejected before capture: " + "; ".join(hits))
    item_id = make_inbox_id()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    ddir = INBOX / "pending" / today
    ddir.mkdir(parents=True, exist_ok=True)
    f = ddir / (item_id + ".md")
    header = "---\n"
    header += "schema: inbox-v1\n"
    header += "id: " + item_id + "\n"
    header += "captured_at: " + datetime.now(timezone.utc).isoformat() + "\n"
    header += "capture_scope: " + capture_scope + "\n"
    header += "project_hint: " + project_hint + "\n"
    header += "routing_basis: " + routing_basis + "\n"
    header += "kind_hint: " + kind_hint + "\n"
    header += "---\n\n"
    f.write_text(header + content.strip() + "\n", encoding="utf-8")
    print("[memory] captured " + item_id + " project_hint=" + project_hint)
    return item_id


def write_memory_entry(pid, kind, sid, content):
    """Shared formal write logic used by cmd_write and cmd_settle (R9)."""
    manifest = load_manifest()
    _, path = resolve_project(manifest, pid)
    kinds = {"state": "STATE.md", "decision": "DECISIONS.md"}
    target = ROOT / path / kinds[kind]
    if not target.exists():
        sys.exit("[memory] ERROR: " + str(target) + " not found")
    today = datetime.now().strftime("%Y-%m-%d")
    if kind == "state":
        entry = "- **[" + sid + "]** " + content + "（" + today + "）"
        text = target.read_text(encoding="utf-8")
        text = text.replace("## 已完成（最近）", "## 已完成（最近）\n" + entry, 1)
        target.write_text(text, encoding="utf-8")
    else:
        entry = "- [" + sid + "] " + content + "（" + today + "）"
        text = target.read_text(encoding="utf-8")
        text += "\n" + entry + "\n"
        target.write_text(text, encoding="utf-8")
    cl = ROOT / path / "CHANGELOG.md"
    if cl.exists():
        cl_text = cl.read_text(encoding="utf-8")
        cl_text += "- " + sid + " " + content[:60] + "（" + today + "，脚本自动记录）\n"
        cl.write_text(cl_text, encoding="utf-8")
    return sid


def next_memory_id(pid, kind):
    manifest = load_manifest()
    _, path = resolve_project(manifest, pid)
    kinds = {"state": "STATE.md", "decision": "DECISIONS.md"}
    f = ROOT / path / kinds[kind]
    text = f.read_text(encoding="utf-8") if f.exists() else ""
    today = datetime.now().strftime("%Y%m%d")
    pat = re.compile(r"\[([A-Z]+-)" + today + r"-(\d{2})\]")
    mx = 0
    for m in pat.finditer(text):
        mx = max(mx, int(m.group(2)))
    prefix = "S" if kind == "state" else "D"
    return prefix + "-" + today + "-" + str(mx + 1).zfill(2)


def cmd_route(args):
    manifest = load_manifest()
    pid, path = resolve_project(manifest, args.project)
    kinds = {"state": "STATE.md", "decision": "DECISIONS.md", "changelog": "CHANGELOG.md"}
    if args.kind not in kinds:
        sys.exit("[memory] ERROR: kind must be state|decision|changelog")
    print(str(ROOT / path / kinds[args.kind]))


def cmd_read(args):
    manifest = load_manifest()
    # --file global: 读全局层，无需项目（协议第一层：未选项目也可读 global）
    if args.file == "global":
        for name in ("RULES.md", "PROJECTS.md", "DECISIONS.md", "TOOLS.md"):
            gf = ROOT / "global" / name
            if gf.exists():
                print("## " + name)
                print(gf.read_text(encoding="utf-8"))
        return
    # 项目级读必须有项目（协议第三层：未选项目时项目级数据 fail-closed）
    if not args.project:
        print("ERROR=PROJECT_REQUIRED")
        print("NEXT_ACTION=SELECT_PROJECT")
        sys.exit(2)
    pid, path = resolve_project(manifest, args.project)
    if args.file == "staging":
        # v2.1 R11: filtered staging read
        items = visible_staging(pid, args.capture_scope)
        if not items:
            print("[memory] no visible staging for " + pid + " scope=" + str(args.capture_scope))
            return
        for f, meta, body in items:
            print("## " + meta.get("id", "?") + " hint=" + meta.get("project_hint", "?") + " scope=" + meta.get("capture_scope", "?"))
            print(body[:200]); print()
        return
    kinds = {"state": "STATE.md", "decision": "DECISIONS.md", "changelog": "CHANGELOG.md"}
    if args.file not in kinds:
        sys.exit("[memory] ERROR: --file must be state|decision|changelog|staging")
    f = ROOT / path / kinds[args.file]
    if not f.exists():
        sys.exit("[memory] ERROR: " + str(f) + " not found")
    print(f.read_text(encoding="utf-8"))


def cmd_search(args):
    manifest = load_manifest()
    pid, path = resolve_project(manifest, args.project)
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


def ensure_ff_pull():
    """R2 (GLM review 2026-08-14): write/settle 前强制 git pull --ff-only。
    失败（工作区脏/远端分叉）即拒绝写入——与 Fail Closed 同构。"""
    r = git('pull', '--ff-only')
    if r.returncode != 0:
        sys.exit('[memory] ERROR: git pull --ff-only failed (worktree dirty or diverged). '
                + 'Resolve local changes / pull conflicts, then retry write. (R2 强制先 pull)')

def cmd_write(args):
    if not args.project:
        print("ERROR=PROJECT_REQUIRED")
        print("NEXT_ACTION=SELECT_PROJECT")
        sys.exit(2)
    ensure_ff_pull()
    manifest = load_manifest()
    pid, path = resolve_project(manifest, args.project)
    if args.kind not in ("state", "decision"):
        sys.exit("[memory] ERROR: write kind must be state|decision")
    if not re.match(r"^[SD]-", args.sid):
        sys.exit("[memory] ERROR: S/D-ID must start with S- or D-")
    write_memory_entry(pid, args.kind, args.sid, args.content)
    print("[memory] wrote " + args.sid + " to " + pid)


def cmd_capture(args):
    manifest = load_manifest()
    if args.project_hint and args.project_hint != "UNKNOWN":
        # canonicalize via resolve_project (aliases work, unknown fails)
        try:
            pid, _ = resolve_project(manifest, args.project_hint)
        except SystemExit:
            sys.exit("[memory] ERROR: --project-hint must be registered project or UNKNOWN")
        hint = pid
    else:
        hint = "UNKNOWN"
    routing_basis = args.routing_basis or ("none" if hint == "UNKNOWN" else "explicit")
    write_inbox_item(args.content, hint, routing_basis, args.kind_hint or "auto", args.capture_scope)


def cmd_status(args):
    pdir = INBOX / "pending"
    items = []
    if pdir.is_dir():
        for d in pdir.iterdir():
            if d.is_dir():
                for f in d.glob("*.md"):
                    meta, body = parse_inbox_item(f)
                    items.append((f, meta, body))
    if args.settler:
        unknown = sum(1 for _, m, _ in items if m.get("project_hint") == "UNKNOWN")
        by_proj = {}
        for _, m, _ in items:
            h = m.get("project_hint", "UNKNOWN")
            by_proj[h] = by_proj.get(h, 0) + 1
        print("[memory] pending=" + str(len(items)))
        print("[memory] unknown=" + str(unknown))
        for k, v in sorted(by_proj.items()):
            print("[memory] " + k + "=" + str(v))
        meta = load_inbox_meta()
        print("[memory] last_settle_date=" + str(meta.get("last_settle_date")))
        due = len(items) >= (load_manifest().get("staging", {}).get("pending_threshold", 20)) or unknown >= 5
        print("[memory] settle_due=" + ("yes" if due else "no"))
        # R8 (GLM review): 超阈值停留天数提醒
        if items:
            oldest_date = None
            for f, _, _ in items:
                try:
                    d = datetime.strptime(f.parent.name, "%Y-%m-%d")
                    if oldest_date is None or d < oldest_date:
                        oldest_date = d
                except Exception:
                    continue
            if oldest_date:
                days = (datetime.now().date() - oldest_date.date()).days
                if days > 0:
                    print("[memory] inbox 超阈值已停留 " + str(days) + " 天（最旧 " + oldest_date.strftime("%Y-%m-%d") + "），建议 settle 整理")
        return
    if not args.project:
        sys.exit("[memory] ERROR: status needs --settler or --project")
    manifest = load_manifest()
    pid, _ = resolve_project(manifest, args.project)
    visible = visible_staging(pid, args.capture_scope)
    mine = sum(1 for _, m, _ in visible if m.get("project_hint") == pid)
    same_unknown = sum(1 for _, m, _ in visible if m.get("project_hint") == "UNKNOWN")
    print("[memory] project=" + pid)
    print("[memory] staging_project=" + str(mine))
    print("[memory] staging_same_origin_unknown=" + str(same_unknown))


def cmd_settle_plan(args):
    pdir = INBOX / "pending"
    if not pdir.is_dir():
        print("[memory] no pending"); return
    all_items = []
    for d in sorted(pdir.iterdir()):
        if d.is_dir():
            for f in sorted(d.glob("*.md")):
                meta, body = parse_inbox_item(f)
                all_items.append((f, meta, body))
    if args.project:
        manifest = load_manifest()
        pid, _ = resolve_project(manifest, args.project)
        all_items = [(f, m, b) for f, m, b in all_items if m.get("project_hint") == pid]
    for f, meta, body in all_items:
        hint = meta.get("project_hint", "UNKNOWN")
        kind = meta.get("kind_hint", "auto")
        cand = meta.get("candidate_project", "")
        if hint != "UNKNOWN" and kind in ("state", "decision"):
            status = "READY"
        elif hint != "UNKNOWN" and kind == "auto":
            status = "NEEDS_KIND"
        elif hint == "UNKNOWN" and cand:
            status = "CANDIDATE"
        else:
            status = "UNRESOLVED"
        print(status + " " + meta.get("id", "?") + " hint=" + hint + " kind=" + kind + " body=" + body[:60])


def cmd_resolve(args):
    f = inbox_item_path(args.id)
    if not f:
        sys.exit("[memory] ERROR: item " + args.id + " not found in pending")
    meta, body = parse_inbox_item(f)
    if args.discard:
        _finalize_item(f, meta, body, "discarded", args.reason or "", None, None)
        print("[memory] discarded " + args.id); return
    if args.covered_by:
        _finalize_item(f, meta, body, "covered", args.reason or "", args.project, args.covered_by)
        print("[memory] covered " + args.id + " by " + args.covered_by); return
    if args.project and args.basis:
        manifest = load_manifest()
        pid, _ = resolve_project(manifest, args.project)
        meta["project_hint"] = pid
        meta["routing_basis"] = args.basis
        if args.kind:
            meta["kind_hint"] = args.kind
        _rewrite_item(f, meta, body)
        print("[memory] resolved " + args.id + " -> " + pid + " basis=" + args.basis); return
    if args.candidate_project:
        meta["candidate_project"] = args.candidate_project
        meta["candidate_reason"] = args.reason or ""
        _rewrite_item(f, meta, body)
        print("[memory] candidate recorded (still UNKNOWN): " + args.id); return
    if args.kind:
        meta["kind_hint"] = args.kind
        _rewrite_item(f, meta, body)
        print("[memory] kind set: " + args.id + " -> " + args.kind); return
    sys.exit("[memory] ERROR: resolve needs one of --project/--discard/--covered-by/--candidate-project/--kind")


def _rewrite_item(f, meta, body):
    header = "---\n"
    for k, v in meta.items():
        header += k + ": " + str(v) + "\n"
    header += "---\n\n"
    f.write_text(header + body + "\n", encoding="utf-8")


def _finalize_item(f, meta, body, disposition, reason, target_project, target_id):
    # move pending -> settled + write receipt
    month = datetime.now().strftime("%Y-%m")
    sdir = INBOX / "settled" / month
    rdir = INBOX / "receipts" / month
    sdir.mkdir(parents=True, exist_ok=True); rdir.mkdir(parents=True, exist_ok=True)
    sid = meta.get("id", f.stem)
    shutil_move(f, sdir / f.name)
    receipt = {
        "schema": "settlement-receipt-v1",
        "id": sid,
        "settled_at": datetime.now(timezone.utc).isoformat(),
        "disposition": disposition,
        "capture_scope": meta.get("capture_scope", ""),
        "original_project_hint": meta.get("project_hint", ""),
        "final_project": target_project,
        "target_id": target_id,
        "reason": reason,
    }
    (rdir / (sid + ".json")).write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")


def shutil_move(src, dst):
    src.replace(dst)


def cmd_settle(args):
    if not args.project:
        print("ERROR=PROJECT_REQUIRED")
        print("NEXT_ACTION=SELECT_PROJECT")
        sys.exit(2)
    ensure_ff_pull()
    # preflight all items first, then apply (atomic-ish)
    manifest = load_manifest()
    pid, _ = resolve_project(manifest, args.project)
    pdir = INBOX / "pending"
    targets = []
    if pdir.is_dir():
        for d in pdir.iterdir():
            if d.is_dir():
                for f in d.glob("*.md"):
                    meta, body = parse_inbox_item(f)
                    if args.id and meta.get("id") not in args.id:
                        continue
                    hint = meta.get("project_hint", "UNKNOWN")
                    kind = meta.get("kind_hint", "auto")
                    if hint != pid:
                        continue
                    if kind not in ("state", "decision"):
                        continue
                    targets.append((f, meta, body))
    if not targets:
        print("[memory] nothing to settle for " + pid); return
    if args.dry_run:
        for f, meta, body in targets:
            print("[memory] would settle " + meta.get("id") + " -> " + pid + "/" + meta.get("kind_hint"));
        return
    for f, meta, body in targets:
        sid = next_memory_id(pid, meta["kind_hint"])
        write_memory_entry(pid, meta["kind_hint"], sid, body)
        _finalize_item(f, meta, body, "promoted", "", pid, sid)
        print("[memory] settled " + meta.get("id") + " -> " + sid + " (" + pid + ")")


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
    if not (INBOX / "pending").is_dir() or not (INBOX / "settled").is_dir():
        problems.append("inbox structure missing")
    if problems:
        for p in problems:
            print("[memory] FAIL " + p)
        return 1
    print("[memory] OK structure valid (v2.1)")
    return 0


def cmd_sync(args):
    """同步 Agent 记忆：读取来源文件 -> 判断 kind -> 生成稳定 ID -> 写入项目线 + CHANGELOG。"""
    if not args.project:
        print("ERROR=PROJECT_REQUIRED")
        print("NEXT_ACTION=SELECT_PROJECT")
        sys.exit(2)
    manifest = load_manifest()
    pid, _ = resolve_project(manifest, args.project)
    src = Path(args.file)
    if not src.exists():
        sys.exit('[memory] ERROR: source file not found: ' + str(src))
    text = src.read_text(encoding='utf-8', errors='ignore').strip()
    if not text:
        sys.exit('[memory] ERROR: empty source')
    # R16: secret preflight BEFORE any write
    hits = secret_hits(text)
    if hits:
        sys.exit('[memory] ERROR: credential-like content rejected in sync: ' + '; '.join(hits))
    # kind 判断
    kind = args.kind
    if kind == 'auto':
        if re.search(r'决策|决定|拍板|约定|今后|以后|规则', text):
            kind = 'decision'
        else:
            kind = 'state'
    if kind not in ('state', 'decision'):
        sys.exit('[memory] ERROR: kind must be state|decision|auto')
    # 正文截断防膨胀（STATE 单条合理长度）
    body = text[:600] + ('...' if len(text) > 600 else '')
    sid = next_memory_id(pid, kind)
    if args.dry_run:
        print('[memory] would sync ' + src.name + ' -> ' + pid + '/' + kind + ' ' + sid + ' body=' + body[:50])
        return
    write_memory_entry(pid, kind, sid, body)
    print('[memory] synced ' + src.name + ' -> ' + sid + ' (' + pid + '/' + kind + ')')


def cmd_sync_batch(args):
    """批量同步目录下所有 .md/.txt 文件到指定项目。"""
    manifest = load_manifest()
    pid, _ = resolve_project(manifest, args.project)
    d = Path(args.dir)
    if not d.is_dir():
        sys.exit('[memory] ERROR: dir not found: ' + str(d))
    files = sorted([f for f in d.iterdir() if f.suffix.lower() in ('.md', '.txt')])
    if not files:
        print('[memory] no .md/.txt files in ' + str(d)); return
    for f in files:
        text = f.read_text(encoding='utf-8', errors='ignore').strip()
        if not text: continue
        hits = secret_hits(text)
        if hits:
            print('[memory] SKIP ' + f.name + ' (credential-like content)'); continue
        kind = args.kind
        if kind == 'auto':
            kind = 'decision' if re.search(r'决策|决定|拍板|约定|今后|以后|规则', text) else 'state'
        body = text[:600] + ('...' if len(text) > 600 else '')
        sid = next_memory_id(pid, kind)
        if args.dry_run:
            print('[memory] would sync ' + f.name + ' -> ' + pid + '/' + kind + ' ' + sid)
            continue
        write_memory_entry(pid, kind, sid, body)
        print('[memory] synced ' + f.name + ' -> ' + sid + ' (' + pid + '/' + kind + ')')

def _bootstrap_protocol_header():
    print("MEMORY_PROTOCOL=v1")
    print("SOURCE_OF_TRUTH=github")


def _bootstrap_project_list(manifest):
    print("PROJECTS:")
    for pid in sorted(manifest["projects"].keys()):
        print("- " + pid)
    print("- new-project")


def _bootstrap_rules_summary():
    print("RULES:")
    print("- project memory is isolated")
    print("- read/write only through memory.py")
    print("- R17 project decisions take precedence")
    print("- R18 memory checkpoint is enabled")
    print("- credentials must never enter memory")


def _git_sync_status():
    """返回 (MEMORY_COMMIT, SYNC_STATUS)：Git 本地 head 与远端同步状态（GPT 2026-08-15 建议）。"""
    head = git('rev-parse', 'HEAD')
    commit = head.stdout.strip()[:12] if head.returncode == 0 else "unknown"
    st = git('status', '--porcelain')
    dirty = bool(st.stdout.strip()) if st.returncode == 0 else True
    if dirty:
        return commit, "stale"  # 本地有未提交改动
    fr = git('fetch', 'origin', '--quiet')
    if fr.returncode != 0:
        return commit, "unknown"
    behind = git('rev-list', '--count', 'HEAD..origin/HEAD')
    ahead = git('rev-list', '--count', 'origin/HEAD..HEAD')
    try:
        b = int(behind.stdout.strip() or '0')
        a = int(ahead.stdout.strip() or '0')
    except Exception:
        return commit, "unknown"
    if b > 0 and a > 0:
        return commit, "conflict"
    if b > 0:
        return commit, "stale"
    if a > 0:
        return commit, "local_ahead"
    return commit, "current"


def _active_project_file():
    return ROOT / ".memory-active-project"


def _check_switch(pid):
    """项目切换检测（GPT 2026-08-15 建议）：bootstrap 到不同于上次的项目时，
    提醒先对旧项目执行 checkpoint，避免丢失未保存状态。sidecar 不入库。"""
    f = _active_project_file()
    prev = f.read_text(encoding="utf-8").strip() if f.exists() else ""
    if prev and prev != pid:
        print("SWITCH_FROM=" + prev)
        print("REMINDER=上次活动项目为 " + prev + "；若其中有未 checkpoint 的状态，请先对其执行 memory.py checkpoint 再继续本项目。")
    f.write_text(pid + "\n", encoding="utf-8")


def cmd_bootstrap(args):
    """协议入口（GPT 评审 2026-08-15 定稿）：Agent 进入记忆线的唯一入口。
    无 --project → 输出协议状态 + 项目列表 + NEXT_ACTION=SELECT_PROJECT（固定首轮响应）。
    有 --project → 输出 ACTIVE_PROJECT/ALLOWED_SCOPE + R18 规则 + 项目 STATE/DECISIONS + staging。
    均返回 MEMORY_COMMIT + SYNC_STATUS（防基于旧 checkout 工作）+ 项目切换提醒。"""
    manifest = load_manifest()
    print("==== MEMORY_BOOTSTRAP ====")
    _bootstrap_protocol_header()
    commit, sync = _git_sync_status()
    print("MEMORY_COMMIT=" + commit)
    print("SYNC_STATUS=" + sync)
    if sync != "current":
        print("NEXT_ACTION=SYNC_MEMORY")
        print("WARNING=memory source not current; run git pull --ff-only before working")
        print("==== END BOOTSTRAP ====")
        return
    if not args.project:
        # 无项目模式：告诉 Agent 当前未选项目，只能读 global
        print("ACTIVE_PROJECT=none")
        print("ALLOWED_SCOPE=global")
        _bootstrap_project_list(manifest)
        _bootstrap_rules_summary()
        print("NEXT_ACTION=SELECT_PROJECT")
        print()
        print("---- GLOBAL READ (PROJECTS/DECISIONS) ----")
        for name in ("PROJECTS.md", "DECISIONS.md"):
            gf = ROOT / "global" / name
            if gf.exists():
                print("## " + name)
                print(gf.read_text(encoding="utf-8"))
        print("==== END BOOTSTRAP ====")
        return
    pid, path = resolve_project(manifest, args.project)
    _check_switch(pid)
    rules_f = ROOT / "global" / "RULES.md"
    print("ACTIVE_PROJECT=" + pid)
    print("ALLOWED_SCOPE=global+" + pid)
    print("MEMORY_CHECKPOINT_POLICY=R18")
    print()
    if rules_f.exists():
        rules = rules_f.read_text(encoding="utf-8")
        print("---- GLOBAL RULES (Checkpoint policy) ----")
        lines = rules.splitlines()
        emit = False
        for ln in lines:
            if ln.startswith("R18") or ln.startswith("R1'"):
                emit = True
            elif ln.startswith("R") and not (ln.startswith("R18") or ln.startswith("R1'")):
                emit = False
            if emit:
                print(ln)
        in_timing = False
        for ln in lines:
            if ln.startswith("## 读写时机"):
                in_timing = True
            elif in_timing and ln.startswith("## "):
                in_timing = False
            if in_timing:
                print(ln)
    print()
    state_f = ROOT / path / "STATE.md"
    if state_f.exists():
        print("---- PROJECT STATE ----")
        print(state_f.read_text(encoding="utf-8"))
    dec_f = ROOT / path / "DECISIONS.md"
    if dec_f.exists():
        dec = dec_f.read_text(encoding="utf-8")
        if dec.strip() and len(dec.strip()) > 0:
            print("---- PROJECT DECISIONS ----")
            print(dec)
    items = visible_staging(pid, args.capture_scope)
    if items:
        print("---- VISIBLE STAGING ----")
        for f, meta, body in items:
            print("## " + meta.get("id", "?") + " hint=" + meta.get("project_hint", "?") + " scope=" + meta.get("capture_scope", "?"))
            print(body[:200]); print()
    print("NEXT_ACTION=READY")
    print("==== END BOOTSTRAP ====")


def git_pull_ff():
    r = git('pull', '--ff-only')
    if r.returncode != 0:
        sys.exit('[memory] ERROR: git pull --ff-only failed (worktree dirty or diverged). Resolve then retry checkpoint.')


def checkpoint_id_marker(pid, checkpoint_id):
    """幂等标记：存于项目本地未跟踪 sidecar（不写进 STATE，避免膨胀；可安全重建）。"""
    marker_dir = ROOT / "projects" / pid / ".checkpoints"
    marker_dir.mkdir(parents=True, exist_ok=True)
    return marker_dir / (checkpoint_id.replace("/", "_").replace(":", "_") + ".txt")


def cmd_checkpoint(args):
    """R18/checkpoint 事务保存（GPT 评审 2026-08-15 推荐）：
    secret preflight -> pull 最新 -> 幂等检查 -> write -> validate -> commit -> push。
    push 被远端抢先时禁止用旧 STATE 重试：重新 pull 最新并重放。"""
    # 0. 项目必填（协议第三层：未选项目时项目级写入 fail-closed）
    if not args.project:
        print("ERROR=PROJECT_REQUIRED")
        print("NEXT_ACTION=SELECT_PROJECT")
        sys.exit(2)
    # 1. secret preflight
    hits = secret_hits(args.content)
    if hits:
        sys.exit("[memory] ERROR: credential-like content rejected in checkpoint: " + "; ".join(hits))
    # 2. pull latest (fail closed)
    git_pull_ff()
    manifest = load_manifest()
    pid, path = resolve_project(manifest, args.project)
    if args.kind not in ("state", "decision"):
        sys.exit("[memory] ERROR: checkpoint kind must be state|decision")
    sid = args.sid
    if not sid:
        sid = next_memory_id(pid, args.kind)
    # 3. idempotency: checkpoint-id already applied -> skip
    if args.checkpoint_id:
        marker = checkpoint_id_marker(pid, args.checkpoint_id)
        if marker.exists():
            print("[memory] checkpoint already applied (idempotent skip): " + args.checkpoint_id)
            return
    # 4. write entry
    write_memory_entry(pid, args.kind, sid, args.content)
    # 5. record idempotency marker AFTER successful write
    if args.checkpoint_id:
        marker = checkpoint_id_marker(pid, args.checkpoint_id)
        marker.write_text("sid=" + sid + "\n" + "applied=" + str(datetime.now(timezone.utc).isoformat()) + "\n", encoding="utf-8")
    # 6. commit + push (closed loop; R9 真源保存)
    kinds = {"state": "STATE.md", "decision": "DECISIONS.md"}
    target = ROOT / path / kinds[args.kind]
    cl = ROOT / path / "CHANGELOG.md"
    files = [str(target), str(cl)]
    # 6a. 并发写冲突检测（GPT 2026-08-15 建议）：除本项目写入文件外，
    #     工作树还有未提交改动 = 可能其他 Agent 正在并发写，提醒但不阻止。
    porc = git('status', '--porcelain')
    others = []
    if porc.returncode == 0:
        my = {str(target), str(cl)}
        for line in porc.stdout.splitlines():
            p = line[3:].strip().strip('"')
            full = (ROOT / p).resolve()
            if str(full) not in my and "/.checkpoints/" not in p:
                others.append(p)
    if others:
        print("[memory] WARN: 工作树存在非本 checkpoint 的未提交改动（可能并发写）: " + "; ".join(others[:5]))
    git('add', '--', *files)
    c = git('commit', '-m', 'memory: checkpoint ' + sid + ' (' + pid + ')')
    if c.returncode != 0:
        err = (c.stderr or "").strip() + (c.stdout or "").strip()
        if "nothing to commit" in err or "no changes added" in err:
            print("[memory] checkpoint " + sid + ": nothing new to commit")
        else:
            sys.exit("[memory] ERROR: checkpoint commit failed: " + err)
    pu = git('push')
    if pu.returncode != 0:
        # 远端前进：禁止 force；重新 pull 最新并重试 push（重放）
        print("[memory] CONFLICT: 远端有他人提交，正在重新 pull 并重放本次 checkpoint（不 force）")
        git_pull_ff()
        pu2 = git('push')
        if pu2.returncode != 0:
            sys.exit("[memory] ERROR: CONFLICT 未自动解决，checkpoint push 仍失败（可能需手工 rebase 合并）。" + pu2.stderr)
        print("[memory] CONFLICT resolved: 已基于最新记忆重放并 push 成功")
    print("[memory] checkpoint " + sid + " (" + pid + ") saved + pushed")


def cmd_register(args):
    manifest = load_manifest()
    pid = args.id
    if not re.match(r"^[a-z0-9-]+$", pid):
        sys.exit("[memory] ERROR: project id must be lowercase alnum+dash")
    if pid in manifest["projects"]:
        sys.exit("[memory] ERROR: project " + pid + " already exists")
    aliases = [a.strip() for a in (args.aliases or "").split(",") if a.strip()]
    manifest["projects"][pid] = {"aliases": aliases, "path": "projects/" + pid, "imports": []}
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    pdir = ROOT / "projects" / pid
    (pdir / "archive").mkdir(parents=True, exist_ok=True)
    (pdir / "STATE.md").write_text("# STATE.md — " + (args.name or pid) + " 项目状态\n\n## 进行中\n- 无。\n\n## 已完成（最近）\n- 无。\n\n## 卡点\n- 无。\n\n## 下一步\n- 无。\n", encoding="utf-8")
    (pdir / "DECISIONS.md").write_text("# DECISIONS.md — " + (args.name or pid) + " 项目决策（append-only）\n", encoding="utf-8")
    (pdir / "CHANGELOG.md").write_text("# CHANGELOG.md — " + (args.name or pid) + " 项目流水（append-only）\n", encoding="utf-8")
    idx = ROOT / "STATE.md"
    if idx.exists():
        it = idx.read_text(encoding="utf-8")
        row = "| " + pid + "（" + (args.name or pid) + "） | projects/" + pid + " | 进行中：无 |"
        it = it.replace("| teaching（教学）", row + "\n| teaching（教学）", 1)
        idx.write_text(it, encoding="utf-8")
    print("[memory] registered project: " + pid)


PROTECT_KW = ("P3PASS", "blocker", "Step 0", "核验令牌", "未决", "待你决定", "待用户", "当前未决卡点")
ARCHIVE_KW = ("resolved", "superseded", "已完成", "已关闭", "已解决", "已了结", "收尾完成", "已提交并推送", "已落定", "历史已解卡点")


def _parse_state_entries(text):
    pat = re.compile(r"^- \*\*\[(S-\d{8}-\d+)\]\*\*")
    entries, cur = [], None
    for ln in text.splitlines():
        m = pat.match(ln)
        if m:
            if cur:
                entries.append(cur)
            cur = {"sid": m.group(1), "body": ln}
        elif cur is not None:
            if ln.startswith("- **[") or ln.startswith("## "):
                entries.append(cur)
                cur = None
            else:
                cur["body"] += "\n" + ln
    if cur:
        entries.append(cur)
    return entries


def cmd_tier_plan(args):
    """Phase M0：只分类，不移动。只读输出 protected / keep-hot / warm-candidate / archive-candidate。"""
    manifest = load_manifest()
    if not args.project:
        print("ERROR=PROJECT_REQUIRED")
        sys.exit(2)
    pid, path = resolve_project(manifest, args.project)
    sf = ROOT / path / "STATE.md"
    if not sf.exists():
        print("ERROR=STATE_NOT_FOUND path=" + str(sf))
        sys.exit(2)

    text = sf.read_text(encoding="utf-8")
    entries = _parse_state_entries(text)
    if not entries:
        print("[memory] no S- entries parsed from " + str(sf))
        return

    ordered = sorted(entries, key=lambda e: e["sid"])
    latest = set(e["sid"] for e in ordered[-args.hot:])

    rows = []
    for e in ordered:
        sid, body = e["sid"], e["body"]
        date = sid[2:10]
        has_resolve = any(k in body for k in ARCHIVE_KW)
        no_blocker = bool(re.search(r"卡点[:：]\s*(无|暂无|None|none|N/A|n/a)", body)) or "无卡点" in body
        if any(k in body for k in PROTECT_KW):
            tier, why = "protected", "含活跃约束/令牌/未决项，永不封存"
        elif "卡点" in body and not has_resolve and not no_blocker:
            tier, why = "protected", "当前未决卡点（含卡点且无已解标记）"
        elif sid in latest:
            tier, why = "keep-hot", "最近 %d 条内，默认激活" % args.hot
        elif has_resolve:
            tier, why = "archive-candidate", "含完成/关闭类标记且非近期"
        else:
            tier, why = "warm-candidate", "非近期且无强保护标记"
        rows.append({"sid": sid, "date": date, "len": len(body), "tier": tier, "why": why})

    total = sum(r["len"] for r in rows)
    print("PROJECT=" + pid)
    print("MODE=READ-ONLY (零文件移动)  HOT_WINDOW=" + str(args.hot))
    print("ENTRIES=" + str(len(rows)) + "  TOTAL_CHARS=" + str(total))
    print()
    print("| SID | 日期 | 字符 | 分层 | 原因 |")
    print("|---|---|---|---|---|")
    for r in rows:
        print("| %s | %s | %d | %s | %s |" % (r["sid"], r["date"], r["len"], r["tier"], r["why"]))
    print()
    for tier in ("protected", "keep-hot", "warm-candidate", "archive-candidate"):
        sub = [r for r in rows if r["tier"] == tier]
        c = sum(r["len"] for r in sub)
        print("%-18s n=%-3d chars=%-7d (%.1f%%)" % (tier, len(sub), c, (100.0 * c / total) if total else 0.0))
    arc = [r for r in rows if r["tier"] == "archive-candidate"]
    if arc:
        print()
        print("若迁移 archive-candidate，可移出 STATE.md 约 %d 字符（%.1f%%），原文 checksum 须保持一致。"
              % (sum(r["len"] for r in arc), 100.0 * sum(r["len"] for r in arc) / total))
    print()
    print("NEXT_ACTION=人工复核本表后再决定是否进入 Phase M1（试点迁移 3-5 条）")


def _router_rows(text):
    rows = []
    for ln in text.splitlines():
        ln = ln.strip()
        if not (ln.startswith("| S-") or ln.startswith("|S-")):
            continue
        cells = [c.strip() for c in ln.strip("|").split("|")]
        if len(cells) < 10:
            continue
        rows.append({"memory_id": cells[0], "kind": cells[1], "topic_keys": cells[2],
                     "entities": cells[3], "period": cells[4], "status": cells[5],
                     "archive_ref": cells[6], "source_ids": cells[7],
                     "superseded_by": cells[8], "sha256_16": cells[9]})
    return rows


def _archive_segment(text, sid):
    m = re.search(r"^\- \*\*\[" + re.escape(sid) + r"\]\*\*.*$", text, re.M)
    return m.group(0) if m else None


def _marker_sids(text):
    return set(re.findall(r"^\- \*\*\[(S-\d{8}-\d+)\]\*\*", text, re.M))


def cmd_verify(args):
    """只读校验 Router↔archive↔STATE 一致性（架构方案风险3防线，索引应可重建）。"""
    manifest = load_manifest()
    problems = []

    state_sids, archive_sids = {}, {}
    for pid, info in manifest["projects"].items():
        sf = ROOT / info["path"] / "STATE.md"
        if sf.exists():
            for sid in _marker_sids(sf.read_text(encoding="utf-8")):
                state_sids.setdefault(sid, []).append(pid)
    archive_root = ROOT / "archive"
    if archive_root.is_dir():
        for fp in archive_root.rglob("*.md"):
            for sid in _marker_sids(fp.read_text(encoding="utf-8")):
                archive_sids.setdefault(sid, []).append(str(fp.relative_to(ROOT)))

    for sid, paths in sorted(archive_sids.items()):
        if len(paths) > 1:
            problems.append("archive SID 重复 " + sid + " -> " + ", ".join(paths))
    for sid in sorted(set(state_sids) & set(archive_sids)):
        problems.append("STATE 与 archive 重复 SID " + sid + " (STATE: " + ", ".join(state_sids[sid]) + "; archive: " + ", ".join(archive_sids[sid]) + ")")

    all_sids = set(state_sids) | set(archive_sids)
    for pid, info in manifest["projects"].items():
        rf = ROOT / info["path"] / "ROUTER.md"
        if not rf.exists():
            continue
        for row in _router_rows(rf.read_text(encoding="utf-8")):
            mid, ref = row["memory_id"], row["archive_ref"]
            if ref == "STATE.md":
                continue
            refpath = ROOT / ref
            if not refpath.exists():
                problems.append(pid + " ROUTER " + mid + ": archive_ref 不存在 " + ref)
                continue
            seg = _archive_segment(refpath.read_text(encoding="utf-8"), mid)
            if seg is None:
                problems.append(pid + " ROUTER " + mid + ": 正文找不到 " + mid + " @ " + ref)
                continue
            sha = hashlib.sha256(seg.encode("utf-8")).hexdigest()[:16]
            if row["sha256_16"] and sha != row["sha256_16"]:
                problems.append(pid + " ROUTER " + mid + ": sha256_16 不匹配 期望=" + row["sha256_16"] + " 实际=" + sha)
            for cell in (row["source_ids"], row["superseded_by"]):
                for sidref in re.findall(r"S-\d{8}-\d+", cell):
                    if sidref not in all_sids:
                        problems.append(pid + " ROUTER " + mid + ": 引用 SID 不可解析 " + sidref)

    if problems:
        for p in problems:
            print("[memory] VERIFY-FAIL " + p)
        print("[memory] VERIFY_FAIL total=" + str(len(problems)))
        return 1
    print("[memory] OK router/archive/state consistent")
    return 0


def main():
    p = argparse.ArgumentParser(description="ai-hub-memory v2.1 router")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("route"); r.add_argument("--project"); r.add_argument("--kind")
    rd = sub.add_parser("read"); rd.add_argument("--project"); rd.add_argument("--file", default="state"); rd.add_argument("--capture-scope")
    s = sub.add_parser("search"); s.add_argument("--project"); s.add_argument("--query")
    w = sub.add_parser("write"); w.add_argument("--project"); w.add_argument("--kind"); w.add_argument("--sid"); w.add_argument("--content")
    v = sub.add_parser("validate")
    vf = sub.add_parser("verify")
    reg = sub.add_parser("register"); reg.add_argument("--id"); reg.add_argument("--name", default=""); reg.add_argument("--aliases", default="")
    cap = sub.add_parser("capture"); cap.add_argument("--capture-scope", required=True); cap.add_argument("--project-hint", default="UNKNOWN"); cap.add_argument("--routing-basis", default=""); cap.add_argument("--kind-hint", default="auto"); cap.add_argument("--content", required=True)
    st = sub.add_parser("status"); st.add_argument("--settler", action="store_true"); st.add_argument("--project"); st.add_argument("--capture-scope")
    sp = sub.add_parser("settle-plan"); sp.add_argument("--all", action="store_true"); sp.add_argument("--project")
    rs = sub.add_parser("resolve"); rs.add_argument("--id", required=True); rs.add_argument("--project"); rs.add_argument("--basis"); rs.add_argument("--kind"); rs.add_argument("--candidate-project"); rs.add_argument("--reason", default=""); rs.add_argument("--covered-by"); rs.add_argument("--discard", action="store_true")
    stl = sub.add_parser("settle"); stl.add_argument("--project"); stl.add_argument("--id", action="append"); stl.add_argument("--dry-run", action="store_true")
    sy = sub.add_parser("sync"); sy.add_argument("--project"); sy.add_argument("--file"); sy.add_argument("--dir"); sy.add_argument("--kind", default="auto"); sy.add_argument("--dry-run", action="store_true")
    bt = sub.add_parser("bootstrap"); bt.add_argument("--project"); bt.add_argument("--capture-scope")
    cp = sub.add_parser("checkpoint"); cp.add_argument("--project"); cp.add_argument("--kind", default="state"); cp.add_argument("--sid"); cp.add_argument("--content", required=True); cp.add_argument("--checkpoint-id")
    tp = sub.add_parser("tier-plan"); tp.add_argument("--project"); tp.add_argument("--hot", type=int, default=5); tp.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    if args.cmd == "route": cmd_route(args)
    elif args.cmd == "read": cmd_read(args)
    elif args.cmd == "search": cmd_search(args)
    elif args.cmd == "write": cmd_write(args)
    elif args.cmd == "validate": sys.exit(cmd_validate(args))
    elif args.cmd == "verify": sys.exit(cmd_verify(args))
    elif args.cmd == "register": cmd_register(args)
    elif args.cmd == "sync": (cmd_sync_batch(args) if args.dir else cmd_sync(args))
    elif args.cmd == "capture": cmd_capture(args)
    elif args.cmd == "status": cmd_status(args)
    elif args.cmd == "settle-plan": cmd_settle_plan(args)
    elif args.cmd == "resolve": cmd_resolve(args)
    elif args.cmd == "settle": cmd_settle(args)
    elif args.cmd == "bootstrap": cmd_bootstrap(args)
    elif args.cmd == "checkpoint": cmd_checkpoint(args)
    elif args.cmd == "tier-plan": cmd_tier_plan(args)


if __name__ == "__main__":
    main()
