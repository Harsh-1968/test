import tkinter as tk
from tkinter import filedialog, messagebox

class NotebookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Notebook")
        self.root.geometry("700x500")
        self.root.config(bg="#ECF0F1")  # Set background color for the window

        # Title Label
        self.title_label = tk.Label(self.root, text="My Notebook", font=("Helvetica", 24, "bold"), bg="#2C3E50", fg="#ECF0F1", pady=20)
        self.title_label.pack(fill='x')

        # Create a Text widget for writing notes
        self.text_area = tk.Text(self.root, width=80, height=20, font=("Helvetica", 12), wrap="word", bg="#FFFFFF", fg="#2C3E50", padx=10, pady=10, bd=2, relief="solid")
        self.text_area.pack(padx=20, pady=20)

        # Button frame
        self.button_frame = tk.Frame(self.root, bg="#ECF0F1")
        self.button_frame.pack(pady=10)

        # Save button with styling
        self.save_button = tk.Button(self.button_frame, text="Save", command=self.save_note, font=("Helvetica", 12), bg="#3498DB", fg="#FFFFFF", relief="flat", width=12, height=2)
        self.save_button.grid(row=0, column=0, padx=10)

        # Load button with styling
        self.load_button = tk.Button(self.button_frame, text="Load", command=self.load_note, font=("Helvetica", 12), bg="#2ECC71", fg="#FFFFFF", relief="flat", width=12, height=2)
        self.load_button.grid(row=0, column=1, padx=10)

        # Clear button with styling
        self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.clear_note, font=("Helvetica", 12), bg="#E74C3C", fg="#FFFFFF", relief="flat", width=12, height=2)
        self.clear_button.grid(row=0, column=2, padx=10)

    def save_note(self):
        # Open file dialog to select where to save the note
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        
        if file_path:
            try:
                # Get the text from the Text widget
                note_content = self.text_area.get("1.0", tk.END).strip()
                if not note_content:
                    messagebox.showwarning("No Content", "There is no content to save!")
                    return
                with open(file_path, 'w') as file:
                    file.write(note_content)
                messagebox.showinfo("Success", "Note saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save note: {str(e)}")

    def load_note(self):
        # Open file dialog to select a file to load
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

        if file_path:
            try:
                # Read the file and display its content in the Text widget
                with open(file_path, 'r') as file:
                    note_content = file.read()
                self.text_area.delete("1.0", tk.END)  # Clear any existing content
                self.text_area.insert(tk.END, note_content)  # Insert the loaded content
                messagebox.showinfo("Success", "Note loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load note: {str(e)}")

    def clear_note(self):
        # Clear the text area
        self.text_area.delete("1.0", tk.END)

# Create the main window for Tkinter
root = tk.Tk()
app = NotebookApp(root)
root.mainloop()
