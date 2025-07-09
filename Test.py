import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# --- Functions ---
def show_message():
    user = entry.get()
    print("Hello,", user, "!")

# --- Main Application Window ---
app = ttk.Window(themename="superhero")
app.title("Ttkbootstrap Demo")
app.geometry("400x300")

signUp = False
Logged = False

# --- Sign-In/-Up ---
if not signUp:
    FrameSign = ttk.Frame(app)
    FrameSign.pack(fill="both", expand=True)  # FIXED

    FrLoad = ttk.Frame(app)

    if not Logged:
        label = ttk.Label(FrameSign, text="Welcome to Narad!\n", font=("Helvetica", 16))
        label.grid(row=0, column=2, pady=20, padx=35)

        label_sign = ttk.Label(FrameSign, text="Please Sign-in", font=("Helvetica", 7))
        label_sign.grid(row=1, column=2, pady=20, padx=10)

        entry = ttk.Entry(FrameSign, bootstyle="info")
        entry.grid(row=2, column=2, pady=10, padx=20, sticky='ew')

        button = ttk.Button(FrameSign, text="Click Me", command=show_message, bootstyle="success-outline")
        button.grid(row=3, column=2, pady=10, padx=10)

        button = ttk.Button(FrameSign, text="Sign-Up",
                            command=lambda: globals().__setitem__('Logged', True),
                            bootstyle="light-outline")
        button.grid(row=3, column=3, pady=20, padx=10)
    else:
        FrLoad.place(relx=0.5, rely=0.5, anchor="center")
        progress = ttk.Progressbar(FrLoad, bootstyle="success-animated", maximum=100, mode='indeterminate')
        progress.pack(pady=20, padx=20, fill="x")
        progress.start(10)


# --- Start the application ---
app.mainloop()