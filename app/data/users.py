import csv
from pathlib import Path

USERS_FILE = Path(__file__).resolve().parent / "users.csv"

users = []
with open(USERS_FILE, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        users.append({
            "id": row["id"],
            "name": row["name"]
        })