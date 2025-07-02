import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

# making gui using tkinter..
root = tk.Tk()
root.title("PyInstaller GUI")
root.geometry("500x500")

label = tk.Label(root,text="Welcome to the Pyinstaller GUI Packager",font=("Aerial", 16))
label.pack(pady=20)

#added app name label
app_name_label = tk.Label(root,text = "enter Application name: ", font=("Aerial", 12))
app_name_label.pack(anchor=W,padx=20, pady=5)


#added app name entry
app_name_entry = Entry(root, width=40)
app_name_entry.pack(anchor=W, padx=20, pady=5)


# Function to browse folder
def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path_var.set(folder_selected)

# Folder selection label
folder_label = tk.Label(root, text="Select Project Folder:", font=("Arial", 12))
folder_label.pack(anchor='w', padx=20, pady=(10, 0))

# Variable to store folder path
folder_path_var = tk.StringVar()

# Button to browse folder
browse_button = tk.Button(root, text="Browse", command=browse_folder)
browse_button.pack(anchor=W, padx=20, pady=5)

# Label to display selected folder path
folder_path_display = tk.Label(root, textvariable=folder_path_var, wraplength=450, fg="blue")
folder_path_display.pack(anchor=W, padx=20)


import os

# Function to update dropdown with .py files from selected folder
def update_entry_dropdown(*args):
    folder = folder_path_var.get()
    if folder:
        py_files = [f for f in os.listdir(folder) if f.endswith(".py")]
        if py_files:
            entry_file_var.set(py_files[0])  # Set default
            entry_dropdown['menu'].delete(0, 'end')
            for file in py_files:
                entry_dropdown['menu'].add_command(label=file, command=tk._setit(entry_file_var, file))
        else:
            entry_file_var.set("No .py files found")

# Variable to store selected entry file
entry_file_var = tk.StringVar()
entry_file_var.set("Select entry file")

# Label
entry_label = tk.Label(root, text="Select Entry Point (.py file):", font=("Arial", 12))
entry_label.pack(anchor=tk.W, padx=20, pady=(10, 0))

# Dropdown menu
entry_dropdown = tk.OptionMenu(root, entry_file_var, "")
entry_dropdown.pack(anchor=tk.W, padx=20, pady=5)

# Trigger update when folder is selected
folder_path_var.trace_add("write", update_entry_dropdown)


root.mainloop()

