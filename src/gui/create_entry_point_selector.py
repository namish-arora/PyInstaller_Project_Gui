import tkinter as tk
import os

from src.utils.custom_tooltip import CustomToolTip




def create_entry_point_selector_with_display(root, folder_path_var):
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

    #frame to hold the label and dropdown menu
    entry_frame = tk.Frame(root)
    entry_frame.pack(anchor=tk.W,padx=20,pady=(10,0))
    # Label for entry file selection
    entry_label = tk.Label(entry_frame,text="Select Entry Point(.py file)",font=("Aerial",12))
    entry_label.pack(side=tk.LEFT)

    entry_dropdown = tk.OptionMenu(entry_frame, entry_file_var, "Select entry file")
    entry_dropdown.config(width=30, font=("Arial", 10), bd=2, fg="blue")
    entry_dropdown.pack(side=tk.LEFT, padx=10)
    CustomToolTip(entry_dropdown, "Select the main Python file to be packaged.\nThis should be the entry point of your application.")

    # Trigger update when folder is selected
    folder_path_var.trace_add("write", update_entry_dropdown)

    return entry_file_var  # Return the variable for further use


  