# RAG over AI Engineering book

A retrieval-augmented generation system built over Chip Huyen's *AI Engineering: Building Applications with Foundation Models*.

This is project 1 of 3 in a focused sprint to build AI engineering skills. The goal is to deeply understand RAG systems by building one end-to-end, evaluating it rigorously, and documenting what worked and what didn't. See `eval_notes.md` for the full experiment log and results.

## Setup

This project expects a PDF of Chip Huyen's *AI Engineering: Building Applications with Foundation Models* placed in the project root as `ai_engineering.pdf`. The PDF is not included in this repository for copyright reasons.

```powershell
# Create environment and install dependencies
uv venv
.\.venv\Scripts\Activate.ps1
uv pip install -r requirements.txt

# Set your Anthropic API key
# Create a .env file with: ANTHROPIC_API_KEY=sk-ant-your-key-here

# Build the index (chunk + embed the book), then query it
python index_book.py
python ask.py
```

## Approach: evaluation-driven development

Every change is measured against a fixed set of 20 hand-written Q&A pairs with verified reference answers (`eval_set.py`). Manual scoring is the source of truth. Each experiment changes one variable, is scored against the same eval set, and is recorded with its result — including regressions. The eval results table is the project's central artifact.

## Results so far

| Experiment | Change | Correct / 20 |
|-----------|--------|--------------|
| Baseline | vector search, top_k=3 | 17 |
| Corpus cleaning | remove back-of-book index | 16 (regression — see notes) |
| Reranking | bi-encoder top_k=20 → cross-encoder → top_3 | 19 |
| Chunking | tested 256 / 512 / 1024 | 19 (best; chunk size is a tradeoff) |

Selected findings (full detail in `eval_notes.md`):
- Cleaning the corpus caused a regression — a junk index chunk was accidentally "load-bearing" for one synthesis question. Aggregate scores can hide per-question regressions.
- Reranking (cross-encoder) gave the biggest gain, but demotes terse fact/formula chunks in favour of prose — hurting a couple of precision questions.
- Chunk size is a tradeoff, not a strict improvement: larger chunks help comparison/synthesis questions, smaller help precision retrieval.

## Status

- [x] Project setup and hello-world LLM call
- [x] PDF ingestion and text extraction
- [x] Vector index with chunking
- [x] End-to-end query pipeline
- [x] Evaluation harness with 20 hand-written Q&A pairs
- [x] Corpus cleaning experiment
- [x] Reranking (cross-encoder)
- [x] Chunking experiments (256 / 512 / 1024)
- [ ] LLM-as-judge (automated scoring)
- [ ] Prompt tuning
- [ ] Streamlit UI
- [ ] Final writeup with eval results

## Stack

Python, LlamaIndex, ChromaDB, Anthropic Claude API, BAAI/bge embeddings + reranker.
