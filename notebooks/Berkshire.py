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
from nltk.corpus import stopwords
from collections import Counter
import pprint

r_server = redis.Redis("localhost")
r_server.ping

### SETUP CODE: TO MOVE ###

def create_dictionary(directory):
    for file in os.listdir(directory):
        if file[0] != ".":
            key = re.findall(r'\d+', file)
            key = int("".join(key))
            text = textract.process(directory + "/" + file)
            r_server.set(key, text)
    return True
    
#scrape_buffett()
#create_dictionary("/Users/ryanneal/Desktop/Warren-Buffett/data/raw")

### END SETUP CODE ###

USELESS_WORDS = stopwords.words("english") + list(string.punctuation)
    
def significant_word(word):
	return word not in USELESS_WORDS or len(word) > 1 or word.isalpha()
        
def create_document(year):
    yearly_report = r_server.get(year)
    return str(yearly_report)

def create_stems(document_text):
	""" Returns list of all unique stems used in a given document """
	def stem(tokens):
        porter = nltk.PorterStemmer()
        return [porter.stem(t) for t in tokens]
    data = document_text.lower()
    words = nltk.wordpunct_tokenize(data)
	return stem(filter(significant_word, words))

def get_entities(document_text):
    sentences = nltk.sent_tokenize(document_text)
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
