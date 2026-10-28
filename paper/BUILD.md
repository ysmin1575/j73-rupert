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
responsibility sentence are filled in. The software version DOI is
https://doi.org/10.5281/zenodo.23724948 (v0.1.0), the concept DOI is
https://doi.org/10.5281/zenodo.23724947, and the preprint DOI is
https://doi.org/10.5281/zenodo.23725007 (reserved, unpublished).

After any intentional source or PDF edit:

1. Rebuild the PDF with Tectonic and inspect an image of every page for
   clipping, overlap, missing glyphs, readable equations and tables, and
   the final DOI links.
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

## 저자의 다음 작업

DOI를 반영한 파일을 기존 저장소의 main에 새 commit으로 올립니다.
기존 v0.1.0 태그와 Zenodo 소프트웨어 기록 23724948은 그대로 유지합니다.
소프트웨어 아카이브의 PDF에는 DOI 자리표시자가 있고, 별도 프리프린트
PDF에는 DOI가 들어 있습니다. 두 PDF는 서로 다른 파일입니다.

최종 paper.pdf를 기존 Zenodo 논문 초안 23725007에 업로드합니다.
업로드한 파일을 내려받아 로컬 최종본과 bytes 및 SHA-256이 같은지
확인한 다음 Publish로 발행합니다. 초안을 새로 만들거나 예약 DOI를 바꾸지 않습니다.
