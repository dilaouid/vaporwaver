import tkinter as tk

def defineField(title: str, selects):
    label = tk.Label(selects, text=title+":")
    label.pack(side=tk.LEFT)

    var = tk.StringVar(selects)
    var.set("Option 1")
    element = tk.OptionMenu(selects, var, "Option 1", "Option 2", "Option 3")
    element.pack(side=tk.LEFT)