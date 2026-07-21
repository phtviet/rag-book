# Eval run — eval_run_latest.md

Auto-pass: 16/20

## Q1 [PASS] (factual)

**Q:** What is quantization?

**A:** Based on the provided context, quantization refers to the practice of converting a model from a format with more bits to a format with fewer bits. It is a straightforward and efficient way to reduce a model's memory footprint.

The context provides a specific example: For a model of 13 billion parameters, using FP32 means 4 bytes per weight or 52 GB for the whole weights. If you can reduce each value to only 2 bytes, the memory needed for the model's weights decreases to 26 GB.

The context also notes that "Reducing precision, also known as quantization, is a cheap and extremely effective way to reduce a model's memory footprint."

**Retrieved:** pages=[344, 148, 352] scores=[0.554, 0.464, 0.428]

**Manual score:** 

---

## Q2 [PASS] (specific_detail)

**Q:** What percentage smaller is DistilBERT than BERT?

**A:** According to the context, DistilBERT reduces the size of a BERT model by 40%.

**Retrieved:** pages=[419, 28, 336] scores=[0.91, 0.551, 0.241]

**Manual score:** 

---

## Q3 [PASS] (factual)

**Q:** What is model distillation?

**A:** Based on the provided context:

Model distillation (also called knowledge distillation) is a method in which a small model (student) is trained to mimic a larger model (teacher). The knowledge of the big model is distilled into the small model, hence the term distillation.

Traditionally, the goal of model distillation is to produce smaller models for deployment. Deploying a big model can be resource-intensive. Distillation can produce a smaller, faster student model that retains performance comparable to the teacher.

**Retrieved:** pages=[419, 451, 420] scores=[0.999, 0.849, 0.135]

**Manual score:** 

---

## Q4 [PASS] (comparison)

**Q:** What's the difference between quantization and distillation?

**A:** Based on the provided context:

**Quantization** involves reducing the precision of a model to reduce its memory footprint and increase its throughput. It refers to converting a model from a format with more bits to a format with fewer bits. For example, reducing a model from 32 bits to 16 bits reduces its memory footprint by half. Quantization can use as few as 16 bits, 8 bits, or even 4 bits for inference.

**Distillation** (also called knowledge distillation or model distillation) is a method in which a small model (student) is trained to mimic the behavior of a larger model (teacher). The knowledge of the big model is distilled into the small model. This produces a smaller, faster student model that retains performance comparable to the teacher model.

The key difference is that quantization reduces the numerical precision of an existing model's parameters, while distillation creates an entirely new smaller model that learns to replicate the larger model's behavior.

**Retrieved:** pages=[451, 344, 419] scores=[0.49, 0.38, 0.144]

**Manual score:** 

---

## Q5 [PASS] (synthesis)

**Q:** How do the chapters on evaluation and inference optimization relate?

**A:** Based on the provided context, the chapters on evaluation and inference optimization relate in the following ways:

1. **Sequential coverage in the book**: The context indicates that inference optimization techniques, including quantization, distillation, and parallelism, are discussed in Chapters 7 through 9, while evaluation is discussed in Chapter 3.

2. **Complementary focus areas**: Evaluation (Chapter 3) focuses on making models better by mitigating risks and uncovering opportunities throughout the model adaptation process. Inference optimization (Chapter 9) focuses on making models faster and cheaper, as stated: "Up until now, the book has discussed various techniques for making models better. This chapter focuses on making them faster and cheaper."

3. **Both are critical for production deployment**: The context mentions that evaluation is "necessary throughout the whole model adaptation process" and is needed "to determine whether an application is ready for deployment." Similarly, inference optimization addresses practical production concerns, noting that "if it's too slow, your users might lose patience, or worse, its predictions might become useless."

The chapters address different but complementary aspects of building AI applications with foundation models—evaluation ensures quality and readiness, while inference optimization ensures practical performance and cost-effectiveness.

**Retrieved:** pages=[430, 68, 429] scores=[0.787, 0.762, 0.741]

**Manual score:** 

---

## Q6 [PASS] (out_of_corpus)

**Q:** What does the book say about quantum computing?

**A:** The provided context does not contain information to answer this question.

**Retrieved:** pages=[443, 534, 22] scores=[0.009, 0.004, 0.003]

**Manual score:** 

---

## Q7 [PASS] (factual)

**Q:** What is RAG?

**A:** Based on the provided context:

RAG stands for **retrieval-augmented generation**. It is a technique that enhances a model's generation by retrieving relevant information from external memory sources. An external memory source can be an internal database, a user's previous chat sessions, or the internet.

The term was coined in the paper "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (Lewis et al., 2020), which proposed RAG as a solution for knowledge-intensive tasks where all available knowledge can't be input into the model directly. With RAG, only the information most relevant to the query, as determined by the retriever, is retrieved and input into the model.

The RAG pattern follows a retrieve-then-generate approach: the system first retrieves relevant information (such as Wikipedia pages most relevant to a question), then the model uses that information to generate an answer. This helps the model generate more detailed responses while reducing hallucinations.

**Retrieved:** pages=[277, 330, 278] scores=[0.942, 0.796, 0.64]

**Manual score:** 

---

## Q8 [PASS] (factual)

**Q:** What are embeddings?

**A:** Based on the provided context:

An embedding is a numerical representation that aims to capture the meaning of the original data. An embedding is a vector - for example, the sentence "the cat sits on a mat" might be represented using an embedding vector that looks like [0.11, 0.02, 0.54].

The context explains that since computers work with numbers, models need to convert their input into numerical representations that computers can process. Embeddings serve this purpose by providing these numerical representations.

In reality, the size of an embedding vector (the number of elements in the embedding vector) is typically between 100 and 10,000. An embedding is considered a representation of complex data in a lower-dimensional space compared to the raw data.

**Retrieved:** pages=[158, 295, 286] scores=[0.077, 0.028, 0.022]

**Manual score:** 

---

## Q9 [FAIL] (synthesis)

**Q:** What are the main techniques for inference optimization?

**A:** Based on the provided context, inference optimization can be done at three main levels:

1. **Model level**: You can reduce a trained model's size or develop more efficient architectures, such as ones without computation bottlenecks in the attention mechanism often used in transformer models.

2. **Hardware level**: You can design more powerful hardware.

3. **Service level**: The inference service runs the model on the given hardware to accommodate user requests. It can incorporate techniques that optimize models for specific hardware and consider usage and traffic patterns to efficiently allocate resources to reduce latency and cost.

The context also mentions that at the service level, most optimization techniques focus on resource management, with batching being identified as one of the easiest ways to reduce cost. Three main batching techniques are mentioned: static batching, dynamic batching, and continuous batching.

**Retrieved:** pages=[429, 464, 450] scores=[0.977, 0.976, 0.963]

**Manual score:** 

---

## Q10 [PASS] (factual)

**Q:** Who is Chip Huyen?

**A:** Based on the provided context, Chip Huyen is a writer and computer scientist specializing in machine learning (ML) systems. She has worked at NVIDIA, Snorkel AI, founded an AI infrastructure startup (which was later acquired), and taught ML systems at Stanford University. She is the author of "Designing Machine Learning Systems" (O'Reilly, 2022), which is an Amazon bestseller in AI and has been translated into over 10 languages. She is also the author of "AI Engineering" and four bestselling Vietnamese books, including the series "Xach ba lo len va Di" (Pack Your Bag and Go).

**Retrieved:** pages=[534, 132, 21] scores=[0.999, 0.924, 0.158]

**Manual score:** 

---

## Q11 [PASS] (factual)

**Q:** What is backward propagation?

**A:** Based on the provided context, backward propagation (or backpropagation) is described as follows:

Backward pass is the process of updating the model's weights using the aggregated signals from the forward pass. It works at a high level by:

1. Comparing the computed output from the forward pass against the expected output (ground truth). The difference between the computed output and the expected output is called the loss.

2. Computing how much each trainable parameter contributes to the mistake. This value is called the gradient. Mathematically, gradients are computed by taking the derivative of the loss with respect to each trainable parameter.

3. Adjusting trainable parameter values using their corresponding gradient. How much each parameter should be readjusted, given its gradient value, is determined by the optimizer (common optimizers include SGD and Adam).

The context notes that during training, both the forward pass and backward pass are executed, while during inference, only the forward pass is executed.

**Retrieved:** pages=[345, 430, 478] scores=[0.235, 0.001, 0.0]

**Manual score:** 

---

## Q12 [PASS] (out_of_corpus)

**Q:** What is Viet's favourite colour?

**A:** The provided context does not contain information to answer this question.

**Retrieved:** pages=[28, 114, 455] scores=[0.004, 0.003, 0.001]

**Manual score:** 

---

## Q13 [FAIL] (factual)

**Q:** What are the best practices of prompt engineering?

**A:** Based on the provided context, here are the best practices for prompt engineering:

1. **Write Clear and Explicit Instructions**
   - Explain without ambiguity what you want the model to do
   - Specify details like scoring systems (e.g., 1-5 or 1-10 scale)
   - Clarify how to handle uncertainty (e.g., pick best answer or output "I don't know")
   - Adjust prompts to prevent undesirable behaviors (e.g., specify integer-only scores if fractional scores are unwanted)

2. **Provide Examples and Relevant Information**
   - Clear instructions with examples and relevant information are essential

3. **Use Step-by-Step Thinking**
   - Ask the model to slow down and think step by step, which can yield surprising improvements

4. **Organize and Version Prompts**
   - Separate prompts from code (e.g., put prompts in a separate file like prompts.py)
   - This approach provides:
     - **Reusability**: Multiple applications can reuse the same prompt
     - **Testing**: Code and prompts can be tested separately
     - **Readability**: Makes both code and prompts easier to read

5. **Keep It Simple**
   - Start by writing your own prompts without tools to better understand the underlying model and requirements
   - If using prompt engineering tools, always inspect the prompts they produce and track API calls

6. **Consider Model Quirks and Biases**
   - AI models have their own quirks and biases that need to be considered

**Retrieved:** pages=[244, 275, 257] scores=[0.987, 0.972, 0.947]

**Manual score:** 

---

## Q14 [PASS] (factual)

**Q:** What are the malicious attacks that can be done with prompt engineering?

**A:** Based on the provided context, there are three main types of prompt attacks:

1. **Prompt extraction**: Extracting the application's prompt, including the system prompt, either to replicate or exploit the application.

2. **Jailbreaking and prompt injection**: Getting the model to do bad things. This includes:
   - **Indirect prompt injection**: Attackers place malicious instructions in tools that the model is integrated with (such as public web pages, GitHub repositories, YouTube videos, and Reddit comments), waiting for models to find them via tools like web search.

3. **Information extraction**: Getting the model to reveal its training data or information used in its context.

These attacks can result in various risks including:
- Remote code or tool execution
- Data leaks
- Social harms (helping attackers gain knowledge about dangerous or criminal activities)
- Misinformation
- Service interruption and subversion
- Brand risk

**Retrieved:** pages=[260, 266, 259] scores=[0.964, 0.95, 0.948]

**Manual score:** 

---

## Q15 [FAIL] (synthesis)

**Q:** What is the future of comparative evaluation?

**A:** According to the provided context, the future of comparative evaluation includes several key aspects:

1. **Continued relevance as models surpass human performance**: As models become stronger and surpass human performance, it might become impossible for human evaluators to give model responses concrete scores. However, human evaluators might still be able to detect differences between outputs, making comparative evaluation potentially "the only option."

2. **Captures human preference**: Comparative evaluation aims to capture the quality we care about: human preference. It reduces the pressure to constantly create more benchmarks to catch up with AI's ever-expanding capabilities.

3. **Won't become saturated**: Unlike benchmarks that become useless when model performance achieves perfect scores, comparative evaluations will never get saturated as long as newer, stronger models are introduced.

4. **Difficult to game**: Comparative evaluation is relatively hard to game, as there's no easy way to cheat, like training your model on reference data. For this reason, many trust the results of public comparative leaderboards more than other public leaderboards.

5. **Complementary role**: For offline evaluation, it can be a great addition to evaluation benchmarks. For online evaluation, it can be complementary to A/B testing. It can provide discriminating signals about models that can't be obtained otherwise.

**Retrieved:** pages=[179, 139, 180] scores=[0.3, 0.153, 0.114]

**Manual score:** 

---

## Q16 [FAIL] (synthesis)

**Q:** When should we finetune a model?

**A:** Based on the provided context, you should finetune a model in the following situations:

1. **After extensive experiments with prompt-based methods**: Finetuning is generally attempted after trying prompt-based approaches, as it requires significantly more resources in data, hardware, and ML talent.

2. **To improve model quality**: The primary reason is to improve a model's quality in terms of both general capabilities and task-specific capabilities.

3. **For specific output structures**: Finetuning is commonly used to improve a model's ability to generate outputs following specific structures, such as JSON or YAML formats.

4. **When the model wasn't sufficiently trained on your task**: If a general-purpose model performs well on benchmarks but not on your specific task, finetuning with your data can be especially useful. Examples include:
   - Converting text to less common SQL dialects
   - Handling customer-specific queries that the model often fails on

5. **When you have the necessary resources**: You should have:
   - Annotated data (which can be slow and expensive to acquire)
   - Knowledge of how to train models
   - Ability to serve and host the finetuned model
   - A policy and budget for monitoring, maintaining, and updating the model

The context emphasizes that if you're just starting to experiment with a project, finetuning is rarely the first thing you should attempt due to high up-front investments and continual maintenance requirements.

**Retrieved:** pages=[335, 66, 337] scores=[0.78, 0.776, 0.764]

**Manual score:** 

---

## Q17 [PASS] (out_of_corpus)

**Q:** How do I make bombs?

**A:** The provided context does not contain information to answer this question.

**Retrieved:** pages=[264, 265, 274] scores=[0.03, 0.004, 0.002]

**Manual score:** 

---

## Q18 [PASS] (comparison)

**Q:** What is the difference between data-centric AI and model-centric AI?

**A:** Based on the provided context:

**Model-centric AI** tries to improve AI performance by enhancing the models themselves. This involves designing new architectures, increasing the sizes of the models, or developing new training techniques.

**Data-centric AI** tries to improve AI performance by enhancing the data. This involves developing new data processing techniques and creating high-quality datasets that allow better models to be trained with fewer resources.

The context also notes that while this division helps guide research, "meaningful technological progress often requires investment in both model and data improvements."

**Retrieved:** pages=[388, 389, 36] scores=[0.999, 0.847, 0.024]

**Manual score:** 

---

## Q19 [PASS] (specific_detail)

**Q:** As of May 2024, how many repositories are dedicated to evaluation, from the author's own analysis of the top 1000 AI-related repositories on Github?

**A:** According to the context, the author found over 50 repositories dedicated to evaluation as of May 2024, from their analysis of the top 1,000 AI-related repositories on GitHub.

**Retrieved:** pages=[140, 62, 141] scores=[0.999, 0.832, 0.578]

**Manual score:** 

---

## Q20 [PASS] (synthesis)

**Q:** How does entropy and cross-entropy relate?

**A:** According to the provided context, entropy and cross-entropy are closely related in the following way:

A language model's cross entropy on a dataset depends on two qualities:

1. The training data's predictability, measured by the training data's entropy
2. How the distribution captured by the language model diverges from the true distribution of the training data

Mathematically, if P is the true distribution of the training data and Q is the distribution learned by the language model:
- The training data's entropy is H(P)
- The divergence of Q with respect to P is measured using the Kullback–Leibler (KL) divergence, represented as DKL(P || Q)

The context also notes that "Entropy and cross entropy share the same mathematical notation, H."

In essence, cross entropy measures how difficult it is for a language model to predict what comes next in a dataset, and this difficulty depends both on the inherent entropy (predictability) of the data itself and on how well the model's learned distribution matches the true data distribution.

**Retrieved:** pages=[143, 144, 146] scores=[0.66, 0.548, 0.496]

**Manual score:** 

---

