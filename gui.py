import os
import csv
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

# Function to fetch the last 10 entries from the database
def fetch_last_10_entries():
    conn = sqlite3.connect('pc_inventory.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pc_inventory ORDER BY ID DESC LIMIT 10')
    data = cursor.fetchall()
    conn.close()
    return data

# Function to display the results in the Treeview
def display_results(data, tree):
    for item in tree.get_children():
        tree.delete(item)
    for row in data:
        tree.insert('', 'end', values=row)

# Function to search entries in the database
def search_entries(search_term):
    conn = sqlite3.connect('pc_inventory.db')
    cursor = conn.cursor()
    query = f'''
        SELECT * FROM pc_inventory
        WHERE SerialNumber LIKE '%{search_term}%' OR
              MemorySerial LIKE '%{search_term}%' OR
              BoardSerial LIKE '%{search_term}%'
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

# Function to add a manual entry to the database
def add_manual_entry(entry_brand, entry_serial_number, entry_memory_serial, entry_board_serial):
    conn = sqlite3.connect('pc_inventory.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO pc_inventory
                      (Brand, SerialNumber, MemorySerial, BoardSerial, DateAdded)
                      VALUES (?, ?, ?, ?, ?)''',
                   (entry_brand, entry_serial_number, entry_memory_serial, entry_board_serial, datetime.now()))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Entry added successfully.")

# Function to edit a manual entry
def edit_manual_entry(entry_id):
    conn = sqlite3.connect('pc_inventory.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pc_inventory WHERE ID = ?', (entry_id,))
    entry_data = cursor.fetchone()
    conn.close()
    return entry_data

# Function to save the edited entry
def save_edited_entry(entry_id, entry_brand, entry_serial_number, entry_memory_serial, entry_board_serial):
    conn = sqlite3.connect('pc_inventory.db')
    cursor = conn.cursor()
    cursor.execute('''UPDATE pc_inventory
                      SET Brand=?, SerialNumber=?, MemorySerial=?, BoardSerial=?
                      WHERE ID=?''',
                   (entry_brand, entry_serial_number, entry_memory_serial, entry_board_serial, entry_id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Entry updated successfully.")

# Function to export all entries to a CSV file
def export_to_csv():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        conn = sqlite3.connect('pc_inventory.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM pc_inventory')
        entries = cursor.fetchall()
        conn.close()

        with open(file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['ID', 'Brand', 'SerialNumber', 'MemorySerial', 'BoardSerial', 'DateAdded'])
            csv_writer.writerows(entries)
        messagebox.showinfo("Success", f"Data exported to {file_path}.")

# Function to remove all entries from the database
def remove_all_entries():
    confirmation = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete all entries?")
    if confirmation:
        conn = sqlite3.connect('pc_inventory.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM pc_inventory')
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "All entries deleted successfully.")
    else:
        messagebox.showinfo("Deletion Cancelled", "Deletion of entries cancelled.")

# Main GUI class
class DatabaseViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("PC Inventory Management")

        # Notebook for tabbed interface
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')

        # Tab 1: Welcome
        self.tab_welcome = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_welcome, text="Welcome")
        self.create_welcome_tab()

        # Tab 2: Search
        self.tab_search = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_search, text="Search")
        self.create_search_tab()

        # Tab 3: Last 10 Entries
        self.tab_last_10_entries = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_last_10_entries, text="Last 10 Entries")
        self.create_last_10_tab()

        # Tab 4: Manual Entry
        self.tab_manual_entry = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_manual_entry, text="Manual Entry")
        self.create_manual_entry_tab()

        # Tab 5: Edit Entry
        self.tab_edit_entry = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_edit_entry, text="Edit Entry")
        self.create_edit_entry_tab()

        # Tab 6: Options (Import/Export)
        self.tab_options = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_options, text="Options")
        self.create_options_tab()

        # Bind the tab changing event to update the last 10 entries view
        self.notebook.bind("<<NotebookTabChanged>>", self.update_last_10_view)

    def create_welcome_tab(self):
        frame_welcome = ttk.Frame(self.tab_welcome, padding=(20, 20))
        frame_welcome.pack(expand=True, fill='both')

        label_welcome = tk.Label(frame_welcome, text="Welcome to PC Inventory Management", font=("Helvetica", 16, "bold"))
        label_welcome.pack(pady=10)

        label_instructions = tk.Label(frame_welcome, text="Use the tabs above to navigate and manage the inventory.",
                                       font=("Helvetica", 12))
        label_instructions.pack(pady=10)

    def create_search_tab(self):
        frame_search = ttk.Frame(self.tab_search, padding=(20, 20))
        frame_search.pack(expand=True, fill='both')

        label_search = tk.Label(frame_search, text="Search:", font=("Helvetica", 16))
        label_search.grid(row=0, column=0, pady=10, padx=10, sticky='w')

        entry_search = tk.Entry(frame_search, font=("Helvetica", 14))
        entry_search.grid(row=0, column=1, pady=10, padx=10)

        button_search = tk.Button(frame_search, text="Search", command=lambda: self.search_data(entry_search.get()))
        button_search.grid(row=0, column=2, pady=10, padx=10)

        # Treeview to display search results
        columns = ['ID', 'Brand', 'SerialNumber', 'MemorySerial', 'BoardSerial', 'DateAdded']
        tree_search = ttk.Treeview(frame_search, columns=columns, show='headings', selectmode="browse")
        for col in columns:
            tree_search.heading(col, text=col)
        tree_search.grid(row=1, column=0, columnspan=3, pady=10)

    def search_data(self, search_term):
        results = search_entries(search_term)
        display_results(results, self.tree_search)

    def create_last_10_tab(self):
        frame_last_10 = ttk.Frame(self.tab_last_10_entries, padding=(20, 20))
        frame_last_10.pack(expand=True, fill='both')

        # Treeview to display last 10 entries
        columns_last_10 = ['ID', 'Brand', 'SerialNumber', 'MemorySerial', 'BoardSerial', 'DateAdded']
        tree_last_10 = ttk.Treeview(frame_last_10, columns=columns_last_10, show='headings', selectmode="browse")
        for col in columns_last_10:
            tree_last_10.heading(col, text=col)
        tree_last_10.pack(expand=True, fill='both')

        # Fetch and display the last 10 entries
        data_last_10 = fetch_last_10_entries()
        display_results(data_last_10, tree_last_10)

    def update_last_10_view(self, event):
        # Update the last 10 entries view when changing to the Last 10 Entries tab
        if self.notebook.tab(self.notebook.select(), "text") == "Last 10 Entries":
            data_last_10 = fetch_last_10_entries()
            display_results(data_last_10, self.tree_last_10)

    def create_manual_entry_tab(self):
        frame_manual_entry = ttk.Frame(self.tab_manual_entry, padding=(20, 20))
        frame_manual_entry.pack(expand=True, fill='both')

        label_brand = tk.Label(frame_manual_entry, text="Brand:", font=("Helvetica", 14))
        label_brand.grid(row=0, column=0, pady=10, padx=10, sticky='w')
        entry_brand = tk.Entry(frame_manual_entry, font=("Helvetica", 14))
        entry_brand.grid(row=0, column=1, pady=10, padx=10)

        label_serial_number = tk.Label(frame_manual_entry, text="Serial Number:", font=("Helvetica", 14))
        label_serial_number.grid(row=1, column=0, pady=10, padx=10, sticky='w')
        entry_serial_number = tk.Entry(frame_manual_entry, font=("Helvetica", 14))
        entry_serial_number.grid(row=1, column=1, pady=10, padx=10)

        label_memory_serial = tk.Label(frame_manual_entry, text="Memory Serial:", font=("Helvetica", 14))
        label_memory_serial.grid(row=2, column=0, pady=10, padx=10, sticky='w')
        entry_memory_serial = tk.Entry(frame_manual_entry, font=("Helvetica", 14))
        entry_memory_serial.grid(row=2, column=1, pady=10, padx=10)

        label_board_serial = tk.Label(frame_manual_entry, text="Board Serial:", font=("Helvetica", 14))
        label_board_serial.grid(row=3, column=0, pady=10, padx=10, sticky='w')
        entry_board_serial = tk.Entry(frame_manual_entry, font=("Helvetica", 14))
        entry_board_serial.grid(row=3, column=1, pady=10, padx=10)

        button_add_entry = tk.Button(frame_manual_entry, text="Add Entry",
                                     command=lambda: add_manual_entry(entry_brand.get(),
                                                                       entry_serial_number.get(),
                                                                       entry_memory_serial.get(),
                                                                       entry_board_serial.get()),
                                     font=("Helvetica", 12))
        button_add_entry.grid(row=4, column=0, columnspan=2, pady=10)

    def create_edit_entry_tab(self):
        frame_edit_entry = ttk.Frame(self.tab_edit_entry, padding=(20, 20))
        frame_edit_entry.pack(expand=True, fill='both')

        label_search_id = tk.Label(frame_edit_entry, text="Enter ID to Edit:", font=("Helvetica", 14))
        label_search_id.grid(row=0, column=0, pady=10, padx=10, sticky='w')

        entry_edit_id = tk.Entry(frame_edit_entry, font=("Helvetica", 14))
        entry_edit_id.grid(row=0, column=1, pady=10, padx=10)

        button_search_entry = tk.Button(frame_edit_entry, text="Search",
                                        command=lambda: self.populate_edit_fields(entry_edit_id.get()),
                                        font=("Helvetica", 12))
        button_search_entry.grid(row=0, column=2, pady=10)

        # Entry fields for editing
        label_brand_edit = tk.Label(frame_edit_entry, text="Brand:", font=("Helvetica", 14))
        label_brand_edit.grid(row=1, column=0, pady=10, padx=10, sticky='w')
        entry_brand_edit = tk.Entry(frame_edit_entry, font=("Helvetica", 14))
        entry_brand_edit.grid(row=1, column=1, pady=10, padx=10)

        label_serial_number_edit = tk.Label(frame_edit_entry, text="Serial Number:", font=("Helvetica", 14))
        label_serial_number_edit.grid(row=2, column=0, pady=10, padx=10, sticky='w')
        entry_serial_number_edit = tk.Entry(frame_edit_entry, font=("Helvetica", 14))
        entry_serial_number_edit.grid(row=2, column=1, pady=10, padx=10)

        label_memory_serial_edit = tk.Label(frame_edit_entry, text="Memory Serial:", font=("Helvetica", 14))
        label_memory_serial_edit.grid(row=3, column=0, pady=10, padx=10, sticky='w')
        entry_memory_serial_edit = tk.Entry(frame_edit_entry, font=("Helvetica", 14))
        entry_memory_serial_edit.grid(row=3, column=1, pady=10, padx=10)

        label_board_serial_edit = tk.Label(frame_edit_entry, text="Board Serial:", font=("Helvetica", 14))
        label_board_serial_edit.grid(row=4, column=0, pady=10, padx=10, sticky='w')
        entry_board_serial_edit = tk.Entry(frame_edit_entry, font=("Helvetica", 14))
        entry_board_serial_edit.grid(row=4, column=1, pady=10, padx=10)

        button_save_entry = tk.Button(frame_edit_entry, text="Save Entry",
                                      command=lambda: self.save_edited_entry(entry_edit_id.get(),
                                                                             entry_brand_edit.get(),
                                                                             entry_serial_number_edit.get(),
                                                                             entry_memory_serial_edit.get(),
                                                                             entry_board_serial_edit.get()),
                                      font=("Helvetica", 12))
        button_save_entry.grid(row=5, column=0, columnspan=2, pady=10)

    def populate_edit_fields(self, entry_id):
        entry_data = edit_manual_entry(entry_id)
        if entry_data:
            entry_brand_edit.set(entry_data[1])
            entry_serial_number_edit.set(entry_data[2])
            entry_memory_serial_edit.set(entry_data[3])
            entry_board_serial_edit.set(entry_data[4])
        else:
            messagebox.showwarning("ID not found", f"No entry found with ID {entry_id}.")

    def create_options_tab(self):
        frame_options = ttk.Frame(self.tab_options, padding=(20, 20))
        frame_options.pack(expand=True, fill='both')

        button_export_csv = tk.Button(frame_options, text="Export to CSV", command=export_to_csv, font=("Helvetica", 12))
        button_export_csv.grid(row=0, column=0, pady=10, padx=10)

        button_remove_entries = tk.Button(frame_options, text="Remove All Entries", command=remove_all_entries, font=("Helvetica", 12))
        button_remove_entries.grid(row=1, column=0, pady=10, padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseViewer(root)
    root.geometry("1300x700")
    root.mainloop()