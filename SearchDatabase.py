import sqlite3

# Function to search by computer_id
def search_by_computer_id(computer_id):
    conn = sqlite3.connect("computers.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM computers
        WHERE computer_id = ?
    ''', (computer_id,))
    result = cursor.fetchall()
    conn.close()
    return result

# Function to search by serial_number
def search_by_serial_number(serial_number):
    conn = sqlite3.connect("computers.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM computers
        WHERE serial_number = ?
    ''', (serial_number,))
    result = cursor.fetchall()
    conn.close()
    return result

# Main function for searching
def search():
    print("Search Options:")
    print("1. Search by computer_id")
    print("2. Search by serial_number")
    
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        computer_id = input("Enter computer_id to search: ")
        result = search_by_computer_id(computer_id)
    elif choice == "2":
        serial_number = input("Enter serial_number to search: ")
        result = search_by_serial_number(serial_number)
    else:
        print("Invalid choice. Exiting.")
        return

    if result:
        print("Search Results:")
        for row in result:
            print(row)
    else:
        print("No matching records found.")

if __name__ == "__main__":
    search()
