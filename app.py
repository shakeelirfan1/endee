import streamlit as st
from src.store import search

st.set_page_config(page_title="Endee Semantic Search", page_icon="🔎")
st.title("🔎 Semantic Search powered by Endee")
q = st.text_input("Ask anything about ML, data, or backend engineering")
cat = st.selectbox("Category filter", ["All", "ML", "Data", "Backend", "GenAI"])
k = st.slider("Results", 1, 10, 5)
if q:
    for h in search(q, k, None if cat == "All" else cat):
        m = h["meta"]
        st.markdown(f"**{m['title']}** · `{m['category']}` · score {h['similarity']:.3f}")
        st.write(m["text"])
