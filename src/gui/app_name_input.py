from src.tools.ui_libs import *
from src.utils.custom_tooltip import CustomToolTip

def create_app_name_input(root):
    app_name_var = tk.StringVar()


    app_frame = tk.Frame(root)  # Frame for app name entry
    app_frame.pack(anchor=tk.W, padx=20, pady=5)

    app_name_label = tk.Label(app_frame, text="Enter Application name: ", font=("Arial", 12))
    app_name_label.pack(side=tk.LEFT)

    app_name_entry = tk.Entry(app_frame, textvariable=app_name_var, width=40, bd=2, font=("Arial", 10), fg="blue")
    app_name_entry.pack(side=tk.RIGHT, padx=10)


    CustomToolTip(app_name_entry, "Enter the name of your application here.\nThis will be used as the executable name.")

    return app_name_var  # Return the variable 