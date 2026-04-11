import tkinter as tk
from tkinter import ttk, messagebox
from time import strftime
import winsound  # Windows only; see note below for cross-platform

# ─────────────────────────────────────────
#  THEME
# ─────────────────────────────────────────
DARK  = {"bg": "#1a1a2e", "fg": "#00ff99", "sub": "#aaaaaa", "btn": "#16213e", "accent": "#0f3460"}
LIGHT = {"bg": "#f0f0f0", "fg": "#111111", "sub": "#555555", "btn": "#dddddd", "accent": "#4488ff"}
theme = DARK

# ─────────────────────────────────────────
#  ROOT
# ─────────────────────────────────────────
root = tk.Tk()
root.title("Clock App")
root.geometry("480x360")
root.resizable(False, False)
root.configure(bg=theme["bg"])

# ─────────────────────────────────────────
#  NOTEBOOK (TABS)
# ─────────────────────────────────────────
style = ttk.Style()
style.theme_use("default")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

tab_clock     = tk.Frame(notebook, bg=theme["bg"])
tab_stopwatch = tk.Frame(notebook, bg=theme["bg"])
tab_alarm     = tk.Frame(notebook, bg=theme["bg"])

notebook.add(tab_clock,     text="  🕐 Clock  ")
notebook.add(tab_stopwatch, text="  ⏱ Stopwatch  ")
notebook.add(tab_alarm,     text="  🔔 Alarm  ")

# ─────────────────────────────────────────
#  TAB 1 — CLOCK
# ─────────────────────────────────────────
time_label = tk.Label(tab_clock, font=("Courier", 58, "bold"),
                      bg=theme["bg"], fg=theme["fg"])
time_label.pack(expand=True)

date_label = tk.Label(tab_clock, font=("Courier", 15),
                      bg=theme["bg"], fg=theme["sub"])
date_label.pack()

toggle_btn = tk.Button(tab_clock, text="☀ Light Mode", font=("Courier", 11),
                       bg=theme["btn"], fg=theme["fg"], relief="flat",
                       padx=10, pady=4)
toggle_btn.pack(pady=12)

def update_clock():
    time_label.config(text=strftime("%H:%M:%S"))
    date_label.config(text=strftime("%A, %B %d %Y"))
    root.after(1000, update_clock)

# ─────────────────────────────────────────
#  TAB 2 — STOPWATCH
# ─────────────────────────────────────────
sw_running   = False
sw_elapsed   = 0.0
sw_start_ref = 0

sw_display = tk.Label(tab_stopwatch, text="00:00:00.0",
                      font=("Courier", 50, "bold"),
                      bg=theme["bg"], fg=theme["fg"])
sw_display.pack(pady=(30, 10))

lap_box = tk.Listbox(tab_stopwatch, font=("Courier", 11),
                     bg=theme["accent"], fg=theme["fg"],
                     selectbackground=theme["btn"],
                     height=4, relief="flat", bd=0)
lap_box.pack(fill="x", padx=40)

sw_btn_frame = tk.Frame(tab_stopwatch, bg=theme["bg"])
sw_btn_frame.pack(pady=10)

def format_sw(seconds):
    h  = int(seconds // 3600)
    m  = int((seconds % 3600) // 60)
    s  = int(seconds % 60)
    ds = int((seconds * 10) % 10)
    return f"{h:02}:{m:02}:{s:02}.{ds}"

def sw_tick():
    if sw_running:
        import time
        elapsed = sw_elapsed + (time.time() - sw_start_ref)
        sw_display.config(text=format_sw(elapsed))
        root.after(100, sw_tick)

def sw_start_stop():
    global sw_running, sw_start_ref, sw_elapsed
    import time
    if not sw_running:
        sw_start_ref = time.time()
        sw_running = True
        start_stop_btn.config(text="  ⏸ Stop  ")
        sw_tick()
    else:
        sw_elapsed += time.time() - sw_start_ref
        sw_running = False
        start_stop_btn.config(text="  ▶ Start  ")

def sw_reset():
    global sw_running, sw_elapsed
    sw_running = False
    sw_elapsed = 0.0
    sw_display.config(text="00:00:00.0")
    start_stop_btn.config(text="  ▶ Start  ")
    lap_box.delete(0, "end")

def sw_lap():
    if sw_running:
        import time
        elapsed = sw_elapsed + (time.time() - sw_start_ref)
        n = lap_box.size() + 1
        lap_box.insert("end", f"  Lap {n:02}:  {format_sw(elapsed)}")
        lap_box.yview("end")

start_stop_btn = tk.Button(sw_btn_frame, text="  ▶ Start  ",
                            font=("Courier", 12), bg=theme["btn"],
                            fg=theme["fg"], relief="flat",
                            padx=8, pady=4, command=sw_start_stop)
start_stop_btn.grid(row=0, column=0, padx=6)

lap_btn = tk.Button(sw_btn_frame, text="  🏁 Lap  ",
                    font=("Courier", 12), bg=theme["btn"],
                    fg=theme["fg"], relief="flat",
                    padx=8, pady=4, command=sw_lap)
lap_btn.grid(row=0, column=1, padx=6)

reset_btn = tk.Button(sw_btn_frame, text="  ↺ Reset  ",
                      font=("Courier", 12), bg=theme["btn"],
                      fg=theme["fg"], relief="flat",
                      padx=8, pady=4, command=sw_reset)
reset_btn.grid(row=0, column=2, padx=6)

# ─────────────────────────────────────────
#  TAB 3 — ALARM
# ─────────────────────────────────────────
alarm_time = None

alarm_title = tk.Label(tab_alarm, text="Set Alarm (HH:MM)",
                       font=("Courier", 14), bg=theme["bg"], fg=theme["sub"])
alarm_title.pack(pady=(30, 6))

alarm_entry = tk.Entry(tab_alarm, font=("Courier", 28, "bold"),
                       width=6, justify="center",
                       bg=theme["accent"], fg=theme["fg"],
                       insertbackground=theme["fg"], relief="flat")
alarm_entry.insert(0, "07:00")
alarm_entry.pack()

alarm_status = tk.Label(tab_alarm, text="No alarm set",
                        font=("Courier", 12), bg=theme["bg"], fg=theme["sub"])
alarm_status.pack(pady=8)

alarm_btn_frame = tk.Frame(tab_alarm, bg=theme["bg"])
alarm_btn_frame.pack()

def set_alarm():
    global alarm_time
    val = alarm_entry.get().strip()
    try:
        h, m = val.split(":")
        assert 0 <= int(h) <= 23 and 0 <= int(m) <= 59
        alarm_time = val
        alarm_status.config(text=f"⏰ Alarm set for {alarm_time}", fg="#00ff99")
    except:
        alarm_status.config(text="Invalid time! Use HH:MM", fg="#ff4444")

def clear_alarm():
    global alarm_time
    alarm_time = None
    alarm_status.config(text="No alarm set", fg=theme["sub"])

def check_alarm():
    if alarm_time and strftime("%H:%M") == alarm_time:
        messagebox.showinfo("⏰ Alarm!", f"Alarm ringing: {alarm_time}")
        try:
            winsound.Beep(1000, 1000)  # Windows only
        except:
            print("\a")  # fallback beep
        clear_alarm()
    root.after(10000, check_alarm)

set_btn = tk.Button(alarm_btn_frame, text="  ✔ Set Alarm  ",
                    font=("Courier", 12), bg=theme["btn"],
                    fg=theme["fg"], relief="flat",
                    padx=8, pady=4, command=set_alarm)
set_btn.grid(row=0, column=0, padx=8)

clear_btn = tk.Button(alarm_btn_frame, text="  ✖ Clear  ",
                      font=("Courier", 12), bg=theme["btn"],
                      fg=theme["fg"], relief="flat",
                      padx=8, pady=4, command=clear_alarm)
clear_btn.grid(row=0, column=1, padx=8)

# ─────────────────────────────────────────
#  DARK / LIGHT TOGGLE
# ─────────────────────────────────────────
def apply_theme(t):
    widgets = [
        (root,            "bg"),
        (tab_clock,       "bg"), (tab_stopwatch, "bg"), (tab_alarm, "bg"),
        (time_label,      "bg"), (date_label,    "bg"), (toggle_btn, "bg"),
        (sw_display,      "bg"), (sw_btn_frame,  "bg"),
        (start_stop_btn,  "bg"), (lap_btn,       "bg"), (reset_btn,  "bg"),
        (alarm_title,     "bg"), (alarm_status,  "bg"), (alarm_btn_frame, "bg"),
        (set_btn,         "bg"), (clear_btn,     "bg"),
    ]
    for w, _ in widgets:
        w.configure(bg=t["bg"])
    for w in [time_label, toggle_btn, sw_display,
              start_stop_btn, lap_btn, reset_btn,
              set_btn, clear_btn]:
        w.configure(fg=t["fg"])
    for w in [date_label, alarm_title, alarm_status]:
        w.configure(fg=t["sub"])
    lap_box.configure(bg=t["accent"], fg=t["fg"])
    alarm_entry.configure(bg=t["accent"], fg=t["fg"])

def toggle_theme():
    global theme
    theme = LIGHT if theme == DARK else DARK
    toggle_btn.config(text="🌙 Dark Mode" if theme == LIGHT else "☀ Light Mode")
    apply_theme(theme)

toggle_btn.config(command=toggle_theme)

# ─────────────────────────────────────────
#  START
# ─────────────────────────────────────────
update_clock()
check_alarm()
root.mainloop()
