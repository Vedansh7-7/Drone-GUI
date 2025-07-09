import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# --- Functions ---
def show_message():
    user = entry.get()
    print("Hello,", user, "!")

# --- Main Application Window ---
# Create the main window using a theme
# The Window class from ttkbootstrap is a themed tk.Tk object.
app = ttk.Window(themename="superhero")
app.title("Ttkbootstrap Demo")
app.geometry("400x300")
signUp = False
Logged = False
#--- Sign-In/-up ---
if not signUp:
    FrameSign = ttk.Frame(app)
    FrameSign.place()
    FrLoad = ttk.Frame(app)
    if not Logged:
        # A label to display text
        label = ttk.Label(FrameSign, text="Welcome to Narad!\n", font=("Helvetica", 16))
        label.grid(row=0,column=2 ,pady=20, padx=35)
        label_sign = ttk.Label(FrameSign, text="Please Sign-in", font=("Helvetica", 7))
        label_sign.grid(row=1, column=2, pady=20, padx=10)
        # An entry widget for user input
        entry = ttk.Entry(FrameSign, bootstyle="info")
        entry.grid(row=2, column=2, pady=10, padx=20, sticky='ew')

        # A button that calls a function
        # The "bootstyle" parameter adds color context (e.g., primary, success, warning)
        button = ttk.Button(FrameSign, text="Click Me", command=show_message, bootstyle="success-outline")
        button.grid(row=3, column=2, pady=10, padx=10)

        button = ttk.Button(FrameSign, text="Sign-Up", command=print("Logging in done"), bootstyle="light-outline")
        button.grid(row=3, column=3, pady=20, padx=10)
    else:
        FrLoad.place()
        # A progress bar
        progress = ttk.Progressbar(FrLoad, bootstyle="striped, success", maximum=100)
        progress.pack(pady=20, padx=20, fill="BOTH")
        progress.start() # Animate the progress bar

# --- Start the application ---
app.mainloop()