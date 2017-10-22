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
from gensim.parsing.preprocessing import STOPWORDS
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import datetime
import seaborn as sns
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from collections import Counter
import pprint
import pandas_datareader.data as web
import datetime

nlp = spacy.load('en')

r_server = redis.Redis("localhost")
r_server.ping

scrape_buffett()

def create_dictionary(directory):
    for file in os.listdir(directory):
        if file[0] != ".":
            key = re.findall(r'\d+', file)
            key = int("".join(key))
            text = textract.process(directory + "/" + file)
            r_server.set(key, text)
    return True

def get_year(key):
    yearly_report = r_server.get(key)
    return str(yearly_report)

#create_dictionary("/Users/ryanneal/Desktop/Warren-Buffett/data/raw")
Ninety_83 = get_year(1983).lower()
test = nltk.word_tokenize(Ninety_83)

useless_words = nltk.corpus.stopwords.words("english") + list(string.punctuation) + list("--") + list("...")

def build_bag_of_words_features_filtered(words):
    return {
        word:1 for word in words \
        if not word in useless_words}

def filter_words(words):
    return [word for word in words if not word in useless_words]

def stem(tokens):
    porter = nltk.PorterStemmer()
    return [porter.stem(t) for t in tokens]

print(stem(filter_words(test)))

word_counter = Counter(stem(filter_words(test)))
most_common_words = word_counter.most_common()[:10]
print(most_common_words)