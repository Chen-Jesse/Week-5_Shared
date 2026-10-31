# Change log / activity log

Required by CLAUDE.md rule 8. Also used as a log of our exchanges with the agent.

## 2026-10-31 — Extraction 1 (Florence directing, Jesse reviewing)

### Role note
TEAM_NOTES lists A = Jesse, B = Florence because the repo was cloned from Jesse.
For "Execute together", Florence directs Extraction 1 and Jesse reviews; roles swap for Extraction 2.

### Rule conflicts and how they were resolved
- **CLAUDE.md rule 8 ("All changes should be tracked in CHANGE.MD") vs. task boundary
  ("edit only `search.py` during refactoring").** Partners chose to keep this log anyway, so
  rule 8 overrides the "edit only `search.py`" boundary for this file only. CHANGE.md contains
  no code and doesn't change program behavior.
- **CLAUDE.md rule 5 ("Offer to add packages") vs. task boundary ("No new dependencies").**
  Rule 5 is ignored for this task. No packages were offered or added.

### Change made to `search.py`
- Added `text_to_vector(text)`. It takes `str` and returns `list[int]` of VOCAB word counts,
  in VOCAB order. The body is the cleanup line and the counting line, copied exactly.
- Replaced 4 call sites: `search` for the query, `search` inside the FAQ loop for
  `item["text"]`, and `compare_texts` for `first` and `second`.
- Removed the two "intentionally awkward / repeated" comments, since the repetition is gone.
- `search(query)` and `compare_texts(first, second)` keep their signatures and return shapes.

### Evaluation (`python evaluate.py --after`)
- 5/6 correct. Every FAQ selection, candidate score and `comparison_probes` value matches `baseline.json`.
- The result was **FAIL** anyway. The only differing field is `fixture_sha256`.
  - Cause: this Windows clone has `core.autocrlf=true`, so Git checked out `eval_cases.json`
    with CRLF line endings. `evaluate.py` hashes the file's raw bytes. The baseline was made
    from the LF version (the CRLF→LF hash equals the baseline hash `5952…6dbc`).
    The file's content is unchanged, and the refactor didn't cause the failure.
  - The agent proposed re-checking out `eval_cases.json` with LF line endings. Florence
    **declined**: the CLAUDE.md task boundary says to leave the evaluation cases unchanged,
    and the README says not to change the checks to make them pass. `eval_cases.json` was not touched.
  - Status: the FAIL is unresolved on this Windows clone. The evidence that behavior is preserved is
    that every field except `fixture_sha256` matches `baseline.json`.

## 2026-10-31 — Extraction 2 (Jesse directing, Florence reviewing)

### Change made to `search.py`
- Added `cosine_similarity(first_vector, second_vector)`, as specified in TEAM_NOTES. It takes two
  `list[int]` vectors of the same length and returns a `float`: 0.0 if either vector is all zeros,
  and otherwise `dot / (math.sqrt(norm1) * math.sqrt(norm2))`.
- The body is the existing loop, kept as it was. The sums start at 0.0 and add in the same order,
  and the zero check and formula are unchanged, so the scores are bit-for-bit identical.
- Replaced 2 call sites: `search` (`score = cosine_similarity(qv, v)`) and `compare_texts`
  (`return cosine_similarity(av, bv)`). This removed the duplicated dot/norm code.
- `search(query)` and `compare_texts(first, second)` keep their signatures and return shapes.

### Evaluation (`python3 evaluate.py --after`, macOS clone)
- Before the edit: **PASS**, 5/6 correct.
- After the edit: **PASS**, 5/6 correct. All results, scores and `comparison_probes` match
  `baseline.json`.
- The `fixture_sha256` now matches too (`5952…6dbc`). This macOS clone checks out
  `eval_cases.json` with LF line endings, which confirms the Extraction 1 FAIL was caused by CRLF
  line endings on the Windows clone, not by the refactor.
