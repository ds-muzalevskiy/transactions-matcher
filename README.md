# Transactions Matcher

This project provides a simple FastAPI for **matching users with transactions** using:
- **Fuzzy string matching** (via `fuzzywuzzy`)  
- **Semantic similarity** (via `sentence-transformers`)  

It’s designed to explore real-world cases where user names in transactions may have typos or inconsistencies, and descriptions need to be semantically matched.

---

## Project Structure

```
app/
 ├── core/               
 ├── data/               
 ├── models/             
 ├── routes/             
 ├── services/           
 └── main.py             
tests/
 ├── test_match_description.py
 └── test_match_transaction.py
Dockerfile
docker-compose.yml
requirements.txt
pytest.ini
README.md
```

---

## Running the Application

### 1. Local Environment

Creare virtual environment:

```bash
python3 -m venv venv
```

Activate virtual environment:

```bash
source venv/bin/activate
```

Upgrade `pip`:

```bash
pip install --upgrade pip
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
uvicorn app.main:app --reload
```

Run the tests:

```bash
pytest -v
```

Run the tests with coverage:

```bash
pytest --cov=app tests/
```

Now the API documentation is available at:  
[http://localhost:8000/docs](http://localhost:8000/docs)

---

### 2. Using `docker-compose`

Build the app:

```bash
docker-compose build
```

Run the tests:

```bash
docker-compose up tests
```

Run the service:

```bash
docker-compose up app
```

---

## API Endpoints

### 1. Match Users to Transaction

**`GET /transactions/match/{transaction_id}`**

- Input: transaction ID  
- Optional query params:
  - `top_k`: number of top results (default: 5)

Example:

```bash
curl "http://localhost:8000/transactions/match/RAZbbmLX?top_k=5"
```

Response:

```
{
  "users":[
    {"id":"BuCoIvL79A","match_metric":100.0},
    {"id":"IYkWtGZXLe","match_metric":46.0},
    {"id":"yDhnGNLelf","match_metric":44.0}
  ],

    "total_number_of_matches":3
}
```

If the match_metric will be low, there could be situation that the 
`total_number_of_matches` will be less than `top_k`.

---

### 2. Match Transactions by Description

**`POST /semantic/match_description`**

- Input: JSON `{ "query": "Transfer from Emma Brown" }`  
- Optional query param:
  - `top_k`: number of top matches to return (default: 5)

Example:

```bash
curl -X POST "http://localhost:8000/semantic/match_description?top_k=3" \
  -H "Content-Type: application/json" \
  -d '{"query": "James Bennett"}'
```

Response:

```
{
  "transactions": [
    {"id": "D5aW2I5o","embedding":[-0.06822924315929413, ...],"similarity": 0.5616059303283691},
    {"id": "Flmxgl6m","embedding":[0.0016708576586097479, ...],"similarity": 0.5085235834121704},
    {"id": "BWIigGOK","embedding":[-0.07320866733789444, ...],"similarity": 0.4854050278663635}
  ],
  "total_number_of_tokens_used": 4
}
```

---

## Limitations

- **Small-scale only**: Matching is done in memory; no vector database is used.  
- **Performance**: Embeddings are recomputed on every request (no caching).  
- **Model choice**: `paraphrase-mpnet-base-v2` is light and provide embeddings of decent quality but not specialized for names.  
- **Threshold tuning**: Fuzzy matching cutoff (`>40`) may miss near-matches.  
- **Locale issues**: Works only with Latin alphabet. For example, non-latin names may not match well.

---

## Possible Improvements

1. **Precompute & cache embeddings** at startup for faster queries.  
2. **Use FAISS or Qdrant** for scalable vector search (10k+ transactions).  
3. **Hybrid scoring**: Combine fuzzy string scores + semantic similarity.  
4. **Model tuning**: Fine-tune embeddings on transaction/user name pairs.  
5. **Better cleaning**: `clean_description()` could be improved to handle multilingual and special characters.  
6. **Production preparation**: Adding authentication, rate limiting, error monitoring. Setting up CI/CD pipeline for the project.

---

## Development Notes

- Project was tested on local machine (python 3.10), with docker (python 3.10) and on google colab (python 3.12).
- The project defaults to **PyTorch backend**; TensorFlow is not required.  
