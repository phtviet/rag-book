# RAG over AI Engineering book

A retrieval-augmented generation system built over Chip Huyen's *AI Engineering: Building Applications with Foundation Models*.

This is project 1 of 3 in a focused sprint to build AI engineering skills. The goal is to deeply understand RAG systems by building one end-to-end, evaluating it rigorously, and documenting what worked and what didn't.

## Setup

This project expects a PDF of Chip Huyen's *AI Engineering: Building Applications with Foundation Models* placed in the project root as `ai_engineering.pdf`. The PDF is not included in this repository for copyright reasons.

```powershell
# Create environment and install dependencies
uv venv
.\.venv\Scripts\Activate.ps1
uv pip install -r requirements.txt

# Set your Anthropic API key
# Create a .env file with: ANTHROPIC_API_KEY=sk-ant-your-key-here

# Run extraction
python extract.py
```

## Status

- [x] Project setup and hello-world LLM call
- [x] PDF ingestion and text extraction
- [ ] Vector index with default chunking
- [ ] End-to-end query pipeline
- [ ] Evaluation harness with 20 hand-written Q&A pairs
- [ ] Chunking experiments
- [ ] Hybrid search (vector + BM25)
- [ ] Reranking
- [ ] Prompt tuning
- [ ] Streamlit UI
- [ ] Final writeup with eval results

## Stack

Python, LlamaIndex, ChromaDB, Anthropic Claude API.