from fuzzywuzzy import process
from fastapi import APIRouter, HTTPException, Query
from app.models.schemas import UserMatchResponse, UserMatch
from app.services.utils import extract_name
from app.services.matcher import fuzzy_match_users
from app.data.users import users
from app.data.transactions import transactions

router = APIRouter()

def find_transaction_by_id(transaction_id: str, threshold: int = 40):
    tx = next((t for t in transactions if t["id"] == transaction_id), None)
    if tx:
        return tx

    choices = {t["id"]: t for t in transactions}
    best_match, score = process.extractOne(transaction_id, choices.keys())
    if score > threshold:
        return choices[best_match]
    return None

@router.get("/match/{transaction_id}", response_model=UserMatchResponse)
def match_transaction(transaction_id: str, top_k: int = Query(default=5, ge=1, description="How many top results to return")):
    transaction = find_transaction_by_id(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    payer_name = extract_name(transaction["description"])
    if not payer_name:
        raise HTTPException(status_code=400, detail="Could not extract name")

    matches = fuzzy_match_users(payer_name, users)

    return UserMatchResponse(
        users=[UserMatch(**m) for m in matches[:top_k]],
        total_number_of_matches=len(matches)
    )