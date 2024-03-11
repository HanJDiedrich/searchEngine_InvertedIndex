import tkinter as tk
import json
import pickle
from bs4 import BeautifulSoup
import requests
from nltk import sent_tokenize
from index_constructor import *
from query_main import *
import nltk
import ssl

from query_main import *
def get_title_and_description(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        title_tag = soup.find('title')
        title = title_tag.text.strip() if title_tag else 'No title available'

        paragraphs = soup.find_all('p')
        content = ' '.join([paragraph.text.strip() for paragraph in paragraphs])
        sentences = sent_tokenize(content)
        description = ' '.join(sentences[:2]) if sentences else 'No description available'

        return title, description

    except Exception as e:
        print(f"Error extracting title and description for {url}: {e}")
        return 'Error', 'Error'


def search_database(document_dictionary, valid_words, missing_words):
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
        
    return top_tier_docs

def on_search_button_click():
    query = entry.get()
    document_dictionary, valid_words, missing_words = get_documents(query)
    results = search_database(document_dictionary, valid_words, missing_words)
    update_results(results)

def update_results(results):
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)  # Clear previous results

    for tier_list in results:
        result_text.insert(tk.END, f"Contains {len(tier_list)} / 20 query terms\n")
        numPrinted = 0
        for doc in tier_list:
            title, description = get_title_and_description(doc)
            result_text.insert(tk.END, f"Title: {title}, URL: {doc}, Description: {description}\n")
            numPrinted += 1
            if numPrinted > 20:
                break
        if numPrinted > 20:
            break


#Create the main window
root = tk.Tk()
root.title("Database Search")

root.geometry("1000x900")
# INDEX STATISTICS
statistics_text = f"TOTAL DOCUMENTS: \n" \
                  f"UNIQUE WORDS: \n" \
                  f"INDEX SIZE: \n" \
                  f"Welcome to our search engine"

label_statistics = tk.Label(root, text=statistics_text)
label_statistics.pack(pady=10)

#Create and place widgets
label = tk.Label(root, text="Enter Search Query:")
label.pack(pady=10)

entry = tk.Entry(root, width=30)
entry.pack(pady=10)

search_button = tk.Button(root, text="Search", command=on_search_button_click, bg="green")
search_button.pack(pady=10)

result_text = tk.Text(root, height=10, width=50, state=tk.DISABLED)
result_text.pack(pady=10)
result_text.pack_propagate(0)

#Run the Tkinter event loop
if __name__ == '__main__':
    
    root.mainloop()