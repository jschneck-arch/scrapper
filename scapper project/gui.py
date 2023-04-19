import tkinter as tk
import threading
import webbrowser

from scrapper import scrape
from auth import get_auth_session

class ScrapperGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Web Scrapper")
        self.master.geometry("400x300")

        self.label1 = tk.Label(self.master, text="Enter URL:")
        self.label1.pack()

        self.entry1 = tk.Entry(self.master, width=50)
        self.entry1.pack()

        self.label2 = tk.Label(self.master, text="Enter Keyword:")
        self.label2.pack()

        self.entry2 = tk.Entry(self.master, width=50)
        self.entry2.pack()

        self.label3 = tk.Label(self.master, text="Enter Username:")
        self.label3.pack()

        self.entry3 = tk.Entry(self.master, width=50)
        self.entry3.pack()

        self.label4 = tk.Label(self.master, text="Enter Password:")
        self.label4.pack()

        self.entry4 = tk.Entry(self.master, width=50, show='*')
        self.entry4.pack()

        self.btn1 = tk.Button(self.master, text="Scrape", command=self.scrape)
        self.btn1.pack(pady=10)

        self.text = tk.Text(self.master)
        self.text.pack()

    def scrape(self):
        url = self.entry1.get()
        keyword = self.entry2.get()
        username = self.entry3.get()
        password = self.entry4.get()

        self.text.delete('1.0', tk.END)

        if not url or not keyword:
            self.text.insert('1.0', 'Please provide both URL and Keyword')
        return
        self.text.insert('1.0', 'Scraping started...\n')

    try:
        for txt_file in scrape(keyword, url, username, password):
            self.text.insert('end', txt_file + '\n')
            self.text.insert('end', 'Scraping finished successfully!\n')
    except Exception as e:
            self.text.insert('end', 'Scraping failed!\n')
            self.text.insert('end', f'Error: {e}\n')

    self.entry1.delete(0, tk.END)
    self.entry2.delete(0, tk.END)
    self.entry3.delete(0, tk.END)
    self.entry4.delete(0, tk.END)
    def search_files(self):
        self.text.delete('1.0', tk.END)
        self.text.insert(tk.END, 'Searching files...\n')
        self.text.update()

        keyword = self.keyword_entry.get()
        url = self.url_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        results = scrape(keyword, url, username, password)
        for result in results:
            self.text.insert(tk.END, result + '\n')
        self.text.insert(tk.END, 'Done.')

    def clear_entries(self):
        self.keyword_entry.delete(0, tk.END)
        self.url_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.text.delete('1.0', tk.END)
