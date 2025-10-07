from fastapi import APIRouter, HTTPException, Query
from app.models.schemas import MatchDescriptionRequest, TransactionMatchResponse, TransactionMatch
from app.services.matcher import semantic_match_transactions
from app.core.model_loader import tokenizer

router = APIRouter()

@router.post("/match_description", response_model=TransactionMatchResponse)
def match_description(
    request: MatchDescriptionRequest,
    top_k: int = Query(default=5, ge=1, description="How many top results to return")
):
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    tokens = tokenizer.encode(query, add_special_tokens=True)
    matches = semantic_match_transactions(query)

    return TransactionMatchResponse(
        transactions=[TransactionMatch(**m) for m in matches[:top_k]],
        total_number_of_tokens_used=len(tokens)
    )