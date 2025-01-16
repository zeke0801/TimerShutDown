import subprocess
import time
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox

def get_shutdown_time(hours, minutes):
    """Calculate the shutdown time based on input hours and minutes"""
    total_seconds = (hours * 3600) + (minutes * 60)
    return total_seconds

def countdown_dialog(root, seconds_left):
    """Display countdown dialog and return True if user confirms shutdown"""
    if seconds_left <= 0:
        root.destroy()
        return False
        
    result = messagebox.askquestion(
        "Shutdown Confirmation", 
        f"System will shutdown in {seconds_left} seconds!\nDo you want to proceed?",
        icon='warning'
    )
    
    root.destroy()
    return result == 'yes'

def wait_and_show_dialog(seconds):
    """Wait for the specified time and show the countdown dialog"""
    time.sleep(seconds)
    
    # Create root window for dialog
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Show 10 second countdown dialog
    for i in range(10, 0, -1):
        if not countdown_dialog(tk.Tk(), i):
            subprocess.run(['shutdown', '/a'])  # Cancel shutdown if user selects 'no'
            print("\nShutdown cancelled by user.")
            return False
    
    return True

def main():
    try:
        print("\nWindows Shutdown Scheduler")
        print("-------------------------")
        hours = int(input("Enter hours (0-23): "))
        minutes = int(input("Enter minutes (0-59): "))
        
        if not (0 <= hours <= 23 and 0 <= minutes <= 59):
            print("Invalid input! Hours should be 0-23 and minutes should be 0-59")
            return
        
        seconds = get_shutdown_time(hours, minutes)
        
        # Calculate and show the shutdown time
        shutdown_time = datetime.now() + timedelta(seconds=seconds)
        print(f"\nSystem will shutdown at: {shutdown_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Schedule shutdown with extra time for confirmation
        subprocess.run(['shutdown', '/s', '/t', str(seconds + 15)])
        
        print("\nShutdown scheduled successfully!")
        print("To cancel, open CMD as administrator and type: shutdown /a")
        
        # Wait until scheduled time and show confirmation dialog
        if wait_and_show_dialog(seconds):
            print("Shutdown proceeding...")
        
    except ValueError:
        print("Please enter valid numbers for hours and minutes!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
