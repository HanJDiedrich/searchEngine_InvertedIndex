import json
import nltk

nltk.download('stopwords')
from nltk.corpus import stopwords

import pickle

from index_constructor import *


#Retrieve all possible documents associated with the terms in the querys
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
    
    #count how many words of the query each document contains
    wordsExistingIndex = []
    docMaxHeap = {} #record #shared words
    for word in set_query_word:
        try: #find Word in inverted index
            #find all documents that contain the word
            for document in invertedIndex[word][0].keys():
                if document in docMaxHeap:
                    #add word to set
                    docMaxHeap[document].add(word)
                else:
                    docMaxHeap[document] = set()
                    docMaxHeap[document].add(word)
            wordsExistingIndex.append(word) #record that the word exists, will help later
            
        except: #move onto the next word
            pass
    print(docMaxHeap)
    count = 0
    for key, value in docMaxHeap.items():
        if len(value) == len(wordsExistingIndex):
            print(f"{key},{value}")
            count += 1
    print(count)
    
    return docMaxHeap, wordsExistingIndex
    

def rank_documents(document_dict, existingWords):
    #Rank based on how many words of the query the document contains
    #Rank based on pagerank
    #Rank based on TF-IDF
    #Rank based on index occurences - rank where the words appear in proximity to eachother
    docsThatContainAllQueryWords = 0
    term_Ranked_IDs = []
    for i in range(len(existingWords), 0 ,-1):
        for key, value in document_dict.items(): #doc_ID: set(query terms)
            if len(value) == i:
                term_Ranked_IDs.append(key)
            if i == len(existingWords):
                docsThatContainAllQueryWords += 1
    
    
    #Combine TF-IDF score for each word in query and combine query term proximity scoring using indicies
    #Calculate proximity scores
    proximity_Scores = {}
    for term in existingWords:
        pass
        #term_info = 
    
    #higher TF-IDF better
    
    #sum up 
   
#Retrieve all URLS relevant documents found
def returnURLS(document_ids):
    urls = []
    
    bookeeper = "C:\\Users\\hanjd\\Desktop\\121\\Project3\\webpages\\WEBPAGES_RAW\\bookkeeping.json"

    with open(bookeeper, 'r') as f:
        data = json.load(f)
        
    for document in document_ids:
        urls.append(data[document])
        #print(f"Document ID: {document_key}, URL: {url}")
    return urls


def query(query):
    word_urls = returnURLS(get_documents(query)[0].keys())
    return word_urls

def getInfo(queryTerms):
    list_urls = query(queryTerms)
    number_urls = len(list_urls)
    return number_urls, list_urls
    
if __name__ == '__main__':
    #Load Inverted Index
    global invertedIndex
    with open('data.pickle', 'rb') as f:
        invertedIndex = pickle.load(f)
    
    #Load document lengths dict
    with open('doc_info.pickle', 'rb') as f:
        docId_docLength = pickle.load(f)
    
    #INDEX STATISTICS
    print(f"TOTAL DOCUMENTS: {len(docId_docLength)}")
    print(f"UNIQUE WORDS: {len(invertedIndex)}")
    print(f"INDEX SIZE: {(os.path.getsize('data.pickle') / 1024):.0f} KB")
    
    print("Welcome to our search engine")
    
    
    while(True):
        print("Enter your query or enter 'exit' to quit")
        queryInput = input("ENTER: ")
        if (queryInput == ""):
            print("Please enter a valid query")
            continue
        if (queryInput == "exit"):
            print("EXITING...")
            break
        document_dictionary, valid_words = get_documents(queryInput)
        
        if len(valid_words) == 0:
            print("NO RESULTS FOUND FOR THIS QUERY")
    
    queryWords = ["artificial intelligence"] #['Informatics','Mondego','Irvine']
    for word in queryWords:
        results = getInfo(word.lower())
        num_urls = results[0]
        list_of_urls = results[1]
        
        
        #print(f"Query: {word} | URLS: {num_urls}\n{list_of_urls[:20]}")
        
    #python query_main.py