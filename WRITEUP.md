# What building a RAG system taught me about evaluation

The world of work is increasingly filled with AI systems, and I want to be prepared for it. Having done a Master of Data Science, I have some experience with machine learning models and understand how they work intuitively, but have not had extensive experience building one.

The field is also moving fast so I need a way to gain practical skills efficiently without doing another 2-year degree. I bought a textbook titled *AI Engineering: Building Applications with Foundation Models*, a 500-page technical book by Chip Huyen, a Vietnamese author that I admire, with the goal of reading it through and becoming proficient that way. I got about a third of the way through the book then stopped for a good 2 months before even thinking about it again, mostly due to work obligations, and my limited willpower only wants to play videogames at the end of the day.

This first project is then born out of frustration at my own inability to retain knowledge and follow through when it comes to learning AI Engineering. I very much prefer clearly defined goals and tangible results, over reading a textbook cover-to-cover to learn a new subject.

## The setup

So, for my first project, I built a retrieval-augmented generation (RAG) system over Chip Huyen's *AI Engineering*.

If you haven't come across RAG before, here's the idea in plain terms. A language model like Claude or ChatGPT knows a lot, but it doesn't know the specific contents of *your* document, and if you ask it about something it hasn't seen, it will sometimes confidently make things up. RAG is a way around that. Instead of asking the model to answer from memory, you first go and *retrieve* the handful of passages from your document that are most relevant to the question, then hand those passages to the model and say "answer using only this." The model does the language part; your document supplies the facts. It's the difference between asking someone to recite an answer from memory versus letting them look it up in the book first.

The pipeline for doing that is fairly standard. You split the book into small chunks, convert each chunk into a list of numbers that captures its meaning (an "embedding"), and store them. When a question comes in, you convert the question the same way and find the chunks whose numbers are most similar, i.e. the passages most related to the question. Then you pass those chunks to Claude to write the answer.

What made the project interesting to me wasn't the pipeline. It was that I wrote a 20-question evaluation set with verified reference answers first, and measured every single change against it. So, it really is all about the process, not the destination, like they say.

That eval set turned out to be the most important thing I built, because almost everything I learned came from a number moving in a direction I didn't expect.

## Finding 1: Cleaning the data made it worse

My first "improvement" was obvious housekeeping: strip the back-of-book index, i.e. pages that contain things like "quantization, 340–352" entries, out of the corpus. They were junk text. I predicted the retrieval would get cleaner and the score would stay flat but most likely improve.

But, the score dropped. One synthesis question on my eval set, "How do the chapters on evaluation and inference optimization relate?" even went from correct to wrong.

When I looked at which chunks were being retrieved, the mechanism was almost funny. The index page I deleted happened to be the only retrieved chunk that contained the word "evaluation" near the word "optimization." It was keyword soup, but that soup was the only thing bridging the two topics the question asked about. The model had been using garbage to answer a question it was never really answering well, and removing the garbage exposed that.

Junk by one measure can be load-bearing by another. A flat aggregate score can bury how much this matters, because the total barely moved even though the composition of the answers changed. I caught it because I checked each question rather than just glancing at the total. If I'd only watched the aggregate number, I'd have concluded cleaning did nothing, moved on to the next experiment, and missed a real problem. You have to look at which questions changed and why, not just the total.

## Finding 2: Reranking helped, but it has a bias worth knowing

The change that helped the most was adding a reranker. The idea is a two-stage retrieval. The first stage uses a fast but rough method to pull a wide pool of 20 candidate chunks (a "bi-encoder" — it compares the question and each chunk separately, which is quick but a bit crude). The second stage uses a slower but sharper method to re-score just those 20 and keep only the best 3 (a "cross-encoder" — it looks at the question and a chunk *together*, which is more accurate but too expensive to run over the whole book). Cheap-and-wide to narrow the field, then expensive-and-precise to pick the winners. It's a standard pattern, and it earned its reputation here. It recovered the synthesis question I broke in Finding 1, and pushed my score up more than any other single change.

But it wasn't free, and the cost showed up in a consistent way. Twice, on a question about the difference between quantization and distillation, and again on one about how entropy and cross-entropy relate, the reranker demoted exactly the chunk I needed. And both times the demoted chunk was a terse one: a definition in the first case, a formula in the second. The reranker consistently preferred longer, explanatory prose over short factual statements, even when the short statement was the actual answer to the question.

I could see it happening in the scores. For the entropy question, the chunk with the formula H(P,Q) = H(P) + D_KL(P||Q) was retrieved by the bi-encoder at rank 2, right near the top. Then the cross-encoder scored it near the bottom and it fell out of the final 3. The answer that came back explained the relationship in words but never gave the formula, because the model never saw it.

The lesson I took from this is that a reranker isn't a strict upgrade, it's a trade. It's very good on the whole, but the thing it quietly trades away is short, high-value factual chunks like definitions and formulas. That's worth knowing before you put one in front of a system where those terse facts are the point.

## Finding 3: My automated judge hallucinated, which is exactly why you validate it

Scoring 20 answers by hand after every experiment gets old fast, and it doesn't scale if I want to run lots of experiments. So I built an LLM-as-judge: a second model call that reads the question, my reference answer, and the generated answer, and returns a score.

The tempting thing here is to build the judge and immediately start trusting its numbers. I made myself validate it against my own hand-scores first, and I'm glad I did, because it did two things that would have quietly poisoned my results if I hadn't checked.

The first was that it was stricter than me, consistently in one direction. When I read its reasoning, it was often right. It caught real gaps where I'd been too lenient, like an answer about embeddings that never mentioned the defining property that similar items end up close together in the vector space. That's a fair catch, and I revised those scores.

But then on one question, the judge claimed the generated answer contained a formula, when that formula was only in my reference answer, not in the answer it was supposed to be grading. It had bled the ground truth into its judgment of the thing it was meant to evaluate independently. That's a real problem, because the judge's reasoning is the only thing I have to audit it by. If the reasoning can invent what it's grading, I can't fully trust the reasoning.

The second problem was that it gave different verdicts for the same input on different runs. I ran the exact same validation three times and got 20, then 19, then 20, and the one that flipped was always the same borderline question. This comes down to how these models work: by default they sample from a probability distribution over possible outputs, so the same input can produce a slightly different answer each time. The fix is to set the temperature to 0, which makes the model always take its single most likely output. That's the right setting for something you want to behave like a measuring instrument, even though it's the wrong setting for creative writing where you want variety. Once I did that, three runs gave identical results.

So I did adopt the judge, but not as a blind replacement for looking at the answers myself. I use it as a reproducible scorer and as a flag for which answers to review by hand. The validation was the whole point. An automated metric you haven't checked can be worse than no metric, because you'll actually trust it.

## The thing underneath all three

Looking back, all three findings have the same shape. I expected one thing, a number told me something different, and the interesting part was always figuring out why. And none of it would have surfaced without the eval set. The corpus-cleaning regression would have shipped without me noticing, because the system would have felt cleaner while actually being worse. The reranker's bias would have looked like a pure win. The judge's hallucination would have gone straight into my results as if it were fact.

The lesson I'm taking into the next project isn't really about RAG. It's that the evaluation set isn't scaffolding you build on the side to check the real work. It is the real work. Making the model changes was the easy part. Knowing whether they actually helped was the hard part, and honestly the only part that made this feel like engineering rather than guessing and hoping.

This is also the kind of thing I want to get good at more broadly. I care about applying careful, evidence-based methods to real problems, and this project was a small, self-contained version of that: the measurement wasn't an afterthought, it was the point.

---

*Code and the full experiment log are on GitHub: https://github.com/phtviet/rag-book. This was project 1 of 3 in a sprint to move into AI engineering.*
