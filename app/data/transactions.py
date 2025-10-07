import csv
from pathlib import Path

TRANSACTIONS_FILE = Path(__file__).resolve().parent / "transactions.csv"

transactions = []
with open(TRANSACTIONS_FILE, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        transactions.append({
            "id": row["id"],
            "amount": float(row.get("amount ($)", 0)), 
            "description": row["description"]
        })