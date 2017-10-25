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

def create_stems(year):
    def get_year(year):
        yearly_report = r_server.get(year)
        return str(yearly_report)

    data = get_year(year).lower()
    words = nltk.wordpunct_tokenize(data)
    useless_words = nltk.corpus.stopwords.words("english") + list(string.punctuation)

    def filter_words(words):
        return [word for word in words if not word in useless_words and len(word) > 1 and word.isalpha()]

    def stem(tokens):
        porter = nltk.PorterStemmer()
        return [porter.stem(t) for t in tokens]

    return stem(filter_words(words))


def count_words(stems):
    word_counter = Counter(stems)
    most_common_words = word_counter.most_common()[:10]
    return most_common_words

print(count_words(create_stems(1989)))