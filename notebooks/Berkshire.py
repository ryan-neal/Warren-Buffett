import sys
import os
import re
import json
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import textract
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
from nltk.corpus import stopwords
from collections import Counter
import pprint
import pandas_datareader.data as web
import datetime

nlp = spacy.load('en')

r_server = redis.Redis("localhost")
r_server.ping
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
Ninety_83 = get_year(1983)
test = nlp(Ninety_83)

print(Ninety_83)

#define some parameters
min_token_length = 2

#Function to check if the token is a noise or not
def isNoise(token):
    is_noise = False
    if token.is_stop == True:
        is_noise = True
    elif len(token.string) <= min_token_length:
        is_noise = True
    return is_noise
def cleanup(token, lower = True):
    if lower:
       token = token.lower()
    return token.strip()

# top unigrams used in the reviews
cleaned_list = [cleanup(word.string) for word in test if not isNoise(word)]
print(Counter(cleaned_list).most_common(10))