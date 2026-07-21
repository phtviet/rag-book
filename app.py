import streamlit as st
from query_rerank import load_query_engine

# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
st.set_page_config(page_title="AI Engineering RAG", page_icon="📚", layout="centered")

st.title("📚 AI Engineering — RAG Q&A")
st.caption(
    "Ask questions about Chip Huyen's *AI Engineering: Building Applications with "
    "Foundation Models*. Answers are generated **only** from the book's content — "
    "if the book doesn't cover it, the system says so rather than guessing."
)

# The exact decline sentence the faithfulness prompt asks for (used to style declines).
DECLINE_MARKERS = [
    "does not contain",
    "cannot answer",
    "not contain information",
    "no information",
]


# ---------------------------------------------------------------------------
# Load the engine ONCE and cache it across re-runs
# ---------------------------------------------------------------------------
@st.cache_resource(show_spinner="Loading models (one-time, ~15s)...")
def get_engine():
    return load_query_engine()


engine = get_engine()


# ---------------------------------------------------------------------------
# Sidebar: what this is + example questions
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("About")
    st.markdown(
        "A retrieval-augmented generation system over a 500-page technical book.\n\n"
        "**Pipeline:** bi-encoder retrieval (top-20) → cross-encoder reranking → "
        "top-3 chunks → Claude, with a faithfulness prompt that answers only from "
        "the retrieved context."
    )
    st.divider()
    st.subheader("Try an example")
    examples = [
        "What is RAG?",
        "What is the difference between quantization and distillation?",
        "What are the main techniques for inference optimization?",
        "How do entropy and cross-entropy relate?",
        "What is the capital of France?",  # out-of-corpus → should decline
    ]
    # Clicking an example stores it as the pending question.
    for ex in examples:
        if st.button(ex, use_container_width=True):
            st.session_state.pending_question = ex


# ---------------------------------------------------------------------------
# Question input
# ---------------------------------------------------------------------------
# A question can arrive either from the text box or from an example button.
typed = st.text_input("Your question:", placeholder="e.g. What is quantization?")
question = typed or st.session_state.pop("pending_question", None)


# ---------------------------------------------------------------------------
# Answer
# ---------------------------------------------------------------------------
if question:
    st.markdown(f"**Question:** {question}")

    with st.spinner("Searching the book and generating an answer..."):
        response = engine.query(question)
    answer = str(response)

    # Style declines differently from real answers.
    is_decline = any(marker in answer.lower() for marker in DECLINE_MARKERS)
    if is_decline:
        st.info(f"🚫 {answer}")
        st.caption("The book doesn't cover this, so the system declined rather than "
                   "answering from outside knowledge.")
    else:
        st.markdown("### Answer")
        st.write(answer)

    # Sources: which pages the answer drew from, with relevance scores.
    st.markdown("### Sources")
    st.caption("Retrieved chunks after reranking. Relevance is the cross-encoder "
               "score — near 0 means the chunk wasn't actually relevant.")
    for i, node in enumerate(response.source_nodes, 1):
        page = node.metadata.get("page", "?")
        score = node.score if node.score is not None else 0.0
        with st.expander(f"Source {i} — page {page}  (relevance {score:.3f})"):
            st.write(node.text)