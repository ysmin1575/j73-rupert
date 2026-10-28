# Frozen status snapshot

This release uses one captured production dataset. The capture interval is
2026-10-27 10:40:50.233026 to 10:41:21.245658 KST (UTC+09:00).
`summary.json` records the UTC times, the captured counts, the exact hashes
of coordinator inputs, and the read contract. The progress record was last
updated at 01:40:48.467462 UTC. The coordinator state, input configuration
and count fields were unchanged across capture. The heartbeat changed;
both progress records are retained. This is an interval capture of
committed root versions, not an atomic filesystem snapshot.

All production contents were read through `compact_storage53.logical_bytes`
or `read`. The SQLite connection used by that API was replaced with strict
`mode=ro`; its writable hot-journal recovery path was not permitted. No
writer lock, recovery, worker start, pause, restart or reconfiguration was
performed. A producer receipt is never treated as an independent proof.

## Files and interpretation

- `summary.json`: production counters, root-status counts by captured proof
  budget and closing-rule category, and the closed-root data-size inventory.
- `progress.json`, `progress-at-capture-end.json`, `state.json`,
  `run_config.json`: exact logical coordinator bytes. The raw controller
  record is not distributed; its original size and digest are in
  `public-provenance.json`.
- `per-root-status.csv.gz`: every one of the 2,057 staged inputs. Each row
  records its proof hash and observation time, whether its current result
  matches that proof, its number of pending boxes, and its status. A closed
  row also has a producer receipt bound to that proof and an empty frontier.
- `open-roots.json`, `closed-roots.json`: the same staged partition.
  Indices refer to the 3,524 queue8b residual / queue10 input population,
  not to the 1,248,480 original angular-grid roots.
- `captured-root-versions.json`: logical hashes of the captured proofs and
  their source commitments. Full producer forests are not embedded here.
- `historical-chain.json`, `historical-accounting.md`, `historical-source-manifest.json`:
  the historical accounting summary and normalized source commitments. Private
  original reports and ledgers are marked not distributed.
  Their historical counters retain their original dates and units. The
  separately preserved historical diagnostic summaries are in
  `../historical-diagnosis/` in the repository distribution.
- `separate-deposit-files.csv.gz`: root-relative producer filenames and observed
  physical byte sizes for the 453 closed roots. It is a proposal inventory,
  not an uploaded archive or a raw-database hash manifest.
- `SHA256SUMS`: hashes of the distributed snapshot bytes, including gzip
  containers. Proof hashes inside the JSON/CSV instead identify logical,
  uncompressed producer bytes. These are different hash conventions.

The production count is 453 closed plus 1,604 open, out of 2,057. Of the
closed producer receipts, 409 contain no tube operation and 44 contain at
least one. A tube-assisted root may also use G, SC and constructive covers;
the category does not assign its entire proof to one theorem.

The coordinator entered stage 2 with 392 closed roots and recorded 61
additional closures by capture. Its 136/1,665 stage visits count visits,
not closures. By the captured proof's retained analysis budget, stage 1
has 431 closed and 1,523 open roots, and stage 2 has 22 closed and 81 open.
Tube visits can retain an earlier budget, so proof-budget grouping is not
a chronology of closure. The 397,906 pending boxes are counted from the
captured individual proof versions. Active roots can change after their
read time; later versions are outside this release.

The historical late chain is
`3,524 - 15 - 25 - 1,401 - 1 - 4 - 21 = 2,057`.
The additional one is historical index 2411. Earlier reductions account
for 1,467 of the 3,524 residual inputs. Including current production gives
`1,467 earlier + 409 computed + 44 tube-assisted + 1,604 open = 3,524`.
These are production/accounting categories, not a full mathematical replay.

The static chain audit found no arithmetic inconsistency after restoring
the units and historical index. In particular, queue4's 12,666 unresolved
input jobs became 22,053 descendant leaves. The first sweep's 1,313
unresolved original roots contained 67,011 leaves. `remaining=0` in the
continuation controller meant no unprocessed input, not a completed cover.

The snapshot is immutable for this version. Do not replace its values with
later live counters when filling publication metadata or updating DOIs.

Raw historical equality-witness records are not distributed. Their original
filename, byte size and hash are in `omitted-historical-witness.json`. This
keeps every shipped mathematical certificate within the independently
replayed exclusion-checker input population.

## Public provenance and original capture commitments

`public-provenance.json` preserves the original snapshot manifest's byte size
and SHA-256 and the omitted controller record's 159-byte commitment.
The `coordinator_sha256` map inside byte-identical `summary.json` identifies
original captured coordinator bytes. Its `controller52.json` entry is an
original-capture commitment, not a claim that the file is distributed.
The current `SHA256SUMS` identifies only files actually shipped in this
public snapshot; public derivative files have their own current hashes.
Original capture times and every captured numerical counter are retained.

Source paths have been replaced with opaque source IDs and basenames.
Source byte sizes and digests are included where captured. The frozen
root-source commitments recorded SHA-256 but not source byte sizes, so
`source_bytes` is explicitly null. The separate-deposit inventory recorded
physical sizes but no raw file digests; its SHA field is empty and marked
`not captured`. Its paths are relative to the stated root directory.
These missing fields have not been inferred from new production reads.
The per-root status gzip is byte-identical to its original captured version.
