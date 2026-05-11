# Tokenization is the process of breaking text into small pieces called "tokens".
# LLMs (Large Language Models) like GPT and Claude don't read words — they read tokens.
# Understanding tokens helps you understand how AI language models actually work.

# =============================================================================
# WHAT IS A TOKEN?
# =============================================================================
#
# A token is a chunk of text — it could be:
#   - A whole word:       "hello"
#   - A word piece:       "un" + "believ" + "able"
#   - Punctuation:        ".", "?", "!"
#   - A number:           "42"
#   - A space + word:     " the" (leading space is part of the token)
#
# LLMs use "subword tokenization" — they break uncommon words into smaller pieces,
# so they never encounter a completely unknown word.
#
# Rule of thumb: 1 token ≈ 4 characters ≈ 0.75 words (in English)
#
# Example tokens (approximate, using GPT-style tokenization):
#   "Hello, world!"      → ["Hello", ",", " world", "!"]           (4 tokens)
#   "tokenization"       → ["token", "ization"]                     (2 tokens)
#   "ChatGPT"            → ["Chat", "G", "PT"]                      (3 tokens)
#   "2024"               → ["2024"]                                  (1 token)
#   "antidisestablishment" → ["anti", "dis", "establishment"]        (3 tokens)

# =============================================================================
# WHY DOES THIS MATTER?
# =============================================================================
#
# 1. Context window:
#    LLMs can only process a limited number of tokens at once.
#    GPT-4 has a 128k token context. Claude has up to 200k tokens.
#    If your document is too long (in tokens), the model can't read all of it.
#
# 2. Pricing:
#    AI API pricing is per token. Fewer tokens = cheaper calls.
#
# 3. Reasoning:
#    The model predicts the NEXT TOKEN, one at a time.
#    It doesn't "understand" words the way humans do — it
#    predicts likely continuations based on patterns in training data.
#
# 4. Non-English text uses MORE tokens per word than English.
#    "Hello" = 1 token, but "مرحبا" (Arabic: hello) may be 3-4 tokens.

# =============================================================================
# SIMPLE WORD TOKENIZER (built from scratch)
# =============================================================================

import re
import string

def simple_word_tokenizer(text):
    """
    Split text into words and punctuation.
    This is a simplified version — real LLM tokenizers are much more complex.
    """
    # Split on whitespace and keep punctuation as separate tokens
    tokens = re.findall(r"\w+|[^\w\s]", text)
    return tokens

def character_tokenizer(text):
    """
    Simplest possible tokenizer: split into individual characters.
    Early models used this approach.
    """
    return list(text)

def subword_demo_tokenizer(word):
    """
    Simulate subword tokenization by splitting long words at common boundaries.
    Real tokenizers (BPE, WordPiece) learn these splits from training data.
    """
    # Simplified: split compound words at common prefixes/suffixes
    prefixes = ["un", "re", "pre", "anti", "dis", "non", "over", "under"]
    suffixes = ["ing", "tion", "ation", "ness", "ful", "less", "able", "ible", "ly"]

    word_lower = word.lower()
    for prefix in prefixes:
        if word_lower.startswith(prefix) and len(word) > len(prefix) + 3:
            rest = word[len(prefix):]
            return [word[:len(prefix)], rest]

    for suffix in suffixes:
        if word_lower.endswith(suffix) and len(word) > len(suffix) + 3:
            base = word[:-len(suffix)]
            return [base, suffix]

    return [word]   # can't split further

def estimate_tokens(text):
    """
    Rough estimate of token count (GPT-style).
    Real count requires the actual tokenizer (tiktoken library).
    """
    return max(1, len(text) // 4)

def build_vocab(texts):
    """
    Build a simple word-level vocabulary (word → index mapping).
    Real LLM vocabularies have ~50,000-100,000 subword tokens.
    """
    vocab = {"<PAD>": 0, "<UNK>": 1, "<START>": 2, "<END>": 3}
    for text in texts:
        for word in simple_word_tokenizer(text.lower()):
            if word not in vocab:
                vocab[word] = len(vocab)
    return vocab

def encode(text, vocab):
    """Convert text to a list of integer token IDs."""
    tokens = simple_word_tokenizer(text.lower())
    return [vocab.get(token, vocab["<UNK>"]) for token in tokens]

def decode(ids, vocab):
    """Convert a list of token IDs back to text."""
    id_to_word = {v: k for k, v in vocab.items()}   # reverse the dictionary
    return " ".join(id_to_word.get(i, "<UNK>") for i in ids)

if __name__ == "__main__":
    print("=== Tokenization Basics ===\n")

    # --- Word tokenization ---
    sample = "Hello, world! Tokenization is how LLMs read text."
    tokens = simple_word_tokenizer(sample)
    print(f"Original: {sample}")
    print(f"Tokens:   {tokens}")
    print(f"Count:    {len(tokens)} tokens\n")

    # --- Subword tokenization simulation ---
    print("--- Subword Tokenization (simplified demo) ---")
    words_to_split = ["unhappy", "tokenization", "preprocessing", "reading", "antidote"]
    for word in words_to_split:
        parts = subword_demo_tokenizer(word)
        print(f"  '{word}' → {parts}")

    # --- Token estimation ---
    print("\n--- Token Count Estimates ---")
    texts = [
        "Hello!",
        "The quick brown fox jumps over the lazy dog.",
        "Artificial intelligence is transforming the world.",
        "A" * 100,
    ]
    for t in texts:
        est = estimate_tokens(t)
        print(f"  {repr(t[:50]):<55} ≈ {est} tokens")

    # --- Vocabulary and encoding ---
    print("\n--- Vocabulary and Encoding ---")
    corpus = [
        "the cat sat on the mat",
        "the dog ran in the park",
        "cats and dogs are friends",
    ]
    vocab = build_vocab(corpus)
    print(f"Vocabulary size: {len(vocab)} unique tokens")
    print(f"Sample vocab entries: { {k: v for k, v in list(vocab.items())[:10]} }")

    sentence = "the cat ran"
    encoded = encode(sentence, vocab)
    decoded = decode(encoded, vocab)
    print(f"\nEncode '{sentence}' → {encoded}")
    print(f"Decode {encoded} → '{decoded}'")

    # --- How LLMs use tokens ---
    print("""
--- How LLMs Think in Tokens ---

LLMs work by:
  1. Tokenizing your input (text → token IDs)
  2. Processing those IDs through many layers of attention
  3. Predicting the MOST LIKELY next token (not word — token!)
  4. Repeating step 3 until done (one token at a time)

Example:
  Input:   "The capital of France is"
  Tokens:  [464, 3139, 286, 4881, 318]   (approx. GPT-2 IDs)

  The model predicts:
    " Paris" with probability 0.98
    " Lyon"  with probability 0.01
    " Rome"  with probability 0.005
    ...

  → It outputs " Paris" (highest probability)
  → Then predicts the token AFTER that, and so on.

This is called "autoregressive generation" — each new token
depends on ALL previous tokens in the context.
""")
