# imports
import os
import nltk
import pickle
from nltk import word_tokenize
from nltk.util import ngrams


def get_n_gram(filename):
    # read in file and split into unigrams and bigrams
    file = open(os.path.join(
        os.getcwd(), f"Code/HW4/ngram_files/{filename}"), 'r')
    text = file.read()

    # initialize unigrams and bigrams
    unigrams = word_tokenize(text.lower())
    bigrams = list(ngrams(unigrams, 2))

    bigram_dict = {}
    # loop through and make bigram count list
    for bigram in bigrams:
        temp = f"{bigram[0]} {bigram[1]}"
        if(bigram in bigram_dict):
            bigram_dict[bigram] += 1
        else:
            bigram_dict[bigram] = 1

    unigram_dict = {}
    # loop through and make unigram count list
    for unigram in unigrams:
        if(unigram in unigram_dict):
            unigram_dict[unigram] += 1
        else:
            unigram_dict[unigram] = 1

    return unigram_dict, bigram_dict


# main code
if __name__ == '__main__':
    english_unigrams, english_bigrams = get_n_gram("LangId.train.English")
    french_unigrams, french_bigrams = get_n_gram("LangId.train.French")
    italian_unigrams, italian_bigrams = get_n_gram("LangId.train.Italian")

    # write to pickle file
    with open('english_unigrams.pickle', 'wb') as handle:
        pickle.dump(english_unigrams, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('english_bigrams.pickle', 'wb') as handle:
        pickle.dump(english_bigrams, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('french_unigrams.pickle', 'wb') as handle:
        pickle.dump(french_unigrams, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('french_bigrams.pickle', 'wb') as handle:
        pickle.dump(french_bigrams, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('italian_unigrams.pickle', 'wb') as handle:
        pickle.dump(italian_unigrams, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('italian_bigrams.pickle', 'wb') as handle:
        pickle.dump(italian_bigrams, handle, protocol=pickle.HIGHEST_PROTOCOL)
