import sqlite3
import tkinter as tk
from tkinter import ttk

class DatabaseViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("PC Inventory Viewer")

        # Create and connect to SQLite database
        self.conn = sqlite3.connect('pc_inventory.db')
        self.cursor = self.conn.cursor()

        # Create widgets
        self.table = ttk.Treeview(root, columns=('ID', 'Brand', 'SerialNumber', 'MemorySerial', 'BoardSerial', 'DateAdded'), show='headings')
        self.table.heading('ID', text='ID')
        self.table.heading('Brand', text='Brand')
        self.table.heading('SerialNumber', text='Serial Number')
        self.table.heading('MemorySerial', text='Memory Serial')
        self.table.heading('BoardSerial', text='Board Serial')
        self.table.heading('DateAdded', text='Date Added')

        self.search_label = tk.Label(root, text="Search:")
        self.search_entry = tk.Entry(root)
        self.search_button = tk.Button(root, text="Search", command=self.search_data)

        # Pack widgets
        self.table.pack(padx=10, pady=10)
        self.search_label.pack(pady=5)
        self.search_entry.pack(pady=5)
        self.search_button.pack(pady=10)

        # Load and display the last 10 entries
        self.load_last_entries()

    def load_last_entries(self):
        # Fetch the last 10 entries from pc_inventory table
        self.cursor.execute('SELECT * FROM pc_inventory ORDER BY ID DESC LIMIT 10')
        data = self.cursor.fetchall()

        # Display the data in the Treeview
        for row in data:
            self.table.insert('', 'end', values=row)

    def search_data(self):
        # Clear previous search results
        for item in self.table.get_children():
            self.table.delete(item)

        # Get the search term from the entry widget
        search_term = self.search_entry.get()

        # Execute the SQL query for searching
        query = f"SELECT * FROM pc_inventory WHERE SerialNumber LIKE '%{search_term}%' OR MemorySerial LIKE '%{search_term}%' OR BoardSerial LIKE '%{search_term}%'"
        self.cursor.execute(query)

        # Fetch the results
        results = self.cursor.fetchall()

        # Display the search results in the Treeview
        for row in results:
            self.table.insert('', 'end', values=row)

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseViewer(root)
    root.mainloop()
