import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import json
import os
import time
import main_app # This assumes main_app.py is in the same directory

# --- Global Variables ---
Logged = False
Staff_Name = "" # To store the name of the logged-in staff
login_message_label = None # To reference the label for login messages
STAFF_DATA_FILE = "staff_data.json" # Name of the JSON file

# --- JSON File Operations ---

def load_staff_data():
    """Loads staff data from the JSON file."""
    if not os.path.exists(STAFF_DATA_FILE):
        return [] # Return empty list if file doesn't exist

    try:
        with open(STAFF_DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: {STAFF_DATA_FILE} is empty or corrupted. Starting with empty data.")
        return []
    except Exception as e:
        print(f"Error loading staff data: {e}")
        return []

def save_staff_data(data):
    """Saves staff data to the JSON file."""
    try:
        with open(STAFF_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving staff data: {e}")

# --- Functions ---

def show_main_ui():
    """
    Destroys login/loading frames and prepares for the main application UI.
    This function will be expanded in the next step to build the main UI.
    """
    global Logged

    # Stop the progress bar before destroying the frame
    progress.stop()

    if FrLoad.winfo_exists():
        FrLoad.destroy() # Destroy the loading frame
    if FrameSign.winfo_exists():
        FrameSign.destroy() # Destroy the sign-in frame

    # --- Placeholder for Main UI ---
    print(f"Logged in successfully as {Staff_Name}! Transitioning to Main UI.")
    main_ui_frame = ttk.Frame(app)
    main_ui_frame.pack(fill="both", expand=True)
    ttk.Label(main_ui_frame, text=f"Welcome, {Staff_Name}! This is the Main Drone Control UI.", font=("Helvetica", 20)).pack(pady=50)
    ttk.Label(main_ui_frame, text="Ready to integrate the map and controls!").pack()
    # In the next prompt, we will replace this placeholder with the actual detailed UI.


def start_loading_animation():
    """
    Shows the loading frame with an indeterminate progress bar.
    """
    # Hide the sign-in frame
    FrameSign.pack_forget()

    # Place the loading frame in the center
    FrLoad.place(relx=0.5, rely=0.5, anchor="center")

    # Start the progress bar animation
    progress.start(10) # 10ms interval for animation update

    # Simulate a loading time and then transition to the main UI
    app.after(3000, show_main_ui) # Call show_main_ui after 3 seconds


def handle_login():
    """
    Handles the login process: validates input against JSON data and starts loading.
    """
    global Logged, Staff_Name, login_message_label

    staff_id = entry_staff_id.get().strip()
    contact_number = entry_contact_number.get().strip()

    if not staff_id or not contact_number:
        if not login_message_label:
            login_message_label = ttk.Label(FrameSign, text="", bootstyle="danger", font=("Helvetica", 9))
            login_message_label.grid(row=6, column=1, columnspan=3, pady=5, padx=10)
        login_message_label.config(text="Please enter both Staff ID and Contact Number.")
        return

    staff_data = load_staff_data()
    found_user = None

    for user in staff_data:
        if user.get('staff_id') == staff_id and user.get('contact_number') == contact_number:
            found_user = user
            break

    if found_user:
        Staff_Name = found_user.get('name', f"Staff {staff_id}") # Use stored name or default
        Logged = True
        if login_message_label:
            login_message_label.config(text="") # Clear any previous messages
        start_loading_animation()
    else:
        if not login_message_label:
            login_message_label = ttk.Label(FrameSign, text="", bootstyle="danger", font=("Helvetica", 9))
            login_message_label.grid(row=6, column=1, columnspan=3, pady=5, padx=10)
        login_message_label.config(text="Invalid Staff ID or Contact Number.")


def register_staff(signup_win, name_entry, id_entry, contact_entry, msg_label):
    """
    Registers a new staff member and saves to JSON.
    """
    new_name = name_entry.get().strip()
    new_id = id_entry.get().strip()
    new_contact = contact_entry.get().strip()

    if not new_name or not new_id or not new_contact:
        msg_label.config(text="All fields are required!", bootstyle="danger")
        return

    staff_data = load_staff_data()

    # Check if Staff ID already exists
    for user in staff_data:
        if user.get('staff_id') == new_id:
            msg_label.config(text="Staff ID already exists. Please choose a different one.", bootstyle="danger")
            return

    # Add new staff member
    staff_data.append({
        'name': new_name,
        'staff_id': new_id,
        'contact_number': new_contact
    })
    save_staff_data(staff_data)

    msg_label.config(text="Registration successful! You can now log in.", bootstyle="success")
    # Close signup window after a short delay
    signup_win.after(1500, signup_win.destroy)


def handle_signup():
    """
    Opens a new Toplevel window for staff registration.
    """
    signup_win = ttk.Toplevel(app)
    signup_win.title("Narad - Staff Registration")
    signup_win.transient(app) # Makes it dependent on the main window
    signup_win.grab_set() # Disables interaction with main window until this is closed
    signup_win.resizable(False, False) # Don't allow resizing
    signup_win.geometry("400x300") # Fixed size for the signup window

    # Center the signup window
    app_x = app.winfo_x()
    app_y = app.winfo_y()
    app_width = app.winfo_width()
    app_height = app.winfo_height()

    signup_width = 400
    signup_height = 300

    center_x = app_x + (app_width // 2) - (signup_width // 2)
    center_y = app_y + (app_height // 2) - (signup_height // 2)

    signup_win.geometry(f"{signup_width}x{signup_height}+{center_x}+{center_y}")


    # Configure grid for centering
    signup_win.grid_rowconfigure(0, weight=1)
    signup_win.grid_rowconfigure(len(signup_win.grid_slaves()) + 1, weight=1) # Adjust row count
    signup_win.grid_columnconfigure(0, weight=1)
    signup_win.grid_columnconfigure(3, weight=1)


    ttk.Label(signup_win, text="Register New Staff", font=("Helvetica", 14, "bold")).grid(row=0, column=1, columnspan=2, pady=15)

    ttk.Label(signup_win, text="Full Name:", font=("Helvetica", 10)).grid(row=1, column=1, pady=5, padx=10, sticky="e")
    entry_name = ttk.Entry(signup_win, bootstyle="primary")
    entry_name.grid(row=1, column=2, pady=5, padx=10, sticky="ew")

    ttk.Label(signup_win, text="Staff ID:", font=("Helvetica", 10)).grid(row=2, column=1, pady=5, padx=10, sticky="e")
    entry_id = ttk.Entry(signup_win, bootstyle="primary")
    entry_id.grid(row=2, column=2, pady=5, padx=10, sticky="ew")

    ttk.Label(signup_win, text="Contact No.:", font=("Helvetica", 10)).grid(row=3, column=1, pady=5, padx=10, sticky="e")
    entry_contact = ttk.Entry(signup_win, bootstyle="primary")
    entry_contact.grid(row=3, column=2, pady=5, padx=10, sticky="ew")

    signup_message_label = ttk.Label(signup_win, text="", bootstyle="info", font=("Helvetica", 9))
    signup_message_label.grid(row=4, column=1, columnspan=2, pady=10)

    btn_register = ttk.Button(signup_win, text="Register",
                              command=lambda: register_staff(signup_win, entry_name, entry_id, entry_contact, signup_message_label),
                              bootstyle="success")
    btn_register.grid(row=5, column=1, pady=15, padx=(10, 5), sticky="e")

    btn_cancel = ttk.Button(signup_win, text="Cancel", command=signup_win.destroy, bootstyle="secondary-outline")
    btn_cancel.grid(row=5, column=2, pady=15, padx=(5, 10), sticky="w")


# --- Main Application Window ---
app = ttk.Window(themename="superhero")
app.title("Narad Medical Courier")
app.state('zoomed') # Set window to zoomed (maximised) state

# --- Sign-In Frame ---
FrameSign = ttk.Frame(app)
FrameSign.pack(fill="both", expand=True) # Occupy the entire window

# Configure grid for centering elements in FrameSign
FrameSign.grid_rowconfigure(0, weight=1)
FrameSign.grid_rowconfigure(7, weight=1) # Increased row count for better spacing
FrameSign.grid_columnconfigure(0, weight=1)
FrameSign.grid_columnconfigure(4, weight=1)

# Welcome Label
label_welcome = ttk.Label(FrameSign, text="Welcome to Narad Medical Courier!", font=("Helvetica", 20, "bold"), bootstyle="primary")
label_welcome.grid(row=1, column=1, columnspan=3, pady=(50, 10), padx=20)

# Sign-in instruction
label_sign_in_instruction = ttk.Label(FrameSign, text="Please Sign-In with your Staff ID and Contact Number", font=("Helvetica", 10), bootstyle="info")
label_sign_in_instruction.grid(row=2, column=1, columnspan=3, pady=10, padx=20)

# Staff ID Entry
ttk.Label(FrameSign, text="Staff ID:", font=("Helvetica", 11)).grid(row=3, column=1, pady=5, padx=(20, 5), sticky="e")
entry_staff_id = ttk.Entry(FrameSign, bootstyle="info", width=30)
entry_staff_id.grid(row=3, column=2, columnspan=2, pady=5, padx=(5, 20), sticky='ew')

# Contact Number Entry
ttk.Label(FrameSign, text="Contact No.:", font=("Helvetica", 11)).grid(row=4, column=1, pady=5, padx=(20, 5), sticky="e")
entry_contact_number = ttk.Entry(FrameSign, bootstyle="info", width=30)
entry_contact_number.grid(row=4, column=2, columnspan=2, pady=5, padx=(5, 20), sticky='ew')

# Login/Sign-up Buttons
button_sign_in = ttk.Button(FrameSign, text="Sign-In", command=handle_login, bootstyle="success")
button_sign_in.grid(row=5, column=2, pady=20, padx=(10, 5), sticky='e')

button_sign_up = ttk.Button(FrameSign, text="Sign-Up", command=handle_signup, bootstyle="light-outline")
button_sign_up.grid(row=5, column=3, pady=20, padx=(5, 10), sticky='w')

# Initialize login_message_label here for consistent placement
login_message_label = ttk.Label(FrameSign, text="", bootstyle="danger", font=("Helvetica", 9))
login_message_label.grid(row=6, column=1, columnspan=3, pady=5, padx=10) # Place it below buttons and pad Y

# --- Loading Frame ---
FrLoad = ttk.Frame(app)

# Progress bar inside FrLoad
progress = ttk.Progressbar(FrLoad, bootstyle="success-animated", maximum=100, mode='indeterminate')
progress.pack(pady=40, padx=50, fill="x")
ttk.Label(FrLoad, text="Authenticating and Loading System...", font=("Helvetica", 12)).pack(pady=10)


# --- Run the Application ---
if not Logged: # Ensure the sign-in frame is visible initially
    FrameSign.tkraise() # Bring FrameSign to the top

app.mainloop()