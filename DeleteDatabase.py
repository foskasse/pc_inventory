import sqlite3

# Function to delete all data from the SQLite database
def delete_all_data():
    conn = sqlite3.connect("computers.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM computers")
    
    conn.commit()
    conn.close()
    print("All data deleted from the database.")

# Main function to delete all data
def main():
    delete_all_data()

if __name__ == "__main__":
    main()
