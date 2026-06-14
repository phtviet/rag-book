import sys
from query import load_query_engine


def inspect(question: str):
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


if __name__ == "__main__":
    # Take the question from the command line, or use a default
    question = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "What percentage smaller is DistilBERT than BERT?"
    inspect(question)