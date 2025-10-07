from fastapi import FastAPI
from app.api.routes import match_transaction, match_description

app = FastAPI(title="Transaction Matcher API")

app.include_router(match_transaction.router, prefix="/transactions")
app.include_router(match_description.router, prefix="/semantic")
