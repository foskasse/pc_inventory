import sqlite3

def fetch_and_print_data(db_file):
    # Connect to SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Fetch all data from pc_inventory table
    cursor.execute('SELECT * FROM pc_inventory')
    data = cursor.fetchall()

    # Print the header
    print("ID\tBrand\tSerialNumber\tMemorySerial\tBoardSerial\tDateAdded")

    # Print the data
    for row in data:
        print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}")

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    # Provide the path to the SQLite database file
    sqlite_db_file = 'pc_inventory.db'  # Update with your actual database file path

    # Fetch and print data from the SQLite database
    fetch_and_print_data(sqlite_db_file)
