import tkinter as tk
import time
import os
import psutil
import sys
import ctypes

PROCESS_NAMES = ["WpcMon.exe", "LockApp.exe"]

def notification(title, text, duration=3):
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.configure(bg="#333333")

    hwnd = root.winfo_id()
    region = ctypes.windll.gdi32.CreateRoundRectRgn(0, 0, 350, 80, 20, 20)
    ctypes.windll.user32.SetWindowRgn(hwnd, region, True)

    frame = tk.Frame(root, bg="#444", padx=10, pady=5)
    frame.pack(fill=tk.BOTH, expand=True)

    title_label = tk.Label(frame, text=title, bg="#444", fg="white", font=("Arial", 16, "bold"))
    title_label.grid(row=0, column=0, sticky="w", padx=5, pady=(5, 2))

    label = tk.Label(frame, text=text, bg="#444", fg="white", font=("Arial", 12))
    label.grid(row=1, column=0, sticky="w", padx=5, pady=(2, 5))

    screen_width = root.winfo_screenwidth()
    notif_width = 350
    x = (screen_width - notif_width) // 2
    y = -80

    root.geometry(f"{notif_width}x80+{x}+{y}")
    root.update()

    for i in range(-80, 20, 2):
        root.geometry(f"{notif_width}x80+{x}+{i}")
        root.update()
        time.sleep(0.001)

    time.sleep(duration)
    for i in range(20, -80, -2):
        root.geometry(f"{notif_width}x80+{x}+{i}")
        root.update()
        time.sleep(0.005)

    root.destroy()

def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin()

def kill_process_by_name():
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] == PROCESS_NAMES[0] or proc.info['name'] == PROCESS_NAMES[1]:
                proc.terminate()
                notification("Success!", f"Disabled Microsoft Family! (PID: {proc.info['pid']})")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

if __name__ == "__main__":
    time.sleep(1.5)
    if not is_admin():
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        except Exception as e:
            notification("Error!", f"Permission error: {e}")
            sys.exit(1)
    else:
        notification("AMFS", "Running in background.")
        while True:
            kill_process_by_name()
            time.sleep(1)
