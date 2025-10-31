import csv
from collections import Counter, defaultdict
import math

# Read and preprocess training data
train_data = []
genre_article_counts = Counter()  # To count articles per genre
word_counts_per_genre = defaultdict(Counter)  # To count word frequencies per genre
total_word_count_per_genre = Counter()  # To count total words per genre
vocabulary = set()

# Read training data
with open("bbc_train.csv", encoding="utf-8") as f:
    rd = csv.reader(f)
    for genre, text in rd:
        words = [w.lower() for w in text.split() if len(w) > 3]
        train_data.append((genre, words))
        genre_article_counts[genre] += 1
        word_counts_per_genre[genre].update(words)
        total_word_count_per_genre[genre] += len(words)
        vocabulary.update(words)

# Total number of articles and vocabulary size
total_articles = sum(genre_article_counts.values())
vocab_size = len(vocabulary)

# Probability of each genre
genre_probs = {genre: count / total_articles for genre, count in genre_article_counts.items()}

# Implement Naive Bayes classifier
def predict_genre(article):
    words = [w.lower() for w in article.split() if len(w) > 3]
    log_probs = {}
    
    for genre in genre_probs:
        # Start with the log of the prior probability of the genre
        log_prob = math.log(genre_probs[genre])
        
        for word in words:
            # Calculate P(w|c) with Laplace smoothing
            word_count = word_counts_per_genre[genre][word]
            word_prob = (word_count + 1) / (total_word_count_per_genre[genre] + vocab_size)
            log_prob += math.log(word_prob)
        
        log_probs[genre] = log_prob

    return max(log_probs, key=log_probs.get)

# Count correctly classified articles
count_of_articles = 0
count_of_correctly_guessed_articles = 0

# Read and classify test data
with open("bbc_test.csv", encoding="utf-8") as f:
    rd = csv.reader(f)
    for topic, text in rd:
        predicted_genre = predict_genre(text)
        print(f"Article topic: {topic}, Predicted genre: {predicted_genre}")
        count_of_articles += 1
        if topic == predicted_genre:
            count_of_correctly_guessed_articles += 1

print(f"Correctly guessed {count_of_correctly_guessed_articles} out of {count_of_articles}")
