import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import qrcode
from PIL import Image, ImageTk
import sqlite3

class QRCodeGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.initialize_gui_components()
        self.create_gui()

    def initialize_gui_components(self):
        self.computer_id_label = None
        self.computer_id_entry = None
        self.qr_code_image_label = None
        self.generate_button = None
        self.print_button = None
        self.save_button = None
        self.qr_image = None

    def create_gui(self):
        input_frame = ttk.Frame(self.root, padding="20")
        input_frame.pack(fill="both", expand=True)

        self.computer_id_label = ttk.Label(input_frame, text="Computer ID:")
        self.computer_id_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.computer_id_entry = ttk.Entry(input_frame)
        self.computer_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.qr_code_image_label = ttk.Label(input_frame)
        self.qr_code_image_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.generate_button = ttk.Button(input_frame, text="Generate QR Code", command=self.generate_qr_code)
        self.generate_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.print_button = ttk.Button(input_frame, text="Print", command=self.print_qr_code)
        self.print_button.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        self.save_button = ttk.Button(input_frame, text="Save as Image", command=self.save_qr_code)
        self.save_button.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

    def generate_qr_code(self):
        computer_id = self.computer_id_entry.get()
        if computer_id:
            if self.validate_computer_id(computer_id):
                try:
                    qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=4,
                    )
                    qr.add_data(computer_id)
                    qr.make(fit=True)

                    self.qr_image = qr.make_image(fill_color="black", back_color="white")
                    self.show_qr_code_image()
                    messagebox.showinfo("Success", "QR Code generated successfully.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to generate QR Code: {e}")
            else:
                messagebox.showwarning("Warning", "Computer ID not found in the database.")
        else:
            messagebox.showwarning("Warning", "Please enter a computer ID.")

    def validate_computer_id(self, computer_id):
        conn = sqlite3.connect("computers.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM computers WHERE computer_id = ?", (computer_id,))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    def show_qr_code_image(self):
        qr_image = self.qr_image.resize((200, 200))
        qr_image = ImageTk.PhotoImage(qr_image)
        self.qr_code_image_label.configure(image=qr_image)
        self.qr_code_image_label.image = qr_image

    def print_qr_code(self):
        if self.qr_image:
            try:
                self.qr_image.show()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to print QR Code: {e}")
        else:
            messagebox.showwarning("Warning", "Please generate a QR Code first.")

    def save_qr_code(self):
        if self.qr_image:
            try:
                file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
                if file_path:
                    self.qr_image.save(file_path)
                    messagebox.showinfo("Success", "QR Code saved as image successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save QR Code as image: {e}")
        else:
            messagebox.showwarning("Warning", "Please generate a QR Code first.")

def main():
    root = tk.Tk()
    app = QRCodeGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
