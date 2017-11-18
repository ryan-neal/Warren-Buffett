from datetime import date
import pandas as pd
from pandas_datareader import DataReader as dr
import sys
import os
import re
import json
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import textract
import string
import spacy
import redis
import itertools as it
import urllib3
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import datetime
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

def generate_expression(key):
	# TODO: Make constant
	EXPRESSIONS = {
		'noun in noun':'{<NN|NNS|NNP|NNPS><IN>*<NN|NNS|NNP|NNPS>+}',
		'adjective_noun_noun':'{<JJ>*<NN|NNS|NNP|NNPS><CC>*<NN|NNS|NNP|NNPS>+}',
		'adjective_noun':'{<JJ>*<NN|NNS|NNP|NNPS>+}',
		'passive_voice':'{<VB|VBD><VBN>+}'
	}
	# TODO: Refactor passive voice
	return EXPRESSIONS[key.lower()]


def get_phrases(document_text, expressions):
    """ Chunk phrases based on input parameters. Return list of tuples
            in the format (phrase, containing sentence).
        """

    new_patterns = 'Phrases: ' + '\n'.join(expressions)
    chunker = nltk.RegexpParser(new_patterns)

    tagged_words = get_tags(document_text)
    word_tree = [chunker.parse(word) for word in tagged_words]  # Identify NP chunks
    phrases = []

    for sent in word_tree:
        sentence = ' '.join(word for word, tag in sent.leaves())
        for subtree in sent.subtrees():
            if subtree.label() == 'Phrases':
                phrase = ' '.join(word for word, tag in subtree.leaves())
                phrases.append((phrase, sentence))

    return phrases


def main():
    #print(get_entities(create_document(1999), 'person'))
    #print(get_tags(create_document(1999)))
    print(get_noun_phrases(create_document(1999)))
    #print(get_stems(create_document(1999)))
    #x = freq_words(create_document(1999))
    #for key, value in x.items():
    #    print(key, value)


if __name__ == '__main__':
	main()