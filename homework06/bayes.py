import typing as tp
import string
import math
from collections import defaultdict, Counter
from math import log
from statistics import mean


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator).lower()


class NaiveBayesClassifier:
    def __init__(self, alpha_smoothing=1):
        self.alpha_smoothing = alpha_smoothing

    def fit(self, marked_data: tp.List[str], marks: tp.List[str]):
        words_by_class_frequency: tp.Dict[str, [tp.Dict[str, int]]] = {}

        for mark in set(marks):
            words_by_class_frequency[mark] = defaultdict(int)
            clean

        all_words = set()

        class_probability = dict.fromkeys(set(marks), list())
        for key in class_probability:
            class_probability[key] = [0, 0]

        for i in range(len(marked_data)):
            current_mark = marks[i]
            class_probability[current_mark][0] += 1
            words = Counter(clean(marked_data[i]).split())
            for word in words:
                all_words.add(word)
                words_by_class_frequency[current_mark][word] += words[word]
                class_probability[current_mark][1] += 1

        all_words_count = len(all_words)

        for key in class_probability:
            class_probability[key][0] = class_probability[key][0] / len(marked_data)
            class_probability[key][1] = (
                len(set(words_by_class_frequency[key].keys)) + self.alpha_smoothing * all_words_count
            )

        for key in words_by_class_frequency:
            for word in words_by_class_frequency[key]:
                words_by_class_frequency[key][word] = (
                    words_by_class_frequency[key][word] + self.alpha_smoothing
                ) / class_probability[key][1]

    def predict(self, X):
        """Perform classification on an array of test vectors X."""
        pass

    def score(self, X_test, y_test):
        """Returns the mean accuracy on the given test data and labels."""
        pass


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

    test = NaiveBayesClassifier(0)
    test.fit(test_data, test_answ)
# посчитать кол-во новостей в каждом классе
# собрать заголовки по классам, разобрать на слова (и пары???)
# формула
#
#
