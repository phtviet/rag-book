import time
from query_rerank import load_query_engine
from eval_set import EVAL_SET


def check_expected(answer: str, expected: list[str]) -> bool:
    """Crude automated check: does the answer contain all expected facts?"""
    answer_lower = answer.lower()
    return all(fact.lower() in answer_lower for fact in expected)


def query_with_retry(query_engine, question: str, max_retries: int = 3):
    """Query the engine, retrying transient errors with exponential backoff.

    Transient API failures (e.g. Anthropic 500 Internal Server Error) usually
    succeed on retry. We wait 1s, 2s, 4s between attempts, then give up.
    """
    for attempt in range(max_retries):
        try:
            return query_engine.query(question)
        except Exception as e:
            if attempt < max_retries - 1:
                wait = 2 ** attempt  # 1s, 2s, 4s
                print(f"  [retry {attempt + 1}/{max_retries - 1}] "
                      f"{type(e).__name__}: {e} — waiting {wait}s...")
                time.sleep(wait)
            else:
                # Out of retries — re-raise so the caller can handle it.
                raise


def main():
    print("Loading query engine...")
    query_engine = load_query_engine()
    print(f"Running {len(EVAL_SET)} eval questions...\n")

    results = []
    for item in EVAL_SET:
        try:
            response = query_with_retry(query_engine, item["question"])
            if response is None:
                raise RuntimeError("query returned None")
            answer = str(response)
            pages = [n.metadata.get("page", "?") for n in response.source_nodes]
            scores = [round(n.score, 3) if n.score is not None else None
                      for n in response.source_nodes]
        except Exception as e:
            print(f"  Q{item['id']} FAILED after retries: {type(e).__name__}: {e}")
            answer = f"[ERROR: {type(e).__name__}: {e}]"
            pages = []
            scores = []

        # Automated check
        if item["out_of_corpus"]:
            decline_signals = ["does not", "doesn't", "no information",
                               "not contain", "cannot find", "can't provide",
                               "don't have information"]
            auto_pass = any(sig in answer.lower() for sig in decline_signals)
        else:
            auto_pass = check_expected(answer, item["expected_contains"])

        results.append({
            "id": item["id"],
            "category": item["category"],
            "question": item["question"],
            "answer": answer,
            "auto_pass": auto_pass,
            "pages": pages,
            "scores": scores,
        })

    # Print a compact report
    print("=" * 70)
    print("EVAL RESULTS")
    print("=" * 70)
    passed = sum(1 for r in results if r["auto_pass"])
    print(f"Auto-pass: {passed}/{len(results)}\n")

    for r in results:
        mark = "PASS" if r["auto_pass"] else "FAIL"
        print(f"[{mark}] Q{r['id']} ({r['category']}): {r['question']}")
        print(f"       pages={r['pages']} scores={r['scores']}")

    # Save full answers to a file for manual review
    with open("eval_run_baseline.md", "w", encoding="utf-8") as f:
        f.write("# Eval run — BASELINE (current system)\n\n")
        f.write(f"Auto-pass: {passed}/{len(results)}\n\n")
        for r in results:
            mark = "PASS" if r["auto_pass"] else "FAIL"
            f.write(f"## Q{r['id']} [{mark}] ({r['category']})\n\n")
            f.write(f"**Q:** {r['question']}\n\n")
            f.write(f"**A:** {r['answer']}\n\n")
            f.write(f"**Retrieved:** pages={r['pages']} scores={r['scores']}\n\n")
            f.write("**Manual score:** \n\n---\n\n")

    print("\nFull answers written to eval_run_baseline.md for manual review.")


if __name__ == "__main__":
    main()