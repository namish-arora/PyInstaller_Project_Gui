import tkinter as tk
from tkinter import ttk
import os
import glob

from ..utils.custom_tooltip import CustomToolTip
from ..utils.image_loader import load_image

def find_python_executables():
    """Search common directories for python executables."""
    python_paths = set()

    # Common Windows install locations
    possible_dirs = [
        os.environ.get("ProgramFiles", ""),
        os.environ.get("ProgramFiles(x86)", ""),
        os.environ.get("LocalAppData", ""),
        os.path.expanduser("~\\AppData\\Local\\Programs"),
        "C:\\Python*",
    ]

    for base_dir in possible_dirs:
        if base_dir and os.path.exists(base_dir):
            matches = glob.glob(os.path.join(base_dir, "**", "python.exe"), recursive=True)
            for match in matches:
                python_paths.add(os.path.normpath(match))

    # Also check PATH environment variable
    for path_dir in os.environ.get("PATH", "").split(os.pathsep):
        exe_path = os.path.join(path_dir.strip('"'), "python.exe")
        if os.path.exists(exe_path):
            python_paths.add(os.path.normpath(exe_path))

    return sorted(python_paths)

def create_python_exe_selector_with_display(root):
    python_frame = tk.Frame(root)
    python_frame.pack(anchor=tk.W, padx=20, pady=10)

    python_exe_var = tk.StringVar()

    # Top row: Label and icon side-by-side
    top_row = tk.Frame(python_frame)
    top_row.pack(anchor=tk.W)

    python_exe_label = tk.Label(top_row, text="Select Python Exe:", font=("Arial", 12))
    python_exe_label.pack(side=tk.LEFT)

    python_icon_image = load_image("python_file.png", (25, 25))
    python_icon_label = tk.Label(top_row, image=python_icon_image)
    python_icon_label.image = python_icon_image
    python_icon_label.pack(side=tk.LEFT, padx=(5, 10))

    # Bottom row: Combobox below the label and icon
    python_exe_dropdown = ttk.Combobox(python_frame, textvariable=python_exe_var, width=80, font=("Arial", 10))
    python_exe_dropdown['values'] = find_python_executables()
    python_exe_dropdown.pack(anchor=tk.W, pady=(5, 0))

    CustomToolTip(python_exe_dropdown, "Select the Python executable.\nThis is required to run PyInstaller.")

    # Display selected path
    # python_exe_text_frame = tk.Frame(root)
    # python_exe_text_frame.pack(anchor=tk.W, padx=20, pady=5)

    # python_exe_display = tk.Text(python_exe_text_frame, height=2, width=70, wrap="word", bd=2, font=("Arial", 10), fg="blue")
    # python_exe_display.pack(side=tk.LEFT, fill=tk.BOTH)

    # def update_python_exe_display(*args):
    #     python_exe = python_exe_var.get()
    #     python_exe_display.delete("1.0", tk.END)
    #     if python_exe:
    #         python_exe_display.insert(tk.END, python_exe)
    #     else:
    #         python_exe_display.insert(tk.END, "No Python executable selected")

    # python_exe_var.trace_add("write", update_python_exe_display)
    # update_python_exe_display()

    # # Copy icon and functionality
    # copy_icon_image = load_image("copy_icon.png", (20, 20))
    # copy_icon_label = tk.Label(python_exe_text_frame, image=copy_icon_image)
    # copy_icon_label.image = copy_icon_image
    # copy_icon_label.pack(side=tk.LEFT, padx=(10, 0))

    # def copy_python_exe():
    #     python_exe = python_exe_var.get()
    #     if python_exe:
    #         root.clipboard_clear()
    #         root.clipboard_append(python_exe)
    #         messagebox.showinfo("Copied", "Python executable path copied to clipboard!")
    #     else:
    #         messagebox.showwarning("Warning", "No Python executable path to copy.")

    # copy_icon_label.bind("<Button-1>", lambda e: copy_python_exe())
    # CustomToolTip(copy_icon_label, "Click to copy")

    return python_exe_var

