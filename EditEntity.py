import sqlite3

# Function to retrieve all components and serial numbers for a computer_id
def get_components_and_serials(computer_id):
    conn = sqlite3.connect("computers.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT component, serial_number FROM computers
        WHERE computer_id = ?
    ''', (computer_id,))
    result = cursor.fetchall()
    conn.close()
    return result

# Function to retrieve computer data by computer_id
def get_computer_data(computer_id):
    conn = sqlite3.connect("computers.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM computers
        WHERE computer_id = ?
    ''', (computer_id,))
    result = cursor.fetchone()
    conn.close()
    return result

# Function to update serial_number for a specific component and computer_id
def update_serial_number(computer_id, component, new_serial_number):
    conn = sqlite3.connect("computers.db")
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE computers
        SET serial_number = ?
        WHERE computer_id = ? AND component = ?
    ''', (new_serial_number, computer_id, component))
    conn.commit()
    conn.close()

# Main function for editing serial numbers
def edit_serial_numbers():
    computer_id = input("Enter computer_id to edit: ")
    computer_data = get_computer_data(computer_id)

    if not computer_data:
        print("No computer found with the given computer_id.")
        return

    print("\nCurrent Computer Data:")
    print("ID: ", computer_data[0])
    print("Computer ID: ", computer_data[1])

    # Display all components and serial numbers for the computer_id
    components_and_serials = get_components_and_serials(computer_id)
    print("\nComponents:")
    for i, (component, serial_number) in enumerate(components_and_serials, start=1):
        print(f"{i} - {component} - Serial Number: {serial_number}")

    # Allow the user to edit serial numbers step by step
    while True:
        print("\nEdit Options:")
        print("Enter the component number to edit its serial number.")
        print("Enter 0 to exit.")

        choice = int(input("Your choice: "))

        if choice == 0:
            print("Exiting the edit process.")
            break
        elif 0 < choice <= len(components_and_serials):
            selected_component = components_and_serials[choice - 1][0]
            new_serial_number = input(f"Enter the new serial number for {selected_component}: ")
            update_serial_number(computer_id, selected_component, new_serial_number)
        else:
            print("Invalid choice. Please enter a valid component number.")

        updated_data = get_computer_data(computer_id)
        print("\nUpdated Computer Data:")
        print("ID: ", updated_data[0])
        print("Computer ID: ", updated_data[1])

        # Display all components and serial numbers for the computer_id after the update
        components_and_serials = get_components_and_serials(computer_id)
        print("\nComponents:")
        for i, (component, serial_number) in enumerate(components_and_serials, start=1):
            print(f"{i} - {component} - Serial Number: {serial_number}")

if __name__ == "__main__":
    edit_serial_numbers()