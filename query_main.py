import math
import json
import sys
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup

import pickle

from index_constructor import *
from basic_query import *


    
def query(queryWord):
    word_urls = returnURLS(get_documents(queryWord))
    return word_urls

def getInfo(word):
    list_urls = query(word)
    number_urls = len(list_urls)
    return number_urls, list_urls
    
if __name__ == '__main__':
    with open('doc_info.pickle', 'rb') as f:
        docId_docLength = pickle.load(f)
    print(docId_docLength)
    
    
    queryWords = ["Mondego"] #['Informatics','Mondego','Irvine']
    for word in queryWords:
        results = getInfo(word.lower())
        num_urls = results[0]
        list_of_urls = results[1]
        
        
        #print(f"Query: {word} | URLS: {num_urls}\n{list_of_urls[:20]}")
        
        
#python query_main.py