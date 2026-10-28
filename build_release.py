"""Build a reproducible ZIP from verified Git-tracked release files only."""
import hashlib
from pathlib import Path
import sys
import zipfile

from refresh_hashes import ROOT, check_file_list


def main():
    archive = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else ROOT.parent/'j73-rupert-v0.1.0.zip'
    if len(sys.argv) > 2 or archive.is_relative_to(ROOT):
        raise ValueError('Usage: build_release.py [ZIP path outside this repository]')
    paths = ['SHA256SUMS']
    for line in (ROOT/'SHA256SUMS').read_text(encoding='utf-8').splitlines():
        digest, relative = line.split('  ', 1)
        path = (ROOT/relative).resolve()
        if not path.is_relative_to(ROOT) or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError('Invalid release hash: '+relative)
        paths.append(relative)
    check_file_list(paths, require_git=True)
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as output:
        for relative in sorted(paths):
            info = zipfile.ZipInfo('j73-rupert/'+relative, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            output.writestr(info, (ROOT/relative).read_bytes(), compresslevel=6)
    with zipfile.ZipFile(archive) as result:
        if result.testzip() is not None:
            raise ValueError('ZIP integrity check failed')
    print(f'{len(paths)} files; {archive.stat().st_size} bytes; '
          f'SHA-256 {hashlib.sha256(archive.read_bytes()).hexdigest()}')


if __name__ == '__main__':
    main()
