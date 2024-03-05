import sqlite3

# Function to connect to the SQLite database
def connect_to_database(database_name):
    conn = sqlite3.connect(database_name)
    return conn

# Function to fetch all data from the SQLite database
def fetch_all_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM computers")
    rows = cursor.fetchall()
    return rows

# Function to perform data validation and check for duplicates
def validate_and_check_duplicates(data):
    unique_entries = set()
    duplicates = []

    for entry in data:
        if len(entry) == 4:  # Check the length of the tuple
            computer_id, component, serial_number, date_created = entry  # Unpack the tuple
            


    return duplicates

# Function to print validation results
def print_validation_results(duplicates):
    if not duplicates:
        print("No duplicates found.")
    else:
        print("Duplicates found:")
        for duplicate in duplicates:
            print(duplicate)

# Main function
def main():
    database_name = "computers.db"
    conn = connect_to_database(database_name)
    data = fetch_all_data(conn)
    duplicates = validate_and_check_duplicates(data)
    print_validation_results(duplicates)
    conn.close()

if __name__ == "__main__":
    main()
