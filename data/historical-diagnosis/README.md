# Historical diagnostic summaries

The historical frontier captured on 27 October 2026 at 01:16:44–01:17:26 KST
contained 1,615 open jobs and 370,364 boxes. The fixed 0.01-radian midpoint
classifier and the depth counts are recorded in [census_summary.json](census_summary.json)
and [final_metrics.json](final_metrics.json). The historical witness search
reported scale-one configurations in 11,170 boxes from 577 jobs: 5,452 identity
boxes and 5,718 T boxes. Positive witnesses were checked during construction
or recovery; a separate audit rechecked every identity witness and 120 T
witnesses, as recorded in [findings_verification.json](findings_verification.json).
The raw equality-witness file is not included, and these historical witnesses
are not replayed by this release. The root sets overlap; family root counts
must not be added. The other 359,194 boxes are UNKNOWN, not negative results.
The historical search summary is [witness_summary.json](witness_summary.json).

A separate frontier captured on 26 October 2026 contained 1,662 open jobs
and 358,906 pending boxes. The tube study covered 7,450 boxes and the complete
pending frontiers of 39 jobs; 1,365 tube applications in those complete
frontiers were checked independently. These results concern the captured
pending frontiers, not complete original-grid proofs. They are not added
to the current production counters.

The earlier width-dependent midpoint classifier and the fixed 0.01-radian
classifier used different proximity rules; their family totals describe
different numerical diagnostics. Neither midpoint classification decides
the presence or absence of an exact scale-one configuration. Private-copy
experiments on these historical inputs are not current production closures.
No finite completion date follows from these records.

The four internal reports are not distributed. Their original byte sizes
and SHA-256 values are retained under `omitted_source_files` in
[historical-diagnosis-manifest.json](../status-snapshot/historical-diagnosis-manifest.json).
That manifest's `files` list contains only the five shipped files in this
directory. The original equality-witness file, `lambda1_witnesses.jsonl.gz`,
has 3,304,005 bytes and SHA-256
`381e7f19af08480a446ab880e00ffb17c164bece50432d957a797b40c02610a4`;
it is also listed in [omitted-historical-witness.json](../status-snapshot/omitted-historical-witness.json).
Its format is not accepted by the released exclusion checker. These dated
summaries are historical evidence, not mathematical acceptance inputs or
the current release counters.
