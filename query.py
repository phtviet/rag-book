import chromadb
from llama_index.core import VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.anthropic import Anthropic
from dotenv import load_dotenv

# Load ANTHROPIC_API_KEY from .env into the environment
load_dotenv()


def load_query_engine():
    # 1. Configure the SAME embedding model used at index time.
    #    The query must be embedded into the same vector space as the chunks.
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

    # 2. Configure the LLM that will write answers from retrieved context.
    #    We must set max_tokens explicitly for Anthropic models.
    Settings.llm = Anthropic(model="claude-sonnet-4-5", max_tokens=1024)

    # 3. Connect to the EXISTING persisted ChromaDB collection (no re-indexing).
    db = chromadb.PersistentClient(path="./chroma_db")
    chroma_collection = db.get_or_create_collection("ai_engineering")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    # 4. Rebuild the index object from the existing vector store.
    #    This does NOT re-embed; it just wraps the stored vectors so we can query them.
    index = VectorStoreIndex.from_vector_store(vector_store)

    # 5. Turn the index into a query engine.
    #    similarity_top_k = how many chunks to retrieve and feed to the LLM.
    query_engine = index.as_query_engine(similarity_top_k=3)
    return query_engine


if __name__ == "__main__":
    print("Loading query engine...")
    query_engine = load_query_engine()

    # Three hand-written test questions about the book's content.
    questions = [
        "What is model distillation?",
        "What are the main techniques for inference optimization?",
        "Why does the author think evaluation is important for AI engineering?",
    ]

    for question in questions:
        print("\n" + "=" * 70)
        print(f"Q: {question}")
        print("=" * 70)

        response = query_engine.query(question)

        print(f"\nA: {response}\n")

        # Inspect WHAT was retrieved — so this isn't a black box.
        print("--- Retrieved from these pages: ---")
        for node in response.source_nodes:
            page = node.metadata.get("page", "?")
            score = node.score
            preview = node.text[:120].replace("\n", " ")
            print(f"  page {page} (score {score:.3f}): {preview}...")