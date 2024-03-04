import os
import csv
import sqlite3
import shutil
from datetime import datetime

def setup_logging():
    log_folder = 'Logs'
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    log_file = os.path.join(log_folder, f"log_{datetime.now().strftime('%Y%m%d')}.txt")
    return log_file

def load_to_database(csv_file, db_file):
    # Read data from CSV file
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)

        # Connect to SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Attempt to add data to the database
        try:
            for pc_data in csv_reader:
                cursor.execute('''INSERT INTO pc_inventory
                                  (Brand, SerialNumber, MemorySerial, BoardSerial)
                                  VALUES (?, ?, ?, ?)''',
                               (pc_data.get('Brand', ''), pc_data.get('SerialNumber', ''),
                                pc_data.get('MemorySerial', ''), pc_data.get('BoardSerial', '')))

            # Commit changes and close the database connection
            conn.commit()
            conn.close()

            return True  # Success
        except Exception as e:
            log_error(f"Error adding data to the database: {e}")
            return False  # Error

def process_csv_file(csv_file, db_file):
    # Load data to the database
    success = load_to_database(csv_file, db_file)

    # Move the CSV file to the "CSVProcessed" folder after processing
    processed_folder = 'CSVProcessed'
    if not os.path.exists(processed_folder):
        os.makedirs(processed_folder)

    try:
        shutil.move(csv_file, os.path.join(processed_folder, os.path.basename(csv_file)))
        log_info(f"CSV file '{os.path.basename(csv_file)}' moved to '{processed_folder}'.")
    except Exception as e:
        log_error(f"Error moving CSV file to '{processed_folder}': {e}")

    return success

def log_info(message):
    log_file = setup_logging()
    with open(log_file, 'a') as log:
        log.write(f"{datetime.now()} - INFO: {message}\n")

def log_error(message):
    log_file = setup_logging()
    with open(log_file, 'a') as log:
        log.write(f"{datetime.now()} - ERROR: {message}\n")

if __name__ == "__main__":
    # Provide the path to the SQLite database file
    sqlite_db_file = 'pc_inventory.db'  # Update with your actual database file path

    # Specify the folder paths
    script_folder = os.path.dirname(os.path.abspath(__file__))
    to_be_processed_folder = os.path.join(script_folder, 'CSVToBeProcessed')

    # Check if there are any CSV files to process
    csv_files = [f for f in os.listdir(to_be_processed_folder) if f.endswith('.csv')]

    if csv_files:
        for csv_file in csv_files:
            # Construct the full path to the CSV file
            csv_file_path = os.path.join(to_be_processed_folder, csv_file)

            # Process the CSV file and log the result
            if process_csv_file(csv_file_path, sqlite_db_file):
                log_info(f"CSV file '{csv_file}' successfully added to the database.")
            else:
                log_error(f"CSV file '{csv_file}' not added to the database due to errors.")
    else:
        log_info("No CSV files found in 'CSVToBeProcessed' folder.")
