"""
Overview:
processes lesson content and returns the weights and a unique lesson hash id (sha256)
returned to the flask app to store in the db

"""
import numpy as np
import pickle

import hashlib

#gensim (for processing text and for lda model)
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS

#nltk (for text processing)
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.corpus import stopwords

def handle_lesson(text):
    """
    input
    text: a str of the lesson content to be processed
    
    output
    lesson_id: a unique hashstring of the processed txt
    weights_array: and lesson_id together in lesson database
    """
    
    #cleans the document
    bow_corpus = process_text(text)
    
    #gets unique id for processed tags
    # lesson_id = get_id(bow_corpus)
    
    #gets the predicted weights for the topic
    weights_array = get_topic_weights(bow_corpus)
    
    #gets unique id for lesson
    # lesson_id = get_id(text)
    
    #checks if id already in database
    #to be implemented
    
    return weights_array

def get_id(bow_corpus):
    #a unique hash of the processed text
    m = hashlib.sha256()
    m.update(bytes(str(bow_corpus), encoding='utf-8'))
    
    return m.hexdigest()

def process_text(text):
    """
    inputs
    text: the preprocess string of text of the lesson
    
    outputs
    bow_corpus: the vectorized count of text words
    
    """
    #call text process helper fn
    processed_doc = preprocess(text)
    
    #create dictionary for gensim
    id2word = gensim.corpora.Dictionary([processed_doc])

    #Term Document Frequency
    bow_corpus = id2word.doc2bow(processed_doc)
    
    return bow_corpus

#lesson process helper functions
def lemmatize_stemming(text):
    
    stemmer = SnowballStemmer('english')
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

def preprocess(text):
    
    #multilingual stopword set, common words in each language that don't contribute to the topic of the document
    multi_lang_stop_words = set(stopwords.words(['russian', 'spanish', 'french', 'german', 'italian']))
    stop_words = gensim.parsing.preprocessing.STOPWORDS.union(multi_lang_stop_words)
    
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in stop_words and len(token) > 3:
            result.append(lemmatize_stemming(token))
    return result

def get_topic_weights(bow_corpus):
    """
    input
    bow_corpus: document text processed for format readable for gensim model
    
    output
    weights_array: 1D np array of len 15, with each idx corresponds to a topic
    """
    
    lda_model = pickle.load(open('lda_model.pkl', 'rb'))

    # call gensim lda model method, returns predicted topic weights
    weights = lda_model.get_document_topics(bow_corpus)
    
    #returns formated weights_array
    return format_topic_weights(weights)

def format_topic_weights(weights):
    """
    input
    weights: list of 2 item tuples, where first item is an int that is the index of where it is to be placed
    
    output
    topic_array: an np array where the predicted topic weights are presented for all 15 topics (most will be sparse)
    """
    topic_array = np.zeros(15)
    
    for i in range(15):
        for idx, weight in weights:
            if idx == i:
                topic_array[idx] = weight

            
    return list(np.round(topic_array, 4))
    
