import tkinter as tk
from tkinter import filedialog, messagebox


from src.utils.custom_tooltip import CustomToolTip
from src.utils.image_loader import load_image

def create_python_exe_selector_with_display(root):
    # Function to browse for Python executable
    def browse_python_exe():
        exe_path = filedialog.askopenfilename(title="Select Python Executable", filetypes=[("Python Executable", "python.exe")])
        if exe_path:
            python_exe_var.set(exe_path)


    python_frame = tk.Frame(root)
    python_frame.pack(anchor=tk.W,padx=20,pady=20)

    python_exe_var = tk.StringVar()
    # python_exe_var.set("Select Python Executable")

    python_exe_label = tk.Label(python_frame,text="Select Python Exe:",font=("Aerial",12))
    python_exe_label.pack(side=tk.LEFT)

    #python file icon add
    python_icon_image = load_image("python_file.png", (25, 25))
    python_icon_label = tk.Label(python_frame, image=python_icon_image)
    python_icon_label.image = python_icon_image  # Keep a reference to avoid garbage collection
    python_icon_label.pack(side=tk.LEFT, padx=(0, 10))  # Add some space between icon and label

    # Browse button

    python_exe_button = tk.Button(python_frame,text="Browse",command=browse_python_exe,fg="black",bg="aqua",width = 20,font=("Arial",10))
    python_exe_button.pack(side=tk.LEFT,padx=10)

    CustomToolTip(python_exe_button, "Click to select the Python executable.\nThis is required to run PyInstaller.")

    #add text area to display pytohnexe path and copy icon beside it to copy yo clipboard
    python_exe_text_frame = tk.Frame(root)
    python_exe_text_frame.pack(anchor=tk.W, padx=20, pady=5)
    python_exe_display = tk.Text(python_exe_text_frame, height=2, width=70, wrap="word", bd=2, font=("Arial", 10), fg="blue")

    python_exe_display.pack(side=tk.LEFT, fill=tk.BOTH)


    # Function to update the Python executable display
    def update_python_exe_display(*args):
        python_exe = python_exe_var.get()
        if python_exe:
            python_exe_display.delete("1.0", tk.END)  # Clear previous text
            python_exe_display.insert(tk.END, python_exe)  # Insert new path
        else:
            python_exe_display.delete("1.0", tk.END)
            python_exe_display.insert(tk.END, "No Python executable selected")  # Default message

    # Trigger update when Python executable changes
    python_exe_var.trace_add("write", update_python_exe_display)

    # Update the display initially
    update_python_exe_display()

    #add a copy icon to copy the python exe path to clipboard
    copy_icon_image = load_image("copy_icon.png", (20, 20))
    copy_icon_label = tk.Label(python_exe_text_frame, image=copy_icon_image)
    copy_icon_label.image = copy_icon_image  # Keep a reference to avoid garbage collection
    copy_icon_label.pack(side=tk.LEFT, padx=(10, 0))  # Add some space between text area and icon

    # Function to copy Python executable path to clipboard
    def copy_python_exe():
        python_exe = python_exe_var.get()
        if python_exe:
            root.clipboard_clear()  # Clear the clipboard
            root.clipboard_append(python_exe)  # Append the Python executable path to the clipboard
            messagebox.showinfo("Copied", "Python executable path copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No Python executable path to copy.")

    # Bind the copy icon to the copy function
    copy_icon_label.bind("<Button-1>", lambda e: copy_python_exe())  # Left-click to copy Python executable path
    CustomToolTip(copy_icon_label,"click to copy")

    return python_exe_var  # Return the variable for further use
