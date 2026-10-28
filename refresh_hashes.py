"""Refresh release hashes using the repository's .gitignore exclusions."""
from pathlib import Path
from fnmatch import fnmatchcase
import hashlib
import subprocess

ROOT = Path(__file__).resolve().parent


def distribution_files(base=ROOT):
    """Apply the simple patterns shipped in .gitignore; reject unsupported rules."""
    patterns = [line.strip() for line in (base/'.gitignore').read_text().splitlines()
                if line.strip() and not line.lstrip().startswith('#')]
    if any(p.startswith('!') or '**' in p or '\\' in p for p in patterns):
        raise ValueError('Unsupported .gitignore rule; update the release file selector')

    def matches(parts, pattern):
        segments = pattern.lstrip('/').split('/')
        if len(segments) == 1 and not pattern.startswith('/'):
            return any(fnmatchcase(part, pattern) for part in parts)
        return len(parts) == len(segments) and all(
            fnmatchcase(part, rule) for part, rule in zip(parts, segments))

    def ignored(relative):
        parts = relative.parts
        if '.git' in parts:
            return True
        for pattern in patterns:
            if pattern.endswith('/'):
                if any(matches(parts[:n], pattern[:-1]) for n in range(1, len(parts))):
                    return True
            elif matches(parts, pattern):
                return True
        return False

    return sorted(p.relative_to(base).as_posix() for p in base.rglob('*')
                  if p.is_file() and not ignored(p.relative_to(base)))


def tracked_files(base=ROOT):
    """Return this release's Git index, or None for a downloaded source archive."""
    if not (base/'.git').exists():
        return None
    result = subprocess.run(['git', '-C', str(base), 'ls-files', '-z'],
                            check=True, stdout=subprocess.PIPE)
    return sorted(result.stdout.decode('utf-8').rstrip('\0').split('\0'))


def check_file_list(paths, base=ROOT, require_git=False):
    """Bind the manifest set, eligible files and (when present) Git-tracked files."""
    paths = list(paths)
    if len(paths) != len(set(paths)):
        raise ValueError('Duplicate distribution path')
    expected = distribution_files(base)
    if sorted(paths) != expected:
        raise ValueError('Manifest and distribution file lists differ: '+repr(
            sorted(set(paths) ^ set(expected))))
    tracked = tracked_files(base)
    if require_git and tracked is None:
        raise ValueError('A Git-tracked release copy is required')
    if tracked is not None and sorted(paths) != tracked:
        raise ValueError('Hashed and Git-tracked file lists differ: '+repr(
            sorted(set(paths) ^ set(tracked))))
    return tracked is not None


def main():
    paths = distribution_files()
    if 'SHA256SUMS' not in paths:
        paths.append('SHA256SUMS')
    # Stage newly added/deleted files before refreshing an existing Git checkout.
    # SHA256SUMS cannot contain its own digest; it is included in the set check.
    tracked = tracked_files()
    if tracked is not None and sorted(paths) != tracked:
        raise ValueError('Stage release additions/deletions with git add -A first')
    rows = [hashlib.sha256((ROOT/p).read_bytes()).hexdigest()+'  '+p
            for p in sorted(paths) if p != 'SHA256SUMS']
    (ROOT/'SHA256SUMS').write_text('\n'.join(rows)+'\n', encoding='utf-8', newline='\n')
    check_file_list(paths)
    print(f'Wrote {len(rows)} distribution hashes; snapshot hashes preserved. '
          f'Git file-list check: {"PASS" if tracked is not None else "not a Git checkout"}.')


if __name__ == '__main__':
    main()
