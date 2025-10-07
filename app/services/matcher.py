from typing import List
from fuzzywuzzy import fuzz
from sklearn.metrics.pairwise import cosine_similarity
from app.core.model_loader import model
from app.data.transactions import transactions
from app.services.utils import clean_description

def fuzzy_match_users(payer_name: str, users: List[dict], threshold: int = 40) -> List[dict]:
    matches = []
    for user in users:
        score = fuzz.token_sort_ratio(payer_name.lower(), user["name"].lower())
        if score>threshold:
            matches.append({"id": user["id"], "match_metric": score})
    matches.sort(key=lambda x: x["match_metric"], reverse=True)
    return matches

def semantic_match_transactions(query: str) -> list[dict]:
    query_name = clean_description(query)
    query_embedding = model.encode(query_name)

    results = []
    for tx in transactions:
        tx_clean = clean_description(tx["description"])
        tx_embedding = model.encode(tx_clean)
        similarity = cosine_similarity([query_embedding], [tx_embedding])[0][0]
        results.append({
            "id": tx["id"],
            "embedding": tx_embedding.tolist(),
            "similarity": float(similarity)
        })

    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results