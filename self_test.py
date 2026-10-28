"""Integrity, all shipped mathematical inputs, discovery checks and PDF pages.

This test reads the release files and writes its report only to stdout. It has
no runtime deadline, sampling bound or parallel worker option.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import time

from refresh_hashes import check_file_list, distribution_files

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent


def hashes(manifest, base):
    count = 0
    for line in manifest.read_text(encoding='utf-8').splitlines():
        digest, relative = line.split('  ', 1)
        path = (base/relative).resolve()
        if not path.is_relative_to(base.resolve()):
            raise ValueError('Manifest path escapes release: '+relative)
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError('SHA-256 mismatch: '+relative)
        count += 1
    return count


def historical_files():
    base = ROOT/'data/status-snapshot'
    manifest = json.loads((base/'historical-diagnosis-manifest.json').read_text(encoding='utf-8'))
    shipped = []
    for row in manifest['files']:
        path = (base/row['path']).resolve()
        if not path.is_relative_to((ROOT/'data/historical-diagnosis').resolve()):
            raise ValueError('Historical path outside diagnostic directory')
        if not path.is_file() or path.stat().st_size != row['bytes']:
            raise ValueError('Historical file missing or size mismatch: '+row['path'])
        if hashlib.sha256(path.read_bytes()).hexdigest() != row['sha256']:
            raise ValueError('Historical source hash mismatch: '+row['path'])
        shipped.append(path)
    actual = sorted(p.resolve() for p in (ROOT/'data/historical-diagnosis').rglob('*') if p.is_file())
    if len(shipped) != len(set(shipped)) or sorted(shipped) != actual:
        raise ValueError('Historical manifest and shipped file lists differ')
    for row in manifest['omitted_source_files']:
        if row.get('distributed') is not False:
            raise ValueError('Historical omitted source marked distributed')
    public = json.loads((base/'public-provenance.json').read_text(encoding='utf-8'))
    if hashlib.sha256((base/'summary.json').read_bytes()).hexdigest() != public['summary_sha256']:
        raise ValueError('Frozen summary provenance mismatch')
    for row in public['public_derivatives']:
        if row['distributed_as'] is None:
            if (base/row['original_basename']).exists():
                raise ValueError('Omitted snapshot source unexpectedly distributed')
            continue
        path = (base/row['distributed_as']).resolve()
        if not path.is_relative_to(base.resolve()) or not path.is_file():
            raise ValueError('Missing public snapshot derivative')
        if path.stat().st_size != row['current_bytes'] or hashlib.sha256(path.read_bytes()).hexdigest() != row['current_sha256']:
            raise ValueError('Public snapshot derivative mismatch: '+row['distributed_as'])
    return len(shipped)


def execution_digests():
    eligible = [ROOT/name for name in distribution_files()]
    code = [p for p in eligible if p.suffix == '.py']
    inputs = [p for p in eligible if p.is_relative_to(ROOT/'data') or
              (p.is_relative_to(ROOT/'paper') and p.suffix in ('.tex', '.pdf'))]
    # The receipt and enclosing manifests are deliberately absent to avoid a
    # circular dependency when a successful run is recorded and then hashed.
    inputs = [p for p in inputs if p.is_file() and p.name not in ('SHA256SUMS', 'release-selftest.json')]
    def bind(paths):
        return {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    return dict(code_sha256=bind(code), input_sha256=bind(inputs))


def integrity_checks():
    main_hashes = hashes(ROOT/'SHA256SUMS', ROOT)
    listed = [line.split('  ', 1)[1] for line in (ROOT/'SHA256SUMS').read_text(encoding='utf-8').splitlines()]
    git_checked = check_file_list(listed+['SHA256SUMS'])
    base = ROOT/'data/status-snapshot'
    snapshot_hashes = hashes(base/'SHA256SUMS', base)
    snapshot_listed = [line.split('  ', 1)[1] for line in (base/'SHA256SUMS').read_text(encoding='utf-8').splitlines()]
    if sorted(snapshot_listed+['SHA256SUMS']) != sorted(p.relative_to(base).as_posix() for p in base.rglob('*') if p.is_file()):
        raise ValueError('Snapshot manifest and distributed file lists differ')
    historical_count = historical_files()
    provenance = json.loads((ROOT/'data/code-provenance.json').read_text(encoding='utf-8'))
    for row in provenance['unchanged_kernel']:
        if hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest() != row['sha256']:
            raise ValueError('Original code provenance mismatch: '+row['path'])
    from pypdf import PdfReader
    expected = json.loads((ROOT/'data/pdf-metadata.json').read_text(encoding='utf-8'))
    pdf_path = ROOT/'paper/paper.pdf'
    if pdf_path.stat().st_size != expected['bytes'] or hashlib.sha256(pdf_path.read_bytes()).hexdigest() != expected['sha256']:
        raise ValueError('PDF metadata size or hash mismatch')
    pages = len(PdfReader(pdf_path).pages)
    if pages != expected['pages']:
        raise ValueError('PDF page count mismatch')
    source_sha256 = {name.removeprefix('paper/'): hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                     for name in distribution_files() if name.startswith('paper/') and name.endswith('.tex')}
    if source_sha256 != expected['source_sha256']:
        raise ValueError('PDF TeX source metadata mismatch')
    visual = expected['visual_review']
    if visual['status'] != 'PASS' or visual['pdf_sha256'] != expected['sha256'] or visual['source_sha256'] != source_sha256:
        raise ValueError('PDF visual-check binding mismatch')
    if sorted(visual['pages_inspected']) != list(range(1, pages+1)):
        raise ValueError('PDF visual check must cover every page')
    return dict(distribution_hashes=main_hashes, snapshot_hashes=snapshot_hashes,
                historical_files=historical_count, git_file_list_checked=git_checked,
                pdf_pages=pages, tex_sources=len(source_sha256))


def main():
    if not __debug__:
        raise RuntimeError('Run Python without -O or PYTHONOPTIMIZE')
    started = time.monotonic()
    checked = integrity_checks()
    digests = execution_digests()
    print(json.dumps(dict(status='INTEGRITY_PASS', **checked), sort_keys=True), flush=True)
    for relative in ['code/checker/check.py', 'code/discovery/check.py']:
        subprocess.run([sys.executable, '-X', 'utf8', '-B', str(ROOT/relative)], cwd=ROOT, check=True)
    print(json.dumps(dict(status='PASS', scope='all shipped local evidence; no complete root or global cover claim',
        **checked, **digests, checks_run=['distribution SHA-256 and file set', 'Git-tracked file set when in a checkout',
        'public snapshot SHA-256 and derivative bindings', 'historical file existence, size and SHA-256',
        'unchanged checker and discovery provenance', 'PDF bytes, pages, SHA-256, TeX and visual-check bindings',
        'all three local certificates and all 2660 tube regions', 'exact discovery and four-contact identities'],
        elapsed_seconds=time.monotonic()-started), sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
