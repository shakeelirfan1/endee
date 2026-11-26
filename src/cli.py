"""Usage: python -m src.cli "how do models avoid overfitting" [--category ML] [-k 5]"""
import argparse
from src.store import search

p = argparse.ArgumentParser()
p.add_argument("query")
p.add_argument("--category")
p.add_argument("-k", type=int, default=5)
a = p.parse_args()
for i, h in enumerate(search(a.query, a.k, a.category), 1):
    m = h["meta"]
    print(f"{i}. [{m['category']}] {m['title']}  (score {h['similarity']:.3f})\n   {m['text']}\n")
