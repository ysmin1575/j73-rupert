# Historical accounting and diagnostic evidence

This document records static historical reports and ledgers. It does not
replay their mathematical certificates. Historical counts are tied to the
source identifiers, original byte sizes and SHA-256 values in
`source-evidence-manifest.json`. Private original documents are marked not distributed.
The current production counters are confined to the frozen release snapshot.

## The chain and its units

The original grid is `12 × 17 × 12 × 17 × 30 = 1,248,480` angular roots.
The first sweep recorded 1,247,167 closed roots and 1,313 roots with unresolved
descendants. Those 1,313 roots contained 67,011 unresolved leaves. These count
different objects. Its 48,895,305 accepted leaves are a historical production
count, not a fresh full-chain independent verification.

A later input job can be an unresolved leaf or a descendant of an original
root. The following is an accounting trail, not repeated subtraction from
the original grid.

| Historical stage | Input jobs | Closed input jobs | Output unresolved leaves or jobs | Qualification |
|---|---:|---:|---:|---|
| First sweep | 1,248,480 original roots | 1,247,167 original roots | 1,313 original roots, containing 67,011 leaves | Original roots and leaves differ. |
| First follow-up | 67,011 leaf jobs | 31,713 of 32,420 processed | 1,133,950 leaves plus 34,591 unprocessed jobs | 32,420 + 34,591 = 67,011. |
| Switched follow-up | 1,168,541 | 924,341 | 244,200 | 1,133,950 + 34,591 = 1,168,541. |
| Reduction A | 244,200 | 207,305 | 36,895 | G closures. |
| Reduction B | 36,895 | 4,563 | 32,332 | Ordinary subtraction applies. |
| Reduction C | 32,332 | 19,666 | 22,053 | 12,666 inputs remain open; splitting expands them. |
| Reduction D | 22,053 | 17,294 | 4,759 | The intervening exploratory queue was not adopted. |
| Reduction E | 4,759 | 654 | 4,105 | Ordinary subtraction applies. |
| Reduction F | 4,105 | 581 | 3,524 | 1,248 stored certificates do not mean 1,248 closed roots. |

An exploratory queue after Reduction F was not a production replacement.
The 3,524 residual jobs form the later index population `0..3523`.
The first three subsequent reductions remove 15, 25 and 1,401 jobs:
`3,524 − 15 − 25 − 1,401 = 2,083`.
A separately recorded closure of job 2411 leaves 2,082. Removing the four
prior closures `{125,255,1052,1995}` gives 2,078. Removing another 21 closures,
comprising 18 held-out and three targeted jobs `{1068,3061,3346}`, gives the
2,057 staged inputs.

The exact final 21 indices are
`37,573,574,763,793,1068,1258,1638,1893,1930,2051,2103,2208,2421,2427,2713,2778,3061,3193,3320,3346`.
The historical ledger, imported closure and effective residual sets were
checked to be disjoint and exhaustive; the staged set equals the effective
residual set minus the prior four and final 21. The shipped
`historical-chain.json` and `status-snapshot/earlier-closures.json` retain the accounting and ID partition.
This is a ledger check, not a new mathematical replay of the underlying proofs.

Three distinctions explain the apparent discrepancies:

1. `32,332 − 19,666 = 12,666` counts open inputs; 22,053 counts descendant leaves.
2. `3,524 − 15 − 25 − 1,401 = 2,083`; job 2411 supplies one further closure.
3. A historical controller's `remaining=0` meant no unprocessed inputs.
   It still had 1,645 open jobs among 3,046 attempted inputs.

## Historical tube-frontier coverage

For a fixed nonzero view and exact reference rotation, `contact-facet`
certificates give actual contacts and supporting normals over a closed
view chart. Their torques enclose a positive ball of radius at least `c`;
a second-order rotation remainder is at most `C θ²`. With `0 < r ≤ 1`
and `Cr < c`, the support gap is at least `cθ − Cθ²` for `0 < θ ≤ r`.
At θ = 0 the exact contact excludes strict containment. Central symmetry
reduces translated strict containment to centered strict containment.
This local theorem makes no global J73 conclusion.

The existing `astra-intersection` schema describes two intersecting exact
equality branches. The canonical T model and its verified identity transfer
use the same polynomial barrier, bounded below by `(|X|+Q+e)/525`, on the
specified box with halfwidth at most `1/9600`. Moving that center to an
arbitrary equality point is not justified. The public theorem statements
and unchanged checker are in `paper/paper.tex` and `code/checker/` relative
to the repository root.

The historical frontier captured on 26 October 2026 at
10:25:18.766258–10:25:49.262151 KST contained 2,057 staged jobs, of which
1,662 were open with 358,906 pending boxes. The region union covered 7,450
pending boxes and all pending boxes of 39 jobs. Twenty of 42 depth-limited
jobs were fully covered. Attribution to the initial atlas, existing frame
regions and newly generated regions gives `4,274 + 1,079 + 2,097 = 7,450`.
There were 475 new regions and 132 regions used in the final coverage.
The historical independent check replayed all 475 new regions, 7,450
inclusions, 39 complete frontiers and their 1,365 tube applications.
These are historical pending-frontier results, not complete original-grid proofs.
Later historical records describe corrections to operational and helper
completion behavior. The current release's checker support is defined by
its distributed code and README.

## Historical frontier diagnosis

The frontier captured on 27 October 2026 at 01:16:44–01:17:26 KST contained
1,615 open jobs and 370,364 boxes. Two numerical classifiers used different
proximity rules. The width-dependent rule chooses a catalogue rotation
within the sum of five box halfwidths plus `1e-10`; the fixed rule uses
midpoint rotation distance at most 0.01 radian. Both prioritize exact
identity intersections. Their classifications must not be combined.

| Family | Width-dependent proximity | Fixed 0.01-rad proximity |
|---|---:|---:|
| T | 64,318 | 55,032 |
| D5 | 15,383 | 27,666 |
| H1 | 30,317 | 38,082 |
| CT | 16,194 | 50,593 |
| TC | 8,828 | 11,295 |
| H4 | 5,840 | 2,555 |
| identity | 5,452 | 5,452 |
| other | 10,676 | 16,142 |
| none | 213,356 | 163,547 |
| Total | 370,364 | 370,364 |

| Depth | Pending boxes | Qualification |
|---|---:|---|
| 0–5 | 34,772 | Subdivision of the shallow band. |
| 6–9 | 254,371 | Together, depth 0–9 has 289,143 boxes. |
| 10–19 | 79,239 | Both historical reports agree. |
| 20–29 | 1,650 | Both historical reports agree. |
| 30 | 332 | All pending boxes of 23 jobs have depth 30. |

The historical positive equality search reported 11,170 boxes in 577 jobs:
5,452 identity boxes in 267 jobs and 5,718 T boxes in 316 jobs. The job sets
overlap. The other 359,194 boxes are UNKNOWN, not negative equality results.
Of the T witnesses, 2,122 had midpoint label `none`; midpoint proximity
therefore cannot decide exact equality incidence. Positive witnesses were
checked during generation or recovery. A separate audit rechecked all
identity witnesses and 120 T witnesses, rather than all 5,718 T witnesses.
A narrower sufficient search found 5,452 identity and 126 additional D5
boxes, totalling 5,578 boxes in 285 jobs. These were different searches on
the same historical frontier.

The dated summaries and witness-file omission are described in
`historical-diagnosis/README.md`. The 1,615 historical open jobs are not the current release's
1,604. The raw equality-witness payload is not distributed and the release
does not replay those historical witnesses.

Most raw angular volume lies in shallow broad boxes, while tiny descendants
near equality can keep a job open. Exact scale-one points prevent a strictly
positive G support margin; nonnegative SC certificates may still apply.
SC construction must handle exact active weights and vanishing factors or
an appropriate square/DAG proof. A positive uniform first-order torque
radius can fail at intersecting equality branches. Every tube application
also requires whole-box inclusion; midpoint incidence alone does not close
a job. Private-copy subdivision and tube experiments on overlapping
historical inputs are not added to current production closure counts.
The historical records establish no finite completion date.

## Region extraction and released verification

`tube-regions.json` contains 2,660 unique `j45-region-v1` payloads: 2,658
`contact-facet` and two `astra-intersection` regions. Identity is SHA-256
of UTF-8 JSON with sorted keys and separators `,` and `:`. The source
records are in `tube-region-provenance.json`.

| Source basename | Records |
|---|---:|
| `initial_regions.json` | 2,156 |
| `generated_regions.json` | 475 |
| `runtime_regions.json` | 2,631 |
| `fitted_regions.json` | 3 |
| `demand_regions.json` | 11 |
| `new_regions.json` | 15 |

Initial plus generated equals the runtime bank. The 29 later regions add
distinct payloads; deduplication uses content, not family or region ID.
The release copies eight mathematical checker modules unchanged and uses
a serial harness with no runtime, worker or sampling cap. Input-format
and resource limits still apply and fail by exception. The harness replays
all three shipped local certificates and the complete region bank.
Region checks alone do not establish inclusion of an original angular box.
The full-chain obligations remain the original cover, every replacement,
exact local arithmetic, all box connections and no missing or unresolved
region. Shipped examples do not replace that unfinished full-chain replay.
