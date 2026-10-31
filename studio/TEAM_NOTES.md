# Team notes — short phrases are enough

Partners: A = Jesse; B = Florence

- Jesse's proposed functions (names, inputs → outputs):
    
    Extraction 1: text_to_vector(text)
    Input: text (str), meaning a query or FAQ text
    Returns: list[int], the count of each VOCAB word in the       cleaned text, in VOCAB order
    Body: the cleanup line followed by the counting line, copied exactly
    Called from (4 places):
    search: qv = text_to_vector(query), once, before the loop as it is now
    search loop: v = text_to_vector(item["text"])
    compare_texts: av = text_to_vector(first) and bv = text_to_vector(second)
    Removes: 8 repeated lines
   
    Extraction 2: cosine_similarity(first_vector, second_vector)
    Input: two list[int] vectors of the same length
    Returns: float. It returns 0.0 if either vector is all zeros, and otherwise dot / (sqrt(norm1) * sqrt(norm2))
    Body: the current loop, kept exactly. The sums start at 0.0 and add in the same order, and the formula keeps math.sqrt(a) * math.sqrt(b), so the scores come out bit-for-bit identical.
    Called from (2 places):
    search loop: score = cosine_similarity(qv, v)
    compare_texts: return cosine_similarity(av, bv)
    Removes: about 20 duplicated lines across the two functions

- Florence's proposed functions (names, inputs → outputs):
Proposed extractions
1. _normalize(text)
Input: text (str)
Returns: str. Stripped, lowercased, with ? and . removed. Same steps as now.
Called from: _vectorize only. That covers what are now 4 copies of the cleaning line: lines 16, 20, 43 and 44.
2. _vectorize(text)
Input: text (str), not yet normalized
Returns: list[int] of length len(VOCAB). Entry i is how many times VOCAB[i] appears in the normalized tokens.
Body: tokens = _normalize(text).split(), then [tokens.count(word) for word in VOCAB]. Splitting once instead of once per vocab word gives the same counts.
Called from:
search: once for the query (line 17) and once per FAQ inside the loop (line 21)
compare_texts: once for each argument (lines 45–46)
3. _cosine(a, b)
Inputs: a, b (equal-length lists of numbers)
Returns: float. 0.0 if either norm is zero, otherwise dot / (math.sqrt(na) * math.sqrt(nb)).
Called from:
search: inside the FAQ loop, replacing lines 22–32
compare_texts: replacing lines 47–56
Keeping scores identical: I'll keep the exact formula, the 0.0 starting values and the two separate math.sqrt calls, so the scores match baseline.json exactly. I won't switch to math.hypot, sqrt(na * nb) or any other form that could round differently.
 

- Our agreed plan (at most two function extractions) and why:

Extraction 1: text_to_vector(text) Input: text (str), meaning a query or FAQ text Returns: list[int], the count of each VOCAB word in the cleaned text, in VOCAB order Body: the cleanup line followed by the counting line, copied exactly Called from (4 places): search: qv = text_to_vector(query), once, before the loop as it is now search loop: v = text_to_vector(item["text"]) compare_texts: av = text_to_vector(first) and bv = text_to_vector(second) Removes: 8 repeated lines

Extraction 2: cosine_similarity(first_vector, second_vector) Input: two list[int] vectors of the same length Returns: float. It returns 0.0 if either vector is all zeros, and otherwise dot / (sqrt(norm1) * sqrt(norm2)) Body: the current loop, kept exactly. The sums start at 0.0 and add in the same order, and the formula keeps math.sqrt(a) * math.sqrt(b), so the scores come out bit-for-bit identical. Called from (2 places): search loop: score = cosine_similarity(qv, v) compare_texts: return cosine_similarity(av, bv) Removes: about 20 duplicated lines across the two functions

- Before: 5 / 6. After: 5 / 6. Behavior check: PASS
