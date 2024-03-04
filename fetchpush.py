import os
import csv
import sqlite3

def load_to_database(csv_file, db_file):
    # Read data from CSV file
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        pc_data = next(csv_reader)  # Assume one row of data in the CSV

        # Connect to SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Insert data into the database with AUTOINCREMENT for ID
        cursor.execute('''INSERT INTO pc_inventory
                          (Brand, SerialNumber, MemorySerial, BoardSerial)
                          VALUES (?, ?, ?, ?)''',
                       (pc_data['Brand'], pc_data['SerialNumber'], pc_data['MemorySerial'], pc_data['BoardSerial']))
        
        # Commit changes and close the database connection
        conn.commit()
        conn.close()

def process_csv_file(csv_file, db_file):
    # Load data to the database
    load_to_database(csv_file, db_file)

    # Delete the CSV file after processing
    os.remove(csv_file)

if __name__ == "__main__":
    # Provide the path to the CSV file and SQLite database file
    csv_file_path = 'pc_inventory_sample.csv'  # Update with your actual file path
    sqlite_db_file = 'pc_inventory.db'  # Update with your actual database file path

    # Check if the CSV file exists
    if os.path.exists(csv_file_path):
        process_csv_file(csv_file_path, sqlite_db_file)
        print("CSV file processed and deleted.")
    else:
        print("CSV file not found.")
