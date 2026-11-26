"""Thin wrapper around the Endee Python client + embedding model."""
import os
from dotenv import load_dotenv
from endee import Endee
from sentence_transformers import SentenceTransformer

load_dotenv()
COLLECTION, FIELD, DIM = "tech_knowledge_base", "embedding", 384
_model = None


def model():
    global _model
    _model = _model or SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def embed(texts):
    return model().encode(texts, normalize_embeddings=True).tolist()


def client():
    c = Endee(os.getenv("ENDEE_TOKEN") or None)
    if os.getenv("ENDEE_BASE_URL"):
        c.set_base_url(os.environ["ENDEE_BASE_URL"])
    return c


def get_collection(c=None, create=False):
    c = c or client()
    names = [x["name"] if isinstance(x, dict) else x for x in c.list_collections()]
    if COLLECTION not in names:
        if not create:
            raise RuntimeError("Collection missing - run `python -m src.ingest` first.")
        c.create_collection(COLLECTION, fields=[{
            "name": FIELD, "type": "vector",
            "params": {"dimension": DIM, "space_type": "cosine", "precision": "int8"},
        }])
    return c.get_collection(COLLECTION)


def search(query, top_k=5, category=None):
    col = get_collection()
    flt = [{"category": {"$eq": category}}] if category else None
    res = col.search(fields={FIELD: {"query": embed([query])[0], "limit": top_k}}, filter=flt)
    return res["results"][FIELD]
