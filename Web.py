# Python code for the web app

from flask import Flask, render_template, request, redirect, url_for, send_file
from datetime import datetime
import sqlite3
import qrcode
from io import BytesIO

app = Flask(__name__)

# Database initialization
def initialize_database():
    conn = sqlite3.connect("computers.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS computers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            computer_id TEXT,
            component TEXT,
            serial_number TEXT,
            date_added TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert data into the database
def insert_data(computer_id, component, serial_number):
    conn = sqlite3.connect("computers.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO computers (computer_id, component, serial_number, date_added)
        VALUES (?, ?, ?, ?)
    ''', (computer_id, component, serial_number, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

# Function to fetch last 10 entries from the database
def get_last_10_entries():
    conn = sqlite3.connect("computers.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM computers
        ORDER BY date_added DESC
        LIMIT 10
    ''')
    entries = cursor.fetchall()
    conn.close()
    return entries

# Function to search entries by computer_id
def search_entries(computer_id):
    conn = sqlite3.connect("computers.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM computers
        WHERE computer_id = ?
    ''', (computer_id,))
    entries = cursor.fetchall()
    conn.close()
    return entries

# Function to generate QR code
def generate_qrcode(computer_id):
    img = qrcode.make(computer_id)
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes

# Function to export database entries to a CSV file
def export_to_csv():
    conn = sqlite3.connect("computers.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM computers")
    rows = cursor.fetchall()
    conn.close()

    with open("computers.csv", "w") as f:
        for row in rows:
            f.write(",".join(str(col) for col in row) + "\n")

# Initialize database
initialize_database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/view_entries')
def view_entries():
    entries = get_last_10_entries()
    return render_template('view_entries.html', entries=entries)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        computer_id = request.form['computer_id']
        entries = search_entries(computer_id)
        return render_template('search_results.html', entries=entries)
    return render_template('search.html')

@app.route('/generate_qrcode', methods=['GET', 'POST'])
def generate_qr():
    if request.method == 'POST':
        computer_id = request.form['computer_id']
        img_bytes = generate_qrcode(computer_id)
        return img_bytes.getvalue(), 200, {'Content-Type': 'image/png'}
    return render_template('generate_qrcode.html')

@app.route('/add_entry', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        computer_id = request.form['computer_id']
        component = request.form['component']
        serial_number = request.form['serial_number']
        insert_data(computer_id, component, serial_number)
        return redirect(url_for('index'))
    return render_template('add_entry.html')

@app.route('/export_csv')
def export_csv():
    export_to_csv()
    return send_file("computers.csv", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
