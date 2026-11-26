"""Embed data/docs.json and upsert it into Endee."""
import json
from pathlib import Path
from src.store import FIELD, embed, get_collection

docs = json.loads((Path(__file__).parent.parent / "data" / "docs.json").read_text())
col = get_collection(create=True)
vecs = embed([f"{d['title']}. {d['text']}" for d in docs])
col.upsert([
    {"id": d["id"], "meta": d, "filter": {"category": d["category"]}, "fields": {FIELD: v}}
    for d, v in zip(docs, vecs)
])
print(f"Upserted {len(docs)} documents into Endee.")
