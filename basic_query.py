import math
import json
import sys
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup

import pickle


def get_documents(word):
    with open('data.pickle', 'rb') as f:
        existing_data = pickle.load(f)
    word_data = existing_data[word][0] #retrive just the data associated with the word
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
