import sys
import chromadb
from llama_index.core import VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from dotenv import load_dotenv

from query_rerank import load_query_engine

load_dotenv()


def inspect(question: str):
    """Show the final answer + the chunks actually used (post-reranking if engine reranks)."""
    engine = load_query_engine()
    response = engine.query(question)

    print(f"\nQUESTION: {question}\n")
    print(f"ANSWER:\n{response}\n")
    print("=" * 70)
    print(f"RETRIEVED {len(response.source_nodes)} CHUNKS (FULL TEXT):")
    print("=" * 70)

    for i, node in enumerate(response.source_nodes, 1):
        page = node.metadata.get("page", "?")
        score = node.score
        print(f"\n--- Chunk {i}: page {page}, score {score:.3f} ---")
        print(node.text)   # FULL text, not truncated
        print("-" * 50)


def inspect_pool(question: str, pool_size: int = 20):
    """Show the RAW bi-encoder candidate pool BEFORE any reranking.

    Uses a retriever (not a query engine), so no LLM call and no reranking —
    just the vector-search candidates, ranked by bi-encoder similarity.
    """
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

    db = chromadb.PersistentClient(path="./chroma_db")
    chroma_collection = db.get_or_create_collection("ai_engineering")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    index = VectorStoreIndex.from_vector_store(vector_store)

    retriever = index.as_retriever(similarity_top_k=pool_size)
    nodes = retriever.retrieve(question)

    print(f"\nQUESTION: {question}\n")
    print(f"BI-ENCODER CANDIDATE POOL (top {pool_size}, BEFORE reranking):\n")
    for rank, node in enumerate(nodes, 1):
        page = node.metadata.get("page", "?")
        score = node.score
        preview = node.text[:100].replace("\n", " ")
        text_lower = node.text.lower()
        marker = "  <-- has 'distillation'/'student'" if ("distillation" in text_lower or "student" in text_lower) else ""
        print(f"  rank {rank:2d}: page {page} (score {score:.3f}){marker}")
        print(f"           {preview}...")


if __name__ == "__main__":
    # Usage:
    #   python inspect_retrieval.py "your question"          -> final answer + used chunks
    #   python inspect_retrieval.py --pool "your question"   -> raw bi-encoder candidate pool
    args = sys.argv[1:]

    if args and args[0] == "--pool":
        question = " ".join(args[1:]) if len(args) > 1 else "What's the difference between quantization and distillation?"
        inspect_pool(question)
    else:
        question = " ".join(args) if args else "What percentage smaller is DistilBERT than BERT?"
        inspect(question)