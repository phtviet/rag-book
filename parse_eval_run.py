"""Parse an eval run markdown file into the structure the judge needs.

This reads the VERBATIM generated answers and manual scores straight out of an
eval_run_*.md file, so nothing is hand-transcribed or paraphrased between the
system's output and the judge's input.

Expected block format (as written by run_eval.py):

    ## Q1 [PASS] (factual)

    **Q:** What is quantization?

    **A:** Quantization refers to ...
    ...possibly multiple paragraphs...

    **Retrieved:** pages=[...] scores=[...]

    **Manual score:** Correct.

    ---
"""

import re


def parse_eval_run(path: str) -> dict:
    """Read an eval run file and return {id: {"answer": str, "human": str}}.

    The answer is taken verbatim (everything between '**A:**' and '**Retrieved:**').
    The human score is taken from '**Manual score:**' and normalised to
    correct / partial / wrong.
    """
    with open(path, encoding="utf-8") as f:
        text = f.read()

    # Normalise Windows line endings so the regexes behave consistently.
    text = text.replace("\r\n", "\n")

    # Split into per-question blocks. Each starts with '## Q<number>'.
    # We keep the delimiter by splitting on a lookahead.
    blocks = re.split(r"\n(?=## Q\d+\s)", text)

    results = {}
    for block in blocks:
        # Which question is this?
        header = re.match(r"##\s*Q(\d+)", block.strip())
        if not header:
            continue
        qid = int(header.group(1))

        # Verbatim answer: everything between '**A:**' and '**Retrieved:**'
        answer_match = re.search(
            r"\*\*A:\*\*\s*(.*?)\s*(?=\*\*Retrieved:\*\*)", block, re.DOTALL
        )
        if not answer_match:
            print(f"  WARNING: no answer found for Q{qid}, skipping")
            continue
        answer = answer_match.group(1).strip()

        # Manual score: text after '**Manual score:**' up to the end/divider
        score_match = re.search(
            r"\*\*Manual score.*?:\*\*\s*(.*?)\s*(?=\n---|\Z)", block, re.DOTALL
        )
        if not score_match or not score_match.group(1).strip():
            print(f"  WARNING: no manual score found for Q{qid}, skipping")
            continue
        human_raw = score_match.group(1).strip()

        results[qid] = {"answer": answer, "human": normalize_human_score(human_raw)}

    return results


def normalize_human_score(score: str) -> str:
    """Map free-text manual scores ('Correct.', 'Partial (missing X)') to a verdict."""
    s = score.strip().lower()
    if s.startswith("correct"):
        return "correct"
    if s.startswith("partial"):
        return "partial"
    if s.startswith("wrong"):
        return "wrong"
    return s  # leave unexpected values visible rather than silently guessing


if __name__ == "__main__":
    import sys
    from collections import Counter

    path = sys.argv[1] if len(sys.argv) > 1 else "eval_run_baseline.md"
    parsed = parse_eval_run(path)

    print(f"Parsed {len(parsed)} questions from {path}")
    print(f"Human scores: {dict(Counter(v['human'] for v in parsed.values()))}\n")

    # Show a preview so you can eyeball that answers came through verbatim.
    for qid in sorted(parsed):
        answer = parsed[qid]["answer"]
        preview = answer[:80].replace("\n", " ")
        print(f"  Q{qid:2d} [{parsed[qid]['human']:8s}] {len(answer):5d} chars | {preview}...")
