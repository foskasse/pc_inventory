Certainly! Below is an example README.md file that you can use to document your Python script:

```markdown
# PC Inventory Management

This Python script allows you to manage PC inventory by loading data from CSV files into an SQLite database and providing a GUI interface to view the last 10 entries and search by serial number, memory serial, and board serial.

## Prerequisites

- Python 3.x
- SQLite

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/pc-inventory-management.git
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create an SQLite database:

   ```bash
   python create_database.py
   ```

## Usage

1. Load PC inventory data from a CSV file:

   ```bash
   python process_csv.py
   ```

2. Run the GUI application to view the last 10 entries and search for specific PCs:

   ```bash
   python gui_app.py
   ```

## File Structure

- `create_database.py`: Creates the SQLite database and the `pc_inventory` table.
- `process_csv.py`: Loads data from a CSV file into the SQLite database.
- `gui_app.py`: Displays a GUI interface to view the last 10 entries and search for PCs.

## Additional Notes

- The database file (`pc_inventory.db`) will be created in the project directory.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
```

Replace the placeholders (`yourusername`, etc.) with your actual details and customize the content based on your project. This example includes sections for prerequisites, setup, usage instructions, file structure, and additional notes. Feel free to modify and expand it according to your specific needs.