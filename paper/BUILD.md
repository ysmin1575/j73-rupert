# Build the interim paper

From the repository root, with Tectonic installed:

```powershell
Push-Location paper
tectonic --untrusted --keep-logs paper.tex
Pop-Location
```

Stop if a command fails. The first build may download public TeX
resources. A local cache can be used with `--only-cached`. Typesetting is
separate from mathematical verification. The publication date (28 October
2026), repository URL (https://github.com/ysmin1575/j73-rupert), and AI-use
responsibility sentence are already filled in. Only the software version
DOI, software concept DOI, and paper DOI remain visible AUTHOR-CONFIRM
items until Zenodo issues them.

After any intentional source or PDF edit:

1. Rebuild the PDF with Tectonic and inspect an image of every page for
   clipping, overlap, missing glyphs, readable equations and tables, and
   visible AUTHOR-CONFIRM items that remain unresolved.
2. Update `data/pdf-metadata.json` with the actual PDF byte size, page
   count, PDF SHA-256, and SHA-256 of every recorded TeX source. Add a new
   visual-check record with its actual time, PDF digest, pages inspected
   and observations. Keep the previous visual-check record as history;
   a check of an earlier PDF does not apply to a rebuilt PDF.
3. In an existing Git checkout, run `git add -A` first to stage intended
   additions and deletions. Then run `python -X utf8 -B refresh_hashes.py`
   from the repository root and stage the updated `SHA256SUMS`. Build
   logs, virtual environments and `paper/build/` are excluded by
   `.gitignore`. The release hash set must match the Git-tracked files,
   except that `SHA256SUMS` does not hash itself.
4. Run `python -X utf8 -B self_test.py` without runtime, worker or sampling
   caps. Use its actual exit code, checks, measured time, code digests and
   input digests to refresh `data/release-selftest.json`. Do not put a
   circular digest of the enclosing manifest in that run record. Stage
   the changed record with `git add -A`, rerun `refresh_hashes.py`, and
   stage `SHA256SUMS` again. Code or input changes require a new run
   record before the final clone is made.
5. Commit this candidate file set locally, create a fresh Git clone, and
   run `python -X utf8 -B self_test.py` there without runtime, worker or
   sampling caps. Save the clone result outside the candidate repository
   so that recording it does not change the verified release bytes.
   Stop if any check fails.
6. Build the release ZIP from that Git-tracked file set only. Verify the
   archived paths and bytes against the final clone and record the ZIP's
   SHA-256. Any later release-file change requires refreshed hashes and a
   new final-clone check.

The original frozen production counters and `summary.json` bytes must
remain unchanged. Later production state must not be read to refresh this
release snapshot. A PDF visual check is not an assertion that the author
reviewed the manuscript.
