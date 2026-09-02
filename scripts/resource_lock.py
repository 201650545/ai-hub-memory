#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""resource_lock.py — 单机 Agent 资源互斥锁（MEMREORG P0-2，GPT R3 终版 2026-09-01）

文件存在性 + TTL lease + 持有 pid 存活三重判定；O_CREAT|O_EXCL 原子占位。
锁落 global/runtime/locks/（gitignored，机器瞬态，不入共享真源）。
Git claims 只解决异步文件认领；端口/NSSM 服务/单实例进程互斥一律走本锁。

用法:
  python scripts/resource_lock.py acquire --resource port:3100 --owner Claude [--ttl 900]
  python scripts/resource_lock.py release --resource port:3100 --owner Claude
  python scripts/resource_lock.py list

退出码: 0=成功 2=参数错误 3=资源被占 4=释放被拒 5=IO错误
"""
import argparse
import ctypes
import json
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCK_DIR = os.path.join(ROOT, "global", "runtime", "locks")
DEFAULT_TTL = 900


def _pid_alive(pid):
    if pid <= 0:
        return False
    h = ctypes.windll.kernel32.OpenProcess(0x1000, False, int(pid))
    if h:
        ctypes.windll.kernel32.CloseHandle(h)
        return True
    return False


def _path(resource):
    name = re.sub(r"[^A-Za-z0-9._-]", "_", resource)
    return os.path.join(LOCK_DIR, name + ".lock")


def _read(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def _stale(info, now):
    if not isinstance(info, dict):
        return True
    if now >= info.get("expires_at", 0):
        return True
    pid = int(info.get("pid", 0))
    return pid > 0 and not _pid_alive(pid)


def acquire(resource, owner, ttl, pid):
    os.makedirs(LOCK_DIR, exist_ok=True)
    path = _path(resource)
    now = time.time()
    info = _read(path)
    if info is not None and not _stale(info, now):
        remain = int(info.get("expires_at", 0) - now)
        print("BUSY %s held by %s (pid %s, %ss remaining)" % (resource, info.get("owner"), info.get("pid"), remain))
        return 3
    if info is not None:
        try:
            os.remove(path)
        except OSError:
            pass
    payload = {"resource": resource, "owner": owner, "pid": pid,
               "created_at": int(now), "expires_at": int(now + ttl)}
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        print("BUSY %s (并发竞态失败，重试即可)" % resource)
        return 3
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)
    print("LOCKED %s -> %s (ttl %ss, pid %d)" % (resource, owner, ttl, pid))
    return 0


def release(resource, owner):
    path = _path(resource)
    info = _read(path)
    if info is None:
        print("RELEASED %s (锁不存在，视为已释放)" % resource)
        return 0
    if info.get("owner") != owner and not _stale(info, time.time()):
        print("DENIED %s held by %s (调用方 %s 不匹配且锁仍有效)" % (resource, info.get("owner"), owner))
        return 4
    try:
        os.remove(path)
    except OSError as e:
        print("IO_ERROR %s" % e)
        return 5
    print("RELEASED %s (%s)" % (resource, owner))
    return 0


def list_locks():
    if not os.path.isdir(LOCK_DIR):
        print("(no locks)")
        return 0
    now = time.time()
    entries = sorted(os.listdir(LOCK_DIR))
    if not entries:
        print("(no locks)")
        return 0
    for name in entries:
        if not name.endswith(".lock"):
            continue
        info = _read(os.path.join(LOCK_DIR, name))
        if isinstance(info, dict):
            state = "STALE" if _stale(info, now) else "HELD"
            remain = int(info.get("expires_at", 0) - now)
            print("%-24s %-6s owner=%-10s pid=%-8s %4ss" % (info.get("resource", name), state, info.get("owner"), info.get("pid"), remain))
        else:
            print("%-24s BROKEN (unreadable)" % name)
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    pa = sub.add_parser("acquire")
    pa.add_argument("--resource", required=True)
    pa.add_argument("--owner", required=True)
    pa.add_argument("--ttl", type=int, default=DEFAULT_TTL)
    pa.add_argument("--pid", type=int, default=0,
                    help="持有进程 pid：传 0（默认）=TTL-only 预约；传存活进程 pid 则该进程死亡锁即 STALE")
    pr = sub.add_parser("release")
    pr.add_argument("--resource", required=True)
    pr.add_argument("--owner", required=True)
    sub.add_parser("list")
    a = p.parse_args()
    if a.cmd == "acquire":
        sys.exit(acquire(a.resource, a.owner, a.ttl, a.pid))
    elif a.cmd == "release":
        sys.exit(release(a.resource, a.owner))
    else:
        sys.exit(list_locks())


if __name__ == "__main__":
    main()
