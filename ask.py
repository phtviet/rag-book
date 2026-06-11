from query import load_query_engine


def main():
    print("Loading query engine (one-time model load)...")
    query_engine = load_query_engine()
    print("Ready. Ask questions about the AI Engineering book.")
    print("Type 'quit' or 'exit' to stop.\n")

    while True:
        question = input("Q: ").strip()

        # Allow clean exit
        if question.lower() in ("quit", "exit", "q"):
            print("Goodbye.")
            break

        # Ignore empty input
        if not question:
            continue

        response = query_engine.query(question)

        print(f"\nA: {response}\n")
        print("--- Retrieved from these pages: ---")
        for node in response.source_nodes:
            page = node.metadata.get("page", "?")
            score = node.score
            preview = node.text[:150].replace("\n", " ")
            print(f"  page {page} (score {score:.3f}): {preview}...")
        print()


if __name__ == "__main__":
    main()