import tkinter as tk
import time

def update_clock():
    current_time = time.strftime('%H:%M:%S')
    clock_label.config(text=current_time)
    clock_label.after(1000, update_clock)

root = tk.Tk()
clock_label = tk.Label(root, font=('Arial', 24))
clock_label.pack()

update_clock()

root.mainloop()