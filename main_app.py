import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkintermapview # For the map
from datetime import datetime
import time # For simulation purposes (e.g., updating time, drone status)

# --- Global references for dynamic updates (we'll expand these as needed) ---
current_time_label = None
logged_in_staff_name = ""
drone_status_label = None
gps_status_label = None
altitude_label = None
speed_label = None
payload_status_label = None
eta_label = None
alerts_listbox = None
# Map view instance
map_widget = None

# --- Functions for Main UI ---

def update_time():
    """Updates the current time in the header."""
    now = datetime.now()
    current_time_label.config(text=now.strftime("%d-%m-%Y | %I:%M:%S %p %Z"))
    current_time_label.after(1000, update_time) # Update every second

def update_drone_telemetry():
    """Simulates and updates drone telemetry data."""
    # In a real app, this would get data from drone sensors/API
    global drone_status_label, gps_status_label, altitude_label, speed_label, payload_status_label, eta_label

    # Simulate states
    import random
    drone_states = ["IDLE", "AWAITING ASSIGNMENT", "EN ROUTE", "DELIVERING", "RETURNING", "CHARGING"]
    gps_states = ["Locked", "Acquiring...", "Lost!"]
    payload_states = ["Secured", "Released"]

    current_drone_state = random.choice(drone_states)
    current_gps_state = random.choice(gps_states)
    current_payload_state = random.choice(payload_states)
    current_altitude = round(random.uniform(0.0, 120.0), 1)
    current_speed = round(random.uniform(0.0, 30.0), 1)
    current_eta = random.randint(1, 60) if current_drone_state == "EN ROUTE" else "--"

    drone_status_label.config(text=current_drone_state, bootstyle="info" if current_drone_state == "IDLE" else "primary")
    gps_status_label.config(text=f"GPS: {current_gps_state}", bootstyle="success" if current_gps_state == "Locked" else "danger")
    altitude_label.config(text=f"Altitude: {current_altitude:.1f} m")
    speed_label.config(text=f"Speed: {current_speed:.1f} m/s")
    payload_status_label.config(text=f"Payload: {current_payload_state}", bootstyle="success" if current_payload_state == "Secured" else "warning")
    eta_label.config(text=f"Estimated ETA: {current_eta} min" if current_eta != "--" else "Estimated ETA: --",
                     bootstyle="warning" if isinstance(current_eta, int) and current_eta <= 10 else "info")


    # Schedule next update
    drone_status_label.after(3000, update_drone_telemetry) # Update every 3 seconds

def add_alert(message, level="info"):
    """Adds a system alert to the alerts listbox."""
    timestamp = datetime.now().strftime("[%H:%M:%S]")
    alerts_listbox.insert(0, f"{timestamp} {message}") # Add to top
    # You could add bootstyle for individual list items if supported,
    # or just use the listbox's default styling.
    # For now, just add the text.

def launch_drone_action():
    print("Drone Launch Initiated!")
    add_alert("Drone Launch Initiated!", "success")
    # Simulate adding a drone path on the map (example points)
    # This requires map_widget to be globally accessible or passed
    if map_widget:
        # Example path for simulation. Replace with actual route data.
        path_points = [
            (28.7041, 77.1025), # Delhi
            (28.5355, 77.3910), # Noida
            (28.7041, 77.1025)  # Back to Delhi
        ]
        map_widget.set_path(path_points) # This adds a path line on the map
        map_widget.set_marker(28.5355, 77.3910, text="Delivery Point")
        add_alert("Route set to Noida. Drone en route.", "info")


def return_to_base_action():
    print("Return to Base Command Issued.")
    add_alert("Drone returning to base.", "warning")

def emergency_landing_action():
    print("EMERGENCY LANDING INITIATED!")
    add_alert("EMERGENCY LANDING INITIATED! Seek immediate visual.", "danger")
    # Potentially disable other controls

def payload_release_action():
    print("Payload Release Command Issued.")
    add_alert("Payload released.", "success")

def new_delivery_action():
    print("Opening New Delivery Form...")
    add_alert("New delivery form opened.", "info")
    # This would open a Toplevel window for input (similar to sign-up)

def view_missions_action():
    print("Viewing Mission Log...")
    add_alert("Viewing mission logs.", "info")

def maintenance_log_action():
    print("Accessing Maintenance Log...")
    add_alert("Accessing maintenance logs.", "info")

def logout_action(parent_app, main_frame):
    """Destroys the current main UI and potentially returns to login screen."""
    if main_frame.winfo_exists():
        main_frame.destroy()
    print("Logged out. Application might return to login screen or exit.")
    # You could re-instantiate your login_screen.py's login frame here
    # For now, let's just let it close if that's the only frame.
    # A cleaner approach would be to have a single "AppController" that swaps frames.
    parent_app.destroy() # For now, just close the application on logout.

# --- Main UI Build Function ---

def build_main_ui(parent_app, staff_name):
    """
    Builds the main drone control GUI within the provided parent_app window.
    """
    global current_time_label, logged_in_staff_name, drone_status_label, \
           gps_status_label, altitude_label, speed_label, payload_status_label, \
           eta_label, alerts_listbox, map_widget

    logged_in_staff_name = staff_name # Store the staff name globally

    main_frame = ttk.Frame(parent_app)
    main_frame.pack(fill="both", expand=True)

    # Configure grid for the main frame (3 columns, multiple rows)
    main_frame.grid_columnconfigure(0, weight=1) # Left panel
    main_frame.grid_columnconfigure(1, weight=3) # Center (Map) panel - wider
    main_frame.grid_columnconfigure(2, weight=1) # Right panel
    main_frame.grid_rowconfigure(1, weight=1) # Main content row

    # --- Header (Top Bar) ---
    header_frame = ttk.Frame(main_frame, bootstyle="dark")
    header_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=5)
    header_frame.grid_columnconfigure(0, weight=1) # Logo/title
    header_frame.grid_columnconfigure(1, weight=2) # Welcome message
    header_frame.grid_columnconfigure(2, weight=1) # Time/Date
    header_frame.grid_columnconfigure(3, weight=0) # Battery
    header_frame.grid_columnconfigure(4, weight=0) # Signal
    header_frame.grid_columnconfigure(5, weight=1) # Logout button

    ttk.Label(header_frame, text="Narad Medical Courier", font=("Helvetica", 18, "bold"), bootstyle="primary").grid(row=0, column=0, padx=15, pady=10, sticky="w")
    ttk.Label(header_frame, text=f"Welcome, {logged_in_staff_name}!", font=("Helvetica", 12), bootstyle="info").grid(row=0, column=1, sticky="w", padx=10)

    current_time_label = ttk.Label(header_frame, text="", font=("Helvetica", 10), bootstyle="light")
    current_time_label.grid(row=0, column=2, sticky="e", padx=10)
    update_time() # Start updating time

    ttk.Label(header_frame, text="🔋 85%", font=("Helvetica", 10), bootstyle="success").grid(row=0, column=3, padx=5, sticky="e")
    ttk.Label(header_frame, text="📶 5G", font=("Helvetica", 10), bootstyle="success").grid(row=0, column=4, padx=5, sticky="e")

    ttk.Button(header_frame, text="Logout", command=lambda: logout_action(parent_app, main_frame), bootstyle="danger-outline").grid(row=0, column=5, padx=15, sticky="e")


    # --- Left Panel: Mission Overview & Controls ---
    left_panel = ttk.Frame(main_frame, bootstyle="secondary")
    left_panel.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
    left_panel.grid_columnconfigure(0, weight=1) # Center content within panel

    ttk.Label(left_panel, text="Current Mission Status", font=("Helvetica", 12, "bold"), bootstyle="info").pack(pady=(15, 5))
    drone_status_label = ttk.Label(left_panel, text="IDLE", font=("Helvetica", 14), bootstyle="info")
    drone_status_label.pack(pady=5)
    ttk.Separator(left_panel).pack(fill="x", padx=10, pady=10)

    ttk.Label(left_panel, text="Drone Telemetry", font=("Helvetica", 12, "bold"), bootstyle="primary").pack(pady=(10, 5))
    gps_status_label = ttk.Label(left_panel, text="GPS: --", font=("Helvetica", 10))
    gps_status_label.pack(anchor="w", padx=20)
    altitude_label = ttk.Label(left_panel, text="Altitude: -- m", font=("Helvetica", 10))
    altitude_label.pack(anchor="w", padx=20)
    speed_label = ttk.Label(left_panel, text="Speed: -- m/s", font=("Helvetica", 10))
    speed_label.pack(anchor="w", padx=20)
    payload_status_label = ttk.Label(left_panel, text="Payload: --", font=("Helvetica", 10))
    payload_status_label.pack(anchor="w", padx=20)
    eta_label = ttk.Label(left_panel, text="Estimated ETA: --", font=("Helvetica", 10))
    eta_label.pack(anchor="w", padx=20, pady=(0, 10))
    ttk.Separator(left_panel).pack(fill="x", padx=10, pady=10)

    # Action Buttons
    ttk.Button(left_panel, text="New Delivery", command=new_delivery_action, bootstyle="primary").pack(fill="x", padx=20, pady=5)
    ttk.Button(left_panel, text="View Missions", command=view_missions_action, bootstyle="info-outline").pack(fill="x", padx=20, pady=5)
    ttk.Button(left_panel, text="Maintenance Log", command=maintenance_log_action, bootstyle="light-outline").pack(fill="x", padx=20, pady=5)

    update_drone_telemetry() # Start updating drone telemetry


    # --- Center Panel: Active Mission Details & Map ---
    center_panel = ttk.Frame(main_frame, bootstyle="dark")
    center_panel.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
    center_panel.grid_rowconfigure(1, weight=1) # Map takes most space
    center_panel.grid_columnconfigure(0, weight=1) # Center content

    ttk.Label(center_panel, text="Active Delivery Details", font=("Helvetica", 12, "bold"), bootstyle="info").pack(pady=(15, 5))

    # TkinterMapView setup
    map_widget = tkintermapview.TkinterMapView(center_panel, width=700, height=500, corner_radius=0)
    map_widget.pack(fill="both", expand=True, padx=10, pady=10)

    # --- IMPORTANT: Configure for OFFLINE Tiles ---
    # You need to pre-download map tiles and store them locally.
    # Replace "path/to/your/local/tiles/{z}/{x}/{y}.png" with the actual path
    # where your map tiles are stored.
    # Example: If your tiles are in a folder named 'my_offline_maps'
    # and organized like my_offline_maps/10/500/300.png, the path would be:
    # "my_offline_maps/{z}/{x}/{y}.png"
    #
    # For a 500 sq. km radius, you'll need tools like Maperitive or SAS.Planet
    # to download OSM tiles for your specific bounding box and zoom levels.
    #
    # If you want to test with online maps temporarily, uncomment the line below
    # and comment out the set_tile_server line.
    map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png") # Online OSM

    # For offline use, point to your local tile directory:
    # Make sure this path exists and contains your downloaded tiles.
    # Example dummy path - YOU MUST CHANGE THIS TO YOUR ACTUAL TILE PATH
    # The map will appear blank if tiles are not found at this path.
    # offline_tile_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "map_tiles", "{z}", "{x}", "{y}.png")
    # map_widget.set_tile_server(offline_tile_path)


    # Set initial position for testing (e.g., a city in India)
    # This is roughly New Delhi, India. Adjust as needed for your ground stations.
    map_widget.set_position(28.6139, 77.2090) # Latitude, Longitude (New Delhi)
    map_widget.set_zoom(10) # Zoom level (adjust for 500 sq. km radius)

    # Add a marker for a hypothetical ground station
    map_widget.set_marker(28.6139, 77.2090, text="Base Station")


    # Delivery Information (placeholders)
    delivery_info_frame = ttk.Frame(center_panel)
    delivery_info_frame.pack(fill="x", padx=10, pady=10)
    delivery_info_frame.grid_columnconfigure(0, weight=1)
    delivery_info_frame.grid_columnconfigure(1, weight=3)

    ttk.Label(delivery_info_frame, text="Destination:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, sticky="w", pady=2)
    ttk.Label(delivery_info_frame, text="Apollo Hospital, Delhi", font=("Helvetica", 10)).grid(row=0, column=1, sticky="w", pady=2)

    ttk.Label(delivery_info_frame, text="Address:", font=("Helvetica", 10, "bold")).grid(row=1, column=0, sticky="w", pady=2)
    ttk.Label(delivery_info_frame, text="Mathura Rd, Sarita Vihar, Delhi 110076", font=("Helvetica", 10)).grid(row=1, column=1, sticky="w", pady=2)

    ttk.Label(delivery_info_frame, text="Recipient:", font=("Helvetica", 10, "bold")).grid(row=2, column=0, sticky="w", pady=2)
    ttk.Label(delivery_info_frame, text="Dr. Priya Sharma - +91 9876543210", font=("Helvetica", 10)).grid(row=2, column=1, sticky="w", pady=2)

    ttk.Label(delivery_info_frame, text="Payload:", font=("Helvetica", 10, "bold")).grid(row=3, column=0, sticky="w", pady=2)
    ttk.Label(delivery_info_frame, text="COVID-19 Vaccines (x50 doses)", font=("Helvetica", 10)).grid(row=3, column=1, sticky="w", pady=2)

    ttk.Label(delivery_info_frame, text="Temp Log:", font=("Helvetica", 10, "bold")).grid(row=4, column=0, sticky="w", pady=2)
    ttk.Label(delivery_info_frame, text="4.2°C (Optimal)", bootstyle="success", font=("Helvetica", 10)).grid(row=4, column=1, sticky="w", pady=2)


    # --- Right Panel: Drone Controls & Alerts ---
    right_panel = ttk.Frame(main_frame, bootstyle="secondary")
    right_panel.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)
    right_panel.grid_columnconfigure(0, weight=1) # Center content within panel

    ttk.Label(right_panel, text="Drone Controls", font=("Helvetica", 12, "bold"), bootstyle="info").pack(pady=(15, 5))
    ttk.Button(right_panel, text="Launch Drone", command=launch_drone_action, bootstyle="success").pack(fill="x", padx=20, pady=5)
    ttk.Button(right_panel, text="Return to Base", command=return_to_base_action, bootstyle="warning-outline").pack(fill="x", padx=20, pady=5)
    ttk.Button(right_panel, text="Emergency Landing", command=emergency_landing_action, bootstyle="danger").pack(fill="x", padx=20, pady=5)
    ttk.Button(right_panel, text="Payload Release", command=payload_release_action, bootstyle="primary-outline").pack(fill="x", padx=20, pady=5)
    ttk.Separator(right_panel).pack(fill="x", padx=10, pady=10)

    ttk.Label(right_panel, text="System Alerts", font=("Helvetica", 12, "bold"), bootstyle="info").pack(pady=(10, 5))
    listbox_bg_color = parent_app.style.lookup('TFrame', 'background', bootstyle="secondary")

    alerts_listbox = tk.Listbox(right_panel, height=10, borderwidth=0, highlightthickness=0,
                                bg=listbox_bg_color, # Use the looked-up color here
                                fg='white', # Keep foreground white for contrast on dark background
                                font=("Helvetica", 9), selectbackground=parent_app.style.colors.primary,
                                selectforeground='white')
    alerts_listbox.pack(fill="both", expand=True, padx=10, pady=5)
    # Add a scrollbar to the listbox
    scrollbar = ttk.Scrollbar(right_panel, command=alerts_listbox.yview, bootstyle="round")
    scrollbar.pack(side="right", fill="y")
    alerts_listbox.config(yscrollcommand=scrollbar.set)

    # Initial alert for testing
    add_alert("System initialized. Awaiting commands.", "info")
    add_alert("Check drone pre-flight diagnostics.", "warning")