import tkinter as tk

window = tk.Tk()
window.title("Vaporwaver")
window.geometry("1280x720")
window.resizable(width=False, height=False)

left_frame = tk.Frame(window)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

image = tk.PhotoImage(file="picts/background/default.png")

preview_label = tk.Label(left_frame)
preview_label.configure(image=image)
preview_label.image = image

preview_label.place(x=40, y=50, width=460, height=555)

import_button = tk.Button(left_frame, text="Import")
import_button.place(x=40, y=555+60, width=460)

right_frame = tk.Frame(window)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

range_1 = tk.Scale(right_frame, from_=0, to=100, orient=tk.HORIZONTAL)
range_1.pack()
range_2 = tk.Scale(right_frame, from_=0, to=100, orient=tk.HORIZONTAL)
range_2.pack()
range_3 = tk.Scale(right_frame, from_=0, to=100, orient=tk.HORIZONTAL)
range_3.pack()
range_4 = tk.Scale(right_frame, from_=0, to=100, orient=tk.HORIZONTAL)
range_4.pack()

select_frame = tk.Frame(right_frame)
select_frame.pack()
label_1 = tk.Label(select_frame, text="Foreground:")
label_1.pack(side=tk.LEFT)

select_1_var = tk.StringVar(select_frame)
select_1_var.set("Option 1")
select_1 = tk.OptionMenu(select_frame, select_1_var, "Option 1", "Option 2", "Option 3")
select_1.pack(side=tk.LEFT)

label_2 = tk.Label(select_frame, text="Background 2:")
label_2.pack(side=tk.LEFT)

select_2_var = tk.StringVar(select_frame)
select_2_var.set("Option 1")
select_2 = tk.OptionMenu(select_frame, select_2_var, "Option 1", "Option 2", "Option 3")
select_2.pack(side=tk.LEFT)

range_5 = tk.Scale(right_frame, from_=0, to=100, orient=tk.HORIZONTAL)
range_5.pack()
range_6 = tk.Scale(right_frame, from_=0, to=100, orient=tk.HORIZONTAL)
range_6.pack()
range_7 = tk.Scale(right_frame, from_=0, to=100, orient=tk.HORIZONTAL)
range_7.pack()
range_8 = tk.Scale(right_frame, from_=0, to=100, orient=tk.HORIZONTAL)
range_8.pack()

# run the main loop
window.mainloop()