# Endee Semantic Search

A semantic search engine over a small technical knowledge base (ML, Data, Backend, GenAI), using **[Endee](https://github.com/endee-io/endee)** as the vector database. Built as an Endee internship project, forked from the official repository.

## Problem Statement

Keyword search fails when users phrase a question differently from the stored text. Searching "how do models avoid memorizing training data" should find the *Overfitting* article even though they share no keywords. This project solves that with embeddings and vector similarity search.

## System Design

```
docs.json ──► SentenceTransformer (all-MiniLM-L6-v2, 384-d) ──► Endee collection (HNSW, cosine, int8)
                                                                        ▲
user query ──► same embedding model ──► Endee search (+ category filter) ┘──► ranked results (CLI / Streamlit)
```

1. **Ingest** (`src/ingest.py`): each document is embedded and upserted with its full record as `meta` and its category as a `filter` tag.
2. **Search** (`src/store.py`): the query is embedded with the same model and sent to Endee, which returns the nearest documents with similarity scores.
3. **Interfaces**: a CLI (`src/cli.py`) and a Streamlit app (`app.py`).

## How Endee Is Used

| Endee feature | Usage |
|---|---|
| `create_collection` | One dense `vector` field: 384 dimensions, `cosine` space, `int8` precision for low memory |
| `upsert` | Stores id, embedding, `meta` (title/text/category) and a `filter` tag per document |
| `search` | Approximate nearest-neighbour (HNSW) search on the embedding field |
| Filters | `[{"category": {"$eq": "ML"}}]` restricts results to one category at query time |

## Setup

**Prerequisites:** Python 3.10+ and an Endee instance: either [Endee Cloud](https://endee.io) (free to start) or a self-hosted Enterprise instance ([30-day evaluation](https://docs.endee.io/v2/quick-start/enterprise)).

```bash
git clone https://github.com/<your-username>/endee.git
cd endee
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                                  # then add your ENDEE_TOKEN (and ENDEE_BASE_URL if self-hosted)
```

## Run

```bash
python -m src.ingest                                   # embed and upload the documents
python -m src.cli "how do models avoid memorizing training data"
python -m src.cli "speed up database reads" --category Backend -k 3
streamlit run app.py                                   # web UI
```

Example: the query *"how do models avoid memorizing training data"* returns **Overfitting** as the top hit.

## Project Structure

```
app.py            Streamlit UI
src/store.py      Endee client, embeddings, search
src/ingest.py     Data ingestion
src/cli.py        Command-line search
data/docs.json    Sample knowledge base (22 documents)
```

## Possible Extensions

Hybrid search with an Endee sparse field, RAG answers by passing retrieved text to an LLM, and loading your own documents with chunking.
