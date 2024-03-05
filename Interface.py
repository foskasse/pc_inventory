import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import csv
import shutil

class ComputerDatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Computer Database Management")
        self.initialize_gui_components()
        self.create_gui()

    def get_last_entries(self):
        with sqlite3.connect("computers.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT computer_id, component, serial_number, date_added
                FROM computers
                ORDER BY computer_id DESC, component
                LIMIT 100
            ''')
            return cursor.fetchall()

    def search(self, computer_id=None):
        with sqlite3.connect("computers.db") as conn:
            cursor = conn.cursor()
            if computer_id:
                cursor.execute('''
                    SELECT computer_id, component, serial_number
                    FROM computers
                    WHERE computer_id LIKE ?
                    ORDER BY computer_id, component
                ''', (f"%{computer_id}%",))
            else:
                cursor.execute('''
                    SELECT computer_id, component, serial_number
                    FROM computers
                    ORDER BY computer_id, component
                ''')
            return cursor.fetchall()

    def update_serial_number(self, computer_id, component, new_serial_number):
        with sqlite3.connect("computers.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE computers
                SET serial_number = ?
                WHERE computer_id = ? AND component = ?
            ''', (new_serial_number, computer_id, component))
            conn.commit()

    def update_treeview(self, data, treeview):
        treeview.delete(*treeview.get_children())
        for row in data:
            treeview.insert('', 'end', values=row)
        treeview.bind("<Double-1>", lambda event, tv=treeview: self.copy_to_clipboard(event, tv))

    def delete_all_entries(self):
        with sqlite3.connect("computers.db") as conn:
            conn.execute('DELETE FROM computers')
            messagebox.showinfo("Delete All Entries", "All entries deleted successfully.")

    def export_all_entries(self):
        with sqlite3.connect("computers.db") as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM computers')
            result = cursor.fetchall()

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(["Computer ID", "Component", "Serial Number"])
                csv_writer.writerows(result)
                messagebox.showinfo("Export All Entries", "All entries exported successfully.")

    def backup_database(self):
        shutil.copy("computers.db", "backup/computers_backup.db")
        messagebox.showinfo("Backup Database", "Database backup created successfully.")

    def restore_database(self):
        file_path = filedialog.askopenfilename(defaultextension=".db", filetypes=[("Database files", "*.db")])
        if file_path:
            shutil.copy(file_path, "computers.db")
            messagebox.showinfo("Restore Database", "Database restored successfully.")

    def perform_search(self):
        search_text = self.search_entry.get()
        result = self.search(computer_id=search_text)
        self.update_treeview(result, self.search_treeview)

    def perform_edit_search(self):
        edit_search_text = self.edit_entry.get()
        result = self.search(computer_id=edit_search_text)
        self.update_edit_treeview(result, self.edit_treeview)

    def update_edit_treeview(self, data, treeview):
        treeview.delete(*treeview.get_children())
        for computer_id, component, serial_number in data:
            treeview.insert('', 'end', iid=f"{computer_id}_{component}", values=(component, serial_number))
        treeview.bind("<Double-1>", lambda event, tv=treeview: self.copy_to_clipboard(event, tv))

    def perform_edit(self):
        computer_id_text = self.edit_entry.get()
        new_serial_text = self.new_serial_entry.get()
        selected_item = self.edit_treeview.selection()
        if selected_item:
            component = self.edit_treeview.item(selected_item, 'values')[0]
            self.update_serial_number(computer_id_text, component, new_serial_text)
            self.perform_edit_search()
            messagebox.showinfo("Edit Serial Number", "Serial Number edited successfully.")
        else:
            messagebox.showwarning("Edit Serial Number", "Please select a component for editing.")

    def copy_to_clipboard(self, event, treeview):
        item = treeview.selection()[0]
        computer_id = treeview.item(item, 'values')[0]
        self.root.clipboard_clear()
        self.root.clipboard_append(computer_id)
        messagebox.showinfo("Copied to Clipboard", f"Computer ID {computer_id} copied to clipboard.")

    def initialize_gui_components(self):
        self.notebook = ttk.Notebook(self.root)
        self.treeview = None
        self.search_entry = None
        self.edit_entry = None
        self.search_treeview = None
        self.edit_treeview = None
        self.new_serial_entry = None

    def create_last_entries_tab(self, notebook):
        tab_last_entries = ttk.Frame(notebook)
        last_entries_label = tk.Label(tab_last_entries, text="Last Entries", font=("Helvetica", 16))
        last_entries_label.pack(pady=10)
        self.treeview = ttk.Treeview(tab_last_entries, columns=('Computer ID', 'Component', 'Serial Number', 'Date Added'), show='headings')
        self.treeview.heading('Computer ID', text='Computer ID')
        self.treeview.heading('Component', text='Component')
        self.treeview.heading('Serial Number', text='Serial Number')
        self.treeview.heading('Date Added', text='Date Added')  # New column for date_added
        self.treeview.pack(expand=1, fill='both')
        self.update_treeview(self.get_last_entries(), self.treeview)
        notebook.add(tab_last_entries, text="Last Entries")

    def create_search_tab(self, notebook):
        tab_search = ttk.Frame(notebook)
        search_label = tk.Label(tab_search, text="Search", font=("Helvetica", 16))
        search_label.pack(pady=10)
        search_entry_label = tk.Label(tab_search, text="Enter Computer ID:")
        search_entry_label.pack()
        self.search_entry = tk.Entry(tab_search)
        self.search_entry.pack(pady=5)
        search_button = tk.Button(tab_search, text="Search", command=self.perform_search)
        search_button.pack(pady=10)
        self.search_treeview = ttk.Treeview(tab_search, columns=('Computer ID', 'Component', 'Serial Number'), show='headings')
        self.search_treeview.heading('Computer ID', text='Computer ID')
        self.search_treeview.heading('Component', text='Component')
        self.search_treeview.heading('Serial Number', text='Serial Number')
        self.search_treeview.pack(expand=1, fill='both')
        notebook.add(tab_search, text="Search")

    def create_edit_entries_tab(self, notebook):
        tab_edit_entries = ttk.Frame(notebook)
        edit_label = tk.Label(tab_edit_entries, text="Edit Entries", font=("Helvetica", 16))
        edit_label.pack(pady=10)
        edit_entry_label = tk.Label(tab_edit_entries, text="Enter Computer ID:")
        edit_entry_label.pack()
        self.edit_entry = tk.Entry(tab_edit_entries)
        self.edit_entry.pack(pady=5)
        edit_search_button = tk.Button(tab_edit_entries, text="Search", command=self.perform_edit_search)
        edit_search_button.pack(pady=5)
        self.edit_treeview = ttk.Treeview(tab_edit_entries, columns=('Component', 'Serial Number'), show='headings')
        self.edit_treeview.heading('Component', text='Component')
        self.edit_treeview.heading('Serial Number', text='Serial Number')
        self.edit_treeview.pack(expand=1, fill='both')
        serial_label = tk.Label(tab_edit_entries, text="Enter New Serial Number:")
        serial_label.pack()
        self.new_serial_entry = tk.Entry(tab_edit_entries)
        self.new_serial_entry.pack(pady=5)
        edit_button = tk.Button(tab_edit_entries, text="Edit Serial Number", command=self.perform_edit)
        edit_button.pack(pady=10)
        notebook.add(tab_edit_entries, text="Edit Entries")

    def create_options_tab(self, notebook):
        tab_options = ttk.Frame(notebook)
        options_label = tk.Label(tab_options, text="Options", font=("Helvetica", 16))
        options_label.pack(pady=10)
        delete_button = tk.Button(tab_options, text="Delete All Entries", command=self.delete_all_entries)
        delete_button.pack(pady=5)
        export_button = tk.Button(tab_options, text="Export All Entries", command=self.export_all_entries)
        export_button.pack(pady=5)
        backup_button = tk.Button(tab_options, text="Backup Database", command=self.backup_database)
        backup_button.pack(pady=5)
        restore_button = tk.Button(tab_options, text="Restore Database", command=self.restore_database)
        restore_button.pack(pady=5)
        notebook.add(tab_options, text="Options")

    def create_gui(self):
        self.create_last_entries_tab(self.notebook)
        self.create_search_tab(self.notebook)
        self.create_edit_entries_tab(self.notebook)
        self.create_options_tab(self.notebook)
        self.notebook.pack(expand=1, fill="both")

def main():
    root = tk.Tk()
    app = ComputerDatabaseApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
