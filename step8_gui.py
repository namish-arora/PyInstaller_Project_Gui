import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image,ImageTk
from tkinter import ttk
import subprocess



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




class CustomRadioButton(tk.Frame):
    def __init__(self, master, text, variable, value, size=20, **kwargs):
        super().__init__(master, **kwargs)
        self.variable = variable
        self.value = value
        self.size = size

        self.canvas = tk.Canvas(self, width=size+10, height=size+10, highlightthickness=0)
        self.canvas.pack(side="left")
        self.label = tk.Label(self, text=text)
        self.label.pack(side="left", padx=5)

        self.canvas.bind("<Button-1>", self.select)
        self.label.bind("<Button-1>", self.select)

        self.draw_circle()

    def draw_circle(self):
        self.canvas.delete("all")
        x0, y0 = 5, 5
        x1, y1 = x0 + self.size, y0 + self.size
        self.canvas.create_oval(x0, y0, x1, y1, outline="black", width=2)
        if self.variable.get() == self.value:
            self.canvas.create_oval(x0+5, y0+5, x1-5, y1-5, fill="blue")

    def select(self, event=None):
        self.variable.set(self.value)
        self.master.update_buttons()

class CustomRadioGroup(tk.Frame):
    def __init__(self, master, options, variable=None, **kwargs):
        super().__init__(master, **kwargs)
        self.variable = variable if variable else tk.StringVar(value=options[0][1])
        self.buttons = []
        for text, value in options:
            btn = CustomRadioButton(self, text, self.variable, value)
            btn.pack(side="left", padx=10)
            self.buttons.append(btn)

    def update_buttons(self):
        for btn in self.buttons:
            btn.draw_circle()



# making gui using tkinter..
root = tk.Tk()
root.title("PyInstaller GUI")
root.geometry("600x1000")

icon = Image.open("ansys_logo_2.jpg").resize((45,45),Image.Resampling.LANCZOS)
icon_image = ImageTk.PhotoImage(icon)
root.iconphoto(False,icon_image)

root.icon_image = icon_image

#make a frame to place python logo , welcome text and toggle button neatly
# Frame for logo and welcome text
logo_frame = tk.Frame(root)  # Set background color to gray90
logo_frame.pack(anchor=tk.W, padx=20, pady=(20,30))
# Python logo
python_logo = Image.open("python_logo.png").resize((25,25), Image.Resampling.LANCZOS)
python_logo_image = ImageTk.PhotoImage(python_logo)
python_logo_label = tk.Label(logo_frame, image=python_logo_image)
python_logo_label.image = python_logo_image  # Keep a reference to avoid garbage collection
python_logo_label.pack(side=tk.LEFT, padx=(0, 10))  # Add some space between logo and text

# Welcome text
welcome_text = tk.Label(logo_frame, text="PyInstaller GUI Packager", font=("Arial", 18))
welcome_text.pack(side=tk.LEFT)





# label = tk.Label(root,text="Pyinstaller GUI Packager",font=("Aerial", 16))
# label.pack(pady=20)

# style = ttk.Style()
# dark_mode = False

# # Toggle button placed at top-right
# toggle_btn = ttk.Button(root, text="🌙", command=toggle_theme)
# toggle_btn.place(relx=1.0, x=-10, y=10, anchor="ne")  # Top-right with 10px padding

# Create a StringVar for app name
app_name_var = tk.StringVar()


app_frame = tk.Frame(root)  # Frame for app name entry
app_frame.pack(anchor=tk.W, padx=20, pady=5)

app_name_label = tk.Label(app_frame, text="Enter Application name: ", font=("Arial", 12))
app_name_label.pack(side=tk.LEFT)

app_name_entry = tk.Entry(app_frame, textvariable=app_name_var, width=40, bd=2, font=("Arial", 10), fg="blue")
app_name_entry.pack(side=tk.RIGHT, padx=10)


CustomToolTip(app_name_entry, "Enter the name of your application here.\nThis will be used as the executable name.")

# Function to browse folder
def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path_var.set(folder_selected)



folder_frame = tk.Frame(root)
folder_frame.pack(anchor=tk.W, padx=20, pady=20)
# Folder selection label
folder_label = tk.Label(folder_frame, text="Select Project Folder:", font=("Arial", 12))
folder_label.pack(side=tk.LEFT)
# Folder icon
folder_icon = Image.open("folder_icon.png").resize((20, 20), Image.Resampling.LANCZOS)
folder_icon_image = ImageTk.PhotoImage(folder_icon)
folder_icon_label = tk.Label(folder_frame, image=folder_icon_image)
folder_icon_label.image = folder_icon_image  # Keep a reference to avoid garbage collection
folder_icon_label.pack(side=tk.LEFT, padx=(0, 10))  # Add some space between icon and label

# Variable to store folder path
folder_path_var = tk.StringVar()
# Button to browse folder
browse_button = tk.Button(folder_frame, text="Browse", command=browse_folder, fg="black", bg="aqua", width=20, font=("Arial", 10))
browse_button.pack(side=tk.LEFT, padx=10)
CustomToolTip(browse_button, "Click to select the folder containing your Python project.\nThis folder should contain the main .py file.")

folder_path_var.set("No folder selected")  # Default message

#make a frame to show to the TextArea and the copy icon beside it
text_frame = tk.Frame(root)
text_frame.pack(anchor=tk.W, padx=20, pady=5)
#give me a text area to display the folder path
folder_path_display = tk.Text(text_frame, height=2, width=70, wrap="word", bd=2, font=("Arial", 10), fg="blue")


# Scrollbar for the text area
# scrollbar = tk.Scrollbar(text_frame, orient="horizontal", command=folder_path_display.xview)
# scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
folder_path_display.pack(side=tk.LEFT, fill=tk.BOTH)

# folder_path_display.configure(xscrollcommand=scrollbar.set)

# Function to update the folder path display
def update_folder_path_display(*args):
    folder_path = folder_path_var.get()
    if folder_path:
        folder_path_display.delete("1.0", tk.END)  # Clear previous text
        folder_path_display.insert(tk.END, folder_path)  # Insert new path
    else:
        folder_path_display.delete("1.0", tk.END)
        folder_path_display.insert(tk.END, "No folder selected")  # Default message

# Trigger update when folder path changes
folder_path_var.trace_add("write", update_folder_path_display)
# Update the display initially
update_folder_path_display()

#add a copy icon to copy the folder path to clipboard
copy_icon = Image.open("copy_icon.png").resize((20, 20), Image.Resampling.LANCZOS)
copy_icon_image = ImageTk.PhotoImage(copy_icon)
copy_icon_label = tk.Label(text_frame, image=copy_icon_image)
copy_icon_label.image = copy_icon_image  # Keep a reference to avoid garbage collection
copy_icon_label.pack(side=tk.LEFT, padx=(10, 0))  # Add some space between text area and icon

# Function to copy folder path to clipboard
def copy_folder_path():
    folder_path = folder_path_var.get()
    if folder_path:
        root.clipboard_clear()  # Clear the clipboard
        root.clipboard_append(folder_path)  # Append the folder path to the clipboard
        messagebox.showinfo("Copied", "Folder path copied to clipboard!")
    else:
        messagebox.showwarning("Warning", "No folder path to copy.")

# Bind the copy icon to the copy function
copy_icon_label.bind("<Button-1>", lambda e: copy_folder_path())  # Left-click to copy folder path

CustomToolTip(copy_icon_label,"click to copy")



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

border_frame = tk.Frame(root,bd=2,relief=SOLID,)
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


python_frame = tk.Frame(root)
python_frame.pack(anchor=W,padx=20,pady=20)

python_exe_var = tk.StringVar()
python_exe_var.set("Select Python Executable")

python_exe_label = tk.Label(python_frame,text="Select Python Exe:",font=("Aerial",12))
python_exe_label.pack(side=tk.LEFT)

#python file icon add
python_icon = Image.open("python_file.png").resize((25,25), Image.Resampling.LANCZOS)
python_icon_image = ImageTk.PhotoImage(python_icon)
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
# Scrollbar for the text area
# scrollbar = tk.Scrollbar(python_exe_text_frame, orient="horizontal", command=python_exe_display.xview)
# scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
python_exe_display.pack(side=tk.LEFT, fill=tk.BOTH)
# python_exe_display.configure(xscrollcommand=scrollbar.set)

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
copy_icon = Image.open("copy_icon.png").resize((20, 20), Image.Resampling.LANCZOS)
copy_icon_image = ImageTk.PhotoImage(copy_icon)
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









preview_label = tk.Label(root, text="Project Folder Contents:", font=("Aerial", 12))
preview_label.pack(anchor=tk.W, padx=20, pady=(10, 0))

text_frame = tk.Frame(root, height=200, width=500)
text_frame.pack(padx=20, pady=5)

text_widget = tk.Text(text_frame, wrap="word", height=7, width=40)

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
#make a frame to place label and radio buttons side by side and use the custom class to size the circles of radio buttons
mode_frame = tk.Frame(root)
mode_frame.pack(anchor=tk.W, padx=10, pady=(20,5))
# Options for packaging mode
options = [
    ("Onefile (--onefile)", "onefile"),
    ("Onefolder (--onedir)", "onefolder")
]
Label(mode_frame,text="Select a packaging mode:",font=("Arial", 12)).pack(side=tk.LEFT, padx=(4,2))
# Create custom radio buttons

radio_group = CustomRadioGroup(mode_frame, options, variable=mode_var_file)
radio_group.pack(side=tk.LEFT, padx=2)


#CustomToolTip(radio_group, "Select the packaging mode for your application.\nOnefile creates a single executable file,\nwhile Onefolder creates a folder with all necessary files.")

#same for window and console radio buttons
mode_var_console = tk.StringVar(value="console") # by default
mode_frame_console = tk.Frame(root)
mode_frame_console.pack(anchor=tk.W, padx=10, pady=(20,5))
# Options for console mode
options_console = [
    ("Console (--console)", "console"),
    ("Windowed (--windowed)", "windowed")
]
# Label for console mode
Label(mode_frame_console,text="Select a console mode:",font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
# Create custom radio buttons for console mode

radio_group_console = CustomRadioGroup(mode_frame_console, options_console, variable=mode_var_console)
radio_group_console.pack(side=tk.LEFT, padx=10)


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
    #i want the command in not in such a big 1 line instead in 2 lines
    
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


def add_text_area():
    # Create a new Text widget and place it above the button
    text_area = tk.Text(root, height=1, width=40)
    text_area.pack(pady=5, before=package_button)  # 'before=btn' places it above the button

def wrapper_function():
    run_pyinstaller()
    add_text_area()

# Button to run PyInstaller
package_button = tk.Button(root, text="Package  Application", command=wrapper_function, fg="white", bg="green", width=40, font=("Aerial", 12))
package_button.pack(pady=20)



root.mainloop()
