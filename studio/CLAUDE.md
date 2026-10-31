1. Read the relevant code before proposing changes.
2. Propose a plan and wait for our agreement before editing.
3. Prompt me for permission if refactoring will change existing behavior.
4. Run the supplied evaluation before and after changes.
5. Offer to add packages that might make the code better, explain your reasoning. 
6. If an evaluation fails, summarize the error and propose possible fixes.
7. Code you write or change in `search.py` should follow PEP 8; don't reformat untouched code or add formatting tools.
8. All changes should be tracked in CHANGE.MD

**The task boundaries below must apply regardless of your selections**:
edit only `search.py` during refactoring; keep the public `search(query)` and
`compare_texts(first, second)` interfaces and return shapes; leave the FAQ data, vocabulary, evaluator, evaluation cases, and saved baseline unchanged.
No new dependencies, live model calls, or feature additions.