import chromadb
from llama_index.core import VectorStoreIndex, Settings
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.prompts import ChatPromptTemplate
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.anthropic import Anthropic
from llama_index.postprocessor.sbert_rerank import SentenceTransformerRerank
from dotenv import load_dotenv

load_dotenv()


# Faithfulness + declining rules go in the SYSTEM message (highest authority).
FAITHFUL_SYSTEM = (
    "You are a question-answering system that answers using ONLY the provided context. "
    "Follow these rules strictly:\n"
    "1. Use ONLY information found in the context below. Do NOT use outside or prior "
    "knowledge, even if you are confident you know the answer.\n"
    "2. Be THOROUGH with the context you are given: include the specific details, names, "
    "techniques, examples, and figures that ARE present in the context. Do not omit "
    "relevant specifics that the context provides.\n"
    "3. If the context does not contain the information needed, clearly state that the "
    "provided context does not contain the answer. Do not guess or fill gaps from general knowledge.\n"
    "4. Do not add facts, figures, examples, or claims that are not present in the context.\n"
    "5. Answer directly. Do NOT preface answers with phrases like 'Based on the provided "
    "context' or 'According to the context'. State the answer directly.\n"
    "The goal: a complete answer that uses everything relevant in the context, and nothing from outside it."
)

FAITHFUL_USER = (
    "Context:\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Question: {query_str}\n"
    "Grounded answer:"
)

FAITHFUL_QA_CHAT_TEMPLATE = ChatPromptTemplate(
    message_templates=[
        ChatMessage(role=MessageRole.SYSTEM, content=FAITHFUL_SYSTEM),
        ChatMessage(role=MessageRole.USER, content=FAITHFUL_USER),
    ]
)


def load_query_engine():
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    Settings.llm = Anthropic(model="claude-sonnet-4-5", max_tokens=1024)

    db = chromadb.PersistentClient(path="./chroma_db")
    chroma_collection = db.get_or_create_collection("ai_engineering")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    index = VectorStoreIndex.from_vector_store(vector_store)

    reranker = SentenceTransformerRerank(
        model="BAAI/bge-reranker-base",
        top_n=3,
    )

    query_engine = index.as_query_engine(
        similarity_top_k=20,
        node_postprocessors=[reranker],
    )

    # Override the CHAT QA template (the one that actually fires - confirmed by diagnostic).
    query_engine.update_prompts(
        {"response_synthesizer:text_qa_template": FAITHFUL_QA_CHAT_TEMPLATE}
    )

    return query_engine


if __name__ == "__main__":
    engine = load_query_engine()
    response = engine.query("How do the chapters on evaluation and inference optimization relate?")
    print(response)
    print("\n--- Retrieved (after rerank) ---")
    for node in response.source_nodes:
        page = node.metadata.get("page", "?")
        score = node.score
        print(f"  page {page} (rerank score {score:.3f})")