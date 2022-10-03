# imports
import os
import nltk
import pickle
from nltk import word_tokenize
from nltk.util import ngrams
import math


def compute_prob(text, unigram_dict, bigram_dict, V):
    unigrams_test = word_tokenize(text)
    bigrams_test = list(ngrams(unigrams_test, 2))

    p_laplace = 1

    for bigram in bigrams_test:
        # print(bigram)
        b = bigram_dict[bigram] if bigram in bigram_dict else 0
        u = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0
        p_laplace = p_laplace * ((b + 1) / (u + V))

    # print("log prob is %.5f == %.5f" % (p_log, math.exp(p_log)))
    return p_laplace


if __name__ == '__main__':
    pickle_file_dir = f"{os.getcwd()}/Code/HW4/pickle_files/"

    # read in pickled documents
    with open(f"{pickle_file_dir}english_unigrams.pickle", "rb") as handle:
        english_unigrams = pickle.load(handle)

    with open(f"{pickle_file_dir}english_bigrams.pickle", "rb") as handle:
        english_bigrams = pickle.load(handle)

    with open(f"{pickle_file_dir}french_unigrams.pickle", "rb") as handle:
        french_unigrams = pickle.load(handle)

    with open(f"{pickle_file_dir}french_bigrams.pickle", "rb") as handle:
        french_bigrams = pickle.load(handle)

    with open(f"{pickle_file_dir}italian_unigrams.pickle", "rb") as handle:
        italian_unigrams = pickle.load(handle)

    with open(f"{pickle_file_dir}italian_bigrams.pickle", "rb") as handle:
        italian_bigrams = pickle.load(handle)

    V = len(english_unigrams) + len(french_unigrams) + len(italian_unigrams)

    # break up test document into sentences
    file = open(os.path.join(os.getcwd(), f"Code/HW4/ngram_files/LangId.test"), 'r')
    test_text = file.read()
    test_text = test_text.split('\n')

    # open solution doc
    solutions = open(os.path.join(os.getcwd(), f"Code/HW4/ngram_files/LangId.sol"), 'r')

    wrong_lines = []
    wrong_count = 0

    # loop through sentences and predict the language of each sentence
    for sentence in test_text:
        pred = ""
        en_pr = compute_prob(sentence, english_unigrams, english_bigrams, V)
        fr_pr = compute_prob(sentence, french_unigrams, french_bigrams, V)
        it_pr = compute_prob(sentence, italian_unigrams, italian_bigrams, V)

        # read solution line
        line = solutions.readline().split(" ")

        if max(en_pr, fr_pr, it_pr) == en_pr:
            pred = "English"

        elif max(en_pr, fr_pr, it_pr) == fr_pr:
            pred = "French"

        else:
            pred = "Italian"

        if len(line[0]) > 0 and line[1][:-2] != pred:
            wrong_count += 1
            wrong_lines.append(line[0])
        
    
    print("Accuracy:", (len(test_text) - wrong_count) / len(test_text))
    print("Incorrect lines:")
    for line in wrong_lines:
        print(line)

    # cleanup files
    file.close()
    solutions.close()