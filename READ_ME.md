Project 3: Search Engine

Milestone 1: Produce an initial index for the corpus and a basic retrieval component 

Team Members:
Han Diedrich
Shayna Lebovitz
Kyle Wendt

02/06/24 - 02/16/24


Files:
index_constructor.py - construct inverted index by pasrsing all html source code in data dump, calculates metadata
main.py - call to create inverted index and retrieve index statistics

basic_query.py - query the inverted index to retrive urls corresponding to query input
query_main.py - call to search the index for a query word

data.pickle - database that hold the inverted index



TODO:
Report all necessary info correctly
- M1 Deliverable


Query:
Load index before initiating all searches
1 word
2 word
2+ word

Ranked Retrival:
For relevant Document Ids:
    Rank intersection between results of having n common, n-1, n-2, and so on
    Rank based on TF-IDF score
    Rank based on word index

Display 20 most relevant links
Return total link count that contains all terms
Return total link count that contains n-1, n-2 terms
Return total link count





GUI:
Proper display
Page Descriptions
