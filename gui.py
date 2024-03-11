import tkinter as tk
from tkinter import scrolledtext

class SearchEngineApp:
    def __init__(self, master):
        self.master = master
        master.title("Search Engine")

        self.query_label = tk.Label(master, text="Enter your query:")
        self.query_label.pack()

        self.query_entry = tk.Entry(master, width=50)
        self.query_entry.pack()

        self.search_button = tk.Button(master, text="Search", command=self.search)
        self.search_button.pack()

        self.output_text = scrolledtext.ScrolledText(master, width=80, height=20)
        self.output_text.pack()

    def search(self):
        query = self.query_entry.get()
        print(query)
        self.output_text.delete(1.0, tk.END)  # Clear previous output
        document_dictionary, valid_words, missing_words = get_documents(query)
        print(document_dictionary)
        if len(valid_words) == 0:
            self.output_text.insert(tk.END, "NO RESULTS FOUND FOR THIS QUERY\n")
            return

        top_tier_docs = []
        tier_num = len(valid_words)
        current_found_docs = 0
        while current_found_docs < 20 and tier_num > 0:
            new_found_ranked = rank_documents(find_Documents_Tier(document_dictionary, tier_num), document_dictionary)
            top_tier_docs.append(new_found_ranked)
            current_found_docs += len(new_found_ranked)
            tier_num -= 1

        num_printed = 0
        for tier_list in top_tier_docs:
            self.output_text.insert(tk.END, f"Contains {len(valid_words) - top_tier_docs.index(tier_list)} / {len(valid_words) + missing_words} query terms\n")
            for doc in tier_list:
                self.output_text.insert(tk.END, f"#{num_printed} doc_ID: {doc[0]} Score: {doc[1]}\n")
                self.output_text.insert(tk.END, returnURL(doc[0]) + "\n")
                num_printed += 1
                if num_printed > 20:
                    break
            if num_printed > 20:
                break
        self.output_text.insert(tk.END, "\n")