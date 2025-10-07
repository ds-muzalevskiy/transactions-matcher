from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer

MODEL_NAME = "sentence-transformers/paraphrase-mpnet-base-v2"
model = SentenceTransformer(MODEL_NAME)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)