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
folder_label = tk.Label(root, text="Select the folder containing your Python files:", font=("Aerial", 12))
folder_label.pack(anchor='w', padx=20, pady=(10, 0))

# Variable to store folder path
folder_path_var = tk.StringVar()

# Button to browse folder
browse_button = tk.Button(root, text="Browse", command=browse_folder)
browse_button.pack(anchor=W, padx=20, pady=5)

# Label to display selected folder path
folder_path_display = tk.Label(root, textvariable=folder_path_var, wraplength=450, fg="blue")
folder_path_display.pack(anchor=W, padx=20)

root.mainloop()

