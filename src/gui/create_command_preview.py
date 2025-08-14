import os
import tkinter as tk
from tkinter import Label


def create_command_preview_with_display(root,app_name_var, folder_path_var, entry_file_var, python_exe_var, mode_var_file, mode_var_console):
    # Create a frame for command preview
    Label(root,text="Current Command:", font=("Aerial", 12)).pack(anchor=tk.W, padx=20, pady=(10, 0))
    #first create a frame to hold text area and scrollbar
    command_frame = tk.Frame(root)
    command_frame.pack(anchor=tk.W, padx=40, pady=5)
    # Text area to display command
    command_text = tk.Text(command_frame, height=3, width=70, wrap="none", bd=2, font=("Arial", 10),fg="blue")
    # Scrollbar for the text area
    scrollbar = tk.Scrollbar(command_frame, orient="horizontal", command=command_text.xview)

    scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    command_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    command_text.configure(xscrollcommand=scrollbar.set)

              


    # Function to update the command preview
    def update_command_preview(*args):
        app_name = app_name_var.get().strip()
        entry_file = entry_file_var.get().strip()
        folder_path = folder_path_var.get().strip()
        python_exe = python_exe_var.get().strip()
        mode_file = mode_var_file.get().strip()
        mode_console = mode_var_console.get().strip()

      

        if not app_name or not entry_file or not folder_path or not python_exe:
            command_text.delete("1.0", tk.END)
            command_text.insert(tk.END, "Please fill all fields to generate the command.")
            return

        entry_path = os.path.join(folder_path, entry_file)
        command = [
            "pyinstaller",
            "--name", app_name,
            entry_path
        ]

        if mode_file == "onefile":
            command.append("--onefile")
        else:
            command.append("--onedir")

        if mode_console == "console":
            command.append("--console")
        else:
            command.append("--windowed")

        
    
        command_text.delete("1.0", tk.END)
        command_text.insert(tk.END, ' '.join(command))



    app_name_var.trace_add("write", update_command_preview)

    entry_file_var.trace_add("write", update_command_preview)
    folder_path_var.trace_add("write", update_command_preview)
    python_exe_var.trace_add("write", update_command_preview)
    mode_var_file.trace_add("write", update_command_preview)
    mode_var_console.trace_add("write", update_command_preview)

    update_command_preview


