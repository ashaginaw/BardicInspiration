import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil

def get_selected_file():
    """Open a file dialog and return the selected file."""
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("MIDI files", "*.mid")])
    root.destroy()  # Destroy the root window after file selection
    return file_path

def show_message(title, message):
    """Display a message box with the given title and message."""
    messagebox.showinfo(title, message)

def save_file(source_file, destination_folder):
    """Code allows the user to select a MIDI file and have it save into the database (MIDI Music)"""
    try:
        if source_file:
            file_name = os.path.basename(source_file)
            destination_path = os.path.join(destination_folder, file_name)
            
            if os.path.abspath(source_file) != os.path.abspath(destination_path):
                shutil.copy(source_file, destination_path)
                return True, f"File '{file_name}' has been accepted and saved to 'MIDI Music' successfully."
            else:
                return False, "Source and destination paths are the same."
        else:
            return False, "No file selected."
    except Exception as e:
        return False, str(e)

def select_and_save_file():
    """Function to select a MIDI file and save it."""
    # Specify the path to the "MIDI Music Folder"
    destination_folder = "MIDI Music"
    
    # Ask the user to select a MIDI file
    source_file = get_selected_file()
    
    if source_file:
        success, message = save_file(source_file, destination_folder)
        if success:
            show_message("File Accepted", message)
        else:
            show_message("Error", message)
    else:
        show_message("Error", "No file selected.")

def on_close(root):
    root.destroy()

def setup_gui(on_close=None):
    root = tk.Tk()
    root.title("Save MIDI File")

    canvas = tk.Canvas(root, width=500, height=250, bg="lightgray")
    canvas.create_text(250, 100, font=("Fixedsys", 11), fill="Grey1",
                       text="Click the button to select a MIDI file\nand save it to 'MIDI Music'",
                       justify="center")
    canvas.pack()

    custom_font = ("Helvetica", 9)

    upload_button = tk.Button(root, text="Select MIDI File", command=select_and_save_file, font=custom_font)
    upload_button.pack()

    if on_close:
        root.protocol("WM_DELETE_WINDOW", on_close)  # Pass on_close function if provided
    else:
        root.protocol("WM_DELETE_WINDOW", root.destroy)

    root.mainloop()

if __name__ == "__main__":
   setup_gui()
