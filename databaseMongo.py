'''
!!!
NO LONGER USED
!!!
'''


from pymongo import MongoClient

client = MongoClient("localhost", 27017)

db = client.invertedIndex

tokens = ["computer","science","ics"]

for word in tokens:
    collection = db[word]
    
    document = {"_id": word, "document_ID": "0/20"}
    collection.insert_one(document)
    
for word in tokens:
    collection = db[word]
    
    print(f"Documents in collection '{word}':")
    for document in collection.find():
        print(document)
    
  
'''
words = db.words
words.insert_one({"word": "ICS", "Frequency": 10})
for word in words.find():
    print(word)
'''
