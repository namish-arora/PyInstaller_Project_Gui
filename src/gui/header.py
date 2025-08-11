import tkinter as tk

# from src.utils.image_loader import load_image

from ..utils.image_loader import load_image

def load_header_with_label(root):
    # Frame for logo and welcome text
    logo_frame = tk.Frame(root)
    logo_frame.pack(anchor=tk.W, padx=20, pady=(20, 30))

    # Python logo
    python_logo_image = load_image("python_logo.png", (50, 50))
    python_logo_label = tk.Label(logo_frame, image=python_logo_image)
    python_logo_label.image = python_logo_image
    python_logo_label.pack(side=tk.LEFT, padx=(0, 10))

    # Welcome text
    welcome_text = tk.Label(logo_frame, text="PyInstaller GUI Packager", font=("Arial", 18))
    welcome_text.pack(side=tk.LEFT)

    
