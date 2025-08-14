import tkinter as tk
from tkinter import Toplevel, Label



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





class HoverTooltip:
    def __init__(self, listbox):
        self.listbox = listbox
        self.tooltip = None
        self.listbox.bind("<Motion>", self.on_hover)
        self.listbox.bind("<Leave>", self.hide_tooltip)

    def on_hover(self, event):
        index = self.listbox.nearest(event.y)
        if index >= 0:
            text = self.listbox.get(index)
            self.show_tooltip(text, event)

    def show_tooltip(self, text, event):
        self.hide_tooltip()
        self.tooltip = Toplevel(self.listbox)
        self.tooltip.wm_overrideredirect(True)
        x = event.x_root + 10
        y = event.y_root + 10
        self.tooltip.geometry(f"+{x}+{y}")
        label = Label(self.tooltip, text=text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


