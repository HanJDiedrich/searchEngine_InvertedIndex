import tkinter as tk

def search_database(query):
    # Implement your database search logic here
    # This function should return the results based on the query
    # For now, let's return dummy data
    return ["Result 1", "Result 2", "Result 3"]

def on_search_button_click():
    query = entry.get()
    results = search_database(query)
    update_results(results)

def update_results(results):
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)  # Clear previous results
    for result in results:
        result_text.insert(tk.END, f"{result}\n")
    result_text.config(state=tk.DISABLED)

#Create the main window
root = tk.Tk()
root.title("Database Search")

#Create and place widgets
label = tk.Label(root, text="Enter Search Query:")
label.pack(pady=10)

entry = tk.Entry(root, width=30)
entry.pack(pady=10)

search_button = tk.Button(root, text="Search", command=on_search_button_click)
search_button.pack(pady=10)

result_text = tk.Text(root, height=10, width=50, state=tk.DISABLED)
result_text.pack(pady=10)

#Run the Tkinter event loop
root.mainloop()