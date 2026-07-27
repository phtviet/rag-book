# RAG over AI Engineering book

A retrieval-augmented generation system built over Chip Huyen's *AI Engineering: Building Applications with Foundation Models*.

This is project 1 of 3 in a focused sprint to build AI engineering skills. The goal is to deeply understand RAG systems by building one end-to-end, evaluating it rigorously, and documenting what worked and what didn't.

**Writeup:** [What building a RAG system taught me about evaluation](WRITEUP.md) — the story of the project and its main findings. Full experiment log in `eval_notes.md`.

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

# Or launch the web app
streamlit run app.py --server.fileWatcherType none
```

## Approach: evaluation-driven development

Every change is measured against a fixed set of 20 hand-written Q&A pairs with verified reference answers (`eval_set.py`). Each experiment changes one variable, is scored against the same eval set, and is recorded with its result — including regressions. The eval results table is the project's central artifact.

Scoring evolved over the project: manual human scoring first (the source of truth), then an **LLM-as-judge** (`judge.py`) validated against those human scores and adopted at `temperature=0` for reproducibility.

## Current system

Retrieval: bi-encoder retrieves a pool of 20 candidates (`BAAI/bge-small-en-v1.5`), a cross-encoder reranker (`BAAI/bge-reranker-base`) re-scores them and keeps the top 3. Chunking: 1024 tokens / 100 overlap. Generation: Claude with a faithfulness prompt that answers only from retrieved context and declines when the context is insufficient.

## Web app

`app.py` is a Streamlit interface over the same query engine: a question box (with example questions), the generated answer, and expandable source chunks showing which book pages the answer drew from and their cross-encoder relevance scores. Out-of-corpus questions render distinctly, showing the system decline rather than answer from outside knowledge.

## Results

| Experiment | Change | Correct / 20 |
|-----------|--------|--------------|
| Baseline | vector search, top_k=3 | 17 |
| Corpus cleaning | remove back-of-book index | 16 (regression — see notes) |
| Reranking | bi-encoder top_k=20 → cross-encoder → top_3 | 19 |
| Chunking | tested 256 / 512 / 1024 | best at 512–1024 |
| Re-scored (post-judge) | stricter semantic grading | 17 |
| Faithfulness prompt | answer only from context, decline if absent | 17 (grounded, no leakage) |

Scores are on a deliberately hard 20-question eval with verified reference answers; the remaining misses are retrieval-recall gaps and one reranker limitation, documented in `eval_notes.md`.

Selected findings (full detail in `eval_notes.md`):
- **Cleaning the corpus caused a regression** — a junk index chunk was accidentally "load-bearing" for one synthesis question. Aggregate scores can hide per-question regressions.
- **Reranking gave the biggest gain**, but the cross-encoder demotes terse fact/formula chunks in favour of prose — hurting a couple of precision questions (two independent cases).
- **Chunk size is a tradeoff, not a strict improvement**: larger chunks help comparison/synthesis questions, smaller help precision retrieval.
- **LLM-as-judge**: validated against human scores (caught real gaps human scoring missed), but exhibited hallucination (bleeding the reference answer into its assessment) and non-determinism at default temperature. Fixed reproducibility with `temperature=0`; adopted as a scorer plus a flag for human review, not a blind replacement.
- **Faithfulness prompting**: a naive "answer only from context" prompt made answers grounded but too terse (it under-used retrieved detail). Rebalancing the prompt to be thorough *with grounded content* recovered completeness without reintroducing outside-knowledge leakage — faithfulness and completeness are not in hard conflict.

## Status

- [x] Project setup and hello-world LLM call
- [x] PDF ingestion and text extraction
- [x] Vector index with chunking
- [x] End-to-end query pipeline
- [x] Evaluation harness with 20 hand-written Q&A pairs
- [x] Corpus cleaning experiment
- [x] Reranking (cross-encoder)
- [x] Chunking experiments (256 / 512 / 1024)
- [x] LLM-as-judge (automated semantic scoring)
- [x] Prompt tuning (faithfulness + declining)
- [x] Streamlit UI
- [x] Final writeup with eval results ([WRITEUP.md](WRITEUP.md))

## Stack

Python, LlamaIndex, ChromaDB, Anthropic Claude API, BAAI/bge embeddings + reranker.
