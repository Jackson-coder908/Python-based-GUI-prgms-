import tkinter as tk
from tkinter import ttk
from datetime import datetime

# ─────────────────────────────────────────
#  THEME
# ─────────────────────────────────────────
BG     = "#1a1a2e"
CARD   = "#16213e"
ACCENT = "#0f3460"
FG     = "#e0e0e0"
GREEN  = "#00ff99"
YELLOW = "#ffd700"
ORANGE = "#ff8c00"
RED    = "#ff4444"
BLUE   = "#4488ff"
PURPLE = "#b44fff"

# ─────────────────────────────────────────
#  ROOT
# ─────────────────────────────────────────
root = tk.Tk()
root.title("BMI Calculator Pro")
root.geometry("520x700")
root.resizable(False, False)
root.configure(bg=BG)

# ─────────────────────────────────────────
#  TITLE
# ─────────────────────────────────────────
tk.Label(root, text="BMI CALCULATOR", font=("Courier", 20, "bold"),
         bg=BG, fg=GREEN).pack(pady=(20, 2))
tk.Label(root, text="with History & Ideal Weight",
         font=("Courier", 10), bg=BG, fg="#888888").pack()

# ─────────────────────────────────────────
#  NOTEBOOK
# ─────────────────────────────────────────
style = ttk.Style()
style.theme_use("default")
style.configure("TNotebook",        background=BG, borderwidth=0)
style.configure("TNotebook.Tab",    background=CARD, foreground=FG,
                padding=[14, 6], font=("Courier", 10))
style.map("TNotebook.Tab",          background=[("selected", ACCENT)],
                                    foreground=[("selected", GREEN)])

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=16, pady=10)

tab_calc    = tk.Frame(notebook, bg=BG)
tab_history = tk.Frame(notebook, bg=BG)
tab_ideal   = tk.Frame(notebook, bg=BG)

notebook.add(tab_calc,    text="  📊 Calculator  ")
notebook.add(tab_history, text="  📋 History  ")
notebook.add(tab_ideal,   text="  🎯 Ideal Weight  ")

# ═════════════════════════════════════════
#  TAB 1 — CALCULATOR
# ═════════════════════════════════════════

# Unit toggle
unit_var = tk.StringVar(value="metric")
unit_frame = tk.Frame(tab_calc, bg=BG)
unit_frame.pack(pady=10)

def toggle_units():
    is_metric = unit_var.get() == "metric"
    for w in metric_fields:
        if is_metric: w.master.pack(fill="x", pady=5)
        else:         w.master.pack_forget()
    for w in imperial_fields:
        if not is_metric: w.master.pack(fill="x", pady=5)
        else:             w.master.pack_forget()
    gender_row.pack_forget()
    gender_row.pack(fill="x", pady=5)

def make_unit_btn(text, value):
    return tk.Radiobutton(unit_frame, text=text, variable=unit_var,
                          value=value, font=("Courier", 10),
                          bg=CARD, fg=FG, selectcolor=ACCENT,
                          activebackground=CARD, activeforeground=GREEN,
                          relief="flat", padx=12, pady=5,
                          command=toggle_units, indicatoron=False)

make_unit_btn("  Metric (kg/cm)  ", "metric").pack(side="left", padx=4)
make_unit_btn("  Imperial (lb/ft) ", "imperial").pack(side="left", padx=4)

# Input card
input_card = tk.Frame(tab_calc, bg=CARD, padx=24, pady=14)
input_card.pack(padx=20, fill="x")

def make_row(parent, label):
    row = tk.Frame(parent, bg=CARD)
    row.pack(fill="x", pady=5)
    tk.Label(row, text=label, font=("Courier", 11),
             bg=CARD, fg="#aaaaaa", width=18, anchor="w").pack(side="left")
    e = tk.Entry(row, font=("Courier", 13, "bold"),
                 bg=ACCENT, fg=GREEN, insertbackground=GREEN,
                 relief="flat", width=10, justify="center")
    e.pack(side="left", padx=6)
    return e

name_entry   = make_row(input_card, "Name (optional)")
age_entry    = make_row(input_card, "Age (years)")
weight_entry = make_row(input_card, "Weight (kg)")
height_entry = make_row(input_card, "Height (cm)")

weight_imp   = make_row(input_card, "Weight (lbs)")
ft_entry     = make_row(input_card, "Height (ft)")
in_entry     = make_row(input_card, "Height (in)")

gender_row = tk.Frame(input_card, bg=CARD)
gender_row.pack(fill="x", pady=5)
tk.Label(gender_row, text="Gender", font=("Courier", 11),
         bg=CARD, fg="#aaaaaa", width=18, anchor="w").pack(side="left")
gender_var = tk.StringVar(value="male")
for g in ["Male", "Female"]:
    tk.Radiobutton(gender_row, text=g, variable=gender_var,
                   value=g.lower(), font=("Courier", 11),
                   bg=CARD, fg=FG, selectcolor=ACCENT,
                   activebackground=CARD, relief="flat").pack(side="left", padx=6)

metric_fields   = [age_entry, weight_entry, height_entry]
imperial_fields = [weight_imp, ft_entry, in_entry]

# Result area
result_frame = tk.Frame(tab_calc, bg=CARD, padx=20, pady=14)
result_frame.pack(padx=20, pady=10, fill="x")

bmi_label      = tk.Label(result_frame, text="--",
                           font=("Courier", 52, "bold"), bg=CARD, fg=GREEN)
bmi_label.pack()

category_label = tk.Label(result_frame, text="Enter your details above",
                           font=("Courier", 13), bg=CARD, fg="#888888")
category_label.pack()

ideal_result   = tk.Label(result_frame, text="",
                           font=("Courier", 11), bg=CARD, fg=PURPLE)
ideal_result.pack(pady=2)

advice_label   = tk.Label(result_frame, text="",
                           font=("Courier", 10), bg=CARD, fg="#888888",
                           wraplength=420, justify="center")
advice_label.pack(pady=4)

# Scale bar
canvas = tk.Canvas(tab_calc, height=30, bg=BG, highlightthickness=0)
canvas.pack(padx=20, fill="x")

def draw_scale(bmi_val=None):
    canvas.update_idletasks()
    w = canvas.winfo_width() or 460
    segs = [(10,18.5,BLUE),(18.5,25,GREEN),(25,30,YELLOW),(30,35,ORANGE),(35,40,RED)]
    lo, hi = 10, 40
    for s, e, c in segs:
        x1 = (s-lo)/(hi-lo)*w
        x2 = (e-lo)/(hi-lo)*w
        canvas.create_rectangle(x1, 8, x2, 22, fill=c, outline="")
    if bmi_val:
        mx = (max(lo,min(hi,bmi_val))-lo)/(hi-lo)*w
        canvas.create_polygon(mx-7,6, mx+7,6, mx,24, fill="white", outline="")

lbl_row = tk.Frame(tab_calc, bg=BG)
lbl_row.pack(padx=20, fill="x")
for txt, col in [("Underweight",BLUE),("Normal",GREEN),("Overweight",YELLOW),("Obese",RED)]:
    tk.Label(lbl_row, text=txt, font=("Courier", 8), bg=BG, fg=col).pack(side="left", expand=True)

# Calculate button
tk.Button(tab_calc, text="  CALCULATE BMI  ",
          font=("Courier", 13, "bold"),
          bg=GREEN, fg=BG, relief="flat",
          padx=16, pady=9, cursor="hand2",
          command=lambda: calculate()).pack(pady=10)

# ─────────────────────────────────────────
#  BMI LOGIC
# ─────────────────────────────────────────
history_data = []

def get_category(bmi):
    if bmi < 18.5: return "Underweight", BLUE,   "Consider increasing caloric intake with nutritious foods."
    if bmi < 25.0: return "Normal",      GREEN,  "Great! Maintain your healthy lifestyle."
    if bmi < 30.0: return "Overweight",  YELLOW, "Consider more physical activity and a balanced diet."
    if bmi < 35.0: return "Obese Class I",  ORANGE, "Consult a healthcare provider for a weight management plan."
    return             "Obese Class II", RED,    "Please seek medical advice for a structured health plan."

def ideal_weight_range(height_m, gender):
    # Hamwi formula
    if gender == "male":
        base = 48.0 + 2.7 * ((height_m * 100 / 2.54) - 60)
    else:
        base = 45.5 + 2.2 * ((height_m * 100 / 2.54) - 60)
    low  = round(max(base * 0.9, 40), 1)
    high = round(base * 1.1, 1)
    return low, high

def calculate():
    try:
        name   = name_entry.get().strip() or "Unknown"
        age    = age_entry.get().strip()

        if unit_var.get() == "metric":
            weight_kg = float(weight_entry.get())
            height_m  = float(height_entry.get()) / 100
        else:
            weight_kg = float(weight_imp.get()) * 0.453592
            ft        = float(ft_entry.get())
            inch      = float(in_entry.get()) if in_entry.get().strip() else 0
            height_m  = (ft * 12 + inch) * 0.0254

        if height_m <= 0 or weight_kg <= 0:
            raise ValueError

        bmi = weight_kg / (height_m ** 2)
        cat, color, advice = get_category(bmi)

        # Ideal weight
        gender  = gender_var.get()
        iw_low, iw_high = ideal_weight_range(height_m, gender)
        diff    = round(weight_kg - (iw_low + iw_high) / 2, 1)
        diff_txt = (f"Lose {abs(diff)} kg to reach ideal range"
                    if diff > 0 else
                    f"Gain {abs(diff)} kg to reach ideal range"
                    if diff < 0 else "You're right in the ideal range!")

        # Update UI
        bmi_label.config(text=f"{bmi:.1f}", fg=color)
        category_label.config(text=cat, fg=color)
        ideal_result.config(
            text=f"🎯 Ideal weight: {iw_low}–{iw_high} kg  |  {diff_txt}")
        advice_label.config(text=advice)
        draw_scale(bmi)

        # Log to history
        entry = {
            "name":     name,
            "age":      age,
            "bmi":      round(bmi, 1),
            "category": cat,
            "weight":   round(weight_kg, 1),
            "height":   round(height_m * 100, 1),
            "ideal":    f"{iw_low}–{iw_high} kg",
            "time":     datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        history_data.append(entry)
        refresh_history()

    except ValueError:
        bmi_label.config(text="--", fg=GREEN)
        category_label.config(text="Invalid input — check your values", fg=RED)
        ideal_result.config(text="")
        advice_label.config(text="")
        draw_scale()

# ═════════════════════════════════════════
#  TAB 2 — HISTORY
# ═════════════════════════════════════════
tk.Label(tab_history, text="Calculation History",
         font=("Courier", 14, "bold"), bg=BG, fg=GREEN).pack(pady=(16, 6))

cols = ("Time", "Name", "BMI", "Category", "Weight", "Ideal")
tree_frame = tk.Frame(tab_history, bg=BG)
tree_frame.pack(padx=16, fill="both", expand=True)

style.configure("Treeview",
                background=CARD, foreground=FG,
                fieldbackground=CARD, rowheight=26,
                font=("Courier", 10))
style.configure("Treeview.Heading",
                background=ACCENT, foreground=GREEN,
                font=("Courier", 10, "bold"))
style.map("Treeview", background=[("selected", ACCENT)])

tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=12)
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=80, anchor="center")
tree.column("Time",     width=120)
tree.column("Category", width=100)
tree.column("Ideal",    width=90)
tree.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
scrollbar.pack(side="right", fill="y")
tree.configure(yscrollcommand=scrollbar.set)

btn_row = tk.Frame(tab_history, bg=BG)
btn_row.pack(pady=10)

def refresh_history():
    tree.delete(*tree.get_children())
    for h in reversed(history_data):
        tree.insert("", "end", values=(
            h["time"], h["name"], h["bmi"],
            h["category"], f"{h['weight']} kg", h["ideal"]
        ))

def clear_history():
    history_data.clear()
    refresh_history()

tk.Button(btn_row, text="  🗑 Clear History  ",
          font=("Courier", 11), bg=CARD, fg=RED,
          relief="flat", padx=10, pady=5,
          command=clear_history).pack(side="left", padx=6)

tk.Button(btn_row, text="  📋 Copy Selected  ",
          font=("Courier", 11), bg=CARD, fg=FG,
          relief="flat", padx=10, pady=5,
          command=lambda: copy_selected()).pack(side="left", padx=6)

def copy_selected():
    sel = tree.selection()
    if not sel: return
    vals = tree.item(sel[0])["values"]
    root.clipboard_clear()
    root.clipboard_append("  |  ".join(str(v) for v in vals))

# ═════════════════════════════════════════
#  TAB 3 — IDEAL WEIGHT REFERENCE
# ═════════════════════════════════════════
tk.Label(tab_ideal, text="Ideal Weight Reference",
         font=("Courier", 14, "bold"), bg=BG, fg=GREEN).pack(pady=(16, 4))
tk.Label(tab_ideal, text="Based on Hamwi Formula",
         font=("Courier", 10), bg=BG, fg="#888888").pack()

# Quick lookup
lookup_frame = tk.Frame(tab_ideal, bg=CARD, padx=20, pady=14)
lookup_frame.pack(padx=20, pady=12, fill="x")

tk.Label(lookup_frame, text="Enter height to look up ideal range:",
         font=("Courier", 11), bg=CARD, fg="#aaaaaa").pack(anchor="w")

lrow = tk.Frame(lookup_frame, bg=CARD)
lrow.pack(fill="x", pady=8)

tk.Label(lrow, text="Height (cm)", font=("Courier", 11),
         bg=CARD, fg="#aaaaaa", width=14, anchor="w").pack(side="left")
lookup_ht = tk.Entry(lrow, font=("Courier", 13, "bold"),
                     bg=ACCENT, fg=GREEN, insertbackground=GREEN,
                     relief="flat", width=8, justify="center")
lookup_ht.pack(side="left", padx=6)

lookup_gender = tk.StringVar(value="male")
for g in ["Male", "Female"]:
    tk.Radiobutton(lrow, text=g, variable=lookup_gender,
                   value=g.lower(), font=("Courier", 11),
                   bg=CARD, fg=FG, selectcolor=ACCENT,
                   activebackground=CARD, relief="flat").pack(side="left", padx=4)

lookup_result = tk.Label(lookup_frame, text="",
                          font=("Courier", 13, "bold"),
                          bg=CARD, fg=PURPLE)
lookup_result.pack(pady=6)

def do_lookup():
    try:
        h_m = float(lookup_ht.get()) / 100
        lo, hi = ideal_weight_range(h_m, lookup_gender.get())
        mid = round((lo + hi) / 2, 1)
        lookup_result.config(
            text=f"Ideal range: {lo} – {hi} kg  (midpoint {mid} kg)")
    except ValueError:
        lookup_result.config(text="Enter a valid height in cm")

tk.Button(lookup_frame, text="  Look Up  ",
          font=("Courier", 11), bg=GREEN, fg=BG,
          relief="flat", padx=10, pady=5,
          command=do_lookup).pack()

# Reference table
tk.Label(tab_ideal, text="Quick Reference Table",
         font=("Courier", 12, "bold"), bg=BG, fg=FG).pack(pady=(10, 4))

ref_cols = ("Height (cm)", "Male (kg)", "Female (kg)")
ref_tree = ttk.Treeview(tab_ideal, columns=ref_cols,
                         show="headings", height=9)
for col in ref_cols:
    ref_tree.heading(col, text=col)
    ref_tree.column(col, width=140, anchor="center")
ref_tree.pack(padx=20, fill="x")

for cm in range(150, 196, 5):
    h = cm / 100
    ml, mh = ideal_weight_range(h, "male")
    fl, fh = ideal_weight_range(h, "female")
    ref_tree.insert("", "end", values=(
        cm, f"{ml}–{mh}", f"{fl}–{fh}"))

# ─────────────────────────────────────────
#  INIT
# ─────────────────────────────────────────
toggle_units()
root.after(100, draw_scale)
root.mainloop()
