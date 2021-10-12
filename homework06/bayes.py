"""Naive Bayes Classifier"""

import string
import typing as tp
from collections import Counter, defaultdict
from math import log
from statistics import mean


def clean(string_to_clean: str) -> str:
    """Cleans string from punctuation, lower all letters
    >> clean("I LoVe Python!!1")
    'i love python1'
    >> clean("$#*I,^ wAnt sle%%ep")
    'i want sleep'
    """
    translator = str.maketrans("", "", string.punctuation)
    return string_to_clean.translate(translator).lower()


class NaiveBayesClassifier:
    """Classify text data by word frequency in given classes"""

    def __init__(self, alpha_smoothing: float = 1e-5):
        self.alpha_smoothing = alpha_smoothing
        self.word_probabilities: tp.Dict[str, [tp.Dict[str, float]]] = {}  # type: ignore
        self.class_probability: tp.Dict[str, float]
        self.default_class_value: tp.Dict[str, float] = {}

    def fit(self, marked_data: tp.List[str], marks: tp.List[str]) -> None:
        """Study on marked data, count words and classes probabilities. Based on Bayes Theorem."""
        for mark in set(marks):
            self.word_probabilities[mark] = defaultdict(int)
        n_words_in_class: tp.Dict[str, int] = dict.fromkeys(set(marks), 0)
        self.class_probability = dict.fromkeys(set(marks), 0)

        all_words = set()

        for i, mark in enumerate(marks):
            self.class_probability[mark] += 1
            words: tp.Dict[str, int] = Counter(clean(marked_data[i]).split())
            for word in words:
                all_words.add(word)
                self.word_probabilities[mark][word] += words[word]
                n_words_in_class[mark] += 1

        all_words_count = len(all_words)

        for key in n_words_in_class:
            self.class_probability[key] = self.class_probability[key] / len(marks)
            nc_ad = n_words_in_class[key] + self.alpha_smoothing * all_words_count
            self.default_class_value[key] = self.alpha_smoothing / nc_ad
            for word in self.word_probabilities[key]:
                self.word_probabilities[key][word] = (
                    self.word_probabilities[key][word] + self.alpha_smoothing
                ) / nc_ad

    def predict(self, unmarked_data: tp.List[str]) -> tp.List[str]:
        """Predict classes for unmarked data, returns list of classes"""
        predicted_classes: tp.List[str] = []
        for row in unmarked_data:
            highest_probability = -2147483648.0
            likely_class = ""
            words: tp.Dict[str, int] = Counter(clean(row).split())
            for key in self.class_probability:
                current_probability = log(self.class_probability[key])
                for word in words:
                    probability = self.word_probabilities[key][word]
                    if probability == 0:
                        probability = self.default_class_value[key]
                    current_probability += log(probability)
                if current_probability > highest_probability:
                    highest_probability = current_probability
                    likely_class = key
            predicted_classes.append(likely_class)
        return predicted_classes

    def score(self, data: tp.List[str], data_classes: tp.List[str]) -> float:
        """Compare predicted classes with real classes on marked data,
        returns percent of correct answers"""
        correct = len(data_classes)
        classifier_results = self.predict(data)
        for i, real_class in enumerate(data_classes):
            if classifier_results[i] != real_class:
                correct -= 1
        return correct / len(data_classes)


if __name__ == "__main__":
    test_data = [
        "I love this sandwich",
        "This is an amazing place",
        "I feel very good about these beers",
        "This is my best work",
        "What an awesome view",
        "I do not like this restaurant",
        "I am tired of this stuff",
        "I can't deal with this",
        "He is my sworn enemy",
        "My boss is horrible",
    ]
    test_answ = [
        "Positive",
        "Positive",
        "Positive",
        "Positive",
        "Positive",
        "Negative",
        "Negative",
        "Negative",
        "Negative",
        "Negative",
    ]

    test = NaiveBayesClassifier()
    test.fit(test_data, test_answ)
    test_to_predict = [
        "The beer was good",
        "I do not enjoy my job",
        "I ain't feeling dandy today",
        "I feel amazing",
        "Gary is a friend of mine",
        "I can't believe I'm doing this",
    ]

    correct_ans = [
        "Positive",
        "Negative",
        "Negative",
        "Positive",
        "Positive",
        "Negative",
    ]
