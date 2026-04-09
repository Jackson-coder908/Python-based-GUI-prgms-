import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import shutil

class FileManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Manager")
        self.geometry("800x500")
        self.current_path = tk.StringVar(value=os.path.expanduser("~"))
        self.setup_ui()
        self.load_directory()

    def setup_ui(self):
        # --- Top bar ---
        top = tk.Frame(self)
        top.pack(fill="x", padx=5, pady=5)

        tk.Button(top, text="⬆ Up", command=self.go_up).pack(side="left")
        tk.Button(top, text="🏠 Home", command=self.go_home).pack(side="left")
        tk.Entry(top, textvariable=self.current_path, width=60).pack(side="left", padx=5)
        tk.Button(top, text="Go", command=self.load_directory).pack(side="left")

        # --- Treeview ---
        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True, padx=5)

        cols = ("Name", "Type", "Size")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings")
        for col in cols:
            self.tree.heading(col, text=col)
        self.tree.column("Name", width=400)
        self.tree.column("Type", width=100)
        self.tree.column("Size", width=100)

        scroll = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self.tree.bind("<Double-1>", self.on_double_click)

        # --- Bottom buttons ---
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x", padx=5, pady=5)

        tk.Button(btn_frame, text="New Folder", command=self.new_folder).pack(side="left", padx=2)
        tk.Button(btn_frame, text="Delete", command=self.delete_item).pack(side="left", padx=2)
        tk.Button(btn_frame, text="Rename", command=self.rename_item).pack(side="left", padx=2)
        tk.Button(btn_frame, text="Copy", command=self.copy_item).pack(side="left", padx=2)
        tk.Button(btn_frame, text="Paste", command=self.paste_item).pack(side="left", padx=2)

        self.clipboard = None
        self.status = tk.Label(self, text="", anchor="w")
        self.status.pack(fill="x", padx=5)

    def load_directory(self):
        path = self.current_path.get()
        if not os.path.isdir(path):
            messagebox.showerror("Error", "Invalid path")
            return
        self.tree.delete(*self.tree.get_children())
        try:
            items = os.listdir(path)
            for name in sorted(items):
                full = os.path.join(path, name)
                if os.path.isdir(full):
                    ftype = "Folder"
                    size = ""
                else:
                    ftype = os.path.splitext(name)[1] or "File"
                    size = f"{os.path.getsize(full)} B"
                self.tree.insert("", "end", values=(name, ftype, size))
            self.status.config(text=f"{len(items)} items in {path}")
        except PermissionError:
            messagebox.showerror("Error", "Permission denied")

    def on_double_click(self, event):
        selected = self.tree.focus()
        if not selected:
            return
        name = self.tree.item(selected)["values"][0]
        full = os.path.join(self.current_path.get(), name)
        if os.path.isdir(full):
            self.current_path.set(full)
            self.load_directory()

    def go_up(self):
        parent = os.path.dirname(self.current_path.get())
        self.current_path.set(parent)
        self.load_directory()

    def go_home(self):
        self.current_path.set(os.path.expanduser("~"))
        self.load_directory()

    def new_folder(self):
        win = tk.Toplevel(self)
        win.title("New Folder")
        tk.Label(win, text="Folder name:").pack(padx=10, pady=5)
        entry = tk.Entry(win, width=30)
        entry.pack(padx=10)
        def create():
            name = entry.get().strip()
            if name:
                os.makedirs(os.path.join(self.current_path.get(), name), exist_ok=True)
                self.load_directory()
                win.destroy()
        tk.Button(win, text="Create", command=create).pack(pady=5)

    def delete_item(self):
        selected = self.tree.focus()
        if not selected:
            return
        name = self.tree.item(selected)["values"][0]
        full = os.path.join(self.current_path.get(), name)
        if messagebox.askyesno("Delete", f"Delete '{name}'?"):
            if os.path.isdir(full):
                shutil.rmtree(full)
            else:
                os.remove(full)
            self.load_directory()

    def rename_item(self):
        selected = self.tree.focus()
        if not selected:
            return
        old_name = self.tree.item(selected)["values"][0]
        win = tk.Toplevel(self)
        win.title("Rename")
        tk.Label(win, text="New name:").pack(padx=10, pady=5)
        entry = tk.Entry(win, width=30)
        entry.insert(0, old_name)
        entry.pack(padx=10)
        def do_rename():
            new_name = entry.get().strip()
            if new_name:
                os.rename(
                    os.path.join(self.current_path.get(), old_name),
                    os.path.join(self.current_path.get(), new_name)
                )
                self.load_directory()
                win.destroy()
        tk.Button(win, text="Rename", command=do_rename).pack(pady=5)

    def copy_item(self):
        selected = self.tree.focus()
        if not selected:
            return
        name = self.tree.item(selected)["values"][0]
        self.clipboard = os.path.join(self.current_path.get(), name)
        self.status.config(text=f"Copied: {name}")

    def paste_item(self):
        if not self.clipboard:
            return
        dest = os.path.join(self.current_path.get(), os.path.basename(self.clipboard))
        if os.path.isdir(self.clipboard):
            shutil.copytree(self.clipboard, dest)
        else:
            shutil.copy2(self.clipboard, dest)
        self.load_directory()

app = FileManager()
app.mainloop()
