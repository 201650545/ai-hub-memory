import os, sys, subprocess, zipfile, time, argparse
from datetime import datetime

REPO = r'D:\ai-hub-memory'
BACKUP_ROOT = r'D:\记忆备份'
KEEP_DAYS = 30


def sh(cmd, cwd=REPO, timeout=180):
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                           encoding='utf-8', errors='ignore', timeout=timeout, shell=True)
        return r.returncode, (r.stdout or '') + (r.stderr or '')
    except Exception as e:
        return -1, str(e)


def git_sync(log):
    log.append('--- git sync ---')
    rc, out = sh('git status --short')
    dirty = [l for l in out.splitlines() if l.strip()]
    if not dirty:
        log.append('工作区干净，无需提交')
    else:
        log.append('待提交 %d 项' % len(dirty))
        sh('git add -A')
        ts = datetime.now().strftime('%Y-%m-%d %H:%M')
        rc, out = sh('git commit -m "chore: 自动备份同步 %s"' % ts)
        log.append('commit rc=%d' % rc)

    for attempt in range(3):
        rc, out = sh('git pull --ff-only')
        if rc != 0:
            log.append('ff-only 失败，尝试 rebase（第 %d 次）' % (attempt + 1))
            rc2, out2 = sh('git rebase origin/master')
            log.append('rebase rc=%d' % rc2)
        rc, out = sh('git push origin master')
        if rc == 0:
            log.append('push 成功')
            break
        log.append('push 失败 rc=%d，重试 %d' % (rc, attempt + 1))
        time.sleep(3)
    else:
        log.append('!! push 连续失败，请人工介入（禁止 force push）')

    rc, sha = sh('git rev-parse --short HEAD')
    rc2, rsha = sh('git rev-parse --short origin/master')
    log.append('HEAD=%s origin/master=%s %s' % (
        sha.strip(), rsha.strip(), '一致' if sha.strip() == rsha.strip() else '!! 不一致'))


def make_backup(log):
    os.makedirs(BACKUP_ROOT, exist_ok=True)
    stamp = datetime.now().strftime('%Y-%m-%d_%H%M')
    target = os.path.join(BACKUP_ROOT, 'ai-hub-memory_%s.zip' % stamp)
    n = 0
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as z:
        for dirpath, dirnames, filenames in os.walk(REPO):
            dirnames[:] = [d for d in dirnames if d not in ('__pycache__',)]
            for fn in filenames:
                p = os.path.join(dirpath, fn)
                rel = os.path.relpath(p, REPO)
                try:
                    z.write(p, rel)
                    n += 1
                except Exception:
                    pass
    size = os.path.getsize(target) / 1024
    log.append('--- backup ---')
    log.append('已打包 %d 个文件 -> %s (%.1f KB)' % (n, target, size))
    return target


def prune(log):
    now = time.time()
    removed = 0
    for fn in os.listdir(BACKUP_ROOT):
        if not fn.startswith('ai-hub-memory_') or not fn.endswith('.zip'):
            continue
        p = os.path.join(BACKUP_ROOT, fn)
        age = (now - os.path.getmtime(p)) / 86400
        if age > KEEP_DAYS:
            os.remove(p)
            removed += 1
    total = len([f for f in os.listdir(BACKUP_ROOT) if f.endswith('.zip')])
    log.append('清理 %d 份过期备份（>%d 天），现存 %d 份' % (removed, KEEP_DAYS, total))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-git', action='store_true')
    args = ap.parse_args()

    log = ['=== 记忆备份 %s ===' % datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    try:
        if not args.no_git:
            git_sync(log)
        make_backup(log)
        prune(log)
    except Exception as e:
        log.append('!! 异常: %s' % e)
    log.append('=== 完成 ===')

    txt = '\n'.join(log)
    print(txt)
    os.makedirs(BACKUP_ROOT, exist_ok=True)
    with open(os.path.join(BACKUP_ROOT, 'backup.log'), 'a', encoding='utf-8') as f:
        f.write(txt + '\n\n')


if __name__ == '__main__':
    main()
