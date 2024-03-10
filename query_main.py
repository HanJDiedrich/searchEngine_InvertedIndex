import json
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import pickle
import numpy
from index_constructor import *

class sortedRank:
    def __init__(self):
        self.data = {}
    def insert(self,key,value): #document_ID, score
        self.data[key] = value
    def sortit(self, reversed = True):
        sorted_items = sorted(self.data.items(), key = lambda x: x[1], reverse = reversed)
        return sorted_items
        
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
    #print(set_query_word)
    
    #count how many words of the query each document contains
    wordsExistingIndex = []
    docMaxHeap = {} #record #shared words
    missingWords = 0
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
            missingWords += 1
    #print(docMaxHeap)
    count = 0
    for key, value in docMaxHeap.items():
        if len(value) == len(wordsExistingIndex):
            #print(f"{key},{value}")
            count += 1
    #print(count)
    
    return docMaxHeap, wordsExistingIndex, missingWords
    
#Create a tier of documents that contain numTerms of the query
def find_Documents_Tier(document_dict, numTerms):
    index_number_of_terms = []
    for key, value in document_dict.items(): #doc_ID: set(query terms)
        if len(value) == numTerms:
            index_number_of_terms.append(key)
    return index_number_of_terms


def rank_documents(top_tier_docs, document_dict):
    #Rank based on how many words of the query the document contains
    #Rank based on pagerank
    #Rank based on TF-IDF
    
    #Rank based on index occurences - rank where the words appear in proximity to eachother
        
    #Find ranked scores and sort term_ranked lists
    listToBeSorted = sortedRank()
    for document in top_tier_docs:
        present_terms = document_dict[document]
        #Find tf-idf scores for document
        #Score(q,d) = sum(tf-idf) #higher Tf-idf means more important or relevant
        tf_idf_score = 0
        
        for term in present_terms:
            #In order to make lower scores -> more relevant, take inverse
            tf_idf_score += (1 - find_TF_IDF_score(term, document))

        #Find proximity score - smaller window better
        #Combine TF-IDF score for each word in query and combine query term proximity scoring using indicies
        #Calculate proximity scores - closer together -> lower score
        proximity_string_list = sortedRank()
        for term in present_terms:
            list_of_indicies = invertedIndex[term][0][document]
            for indicie in list_of_indicies:
                proximity_string_list.insert(term, indicie)
        #sort
        inOrder_string = proximity_string_list.sortit(False)
        proximity_score = find_index_proximity_score(inOrder_string, present_terms)
        #print(inOrder_string)
        #print(proximity_score)
        
        total_score = tf_idf_score + proximity_score
        #insert into list
        listToBeSorted.insert(document, total_score)
        
    #sort list, return
    finallyRanked = listToBeSorted.sortit(False) #lower is now more significant
    return finallyRanked

#Finds proximity score
def find_index_proximity_score(string_list, terms):
    smallestWindow = 0
    for i in range(len(string_list) - 1):
        smallestWindow += string_list[i + 1][1] - string_list[i][1]
    #hash score
    score = smallestWindow - (len(terms)/2)
    
    if smallestWindow < 10:
        mapped_score = map_score(score, 0, 10)
    elif smallestWindow < 100:
        mapped_score = map_score(score, 0, 100)
    elif smallestWindow < 100:
        mapped_score = map_score(score, 0, 1000)
    else:
        mapped_score = map_score(score, 0, 10000)
    #smaller is better
    return mapped_score

def map_score(value, minimum, maximum):
    if value == 0:
        return 0
    mapped = (value - minimum) / (maximum - minimum)
    mapped = max(0, min(mapped, 1))
    
    return mapped
    
def find_TF_IDF_score(word, document):
    try: #Search invertedindex
        return invertedIndex[word][1][document]
    except: #No tf-IDF value found for word and document
        return 0
    
#Retrieve all URLS relevant documents found
def returnURL(document_id):
    bookeeper = "C:\\Users\\hanjd\\Desktop\\121\\Project3\\webpages\\WEBPAGES_RAW\\bookkeeping.json"

    with open(bookeeper, 'r') as f:
        data = json.load(f)
        
    return data[document_id]

#MAIN
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
        print("Enter your query or enter '404' to quit")
        queryInput = input("ENTER: ")
        if (queryInput == ""):
            print("Please enter a valid query")
            continue
        if (queryInput == "404"):
            print("EXITING...")
            break
        document_dictionary, valid_words, missing_words = get_documents(queryInput)
        if len(valid_words) == 0:
            print("NO RESULTS FOUND FOR THIS QUERY")
            continue
        #SEARCH
        
        #Access tiers to get top 20 relevant documents #top tier at index 0
        top_tier_docs = []
        tier_num = len(valid_words)
        current_found_docs = 0
        #We've got the top tiers that will give us the top 20
        while(current_found_docs < 20 and tier_num > 0):
            #top_tier_docs.append(find_Documents_Tier(document_dictionary, tier_num))
            new_found_ranked = rank_documents(find_Documents_Tier(document_dictionary, tier_num), document_dictionary)
            #print(new_found_ranked)
            top_tier_docs.append(new_found_ranked)
            current_found_docs += len(new_found_ranked)
            tier_num -= 1
        
        #OUTPUT
        numPrinted = 0
        for tier_list in top_tier_docs:
            print(f"Contains {len(valid_words) - top_tier_docs.index(tier_list)} / {len(valid_words) + missing_words} query terms")
            for doc in tier_list:
                print(f"#{numPrinted} doc_ID: {doc[0]} Score: {doc[1]}")
                print(returnURL(doc[0]))
                numPrinted += 1
                if numPrinted > 20:
                    break
            if numPrinted > 20:
                    break        
        print()
        #Get top tiered index, if results > 20, we good
        #if total results < 20, move down to lower indexes
        #print out document(url) results and descriptions
        

#python query_main.py