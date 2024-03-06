import math
import json
import sys
import os
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

import pickle

def get_documents(query):
    #Find valid words in query
    stop_words = set(stopwords.words('english'))
    words = query.split()
    queryWords = []
    for word in words:
        #if word is not present in list and not a number and is not a stop word
        if (word not in queryWords) and (word not in stop_words) and (not word.isnumeric()):
            queryWords.append(word.lower())
    set_query_word = queryWords
    print(set_query_word)

    
    
    with open('data.pickle', 'rb') as f:
        existing_data = pickle.load(f)
        
        
    word_data = existing_data[set_query_word[0]][0] #retrive just the data associated with the word
    document_ids = word_data

    #existing_data[word][1]["doc"] = 100
    print(existing_data[word])
    
    return document_ids
    
        
def returnURLS(document_ids):
    urls = []
    
    bookeeper = "C:\\Users\\hanjd\\Desktop\\121\\Project3\\webpages\\WEBPAGES_RAW\\bookkeeping.json"

    with open(bookeeper, 'r') as f:
        data = json.load(f)
        
    for document in document_ids:
        urls.append(data[document])
        
    return urls
