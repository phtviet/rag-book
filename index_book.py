import chromadb
from llama_index.core import VectorStoreIndex, StorageContext, Document, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

from extract import extract_book

INDEX_PAGES = set(range(521, 534))  # 521..533 inclusive = back-of-book index

def build_index():
    # 1. Extract the book text (reusing session 2's function)
    print("Extracting book text...")
    pages = extract_book("ai_engineering.pdf", skip_front_pages=20, skip_back_pages=1, exclude_pages=INDEX_PAGES)
    print(f"  {len(pages)} pages extracted (index pages 521-533 excluded).")

    # 2. Convert pages into LlamaIndex Document objects.
    #    We keep the page number as metadata so retrieved chunks can cite their source page.
    documents = [
        Document(text=text, metadata={"page": page_num})
        for page_num, text in pages
    ]

    # 3. Configure the embedding model (local, free, no API key).
    #    First run downloads the model (~130MB); later runs use the cached copy.
    print("Loading embedding model (first run downloads it)...")
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

    # 4. Configure how text is split into chunks.
    #    chunk_size = max tokens per chunk; chunk_overlap = shared tokens between neighbors.
    #    These are starting values — we tune them in week 2.
    CHUNK_SIZE = 1024       # Experiment 3A: was 512
    CHUNK_OVERLAP = 100     # proportional to chunk size

    Settings.node_parser = SentenceSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

    # 5. Set up ChromaDB as a persistent local vector store.
    #    PersistentClient writes to disk, so the index survives between runs.
    print(f"Building index (chunk_size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})...")
    db = chromadb.PersistentClient(path="./chroma_db")
    # Delete any existing collection so re-indexing replaces rather than appends
    try:
        db.delete_collection("ai_engineering")
    except Exception:
        pass
    chroma_collection = db.get_or_create_collection("ai_engineering")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # 6. Build the index. This is where the real work happens:
    #    each document is chunked, each chunk is embedded into a vector,
    #    and every vector is stored in ChromaDB.
    print("Building index (chunking + embedding all pages — this takes a few minutes)...")
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
    )

    # 7. Report how many chunks were stored.
    count = chroma_collection.count()
    print(f"\nDone. {count} chunks stored in ./chroma_db")

    return index


if __name__ == "__main__":
    build_index()