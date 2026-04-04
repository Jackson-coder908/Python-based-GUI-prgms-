import tkinter as tk
from tkinter import messagebox

def add_numbers():
    try:
        num1 = float(entry1.get())
        num2 = float(entry2.get())
        result = num1 + num2
        label_result.config(text=f"Result: {result}", fg="green")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers")

# 1. Create Window
root = tk.Tk()
root.title("KTU S6 Simple Adder")
root.geometry("300x250")

# 2. UI Elements
tk.Label(root, text="Enter Number 1:").pack(pady=5)
entry1 = tk.Entry(root)
entry1.pack()

tk.Label(root, text="Enter Number 2:").pack(pady=5)
entry2 = tk.Entry(root)
entry2.pack()

# 3. Button with Command
btn_add = tk.Button(root, text="Add", command=add_numbers, bg="blue", fg="white")
btn_add.pack(pady=20)

label_result = tk.Label(root, text="Result: ", font=("Arial", 12, "bold"))
label_result.pack()

# 4. Start Application
root.mainloop()
