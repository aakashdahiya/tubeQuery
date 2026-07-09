# TubeQuery

A retrieval-augmented generation (RAG) web application that answers questions about YouTube videos with timestamp-cited responses grounded in the video's transcript.

## What it does

Paste a YouTube URL, ask a question, get an answer with clickable timestamp citations. If the answer isn't in the video, TubeQuery says so honestly instead of hallucinating.

[![TubeQuery demo]
](https://www.youtube.com/watch?v=BX6XgWdOXwE)


## Features

- Transcript-based Q&A with source citations (timestamps)
- Sentence-boundary chunking that preserves timestamps through the pipeline
- Local caching of embedded chunks (subsequent queries on the same video are ~30x faster)
- Prompt-injection resistance via system prompt design
- Honest refusal when the answer isn't in the source

## Tech stack

- **Backend:** FastAPI, Python 3.13
- **Embeddings:** sentence-transformers (all-MiniLM-L6-v2)
- **Vector search:** cosine similarity (numpy)
- **Generation:** Anthropic Claude Haiku 4.5
- **Frontend:** Vanilla HTML, CSS, JavaScript (no framework)
- **Storage:** JSON file cache

## Architecture

YouTube URL → Transcript fetch → Chunking (with timestamps) → Embedding →
Vector cache → Question embedding → Cosine retrieval (top-k) →
Claude generation with grounded prompt → Timestamp-cited answer

## Running locally

**Requirements:** Python 3.11+, an Anthropic API key

```bash
git clone https://github.com/aakashdahiya/tubeQuery.git
cd tubeQuery/tubequery
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file with your Anthropic API key:

## Running locally

**Requirements:** Python 3.11+, an Anthropic API key

```bash
git clone https://github.com/aakashdahiya/tubeQuery.git
cd tubeQuery/tubequery
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file with your Anthropic API key:

Start the backend:

```bash
python -m uvicorn api:app --reload
```

Open `index.html` in your browser.

## Design decisions

**Snippet-boundary chunking.** Instead of cutting text at exactly N characters, chunks respect YouTube's natural transcript segments. This avoids mid-sentence breaks that degrade embedding quality.

**Local caching.** Each video's embedded chunks are saved to disk after first fetch. Subsequent queries skip the expensive fetch/chunk/embed pipeline. Reduced per-query time from ~25s to ~2s.

**Grounded generation.** System prompt explicitly instructs Claude to use only the retrieved excerpts and to refuse when the answer isn't present. Prevents hallucination and preserves verifiability.

## What I learned building this

- Chunking is more consequential than the embedding model itself
- Retrieval quality varies enormously by content type (natural speech > technical content with symbols)
- Serialization gotchas: numpy dtype changes when going through JSON (float32 → float64) — cost me an hour of debugging

## Roadmap

- [ ] Deploy publicly
- [ ] Multi-video synthesis (research-tool mode)
- [ ] pgvector for scalable retrieval
- [ ] Notes/summary generation

## License

MIT
