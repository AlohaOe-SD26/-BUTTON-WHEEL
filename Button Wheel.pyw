# -*- coding: utf-8 -*-
# PYTHON SCRIPT FOR BUTTON WHEEL (Version: Reverted + AHK Script Creation & Launch)

# --- Bootstrap & Dependency Check ---
import sys
import os
import subprocess
import importlib.metadata
import logging
import time
from pathlib import Path
import shutil
import traceback # Ensure traceback is imported for exception hook
try:
    # Conditional import for Windows-specific sound
    if sys.platform == "win32":
        import winsound
    else:
        winsound = None # Flag that winsound is not available
except ImportError:
    winsound = None # Handle case where module might be missing even on Windows

# --- Configuration ---
REQUIRED_PACKAGES = {"PySide6": "PySide6", "pynput": "pynput"}
APP_NAME = "ButtonWheel"; PROFILES_DIR_NAME = "PROFILES"; LOG_DIR_NAME = "LOGS"; SCRIPTS_DIR_NAME = "Scripts"
LOGGING_INITIALIZED = False

try:
    if getattr(sys, 'frozen', False):
        BASE_DIR = Path(sys.executable).parent.resolve()
    else:
        BASE_DIR = Path(__file__).parent.resolve()
except NameError:
    BASE_DIR = Path.cwd()
    print(f"WARNING: '__file__' not defined, using CWD: {BASE_DIR}", file=sys.stderr)

PROFILES_DIR = BASE_DIR / PROFILES_DIR_NAME
LOG_DIR = BASE_DIR / LOG_DIR_NAME
SCRIPTS_DIR = BASE_DIR / SCRIPTS_DIR_NAME

# --- Early Logging Setup ---
def setup_early_logging():
    # ... (Setup logging - No changes needed here) ...
    global LOGGING_INITIALIZED
    try:
        if not os.access(str(BASE_DIR), os.W_OK): print(f"CRITICAL ERROR: Cannot write to base directory '{BASE_DIR}'. Check permissions.", file=sys.stderr); return False
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        if not os.access(str(LOG_DIR), os.W_OK): print(f"CRITICAL ERROR: Log directory '{LOG_DIR}' is not writable. Check permissions.", file=sys.stderr); return False
        log_filename = LOG_DIR / f"{time.strftime('%Y-%m-%d_%H-%M-%S')}_ERROR_LOG.log"
        log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(module)s:%(lineno)d] - %(message)s')
        root_logger = logging.getLogger(); root_logger.setLevel(logging.DEBUG)
        if root_logger.hasHandlers(): root_logger.handlers.clear()
        file_handler = logging.FileHandler(log_filename, encoding='utf-8'); file_handler.setFormatter(log_formatter); file_handler.setLevel(logging.WARNING); root_logger.addHandler(file_handler)
        console_handler = logging.StreamHandler(sys.stderr); console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s')); console_handler.setLevel(logging.INFO); root_logger.addHandler(console_handler)
        logging.info(f"Logging initialized (File Level: WARNING, Console Level: INFO). Log file: {log_filename}")
        LOGGING_INITIALIZED = True; return True
    except Exception as e: print(f"CRITICAL ERROR: Failed to set up logging: {e}", file=sys.stderr); traceback.print_exc(file=sys.stderr); LOGGING_INITIALIZED = False; return False
if not setup_early_logging():
    if sys.stdin.isatty(): input("Press Enter to exit...")
    sys.exit(1)

# --- Dependency Check Function ---
def check_and_install_dependencies():
    # ... (Check dependencies - No changes needed here) ...
    logging.info("Checking dependencies...")
    packages_to_install = []
    for pkg_name, import_name in REQUIRED_PACKAGES.items():
        try: version = importlib.metadata.version(import_name); logging.info(f"Found {pkg_name} version {version}")
        except importlib.metadata.PackageNotFoundError: logging.warning(f"Dependency '{pkg_name}' not found."); packages_to_install.append(pkg_name)
        except Exception as e: logging.error(f"Error checking dependency '{pkg_name}': {e}"); packages_to_install.append(pkg_name)
    if not packages_to_install: logging.info("All dependencies are satisfied."); return True
    logging.warning(f"Attempting to install missing packages: {', '.join(packages_to_install)}")
    print(f"INFO: Attempting to install: {', '.join(packages_to_install)}... (Details in log file)", file=sys.stderr); sys.stderr.flush()
    try:
        try: pip_check_args = [sys.executable, "-m", "pip", "--version"]; subprocess.check_output(pip_check_args, stderr=subprocess.STDOUT); logging.info("pip command found.")
        except (subprocess.CalledProcessError, FileNotFoundError) as e: logging.critical(f"'pip' command check failed: {e}. Ensure Python/pip are in PATH."); print("CRITICAL ERROR: 'pip' required but not found/failed.", file=sys.stderr); return False
        install_args = [sys.executable, "-m", "pip", "install"] + packages_to_install; logging.info(f"Running command: {' '.join(install_args)}")
        install_process = subprocess.Popen(install_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace'); install_stdout, install_stderr = install_process.communicate(); returncode = install_process.returncode
        if install_stdout: logging.info(f"pip install stdout:\n{install_stdout.strip()}")
        if install_stderr: logging.warning(f"pip install stderr:\n{install_stderr.strip()}")
        logging.info(f"pip install process finished with return code: {returncode}")
        if returncode != 0: logging.critical(f"pip install failed (code: {returncode}). Try installing manually: pip install {' '.join(packages_to_install)}"); print(f"CRITICAL ERROR: Failed to install required packages. Check log.", file=sys.stderr); return False
        else:
            logging.info("pip install seems successful. Verifying..."); print("INFO: Installation attempt finished. Verifying...", file=sys.stderr)
            all_found = True
            for pkg_name, import_name in REQUIRED_PACKAGES.items():
                try: version = importlib.metadata.version(import_name); logging.info(f"Verified {pkg_name} version {version}")
                except importlib.metadata.PackageNotFoundError: logging.critical(f"Verification FAILED for {pkg_name} after install."); print(f"CRITICAL ERROR: Package '{pkg_name}' verification failed!", file=sys.stderr); all_found = False
            if not all_found: print("CRITICAL ERROR: Package verification failed.", file=sys.stderr); return False
            logging.info("Dependency verification successful."); print("INFO: Dependency verification successful.", file=sys.stderr); return True
    except Exception as e: logging.critical(f"Unexpected error during dependency installation: {e}"); logging.exception(e); print(f"CRITICAL ERROR during dependency installation: {e}", file=sys.stderr); return False
logging.info(f"--- Starting {APP_NAME} ---"); logging.info(f"Base directory: {BASE_DIR}")
if not check_and_install_dependencies():
    logging.critical("Exiting due to dependency issues.")
    if sys.stdin.isatty(): input("Press Enter to exit...")
    sys.exit(1)

# --- Main Application Imports ---
logging.info("Loading application modules...")
try:
    import json; import math; import traceback; import webbrowser; import shlex; import threading; from datetime import datetime; import importlib.resources
    from PySide6.QtWidgets import ( QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QRadioButton, QLineEdit, QListWidget, QListWidgetItem, QTabWidget, QStackedWidget, QSpinBox, QSizePolicy, QFrame, QScrollArea, QColorDialog, QFontDialog, QSystemTrayIcon, QMenu, QFileDialog, QSpacerItem, QMessageBox, QComboBox, QProgressBar, QInputDialog, QCheckBox )
    from PySide6.QtGui import ( QPainter, QPen, QColor, QBrush, QFont, QIcon, QPixmap, QPainterPath, QPolygonF, QCursor, QAction, QDesktopServices )
    from PySide6.QtCore import ( Qt, Signal, QRect, QPoint, QSize, QPointF, QRectF, QThread, QObject, QTimer, QUrl, QItemSelectionModel, Slot, QMetaObject )
    from pynput import keyboard
    logging.info("Application modules loaded successfully.")
except ImportError as e: logging.critical(f"Failed to import required module '{e.name}'."); logging.exception(e); print(f"CRITICAL ERROR: Failed import '{e.name}'.", file=sys.stderr); sys.exit(1)
except Exception as e: logging.critical(f"Unexpected error during main imports: {e}"); logging.exception(e); print(f"CRITICAL ERROR during application imports: {e}", file=sys.stderr); sys.exit(1)

# --- constants.py ---
# ... (No changes needed here) ...
PROFILE_SCHEMA_VERSION = "1.0"; DEFAULT_PROFILE_NAME = "default.json"; ACTIVE_PROFILE_CONFIG = BASE_DIR / ".active_profile"
INNER_RADIUS = 35; OUTER_RADIUS = 85; BUTTON_DIAMETER = 40; BUTTON_RADIUS = BUTTON_DIAMETER / 2; HOVER_SCALE_FACTOR = 1.1
BUTTON_SLOTS = [ "inner_top", "inner_bottom", "inner_left", "inner_right", "outer_E", "outer_NE", "outer_N", "outer_NW", "outer_W", "outer_SW", "outer_S", "outer_SE", ]
DEFAULT_HOTKEY = "<ctrl>+<alt>+w"

# --- profile_manager.py ---
class ProfileManager:
    # ... (No changes needed here) ...
    def __init__(self): self.profiles_dir = PROFILES_DIR; self.active_profile_path = None; self.ensure_profiles_dir(); self.load_active_profile_path()
    def ensure_profiles_dir(self):
        try: self.profiles_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e: logging.critical(f"Error creating profiles directory {self.profiles_dir}: {e}")
    def get_profile_path(self, profile_name):
        if not profile_name: return None
        if not profile_name.lower().endswith('.json'): profile_name += '.json'
        return self.profiles_dir / profile_name
    def list_profiles(self):
        self.ensure_profiles_dir(); profiles = []
        try:
            for item in self.profiles_dir.glob('*.json'):
                if item.is_file(): profiles.append(item.stem)
        except Exception as e: logging.error(f"Error listing profiles in {self.profiles_dir}: {e}")
        return sorted(profiles)
    def load_profile_data(self, profile_name=None):
        path_to_load = None
        if profile_name: path_to_load = self.get_profile_path(profile_name)
        elif self.active_profile_path and self.active_profile_path.exists(): path_to_load = self.active_profile_path
        else:
            default_path = self.get_profile_path(DEFAULT_PROFILE_NAME)
            if default_path.exists(): path_to_load = default_path
            else: logging.warning("No active profile set and default.json not found."); return self.get_default_profile_structure()
        if not path_to_load or not path_to_load.exists(): logging.error(f"Profile not found: {path_to_load or profile_name}"); return self.get_default_profile_structure()
        try:
            with open(path_to_load, 'r', encoding='utf-8') as f: data = json.load(f)
            if 'version' not in data or 'buttons' not in data: logging.warning(f"Profile {path_to_load.name} invalid/outdated."); return self.get_default_profile_structure()
            logging.info(f"Loaded profile: {path_to_load.name}")
            loaded_buttons = data.get("buttons", {}); changed = False
            for slot_id in BUTTON_SLOTS:
                if slot_id not in loaded_buttons: logging.warning(f"Slot '{slot_id}' missing in '{path_to_load.name}'. Adding default."); loaded_buttons[slot_id] = self.get_default_button_data(slot_id); changed = True
            if changed: data["buttons"] = loaded_buttons
            data.setdefault('global_settings', {}); data['global_settings'].setdefault('show_hide_hotkey', DEFAULT_HOTKEY)
            return data
        except json.JSONDecodeError as e: logging.error(f"Error decoding JSON profile {path_to_load.name}: {e}")
        except Exception as e: logging.error(f"Error reading profile {path_to_load.name}: {e}")
        return self.get_default_profile_structure()
    def save_profile_data(self, profile_name, data):
        if not profile_name: logging.error("Save failed: No profile name specified."); return False
        save_path = self.get_profile_path(profile_name); self.ensure_profiles_dir()
        data.setdefault('version', PROFILE_SCHEMA_VERSION); data.setdefault('global_settings', {}); data.setdefault('buttons', {})
        data['global_settings'].setdefault('show_hide_hotkey', DEFAULT_HOTKEY)
        try:
            with open(save_path, 'w', encoding='utf-8') as f: json.dump(data, f, indent=4)
            logging.info(f"Saved profile: {save_path.name}"); return True
        except IOError as e: logging.error(f"IOError saving profile {save_path.name}: {e}")
        except Exception as e: logging.error(f"Unexpected error saving profile {save_path.name}: {e}"); logging.exception(e)
        return False
    def get_default_profile_structure(self):
        profile = {"version": PROFILE_SCHEMA_VERSION, "global_settings": {"show_hide_hotkey": DEFAULT_HOTKEY }, "buttons": {}}
        for slot_id in BUTTON_SLOTS: profile["buttons"][slot_id] = self.get_default_button_data(slot_id)
        return profile
    def get_default_button_data(self, slot_id): return {"label": "", "icon_path": "", "action_type": "None", "target": "", "arguments": ""}
    def load_active_profile_path(self):
        try:
            if ACTIVE_PROFILE_CONFIG.exists():
                active_name = ACTIVE_PROFILE_CONFIG.read_text(encoding='utf-8').strip(); path = self.get_profile_path(active_name)
                if path and path.exists(): self.active_profile_path = path; logging.info(f"Active profile set to: {active_name}")
                else: logging.warning(f"Saved active profile '{active_name}' not found."); self.active_profile_path = None; ACTIVE_PROFILE_CONFIG.unlink(missing_ok=True)
            else: logging.info("No active profile config file found."); self.active_profile_path = None
        except Exception as e: logging.error(f"Error loading active profile config: {e}"); self.active_profile_path = None
    def set_active_profile(self, profile_name):
        path = self.get_profile_path(profile_name)
        if not path or not path.exists(): logging.error(f"Cannot set active profile: '{profile_name}' not found."); return False
        try: ACTIVE_PROFILE_CONFIG.write_text(profile_name, encoding='utf-8'); self.active_profile_path = path; logging.info(f"Set active profile to: {profile_name}"); return True
        except Exception as e: logging.error(f"Error saving active profile config: {e}"); return False
    def get_active_profile_name(self): return self.active_profile_path.stem if self.active_profile_path else None

# --- action_handler.py ---
class ActionHandler:
    # ... (No changes needed here) ...
    def __init__(self, controller=None): self.controller = controller
    def execute_action(self, button_data):
        action_type=button_data.get("action_type", "None"); target=button_data.get("target", ""); args_string=button_data.get("arguments", ""); label=button_data.get("label", "Unnamed Button"); logging.info(f"Executing action for '{label}': Type={action_type}, Target={target}")
        try:
            if action_type == "None": return
            elif action_type == "Launch App":
                if not target: logging.warning("Launch App failed: No target specified."); self.show_error("Action Error", "No target application specified."); return
                target_path = Path(target); resolved_path_str = target
                if not target_path.exists():
                    resolved_path = shutil.which(target)
                    if resolved_path: target_path = Path(resolved_path); resolved_path_str=resolved_path; logging.info(f"Resolved '{target}' to '{target_path}' using PATH.")
                    else: logging.error(f"Launch App failed: Target not found: {target}"); self.show_error("Action Error", f"Target application not found:\n{target}"); return
                command = [resolved_path_str]
                if args_string:
                    try: command.extend(shlex.split(args_string))
                    except ValueError as e: logging.error(f"Argument parsing error for '{args_string}': {e}"); self.show_error("Argument Error", f"Could not parse arguments:\n{args_string}\n\nError: {e}"); return
                logging.info(f"Running command: {command}"); creationflags = 0; start_new_session = False
                if sys.platform == "win32": creationflags = subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP
                else: start_new_session = True
                cwd = target_path.parent if target_path.parent.is_dir() else None; subprocess.Popen(command, cwd=cwd, creationflags=creationflags, start_new_session=start_new_session, close_fds=True)
            elif action_type == "Run CMD":
                if not target: logging.warning("Run CMD failed: No command specified."); self.show_error("Action Error", "No command specified."); return
                logging.info(f"Running CMD: {target}"); creationflags = 0; start_new_session = False
                if sys.platform == "win32": creationflags = subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP; full_cmd = ['cmd', '/c', target]
                else: start_new_session = True; full_cmd = ['sh', '-c', target]
                subprocess.Popen(full_cmd, creationflags=creationflags, start_new_session=start_new_session, close_fds=True)
            elif action_type == "Run Script" or action_type == "Run File":
                action_name = action_type;
                if not target: logging.warning(f"{action_name} failed: No target specified."); self.show_error("Action Error", f"No target file specified for '{action_name}'."); return
                target_path = Path(target).resolve();
                if not target_path.exists(): logging.error(f"{action_name} failed: Target not found: {target_path}"); self.show_error("Action Error", f"Target file/folder not found:\n{target_path}"); return
                logging.info(f"Attempting to open '{target_path}' using OS default handler.")
                success = QDesktopServices.openUrl(QUrl.fromLocalFile(str(target_path)))
                if not success: logging.error(f"Failed to open '{target_path}' using QDesktopServices."); self.show_error("Execution Error", f"Could not open file/script:\n{target_path}\n\nCheck file associations or permissions.")
            elif action_type == "Open URL":
                if not target: logging.warning("Open URL failed: No URL specified."); self.show_error("Action Error", "No URL specified."); return
                url_target = target
                if not (url_target.startswith("http://") or url_target.startswith("https://") or url_target.startswith("file:")):
                    local_path = Path(url_target)
                    try: resolved_local_path = local_path.resolve(strict=True); logging.info(f"Opening local path via URL action: {resolved_local_path}"); QDesktopServices.openUrl(QUrl.fromLocalFile(str(resolved_local_path))); return
                    except FileNotFoundError: logging.info(f"Local path '{url_target}' not found, treating as web URL."); url_target = "http://" + url_target
                    except Exception as path_e: logging.error(f"Error resolving local path '{url_target}': {path_e}"); url_target = "http://" + url_target
                logging.info(f"Opening web URL/URI: {url_target}"); QDesktopServices.openUrl(QUrl(url_target))
            elif action_type == "Switch Profile": logging.warning("Action 'Switch Profile' needs implementation in AppController."); self.show_error("Not Implemented", f"Action 'Switch Profile' to '{target}' is not fully implemented yet.")
            elif action_type == "OPEN_PROFILE_SELECTOR":
                logging.info("Opening Profile Selector window.");
                if self.controller and hasattr(self.controller, 'show_config_window'): QTimer.singleShot(0, lambda: self.controller.show_config_window(target_tab_index=0))
                else: logging.error("AppController reference not available to ActionHandler."); self.show_error("Internal Error", "Cannot open profile selector.")
            else: logging.warning(f"Unknown action type encountered: {action_type}")
        except FileNotFoundError: logging.error(f"Execution failed: Command or target not found: {target}"); self.show_error("Execution Error", f"Command or application not found:\n{target}")
        except PermissionError: logging.error(f"Execution failed: Permission denied for: {target}"); self.show_error("Execution Error", f"Permission denied to access:\n{target}")
        except Exception as e: logging.critical(f"Unexpected error executing action for '{label}': {e}"); logging.exception(e); self.show_error("Unexpected Error", f"An error occurred:\n{e}")
    def show_error(self, title, message):
        def _do_show():
            try:
                if QApplication.instance(): msg_box = QMessageBox(QMessageBox.Warning, title, message, QMessageBox.Ok); msg_box.setWindowFlags(msg_box.windowFlags() | Qt.WindowStaysOnTopHint); msg_box.exec()
                else: logging.warning(f"GUI unavailable for error: {title} - {message}"); print(f"ERROR: {title} - {message}", file=sys.stderr)
            except Exception as e: logging.error(f"Failed to show error message box: {e}"); logging.warning(f"(Original error was: {title} - {message})"); print(f"ERROR: {title} - {message}", file=sys.stderr)
        if QApplication.instance() and QThread.currentThread() != QApplication.instance().thread(): QTimer.singleShot(0, _do_show)
        else: _do_show()

# --- launcher_window.py ---
class LauncherWindow(QWidget):
    # ... (No changes needed here) ...
    item_activated = Signal(dict); hide_request = Signal()
    def __init__(self, profile_data): super().__init__(); self.profile_data = profile_data if profile_data else {}; self.button_geometries = {}; self.hovered_slot_id = None; self.center_pos = QPoint(0, 0); self.setup_ui(); self.calculate_button_geometries()
    def setup_ui(self): self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.ToolTip); self.setAttribute(Qt.WA_TranslucentBackground); self.setMouseTracking(True); diameter = (OUTER_RADIUS + BUTTON_RADIUS) * 2 + 20; self.initial_size = QSize(int(diameter), int(diameter)); self.resize(self.initial_size)
    def update_profile_data(self, new_profile_data): self.profile_data = new_profile_data if new_profile_data else {}; self.calculate_button_geometries(); self.update()
    def calculate_button_geometries(self):
        self.button_geometries = {}; center = QPointF(self.width() / 2.0, self.height() / 2.0); buttons_config = self.profile_data.get("buttons", {})
        inner_coords = {"inner_top": (center.x(), center.y() - INNER_RADIUS), "inner_bottom": (center.x(), center.y() + INNER_RADIUS), "inner_left": (center.x() - INNER_RADIUS, center.y()), "inner_right": (center.x() + INNER_RADIUS, center.y()),};
        for slot_id, pos in inner_coords.items(): rect = QRectF(pos[0] - BUTTON_RADIUS, pos[1] - BUTTON_RADIUS, BUTTON_DIAMETER, BUTTON_DIAMETER); self.button_geometries[slot_id] = {"rect": rect, "data": buttons_config.get(slot_id, {})}
        outer_angles = {"outer_E": 0, "outer_NE": 45, "outer_N": 90, "outer_NW": 135, "outer_W": 180, "outer_SW": 225, "outer_S": 270, "outer_SE": 315,};
        for slot_id, angle_deg in outer_angles.items(): angle_rad = math.radians(angle_deg); x = center.x() + OUTER_RADIUS * math.cos(angle_rad); y = center.y() - OUTER_RADIUS * math.sin(angle_rad); rect = QRectF(x - BUTTON_RADIUS, y - BUTTON_RADIUS, BUTTON_DIAMETER, BUTTON_DIAMETER); self.button_geometries[slot_id] = {"rect": rect, "data": buttons_config.get(slot_id, {})}
    def paintEvent(self, event):
        painter = QPainter(self); painter.setRenderHint(QPainter.Antialiasing); default_pen = QPen(QColor(50, 50, 50, 220), 2); default_brush = QBrush(QColor(150, 150, 150, 200)); hover_pen = QPen(QColor(255, 255, 0, 220), 3); hover_brush = QBrush(QColor(180, 180, 180, 230)); text_pen = QPen(Qt.white); label_font = QFont("Arial", 8)
        for slot_id, geom in self.button_geometries.items():
            rect = geom["rect"]; button_data = geom["data"]; label = button_data.get("label", ""); action_type = button_data.get("action_type", "None"); is_hovered = (slot_id == self.hovered_slot_id); is_active = (action_type != "None"); current_rect = rect; current_pen = default_pen; current_brush = default_brush
            if not is_active: c = current_brush.color(); c.setAlpha(100); current_brush.setColor(c); c = current_pen.color(); c.setAlpha(150); current_pen.setColor(c)
            if is_hovered and is_active: current_pen = hover_pen; current_brush = hover_brush; scale = HOVER_SCALE_FACTOR; current_rect = QRectF(rect.center().x() - BUTTON_RADIUS * scale, rect.center().y() - BUTTON_RADIUS * scale, BUTTON_DIAMETER * scale, BUTTON_DIAMETER * scale)
            painter.setPen(current_pen); painter.setBrush(current_brush); painter.drawEllipse(current_rect)
            if label and is_active: painter.setPen(text_pen); painter.setFont(label_font); painter.drawText(current_rect, Qt.AlignCenter | Qt.TextWordWrap, label)
    def _get_slot_id_at(self, point):
        active_buttons = {slot_id: geom["rect"] for slot_id, geom in self.button_geometries.items() if geom.get("data", {}).get("action_type", "None") != "None"};
        if self.hovered_slot_id and self.hovered_slot_id in active_buttons:
            geom_hovered = self.button_geometries[self.hovered_slot_id]; center_hovered = geom_hovered["rect"].center(); radius_sq_hovered = (BUTTON_RADIUS * HOVER_SCALE_FACTOR) ** 2; dist_sq_hovered = (point.x() - center_hovered.x())**2 + (point.y() - center_hovered.y())**2
            if dist_sq_hovered <= radius_sq_hovered: return self.hovered_slot_id
        for slot_id, rect in active_buttons.items():
            if slot_id == self.hovered_slot_id: continue
            center = rect.center(); radius_sq = (BUTTON_RADIUS ** 2); dist_sq = (point.x() - center.x())**2 + (point.y() - center.y())**2
            if dist_sq <= radius_sq: return slot_id
        return None
    def mouseMoveEvent(self, event):
        pos = event.position().toPoint(); current_hover_id = self._get_slot_id_at(pos)
        if current_hover_id != self.hovered_slot_id: self.hovered_slot_id = current_hover_id; self.update()
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            clicked_slot_id = self._get_slot_id_at(event.position().toPoint())
            if clicked_slot_id:
                button_data = self.button_geometries[clicked_slot_id].get("data", {})
                if button_data: logging.debug(f"Launcher emitting item_activated for {clicked_slot_id}"); self.item_activated.emit(button_data)
            else: logging.debug("Launcher emitting hide_request (background click)"); self.hide_request.emit()
        elif event.button() == Qt.RightButton: logging.debug("Launcher emitting hide_request (right-click)"); self.hide_request.emit()
    def leaveEvent(self, event):
        if self.hovered_slot_id is not None: self.hovered_slot_id = None; self.update()
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape: logging.debug("Launcher emitting hide_request (Escape key)"); self.hide_request.emit()
    def show_at_cursor(self):
        cursor_pos = QCursor.pos(); diameter = (OUTER_RADIUS + BUTTON_RADIUS) * 2 + 20; self.resize(int(diameter), int(diameter)); self.calculate_button_geometries(); x = cursor_pos.x() - self.width() // 2; y = cursor_pos.y() - self.height() // 2; self.move(x, y); logging.debug(f"Showing launcher at ({x},{y}) with size {self.size()}"); self.show(); self.activateWindow(); self.raise_()

# --- config_window.py ---
class ConfigWindow(QMainWindow):
    # ... (No changes needed here) ...
    profile_activated = Signal(str)
    def __init__(self, profile_manager, action_handler):
        super().__init__(); self.profile_manager = profile_manager; self.action_handler = action_handler; self.current_edit_profile_name = None; self.button_widgets = {}; self.is_modified = False
        self.setWindowTitle(f"{APP_NAME} - Configuration"); self.setMinimumSize(800, 600); self._init_ui(); self._connect_signals(); self.refresh_profile_list(); self.load_profile_for_editing(self.profile_manager.get_active_profile_name())
    def _init_ui(self):
        self.main_widget = QWidget(); self.setCentralWidget(self.main_widget); self.layout = QVBoxLayout(self.main_widget); self.tab_widget = QTabWidget(); self.layout.addWidget(self.tab_widget)
        self.profile_selector_tab = QWidget(); self.selector_layout = QVBoxLayout(self.profile_selector_tab); self.selector_group = QGroupBox("Available Profiles"); self.selector_group_layout = QVBoxLayout(); self.profile_list_widget = QListWidget(); self.profile_list_widget.setToolTip("Select a profile to activate or edit."); self.selector_group_layout.addWidget(self.profile_list_widget); self.selector_buttons_layout = QHBoxLayout(); self.activate_button = QPushButton("Set as Active Profile"); self.activate_button.setToolTip("Make the selected profile active when using the hotkey."); self.edit_selected_button = QPushButton("Edit Selected Profile"); self.edit_selected_button.setToolTip("Load the selected profile into the 'Profile Builder' tab."); self.delete_profile_button = QPushButton("Delete Selected"); self.selector_buttons_layout.addWidget(self.activate_button); self.selector_buttons_layout.addWidget(self.edit_selected_button); self.selector_buttons_layout.addStretch(); self.selector_buttons_layout.addWidget(self.delete_profile_button); self.selector_group_layout.addLayout(self.selector_buttons_layout); self.selector_group.setLayout(self.selector_group_layout); self.selector_layout.addWidget(self.selector_group); self.active_profile_label = QLabel("Active Profile: None"); self.selector_layout.addWidget(self.active_profile_label)
        self.hide_cmd_checkbox = QCheckBox("Hide Console Window on Startup"); self.hide_cmd_checkbox.setToolTip("Informational: Actual hiding requires saving the script with a '.pyw' extension on Windows."); self.hide_cmd_checkbox.setChecked(True); self.selector_layout.addWidget(self.hide_cmd_checkbox)
        self.hide_on_set_active_checkbox = QCheckBox("Hide Config Window on Set Active"); self.hide_on_set_active_checkbox.setToolTip("If checked, this configuration window will hide automatically after clicking 'Set as Active Profile'."); self.hide_on_set_active_checkbox.setChecked(True); self.selector_layout.addWidget(self.hide_on_set_active_checkbox)
        self.selector_layout.addStretch(); self.tab_widget.addTab(self.profile_selector_tab, "Profile Selector")
        self.profile_builder_tab = QWidget(); self.builder_layout = QVBoxLayout(self.profile_builder_tab); self.builder_profile_actions_layout = QHBoxLayout(); self.editing_profile_label = QLabel("Editing: None"); self.load_to_edit_button = QPushButton("Load Profile to Edit..."); self.load_to_edit_button.setToolTip("Select an existing profile to load into the editor."); self.new_profile_button = QPushButton("New Profile"); self.save_profile_button = QPushButton("Save Changes"); self.save_as_button = QPushButton("Save As..."); self.import_button = QPushButton("Import Profile..."); self.export_button = QPushButton("Export Profile..."); self.builder_profile_actions_layout.addWidget(self.editing_profile_label); self.builder_profile_actions_layout.addStretch(); self.builder_profile_actions_layout.addWidget(self.load_to_edit_button); self.builder_profile_actions_layout.addWidget(self.new_profile_button); self.builder_profile_actions_layout.addWidget(self.save_profile_button); self.builder_profile_actions_layout.addWidget(self.save_as_button); self.builder_profile_actions_layout.addWidget(self.import_button); self.builder_profile_actions_layout.addWidget(self.export_button); self.builder_layout.addLayout(self.builder_profile_actions_layout)
        self.global_settings_group = QGroupBox("Global Profile Settings"); self.global_settings_layout = QGridLayout(); self.global_settings_layout.addWidget(QLabel("Show/Hide Hotkey:"), 0, 0); self.hotkey_edit = QLineEdit(); self.hotkey_edit.setToolTip("Format: Modifiers (<ctrl>, <alt>, <shift>, <cmd>) joined by '+' then the key (e.g., w, <f1>, <space>).\nExample: <ctrl>+<alt>+w"); self.global_settings_layout.addWidget(self.hotkey_edit, 0, 1); self.global_settings_layout.setColumnStretch(1, 1); self.global_settings_group.setLayout(self.global_settings_layout); self.builder_layout.addWidget(self.global_settings_group)
        self.scroll_area = QScrollArea(); self.scroll_area.setWidgetResizable(True); self.scroll_content = QWidget(); self.scroll_layout = QVBoxLayout(self.scroll_content); self.scroll_area.setWidget(self.scroll_content); self.builder_layout.addWidget(self.scroll_area); action_types = ["None", "Launch App", "Run CMD", "Run Script", "Run File", "Open URL", "Switch Profile", "OPEN_PROFILE_SELECTOR"]; self.button_widgets = {}
        for slot_id in BUTTON_SLOTS:
            group_box = QGroupBox(f"Button: {slot_id.replace('_', ' ').title()}"); grid_layout = QGridLayout(); label_edit = QLineEdit(); icon_path_edit = QLineEdit(); browse_icon_button = QPushButton("..."); browse_icon_button.setFixedWidth(30); action_type_combo = QComboBox(); action_type_combo.addItems(action_types); target_edit = QLineEdit(); browse_target_button = QPushButton("..."); browse_target_button.setFixedWidth(30); args_label = QLabel("Arguments:"); args_edit = QLineEdit()
            grid_layout.addWidget(QLabel("Display Label:"), 0, 0); grid_layout.addWidget(label_edit, 0, 1, 1, 2); grid_layout.addWidget(QLabel("Icon Path:"), 1, 0); grid_layout.addWidget(icon_path_edit, 1, 1); grid_layout.addWidget(browse_icon_button, 1, 2); grid_layout.addWidget(QLabel("Action Type:"), 2, 0); grid_layout.addWidget(action_type_combo, 2, 1, 1, 2); grid_layout.addWidget(QLabel("Action Target:"), 3, 0); grid_layout.addWidget(target_edit, 3, 1); grid_layout.addWidget(browse_target_button, 3, 2); grid_layout.addWidget(args_label, 4, 0); grid_layout.addWidget(args_edit, 4, 1, 1, 2)
            self.button_widgets[slot_id] = {"group": group_box, "label": label_edit, "icon_path": icon_path_edit, "browse_icon": browse_icon_button, "action_type": action_type_combo, "target": target_edit, "browse_target": browse_target_button, "args_label": args_label, "args": args_edit}; args_label.setVisible(False); args_edit.setVisible(False); group_box.setLayout(grid_layout); self.scroll_layout.addWidget(group_box)
        self.scroll_layout.addStretch(); self.tab_widget.addTab(self.profile_builder_tab, "Profile Builder")
    def _connect_signals(self): # ... (No changes needed here) ...
        self.activate_button.clicked.connect(self.activate_selected_profile); self.edit_selected_button.clicked.connect(self.edit_selected_profile); self.delete_profile_button.clicked.connect(self.delete_selected_profile); self.profile_list_widget.itemDoubleClicked.connect(self.edit_selected_profile); self.load_to_edit_button.clicked.connect(self.load_existing_profile_into_builder); self.new_profile_button.clicked.connect(self.create_new_profile); self.save_profile_button.clicked.connect(self.save_edited_profile); self.save_as_button.clicked.connect(self.save_edited_profile_as); self.import_button.clicked.connect(self.import_profile); self.export_button.clicked.connect(self.export_profile); self.hotkey_edit.textChanged.connect(self.mark_as_modified)
        for slot_id, widgets in self.button_widgets.items():
            widgets["action_type"].currentIndexChanged.connect(lambda index, sid=slot_id: self.on_action_type_changed(sid)); widgets["browse_icon"].clicked.connect(lambda checked=False, sid=slot_id: self.browse_for_icon(sid)); widgets["browse_target"].clicked.connect(lambda checked=False, sid=slot_id: self.browse_for_target(sid)); widgets["label"].textChanged.connect(self.mark_as_modified); widgets["icon_path"].textChanged.connect(self.mark_as_modified); widgets["action_type"].currentIndexChanged.connect(self.mark_as_modified); widgets["target"].textChanged.connect(self.mark_as_modified); widgets["args"].textChanged.connect(self.mark_as_modified)
    def mark_as_modified(self, text=None): # ... (No changes needed here) ...
        if not self.is_modified: self.is_modified = True; self.update_window_title()
    def mark_as_saved(self): # ... (No changes needed here) ...
        if self.is_modified: self.is_modified = False; self.update_window_title()
    def update_window_title(self): # ... (No changes needed here) ...
        title = f"{APP_NAME} - Configuration"; profile_part = f" (Editing: {self.current_edit_profile_name}.json)" if self.current_edit_profile_name else " (Editing: New Profile)"; modified_part = "*" if self.is_modified else ""; self.setWindowTitle(f"{title}{profile_part}{modified_part}"); self.editing_profile_label.setText(f"Editing: {self.current_edit_profile_name or 'New Profile'}{modified_part}")
    def refresh_profile_list(self): # ... (No changes needed here) ...
        current_selection_text = None; item_to_select = None; current_item = self.profile_list_widget.currentItem()
        if current_item: current_selection_text = current_item.text()
        self.profile_list_widget.clear(); profiles = self.profile_manager.list_profiles(); self.profile_list_widget.addItems(profiles)
        if current_selection_text:
            items = self.profile_list_widget.findItems(current_selection_text, Qt.MatchFlag.MatchExactly)
            if items: item_to_select = items[0]
        active_name = self.profile_manager.get_active_profile_name()
        if active_name:
            self.active_profile_label.setText(f"Active Profile: {active_name}.json")
            if not item_to_select or (item_to_select and item_to_select.text() == active_name):
                items = self.profile_list_widget.findItems(active_name, Qt.MatchFlag.MatchExactly)
                if items: item_to_select = items[0]
        else: self.active_profile_label.setText("Active Profile: None")
        if item_to_select: self.profile_list_widget.setCurrentItem(item_to_select)
        try: self.profile_list_widget.currentItemChanged.disconnect()
        except RuntimeError: pass
        self.profile_list_widget.currentItemChanged.connect(self.on_profile_list_selection_changed)
        self.on_profile_list_selection_changed(self.profile_list_widget.currentItem(), None)
    def on_profile_list_selection_changed(self, current, previous): # ... (No changes needed here) ...
        has_selection = current is not None; self.activate_button.setEnabled(has_selection); self.edit_selected_button.setEnabled(has_selection); self.delete_profile_button.setEnabled(has_selection)
    def activate_selected_profile(self): # ... (No changes needed here) ...
        selected_item = self.profile_list_widget.currentItem();
        if not selected_item: self.action_handler.show_error("Error", "No profile selected."); return
        profile_name = selected_item.text()
        if self.profile_manager.set_active_profile(profile_name):
            logging.info(f"Profile '{profile_name}.json' activated."); self.profile_activated.emit(profile_name); self.refresh_profile_list()
            if self.hide_on_set_active_checkbox.isChecked(): logging.info("Hiding config window after setting active profile."); QTimer.singleShot(0, self.hide)
        else: self.action_handler.show_error("Error", f"Failed to activate profile '{profile_name}.json'. Check logs.")
    def edit_selected_profile(self): # ... (No changes needed here) ...
        selected_item = self.profile_list_widget.currentItem();
        if not selected_item: self.action_handler.show_error("Error", "No profile selected in the list to edit."); return
        profile_name = selected_item.text();
        if self.load_profile_for_editing(profile_name): self.tab_widget.setCurrentWidget(self.profile_builder_tab)
    def delete_selected_profile(self): # ... (No changes needed here) ...
        selected_item = self.profile_list_widget.currentItem();
        if not selected_item: self.action_handler.show_error("Error", "No profile selected to delete."); return
        profile_name = selected_item.text(); active_name = self.profile_manager.get_active_profile_name()
        if profile_name == active_name: self.action_handler.show_error("Delete Error", "Cannot delete the currently active profile."); return
        reply = QMessageBox.question(self, "Confirm Deletion", f"Are you sure you want to delete profile:\n{profile_name}.json?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            profile_path = self.profile_manager.get_profile_path(profile_name)
            try:
                if profile_path and profile_path.exists(): profile_path.unlink(); logging.info(f"Deleted profile: {profile_path}")
                else: logging.warning(f"Tried to delete profile, but path not found: {profile_path}")
                if self.current_edit_profile_name == profile_name: self.create_new_profile()
                self.refresh_profile_list()
            except OSError as e: logging.error(f"Error deleting profile file {profile_path}: {e}"); self.action_handler.show_error("Delete Error", f"Could not delete profile file:\n{e}")
            except Exception as e: logging.error(f"Unexpected error deleting profile {profile_path}: {e}"); self.action_handler.show_error("Delete Error", f"An unexpected error occurred:\n{e}")
    def confirm_discard_changes(self): # ... (No changes needed here) ...
        if not self.is_modified: return True
        reply = QMessageBox.question(self, "Unsaved Changes", f"You have unsaved changes in profile '{self.current_edit_profile_name or 'New Profile'}'.\nDiscard changes?", QMessageBox.Discard | QMessageBox.Cancel, QMessageBox.Cancel)
        return reply == QMessageBox.Discard
    def load_profile_for_editing(self, profile_name): # ... (No changes needed here) ...
        if not self.confirm_discard_changes(): return False
        if not profile_name:
            default_path = self.profile_manager.get_profile_path(DEFAULT_PROFILE_NAME)
            if default_path.exists(): profile_name = DEFAULT_PROFILE_NAME; logging.info(f"No profile specified, loading default: {profile_name}")
            else: logging.info("No profile specified and no default found, creating new."); return self.create_new_profile()
        profile_data = self.profile_manager.load_profile_data(profile_name)
        if not profile_data: self.action_handler.show_error("Load Error", f"Could not load profile '{profile_name}' for editing."); self.create_new_profile(); return False
        self.current_edit_profile_name = profile_name; global_settings = profile_data.get("global_settings", {}); hotkey = global_settings.get("show_hide_hotkey", DEFAULT_HOTKEY)
        self.hotkey_edit.blockSignals(True); self.hotkey_edit.setText(hotkey); self.hotkey_edit.blockSignals(False)
        buttons_config = profile_data.get("buttons", {})
        for slot_id, widgets in self.button_widgets.items():
            button_data = buttons_config.get(slot_id, self.profile_manager.get_default_button_data(slot_id))
            widgets["label"].blockSignals(True); widgets["label"].setText(button_data.get("label", "")); widgets["label"].blockSignals(False); widgets["icon_path"].blockSignals(True); widgets["icon_path"].setText(button_data.get("icon_path", "")); widgets["icon_path"].blockSignals(False); action_type = button_data.get("action_type", "None"); widgets["action_type"].blockSignals(True); index = widgets["action_type"].findText(action_type); widgets["action_type"].setCurrentIndex(index if index != -1 else 0); widgets["action_type"].blockSignals(False); widgets["target"].blockSignals(True); widgets["target"].setText(button_data.get("target", "")); widgets["target"].blockSignals(False); widgets["args"].blockSignals(True); widgets["args"].setText(button_data.get("arguments", "")); widgets["args"].blockSignals(False); self.update_button_widget_state(slot_id, action_type)
        self.save_profile_button.setEnabled(True); self.mark_as_saved(); self.update_window_title(); return True
    def load_existing_profile_into_builder(self): # ... (No changes needed here) ...
        profiles = self.profile_manager.list_profiles();
        if not profiles: self.action_handler.show_error("No Profiles", "There are no existing profiles to load."); return
        current_loaded_index = profiles.index(self.current_edit_profile_name) if self.current_edit_profile_name in profiles else 0
        profile_name, ok = QInputDialog.getItem(self, "Load Profile to Edit", "Select a profile:", profiles, current_loaded_index, False)
        if ok and profile_name: self.load_profile_for_editing(profile_name)
    def gather_data_from_builder(self): # ... (No changes needed here) ...
        profile_data = {"version": PROFILE_SCHEMA_VERSION, "global_settings": {}, "buttons": {}}; profile_data["global_settings"]["show_hide_hotkey"] = self.hotkey_edit.text() or DEFAULT_HOTKEY
        for slot_id, widgets in self.button_widgets.items(): profile_data["buttons"][slot_id] = {"label": widgets["label"].text(), "icon_path": widgets["icon_path"].text(), "action_type": widgets["action_type"].currentText(), "target": widgets["target"].text(), "arguments": widgets["args"].text() if widgets["args"].isVisible() else ""}
        return profile_data
    def save_edited_profile(self): # ... (No changes needed here) ...
        if not self.current_edit_profile_name: self.save_edited_profile_as(); return
        profile_data = self.gather_data_from_builder()
        if self.profile_manager.save_profile_data(self.current_edit_profile_name, profile_data):
            self.mark_as_saved(); self.action_handler.show_error("Success", f"Profile '{self.current_edit_profile_name}.json' saved.")
            if self.current_edit_profile_name == self.profile_manager.get_active_profile_name(): self.profile_activated.emit(self.current_edit_profile_name)
            self.refresh_profile_list()
        else: self.action_handler.show_error("Save Error", f"Failed to save profile '{self.current_edit_profile_name}.json'. Check logs.")
    def save_edited_profile_as(self): # ... (No changes needed here) ...
        profile_data = self.gather_data_from_builder(); suggested_name = self.current_edit_profile_name if self.current_edit_profile_name else "new_profile"; options = QFileDialog.Options()
        file_path_obj, selected_filter = QFileDialog.getSaveFileName(self, "Save Profile As", str(self.profile_manager.profiles_dir / f"{suggested_name}.json"), "JSON Files (*.json);;All Files (*)", options=options)
        if file_path_obj:
            save_path = Path(file_path_obj);
            if save_path.suffix.lower() != '.json': save_path = save_path.with_suffix('.json')
            profile_name = save_path.stem; save_result = self.profile_manager.save_profile_data(profile_name, profile_data)
            if save_result: self.mark_as_saved(); self.action_handler.show_error("Success", f"Profile saved as '{profile_name}.json'."); self.current_edit_profile_name = profile_name; self.update_window_title(); self.refresh_profile_list(); self.save_profile_button.setEnabled(True)
            else: self.action_handler.show_error("Save Error", f"Failed to save profile as '{profile_name}.json'. Check logs.")

    def create_new_profile(self): # Fixed NameError Here
        """Resets the builder UI to a default state."""
        if not self.confirm_discard_changes(): return False
        self.current_edit_profile_name = None; default_profile_data = self.profile_manager.get_default_profile_structure(); default_hotkey = default_profile_data.get("global_settings", {}).get("show_hide_hotkey", DEFAULT_HOTKEY)

        widgets_to_block = [
            self.hotkey_edit
        # --- CORRECTED LIST COMPREHENSION (Fix 2) ---
        ] + [self.button_widgets[slot][key] # Use correct access here
             for slot in self.button_widgets
             for key in self.button_widgets[slot]
             if isinstance(self.button_widgets[slot][key], (QLineEdit, QComboBox))]
        # --- END CORRECTION ---

        for widget in widgets_to_block: widget.blockSignals(True) # Block signals
        self.hotkey_edit.setText(default_hotkey)
        buttons_config = default_profile_data.get("buttons", {})
        for slot_id, widgets in self.button_widgets.items():
            button_data = buttons_config.get(slot_id, self.profile_manager.get_default_button_data(slot_id)); widgets["label"].setText(button_data.get("label", "")); widgets["icon_path"].setText(button_data.get("icon_path", "")); action_type = button_data.get("action_type", "None"); index = widgets["action_type"].findText(action_type); widgets["action_type"].setCurrentIndex(index if index != -1 else 0); widgets["target"].setText(button_data.get("target", "")); widgets["args"].setText(button_data.get("arguments", "")); self.update_button_widget_state(slot_id, action_type)
        for widget in widgets_to_block: widget.blockSignals(False) # Unblock signals
        self.save_profile_button.setEnabled(False); self.mark_as_saved(); self.update_window_title(); return True

    def import_profile(self): # ... (No changes needed here) ...
        options = QFileDialog.Options(); file_paths, _ = QFileDialog.getOpenFileNames(self, "Import Profile(s)", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_paths:
            imported_count = 0; errors = []; import shutil
            for file_path in file_paths:
                source_path = Path(file_path); dest_path = self.profile_manager.profiles_dir / source_path.name
                try:
                    try:
                        with open(source_path, 'r', encoding='utf-8') as f_in: temp_data = json.load(f_in)
                        if 'version' not in temp_data or 'buttons' not in temp_data: raise ValueError("Invalid profile structure")
                        logging.info(f"Validation passed for {source_path.name}")
                    except Exception as val_e: logging.warning(f"Skipping import of invalid profile {source_path.name}: {val_e}"); errors.append(f"{source_path.name}: Invalid format ({val_e})"); continue
                    if dest_path.exists():
                        reply = QMessageBox.warning(self, "Overwrite Confirmation", f"Profile '{source_path.name}' already exists. Overwrite?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.No)
                        if reply == QMessageBox.No: continue
                        elif reply == QMessageBox.Cancel: break
                    shutil.copy2(source_path, dest_path); logging.info(f"Imported profile: {source_path.name} to {dest_path}"); imported_count += 1
                except Exception as e: logging.error(f"Error importing profile {source_path.name}: {e}"); errors.append(f"{source_path.name}: {e}")
            message = f"Successfully imported {imported_count} profile(s)."
            if errors: message += "\n\nErrors or skips occurred during import:\n" + "\n".join(errors); self.action_handler.show_error("Import Complete with Issues", message)
            elif imported_count > 0: self.action_handler.show_error("Import Complete", message)
            if imported_count > 0: self.refresh_profile_list()
    def export_profile(self): # ... (No changes needed here) ...
        if not self.current_edit_profile_name: self.action_handler.show_error("Export Error", "No profile loaded in the builder to export."); return
        source_path = self.profile_manager.get_profile_path(self.current_edit_profile_name)
        if not source_path or not source_path.exists(): self.action_handler.show_error("Export Error", f"Cannot find source file for '{self.current_edit_profile_name}'. Save it first?"); return
        options = QFileDialog.Options(); dir_path = QFileDialog.getExistingDirectory(self, f"Select Directory to Export '{self.current_edit_profile_name}.json' to", "", options=options)
        if dir_path:
            dest_dir = Path(dir_path); dest_path = dest_dir / source_path.name
            try:
                if dest_path.exists():
                    reply = QMessageBox.warning(self, "Overwrite Confirmation", f"File '{dest_path.name}' already exists. Overwrite?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if reply == QMessageBox.No: return
                import shutil; shutil.copy2(source_path, dest_path); logging.info(f"Exported '{source_path.name}' to '{dest_path}'"); self.action_handler.show_error("Export Complete", f"Profile exported to:\n{dest_path}")
            except Exception as e: logging.error(f"Error exporting profile {source_path.name} to {dest_dir}: {e}"); self.action_handler.show_error("Export Error", f"Could not export profile:\n{e}")
    def on_action_type_changed(self, slot_id): # ... (No changes needed here) ...
        widgets = self.button_widgets[slot_id]; action_type = widgets["action_type"].currentText(); self.update_button_widget_state(slot_id, action_type); self.mark_as_modified()
    def update_button_widget_state(self, slot_id, action_type): # ... (No changes needed here) ...
        widgets = self.button_widgets[slot_id]; is_launch = (action_type == "Launch App"); is_script = (action_type == "Run Script"); is_cmd = (action_type == "Run CMD"); is_url = (action_type == "Open URL"); is_switch = (action_type == "Switch Profile"); is_open_selector = (action_type == "OPEN_PROFILE_SELECTOR"); is_none = (action_type == "None"); is_run_file = (action_type == "Run File")
        widgets["args_label"].setVisible(is_launch or is_script); widgets["args"].setVisible(is_launch or is_script); widgets["target"].setEnabled(not is_none and not is_open_selector); widgets["browse_target"].setEnabled(is_launch or is_script or is_switch or is_run_file)
        if is_none or is_open_selector: widgets["target"].setText(""); widgets["args"].setText("")
    def browse_for_icon(self, slot_id): # ... (No changes needed here) ...
        widgets = self.button_widgets[slot_id]; options = QFileDialog.Options(); file_path, _ = QFileDialog.getOpenFileName(self, "Select Icon File", "", "Image Files (*.png *.ico *.jpg *.bmp);;All Files (*)", options=options)
        if file_path: widgets["icon_path"].setText(file_path); self.mark_as_modified()
    def browse_for_target(self, slot_id): # ... (No changes needed here) ...
        widgets = self.button_widgets[slot_id]; action_type = widgets["action_type"].currentText(); current_target = widgets["target"].text(); start_dir = ""
        if current_target: target_path = Path(current_target);
        if target_path.is_file() and target_path.parent.exists(): start_dir = str(target_path.parent)
        elif target_path.is_dir() and target_path.exists(): start_dir = str(target_path)
        elif target_path.parent.exists(): start_dir = str(target_path.parent)
        options = QFileDialog.Options(); file_path = None
        if action_type == "Launch App":
            if not start_dir or not Path(start_dir).is_dir(): start_dir = str(BASE_DIR)
            file_path, _ = QFileDialog.getOpenFileName(self, "Select Application", start_dir, "Executables (*.exe *.app *.sh);;All Files (*)", options=options)
        elif action_type == "Run Script":
            scripts_dir_str = str(SCRIPTS_DIR);
            if not start_dir or not Path(start_dir).is_dir(): start_dir = scripts_dir_str
            try: SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
            except Exception as e: logging.error(f"Could not create Scripts directory {SCRIPTS_DIR}: {e}")
            file_path, _ = QFileDialog.getOpenFileName(self, "Select Script", start_dir, "Scripts (*.py *.pyw *.bat *.sh *.ahk);;All Files (*)", options=options)
        elif action_type == "Run File":
            if not start_dir or not Path(start_dir).is_dir(): start_dir = str(BASE_DIR)
            file_path, _ = QFileDialog.getOpenFileName(self, "Select File", start_dir, "All Files (*)", options=options)
        elif action_type == "Switch Profile":
            profiles = self.profile_manager.list_profiles(); current_index = profiles.index(current_target) if current_target in profiles else 0
            profile_name, ok = QInputDialog.getItem(self, "Select Profile to Switch To", "Profile:", profiles, current_index, False)
            if ok and profile_name: widgets["target"].setText(profile_name); self.mark_as_modified()
            return
        if file_path: widgets["target"].setText(file_path); self.mark_as_modified()
    def closeEvent(self, event): # ... (No changes needed here) ...
        if not self.confirm_discard_changes(): event.ignore(); return
        logging.info("Configuration window closing."); event.accept()
    def switch_to_tab(self, index): # ... (No changes needed here) ...
        if 0 <= index < self.tab_widget.count(): self.tab_widget.setCurrentIndex(index)

# --- hotkey_listener.py ---
class HotkeyListener(QObject):
    # ... (Class definition remains the same as provided) ...
    hotkey_pressed = Signal(); quit_signal = Signal()
    def __init__(self, hotkey_str):
        super().__init__(); self.hotkey_str = hotkey_str if hotkey_str else DEFAULT_HOTKEY; self.listener_thread = None; self.listener = None; self.stop_event = threading.Event(); self._setup_hotkey()
    def _setup_hotkey(self):
        self.activation_key_combo = self.hotkey_str; logging.info(f"Hotkey set to: {self.activation_key_combo}")
    def _listener_thread_target(self):
        try:
            hotkey_actions = { self.activation_key_combo: self.on_activate }; logging.info("Starting pynput listener...")
            try:
                with keyboard.GlobalHotKeys(hotkey_actions) as self.listener: logging.info("Pynput listener successfully created and started."); self.listener.join()
            except Exception as listener_init_e: logging.critical(f"Failed to create/start pynput listener: {listener_init_e}"); logging.exception(listener_init_e); QTimer.singleShot(0, lambda: ActionHandler().show_error("Hotkey Listener Error", f"Failed to initialize hotkey listener.\nCheck OS permissions or hotkey format ('{self.activation_key_combo}').\n\nError: {listener_init_e}")) ; return
        except ValueError as ve: logging.critical(f"Invalid hotkey format '{self.activation_key_combo}': {ve}"); QTimer.singleShot(0, lambda: ActionHandler().show_error("Invalid Hotkey", f"Invalid hotkey format configured:\n'{self.activation_key_combo}'\nPlease fix it in the profile settings."))
        except Exception as e:
            logging.critical(f"Error in hotkey listener thread: {e}"); logging.exception(e)
            if "listener" in str(e).lower() and ("permission" in str(e).lower() or "failed" in str(e).lower()): logging.critical("Check OS permissions for Input Monitoring (macOS) or input group/sudo (Linux)."); QTimer.singleShot(0, lambda: ActionHandler().show_error("Hotkey Listener Error", f"Could not maintain hotkey listener.\nCheck OS Input Monitoring/Permissions.\nError: {e}"))
            else: QTimer.singleShot(0, lambda: ActionHandler().show_error("Hotkey Listener Error", f"An unexpected error occurred:\n{e}"))
        finally: logging.info("Pynput listener thread stopped."); self.listener = None
    def on_activate(self): logging.info("Activation hotkey pressed!"); self.hotkey_pressed.emit()
    def start(self):
        if self.listener_thread is not None and self.listener_thread.is_alive(): logging.warning("Hotkey listener thread already running."); return
        logging.info("Starting hotkey listener thread..."); self.stop_event.clear(); self.listener_thread = threading.Thread(target=self._listener_thread_target, daemon=True); self.listener_thread.start()
    def stop(self):
        if not self.listener_thread or not self.listener_thread.is_alive(): return
        logging.info("Stopping hotkey listener..."); self.stop_event.set()
        listener_instance = getattr(self, 'listener', None)
        if listener_instance:
            try:
                # Correctly check for GlobalHotKeys specific stop method
                if isinstance(listener_instance, keyboard.GlobalHotKeys) and hasattr(listener_instance, 'stop'):
                    listener_instance.stop()
                else:
                    logging.warning(f"Listener instance is not GlobalHotKeys or has no stop method: {type(listener_instance)}")
            except Exception as e: logging.error(f"Error stopping pynput listener directly: {e}")
        if self.listener_thread and self.listener_thread.is_alive():
            self.listener_thread.join(timeout=1.0)
            if self.listener_thread.is_alive(): logging.warning("Hotkey listener thread did not stop gracefully after join.")
        self.listener_thread = None; self.listener = None; logging.info("Hotkey listener stopped.")
    def update_hotkey(self, new_hotkey_str):
        if not new_hotkey_str: new_hotkey_str = DEFAULT_HOTKEY
        if new_hotkey_str == self.hotkey_str: logging.info("Hotkey unchanged, listener restart not required."); return
        logging.info(f"Updating hotkey from '{self.hotkey_str}' to: '{new_hotkey_str}'"); self.stop(); time.sleep(0.1); self.hotkey_str = new_hotkey_str; self._setup_hotkey(); self.start()

# --- app_controller.py ---
class AppController(QObject):
    # ... (Rest of the class definition remains the same as provided) ...
    def __init__(self, app):
        super().__init__(); self.app = app; self.profile_manager = ProfileManager(); self.action_handler = ActionHandler(controller=self); self.config_window = ConfigWindow(self.profile_manager, self.action_handler); self.current_profile_data = self.profile_manager.load_profile_data(); self.launcher_window = LauncherWindow(self.current_profile_data); initial_hotkey = self.current_profile_data.get("global_settings", {}).get("show_hide_hotkey", DEFAULT_HOTKEY); self.hotkey_listener = HotkeyListener(initial_hotkey); self._connect_signals(); self.hotkey_listener.start(); self.config_window.show()
    def _connect_signals(self):
        self.hotkey_listener.hotkey_pressed.connect(self.toggle_launcher); self.launcher_window.item_activated.connect(self.on_launcher_item_activated); self.launcher_window.hide_request.connect(self.hide_launcher); self.config_window.profile_activated.connect(self.on_profile_activated)
    @Slot()
    def toggle_launcher(self):
        if QThread.currentThread() != self.thread(): QTimer.singleShot(0, self.toggle_launcher); return
        if self.launcher_window.isVisible(): self.hide_launcher()
        else:
            self.current_profile_data = self.profile_manager.load_profile_data()
            if not self.current_profile_data: logging.error("Failed to load profile data before showing launcher."); self.action_handler.show_error("Error", "Could not load active profile data."); return
            self.launcher_window.update_profile_data(self.current_profile_data); self.launcher_window.show_at_cursor()
    @Slot()
    def hide_launcher(self):
        if QThread.currentThread() != self.thread(): QTimer.singleShot(0, self.hide_launcher); return
        self.launcher_window.hide(); self.launcher_window.hovered_slot_id = None
    @Slot(dict)
    def on_launcher_item_activated(self, button_data):
        logging.debug("Controller received item_activated signal."); self.hide_launcher(); QTimer.singleShot(50, lambda bd=button_data: self.action_handler.execute_action(bd))

    # --- MODIFIED on_profile_activated ---
    @Slot(str)
    def on_profile_activated(self, profile_name):
        """Updates hotkey AND runs AHK script when a profile is activated."""
        logging.info(f"Controller notified: Profile '{profile_name}' activated.")
        self.current_profile_data = self.profile_manager.load_profile_data(profile_name)
        if not self.current_profile_data:
            logging.error(f"Failed to reload activated profile data for '{profile_name}'")
            return

        # Update Hotkey Listener
        new_hotkey = self.current_profile_data.get("global_settings", {}).get("show_hide_hotkey", DEFAULT_HOTKEY)
        if hasattr(self, 'hotkey_listener') and self.hotkey_listener:
            self.hotkey_listener.update_hotkey(new_hotkey)

        # --- ADDED: Run AHK Script ---
        ahk_script_filename = "Youtube Pause.ahk"
        ahk_script_path = SCRIPTS_DIR / ahk_script_filename
        if ahk_script_path.exists():
            logging.info(f"Attempting to run AHK script: {ahk_script_path}")
            try:
                # Use QDesktopServices to open the file with its associated application
                success = QDesktopServices.openUrl(QUrl.fromLocalFile(str(ahk_script_path)))
                if success:
                    logging.info(f"Successfully launched '{ahk_script_filename}'.")
                else:
                    logging.error(f"Failed to launch '{ahk_script_filename}' using QDesktopServices. Is AutoHotkey installed and associated?")
                    # Optionally show an error to the user
                    # self.action_handler.show_error("AHK Launch Error", f"Could not launch '{ahk_script_filename}'.\nEnsure AutoHotkey is installed and associated with .ahk files.")
            except Exception as e:
                logging.error(f"Error attempting to launch AHK script '{ahk_script_path}': {e}", exc_info=True)
                # Optionally show an error to the user
                # self.action_handler.show_error("AHK Launch Error", f"An unexpected error occurred while launching '{ahk_script_filename}':\n{e}")
        else:
            logging.warning(f"Cannot run AHK script: '{ahk_script_path}' not found.")
        # --- END ADDED ---

    @Slot()
    @Slot(int)
    def show_config_window(self, target_tab_index=None): # ... (No changes needed here) ...
        if QThread.currentThread() != self.thread(): QTimer.singleShot(0, lambda: self.show_config_window(target_tab_index)); return
        self.config_window.show(); self.config_window.raise_(); self.config_window.activateWindow()
        if target_tab_index is not None: self.config_window.switch_to_tab(target_tab_index)
    @Slot()
    def quit_application(self): # ... (No changes needed here) ...
        logging.info("Quit requested.");
        if hasattr(self, 'hotkey_listener') and self.hotkey_listener: self.hotkey_listener.stop()
        QTimer.singleShot(150, self.app.quit)

# --- AHK Script Content ---
YOUTUBE_PAUSE_AHK_CONTENT = r"""
; Auto-generated YOUTUBE PAUSE - PAUSE BUTTON script - Created by ButtonWheel Python Script

; Set the coordinate mode to screen
CoordMode, Mouse, Screen

; Define variables to store the selected click location and the original mouse location
global ClickX := 245
global ClickY := 103
global OriginalX := 0
global OriginalY := 0

; Hotkey to select the click location
!*::
{
    MouseGetPos, ClickX, ClickY
    MsgBox, Click location set to: %ClickX%, %ClickY%
    return
}

; Function to perform the volume up, volume down, and click sequence
PerformSequence()
{
    global ClickX, ClickY, OriginalX, OriginalY

    ; Log the current mouse position
    MouseGetPos, OriginalX, OriginalY

    ; Increase volume by 1
    Send {Volume_Up}
    Sleep, 50

    ; Decrease volume by 1
    Send {Volume_Down}
    Sleep, 50

    ; Teleport to the selected location and click
    MouseMove, %ClickX%, %ClickY%, 0
    Click
    Sleep, 50

    ; Teleport back to the original position
    MouseMove, %OriginalX%, %OriginalY%, 0

    return
}

; Hotkeys to perform the sequence
; `:: ; Backtick example - commented out
; PerformSequence()
; return

Pause:: ; Pause/Break key example
PerformSequence()
return
"""

# --- Main Execution ---
def main():
    # --- Start of main ---
    logging.info("--- Entering main() ---")
    try:
        # Ensure operational directories exist
        dirs_to_create = [PROFILES_DIR, SCRIPTS_DIR, LOG_DIR]; logging.info(f"Checking operational directories: {dirs_to_create}")
        for dir_path in dirs_to_create:
            parent_dir = dir_path.parent
            if not os.access(str(parent_dir), os.W_OK | os.X_OK): raise PermissionError(f"Cannot write/access parent directory: {parent_dir}")
            dir_path.mkdir(parents=True, exist_ok=True)
            if not os.access(str(dir_path), os.W_OK | os.X_OK): raise PermissionError(f"Cannot write/access directory: {dir_path}")
            logging.info(f"Ensured directory exists and is writable/accessible: {dir_path}")

        # --- Create Default AHK Script if it doesn't exist ---
        ahk_script_filename = "Youtube Pause.ahk"; ahk_script_path = SCRIPTS_DIR / ahk_script_filename
        if not ahk_script_path.exists():
            logging.info(f"'{ahk_script_filename}' not found in {SCRIPTS_DIR}. Creating default script...")
            try:
                with open(ahk_script_path, 'w', encoding='utf-8') as f_ahk: f_ahk.write(YOUTUBE_PAUSE_AHK_CONTENT)
                logging.info(f"Successfully created default '{ahk_script_filename}'.")
            except IOError as e: logging.error(f"Failed to create default AHK script '{ahk_script_path}': {e}")
            except Exception as e_general: logging.error(f"An unexpected error occurred while creating default AHK script: {e_general}", exc_info=True)
        else: logging.info(f"Default AHK script '{ahk_script_filename}' already exists.")
        # --- End AHK Script Creation ---

    except PermissionError as pe: logging.critical(f"Permission error setting up directories: {pe}"); print(f"CRITICAL ERROR: Permission denied accessing or writing to necessary directories.\nCheck permissions for: {pe}\nBase Directory: {BASE_DIR}", file=sys.stderr); sys.exit(1)
    except Exception as e: logging.critical(f"Cannot create necessary operational directories: {e}"); logging.exception(e); print(f"CRITICAL ERROR: Cannot create directories ({PROFILES_DIR_NAME}, {LOG_DIR_NAME}, {SCRIPTS_DIR_NAME}). Check permissions in {BASE_DIR}. Error: {e}", file=sys.stderr); sys.exit(1)

    # --- Rest of main ---
    logging.info("Setting up Qt Application..."); QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough); QApplication.setAttribute(Qt.AA_EnableHighDpiScaling); QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    try: app = QApplication(sys.argv)
    except Exception as e: logging.critical(f"Failed to create QApplication instance: {e}"); logging.exception(e); print(f"CRITICAL ERROR: Failed to create QApplication instance: {e}", file=sys.stderr); sys.exit(1)
    app.setQuitOnLastWindowClosed(False)
    logging.info("Setting up Controller and Tray Icon..."); controller = None; tray_icon = None; is_tray_available = QSystemTrayIcon.isSystemTrayAvailable()
    if is_tray_available:
        logging.info("System tray is available.")
        try:
            icon_pixmap = QPixmap(32, 32); icon_pixmap.fill(Qt.cyan); app_icon = QIcon(icon_pixmap)
            tray_icon = QSystemTrayIcon(app_icon); tray_icon.setToolTip(f"{APP_NAME} - Running"); menu = QMenu(); show_config_action = QAction("Show Configuration"); quit_action = QAction("Quit")
            menu.addAction(show_config_action); menu.addSeparator(); menu.addAction(quit_action); tray_icon.setContextMenu(menu)
            logging.info("Initializing AppController..."); controller = AppController(app); logging.info("AppController initialized.") # Controller init needs to be here
            app.aboutToQuit.connect(controller.quit_application); show_config_action.triggered.connect(controller.show_config_window); quit_action.triggered.connect(controller.quit_application)
            tray_icon.activated.connect(lambda reason: controller.show_config_window() if reason == QSystemTrayIcon.ActivationReason.Trigger else None); tray_icon.show()
        except Exception as e:
            logging.critical(f"Failed to setup application controller or tray icon: {e}"); logging.exception(e); print(f"CRITICAL ERROR: Failed to set up application UI or tray icon: {e}", file=sys.stderr)
            if controller and hasattr(controller, 'hotkey_listener'): controller.hotkey_listener.stop()
            if tray_icon: tray_icon.hide()
            if sys.stdin.isatty(): input("Press Enter to exit..."); sys.exit(1)
    else:
        logging.warning("QSystemTrayIcon not available. Running without tray icon."); print("WARNING: System tray icon not available on this system. Running without it.", file=sys.stderr)
        try:
            # Initialize controller even without tray
            logging.info("Initializing AppController (no tray)..."); controller = AppController(app); logging.info("AppController initialized.")
            app.aboutToQuit.connect(controller.quit_application); app.setQuitOnLastWindowClosed(True)
            logging.warning("Application will exit when configuration window is closed (no system tray).")
        except Exception as e: logging.critical(f"Failed to setup application controller without tray: {e}"); logging.exception(e); print(f"CRITICAL ERROR: Failed to set up application controller: {e}", file=sys.stderr); sys.exit(1)
    logging.info(f"{APP_NAME} started successfully."); print("--- Application Started (Logging to file in LOGS directory) ---", file=sys.stderr)
    exit_code = 0
    try: exit_code = app.exec()
    except Exception as e:
        logging.critical(f"Unhandled error during Qt event loop (app.exec): {e}"); logging.exception(e)
        if controller and hasattr(controller, 'hotkey_listener'): controller.hotkey_listener.stop()
        exit_code = 1
    logging.info(f"{APP_NAME} exiting with code {exit_code}."); sys.exit(exit_code)

# --- Global Exception Hook ---
def handle_exception(exc_type, exc_value, exc_traceback):
    # ... (No changes needed here) ...
    tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback); tb_string = "".join(tb_lines); timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    error_message = f"--- CRITICAL UNHANDLED ERROR ({timestamp}) ---\n{tb_string}--- END CRITICAL ERROR ---"; print(error_message, file=sys.stderr); sys.stderr.flush()
    if LOGGING_INITIALIZED: logging.critical(error_message)
    else:
        try:
            fallback_log = BASE_DIR / "buttonwheel_CRITICAL_ERROR.log"
            try:
                with open(fallback_log, "a", encoding="utf-8") as f_err: f_err.write(f"{error_message}\n")
            except Exception as file_err: print(f"ERROR: Could not write to fallback log file {fallback_log}: {file_err}", file=sys.stderr)
        except Exception as outer_e: print(f"ERROR: Could not attempt fallback logging: {outer_e}", file=sys.stderr)
    msg_handler = None
    try:
         global controller # Access the controller instance created in main()
         if 'controller' in globals() and controller and hasattr(controller, 'action_handler'): msg_handler = controller.action_handler
         elif QApplication.instance(): msg_handler = ActionHandler() # Fallback
    except Exception as handler_find_err: print(f"ERROR: Could not get ActionHandler for error message: {handler_find_err}", file=sys.stderr)
    if msg_handler:
        try: QTimer.singleShot(100, lambda: msg_handler.show_error("Critical Error", f"An unhandled error occurred:\n{exc_value}\n\nCheck logs/console for details."))
        except Exception as msg_e: print(f"ERROR: Failed to show critical error message box: {msg_e}", file=sys.stderr)
    if sys.stdin.isatty(): input("Unhandled error occurred. Press Enter to exit...")


# --- Entry Point ---
if __name__ == "__main__":
    sys.excepthook = handle_exception
    controller = None # Define globally for exception hook access
    try:
        main()
    except SystemExit as se:
         logging.info(f"SystemExit called with code {se.code}")
         raise # Re-raise to allow proper exit
    except Exception as main_err:
        # Log the error that occurred *before* the main event loop
        logging.critical(f"Error during main() execution before event loop: {main_err}")
        # The exception hook will likely have already run, but call it again just in case.
        # This might result in duplicate output for early errors, but ensures logging/display.
        handle_exception(type(main_err), main_err, main_err.__traceback__)
        sys.exit(1) # Exit with error code if main fails early
