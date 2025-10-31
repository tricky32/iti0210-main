import os
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import defaultdict, Counter
import random
import tiktoken  # For subword tokenization

# Download NLTK resources for tokenization
nltk.download("punkt")

# EOS token (end of sentence)
EOS = "<EOS>"

# Tokenize text into words
def tokenize_word(text):
    tokens = []
    for sentence in sent_tokenize(text):
        tokens.append(EOS)  # Add EOS before each sentence
        tokens.extend(word_tokenize(sentence))
    tokens.append(EOS)  # Add EOS at the end
    return tokens

# Tokenize text into characters
def tokenize_char(text):
    tokens = []
    for sentence in sent_tokenize(text):
        tokens.append(EOS)  # Add EOS before each sentence
        tokens.extend(list(sentence))  # Split into characters
    tokens.append(EOS)
    return tokens

# Tokenize text into subwords using GPT-2 tokenizer
def tokenize_subword(text):
    enc = tiktoken.get_encoding("gpt2")
    return [EOS] + enc.encode(text) + [EOS]

# Build n-gram model
def build_ngram_model(tokens, n):
    ngrams = defaultdict(Counter)
    for i in range(len(tokens) - n + 1):
        context = tuple(tokens[i:i + n - 1])  # First (n-1) tokens
        next_token = tokens[i + n - 1]
        ngrams[context][next_token] += 1
    return ngrams

# Generate text using n-gram models with fallback
def generate_text(ngrams_dict, start_tokens, max_length=50, is_subword=False):
    context = tuple(start_tokens[-(len(start_tokens) - 1):])
    generated_tokens = list(start_tokens)

    for _ in range(max_length):
        while context not in ngrams_dict and len(context) > 1:
            context = context[1:]  # Fallback to shorter context
        if context not in ngrams_dict:
            break  # No valid continuation found
        next_token = random.choices(
            list(ngrams_dict[context].keys()),
            weights=ngrams_dict[context].values()
        )[0]
        if next_token == EOS:
            break
        generated_tokens.append(next_token)
        context = tuple(generated_tokens[-(len(context)):])

    if is_subword:
        enc = tiktoken.get_encoding("gpt2")
        return enc.decode([tok for tok in generated_tokens if tok != EOS])
    return " ".join(generated_tokens)

# Example usage
if __name__ == "__main__":
    # Get the current directory and load the text file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "Moby_Dick.txt")
    with open(file_path, encoding="utf-8") as f:
        text = f.read()

    # Tokenize the text
    tokens_word = tokenize_word(text)
    tokens_char = tokenize_char(text)
    tokens_subword = tokenize_subword(text)

    # Build n-gram models for 2, 3, and 4 grams
    bigram_word = build_ngram_model(tokens_word, 2)
    trigram_word = build_ngram_model(tokens_word, 3)
    fourgram_word = build_ngram_model(tokens_word, 4)

    bigram_char = build_ngram_model(tokens_char, 2)
    trigram_char = build_ngram_model(tokens_char, 3)
    fourgram_char = build_ngram_model(tokens_char, 4)

    bigram_subword = build_ngram_model(tokens_subword, 2)
    trigram_subword = build_ngram_model(tokens_subword, 3)
    fourgram_subword = build_ngram_model(tokens_subword, 4)

    # Example starting tokens
    start_tokens_word = ["Call", "me", "Ishmael", ".", "Some", "years", "ago", "never", "mind", "how", "long", "precisely", ".", "Having", "little", "or", "no", "money", "in", "my", "purse", "and", "nothing", "particular", "to"]

    start_tokens_char = ["C", "a", "l", "l", " ", "m", "e", " ", "I", "s", "h", "m", "a", "e", "l", ".", " ", "S", "o", "m", "e", " ", "y", "e", "a", "r", "s", " ", "a", "g", "o", ",", " ", "n", "e", "v", "e", "r", " ", "m", "i", "n", "d", " ", "h", "o", "w", " ", "l", "o", "n", "g", " ", "p", "r", "e", "c", "i", "s", "e", "l", "y", "."]

    enc = tiktoken.get_encoding("gpt2")
    start_tokens_subword = enc.encode("Call me Ishmael. Some years ago, never mind how long precisely.")


    # Generate example sentences for each tokenizer and n-gram size
    print("\n### Word Tokenization ###")
    print("Bigram:", generate_text(bigram_word, start_tokens_word))
    print("Trigram:", generate_text(trigram_word, start_tokens_word))
    print("4-gram:", generate_text(fourgram_word, start_tokens_word))

    print("\n### Character Tokenization ###")
    print("Bigram:", generate_text(bigram_char, start_tokens_char))
    print("Trigram:", generate_text(trigram_char, start_tokens_char))
    print("4-gram:", generate_text(fourgram_char, start_tokens_char))

    print("\n### Subword Tokenization ###")
    print("Bigram:", generate_text(bigram_subword, start_tokens_subword, is_subword=True))
    print("Trigram:", generate_text(trigram_subword, start_tokens_subword, is_subword=True))
    print("4-gram:", generate_text(fourgram_subword, start_tokens_subword, is_subword=True))
