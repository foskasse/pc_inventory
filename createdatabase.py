def load_to_database(csv_file, db_file):
    # Read data from CSV file
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        try:
            pc_data = next(csv_reader)  # Assume one row of data in the CSV
        except StopIteration:
            print("CSV file is empty.")
            return

        # Debug prints
        print(f"pc_data: {pc_data}")

        # Connect to SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Insert data into the database with AUTOINCREMENT for ID
        try:
            cursor.execute('''INSERT INTO pc_inventory
                              (Brand, SerialNumber, MemorySerial, BoardSerial)
                              VALUES (?, ?, ?, ?)''',
                           (pc_data.get('Brand', ''), pc_data.get('SerialNumber', ''),
                            pc_data.get('MemorySerial', ''), pc_data.get('BoardSerial', '')))
        except Exception as e:
            print(f"Error inserting into database: {e}")

        # Commit changes and close the database connection
        conn.commit()
        conn.close()
