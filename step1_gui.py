# making gui uisng tkinter..
import tkinter as tk
from tkinter import *
from tkinter import messagebox

root = tk.Tk()
root.title("PyInstaller GUI")
root.geometry("500x500")

label = tk.Label(root,text="Welcome to the Pyinstaller GUI Packager",font=("Aerial", 16))
label.pack(pady=20)

root.mainloop()