"""Serial replay without runtime, worker or sampling cutoffs.

The unchanged v2 predicates enforce input-format and resource limits:
exponents <= 64, at most 1,000,000 Bernstein coefficients, tube grids 1..16.
Invalid inputs fail with an exception; they are never skipped as accepted.
"""
from pathlib import Path
import argparse
import hashlib
import json
import time
from collections import Counter
from exact import loads, bounds, need
from local import verify_leaf, RULE_COUNTS
from cover import walk
from geometry import rotation
import tube


def replay_region(region):
    tube.reject_floats(region)
    need(region.get('schema') == 'j45-region-v1', 'tube region schema')
    need(region.get('model') in ('contact-facet', 'astra-intersection'), 'tube region model')
    need(region['input_hash'] == tube.geometry_hash(), 'tube geometry binding')
    reference = rotation(region['reference_T_body_Q5'])
    if region['model'] == 'contact-facet':
        tube.contact_region(region, reference)
    else:
        tube.intersection_region(region, reference)


def certificates(repo):
    metadata = loads((repo/'data/certificate-provenance.json').read_bytes())
    accepted = []
    for row in metadata['certificates']:
        path = (repo/row['path']).resolve()
        need(path.is_relative_to(repo), 'certificate path boundary')
        cert = loads(path.read_bytes())
        if cert.get('op') in ('G', 'SC', 'tube'):
            verify_leaf(cert)
        else:
            walk(cert, bounds(cert['original_box'], 5))
        accepted.append(row['path'])
        print('ACCEPT certificate '+row['path'], flush=True)
    return accepted


def regions(repo):
    bank = loads((repo/'data/tube-regions.json').read_bytes())
    need(bank['schema'] == 'j73-interim-region-bank-v1', 'region bank schema')
    seen = set()
    models = Counter()
    for ordinal, row in enumerate(bank['regions'], 1):
        region = row['region']
        digest = hashlib.sha256(json.dumps(region, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()).hexdigest()
        need(digest == row['sha256'] and digest not in seen, 'region hash or duplicate')
        replay_region(region)
        seen.add(digest)
        models[region['model']] += 1
        if ordinal % 50 == 0:
            print(f'ACCEPT regions {ordinal}/{len(bank["regions"])}', flush=True)
    return dict(regions=len(seen), models=dict(models))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    repo = args.repo.resolve()
    started = time.monotonic()
    accepted = certificates(repo)
    result = dict(status='ACCEPT', scope='all shipped local certificates and all shipped regions; no complete root or global cover claim',
                  certificates=accepted, **regions(repo), rule_counts=dict(RULE_COUNTS), elapsed_seconds=time.monotonic()-started)
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
