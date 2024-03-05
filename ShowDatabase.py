import sqlite3

# Function to fetch and display data from the SQLite database
def display_database():
    conn = sqlite3.connect("computers.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM computers")
    rows = cursor.fetchall()

    if not rows:
        print("No data in the database.")
    else:
        print("Database Results:")
        print("ID | Computer_ID | Component | Serial_Number | Date Created")
        print("-" * 60)  # Adjusted width for formatting
        for row in rows:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}")  # Include date_created field

    conn.close()

# Main function to display database results
def main():
    display_database()

if __name__ == "__main__":
    main()
