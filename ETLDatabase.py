import sqlite3
import csv
import os
import shutil
import logging
from datetime import datetime
import random

# Set up logging
log_folder = "Logs"
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

log_filename = os.path.join(log_folder, f"log_{datetime.now().strftime('%Y-%m-%d')}.txt")
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

# Function to create SQLite table
def create_table():
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

# Function to create the SQLite database
def create_database():
    conn = sqlite3.connect("computers.db")
    conn.close()

# Function to generate a random computer ID
def generate_computer_id():
    return str(random.randint(1000, 9999))

# Function to insert data into SQLite database
def insert_data(computer_id, component, serial_number):
    conn = sqlite3.connect("computers.db")
    cursor = conn.cursor()
    date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO computers (computer_id, component, serial_number, date_added)
        VALUES (?, ?, ?, ?)
    ''', (computer_id, component, serial_number, date_added))
    conn.commit()
    conn.close()

# Function to process a CSV file
def process_csv_file(file_path):
    computer_id = generate_computer_id()
    with open(file_path, 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            component = row['Component']
            serial_number = row['SerialNumber']
            insert_data(computer_id, component, serial_number)

# Function to move the processed CSV file
def move_processed_file(file_path):
    processed_folder = "CSVProcessed"
    if not os.path.exists(processed_folder):
        os.makedirs(processed_folder)
    shutil.move(file_path, os.path.join(processed_folder, os.path.basename(file_path)))

# Main function to process CSV files in the "CSVToBeProcessed" folder
def main():
    create_database()
    create_table()

    input_folder = "CSVToBeProcessed"
    for filename in os.listdir(input_folder):
        if filename.endswith(".csv"):
            file_path = os.path.join(input_folder, filename)
            try:
                process_csv_file(file_path)
                move_processed_file(file_path)
                logging.info(f"Processed and moved {filename}.")
            except Exception as e:
                logging.error(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    main()
