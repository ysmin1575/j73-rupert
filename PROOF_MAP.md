# Proof map for the J73 interim report

The paper proves local statements about projections of J73. This release
provides executable checks for the supplied local data. The complete
finite exclusion cover is still open. This map separates the mathematical
implications from the archive that would be needed to apply them globally.

## From a passage to a point in the reduced domain

For a convex solid, a passage with positive clearance gives strict
containment of one planar projection in another after a planar rigid
motion. J73 is centrally symmetric. Averaging a translated containment
with its central reflection reduces the exclusion question to centered
projections. The proper symmetries and the choice of screen frames then
give the closed five-angle domain used in the paper.

The original rational grid covers that domain. A finite replacement tree
would preserve the cover only if each replacement covers exactly the
same parent region and retains its closed boundary. A locally valid
inequality without that connection does not exclude an original root.

## Coincidence explains the local difficulty

An exact order-three rotation inherited from the parent solid does not
preserve J73, but it preserves certain projections. The paper constructs
the resulting open coincidence family. The independent program
`code/discovery/check.py` reconstructs the vertices, exact rotation
identities, sign comparisons, orbit and pose labels, and four-contact
identities. The included evidence is checked rather than accepted as a
saved verdict.

At an exact coincidence, a strictly positive separation margin is
unavailable. This does not give a passage: touching projections are not
strictly nested projections. It motivates signed, nonnegative contact
identities and neighborhoods whose boundary and equality cases are
included explicitly.

## Four certificate interfaces

| Interface | Mathematical reason for exclusion | Main checker code |
|---|---|---|
| G | An inner projected vertex has support strictly larger than every outer vertex in a fixed screen direction throughout the angular box. Outward bounds include the angular Taylor remainder. | `local.py:G`, `image.py` |
| SC | Genuine outer support contacts with nonnegative weights give a signed polynomial obstruction. Exact factors, image constraints and polynomial evidence must justify every zero and boundary case. | `local.py:SC`, `polynomial.py`, `image.py` |
| COVER | A finite family of certified children covers the declared original box. Box splits, fan partitions, coordinate charts and their connections are reconstructed, including shared boundaries. | `cover.py`, `image.py` |
| tube | A checked contact-facet or canonical mixed-intersection region excludes strict containment, and a checked coordinate/label map contains the entire original angular box in that region. | `tube.py`, `tube_intersection.py`, `image.py` |

These are interfaces, not four unrelated global arguments. COVER joins
local exclusions to the domain. A COVER can contain SC leaves; the local
SC inequality and the cover connection have separate obligations.

## Contact tubes

For a contact-facet region, the contact torques enclose a positive ball
of radius at least `c`. The rotation remainder is bounded above by
`C theta^2`. The condition `C r < c` makes
`c theta - C theta^2` positive for `0 < theta <= r`. At `theta = 0`, the
exact supporting contact itself excludes strict containment. All support
and positivity requirements hold over the declared closed view chart.

At the specified intersection of coincidence families, a positive
first-order bound may fail. The mixed-barrier theorem instead uses the
explicit canonical polynomial inequality, with the stated view and
rotation ranges. It does not authorize moving the center to an arbitrary
point of an equality family. Exact identity transfers must be checked.

`code/verify_tube_regions.py` verifies each `j45-region-v1` payload's
schema, geometry hash, exact reference rotation and local model. This
region-only test does not check original-box inclusion. For a tube
application, `tube.verify` additionally checks the whole angular box and
its transport labels. The supplied tube certificate exercises both parts.

## What is checked in this repository

The three disclosed local examples are identified individually in
`data/certificate-provenance.json`. Their source root, operation,
logical source hash and captured proof hash are recorded. They are not
complete root forests. The mathematical acceptance of those examples
does not establish the closure of their source roots.

The region bank contains all distinct payloads collected from the
recorded banks. Canonical JSON content hashes determine identity and
deduplication; family names and region IDs do not. Region provenance is
recorded separately. The release checker recomputes the inequalities
instead of trusting stored production PASS strings.

The frozen production-status directory fixes the observed production
counters and captured per-root versions. Its 453 closed roots and 1,604
remaining roots are production counters. The historical accounting
files establish how the staged job IDs were selected, but their ID-set
checks do not replay all preceding certificates. Historical frontier
English summary and equality-witness JSON retain their own capture times
and verification scope. The raw historical equality-witness collection
is not included in this repository. The four internal historical reports
are omitted sources with original sizes and SHA-256 values, not shipped
documents. The raw controller record is also omitted; `summary.json`
retains its original bytes and source digest. `public-provenance.json`
distinguishes those original capture hashes from the public derivative
files and snapshot manifest.

The release self-test checks file hashes, the supplied local certificates,
the full region bank, the independent discovery program and PDF page
count, PDF byte size, TeX source hashes and the current visual-check binding.
All five shipped historical diagnostic files are checked for existence,
byte size and SHA-256 against their own manifest. Omitted sources are
provenance only; there is no new equality-witness replay. The self-test does
not check every original-to-final replacement edge. Its scope is stated
in `data/release-selftest.json`. A final complete verification must retain
the exact command, Python and arithmetic dependencies, measured elapsed
time, code/input digests and complete input population in its receipt.

## What a complete global argument still requires

A final claim would require all of the following to be supplied and
verified together:

1. The exact vertex input, ordering, symmetry reduction and initial grid.
2. Every retained first-sweep witness and every adopted later replacement.
3. A finite, acyclic graph with the identical parent region at every
   replacement and no missing, duplicated or unsupported coverage.
4. Exact local inequalities and whole-box membership for every accepted
   leaf, including all shared boundaries and equality cases.
5. No unresolved, skipped, rejected or exceptional reachable leaf.
6. A fresh exhaustive replay of that fixed archive with its code,
   arithmetic dependencies, hashes and execution receipt.

The earlier proof dependency of a retained legacy certificate remains
necessary until that certificate is replaced and the replacement is
checked. A smaller proposed proof system does not by itself remove old
dependencies from the stored computation.

The remaining boxes include exact equality configurations, intersections
where first-order bounds degenerate, and original angular boxes that
cannot yet be placed wholly in an available local region. Refinement and
additional search have no established finite termination bound. The
paper therefore gives no completion date and draws no non-Rupert
conclusion for J73.

## Independent checker and trust base

The eight mathematical modules listed in `data/code-provenance.json` are
unchanged copies of checker v2. The release entrypoint is a new serial
harness with no timed or worker modes. Exact rational and quadratic-field
arithmetic, outward bounds, coordinate images and polynomial evidence
are implemented inside that checker; it imports no producer mathematics.

Independence from the producer reduces shared implementation assumptions
but is not a formal proof-assistant guarantee. The mathematical arguments,
checker/parser implementation, Python runtime and hardware remain in the
trust base. SHA-256 fixes the reviewed inputs; it does not prove the
mathematical statements in those inputs.
