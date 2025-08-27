import os
import sys
import json
import csv
import logging
import time
import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import urllib.request
from threading import Timer
import platform

# Constants
SCRIPT_NAME = "BreakTimer"
VERSION = "1.0.0"
BACKGROUND_MODE = True  # Set to False for debugging

# Directory structure
SCRIPT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
CONFIG_DIR = os.path.join(SCRIPT_DIR, "config")
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
NOTIFICATIONS_DIR = os.path.join(SCRIPT_DIR, "notifications")
SOUNDS_DIR = os.path.join(SCRIPT_DIR, "sounds")
LOG_DIR = os.path.join(SCRIPT_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "break_timer.log")

# Default configurations
DEFAULT_SETTINGS = {
    "notification_sound": True,
    "visual_alerts": True,
    "minimize_to_tray": True,
    "start_on_boot": False,
    "check_updates": True,
    "theme": "system",
    "last_update_check": ""
}

DEFAULT_TIMERS = {
    "presets": [
        {"name": "Quick Break", "duration": 5, "color": "#4CAF50"},
        {"name": "Coffee Break", "duration": 15, "color": "#2196F3"},
        {"name": "Lunch Break", "duration": 30, "color": "#FFC107"},
        {"name": "MOVE CAR", "duration": 110, "color": "#9C27B0"}
    ],
    "custom": []
}

DEFAULT_REMINDERS = {
    "halfway": "You're halfway through your break!",
    "almost_done": "Break almost over, 10% time remaining.",
    "completed": "Break completed. Time to get back to work!",
    "missed": "You missed your scheduled break!"
}

# Required Python packages
REQUIRED_PACKAGES = [
    "plyer",    # For notifications
    "pygame",   # For sound
    "pillow",   # For image processing
    "ttkthemes" # For better looking themes
]

# Setup logging
def setup_logging():
    """Set up the logging configuration"""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Add console handler if not in background mode
    if not BACKGROUND_MODE:
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter(log_format)
        console.setFormatter(formatter)
        logging.getLogger("").addHandler(console)

def first_time_install():
    """Perform first-time installation steps"""
    logging.info("Starting first-time installation...")
    
    # Create directory structure
    dirs = [CONFIG_DIR, DATA_DIR, NOTIFICATIONS_DIR, SOUNDS_DIR, LOG_DIR]
    for directory in dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f"Created directory: {directory}")
    
    # Create default configuration files
    if not os.path.exists(os.path.join(CONFIG_DIR, "settings.json")):
        with open(os.path.join(CONFIG_DIR, "settings.json"), "w") as f:
            json.dump(DEFAULT_SETTINGS, f, indent=4)
            logging.info("Created default settings.json")
    
    if not os.path.exists(os.path.join(CONFIG_DIR, "timers.json")):
        with open(os.path.join(CONFIG_DIR, "timers.json"), "w") as f:
            json.dump(DEFAULT_TIMERS, f, indent=4)
            logging.info("Created default timers.json")
    
    if not os.path.exists(os.path.join(NOTIFICATIONS_DIR, "reminders.json")):
        with open(os.path.join(NOTIFICATIONS_DIR, "reminders.json"), "w") as f:
            json.dump(DEFAULT_REMINDERS, f, indent=4)
            logging.info("Created default reminders.json")
    
    # Create history file with headers
    if not os.path.exists(os.path.join(DATA_DIR, "history.csv")):
        with open(os.path.join(DATA_DIR, "history.csv"), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Time", "Break Type", "Duration (min)", "Completed"])
            logging.info("Created history.csv with headers")
    
    # Add empty sound files
    for sound_file in ["alert1.wav", "alert2.wav"]:
        sound_path = os.path.join(SOUNDS_DIR, sound_file)
        if not os.path.exists(sound_path):
            # Create an empty file (in a real app, you would include actual sound files)
            with open(sound_path, "wb") as f:
                pass
            logging.info(f"Created placeholder sound file: {sound_file}")
    
    # Check and install dependencies
    install_dependencies()
    
    # Create flag file to indicate installation is complete
    with open(os.path.join(CONFIG_DIR, ".installed"), "w") as f:
        f.write(f"Installed on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logging.info("Installation complete")

def install_dependencies():
    """Check and install required Python packages"""
    logging.info("Checking dependencies...")
    
    missing_packages = []
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package)
            logging.info(f"Package {package} is already installed")
        except ImportError:
            missing_packages.append(package)
            logging.warning(f"Package {package} is missing")
    
    if missing_packages:
        logging.info(f"Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
            logging.info("Successfully installed all missing packages")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to install packages: {e}")
            if not BACKGROUND_MODE:
                print(f"Error: Failed to install required packages. Please install them manually: {', '.join(missing_packages)}")
                sys.exit(1)

def check_for_updates():
    """Check for script updates"""
    logging.info("Checking for updates...")
    
    # Update settings with last check time
    settings = load_settings()
    settings["last_update_check"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_settings(settings)
    
    # In a real application, you would check a server for updates
    # This is a placeholder for the actual update check logic
    logging.info("Update check completed - no updates available")
    return False

def load_settings():
    """Load settings from configuration file"""
    try:
        with open(os.path.join(CONFIG_DIR, "settings.json"), "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading settings: {e}")
        return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    """Save settings to configuration file"""
    try:
        with open(os.path.join(CONFIG_DIR, "settings.json"), "w") as f:
            json.dump(settings, f, indent=4)
        return True
    except Exception as e:
        logging.error(f"Error saving settings: {e}")
        return False

def load_timers():
    """Load timer configurations"""
    try:
        with open(os.path.join(CONFIG_DIR, "timers.json"), "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading timers: {e}")
        return DEFAULT_TIMERS.copy()

def save_timers(timers):
    """Save timer configurations"""
    try:
        with open(os.path.join(CONFIG_DIR, "timers.json"), "w") as f:
            json.dump(timers, f, indent=4)
        return True
    except Exception as e:
        logging.error(f"Error saving timers: {e}")
        return False

def load_reminders():
    """Load notification reminder templates"""
    try:
        with open(os.path.join(NOTIFICATIONS_DIR, "reminders.json"), "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading reminders: {e}")
        return DEFAULT_REMINDERS.copy()

def record_break_history(break_type, duration, completed=True):
    """Record a break in the history file"""
    now = datetime.datetime.now()
    try:
        with open(os.path.join(DATA_DIR, "history.csv"), "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                now.strftime("%Y-%m-%d"), 
                now.strftime("%H:%M:%S"),
                break_type,
                duration,
                "Yes" if completed else "No"
            ])
        logging.info(f"Recorded break: {break_type}, {duration} min, completed: {completed}")
        return True
    except Exception as e:
        logging.error(f"Error recording break history: {e}")
        return False

# Import GUI-related modules only after dependencies are installed
try:
    from plyer import notification
    import pygame
    from PIL import Image, ImageTk
    from ttkthemes import ThemedTk
except ImportError:
    # These will be installed in the first run
    pass

class BreakTimer:
    """Main application class"""
    def __init__(self, root):
        self.root = root
        self.root.title(f"{SCRIPT_NAME} v{VERSION}")
        self.root.geometry("400x300")  # Reduced from 800x600 (50% size)
        self.root.minsize(300, 200)    # Reduced from 600x400 (50% size)
        
        # Center the window on screen
        self.center_window()
        
        # Initialize with settings
        self.settings = load_settings()
        self.timers = load_timers()
        self.reminders = load_reminders()
        
        # Set theme if ttkthemes is available
        if "ttkthemes" in sys.modules:
            if self.settings["theme"] == "system":
                # Use system theme based detection
                if platform.system() == "Windows":
                    self.root.set_theme("vista")
                elif platform.system() == "Darwin":  # macOS
                    self.root.set_theme("aqua")
                else:  # Linux and others
                    self.root.set_theme("clearlooks")
            else:
                self.root.set_theme(self.settings["theme"])
        
        # Initialize sound (after pygame is imported)
        pygame.mixer.init()
        
        # Set up the UI
        self.setup_ui()
        
        # Active timers
        self.active_timers = {}
        self.update_job = None
        
        # Set up notification system
        self.setup_notification_system()
        
        # Register for destroy event
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        logging.info("Application initialized")
    
    def center_window(self):
        """Center a window on the screen and ensure it's not off-screen"""
        window = self.root
        window.update_idletasks()
        
        width = window.winfo_width()
        height = window.winfo_height()
        
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        # Calculate position for center
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Ensure window is not off-screen
        x = max(0, min(x, screen_width - width))
        y = max(0, min(y, screen_height - height))
        
        window.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Set up the application UI"""
        # Main container
        self.main_container = ttk.Frame(self.root, padding="10")
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create a notebook with tabs
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create tabs
        self.timers_tab = ttk.Frame(self.notebook)
        self.active_tab = ttk.Frame(self.notebook)
        self.history_tab = ttk.Frame(self.notebook)
        self.settings_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.timers_tab, text="Timers")
        self.notebook.add(self.active_tab, text="Active Timers")
        self.notebook.add(self.history_tab, text="History")
        self.notebook.add(self.settings_tab, text="Settings")
        
        # Set up each tab
        self.setup_timers_tab()
        self.setup_active_tab()
        self.setup_history_tab()
        self.setup_settings_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(self.main_container, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def setup_timers_tab(self):
        """Set up the timers tab with preset and custom timers"""
        # Top frame for preset timers
        preset_frame = ttk.LabelFrame(self.timers_tab, text="Preset Timers")
        preset_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Grid of preset timer buttons
        self.create_timer_buttons(preset_frame, self.timers["presets"])
        
        # Bottom frame for custom timers
        custom_frame = ttk.LabelFrame(self.timers_tab, text="Custom Timers")
        custom_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Add button for creating new custom timer
        ttk.Button(custom_frame, text="Create New Timer", command=self.create_custom_timer).pack(pady=5)
        
        # Grid of custom timer buttons
        if self.timers["custom"]:
            self.create_timer_buttons(custom_frame, self.timers["custom"])
        else:
            ttk.Label(custom_frame, text="No custom timers yet. Click 'Create New Timer' to add one.").pack(pady=20)
    
    def create_timer_buttons(self, parent, timer_list):
        """Create a grid of timer buttons"""
        # Create a frame for the grid
        grid_frame = ttk.Frame(parent)
        grid_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configure grid
        cols = 4  # Number of columns
        for i, timer in enumerate(timer_list):
            row, col = divmod(i, cols)
            
            # Create button frame with border
            btn_frame = ttk.Frame(grid_frame, borderwidth=2, relief=tk.RAISED)
            btn_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            # Add color indicator
            color_indicator = tk.Frame(btn_frame, background=timer["color"], height=5)
            color_indicator.pack(fill=tk.X, expand=False)
            
            # Add timer name
            ttk.Label(btn_frame, text=timer["name"], font=("", 12, "bold")).pack(pady=5)
            
            # Add duration
            ttk.Label(btn_frame, text=f"{timer['duration']} minutes").pack()
            
            # Add start button
            ttk.Button(btn_frame, text="Start Timer", 
                       command=lambda t=timer: self.start_timer(t)).pack(pady=10)
        
        # Configure grid weights
        rows, remainder = divmod(len(timer_list), cols)
        if remainder > 0:
            rows += 1
        
        for i in range(rows):
            grid_frame.rowconfigure(i, weight=1)
        for i in range(cols):
            grid_frame.columnconfigure(i, weight=1)
    
    def create_custom_timer(self):
        """Open dialog to create a custom timer"""
        # Create a new top-level window
        dialog = tk.Toplevel(self.root)
        dialog.title("Create Custom Timer")
        dialog.geometry("400x300")
        dialog.transient(self.root)  # Make it modal
        dialog.grab_set()
        
        # Position dialog next to main window
        self.position_dialog_window(dialog)
        
        # Form frame
        form_frame = ttk.Frame(dialog, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Timer name
        ttk.Label(form_frame, text="Timer Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=name_var, width=30).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Timer duration with hours, minutes, seconds
        ttk.Label(form_frame, text="Duration:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        # Create a frame for the time inputs
        time_frame = ttk.Frame(form_frame)
        time_frame.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Hours
        hours_var = tk.IntVar(value=0)
        ttk.Spinbox(time_frame, from_=0, to=24, textvariable=hours_var, width=3).pack(side=tk.LEFT)
        ttk.Label(time_frame, text="hours").pack(side=tk.LEFT, padx=(2, 10))
        
        # Minutes
        minutes_var = tk.IntVar(value=15)
        ttk.Spinbox(time_frame, from_=0, to=59, textvariable=minutes_var, width=3).pack(side=tk.LEFT)
        ttk.Label(time_frame, text="minutes").pack(side=tk.LEFT, padx=(2, 10))
        
        # Seconds
        seconds_var = tk.IntVar(value=0)
        ttk.Spinbox(time_frame, from_=0, to=59, textvariable=seconds_var, width=3).pack(side=tk.LEFT)
        ttk.Label(time_frame, text="seconds").pack(side=tk.LEFT, padx=(2, 5))
        
        # Color picker
        ttk.Label(form_frame, text="Color:").grid(row=2, column=0, sticky=tk.W, pady=5)
        color_var = tk.StringVar(value="#3498db")
        
        # Since tkinter doesn't have a built-in color picker, we'll use a combobox with common colors
        colors = {
            "Blue": "#3498db",
            "Green": "#2ecc71",
            "Red": "#e74c3c",
            "Purple": "#9b59b6",
            "Orange": "#e67e22",
            "Yellow": "#f1c40f",
            "Teal": "#1abc9c",
            "Gray": "#95a5a6"
        }
        
        color_combo = ttk.Combobox(form_frame, textvariable=color_var, values=list(colors.keys()), state="readonly", width=15)
        color_combo.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Function to update color_var with hex value when a color name is selected
        def update_color(*args):
            selected_color = color_combo.get()
            if selected_color in colors:
                color_var.set(colors[selected_color])
        
        color_combo.bind("<<ComboboxSelected>>", update_color)
        
        # Set initial selection
        color_combo.set("Blue")
        
        # Custom notification settings
        ttk.Label(form_frame, text="Custom Notifications:").grid(row=3, column=0, sticky=tk.W, pady=5)
        custom_notifications_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(form_frame, variable=custom_notifications_var).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        def save_custom_timer():
            # Validate inputs
            name = name_var.get().strip()
            hours = hours_var.get()
            minutes = minutes_var.get()
            seconds = seconds_var.get()
            color = color_var.get()
            
            # Calculate total duration in minutes (conversion to float for seconds)
            duration = hours * 60 + minutes + seconds / 60
            
            if not name:
                messagebox.showerror("Error", "Timer name is required", parent=dialog)
                return
            
            if duration < 0.1:  # Allow at least 6 seconds
                messagebox.showerror("Error", "Duration must be at least 6 seconds", parent=dialog)
                return
            
            # Create the new timer
            new_timer = {
                "name": name,
                "duration": duration,
                "color": color,
                "custom": True
            }
            
            # Add to timers list
            self.timers["custom"].append(new_timer)
            save_timers(self.timers)
            
            # Update UI
            self.refresh_timers_tab()
            
            # Close dialog
            dialog.destroy()
            
            self.status_var.set(f"Custom timer '{name}' created")
            logging.info(f"Created custom timer: {name}, {duration} min")
        
        ttk.Button(button_frame, text="Save", command=save_custom_timer).pack(side=tk.LEFT, padx=5)
    
    def position_dialog_window(self, dialog):
        """Position a dialog window next to the main window and ensure it's not off-screen"""
        self.root.update_idletasks()  # Ensure main window dimensions are updated
        
        # Get main window position and size
        main_x = self.root.winfo_x()
        main_y = self.root.winfo_y()
        main_width = self.root.winfo_width()
        main_height = self.root.winfo_height()
        
        # Get dialog dimensions
        dialog.update_idletasks()
        dialog_width = dialog.winfo_reqwidth()
        dialog_height = dialog.winfo_reqheight()
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # First try to position to the right of the main window
        x = main_x + main_width + 10
        y = main_y
        
        # If that would place it off-screen horizontally, try positioning to the left
        if x + dialog_width > screen_width:
            x = main_x - dialog_width - 10
        
        # If still off-screen horizontally, position at the right edge of screen
        if x < 0:
            x = max(0, screen_width - dialog_width)
        
        # If off-screen vertically, try to align with top of screen
        if y + dialog_height > screen_height:
            y = max(0, screen_height - dialog_height)
        
        # Apply the position
        dialog.geometry(f"+{x}+{y}")
    
    def refresh_timers_tab(self):
        """Refresh the timers tab to show updated timer list"""
        # Clear the tab
        for widget in self.timers_tab.winfo_children():
            widget.destroy()
        
        # Rebuild the tab
        self.setup_timers_tab()
    
    def setup_active_tab(self):
        """Set up the active timers tab"""
        # Scrollable frame for active timers
        self.active_frame = ttk.Frame(self.active_tab)
        self.active_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Initial message
        self.no_active_label = ttk.Label(self.active_frame, text="No active timers", font=("", 12))
        self.no_active_label.pack(pady=30)
    
    def setup_history_tab(self):
        """Set up the break history tab"""
        # Controls at the top
        control_frame = ttk.Frame(self.history_tab)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(control_frame, text="Break History").pack(side=tk.LEFT)
        ttk.Button(control_frame, text="Export to CSV", 
                  command=self.export_history).pack(side=tk.RIGHT, padx=5)
        ttk.Button(control_frame, text="Generate Report", 
                  command=self.generate_report).pack(side=tk.RIGHT, padx=5)
        
        # Treeview for history data
        columns = ("Date", "Time", "Break Type", "Duration", "Completed")
        self.history_tree = ttk.Treeview(self.history_tab, columns=columns, show="headings")
        
        # Configure the columns
        for col in columns:
            self.history_tree.heading(col, text=col)
            width = 120 if col in ("Break Type", "Duration") else 100
            self.history_tree.column(col, width=width, anchor=tk.CENTER)
        
        self.history_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.history_tree, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load history data
        self.load_history_data()
    
    def load_history_data(self):
        """Load and display break history data"""
        # Clear existing data
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        try:
            with open(os.path.join(DATA_DIR, "history.csv"), "r", newline="") as f:
                reader = csv.reader(f)
                headers = next(reader)  # Skip the header row
                
                for i, row in enumerate(reader):
                    self.history_tree.insert("", "end", values=row, iid=f"item{i}")
        except Exception as e:
            logging.error(f"Error loading history data: {e}")
            self.status_var.set("Error loading history data")
    
    def export_history(self):
        """Export history data to a CSV file"""
        # Ask for save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Break History"
        )
        
        if not file_path:
            return
        
        try:
            # Copy the history file to the selected location
            import shutil
            shutil.copy2(os.path.join(DATA_DIR, "history.csv"), file_path)
            
            self.status_var.set(f"History exported to {file_path}")
            logging.info(f"Exported history to {file_path}")
            messagebox.showinfo("Export Complete", f"Break history has been exported to:\n{file_path}")
        except Exception as e:
            logging.error(f"Error exporting history: {e}")
            self.status_var.set("Error exporting history")
            messagebox.showerror("Export Error", f"Failed to export history: {e}")
    
    def generate_report(self):
        """Generate a break compliance report"""
        # Create a new window for the report
        report_window = tk.Toplevel(self.root)
        report_window.title("Break Compliance Report")
        report_window.geometry("600x500")
        
        # Load history data
        try:
            breaks_data = []
            with open(os.path.join(DATA_DIR, "history.csv"), "r", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    breaks_data.append(row)
        except Exception as e:
            logging.error(f"Error reading history for report: {e}")
            ttk.Label(report_window, text=f"Error generating report: {e}").pack(pady=20)
            return
        
        # If no data
        if not breaks_data:
            ttk.Label(report_window, text="No break history available to generate a report.", 
                     font=("", 12)).pack(pady=20)
            return
        
        # Create report content
        report_frame = ttk.Frame(report_window, padding="20")
        report_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(report_frame, text="Break Compliance Report", 
                 font=("", 16, "bold")).pack(pady=10)
        
        # Time period
        if breaks_data:
            first_date = breaks_data[0]["Date"]
            last_date = breaks_data[-1]["Date"]
            period_text = f"Period: {first_date} to {last_date}"
        else:
            period_text = "No data available"
            
        ttk.Label(report_frame, text=period_text, font=("", 12)).pack(pady=5)
        
        # Statistics
        stats_frame = ttk.LabelFrame(report_frame, text="Statistics")
        stats_frame.pack(fill=tk.X, expand=False, pady=10)
        
        # Calculate statistics
        total_breaks = len(breaks_data)
        completed_breaks = sum(1 for b in breaks_data if b["Completed"] == "Yes")
        completion_rate = (completed_breaks / total_breaks * 100) if total_breaks > 0 else 0
        
        # Group by type
        break_types = {}
        for b in breaks_data:
            break_type = b["Break Type"]
            if break_type not in break_types:
                break_types[break_type] = {"total": 0, "completed": 0}
            
            break_types[break_type]["total"] += 1
            if b["Completed"] == "Yes":
                break_types[break_type]["completed"] += 1
        
        # Display statistics
        ttk.Label(stats_frame, text=f"Total Breaks: {total_breaks}").pack(anchor=tk.W, padx=10, pady=2)
        ttk.Label(stats_frame, text=f"Completed Breaks: {completed_breaks}").pack(anchor=tk.W, padx=10, pady=2)
        ttk.Label(stats_frame, text=f"Completion Rate: {completion_rate:.1f}%").pack(anchor=tk.W, padx=10, pady=2)
        
        # Break type statistics
        types_frame = ttk.LabelFrame(report_frame, text="Break Types")
        types_frame.pack(fill=tk.X, expand=False, pady=10)
        
        for break_type, stats in break_types.items():
            type_rate = (stats["completed"] / stats["total"] * 100) if stats["total"] > 0 else 0
            type_text = f"{break_type}: {stats['completed']}/{stats['total']} completed ({type_rate:.1f}%)"
            ttk.Label(types_frame, text=type_text).pack(anchor=tk.W, padx=10, pady=2)
        
        # Recommendations
        recommendations_frame = ttk.LabelFrame(report_frame, text="Recommendations")
        recommendations_frame.pack(fill=tk.X, expand=False, pady=10)
        
        if completion_rate < 50:
            recommendation = "You're missing more than half your breaks. Try setting more realistic break schedules."
        elif completion_rate < 80:
            recommendation = "Your break completion rate could be improved. Consider adjusting your break duration or frequency."
        else:
            recommendation = "Great job! You're taking regular breaks which is excellent for productivity and health."
            
        ttk.Label(recommendations_frame, text=recommendation, wraplength=500).pack(anchor=tk.W, padx=10, pady=5)
        
        # Action buttons
        button_frame = ttk.Frame(report_frame)
        button_frame.pack(fill=tk.X, expand=False, pady=10)
        
        ttk.Button(button_frame, text="Close", command=report_window.destroy).pack(side=tk.RIGHT, padx=5)
        
        def print_report():
            # In a real application, this would format and print the report
            messagebox.showinfo("Print", "Printing functionality would be implemented here.", parent=report_window)
            
        ttk.Button(button_frame, text="Print Report", command=print_report).pack(side=tk.RIGHT, padx=5)
        
        logging.info("Generated break compliance report")
    
    def setup_settings_tab(self):
        """Set up the settings tab"""
        settings_frame = ttk.Frame(self.settings_tab, padding="20")
        settings_frame.pack(fill=tk.BOTH, expand=True)
        
        # Notification settings
        notification_frame = ttk.LabelFrame(settings_frame, text="Notifications")
        notification_frame.pack(fill=tk.X, pady=10)
        
        # Sound toggle
        self.sound_var = tk.BooleanVar(value=self.settings.get("notification_sound", True))
        ttk.Checkbutton(notification_frame, text="Enable sound alerts", 
                       variable=self.sound_var).pack(anchor=tk.W, padx=20, pady=5)
        
        # Visual alerts toggle
        self.visual_var = tk.BooleanVar(value=self.settings.get("visual_alerts", True))
        ttk.Checkbutton(notification_frame, text="Enable visual notifications", 
                       variable=self.visual_var).pack(anchor=tk.W, padx=20, pady=5)
        
        # Application settings
        app_frame = ttk.LabelFrame(settings_frame, text="Application")
        app_frame.pack(fill=tk.X, pady=10)
        
        # Minimize to tray option
        self.tray_var = tk.BooleanVar(value=self.settings.get("minimize_to_tray", True))
        ttk.Checkbutton(app_frame, text="Minimize to system tray", 
                       variable=self.tray_var).pack(anchor=tk.W, padx=20, pady=5)
        
        # Start on boot option
        self.boot_var = tk.BooleanVar(value=self.settings.get("start_on_boot", False))
        ttk.Checkbutton(app_frame, text="Start on system boot", 
                       variable=self.boot_var).pack(anchor=tk.W, padx=20, pady=5)
        
        # Update check option
        self.update_var = tk.BooleanVar(value=self.settings.get("check_updates", True))
        ttk.Checkbutton(app_frame, text="Automatically check for updates", 
                       variable=self.update_var).pack(anchor=tk.W, padx=20, pady=5)
        
        # Theme selection
        theme_frame = ttk.Frame(app_frame)
        theme_frame.pack(fill=tk.X, padx=20, pady=5)
        
        ttk.Label(theme_frame, text="Theme:").pack(side=tk.LEFT, padx=5)
        
        themes = ["system", "clearlooks", "vista", "xpnative", "aqua", "clam", "alt"]
        self.theme_var = tk.StringVar(value=self.settings.get("theme", "system"))
        theme_combo = ttk.Combobox(theme_frame, textvariable=self.theme_var, 
                                  values=themes, state="readonly", width=15)
        theme_combo.pack(side=tk.LEFT, padx=5)
        
        # Buttons
        button_frame = ttk.Frame(settings_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(button_frame, text="Restore Defaults", 
                  command=self.restore_default_settings).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Save Settings", 
                  command=self.save_current_settings).pack(side=tk.RIGHT, padx=5)
        
        # About section
        about_frame = ttk.LabelFrame(settings_frame, text="About")
        about_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(about_frame, text=f"{SCRIPT_NAME} v{VERSION}").pack(anchor=tk.W, padx=20, pady=2)
        ttk.Label(about_frame, text="A customizable break timer application").pack(anchor=tk.W, padx=20, pady=2)
        
        # Add a hyperlink to a hypothetical website
        link_frame = ttk.Frame(about_frame)
        link_frame.pack(anchor=tk.W, padx=20, pady=2)
        
        ttk.Label(link_frame, text="Visit:").pack(side=tk.LEFT)
        
        # Create a hyperlink label (blue and underlined)
        link_label = ttk.Label(link_frame, text="www.breaktimer-app.com", 
                              foreground="blue", cursor="hand2")
        link_label.pack(side=tk.LEFT, padx=5)
        
        # Add underline
        font = link_label.cget("font")
        link_label.configure(font=(font, 9, "underline"))
    
    def restore_default_settings(self):
        """Restore settings to default values"""
        self.sound_var.set(DEFAULT_SETTINGS["notification_sound"])
        self.visual_var.set(DEFAULT_SETTINGS["visual_alerts"])
        self.tray_var.set(DEFAULT_SETTINGS["minimize_to_tray"])
        self.boot_var.set(DEFAULT_SETTINGS["start_on_boot"])
        self.update_var.set(DEFAULT_SETTINGS["check_updates"])
        self.theme_var.set(DEFAULT_SETTINGS["theme"])
        
        messagebox.showinfo("Settings", "Default settings have been restored. Click 'Save Settings' to apply.")
    
    def save_current_settings(self):
        """Save current settings configuration"""
        # Update settings dictionary
        self.settings["notification_sound"] = self.sound_var.get()
        self.settings["visual_alerts"] = self.visual_var.get()
        self.settings["minimize_to_tray"] = self.tray_var.get()
        self.settings["start_on_boot"] = self.boot_var.get()
        self.settings["check_updates"] = self.update_var.get()
        self.settings["theme"] = self.theme_var.get()
        
        # Save to file
        if save_settings(self.settings):
            messagebox.showinfo("Settings", "Settings saved successfully")
            self.status_var.set("Settings saved")
            logging.info("Settings saved")
            
            # If theme changed, notify about restart
            if self.theme_var.get() != self.settings.get("theme"):
                messagebox.showinfo("Theme Changed", 
                                  "The theme change will take effect after restarting the application")
        else:
            messagebox.showerror("Error", "Failed to save settings")
            self.status_var.set("Error saving settings")
    
    def setup_notification_system(self):
        """Set up the notification system"""
        # Initialize pygame mixer for sounds if needed
        if self.settings.get("notification_sound", True):
            try:
                pygame.mixer.init()
                logging.info("Sound system initialized")
            except Exception as e:
                logging.error(f"Failed to initialize sound system: {e}")
    
    def start_timer(self, timer_config):
        """Start a new break timer"""
        timer_id = f"{timer_config['name']}_{time.time()}"
        duration_sec = timer_config['duration'] * 60
        
        # Create timer object
        timer_obj = {
            "id": timer_id,
            "name": timer_config['name'],
            "duration": timer_config['duration'],
            "duration_sec": duration_sec,
            "color": timer_config['color'],
            "start_time": time.time(),
            "end_time": time.time() + duration_sec,
            "remaining": duration_sec,
            "progress": 0,
            "status": "active",
            "notifications": {
                "halfway": False,
                "almost_done": False
            }
        }
        
        # Add to active timers
        self.active_timers[timer_id] = timer_obj
        
        # Show notification
        self.show_notification(f"Started: {timer_config['name']}", 
                              f"Break timer for {timer_config['duration']} minutes has started")
        
        # Add timer to active tab
        self.add_timer_to_active_tab(timer_obj)
        
        # Start update cycle if not already running
        if self.update_job is None:
            self.update_timer_progress()
        
        self.status_var.set(f"Started {timer_config['name']} timer for {timer_config['duration']} minutes")
        logging.info(f"Started timer: {timer_config['name']}, {timer_config['duration']} min")
        
        # Switch to active tab
        self.notebook.select(self.active_tab)
    
    def add_timer_to_active_tab(self, timer_obj):
        """Add a timer to the active timers tab"""
        # Hide 'no active timers' message if visible
        if hasattr(self, 'no_active_label') and self.no_active_label.winfo_exists():
            self.no_active_label.pack_forget()
        
        # Create a frame for this timer
        timer_frame = ttk.LabelFrame(self.active_frame, text=timer_obj["name"])
        timer_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Store reference to the frame
        timer_obj["frame"] = timer_frame
        
        # Time display
        time_frame = ttk.Frame(timer_frame)
        time_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(time_frame, text="Time remaining:").pack(side=tk.LEFT, padx=5)
        
        # Time label with minutes:seconds format
        timer_obj["time_var"] = tk.StringVar(value=self.format_time(timer_obj["remaining"]))
        ttk.Label(time_frame, textvariable=timer_obj["time_var"], 
                 font=("", 12, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        timer_obj["progress_var"] = tk.DoubleVar(value=0)
        progress_bar = ttk.Progressbar(timer_frame, variable=timer_obj["progress_var"], 
                                      maximum=100, length=300)
        progress_bar.pack(fill=tk.X, padx=10, pady=5)
        
        # Control buttons
        button_frame = ttk.Frame(timer_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Pause/Resume button (future feature)
        timer_obj["pause_button"] = ttk.Button(button_frame, text="Pause", 
                                         command=lambda t=timer_obj: self.pause_timer(t))
        timer_obj["pause_button"].pack(side=tk.LEFT, padx=5)
        
        # Stop button
        ttk.Button(button_frame, text="Stop", 
                  command=lambda t=timer_obj: self.stop_timer(t, completed=False)).pack(side=tk.LEFT, padx=5)
        
        # Complete button
        ttk.Button(button_frame, text="Complete Break", 
                  command=lambda t=timer_obj: self.stop_timer(t, completed=True)).pack(side=tk.RIGHT, padx=5)
    
    def format_time(self, seconds):
        """Format seconds into MM:SS format"""
        minutes, seconds = divmod(int(seconds), 60)
        return f"{minutes:02d}:{seconds:02d}"
    
    def update_timer_progress(self):
        """Update all active timers"""
        now = time.time()
        active_count = 0
        
        for timer_id, timer in list(self.active_timers.items()):
            if timer["status"] != "active":
                continue
                
            active_count += 1
            
            # Calculate remaining time and progress
            elapsed = now - timer["start_time"]
            remaining = max(0, timer["duration_sec"] - elapsed)
            progress = min(100, (elapsed / timer["duration_sec"]) * 100)
            
            # Update timer object
            timer["remaining"] = remaining
            timer["progress"] = progress
            
            # Update UI elements
            timer["time_var"].set(self.format_time(remaining))
            timer["progress_var"].set(progress)
            
            # Check for timer completion
            if remaining <= 0:
                self.timer_completed(timer)
                continue
            
            # Check for halfway notification
            if not timer["notifications"]["halfway"] and progress >= 50:
                timer["notifications"]["halfway"] = True
                self.show_notification(f"{timer['name']} - Halfway", 
                                     self.reminders["halfway"])
            
            # Check for almost done notification
            if not timer["notifications"]["almost_done"] and progress >= 90:
                timer["notifications"]["almost_done"] = True
                self.show_notification(f"{timer['name']} - Almost Done", 
                                     self.reminders["almost_done"])
        
        # Schedule next update if there are active timers
        if active_count > 0:
            self.update_job = self.root.after(1000, self.update_timer_progress)
        else:
            self.update_job = None
            
            # Show 'no active timers' message if all timers are stopped
            if not self.active_timers:
                self.no_active_label.pack(pady=30)
    
    def timer_completed(self, timer):
        """Handle timer completion"""
        # Update status
        timer["status"] = "completed"
        
        # Show notification
        self.show_notification(f"{timer['name']} Completed", 
                             self.reminders["completed"])
        
        # Play sound
        self.play_sound("alert2.wav")
        
        # Record in history
        record_break_history(timer["name"], timer["duration"], completed=True)
        
        # Remove from active timers
        self.remove_timer(timer)
    
    def pause_timer(self, timer):
        """Pause or resume a timer"""
        if timer["status"] == "active":
            # Pause the timer
            timer["status"] = "paused"
            timer["pause_time"] = time.time()
            timer["pause_button"].configure(text="Resume")
            self.status_var.set(f"Paused {timer['name']} timer")
            logging.info(f"Paused timer: {timer['name']}")
        else:
            # Resume the timer
            timer["status"] = "active"
            
            # Adjust start and end times
            pause_duration = time.time() - timer["pause_time"]
            timer["start_time"] += pause_duration
            timer["end_time"] += pause_duration
            
            timer["pause_button"].configure(text="Pause")
            self.status_var.set(f"Resumed {timer['name']} timer")
            logging.info(f"Resumed timer: {timer['name']}")
    
    def stop_timer(self, timer, completed=False):
        """Stop a timer"""
        # Update status
        timer["status"] = "stopped"
        
        # Record in history
        record_break_history(timer["name"], timer["duration"], completed=completed)
        
        # Show notification if break was completed manually
        if completed:
            self.show_notification(f"{timer['name']} Completed", 
                                 "Break marked as completed")
        
        self.status_var.set(f"Stopped {timer['name']} timer")
        logging.info(f"Stopped timer: {timer['name']}, completed: {completed}")
        
        # Remove from active timers
        self.remove_timer(timer)
    
    def remove_timer(self, timer):
        """Remove a timer from the active timers list and UI"""
        # Remove the frame from UI
        if "frame" in timer and timer["frame"].winfo_exists():
            timer["frame"].destroy()
        
        # Remove from active timers dict
        if timer["id"] in self.active_timers:
            del self.active_timers[timer["id"]]
        
        # Show 'no active timers' message if all timers are stopped
        if not self.active_timers:
            self.no_active_label.pack(pady=30)
    
    def show_notification(self, title, message):
        """Show a system notification"""
        if self.settings.get("visual_alerts", True):
            try:
                notification.notify(
                    title=title,
                    message=message,
                    app_name=SCRIPT_NAME,
                    timeout=10
                )
                logging.info(f"Showed notification: {title}")
            except Exception as e:
                logging.error(f"Failed to show notification: {e}")
        
        # Play sound
        if self.settings.get("notification_sound", True):
            self.play_sound("alert1.wav")
    
    def play_sound(self, sound_file):
        """Play a notification sound"""
        if not self.settings.get("notification_sound", True):
            return
            
        try:
            sound_path = os.path.join(SOUNDS_DIR, sound_file)
            if os.path.exists(sound_path) and os.path.getsize(sound_path) > 0:
                pygame.mixer.music.load(sound_path)
                pygame.mixer.music.play()
                logging.info(f"Played sound: {sound_file}")
            else:
                # Play system beep if sound file is missing or empty
                import winsound
                winsound.MessageBeep()
        except Exception as e:
            logging.error(f"Failed to play sound: {e}")
            try:
                # Fallback to system beep
                import winsound
                winsound.MessageBeep()
            except:
                pass
    
    def on_close(self):
        """Handle application closing"""
        # Check if there are active timers
        active_count = sum(1 for t in self.active_timers.values() if t["status"] == "active")
        
        if active_count > 0:
            response = messagebox.askyesno("Confirm Exit", 
                                         "There are active timers running. Are you sure you want to exit?")
            if not response:
                return
        
        # Save settings
        save_settings(self.settings)
        
        # Record any active timers as not completed
        for timer in self.active_timers.values():
            if timer["status"] == "active":
                record_break_history(timer["name"], timer["duration"], completed=False)
        
        logging.info("Application closed")
        self.root.destroy()

def check_and_run():
    """Check installation status and run the application"""
    # Check if this is the first run
    is_first_run = not os.path.exists(os.path.join(CONFIG_DIR, ".installed"))
    
    # Setup logging
    setup_logging()
    logging.info(f"Starting {SCRIPT_NAME} v{VERSION}")
    
    if is_first_run:
        logging.info("First run detected")
        first_time_install()
    else:
        logging.info("Checking for updates")
        check_for_updates()
    
    # Import required modules for GUI
    try:
        import tkinter as tk
        from tkinter import ttk, messagebox, filedialog
        from plyer import notification
        import pygame
        from PIL import Image, ImageTk
        from ttkthemes import ThemedTk
    except ImportError as e:
        logging.error(f"Failed to import required modules: {e}")
        if not BACKGROUND_MODE:
            print(f"Error: Missing required modules. Please run the application again.")
        sys.exit(1)
    
    # Create root window (themed if possible)
    try:
        root = ThemedTk()
    except Exception:
        root = tk.Tk()
    
    # Initialize the application
    app = BreakTimer(root)
    
    # Run the main loop
    root.mainloop()

if __name__ == "__main__":
    # Handle running in background mode
    if BACKGROUND_MODE and platform.system() == "Windows":
        try:
            import ctypes
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except:
            pass
    
    # Run the application
    check_and_run()
