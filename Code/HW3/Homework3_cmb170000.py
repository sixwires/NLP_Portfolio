# imports
import os
import random
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def tokenize_text_file(filename):
    file = open(os.path.join(os.getcwd(), f"Code/HW3/{filename}"), 'r')
    text = file.read()

    return [t.lower() for t in nltk.word_tokenize(text) if t.isalpha() and t not in stopwords.words('english') and len(t) > 5]
    # return tokens


def preprocess_tokens(tokens):
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in tokens]
    unique_lemmas = set(lemmas)

    tags = nltk.pos_tag(unique_lemmas)

    # create list of nouns
    # TODO: edit to make it only store nouns
    nouns_list = []
    for token, pos in tags:
        if pos == "NN":
            nouns_list.append(token)

    print("Number of nouns:", len(nouns_list))
    print("\nFirst 20 unique lemmas with POS:")
    print(tags[-20:])

    return nouns_list


def get_lexical_diversity(tokens):
    print("Removing stopwords, and words less than length 5")
    print("Number of tokens in text:", len(tokens))
    print("Number of unique tokens in text:", len(set(tokens)))
    print("Lexical diversity:",
          f"{round((len(set(tokens)) / len(tokens)) * 100)}%")
    return


def run_game(nouns):
    score = 5
    in_letter = ""
    display_word = ""

    word = random.choice(nouns)

    for i in range(len(word)):
        display_word += "_"

    print("\nLet's play a word guessing game!")

    while score > 0 and in_letter != "!":
        correct = False

        print(display_word)
        in_letter = input("Enter a letter: ")

        for i in range(len(word)):
            if word[i] == in_letter:
                correct = True
                display_word = display_word[:i] + in_letter + display_word[i + 1:]
                score += 1

        if correct:
            print("Right!")
        else:
            print("Sorry, guess again.")
            score -= 1

        # check for correct word
        if display_word.lower() == word:
            print("You solved it!")
            word = random.choice(nouns)
            for i in range(len(word)):
                display_word += "_"

        print("Your current score is", score)


# main code
if __name__ == '__main__':
    tokens = tokenize_text_file("anat19.txt")

    get_lexical_diversity(tokens)

    nouns = preprocess_tokens(tokens)

    run_game(nouns)
