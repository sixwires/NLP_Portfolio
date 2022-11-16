import os
from bs4 import BeautifulSoup
import requests
import urllib.request
import re
import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import pickle
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('stopwords')

WIKI_LINK = 'https://en.wikipedia.org'
STARTING_LINK = 'https://en.wikipedia.org/wiki/New_York_City'
KEYWORD = 'York'
CORPUS_STOPWORDS = ['pdf', 'isbn', 'also', 'one']
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

def crawl(starter_url, keyword):
    r = requests.get(starter_url)
    max_link_cnt = 15
    links = []

    data = r.text
    soup = BeautifulSoup(data, 'lxml')

    counter = 0

    # write urls found to url.txt
    for link in soup.find_all('a'):
        link_str = str(link.get('href'))

        if keyword in link_str or keyword.lower() in link_str:
            if link_str.startswith('/url?q='):
                link_str = link_str[7:]
                print('MOD:', link_str)

            if '&' in link_str:
                i = link_str.find('&')
                link_str = link_str[:i]

            if link_str.startswith('http') and 'google' not in link_str:
                links.append(link_str)
                counter += 1

        if counter > max_link_cnt:
            break

    return links


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True


def scrape_text(url, count):
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'lxml')
    data = soup.findAll(text=True)
    result = filter(visible, data)
    temp_list = list(result)      # list from filter
    temp_str = ' '.join(temp_list)

    with open(f'url{count}.txt', 'w') as f:
        f.write(temp_str)

    return f'url{count}.txt'


def clean_file(filename):

    with open(filename, 'r') as file:
        data = file.read().replace('\n', '')
        data = data.replace('\t', '')
        text_chunks = [chunk for chunk in data.splitlines()
                       if not re.match(r'^\s*$', chunk)]

    # remove the unclean file
    os.remove(filename)

    text = ' '.join(text_chunks)
    with open(filename, 'w') as f:
        f.write(text)

    return text.lower()


def tokenize_file_unigram(filename):
    with open(filename, 'r') as f:
        text = f.read()
        tokens = [t.lower() for t in nltk.word_tokenize(
            text) if t.isalpha() and t not in stopwords.words('english') and t not in CORPUS_STOPWORDS and t not in MONTHS]
        return tokens


def count_tokens(tokens):
    token_dict = {}

    for token in tokens:
        if(token in token_dict):
            token_dict[token] += 1
        else:
            token_dict[token] = 1

    return token_dict


def get_top_terms(terms_dict):
    return {k: v for k, v in sorted(terms_dict.items(), key=lambda item: item[1])}


def tokenize_file_sentence(filename):
    with open(filename, 'r') as f:
        text = f.read()
        sentences = sent_tokenize(text)

    with open(f'{filename[:-4]}.pickle', 'wb') as f:
        pickle.dump(sentences, f)

    return sentences


# main code
if __name__ == '__main__':
    links = crawl(STARTING_LINK, KEYWORD)
    print(links)
    count = 0
    tokens = []  # individual tokens from all visited sites
    coropora = []  # tokenized sentences

    for link in links:
        filename = scrape_text(link, count)
        count += 1
        tokens += tokenize_file_unigram(filename)
        coropora += tokenize_file_sentence(filename)

    unigram_counts = get_top_terms(count_tokens(tokens))

    # output top terms and chosen terms
    print("Top terms:\n")
    for token in list(unigram_counts)[-50:]:
        if token not in stopwords.words('english'):
            print(token, '\t', unigram_counts[token])

    print("Top terms chosen:")
    chosen_tokens = ['new', 'york', 'city', 'manhattan', 'park', 'united', 'island', 'center', 'american', 'brooklyn']
    for token in chosen_tokens:
        print(token)
