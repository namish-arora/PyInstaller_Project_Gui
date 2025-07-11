import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image,ImageTk

class CustomToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tip_window or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, background="#ffffe0", relief="solid", borderwidth=1, font=("Aerial", 10))
        label.pack(ipadx=5, ipady=2)

    def hide_tip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None


# making gui using tkinter..
root = tk.Tk()
root.title("PyInstaller GUI")
root.geometry("600x1000")

icon = Image.open("ansys_logo_2.jpg").resize((45,45),Image.Resampling.LANCZOS)
icon_image = ImageTk.PhotoImage(icon)
root.iconphoto(False,icon_image)

root.icon_image = icon_image


label = tk.Label(root,text="Welcome to the Pyinstaller GUI Packager",font=("Aerial", 16))
label.pack(pady=20)


# Create a StringVar for app name
app_name_var = tk.StringVar()

# Label
app_name_label = tk.Label(root, text="Enter Application name: ", font=("Arial", 12))
app_name_label.pack(anchor=tk.W, padx=20, pady=5)

# Entry with StringVar binding
app_name_entry = tk.Entry(root, textvariable=app_name_var, width=40, bd=2, font=("Arial", 10))
app_name_entry.pack(anchor=tk.W, padx=20, pady=5)


CustomToolTip(app_name_entry, "Enter the name of your application here.\nThis will be used as the executable name.")

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
browse_button = tk.Button(root, text="Browse", command=browse_folder,fg="black",bg="aqua", width = 10,font=("Arial", 10))
browse_button.pack(anchor=W, padx=20, pady=5)

CustomToolTip(browse_button, "Click to select the folder containing your Python project.\nThis folder should contain the main .py file.")

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

border_frame = tk.Frame(root,bd=2,relief=SOLID)
border_frame.pack(anchor=W,padx=20,pady=20)

# Dropdown menu
entry_dropdown = tk.OptionMenu(border_frame, entry_file_var, "")
entry_dropdown.pack(anchor=tk.W, padx=20, pady=5)

CustomToolTip(entry_dropdown,text="Select the main Python file to be packaged.\nThis should be the entry point of your application.")

# Trigger update when folder is selected
folder_path_var.trace_add("write", update_entry_dropdown)


# Function to browse for Python executable
def browse_python_exe():
    exe_path = filedialog.askopenfilename(title="Select Python Executable", filetypes=[("Python Executable", "python.exe")])
    if exe_path:
        python_exe_var.set(exe_path)

# Variable to store Python executable path
python_exe_var = tk.StringVar()

# Label
python_exe_label = tk.Label(root, text="Select Python Executable:", font=("Arial", 12))
python_exe_label.pack(anchor=tk.W, padx=20, pady=(10, 0))

# Browse button
python_exe_button = tk.Button(root, text="Browse", command=browse_python_exe,fg="black",bg="aqua",width = 10, font=("Arial", 10))
python_exe_button.pack(anchor=tk.W, padx=20, pady=5)

CustomToolTip(python_exe_button, "Click to select the Python executable.\nThis is required to run PyInstaller.")

# Display selected path
python_exe_display = tk.Label(root, textvariable=python_exe_var, wraplength=450, fg="blue")
python_exe_display.pack(anchor=tk.W, padx=20)



preview_label = tk.Label(root, text="Project Folder Contents:", font=("Aerial", 12))
preview_label.pack(anchor=tk.W, padx=20, pady=(10, 0))

text_frame = tk.Frame(root, height=200, width=500)
text_frame.pack(padx=20, pady=5)

text_widget = tk.Text(text_frame, wrap="word", height=10, width=40)

scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)

text_widget.config(yscrollcommand=scrollbar.set)

scrollbar.pack(side=tk.RIGHT,fill = tk.Y)
text_widget.pack(side=tk.LEFT)

# Function to update preview
def update_folder_preview(*args):
    folder = folder_path_var.get()
    text_widget.delete("1.0", tk.END)
    if folder and os.path.isdir(folder):
        for root_dir, dirs, files in os.walk(folder):
            level = root_dir.replace(folder, '').count(os.sep)
            indent = ' ' * 4 * level
            text_widget.insert(tk.END, f"{indent}📁 {os.path.basename(root_dir)}\n")
            sub_indent = ' ' * 4 * (level + 1)
            for f in files:
                text_widget.insert(tk.END, f"{sub_indent}📄 {f}\n")

# Trigger preview update when folder is selected
folder_path_var.trace_add("write", update_folder_preview)


mode_var_file = tk.StringVar(value="onefile") # by default 
Label(root,text="Select a packaging mode:", font=("Arial", 12)).pack(anchor=W,padx=20,pady=10)

# making a frame to place label and radio buttons
radio_frame = tk.Frame(root)
radio_frame.pack(anchor=tk.W, padx=20, pady=5)

onefile_radio = tk.Radiobutton(radio_frame,text="Onefile(--onefile)",variable=mode_var_file, value="onefile", font=("Arial", 10))
onefile_radio.pack(side=tk.LEFT, padx=10)

CustomToolTip(onefile_radio, "Select this option to create a single executable file.\nThis is useful for distributing your application as one file.")

onefolder_radio = tk.Radiobutton(radio_frame,text="Onefolder(--onedir)",variable=mode_var_file, value="onefolder", font=("Arial", 10))
onefolder_radio.pack(side=tk.LEFT, padx=10)

CustomToolTip(onefolder_radio, "Select this option to create a folder containing all files.\nThis is useful for debugging or if your app has multiple files.")

#same for option for console or windowed

mode_var_console = tk.StringVar(value="console") #by default
Label(root,text="Select a console mode:", font=("Arial", 12)).pack(anchor=W,padx=20)

#making a frame to place radio button for console or windowed
console_frame = tk.Frame(root)
console_frame.pack(anchor=tk.W, padx=20, pady=5)

console_radio = tk.Radiobutton(console_frame,text="console based",variable=mode_var_console,value="console",font=("Aerial",10))
console_radio.pack(side=tk.LEFT, padx=10)

CustomToolTip(console_radio, "Select this option to run the application in console mode.\nThis is useful for applications that require console input/output.")

window_radio = tk.Radiobutton(console_frame,text="window based",variable=mode_var_console,value="window",font=("Aerial",10))
window_radio.pack(side=tk.LEFT, padx=10)

CustomToolTip(window_radio, "Select this option to run the application in windowed mode.\nThis is useful for GUI applications that do not require a console.")




#label for displaying current command
Label(root,text="Current Command:", font=("Arial", 12)).pack(anchor=W, padx=20, pady=(10, 0))


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




# Function to run PyInstaller with the selected options

def update_command_preview(*args):
    app_name = app_name_entry.get()
    entry_file = entry_file_var.get()
    folder_path = folder_path_var.get()
    python_exe = python_exe_var.get()
    mode_file = mode_var_file.get()
    mode_console = mode_var_console.get()

    if not app_name or not entry_file or not folder_path or not python_exe:
        command_text.delete("1.0", tk.END)
        command_text.insert(tk.END, "Please fill all fields to generate the command.")
        return

    entry_path = os.path.join(folder_path, entry_file)
    command = [
        python_exe,
        "-m", "PyInstaller",
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



import subprocess

def run_pyinstaller():
    app_name = app_name_entry.get()
    entry_file = entry_file_var.get()
    folder_path = folder_path_var.get()
    python_exe = python_exe_var.get()
    mode_file = mode_var_file.get()
    mode_console = mode_var_console.get()

    if not app_name or not entry_file or not folder_path or not python_exe:
        messagebox.showerror("Error", "Please fill all fields before running PyInstaller.")
        return

    entry_path = os.path.join(folder_path, entry_file)
    
    command = [
        python_exe,
        "-m", "PyInstaller",
        "--name", app_name,
       
        entry_path
    ]

    # Update command text area
    if mode_file == "onefile":
        command.append("--onefile")
    else:
        command.append("--onedir")
    if mode_console == "console":
        command.append("--console")
    else:
        command.append("--windowed")

    # Clear and insert the command into the text area

    command_text.delete("1.0", tk.END)
    command_text.insert(tk.END, ' '.join(command))

    try:
        subprocess.run(command, check=True)
        messagebox.showinfo("Success", f"App '{app_name}' packaged successfully!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Packaging failed:\n{e}")


package_button = tk.Button(root, text="Package App",width=40, command=run_pyinstaller, bg="green", fg="white", font=("Arial", 12))
package_button.pack(pady=20)

root.mainloop()

