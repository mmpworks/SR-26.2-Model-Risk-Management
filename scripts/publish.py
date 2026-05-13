#!/usr/bin/env python3
"""publish.py — single-source-of-truth publisher for ffiec-public CORE.

Reads `publish.manifest.yml` at the repo root and pushes derived artifacts to
downstream targets:

  publish.py rfi               # resolve + stage + show diff (no commit)
  publish.py rfi --list        # show resolved {dest -> source} map and exit
  publish.py rfi --push        # commit AND push to the configured remote
  publish.py herald            # orchestrate Herald.Website R2 syncs (TBD)

Requires: pyyaml, pathspec.  Install:  pip install pyyaml pathspec
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

try:
    import yaml
    import pathspec
except ImportError as e:
    sys.exit(f"missing dependency: {e.name}.  Install: pip install pyyaml pathspec")


REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "publish.manifest.yml"
CACHE_DIR = REPO_ROOT / ".publish-cache"
SKIP_DIRS = {".git", ".publish-cache", "node_modules", ".idea", ".venv", "claude-memory-compiler"}


def load_manifest() -> dict:
    if not MANIFEST_PATH.exists():
        sys.exit(f"manifest not found: {MANIFEST_PATH}")
    with MANIFEST_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def resolve_files(target_cfg: dict) -> dict[str, Path]:
    """Walk CORE, apply include/exclude/overrides.

    Returns {dest_rel_posix: src_abs_path}.  `dest_rel_posix` is the path the
    file should appear at in the downstream repo; for non-overrides it equals
    the source path; for overrides it's renamed to the override key.
    """
    include = pathspec.GitIgnoreSpec.from_lines(target_cfg.get("include") or [])
    exclude = pathspec.GitIgnoreSpec.from_lines(target_cfg.get("exclude") or [])
    overrides = target_cfg.get("overrides") or {}

    result: dict[str, Path] = {}
    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            abs_path = Path(root) / fn
            rel = abs_path.relative_to(REPO_ROOT).as_posix()
            if include.match_file(rel) and not exclude.match_file(rel):
                result[rel] = abs_path

    for dest_rel, src_rel in overrides.items():
        src_abs = REPO_ROOT / src_rel
        if not src_abs.exists():
            print(f"  ! override source missing: {src_rel} (target: {dest_rel})", file=sys.stderr)
            continue
        # Don't ship the source file under its own name AND the override name.
        result.pop(src_rel, None)
        result[dest_rel] = src_abs

    return result


def git(args: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=cwd, check=check, capture_output=True, text=True)


def ensure_cache(remote: str, branch: str, cache: Path) -> None:
    """(Re-)clone the downstream repo to a fresh cache dir.

    Always-fresh-clone: simpler than incremental refresh and the tradeoff
    (one clone per publish) is negligible for repos this size.
    """
    if cache.exists():
        shutil.rmtree(cache)
    cache.parent.mkdir(parents=True, exist_ok=True)
    try:
        git(["clone", remote, str(cache)])
    except subprocess.CalledProcessError as e:
        sys.exit(
            f"\n  clone failed: {e.stderr.strip()}\n"
            f"  Verify the remote exists and you have access:\n"
            f"    gh repo view <owner>/<repo>\n"
        )
    # For a fresh / empty remote the clone may leave HEAD detached or on a
    # default branch — force-create the configured branch either way.
    git(["checkout", "-B", branch], cwd=cache, check=False)


def wipe_working_tree(cache: Path) -> None:
    for entry in cache.iterdir():
        if entry.name == ".git":
            continue
        if entry.is_dir():
            shutil.rmtree(entry)
        else:
            entry.unlink()


def cmd_rfi(args: argparse.Namespace) -> int:
    manifest = load_manifest()
    rfi = manifest.get("rfi") or {}
    if not rfi.get("enabled"):
        sys.exit("rfi target is disabled in manifest")

    files = resolve_files(rfi)
    print(f"resolved {len(files)} file(s) for RFI publish")

    if args.list:
        for dest in sorted(files):
            src = files[dest].relative_to(REPO_ROOT).as_posix()
            tag = "(override)" if src != dest else ""
            print(f"  {dest:<60}  <-  {src}  {tag}".rstrip())
        return 0

    remote = rfi.get("remote")
    branch = rfi.get("branch", "main")
    if not remote:
        sys.exit("rfi.remote not set in manifest")

    cache = CACHE_DIR / "rfi"
    print(f"preparing cache: {cache}")
    ensure_cache(remote, branch, cache)

    print("wiping working tree (preserving .git/)")
    wipe_working_tree(cache)

    print(f"copying {len(files)} file(s)")
    for dest_rel, src_abs in files.items():
        dest_abs = cache / dest_rel
        dest_abs.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_abs, dest_abs)

    git(["add", "-A"], cwd=cache)
    diff = git(["diff", "--cached", "--shortstat"], cwd=cache, check=False)
    if not diff.stdout.strip():
        print("no changes — nothing to publish")
        return 0

    print(f"\nstaged: {diff.stdout.strip()}")

    if not args.push:
        print("(re-run with --push to commit and push)")
        return 0

    msg = (rfi.get("commit_message") or "RFI publish — {date_iso}").format(
        date_iso=date.today().isoformat()
    )
    git(["commit", "-m", msg], cwd=cache)
    print(f"committed: {msg}")
    git(["push", "origin", branch], cwd=cache)
    print(f"pushed to {remote} {branch}")
    return 0


def cmd_herald(args: argparse.Namespace) -> int:
    manifest = load_manifest()
    herald = manifest.get("herald") or {}
    if not herald.get("enabled"):
        sys.exit("herald target is disabled in manifest (enable when new pages exist)")
    sys.exit("herald sync not yet implemented")


def main() -> int:
    p = argparse.ArgumentParser(prog="publish.py", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    rfi = sub.add_parser("rfi", help="squash-publish RFI slice to public repo")
    rfi.add_argument("--list", action="store_true", help="list resolved files and exit")
    rfi.add_argument("--push", action="store_true", help="commit AND push (default: stage and show)")
    rfi.set_defaults(func=cmd_rfi)

    herald = sub.add_parser("herald", help="orchestrate Herald.Website R2 syncs")
    herald.set_defaults(func=cmd_herald)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
