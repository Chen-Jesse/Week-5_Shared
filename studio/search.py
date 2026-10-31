"""Working but repetitive FAQ search. Refactor this file only.
The vectors are word counts, NOT learned semantic embeddings.
"""
import math

FAQS = [
    {"id": "password", "text": "Reset your password using the account portal."},
    {"id": "expenses", "text": "Submit travel expenses with a receipt."},
    {"id": "leave", "text": "Request vacation leave through your manager."},
]
VOCAB = ["password", "account", "travel", "expenses", "receipt", "vacation", "leave", "manager"]


def text_to_vector(text):
    t = text.strip().lower().replace("?", "").replace(".", "")
    return [t.split().count(word) for word in VOCAB]


def cosine_similarity(first_vector, second_vector):
    dot = 0.0
    norm1 = 0.0
    norm2 = 0.0
    for i in range(len(first_vector)):
        dot += first_vector[i] * second_vector[i]
        norm1 += first_vector[i] ** 2
        norm2 += second_vector[i] ** 2
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (math.sqrt(norm1) * math.sqrt(norm2))


def search(query):
    qv = text_to_vector(query)
    results = []
    for item in FAQS:
        v = text_to_vector(item["text"])
        score = cosine_similarity(qv, v)
        results.append({"id": item["id"], "score": score})
    best = results[0]
    for row in results:
        if row["score"] > best["score"]:
            best = row
    return {"id": best["id"], "score": best["score"], "scores": results}


def compare_texts(first, second):
    av = text_to_vector(first)
    bv = text_to_vector(second)
    return cosine_similarity(av, bv)


if __name__ == "__main__":
    result = search("How do I reset my password?")
    for row in result["scores"]:
        print(row["id"], round(row["score"], 4))
    print("Selected FAQ:", result["id"])
