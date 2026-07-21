from query_rerank import load_query_engine

query_engine = load_query_engine()

prompts = query_engine.get_prompts()
for key, prompt in prompts.items():
    print(f"=== {key} ===")
    print(prompt.get_template())
    print()