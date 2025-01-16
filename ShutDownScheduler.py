import tkinter as tk
from tkinter import messagebox
import time
import threading
import os
#import ctypes

def on_focus_in(event):
    event.widget.configure(borderwidth=2, relief="solid", highlightbackground="blue", highlightcolor="blue")

def on_focus_out(event):
    event.widget.configure(borderwidth=1, relief="solid", highlightbackground="black", highlightcolor="black")

def schedule_shutdown():
    try:
        hours = int(hour_var.get())
        minutes = int(minute_var.get())
        seconds = int(second_var.get())
        
        total_seconds = hours * 3600 + minutes * 60 + seconds
        if total_seconds <= 0:
            messagebox.showerror("Error", "Please enter a valid time.")
            return
        
        shutdown_time = total_seconds - 10  # Show warning 10 seconds before shutdown
        
        def countdown():
            time.sleep(shutdown_time)
            
            # Show warning
            def cancel_shutdown():
                os.system("shutdown -a")
                for widget in (hour_entry, minute_entry, second_entry, schedule_button):
                    widget.config(state=tk.NORMAL)
                messagebox.showinfo("Cancelled", "Shutdown has been cancelled.")
            
            def show_warning():
                warning_window = tk.Toplevel(root)
                warning_window.title("Shutdown Warning")
                warning_window.geometry("300x150")
                
                # Center the warning window
                warning_window.geometry("+%d+%d" % (
                    root.winfo_x() + (root.winfo_width() / 2) - (300 / 2),
                    root.winfo_y() + (root.winfo_height() / 2) - (150 / 2)))
                
                tk.Label(warning_window, text="Shutdown is imminent in 10 seconds!", pady=20).pack()
                
                cancel_btn = tk.Button(warning_window, text="Cancel Shutdown", command=lambda: [cancel_shutdown(), warning_window.destroy()])
                cancel_btn.pack(pady=10)
                
                # Auto close after 10 seconds if no response
                warning_window.after(10000, lambda: [warning_window.destroy(), os.system("shutdown /s /t 0")])
                
                # Make window stay on top
                warning_window.lift()
                warning_window.focus_force()
            
            # Show warning in main thread
            root.after(0, show_warning)
            
        threading.Thread(target=countdown, daemon=True).start()
        for widget in (hour_entry, minute_entry, second_entry, schedule_button):
            widget.config(state=tk.DISABLED)
        messagebox.showinfo("Scheduled", f"Shutdown scheduled in {hours}h {minutes}m {seconds}s")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values.")

# GUI Setup
root = tk.Tk()
root.title("Shutdown Timer")

# Set window size to half of the current screen size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = screen_width // 2
window_height = screen_height // 2
root.geometry(f"{window_width}x{window_height}")
# Header
tk.Label(root, text="Shutdown Scheduler Program", font=("Arial", 14, "bold"), anchor="w").pack(fill="x", padx=10, pady=5)
tk.Label(root, text="This program is for scheduling shutdown to programs that has downloading stuff like installing games in Steam that takes hours or downloading a ZIP file in browser; this app lets you set a time to shutdown based on the estimated completion time so you can sleep already.", wraplength=window_width - 20, justify="left").pack(padx=10, pady=5)

# Variables
hour_var = tk.StringVar()
minute_var = tk.StringVar()
second_var = tk.StringVar()

# Layout
tk.Label(root, text="Hour:").pack(pady=10)
hour_entry = tk.Entry(root, textvariable=hour_var)
hour_entry.configure(borderwidth=1, relief="solid")
hour_entry.pack(pady=5)
hour_entry.bind("<FocusIn>", on_focus_in)
hour_entry.bind("<FocusOut>", on_focus_out)

tk.Label(root, text="Minutes:").pack(pady=10)
minute_entry = tk.Entry(root, textvariable=minute_var)
minute_entry.configure(borderwidth=1, relief="solid")
minute_entry.pack(pady=5)
minute_entry.bind("<FocusIn>", on_focus_in)
minute_entry.bind("<FocusOut>", on_focus_out)

tk.Label(root, text="Seconds:").pack(pady=10)
second_entry = tk.Entry(root, textvariable=second_var)
second_entry.configure(borderwidth=1, relief="solid")
second_entry.pack(pady=5)
second_entry.bind("<FocusIn>", on_focus_in)
second_entry.bind("<FocusOut>", on_focus_out)

# Create a style frame for the button to make it rounded
button_frame = tk.Frame(root)
button_frame.pack(pady=20)  # Increased padding

schedule_button = tk.Button(button_frame, text="Schedule Shutdown", command=schedule_shutdown,
                             relief="raised",
                             borderwidth=2,
                             padx=15,
                             pady=8,
                             bg="#D9534F",  # Reddish color (you can adjust the hex code)
                             fg="white",    # White text color
                             activebackground="#C9302C",  # Darker red for active state
                             activeforeground="white")    # White text on active


schedule_button.pack()

# Footer with increased spacing
tk.Label(root, text="Made by Wolf - Z", font=("Arial", 10, "italic"), anchor="center").pack(side="bottom", pady=20)

root.mainloop()