import tkinter as tk



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