import sys
import os
import re
from scraper import scrape_buffett
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
from gensim import corpora, summarization
from gensim.models.ldamodel import LdaModel
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import datetime
import seaborn as sns
import nltk
from nltk.corpus import stopwords
from collections import Counter
import pprint
import pandas_datareader.data as web
import datetime

r_server = redis.Redis("localhost")
r_server.ping

#scrape_buffett()

def create_dictionary(directory):
    for file in os.listdir(directory):
        if file[0] != ".":
            key = re.findall(r'\d+', file)
            key = int("".join(key))
            text = textract.process(directory + "/" + file)
            r_server.set(key, text)
    return True

#create_dictionary("/Users/ryanneal/Desktop/Warren-Buffett/data/raw")

def create_document(year):
    yearly_report = r_server.get(year)
    return str(yearly_report)

def create_yearly_stems(year):
    data = create_document(year).lower()
    words = nltk.wordpunct_tokenize(data)
    useless_words = stopwords.words("english") + list(string.punctuation)

    def filter_words(words):
        return [word for word in words if not word in useless_words and len(word) > 1 and word.isalpha()]

    def stem(tokens):
        porter = nltk.PorterStemmer()
        return [porter.stem(t) for t in tokens]

    return stem(filter_words(words))

def create_all_stems(years):
    stems = []
    for year in years:
        stems.append(create_yearly_stems(year))
    return stems


def get_yearly_entities(year):
    sentences = nltk.sent_tokenize(create_document(year))
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)

    def extract_entity_names(t):
        entity_names = []

        if hasattr(t, 'label') and t.label:
            if t.label() == 'NE':
                entity_names.append(' '.join([child[0] for child in t]))
            else:
                for child in t:
                    entity_names.extend(extract_entity_names(child))

        return entity_names

    entity_names = []
    for tree in chunked_sentences:
        # Print results per sentence
        # print extract_entity_names(tree)

        entity_names.extend(extract_entity_names(tree))
    return entity_names

def get_all_entities(years):
    entities = []
    for year in years:
        entities.append(get_yearly_entities(year))
    return entities

def count_entities(entities):
    counter = Counter(entities)
    return counter

def count_words(stems):
    word_counter = Counter(stems)
    most_common_words = word_counter.most_common()[:10]
    return most_common_words

def count_all_words(stems):
    dictionary = Counter()
    for stem in stems:
        dictionary.update(stem)
    return dictionary

def count_all_entities(entities):
    dictionary = Counter()
    for entity in entities:
        counter = Counter(entity)
        dictionary += counter
    return dictionary

#print(len(count_all_words(create_all_stems(range(1977, 2017)))))