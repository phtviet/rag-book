import chromadb
from llama_index.core import VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.anthropic import Anthropic
from llama_index.postprocessor.sbert_rerank import SentenceTransformerRerank
from dotenv import load_dotenv

load_dotenv()


def load_query_engine():
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    Settings.llm = Anthropic(model="claude-sonnet-4-5", max_tokens=1024)

    db = chromadb.PersistentClient(path="./chroma_db")
    chroma_collection = db.get_or_create_collection("ai_engineering")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    index = VectorStoreIndex.from_vector_store(vector_store)

    # The reranker: re-scores candidates with a cross-encoder, keeps the best top_n.
    reranker = SentenceTransformerRerank(
        model="BAAI/bge-reranker-base",
        top_n=3,   # final number of chunks passed to the LLM
    )

    # Retrieve a WIDER pool (20), then rerank down to 3.
    # similarity_top_k=20 = initial candidate pool; node_postprocessors reranks it.
    query_engine = index.as_query_engine(
        similarity_top_k=20,
        node_postprocessors=[reranker],
    )
    return query_engine


if __name__ == "__main__":
    engine = load_query_engine()
    # Quick manual check on the problem question before running full eval
    response = engine.query("How do the chapters on evaluation and inference optimization relate?")
    print(response)
    print("\n--- Retrieved (after rerank) ---")
    for node in response.source_nodes:
        page = node.metadata.get("page", "?")
        score = node.score
        print(f"  page {page} (rerank score {score:.3f})")