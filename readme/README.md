Students: Florence Atienza & Jesse Chen
We observed an odd issue in which Jesse's system returns eval as PASS while Florence's returns as FAIL. After troubleshooting, we were found the following explanation:

    "PASS / FAIL" compares everything in the new report against baseline.json (evaluate.py:67). That includes one field that has nothing to do with search.py: fixture_sha256, a fingerprint (SHA-256 hash) of the raw bytes of eval_cases.json (evaluate.py:32). Its job is to show that the test questions weren't edited.

    The mismatch happens like this:
    Text files end each line with an invisible marker. Mac and Linux use one character (\n, called LF). Windows traditionally uses two (\r\n, called CRLF).
    
    The repo stores eval_cases.json with LF. Jesse made the baseline on a Mac, so his fingerprint was computed from the LF bytes.
    
    Your Git is set to core.autocrlf=true, so when you cloned, it converted the file to CRLF on your disk.
    The visible content is the same, but the bytes differ, so the fingerprint differs. The evaluator reads that as "the test questions changed" and reports FAIL.
    
    The evidence:
    Every other field matches the baseline exactly on your machine: all selections, all 18 scores and the 3 compare_texts results.
    When I converted your file's line endings to LF and hashed it, I got the baseline fingerprint exactly (5952…6dbc).
    Jesse's Mac clone runs the same main code and gets PASS.

Additionally, our change log can be found here: [CHANGE.md](../studio/CHANGE.md)