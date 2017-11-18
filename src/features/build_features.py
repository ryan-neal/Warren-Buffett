from datetime import date
from pandas_datareader import DataReader as dr
import pandas as pd
import numpy as np
import string
import itertools as it
import seaborn as sns
import nltk
from nltk.corpus import stopwords
from collections import Counter

import pymongo

client = pymongo.MongoClient()
db = client['BerkshireHathaway']['reports']


def create_document(year):
    """ Given a year, query MongoDB for the corresponding report """
    return db.find_one({'year':str(year)})['text'].decode('utf-8')

USELESS_WORDS = stopwords.words("english") + list(string.punctuation)

def significant_word(word):
    return word not in USELESS_WORDS and len(word) > 1

def get_stems(document_text):
    """ Given the raw text of a document, return list of all unique stems """

    def stem(tokens):
        porter = nltk.PorterStemmer()
        return [porter.stem(t) for t in tokens]

    data = document_text.lower()
    words = nltk.word_tokenize(data)
    return stem(filter(significant_word, words))


def get_entities(document_text, entity_type=None):
    """ Given the raw text of a document, returns all named entities as a
        list of tuples in the form of (NE type, entity_name)
     """

    def chunk(text):
        return nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(text)))

    chunked_document = chunk(document_text)
    entity_trees = filter(lambda word: type(word) is not tuple, chunked_document)
    entity_names = [(word.label(), ' '.join([child[0] for child in word]))
                    for word in entity_trees]
	
	# Optional: Filter entities based on type
    if entity_type:
    	return [e for e in entity_names if e[0].lower() == entity_type.lower()]
    
    return entity_names

def get_word_count(document_text):
    word_token = nltk.word_tokenize(document_text)
    word_token = [word for word in word_token if word.isalpha()]
    return (len(word_token))

def get_average_word_length(document_text):
    words = nltk.word_tokenize(document_text)
    filtered_words = list(filter(lambda word: word.isalpha(), words))
    return len(''.join(filtered_words)) / len(filtered_words)
    
def get_sentence_count(document_text):
	return len(nltk.sent_tokenize(document_text))

def get_market_returns():
    '''Getting Berkshire & SP 500 returns'''
    start_date = date(1979, 12, 31)
    end_date = date(2016, 12, 31)
    y_bk = dr('BRK-A', 'yahoo', start=start_date)
    y_bk = y_bk['Adj Close']
    y_sp = dr('^SP500TR', 'yahoo', start=start_date) #TODO: Get longer backfill
    y_sp = y_sp['Adj Close']
    ts = pd.concat([y_bk, y_sp], axis=1)
    ts.columns.values[0] = 'BRK-A'
    ts.columns.values[1] = 'SP500TR'
    dates_ann = pd.date_range(start_date, end_date, freq='A')
    ts_annualret = ts.reindex(dates_ann, method='ffill').pct_change()
    ts_annualret.pct_change()

    return ts_annualret

def get_good_years():
    df = get_market_returns()
    df.index = df.index.strftime('%Y')
    good_years = df[df["BRK-A"] > 0]
    arr = np.array(good_years.index)
    inter = lambda x: (int(x) -1 )
    funct = np.vectorize(inter)
    return (funct(arr))

def get_good():
    return_list = []
    for year in get_good_years():
        doc = create_document(year)
        return_list.append(get_noun_phrases(doc))
    return list(it.chain.from_iterable(return_list))

def get_bad():
    return_list = []
    for year in get_bad_years():
        doc = create_document(year)
        return_list.append(get_noun_phrases(doc))
    return list(it.chain.from_iterable(return_list))

def get_bad_years():
    df = get_market_returns()
    df.index = df.index.strftime('%Y')
    bad_years = df[df["BRK-A"] <= 0]
    arr = np.array(bad_years.index)
    inter = lambda x: (int(x) -1 )
    funct = np.vectorize(inter)
    return (funct(arr))

def freq_words(document_text):
    freqdist = nltk.FreqDist()

    for word in nltk.word_tokenize(document_text):
        if significant_word(word):
            freqdist[word.lower()] += 1
    return freqdist

def get_tags(document_text):
    tokenized_sentence = nltk.sent_tokenize(document_text)
    tokenized_words = [nltk.word_tokenize(sentence) for sentence in tokenized_sentence]
    tagged_words = [nltk.pos_tag(word) for word in tokenized_words]
    return tagged_words

def get_noun_phrases(document_text):
    tagged_words = get_tags(document_text)
    new_patterns = """
        NP:    {<NN|NNS|NNP|NNPS><IN>*<NN|NNS|NNP|NNPS>+}
               {<JJ>*<NN|NNS|NNP|NNPS><CC>*<NN|NNS|NNP|NNPS>+}
               {<JJ>*<NN|NNS|NNP|NNPS>+}

        """
    chunker = nltk.RegexpParser(new_patterns)
    word_tree = [chunker.parse(word) for word in tagged_words]  # Identify NP chunks
    nps = []
    for sent in word_tree:
        tree = chunker.parse(sent)
        for subtree in tree.subtrees():
            if subtree.label() == 'NP':
                t = subtree
                t = ' '.join(word for word, tag in t.leaves())
                nps.append(t)
    return nps

def main():
    #print(get_entities(create_document(1999), 'person'))
    #print(get_tags(create_document(1999)))
    #print(get_noun_phrases(create_document(1979)))
    print(get_market_returns())
    #print(get_good_years())
    #print(get_bad_years())
    #goods = set(get_good())
    #bads = set(get_bad())
    #good_set = goods - bads
    #bad_set = bads-goods
    #print(good_set)
    #print(bad_set)



if __name__ == '__main__':
	main()