# Proposed separate deposit of staged closed-root data

The GitHub interim package includes three disclosed local certificates
and every tube region collected for this release. It does not include
the complete certificate forests for the closed staged roots. The full
closed-root certificates (about 560 MB of observed producer files) are not
deposited in this interim version; they will accompany the final version.
No deposit date is promised. No separate Zenodo data record has been
created during preparation.

## Exact observed source-file inventory

The frozen capture identifies 453 closed staged roots. Their observed
producer files are listed individually in
`data/status-snapshot/separate-deposit-files.csv.gz`:

| Inventory property | Value |
|---|---:|
| Files | 3,771 |
| Total observed physical bytes | 559,517,066 |
| Largest observed file | 8,867,840 bytes |
| Packed-operation database containers | 453 |
| Root metadata files | 3,318 |

Each CSV row has `root`, an opaque `source_id`, `basename`,
`root_relative_path`, `bytes`, `sha256`, `digest_status` and `role`.
Paths are relative to the directory for the stated root. The SHA-256 field
is empty and `digest_status` is `not captured`: the frozen inventory
measured physical sizes but did not hash live raw producer files. Source
IDs identify inventory entries, not content hashes. The CSV and its
snapshot metadata are bound by the snapshot's SHA-256 manifest. Every observed file is below
50 MB, but the aggregate exceeds the intended GitHub data budget of
about 300 MB.

This is an exact inventory of the files and physical sizes observed for
those captured closed roots. It is not a byte-for-byte frozen copy of
their database containers. Container sizes can include unreferenced
artifact versions. Raw databases were not copied or hashed while
production was running, so the inventory must not be represented as a
content-hash manifest for a ready-to-upload database archive.

## Proposed deposit scope

The proposed data record would preserve the logical certificate forests
referenced by the captured versions of those 453 roots, together with
the metadata needed to decode, bind and replay them. It should include:

1. The exact captured root/proof identifiers already listed in the status
   snapshot, and all logical operations referenced by those proof versions.
2. Canonical portable certificate records or the documented logical
   compact-storage export, with SHA-256 values for the exported bytes.
3. The exact input geometry, root boxes and symmetry/label bindings.
4. Every referenced region and mathematical dependency, using the
   `j45-region-v1` payloads where applicable.
5. A manifest giving the final exported filenames, exact sizes, hashes,
   encoding and decompression specification, and their relation to this
   release's captured versions.
6. The verification commands, unchanged checker provenance, and an
   exhaustive receipt for the files actually deposited.

The named source-file CSV is the extraction inventory, not a requirement
to deposit every producer file unchanged. Logs, heartbeats, scratch data
and unreferenced versions need not be included. Their removal and any
logical normalization must be documented, with the final exported size
and file list measured after extraction. Nothing in this proposal permits
modifying the running production directories.

An optional, separate historical diagnostic deposit could also preserve
`lambda1_witnesses.jsonl.gz`, source ID `src-381e7f19af08480a4` (3,304,005 bytes;
SHA-256 `381e7f19af08480a446ab880e00ffb17c164bece50432d957a797b40c02610a4`).
Its source ID, basename, original size and digest are recorded in
`data/source-evidence-manifest.json`. That raw file is not distributed
in this GitHub release and is not part of the closed-root inventory
above. Any such deposit should document its historical encoding,
recovery and replay scope; it is not a checker v2 exclusion certificate.

## Earlier-chain dependencies

Even a complete deposit of the closed staged-root forests would not be a
complete original-grid proof. Staged inputs came from earlier replacement
queues. A full-chain archive would additionally need the original grid,
all retained earlier leaves, the selected replacement graph, the exact
unchanged parent region at every handoff, and the original mathematical
dependencies of every legacy witness not replaced and rechecked.

`data/historical-accounting.md` and `data/historical-chain.json` document the population
accounting. Their static ID partition checks do not supply missing
certificate arithmetic. The final deposit must distinguish independent
verification of local records, whole staged-root replay, and exhaustive
original-to-final cover verification. It must not combine them into one
unqualified PASS statement.

## Suggested record metadata

Use a separate Zenodo Dataset record under CC BY 4.0, by Sumin Yoo,
Independent researcher, Republic of Korea. A suitable title begins
`Towards a computer-assisted exclusion of Rupert's property for J73:`
and describes the fixed staged-root certificate data. State the capture
interval and exact verification scope in the description. Do not use the
paper DOI or software DOI as the dataset's own DOI.

After publication, link the dataset from the paper as supplementary
material and retain the dataset's version-specific DOI in the software
README. A future dataset revision should preserve its own fixed manifest
and state which earlier version it extends. The author performs the
deposit and publication; this document only prepares its scope.
