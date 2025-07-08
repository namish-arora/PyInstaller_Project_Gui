import tkinter as tk
from PIL import Image, ImageTk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog


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
root.geometry("600x900")


# original_image = Image.open("python_logo.png")
# # Resize the image to fit the label
# resized_image = original_image.resize((100, 100), Image.ANTIALIAS)
# # Convert the image to PhotoImage
# image_photo = ImageTk.PhotoImage(resized_image)
# # Create a label to display the image
# image_label = tk.Label(root, image=image_photo)

# image_label.pack(pady=10)


label = tk.Label(root,text="Welcome to the Pyinstaller GUI Packager",font=("Aerial", 16))
label.pack(pady=20)



#added app name label
app_name_label = tk.Label(root,text = "Enter Application name: ", font=("Aerial", 12))
app_name_label.pack(anchor=W,padx=20, pady=5)


app_name_entry = tk.Entry(root, width=40)
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
browse_button = tk.Button(root, text="Browse", command=browse_folder)
browse_button.pack(anchor=W, padx=20, pady=5)

CustomToolTip(browse_button, "Click to select the folder containing your Python project.\nThis folder should contain your .py files.")

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
python_exe_button = tk.Button(root, text="Browse", command=browse_python_exe)
python_exe_button.pack(anchor=tk.W, padx=20, pady=5)

CustomToolTip(python_exe_button, "Click to select the Python executable.\nThis is required to run PyInstaller.")

# Display selected path
python_exe_display = tk.Label(root, textvariable=python_exe_var, wraplength=450, fg="blue")
python_exe_display.pack(anchor=tk.W, padx=20)


# Label for file preview
preview_label = tk.Label(root, text="Project Folder Contents:", font=("Arial", 12))
preview_label.pack(anchor=tk.W, padx=20, pady=(10, 0))

# Scrollable text widget to show folder contents
preview_text = tk.Text(root, height=10, width=60, wrap="none")
preview_text.pack(padx=20, pady=5)

# Scrollbar
scroll_y = tk.Scrollbar(root, orient="vertical", command=preview_text.yview)
scroll_y.pack(side="right", fill="y")
preview_text.configure(yscrollcommand=scroll_y.set)

# Function to update preview
def update_folder_preview(*args):
    folder = folder_path_var.get()
    preview_text.delete("1.0", tk.END)
    if folder and os.path.isdir(folder):
        for root_dir, dirs, files in os.walk(folder):
            level = root_dir.replace(folder, '').count(os.sep)
            indent = ' ' * 4 * level
            preview_text.insert(tk.END, f"{indent}📁 {os.path.basename(root_dir)}\n")
            sub_indent = ' ' * 4 * (level + 1)
            for f in files:
                preview_text.insert(tk.END, f"{sub_indent}📄 {f}\n")

# Trigger preview update when folder is selected
folder_path_var.trace_add("write", update_folder_preview)


#step 5: Adding a button to run PyInstaller
def run_pyinstaller(): 
    app_name = app_name_entry.get()
    entry_file = entry_file_var.get()
    folder_path = folder_path_var.get()
    python_exe = python_exe_var.get()

    if not app_name or not entry_file or not folder_path or not python_exe:
        messagebox.showerror("Error", "Please fill all fields before running PyInstaller.")
        return

    command = f'"{python_exe}" -m PyInstaller --name "{app_name}" --onefile "{os.path.join(folder_path, entry_file)}"'
    
    
    messagebox.showinfo("Command to Run", command)



#radio buttons to select packaing options like onefile or onefolder
# Packaging options
mode_var_file = tk.StringVar(value="onefile") # by default 
Label(root,text="Select a packaging mode:", font=("Arial", 12)).pack(anchor=W,padx=20)

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

package_button = tk.Button(root, text="Package App",width=40 ,command=run_pyinstaller, bg="green", fg="white", font=("Aerial", 12))
package_button.pack(pady=40)

root.mainloop()

