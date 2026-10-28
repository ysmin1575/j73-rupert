# Towards a computer-assisted exclusion of Rupert's property for the parabigyrate rhombicosidodecahedron

Interim report, version 0.1. Sumin Yoo, Independent researcher, Republic of Korea.

Publication date: 28 October 2026.
Repository: https://github.com/ysmin1575/j73-rupert.

This release presents local exclusion theorems for Johnson solid J73, an
independent checker, a small set of local certificates, tube regions, and a
frozen account of the running computation. The computation and exhaustive
verification of the complete cover remain unfinished. No conclusion that
J73 is non-Rupert is claimed, and no completion date is given.

## What the release establishes

The paper proves a hidden family of coincident projections and gives local
exclusion criteria based on support gaps, signed contacts, contact patches,
and a mixed barrier at a specified intersection of coincidence families.
The proof map in [PROOF_MAP.md](PROOF_MAP.md) connects these statements to
the four certificate interfaces: G, SC, COVER, and tube.

The exact discovery program was rerun during preparation. It reproduced
the 1,440 sign checks, comprising 1,404 positive values and 36 zeros, and the
rotation, orbit, pose-label, and four-contact identities described in the
paper. That run took 1.400 seconds on the preparation machine while
production continued.

The supplied local certificate set consists of one G certificate, one
COVER certificate with its local subcertificates, and one tube application.
They were selected in increasing closed-root index and operation order as
the first available example of each of those forms. This is a disclosed
example set, not a statistical sample. No complete staged-root forest is
claimed to be included or independently verified by these three files.

The tube bank contains all 2,660 distinct regions collected for this
release: 2,658 contact-facet regions and two astra-intersection regions.
Each payload retains the single `j45-region-v1` format. Replaying a region
establishes its local inequalities. It does not, by itself, establish that
an original angular box lies inside it. The separate tube application
certificate includes that connection.

An earlier serial standalone replay accepted every supplied local certificate
and all 2,660 regions in 1687.151 seconds. Its original input/kernel hashes
and result remain in `data/checker-replay.json`. The current release self-test
run is recorded separately in `data/release-selftest.json`, with its exit code,
checks, measured time, environment and code/input digests. It checks the
manifests, all three local certificates, all 2,660 regions, discovery and PDF
metadata. The final distribution is also tested from a new local Git clone;
that packaging receipt accompanies the release. Tests print to standard output
and do not change repository files. These are local-evidence results, not
acceptance of a complete staged root or the original-to-final cover.

## Run the checks

Use Python 3.11 or later. The mathematical checker and the discovery
program use the Python standard library. The release self-test also uses
`pypdf==6.20.1` to read the actual PDF page tree.
Download or clone the repository, open a terminal in the directory containing README.md, and run:

```powershell
python -m pip install -r requirements.txt
python -X utf8 -B self_test.py
```

The self-test verifies the SHA-256 manifests, replays every supplied local
certificate and every tube region, runs the discovery checks, and checks
the paper's PDF page count. It uses only files in this repository. It does
not query the live production folders or rerun the search. A successful
exit is evidence for those tasks only.

The mathematical checks can also be run separately without installing
`pypdf`:

```powershell
python -X utf8 -B code/checker/check.py
python -X utf8 -B code/verify_tube_regions.py
python -X utf8 -B code/discovery/check.py
```

The first command checks all supplied certificates and all regions. The
second repeats the region-only part. The entrypoints are serial and have
no runtime, worker, or sampling caps. They do not start producer workers.
The preparation runs were scheduled one at a time alongside the ongoing
production computation. Runtime on another machine can differ.

Here, absence of caps means there is no runtime deadline, worker limit or
sampling cutoff in the replay tools. Input-format and resource limits still
apply: polynomial exponents are at most 64, a Bernstein conversion permits
at most 1,000,000 coefficients, and tube grids must be integers from 1 to 16.
Unsupported or oversized inputs fail with an exception and a nonzero exit;
they are not skipped or reported as partial success.

Do not run Python with `-O` or `PYTHONOPTIMIZE`. The self-test rejects
optimized execution. If saving the test output, write it outside this
repository so that the recorded distribution files remain unchanged.

## Frozen production status

The current counters below come from `data/status-snapshot/summary.json`,
captured on 27 October 2026 from 10:40:50.233026 to 10:41:21.245658 KST
(01:40:50.233026 to 01:41:21.245658 UTC). The production coordinator's
recorded update was 01:40:48.467462 UTC. The capture read logical records
through the compact-storage API with read-only database connections.

| Production counter | Frozen value |
|---|---:|
| Staged input roots | 2,057 |
| Closed roots | 453 |
| Remaining roots | 1,604 |
| Captured pending boxes | 397,906 |
| Current production stage | 2 |
| Stage visits recorded | 136 of 1,665 |
| Closed at the start of stage 2 | 392 |
| Additional closures recorded by capture | 61 |

These are production counters, not independently verified global results.
Coordinator counts and state remained unchanged during capture; its
heartbeat changed. Individual active-root versions were observed during
the stated interval. This is a rolling capture, not an atomic filesystem
snapshot. The exact captured versions and per-root values are retained.

The closing-rule classification is disjoint: a root with a tube
application is classified as tube-assisted; the other closed roots are
classified as computed G/SC/COVER closures.

| Captured proof-object stage | Computed G/SC/COVER | Tube-assisted | Closed total |
|---|---:|---:|---:|
| 1 | 392 | 39 | 431 |
| 2 | 17 | 5 | 22 |
| Total | 409 | 44 | 453 |

The proof-object stage describes the captured proof record. It is not the
coordinator's chronological stage accounting, so its rows must not be
substituted for the coordinator's 392 earlier and 61 additional closures.

The snapshot directory contains the open-root list, captured root-version
identifiers, a compressed per-root CSV, public coordinator counters and its
own `SHA256SUMS`. The raw controller record is not distributed. Its original
159-byte size and SHA-256, the original snapshot-manifest digest, and the
bindings of public derivatives are in `data/status-snapshot/public-provenance.json`.
The original `summary.json` bytes are preserved; its controller digest
identifies omitted source bytes, not an included file. The top-level
manifest binds the public release. A hash identifies bytes; it does not
establish a mathematical inequality.

## How the root populations are related

The first sweep used `12 × 17 × 12 × 17 × 30 = 1,248,480` angular roots.
After successive replacements, its unresolved descendants formed the
queue8b population of 3,524 jobs. These are different units: a later job
can be a descendant of an original root. The complete accounting trail is
in `data/historical-accounting.md` and `data/historical-chain.json`.

The later ID accounting is:

```text
3,524 − 15 (queue10) − 25 (J39) − 1,401 (continuation6) = 2,083
2,083 − 1 (historical closure of index 2411, imported in J42) = 2,082
2,082 − 4 (prior closures) − 21 (J47 closures) = 2,057 staged jobs
```

The ID partitions were checked against the frozen historical ledgers.
This is an accounting check, not a new replay of all their mathematical
certificates. Two other distinctions matter: queue4 left 12,666 input jobs
open but emitted 22,053 descendant leaves; and continuation6's
`remaining=0` meant that no input job awaited processing, while unresolved
geometric jobs remained. The apparent discrepancies disappear when those
units and index 2411 are included.

## Historical frontier diagnosis

The dated English summary in `data/historical-diagnosis/README.md` describes an earlier
frontier captured near 01:16–01:17 KST on the same date. Its 1,615 open jobs
and 370,364 boxes are historical diagnostic values, not replacements for
the release's 1,604 remaining roots and 397,906 captured boxes. The
width-dependent and fixed 0.01-radian family classifiers must not be combined.

The historical summary records an exact equality-witness collection covering
11,170 boxes in 577 jobs: 5,452 identity boxes and 5,718 T-equality boxes.
The summary reports checks of all positive witnesses during generation or recovery.
The separate historical audit rechecked all identity witnesses and a sample
of 120 T witnesses, rather than replaying all T witnesses a second time.
This repository retains the English historical summary, diagnostic JSON and source-file
hashes; the raw `lambda1_witnesses.jsonl.gz` collection is not included.
The release self-test checks the existence, byte size and SHA-256 of all five
shipped historical files against `historical-diagnosis-manifest.json`.
The four internal reports and raw witnesses are recorded as omitted sources,
not required repository paths. No new historical equality-witness replay is
claimed. The paper and `data/historical-accounting.md`
explain the scope, depth distribution, and why proximity labels cannot
establish exact equality incidence. `DATA_DEPOSIT.md` identifies the raw
historical file for an optional separate deposit.

## Files and data limits

| Path | Contents |
|---|---|
| `paper/` | Integrated interim article, TeX sources and figures |
| `PROOF_MAP.md` | Mathematical argument, certificate interfaces and outstanding obligations |
| `code/checker/` | Independent checker v2 mathematical kernel and serial release entrypoint |
| `code/discovery/` | Unchanged discovery checker and its exact evidence |
| `code/verify_tube_regions.py` | Region-only entrypoint over the independent kernel |
| `data/certificates/` | Three disclosed local examples |
| `data/tube-regions.json` | All 2,660 distinct region payloads |
| `data/status-snapshot/` | Frozen current production status and source-file inventory |
| `data/historical-diagnosis/` | Dated English historical summary and four diagnostic JSON files; internal reports and raw witnesses omitted |
| `data/*provenance*.json` | Certificate, region and source-code provenance |
| `data/checker-replay.json` | Standalone all-input checker result with code and input bindings |
| `data/pdf-metadata.json` | Declared PDF page count and PDF identity |
| `DATA_DEPOSIT.md` | Scope and exact physical inventory for the closed-root certificates to accompany the final version |

The observed closed-root producer files total 559,517,066 bytes across
3,771 files, larger than the intended GitHub data budget. Each observed
file is below 50 MB; the largest is 8,867,840 bytes. The full closed-root
certificates are not deposited in this interim version; they will accompany
the final version. No deposit date is promised. The exact observed inventory is
`data/status-snapshot/separate-deposit-files.csv.gz`. It is not a frozen
copy of mutable database containers or a verified certificate archive.
See [DATA_DEPOSIT.md](DATA_DEPOSIT.md) for what a separate deposit would
need. No such online data record has been created during preparation.

## Checker provenance and trust

Eight mathematical modules are copied unchanged from checker v2:
`exact.py`, `polynomial.py`, `geometry.py`, `image.py`, `local.py`,
`cover.py`, `tube.py`, and `tube_intersection.py`. Their source hashes are
recorded in `data/code-provenance.json`. The release `check.py` is a new
serial harness with no runtime, worker or sampling cutoff over those predicates.
The input-format and resource limits listed above still apply. The source CLI with timed
or worker modes, and its bounded exporter, are not release reproduction
tools and are not shipped.

The checker uses exact rational and quadratic-field arithmetic and
outward interval bounds. Saved producer verdicts and proposed directions
are inputs to be checked, not trusted conclusions. The remaining trust
base includes the mathematical arguments, parser, arithmetic and geometry
implementations, Python runtime and hardware. A complete proof-assistant
verification has not been supplied.

## Rebuild the paper or update metadata

Typesetting is separate from the mathematical tests. With Tectonic
installed, run from this repository:

```powershell
Push-Location paper
tectonic --untrusted paper.tex
Pop-Location
```

Tectonic may download TeX resources on its first run. A page count is an
integrity check, not a substitute for viewing the PDF. Inspect the title
page, status table and AI-use paragraph after changing the article, and render
and inspect every page image for clipping, overlap, missing glyphs and legibility.

After intentional document or metadata changes, run:

```powershell
git add -A
python -X utf8 -B refresh_hashes.py
git add SHA256SUMS
python -X utf8 -B self_test.py
```

`refresh_hashes.py` updates the top-level manifest. It leaves the frozen
snapshot's internal manifest intact. The Git commands apply in a Git checkout;
omit them for a downloaded source archive. The hasher and ZIP builder apply
the same `.gitignore` exclusions. In a checkout the manifest paths plus
`SHA256SUMS` must equal the Git-tracked list; stage additions and deletions
before refreshing. The self-test repeats the file-set check.

After typesetting, update `data/pdf-metadata.json` with actual bytes, pages,
PDF SHA-256 and the SHA-256 of every TeX source, including figures. Move the
previous visual-check record to `visual_review_history`; create a new
`visual_review` with the time, every inspected page, observations, PDF SHA
and TeX bindings only after viewing every new page image. Refresh the public
self-test receipt after a new full run, then refresh hashes. Final packaging
must be tested from a new Git-tracked clone. Do not change certificate data
or checker predicates to make a failed test pass.

From that verified Git checkout, build the deterministic archive outside it:

```powershell
python -X utf8 -B build_release.py ..\j73-rupert-v0.1.0.zip
```

The builder checks every hash and requires an exact match to the Git-tracked
file list. Ignored virtual environments, PDF logs and page images are excluded.

## Citation, licences and confirmation

Software version DOI: [AUTHOR-CONFIRM: version-specific software DOI]

Software concept DOI: [AUTHOR-CONFIRM: software concept DOI]

Paper DOI: [AUTHOR-CONFIRM: separate preprint DOI]

Use the software version-specific DOI when it has been issued, and cite
the paper separately. `CITATION.cff` describes software version 0.1.0.
The publication date is 28 October 2026, and the repository URL is
https://github.com/ysmin1575/j73-rupert. The article is labelled
`Interim report, version 0.1`. Only the three DOI fields above remain
visible AUTHOR-CONFIRM items; they are filled after Zenodo issues them.

Code is MIT licensed. The paper text and data are CC BY 4.0. Retain
`LICENSE`, `LICENSE-CC-BY-4.0.txt`, `LICENSES.md` and the upstream notices.
The original Gihyo Jung MIT attribution is preserved in `NOTICE`.

Claude (Anthropic) and OpenAI Codex assisted with literature checks,
mathematical derivations, code and drafting. Mathematical acceptance
requires the exact or outward-rounded checks described above; it does
not follow from a language-model response. The author directed the project
and takes responsibility for the submitted text. Verification of the complete
certificate chain remains unfinished.
