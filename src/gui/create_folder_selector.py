from src.tools.core_libs import *
from src.tools.ui_libs import *
from src.utils.custom_tooltip import CustomToolTip
from src.utils.image_loader import load_image

def create_folder_selector_with_display(root):
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
    folder_icon_image = load_image("folder_icon.png", (25, 25))
    folder_icon_label = tk.Label(folder_frame, image=folder_icon_image)
    folder_icon_label.image = folder_icon_image  # Keep a reference to avoid garbage collection
    folder_icon_label.pack(side=tk.LEFT, padx=(0, 10))  # Add some space between icon and label

    # Variable to store folder path
    folder_path_var = tk.StringVar()
    # Button to browse folder
    browse_button = tk.Button(folder_frame, text="Browse", command=browse_folder, fg="black", bg="aqua", width=20, font=("Arial", 10))
    browse_button.pack(side=tk.LEFT, padx=10)
    CustomToolTip(browse_button, "Click to select the folder containing your Python project.\nThe main.py should be present in the src subfolder.")

        #make a frame to show to the TextArea and the copy icon beside it
    text_frame = tk.Frame(root)
    text_frame.pack(anchor=tk.W, padx=20, pady=5)
    #give me a text area to display the folder path
    folder_path_display = tk.Text(text_frame, height=2, width=70, wrap="word", bd=2, font=("Aerial", 10), fg="blue")


    folder_path_display.pack(side=tk.LEFT, fill=tk.BOTH)

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
    copy_icon_image = load_image("copy_icon.png", (20, 20))
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

    # Return the folder path variable for further use
    return folder_path_var