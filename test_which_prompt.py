from llama_index.core import PromptTemplate
from query_rerank import load_query_engine

engine = load_query_engine()

# Override BOTH the plain and chat QA templates with distinct markers.
plain_marker = PromptTemplate(
    "PLAIN_TEMPLATE_FIRED. Context:\n{context_str}\nQuery: {query_str}\nAnswer: "
)

engine.update_prompts({
    "response_synthesizer:text_qa_template": plain_marker,
})

resp = engine.query("What is quantization?")
print("\n=== ANSWER ===")
print(resp)