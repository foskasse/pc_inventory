from fpdf import FPDF
import sqlite3

# Function to fetch data from the SQLite database
def fetch_data():
    conn = sqlite3.connect("computers.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM computers")
    rows = cursor.fetchall()

    conn.close()
    return rows

# Function to generate PDF with database entries
def generate_pdf():
    data = fetch_data()

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add header
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(0, 10, "Enterprise Database Report", ln=True, align="C")
    pdf.ln(5)

    # Add table headers
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(20, 10, "ID", border=1, ln=False, align="C")
    pdf.cell(50, 10, "Computer ID", border=1, ln=False, align="C")
    pdf.cell(50, 10, "Component", border=1, ln=False, align="C")
    pdf.cell(50, 10, "Serial Number", border=1, ln=False, align="C")
    pdf.cell(30, 10, "Date Created", border=1, ln=True, align="C")

    # Add table data
    pdf.set_font("Arial", size=10)
    for row in data:
        pdf.cell(20, 10, str(row[0]), border=1, ln=False, align="C")
        pdf.cell(50, 10, str(row[1]), border=1, ln=False)
        pdf.cell(50, 10, str(row[2]), border=1, ln=False)
        pdf.cell(50, 10, str(row[3]), border=1, ln=False)
        pdf.cell(30, 10, str(row[4]), border=1, ln=True, align="C")

    # Add footer
    pdf.set_y(-15)
    pdf.set_font("Arial", size=8)
    pdf.cell(0, 10, f"Page {pdf.page_no()}", align="C")

    pdf.output("enterprise_report.pdf")

    print("PDF generated successfully.")

if __name__ == "__main__":
    generate_pdf()
