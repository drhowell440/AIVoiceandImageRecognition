import tkinter as tk
from tkinter import simpledialog

def get_name_popup():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    user_input = simpledialog.askstring("Input", "New face detected. Please provide a name or press Enter to skip:")
    root.destroy()
    return user_input

print(get_name_popup())
