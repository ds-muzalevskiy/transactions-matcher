from typing import List
from pydantic import BaseModel

class MatchDescriptionRequest(BaseModel):
    query: str

class UserMatch(BaseModel):
    id: str
    match_metric: float

class TransactionMatch(BaseModel):
    id: str
    embedding: List[float]
    similarity: float

class TransactionMatchResponse(BaseModel):
    transactions: List[TransactionMatch]
    total_number_of_tokens_used: int

class UserMatchResponse(BaseModel):
    users: List[UserMatch]
    total_number_of_matches: int
