from src.features import parse
from src.data import query
import string
import nltk
from nltk.corpus import stopwords
from collections import Counter

import pymongo

client = pymongo.MongoClient()
db = client['BerkshireHathaway']['reports']

USELESS_WORDS = stopwords.words("english") + list(string.punctuation)

def get_sp(year):
    return db.find_one({'year': str(year)})['s&p-returns']

def get_brk(year):
    return db.find_one({'year': str(year)})['brk-returns']

def create_document(year):
    """ Given a year, query MongoDB for the corresponding report """
    return db.find_one({'year':str(year)})['text'].decode('utf-8')

def significant_word(word):
    return word not in USELESS_WORDS and len(word) > 1# and word.isalpha()

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

def get_lexical_diversity(document_text):
    words = ntlk.word_tokenize(document_text)
    return len(set(words))/len(words)

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
    """ Chunk phrases from document based on input parameters. 

    Args:
        document_text: String representing document to be parsed
        expressions: Iterable of expressions to chunk by

    Returns:
        list of tuples in the format (phrase, containing sentence)
    """
    new_patterns = 'Phrases: ' + '\n'.join(expressions) 
    chunker = nltk.RegexpParser(new_patterns)
    
    tagged_words = get_tags(document_text)
    # Identify NP chunks
    word_tree = [chunker.parse(word) for word in tagged_words]
    phrases = []
    
    for sent in word_tree:
        sentence = ' '.join(word for word, tag in sent.leaves())
        for subtree in sent.subtrees():
            if subtree.label() == 'Phrases':
                phrase = ' '.join(word for word, tag in subtree.leaves())
                phrases.append((phrase, sentence))
                                
    return phrases


def phrase_count(phrases):
    """ Order phrases by commonality 

    Args:
        phrases: list of tuples

    Returns:
        list of tuples in the format (phrase, count)
    """

    return Counter(tup[0] for tup in phrases).most_common()


def expression_percent(document_text, expressions):
    """ Returns % of sentences with expressions out of total # of sentences """
    phrases = get_phrases(document_text, expressions) 
    phrase_sents = set(tup[1] for tup in phrases)
    return len(phrase_sents) / get_sentence_count(document_text)

# TODO: separate file
def passive_voice_percent(start, end):
    exp = [generate_expression('passive_voice')]
    return [(year, expression_percent(create_document(year), exp))
            for year in range(start, end)]

def passive_voice_percent(start_year, end_year):
    exp = [parse.generate_expression('passive_voice')]
    return [(year, parse.expression_percent(query.create_document(year), exp))
            for year in range(start_year, end_year)]

def main():
    #pv = get_phrases(create_document(1990), [generate_expression('passive_voice')])
    #print('\n'.join(': '.join(tup) for tup in pv))
    print(passive_voice_percent(2000, 2017))


if __name__ == '__main__':
    main()