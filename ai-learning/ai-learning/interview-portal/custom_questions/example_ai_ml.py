"""
AI / ML Engineer — Custom Question Pack
========================================
Drop any .py file in this folder with NAME, DESCRIPTION, ICON, and QUESTIONS
to add it as a selectable pack on the portal landing page.

Required fields per question:
  type         : "mcq" | "find_the_bug" | "coding"
  difficulty   : "easy" | "medium" | "hard"
  topic        : str
  question     : str
  correct_answer: str
  explanation  : str  (shown after answering)
  remember     : str  (single key rule/insight)

MCQ extras      : options (list of 4 strings, e.g. "A) ...")
find_the_bug    : code (str), language (str)
coding          : language (str), starter_code (str)
"""

NAME        = "AI / ML Engineering"
DESCRIPTION = "LLMs, training loops, fine-tuning, evaluation, MLOps"
ICON        = "🤖"

QUESTIONS = [
    # ── Easy ──────────────────────────────────────────────────────────────────
    {
        "type": "mcq",
        "difficulty": "easy",
        "topic": "Transformer Architecture",
        "question": (
            "In transformer self-attention, what is the role of the scaling factor "
            "1/√d_k in the attention formula  softmax(QK^T / √d_k) · V ?"
        ),
        "options": [
            "A) It normalises the output values to the range [0, 1]",
            "B) It prevents dot-products from growing large and pushing softmax into "
               "low-gradient regions",
            "C) It controls the learning rate of the attention weights",
            "D) It reduces the number of parameters in the attention head",
        ],
        "correct_answer": (
            "B) It prevents dot-products from growing large and pushing softmax into "
            "low-gradient regions"
        ),
        "explanation": (
            "When d_k is large, the dot products QK^T grow in magnitude, pushing "
            "softmax into regions where the gradient is near zero (saturation). "
            "Dividing by √d_k keeps the variance of the dot products roughly at 1 "
            "regardless of d_k, stabilising gradients and training."
        ),
        "remember": (
            "Scale by 1/√d_k to stop large d_k from saturating softmax. "
            "Vanishing gradient ∝ sharpness of the softmax distribution."
        ),
    },
    {
        "type": "mcq",
        "difficulty": "easy",
        "topic": "Tokenisation",
        "question": (
            "Why do most modern LLMs use Byte-Pair Encoding (BPE) or similar "
            "subword tokenisation rather than character-level or word-level tokenisation?"
        ),
        "options": [
            "A) Subword tokenisation requires less GPU memory at inference time",
            "B) It balances vocabulary size with the ability to handle rare/unknown "
               "words by splitting them into known subword units",
            "C) BPE tokens are easier for the model to interpret semantically",
            "D) Character-level models cannot represent numbers or punctuation",
        ],
        "correct_answer": (
            "B) It balances vocabulary size with the ability to handle rare/unknown "
            "words by splitting them into known subword units"
        ),
        "explanation": (
            "Word-level tokenisation fails on out-of-vocabulary words and needs a huge "
            "vocab. Character-level keeps vocab tiny but sequences become very long, "
            "increasing compute. BPE merges frequent byte pairs iteratively, producing a "
            "compact vocab (32k–100k) that can still represent any input without an "
            "<UNK> token."
        ),
        "remember": (
            "BPE trade-off: vocab ~32–100k tokens. Rare words split into subwords "
            "(e.g. 'unhappiness' → 'un', '##happy', '##ness'). No <UNK>."
        ),
    },

    # ── Medium ─────────────────────────────────────────────────────────────────
    {
        "type": "mcq",
        "difficulty": "medium",
        "topic": "Fine-tuning & PEFT",
        "question": (
            "What does LoRA (Low-Rank Adaptation) do to reduce the number of "
            "trainable parameters during fine-tuning?"
        ),
        "options": [
            "A) Prunes attention heads that fall below an importance threshold",
            "B) Decomposes weight updates into two small low-rank matrices A and B "
               "instead of updating the full weight matrix",
            "C) Freezes all layers except the final classification head",
            "D) Quantises weights to 4-bit before the fine-tuning forward pass",
        ],
        "correct_answer": (
            "B) Decomposes weight updates into two small low-rank matrices A and B "
            "instead of updating the full weight matrix"
        ),
        "explanation": (
            "LoRA adds trainable matrices A (d×r) and B (r×k) alongside frozen "
            "pre-trained weights W (d×k), where rank r << d. The effective weight "
            "becomes W + BA. Because r is tiny (e.g. 8 or 16), trainable parameters "
            "drop by 10,000× on large models while quality stays close to full fine-tuning."
        ),
        "remember": (
            "LoRA: W' = W + BA, rank r << d. "
            "Only A and B are trained. W stays frozen. "
            "~10,000× fewer params than full fine-tuning."
        ),
    },
    {
        "type": "find_the_bug",
        "difficulty": "medium",
        "topic": "PyTorch Training Loop",
        "question": "Find and fix the bug in this PyTorch training loop:",
        "language": "python",
        "code": (
            "for epoch in range(num_epochs):\n"
            "    for batch_idx, (inputs, labels) in enumerate(train_loader):\n"
            "        inputs  = inputs.to(device)\n"
            "        labels  = labels.to(device)\n"
            "        outputs = model(inputs)\n"
            "        loss    = criterion(outputs, labels)\n"
            "        loss.backward()\n"
            "        optimizer.step()\n"
            "\n"
            "        if batch_idx % 100 == 0:\n"
            "            print(f'Epoch {epoch} | Loss: {loss.item():.4f}')"
        ),
        "correct_answer": (
            "Missing optimizer.zero_grad() before loss.backward(). "
            "Without it, gradients accumulate across batches, corrupting all updates. "
            "Add `optimizer.zero_grad()` as the first line inside the inner loop."
        ),
        "explanation": (
            "PyTorch accumulates gradients in each parameter's .grad tensor by default. "
            "Without zero_grad() the gradient used in step() is the sum of all previous "
            "batches' gradients, not just the current one. This causes divergence or "
            "severely distorted updates. The fix: call optimizer.zero_grad() before "
            "loss.backward() on every iteration."
        ),
        "remember": (
            "PyTorch training mantra: "
            "zero_grad() → forward() → loss() → backward() → step(). "
            "Never skip zero_grad()."
        ),
    },

    # ── Hard ───────────────────────────────────────────────────────────────────
    {
        "type": "mcq",
        "difficulty": "hard",
        "topic": "RLHF & Alignment",
        "question": (
            "In the PPO-based RLHF objective, what is the purpose of the "
            "KL-divergence penalty term  β · KL[π_θ || π_ref] ?"
        ),
        "options": [
            "A) It speeds up policy gradient convergence by reducing variance",
            "B) It prevents the fine-tuned policy from drifting too far from the "
               "reference SFT model, avoiding reward hacking and output degradation",
            "C) It measures semantic similarity between generated and reference completions",
            "D) It normalises reward scores to zero mean across each training batch",
        ],
        "correct_answer": (
            "B) It prevents the fine-tuned policy from drifting too far from the "
            "reference SFT model, avoiding reward hacking and output degradation"
        ),
        "explanation": (
            "Without the KL penalty the policy over-optimises the reward model, "
            "producing text that scores high on the RM but is incoherent or degenerate "
            "(reward hacking). The β coefficient is a leash: high β = stays close to "
            "SFT, low β = pursues reward aggressively. InstructGPT used β ≈ 0.02. "
            "Constitutional AI and DPO handle this differently but the principle holds."
        ),
        "remember": (
            "KL penalty = leash on RL fine-tuning. "
            "Stops reward hacking by keeping π_θ close to π_ref. "
            "β controls the trade-off: alignment vs reward maximisation."
        ),
    },
    {
        "type": "coding",
        "difficulty": "hard",
        "topic": "Evaluation Metrics",
        "question": (
            "Implement perplexity from scratch.\n\n"
            "Perplexity = exp( -1/N · Σ log P(token_i) )\n\n"
            "Examples:\n"
            "  perplexity([-0.5, -1.2, -0.8, -2.1, -0.3])  →  ~4.93\n"
            "  perplexity([-0.1, -0.1, -0.1])               →  ~1.105  (near-perfect model)\n"
            "  perplexity([-10, -10, -10])                   →  ~e^10 ≈ 22026 (terrible model)"
        ),
        "language": "python",
        "starter_code": (
            "import math\n"
            "from typing import List\n\n\n"
            "def perplexity(log_probs: List[float]) -> float:\n"
            '    """\n'
            "    Calculate perplexity from per-token log-probabilities (natural log).\n\n"
            "    Args:\n"
            "        log_probs: list of log P(token_i) — must be non-empty, all <= 0\n"
            "    Returns:\n"
            "        Perplexity score (float >= 1; lower is better)\n"
            "    Raises:\n"
            "        ValueError if log_probs is empty\n"
            '    """\n'
            "    pass\n"
        ),
        "correct_answer": (
            "import math\n"
            "from typing import List\n\n\n"
            "def perplexity(log_probs: List[float]) -> float:\n"
            "    if not log_probs:\n"
            "        raise ValueError('log_probs must not be empty')\n"
            "    avg_neg_log_prob = -sum(log_probs) / len(log_probs)\n"
            "    return math.exp(avg_neg_log_prob)\n"
        ),
        "explanation": (
            "Perplexity is the exponent of the average negative log-likelihood per token. "
            "A perplexity of 1 means the model always predicts the next token perfectly; "
            "higher values mean more 'surprise'. GPT-2 achieves ~35 on PTB; GPT-3 ~20; "
            "modern LLMs can go below 10 on in-domain text. It's used to compare language "
            "models on the same test set — lower is strictly better."
        ),
        "remember": (
            "PP = exp(-1/N · Σ log P(t_i)). "
            "Average NLL → exponentiate. "
            "Lower = better. In-domain GPT-4 ≈ single digits. "
            "Doubles when NLL increases by ln(2) ≈ 0.69."
        ),
    },
]
