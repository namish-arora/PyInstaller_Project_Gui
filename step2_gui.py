# making gui uisng tkinter..
import tkinter as tk
from tkinter import *
from tkinter import messagebox

root = tk.Tk()
root.title("PyInstaller GUI")
root.geometry("500x500")

label = tk.Label(root,text="Welcome to the Pyinstaller GUI Packager",font=("Aerial", 16))
label.pack(pady=20)

#added app name label
app_name_label = tk.Label(root,text = "enter Application name: ", font=("Aerial", 12))
app_name_label.pack(anchor=W,padx=20, pady=5)

#added app name entry
app_name_entry = Entry(root, width=40)
app_name_entry.pack(anchor=W, padx=20, pady=5)


root.mainloop()