# Source-to-claim map for the interim report

The mathematical statements and proofs are in `paper/paper.tex`. The paths
in the first table identify files distributed in this repository, relative
to its root. Historical source records that are not distributed are listed
separately by stable source ID, basename, size, date and SHA-256. Their
digests identify the original source bytes; they are not links to files
included in this release.

The current counters are fixed by `data/status-snapshot/summary.json`.
Historical accounting and diagnostics have their own dated populations.
Neither population is an exhaustive verification of the original grid.

| Paper content | Distributed source | Scope |
|---|---|---|
| Exact body, vertex numbering, D5 reduction and rational first grid | `paper/paper.tex`, Section 2 and Section 7.1; `code/checker/geometry.py`; `data/status-snapshot/release-input-binding.json` | The construction and reduction are stated in the paper; the checker reconstructs the declared body. The complete original-root cover is not replayed by this release. |
| Open coincidence cone, order-three rotation, orbit, pose labels and four contacts | `paper/paper.tex`, Section 3; `code/discovery/check.py`; `code/discovery/evidence.json`; `data/discovery-replay.json` | The integrated discovery argument and its exact program are included. The discovery program does not import production modules. |
| Uniform contact patch | `paper/paper.tex`, Theorem 4.2; `code/checker/tube.py` | The paper gives the general theorem and proof. The checker implements the four-contact contact-facet form. |
| Signed contacts and exact polynomial evidence | `paper/paper.tex`, Theorem 4.3; `code/checker/local.py`; `code/checker/polynomial.py` | Submitted evidence must satisfy the exact support, weight and nonnegativity obligations. |
| Closed fan polygons and rotation cones | `paper/paper.tex`, Section 4.4; `code/checker/cover.py` | Closed-child union and the view, rotation and original-angle image obligations are part of acceptance. |
| Canonical mixed-barrier tube | `paper/paper.tex`, Section 5; `code/checker/tube_intersection.py`; `data/tube-regions.json` | The stated canonical intersection, clamped coordinates, support table and conservative constants are retained. An arbitrary change of center is not justified. |
| Whole-box membership | `paper/paper.tex`, Section 6; `code/checker/image.py`; `code/checker/tube.py`; `code/checker/cover.py` | Every accepted local application needs its checked coordinate image and whole-box inclusion. |
| Four certificate types and trust base | `paper/paper.tex`, Sections 6.2 and 9; `PROOF_MAP.md`; `code/checker/`; `data/code-provenance.json`; `data/release-selftest.json` | The release checks G, SC, COVER and tube evidence within its stated local population. Stored producer verdicts do not constitute acceptance. |
| Current stage and rule counters | `data/status-snapshot/summary.json`; `data/status-snapshot/per-root-status.csv.gz`; `data/status-snapshot/captured-root-versions.json`; `data/status-snapshot/README.md` | Rolling capture on 27 October 2026, 10:40:50.233026-10:41:21.245658 KST. These are production counters. The raw controller record is not distributed; its original digest remains provenance. |
| Historical root accounting | `data/historical-accounting.md`; `data/historical-chain.json`; `data/status-snapshot/earlier-closures.json`; `data/source-evidence-manifest.json` | The static audit checks units and disjoint ID partitions, not every historical mathematical certificate. |
| Historical family, depth and scale-one witnesses | `paper/frontier.tex`; `data/historical-diagnosis/README.md`; `data/historical-diagnosis/census_summary.json`; `data/historical-diagnosis/final_metrics.json`; `data/historical-diagnosis/witness_summary.json`; `data/historical-diagnosis/findings_verification.json` | Historical rolling capture on 27 October 2026, 01:16:44-01:17:26 KST. Midpoint family labels are distinct from rigorous positive witnesses. The 3,304,005-byte raw equality-witness file is not distributed or replayed by this release. Its original digest is in the omissions inventory. |
| Historical tube-frontier coverage and independent verification | `data/historical-diagnosis/README.md`; `data/status-snapshot/historical-diagnosis-manifest.json` | The 26 October 2026 pending-frontier result is distinct from an original-grid proof and is not added to current production counters. The released checker supports tube certificates; earlier descriptions of unsupported tube checking are superseded. |
| Legacy witness dependencies | `paper/paper.tex`, Sections 6.2, 9 and 10; `PROOF_MAP.md` | Balls, tapers and collision arguments have not all been replaced by independently verified G/SC/COVER/tube evidence. Their original proof dependencies remain obligations wherever those witnesses are retained. |

## Private historical source records

The following records are **not distributed**. The date 2026-10-27 is the
date of the frozen provenance inventory, not a claim about each record's
creation date. Full source identifiers, sizes and digests also appear in
`data/source-evidence-manifest.json`. This table records provenance and
does not provide missing proof payloads or a new mathematical replay.

| Source ID | Basename | Bytes | Provenance date | SHA-256 |
|---|---|---:|---|---|
| `src-14c86cbed8f0f001` | `INVENTORY_v2.md` | 15,102 | 2026-10-27 | `14c86cbed8f0f001ec0368d3020b881bbd6cc911c03103476dba74bf6c7e4f8c` |
| `src-fdc77b2b3dd84f4c` | `MAP_v2.md` | 8,767 | 2026-10-27 | `fdc77b2b3dd84f4ca805c35c81bd893672ca8248795d355f922b4202c1b57e00` |
| `src-ca6e021cfc12af91` | `TCB_v2.md` | 3,101 | 2026-10-27 | `ca6e021cfc12af914f58a20306ab108d02565261dbb995d46c73b0bd3439656b` |
| `src-e81b555efe10ef7c` | `theorem.md` | 7,254 | 2026-10-27 | `e81b555efe10ef7c28e462e028250aca7d3c03da5f8932719bd73e3a0c69a694` |
| `src-917e39759c5a7705` | `containment_static.md` | 17,359 | 2026-10-27 | `917e39759c5a77058ef3cc53de414f1b03622b6961eec2173808fe6ac597e113` |
| `src-cbdc118ba294b922` | `theorem_static.md` | 16,700 | 2026-10-27 | `cbdc118ba294b922c62aa4b674067175b65f34f1ff718b1c3bc58f082f81dfbf` |

The full original-to-final certificate chain remains unfinished. The
external references follow the earlier source audit; this report does
not claim a new exhaustive literature search. The earlier snub-cube note
is cited only for the distinction between a touching family and a strict
passage.
