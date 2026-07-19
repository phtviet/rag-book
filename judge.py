"""LLM-as-judge: score generated answers against verified reference answers,
then validate the judge against human scores before trusting it.

Two-phase workflow:
  1. Build/parse a set of (question, reference, generated answer, human_score) rows.
  2. Run the judge on each, compare judge verdict vs human score, report agreement.

The judge is only trustworthy if it agrees with human scores. Read the
disagreements' rationales to decide whether the judge's reasoning is sound.
"""
from parse_eval_run import parse_eval_run
import json
import re
import time

from anthropic import Anthropic
from dotenv import load_dotenv

from eval_set import EVAL_SET

load_dotenv()

client = Anthropic()

JUDGE_MODEL = "claude-sonnet-4-5"

JUDGE_PROMPT = """You are evaluating whether a generated answer correctly answers a question, judged against a verified reference answer.

QUESTION:
{question}

REFERENCE ANSWER (the verified ground truth, written from the source book):
{reference}

GENERATED ANSWER (to be judged):
{answer}

QUESTION TYPE: {category}

IMPORTANT RULES — apply these before assigning a verdict:
1. The reference is the ground truth for FACTS, not a template to match. Judge meaning and factual accuracy, not phrasing, structure, or coverage of every detail.
2. NEVER penalise the generated answer for containing accurate, relevant information that is NOT in the reference. Extra correct content is a positive, or at worst neutral. It is NOT evidence of error.
3. Distinguish CORE concepts from SECONDARY detail:
   - A CORE concept is one without which the answer fundamentally fails to convey what the thing IS or how it works. Missing one = partial.
   - SECONDARY detail (extra examples, additional techniques in a list, minor elaborations, specific numbers that aren't the point of the question) being absent does NOT make an answer partial, so long as the core is correct and present.
4. Only mark inaccuracy as WRONG. An answer that is accurate but less exhaustive than the reference is CORRECT, not wrong.

Apply the standard for the question type:
- factual / specific_detail: the core definition/fact must be ACCURATE and match the reference. For specific_detail questions, the specific value asked for must be present and correct.
- comparison: the key differences between the concepts must be stated clearly and accurately.
- synthesis: the answer must form and correctly link the connection between the concepts, matching the RELATIONSHIP described in the reference (not merely mentioning both topics).
- out_of_corpus: a CORRECT answer declines or states the information is not available / not in the source. Fabricating a substantive answer is WRONG.

Assign one verdict:
- "correct": accurate, and conveys the CORE concept(s) the question asks about, consistent with the reference. May omit secondary details. May include extra accurate information.
- "partial": accurate as far as it goes, but a CORE concept, defining property, or required specific value is MISSING.
- "wrong": contains inaccuracies or fabrications, or misses the core concept the question asks about entirely.

Respond with ONLY a JSON object, no other text:
{{"verdict": "correct" | "partial" | "wrong", "rationale": "one sentence explaining the verdict; if partial or wrong, name the specific CORE concept that is missing or inaccurate"}}
"""


def judge_answer(question: str, reference: str, answer: str, category: str,
                 max_retries: int = 3) -> dict:
    """Run the judge on one (question, reference, answer) triple.

    Returns {"verdict": ..., "rationale": ...}. On persistent failure returns
    a verdict of "error" so one bad call doesn't crash the whole validation.
    """
    prompt = JUDGE_PROMPT.format(
        question=question, reference=reference, answer=answer, category=category
    )

    for attempt in range(max_retries):
        try:
            response = client.messages.create(
                model=JUDGE_MODEL,
                max_tokens=512, 
                temperature=0, #Greedy decoding
                messages=[{"role": "user", "content": prompt}],
            )
            raw = response.content[0].text.strip()
            return parse_verdict(raw)
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                return {"verdict": "error", "rationale": f"{type(e).__name__}: {e}"}


def parse_verdict(raw: str) -> dict:
    """Extract the JSON verdict from the model's response, defensively.

    LLMs sometimes wrap JSON in ```json fences or add stray text, so we strip
    fences and, if needed, locate the first {...} block before parsing.
    """
    text = raw.strip()
    # Strip markdown code fences if present
    text = re.sub(r"^```(?:json)?", "", text).strip()
    text = re.sub(r"```$", "", text).strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Fallback: grab the first {...} block
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
    return {"verdict": "parse_error", "rationale": f"could not parse: {raw[:150]}"}

def main():
    import sys
    run_file = sys.argv[1] if len(sys.argv) > 1 else "eval_run_latest.md"
    print(f"Parsing {run_file}...")
    GENERATED = parse_eval_run(run_file)
    print(f"Loaded {len(GENERATED)} scored answers.\n")

    ref_by_id = {item["id"]: item for item in EVAL_SET}

    rows = []
    agree = 0
    for eid in sorted(GENERATED):
        item = ref_by_id[eid]
        gen = GENERATED[eid]
        result = judge_answer(
            question=item["question"],
            reference=item["reference_answer"],
            answer=gen["answer"],
            category=item["category"],
        )
        judge_verdict = result.get("verdict", "error")
        human = gen["human"]
        match = "OK " if judge_verdict == human else ">> MISMATCH"
        if judge_verdict == human:
            agree += 1
        rows.append({
            "id": eid,
            "category": item["category"],
            "human": human,
            "judge": judge_verdict,
            "match": match,
            "rationale": result.get("rationale", ""),
        })
        print(f"Q{eid:2d} [{match}] human={human:8s} judge={judge_verdict:8s}  ({item['category']})")

    n = len(rows)
    print(f"\nAgreement: {agree}/{n} ({100*agree//n if n else 0}%)")
    print("\nMismatches (read these to decide if you trust the judge):")
    for r in rows:
        if r["match"] != "OK ":
            print(f"  Q{r['id']} ({r['category']}): human={r['human']} judge={r['judge']}")
            print(f"     judge's reasoning: {r['rationale']}")

    # Save full detail for the notebook
    with open("judge_validation.md", "w", encoding="utf-8") as f:
        f.write("# LLM-as-judge validation vs human scores\n\n")
        f.write(f"Agreement: {agree}/{n}\n\n")
        f.write("| Q | category | human | judge | match | judge rationale |\n")
        f.write("|---|----------|-------|-------|-------|------------------|\n")
        for r in rows:
            f.write(f"| {r['id']} | {r['category']} | {r['human']} | {r['judge']} | "
                    f"{'OK' if r['match']=='OK ' else 'MISMATCH'} | {r['rationale']} |\n")
    print("\nWrote judge_validation.md")


if __name__ == "__main__":
    main()
