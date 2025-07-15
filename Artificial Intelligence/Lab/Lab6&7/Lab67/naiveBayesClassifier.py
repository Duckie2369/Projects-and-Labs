import sys
import pandas as pd
import numpy as np

class NaiveBayesFilter:
    def __init__(self):
        # Initialize class attributes
        self.data = None  # Stores the word count DataFrame
        self.vocabulary = set()  # Set of unique words across all messages
        self.p_spam = 0  # Prior probability of spam
        self.p_ham = 0  # Prior probability of ham
        self.parameters_spam = {}  # Word probabilities for spam messages
        self.parameters_ham = {}  # Word probabilities for ham messages

    def fit(self, X, y):
        # Check if X is tokenized (list of lists) or not (strings)
        if isinstance(X.iloc[0], list):
            # Assume X is already tokenized
            tokenized_messages = X
        else:
            # Tokenize messages
            tokenized_messages = X.apply(lambda msg: msg.split())

        # Initialize vocabulary
        for message in tokenized_messages:
            self.vocabulary.update(message)
        self.vocabulary = sorted(self.vocabulary)  # Convert to sorted list

        # Create a DataFrame to store word counts
        word_count_data = pd.DataFrame(0, index=range(len(X)), columns=self.vocabulary)
        word_count_data['Label'] = y

        # Populate word counts in the DataFrame
        for i, message in enumerate(tokenized_messages):
            for word in message:
                if word in self.vocabulary:
                    word_count_data.at[i, word] += 1

        # Save the word count DataFrame
        self.data = word_count_data

        # Calculate the prior probabilities
        self.p_spam = (y == 'spam').mean()
        self.p_ham = 1 - self.p_spam

        # Split data into spam and ham messages
        spam_data = word_count_data[word_count_data['Label'] == 'spam']
        ham_data = word_count_data[word_count_data['Label'] == 'ham']

        # Calculate word probabilities for spam and ham
        total_spam_words = spam_data[self.vocabulary].sum().sum()
        total_ham_words = ham_data[self.vocabulary].sum().sum()

        for word in self.vocabulary:
            self.parameters_spam[word] = (spam_data[word].sum() + 1) / (total_spam_words + len(self.vocabulary))
            self.parameters_ham[word] = (ham_data[word].sum() + 1) / (total_ham_words + len(self.vocabulary))

        return self.data, self.vocabulary, self.p_spam, self.p_ham, self.parameters_spam, self.parameters_ham


    def predict(self, X):
        labels = []
        for message in X:
            # If the input is already tokenized (list of words), use it directly
            if isinstance(message, list):
                words = message
            else:
                # Otherwise, tokenize the message
                words = message.split()

            # Calculate log probabilities to avoid underflow
            log_p_ham = np.log(self.p_ham)
            log_p_spam = np.log(self.p_spam)

            for word in words:
                if word in self.vocabulary:
                    log_p_ham += np.log(self.parameters_ham.get(word, 1))
                    log_p_spam += np.log(self.parameters_spam.get(word, 1))

            # Compare the posterior probabilities and assign the label
            if log_p_spam > log_p_ham:
                labels.append("spam")
            else:
                labels.append("ham")
        return labels

    def predict_proba(self, X):
        proba = []

        for message in X:
            # If the input is already tokenized (list of words), use it directly
            if isinstance(message, list):
                words = message
            else:
                # Otherwise, tokenize the message
                words = message.split()

            # Calculate log probabilities to avoid underflow
            log_p_ham = np.log(self.p_ham)
            log_p_spam = np.log(self.p_spam)

            for word in words:
                if word in self.vocabulary:
                    log_p_ham += np.log(self.parameters_ham.get(word, 1))
                    log_p_spam += np.log(self.parameters_spam.get(word, 1))

            # Convert log probabilities back to probabilities
            p_ham = np.exp(log_p_ham)
            p_spam = np.exp(log_p_spam)

            # Normalize probabilities
            total = p_ham + p_spam
            if total == 0:
                total += 1e-10  # Prevent division by zero
            p_ham /= total
            p_spam /= total

            proba.append((p_ham, p_spam))

        return proba


    def score(self, true_labels, predicted_labels):
        # Ensure inputs are of the same length
        assert len(true_labels) == len(predicted_labels), "Mismatched input lengths."

        # Count true positives and false negatives
        true_positives = 0
        false_negatives = 0

        for true, pred in zip(true_labels, predicted_labels):
            if true == "spam":
                if pred == "spam":
                    true_positives += 1
                else:
                    false_negatives += 1

        # Handle case where there are no true positives or false negatives
        if true_positives + false_negatives == 0:
            return 0.0  # Avoid division by zero, return recall as 0

        # Calculate recall
        recall = true_positives / (true_positives + false_negatives)
        return recall