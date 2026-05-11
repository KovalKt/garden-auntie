# 🌱 Garden Auntie

A RAG-powered gardening assistant that answers questions in Ukrainian,
grounded in a custom knowledge base of gardening guides, local planting
calendars, and Stardew Valley crop data.

Built as a learning project to explore LangChain, ChromaDB, and
retrieval-augmented generation.

---

## What it does

- Answers gardening questions in Ukrainian, using your own documents as
  the primary source
- Retrieves the most relevant chunks from a local vector database before
  generating any answer — so responses are grounded in real sources, not
  just model memory
- Shows which documents each answer was drawn from
- Remembers conversation history within a session for natural follow-up
  questions
- Works with PDFs and plain text files — drop new docs in and re-run
  the ingest script

---

## Tech stack

| Layer | Tool |
|---|---|
| LLM | GPT-4o-mini via OpenAI API |
| Embeddings | text-embedding-3-small |
| Vector store | ChromaDB (local) |
| RAG framework | LangChain |
| UI | Streamlit |

---

## Project structure

garden-auntie/
├── data/docs/          # your source documents (PDFs, txt)
├── src/
│   ├── ingest.py       # loads docs, creates embeddings, builds ChromaDB
│   ├── retriever.py    # RAG query logic + LLM call
│   └── app.py          # Streamlit UI
├── chroma_db/          # vector database (auto-generated, not committed)
├── .env                # API keys (not committed)
└── requirements.txt

---

## Setup

**1. Clone and install**
```bash
git clone https://github.com/KovalKt/garden-auntie
cd garden-auntie
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**2. Add your API key**

Create a `.env` file:
OPENAI_API_KEY=your_key_here

**3. Add documents**

Drop `.pdf` or `.txt` files into `data/docs/`. Then build the vector database:
```bash
python src/ingest.py
```

**4. Run the app**
```bash
streamlit run src/app.py
```

---

## How RAG works here

1. At ingest time, documents are split into ~800-character chunks,
   embedded into vectors, and stored in ChromaDB
2. At query time, the user's question is embedded with the same model
3. ChromaDB finds the 4 most semantically similar chunks
4. Those chunks + the question are sent to GPT-4o-mini with a Ukrainian
   system prompt
5. The answer is grounded in the retrieved text, not model memory alone

---

## Building your knowledge base

Add `.pdf` or `.txt` files to `data/docs/` before running `ingest.py`.

Suggested sources:
- Vegetable growing guides (RHS, GrowVeg, or similar)
- A planting calendar for your local climate zone
- Companion planting references

The app works best with 5–15 focused documents rather than a large
generic corpus. *Personal notes about your own garden* work especially
well — the model already knows general gardening, so local and specific
knowledge adds the most value.

---

## Possible extensions

- Add a seasonal filter (only retrieve docs relevant to current month)
- Support voice input in Ukrainian
- Add a web scraper to auto-update the knowledge base
- Deploy to Streamlit Cloud for public access
