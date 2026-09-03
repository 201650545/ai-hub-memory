import os, zipfile, shutil, subprocess, tempfile

REPO = r'D:\ai-hub-memory'
BACKUP_ROOT = r'D:\记忆备份'
TARGET = os.path.join(BACKUP_ROOT, 'ai-hub-memory_2026-09-02_2103.zip')
TMPZIP = os.path.join(BACKUP_ROOT, '_repack_final.tmp.zip')  # 必须同盘


def sh(cmd, cwd=REPO, timeout=180):
    r = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True,
                       text=True, errors='ignore', timeout=timeout)
    return r.returncode, ((r.stdout or '') + (r.stderr or '')).strip()


print('=== 1. 补推 ===')
rc, out = sh('git add -A')
rc, out = sh('git commit -m "chore: 备份自动化执行记录 2026-09-02（最终态）"')
print('commit rc=%d %s' % (rc, out[:120]))
rc, out = sh('git pull --ff-only')
print('pull rc=%d %s' % (rc, out[:120]))
rc, out = sh('git push origin master')
print('push rc=%d %s' % (rc, out[:160]))
rc, head = sh('git rev-parse --short HEAD')
rc, rem = sh('git ls-remote origin refs/heads/master')
remote_sha = rem.split()[0][:7] if rem else ''
print('HEAD=%s 远端实际=%s' % (head, remote_sha))
if rc != 0 or head != remote_sha:
    print('!! 不一致，中止重打包')
    raise SystemExit(1)

print()
print('=== 2. 重打包 ===')
n = 0
if os.path.exists(TMPZIP):
    os.remove(TMPZIP)
with zipfile.ZipFile(TMPZIP, 'w', zipfile.ZIP_DEFLATED) as z:
    for dirpath, dirnames, filenames in os.walk(REPO):
        dirnames[:] = [d for d in dirnames if d not in ('__pycache__',)]
        for fn in filenames:
            bn = fn
            if bn.startswith('_repack') or bn.startswith('_verify') or bn.startswith('_finalize'):
                continue
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, REPO)
            try:
                z.write(p, rel)
                n += 1
            except Exception:
                pass

with zipfile.ZipFile(TMPZIP, 'r') as z:
    names = z.namelist()
    bad = z.testzip()
gitn = [x for x in names if x.startswith('.git/')]
core = ['.git/HEAD', '.git/config', '.git/index', '.git/packed-refs',
        '.git/refs/heads/master', '.git/refs/remotes/origin/master']
core_ok = all(c in names for c in core)
print('新包 %d 条目 / %.2f KB | testzip=%s | .git=%d | 核心=%s | 无重复=%s'
      % (n, os.path.getsize(TMPZIP) / 1024, bad, len(gitn), core_ok, len(names) == len(set(names))))

print()
print('=== 3. 解包实测（根目录即 TMPX，无子目录层） ===')
TMPX = os.path.join(tempfile.gettempdir(), 'vf_last')
if os.path.exists(TMPX):
    shutil.rmtree(TMPX, ignore_errors=True)
os.makedirs(TMPX)
with zipfile.ZipFile(TMPZIP, 'r') as z:
    z.extractall(TMPX)
r1, h = sh('git rev-parse --short HEAD', cwd=TMPX)
r2, st = sh('git status --short', cwd=TMPX)
r3, fk = sh('git fsck --no-progress', cwd=TMPX, timeout=300)
has_mem = os.path.exists(os.path.join(TMPX, '.workbuddy', 'memory', '2026-09-02.md'))
print('HEAD=%s | 工作区=%r | fsck rc=%d | 含当日记忆=%s' % (h, st, r3, has_mem))
shutil.rmtree(TMPX, ignore_errors=True)

ok = (bad is None and core_ok and r1 == 0 and h == head and st == '' and r3 == 0 and has_mem)
print()
print('=== 4. 原子替换 ===')
if ok:
    bak = TARGET + '.old'
    if os.path.exists(TARGET):
        if os.path.exists(bak):
            os.remove(bak)
        os.replace(TARGET, bak)
    os.replace(TMPZIP, TARGET)
    if os.path.exists(bak):
        os.remove(bak)
    print('替换完成 -> %.2f KB' % (os.path.getsize(TARGET) / 1024))
    print('目录残留检查:', [f for f in os.listdir(BACKUP_ROOT) if f.startswith('_') or f.endswith('.old')] or '无')
else:
    print('!! 校验未通过，保留原包，删除临时包')
    os.remove(TMPZIP)
