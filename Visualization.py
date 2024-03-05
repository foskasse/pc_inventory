import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3

# Function to fetch data from the SQLite database
def fetch_data():
    conn = sqlite3.connect("computers.db")
    cursor = conn.cursor()
    cursor.execute("SELECT component, COUNT(*) FROM computers GROUP BY component")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Function to display the pie chart
def show_pie_chart():
    data = fetch_data()
    labels = [row[0] for row in data]
    sizes = [row[1] for row in data]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.title('Component Distribution')
    plt.show()

# GUI
def create_gui():
    root = tk.Tk()
    root.title("Data Visualization")

    # Notebook (Tabs)
    notebook = ttk.Notebook(root)

    # Pie Chart Tab
    tab_pie_chart = ttk.Frame(notebook)
    pie_chart_button = tk.Button(tab_pie_chart, text="Show Pie Chart", command=show_pie_chart)
    pie_chart_button.pack(padx=20, pady=20)

    notebook.add(tab_pie_chart, text="Pie Chart")

    notebook.pack(expand=1, fill='both')

    root.mainloop()

# Run the GUI
create_gui()
