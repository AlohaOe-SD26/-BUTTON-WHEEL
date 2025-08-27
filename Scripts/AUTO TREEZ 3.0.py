import sys
import os
import subprocess
from pathlib import Path
import json
from datetime import datetime
import time
import traceback
import threading
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random

# --- Constants and Configuration (Standard Libraries Only) ---
APP_NAME = "Treez Auditor Bot"
APP_DATA_DIR_NAME = "TreezAutomatorData"
VENV_DIR_NAME = "venv"
CONFIG_JSON_FILENAME = "config.json"
SETUP_FLAG_FILENAME = "setup.complete"
SESSION_ID_LOG_FILENAME = "session_ids.txt"

SCRIPT_DIR = Path(__file__).resolve().parent
APP_DATA_PATH = SCRIPT_DIR / APP_DATA_DIR_NAME
VENV_PATH = APP_DATA_PATH / VENV_DIR_NAME
CONFIG_JSON_FILE_PATH = APP_DATA_PATH / CONFIG_JSON_FILENAME
# CORRECTED LINE: Fixed the typo from SETUP_FLAG_FILE_FILE_PATH to SETUP_FLAG_FILE_PATH
SETUP_FLAG_FILE_PATH = APP_DATA_PATH / SETUP_FLAG_FILENAME
SESSION_ID_LOG_FILE_PATH = APP_DATA_PATH / SESSION_ID_LOG_FILENAME

# Google Sheet Configuration
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1DA1FjHQfK0a_1zpeRZh5GKpMTL6zRCyletGi5nsB33I"
GOOGLE_CREDENTIALS_FILENAME = "google_credentials.json"
GOOGLE_CREDENTIALS_PATH = APP_DATA_PATH / GOOGLE_CREDENTIALS_FILENAME

# --- Helper to get platform-specific venv paths (Standard Libraries Only) ---
def get_venv_python_pip_paths(venv_root):
    if not isinstance(venv_root, Path): venv_root = Path(venv_root)
    if os.name == 'nt':
        python_exe = venv_root / "Scripts" / "python.exe"
        pip_exe = venv_root / "Scripts" / "pip.exe"
    else:
        python_exe = venv_root / "bin" / "python"
        pip_exe = venv_root / "bin" / "pip"
    return python_exe, pip_exe

# --- Setup and Config Managers (Standard Libraries Only) ---
class SetupManager:
    def __init__(self, logger_callback=None):
        self.log = logger_callback or print

    def check_and_perform_setup(self):
        self.log("Verifying environment...")
        if SETUP_FLAG_FILE_PATH.exists():
            venv_python_exe, _ = get_venv_python_pip_paths(VENV_PATH)
            if venv_python_exe.exists():
                self.log("Setup flag found and venv executable exists. Assuming environment is OK.")
                return True
            else:
                self.log("ERROR: Setup flag exists, but venv Python executable is missing! Forcing re-run of setup.")
                SETUP_FLAG_FILE_PATH.unlink(missing_ok=True)
                # Clean up incomplete venv directory if present
                if VENV_PATH.exists():
                    self.log(f"Cleaning up incomplete venv directory: {VENV_PATH}")
                    try:
                        import shutil
                        shutil.rmtree(VENV_PATH)
                    except Exception as e:
                        self.log(f"WARN: Could not remove old venv directory: {e}")

        self.log("Starting first-time setup process...")
        try:
            APP_DATA_PATH.mkdir(parents=True, exist_ok=True)
            
            current_python_executable = str(sys.executable)
            self.log(f"Using system Python executable: {current_python_executable}")
            
            if not VENV_PATH.exists():
                self.log(f"Creating Python virtual environment at: {VENV_PATH}")
                try:
                    result = subprocess.run(
                        [current_python_executable, "-m", "venv", str(VENV_PATH)],
                        check=True,
                        capture_output=True,
                        text=True,
                        timeout=300
                    )
                    self.log(f"Venv creation stdout:\n{result.stdout}")
                    if result.stderr:
                        self.log(f"Venv creation stderr:\n{result.stderr}")
                except subprocess.CalledProcessError as e:
                    self.log(f"ERROR: Venv creation failed with exit code {e.returncode}")
                    self.log(f"Stdout: {e.stdout}")
                    self.log(f"Stderr: {e.stderr}")
                    return False
                except subprocess.TimeoutExpired:
                    self.log("ERROR: Venv creation timed out after 300 seconds.")
                    return False
                except Exception as e:
                    self.log(f"ERROR: An unexpected error occurred during venv creation: {e}")
                    return False

            python_exe, pip_exe = get_venv_python_pip_paths(VENV_PATH)
            if not python_exe.exists():
                self.log(f"ERROR: venv Python executable not found after creation: {python_exe}. Check permissions or Python installation.")
                return False
            if not pip_exe.exists():
                self.log(f"ERROR: venv Pip executable not found after creation: {pip_exe}. Check permissions or Python installation.")
                return False

            packages_to_install = ["playwright", "pandas", "openpyxl", "pygetwindow", "gspread", "oauth2client"]
            self.log(f"Installing required packages: {', '.join(packages_to_install)}")
            try:
                result = subprocess.run(
                    [str(pip_exe), "install", "--upgrade"] + packages_to_install,
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=600
                )
                self.log(f"Package installation stdout:\n{result.stdout}")
                if result.stderr:
                    self.log(f"Package installation stderr:\n{result.stderr}")
            except subprocess.CalledProcessError as e:
                self.log(f"ERROR: Package installation failed with exit code {e.returncode}")
                self.log(f"Stdout: {e.stdout}")
                self.log(f"Stderr: {e.stderr}")
                return False
            except subprocess.TimeoutExpired:
                self.log("ERROR: Package installation timed out after 600 seconds.")
                return False
            except Exception as e:
                self.log(f"ERROR: An unexpected error occurred during package installation: {e}")
                return False

            self.log("Installing Playwright browser dependencies...")
            try:
                result = subprocess.run(
                    [str(python_exe), "-m", "playwright", "install"],
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=900
                )
                self.log(f"Playwright install stdout:\n{result.stdout}")
                if result.stderr:
                    self.log(f"Playwright install stderr:\n{result.stderr}")
            except subprocess.CalledProcessError as e:
                self.log(f"ERROR: Playwright browser installation failed with exit code {e.returncode}")
                self.log(f"Stdout: {e.stdout}")
                self.log(f"Stderr: {e.stderr}")
                return False
            except subprocess.TimeoutExpired:
                self.log("ERROR: Playwright browser installation timed out after 900 seconds.")
                return False
            except Exception as e:
                self.log(f"ERROR: An unexpected error occurred during Playwright installation: {e}")
                return False

            ConfigManager(self.log).create_default_config_if_not_exists()
            SETUP_FLAG_FILE_PATH.touch()
            self.log("Setup complete! Please configure login details in 'config.json' and restart.")
            self.log(f"Also, if using Google Sheets, place '{GOOGLE_CREDENTIALS_FILENAME}' in '{APP_DATA_PATH}'")
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, Exception) as e:
            self.log(f"CRITICAL ERROR during setup: {type(e).__name__} - {e}")
            if hasattr(e, 'stdout') and e.stdout: self.log(f"Stdout: {e.stdout}")
            if hasattr(e, 'stderr') and e.stderr: self.log(f"Stderr: {e.stderr}")
            self.log(traceback.format_exc())
            return False

class ConfigManager:
    def __init__(self, logger_callback=None):
        self.log = logger_callback or print

    def create_default_config_if_not_exists(self):
        if not CONFIG_JSON_FILE_PATH.exists():
            self.log(f"Creating template {CONFIG_JSON_FILENAME}")
            template_data = {"username": "your_email@example.com", "password": "your_password"}
            try:
                with CONFIG_JSON_FILE_PATH.open("w") as f:
                    json.dump(template_data, f, indent=2)
            except IOError as e:
                self.log(f"ERROR writing template config: {e}")

    def load_config(self):
        if not CONFIG_JSON_FILE_PATH.exists():
            self.log(f"{CONFIG_JSON_FILENAME} not found. Creating default.")
            self.create_default_config_if_not_exists()
            return None
        try:
            with CONFIG_JSON_FILE_PATH.open("r") as f:
                config_data = json.load(f)
            if not all(k in config_data for k in ["username", "password"]) or not config_data["username"] or not config_data["password"]:
                raise ValueError("Config missing 'username' or 'password', or values are empty.")
            return config_data
        except (json.JSONDecodeError, ValueError, IOError) as e:
            self.log(f"ERROR loading/parsing {CONFIG_JSON_FILENAME}: {e}")
            return None

def start_application():
    import pandas as pd
    import pygetwindow
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials

    class GoogleSheetManager:
        def __init__(self, logger_callback=None):
            self.log = logger_callback or print
            self.gc = None

        def authenticate(self):
            try:
                if not GOOGLE_CREDENTIALS_PATH.exists():
                    self.log(f"ERROR: Google credentials file not found at {GOOGLE_CREDENTIALS_PATH}. Please create one.")
                    self.log("Refer to gspread documentation for service account setup.")
                    return False

                scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
                creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS_PATH, scope)
                self.gc = gspread.authorize(creds)
                self.log("Successfully authenticated with Google Sheets.")
                return True
            except Exception as e:
                self.log(f"ERROR during Google Sheets authentication: {e}")
                self.log(traceback.format_exc())
                return False

        def get_worksheet_titles(self, spreadsheet_url):
            if not self.gc:
                self.log("Google Sheets not authenticated. Cannot fetch titles.")
                return []
            try:
                self.log(f"Attempting to open Google Sheet at URL: {spreadsheet_url}")
                spreadsheet = self.gc.open_by_url(spreadsheet_url)
                titles = [ws.title for ws in spreadsheet.worksheets()]
                self.log(f"Found tabs: {', '.join(titles)}")
                return titles
            except gspread.exceptions.SpreadsheetNotFound:
                self.log(f"ERROR: Spreadsheet not found at URL: {spreadsheet_url}. Please ensure the URL is correct and the service account has access.")
                self.log(traceback.format_exc())
                return []
            except Exception as e:
                self.log(f"ERROR fetching worksheet titles: {e}")
                self.log(traceback.format_exc())
                return []

        def get_worksheet_data(self, spreadsheet_url, worksheet_title):
            if not self.gc:
                self.log("Google Sheets not authenticated. Cannot fetch data.")
                return []
            try:
                spreadsheet = self.gc.open_by_url(spreadsheet_url)
                worksheet = spreadsheet.worksheet(worksheet_title)
                data = worksheet.get_all_values()
                self.log(f"Successfully retrieved {len(data)} rows from '{worksheet_title}'.")
                return data
            except gspread.exceptions.WorksheetNotFound:
                self.log(f"ERROR: Worksheet '{worksheet_title}' not found in the spreadsheet.")
                self.log(traceback.format_exc())
                return []
            except Exception as e:
                self.log(f"ERROR fetching worksheet data: {e}")
                self.log(traceback.format_exc())
                return []

    class TreezAuditorBot:
        def __init__(self, config, gui_callbacks, screen_size, settings):
            self.username = config["username"]
            self.password = config["password"]
            self.gui_add_log = gui_callbacks["add_log"]
            self.gui_update_status = gui_callbacks["update_status"]
            self.gui_update_progress = gui_callbacks["update_progress"]
            self.screen_width = screen_size['width']
            self.screen_height = screen_size['height']
            self.settings = settings
            self.playwright = None
            self.browser = None
            self.context = None
            self.page = None
            self.running_event = threading.Event()
            self.stores = {"H80": "h80d", "FSD": "fstreet"}
            self.session_id = None
            self.gs_manager = GoogleSheetManager(self._log)

        def _log(self, message): self.gui_add_log(f"[{datetime.now().strftime('%I:%M:%S %p')} Bot] {message}")
        def _status(self, message): self.gui_update_status(message)

        def _generate_session_id(self):
            day_initials = ['M', 'T', 'W', 'H', 'F', 'S', 'U']
            day_of_week = datetime.now().weekday()
            day_initial = day_initials[day_of_week]
            used_ids = set()
            if SESSION_ID_LOG_FILE_PATH.exists():
                with SESSION_ID_LOG_FILE_PATH.open("r") as f:
                    used_ids = set(line.strip() for line in f)
            while True:
                random_nums = ''.join(random.choices('0123456789', k=3))
                new_id = f"{day_initial}{random_nums}"
                if new_id not in used_ids:
                    with SESSION_ID_LOG_FILE_PATH.open("a") as f:
                        f.write(new_id + "\n")
                    self.session_id = new_id
                    self._log(f"Generated new Session ID: {self.session_id}")
                    return

        def _navigate_to(self, url, page_name):
            self._status(f"Navigating to {page_name}...")
            self._log(f"Attempting to navigate to {page_name}: {url}")
            try:
                response = self.page.goto(url, timeout=90000, wait_until="domcontentloaded")
                if not response:
                    self._log(f"WARN: Navigation to {page_name} did not return a response.")
                    return False
                if response.status >= 400:
                    self._log(f"ERROR: Received HTTP status {response.status} for {page_name}.")
                    return False
                self._log(f"Successfully loaded page with URL: {self.page.url}")
                return True
            except PlaywrightTimeoutError:
                self._log(f"ERROR: Timeout after 90s while navigating to {page_name}.")
                return False
            except Exception as e:
                self._log(f"ERROR: An unexpected error occurred during navigation to {page_name}: {e}")
                return False

        def _login(self, store_url_fragment):
            """
            Attempts to log into the Treez portal for the given store fragment.
            This function is designed to be robust, always attempting login if on the login page,
            and verifying a successful redirect.
            Returns True if successfully logged in and on an expected post-login page, False otherwise.
            """
            self._log(f"Attempting login for {store_url_fragment.upper()}...")
            login_url = f"https://{store_url_fragment}.treez.io/portalDispensary/portal/login"
            
            # Step 1: Always navigate to the login page first
            if not self._navigate_to(login_url, f"{store_url_fragment.upper()} Login Page"):
                self._log(f"CRITICAL: Failed to load login page for {store_url_fragment.upper()}. Cannot proceed with login.")
                return False

            # Step 2: Check if we are currently on the login page URL
            # Only attempt to fill credentials and sign in if we are actually on the login page URL
            if "portalDispensary/portal/login" in self.page.url:
                self._log("Currently on the login page URL. Attempting to fill credentials and sign in.")
                try:
                    # Use more robust get_by_ methods and explicit waits
                    email_field = self.page.get_by_label("Email")
                    password_field = self.page.get_by_role("textbox", name="Password")
                    sign_in_button = self.page.get_by_test_id("sign-in-button")

                    # Wait for elements to be visible and enabled before interacting
                    email_field.wait_for(state='visible', timeout=15000)
                    password_field.wait_for(state='visible', timeout=15000)
                    sign_in_button.wait_for(state='visible', timeout=15000)

                    email_field.fill(self.username, timeout=30000)
                    self._log("Filled username.")
                    password_field.fill(self.password, timeout=30000)
                    self._log("Filled password.")
                    self._log("Clicking Sign In button...")
                    
                    # Expect navigation away from the login page after clicking sign-in
                    with self.page.expect_navigation(url=lambda url: "portal/login" not in url, timeout=60000):
                        sign_in_button.click(timeout=30000)
                    
                    self._log(f"Sign In clicked and navigation awaited. Current URL: {self.page.url}")

                except PlaywrightTimeoutError as e:
                    self._log(f"ERROR: Timeout during login process (e.g., fields not found, navigation failed): {e}")
                    self._log(traceback.format_exc())
                    return False
                except Exception as e:
                    self._log(f"ERROR: An unexpected error occurred during login interaction: {e}")
                    self._log(traceback.format_exc())
                    return False
            else:
                self._log("Not on the login page URL. Assuming session is active or already redirected.")

            # Step 3: Verify final URL to confirm successful login
            final_url_success = False
            for url_part in ["portalDispensary/portal/DiscountManagement", "portalDispensary/portal/ProductManagement", "portalDispensary/portal/Dashboard"]:
                if url_part in self.page.url:
                    final_url_success = True
                    break
            
            if final_url_success:
                self._log(f"Login successful. Landed on a recognized portal page. Current URL: {self.page.url}")
                return True
            else:
                self._log(f"Login failed: Did not land on a recognized post-login page after attempt. Current URL: {self.page.url}")
                # Check for common error messages on the page if login truly failed
                if self.page.locator('text=Invalid email or password').is_visible() or \
                   self.page.locator('text=Login failed').is_visible() or \
                   self.page.locator('text=Authentication Failed').is_visible():
                    self._log("Detected potential login error message on page (e.g., 'Invalid email/password').")
                return False


        def _wait_for_dynamic_list_to_load(self, item_selector, page_name):
            self._status(f"Waiting for {page_name} to fully load...")
            self._log(f"Verifying list items with selector: '{item_selector}'")
            try:
                self.page.wait_for_selector(item_selector, timeout=60000)
                self._log("Initial items detected. Starting dynamic load check.")
            except PlaywrightTimeoutError:
                self._log(f"Warning: No items found for '{page_name}' with selector '{item_selector}' after 60s.")
                return 0
            last_count, stable_checks = -1, 0
            while self.running_event.is_set():
                current_count = self.page.locator(item_selector).count()
                if current_count > 0 and current_count == last_count:
                    stable_checks += 1
                    if stable_checks >= 2:
                        self._log(f"Item count ({current_count}) is stable. {page_name} page has loaded.")
                        return current_count
                else:
                    stable_checks = 0
                last_count = current_count
                self._log(f"Page is still loading... Found {current_count} items. Waiting 3s...")
                time.sleep(3)
            return last_count
        
        def _save_to_excel(self, data, store_key, report_type):
            if not data:
                self._log(f"No data was scraped for {store_key} {report_type}, so no file will be saved.")
                return
            date_str = datetime.now().strftime("%Y-%m-%d")
            filename = f"{store_key} {report_type} List_{date_str} - {self.session_id}.xlsx"
            self._status(f"Saving data to {filename}...")
            try:
                if report_type == "Product Groups":
                    df = pd.DataFrame(data, columns=["Product Group Name", "Sync Toggle State", "Product Group Category", "Product Group Full HTML Code Structure"])
                else:
                    discount_columns = [
                        "Discount Name", "Discount Activity Toggle State", "Discount Type",
                        "Discount Title - Management", "Stacking",
                        "BIN 1 Product Group - Title", "BIN 1 - Value", 
                        "BIN 2 Product Group - Title", "BIN 2 - Value",
                        "Discount Value - Type", "Discount Value - Value",
                        "Fulfillment Types", "Start Date", "Start Time", "End Date", "End Time", "Recurrence"
                    ]
                    for row in data:
                        for col in discount_columns:
                            row.setdefault(col, "N/A")
                    df = pd.DataFrame(data, columns=discount_columns)
                df.to_excel(filename, index=False)
                self._log(f"Successfully saved {len(data)} rows to '{filename}'.")
            except Exception as e:
                self._log(f"ERROR saving Excel file '{filename}': {e}")
                self._status(f"Error saving {filename}")

        def _close_discount_popup_window(self):
            """
            Clicks a calculated off-element position (100 pixels below center of 'Sandwich' button)
            to close a popup using a double-click.
            Includes retry logic: if the popup container is not hidden after 3s, retry the click.
            """
            self._log("Attempting to close popup using Sandwich button reference with retry logic...")
            max_retries = 3 # Maximum number of attempts to close the popup
            # The general popup container to wait for it to become hidden
            popup_container_selector = 'div.animated.edit-pane.slide-in'
            # Locator for the sandwich button (options button)
            sandwich_button_locator = self.page.locator('i.material-icons:has-text("menu")')

            for attempt in range(1, max_retries + 1):
                try:
                    self._log(f"Closing attempt {attempt} of {max_retries}.")
                    
                    # 1. Get the bounding box of the sandwich button
                    self._log("Waiting for Sandwich button to be visible and getting its coordinates...")
                    sandwich_button_locator.wait_for(state='visible', timeout=15000)
                    box = sandwich_button_locator.bounding_box()
                    
                    if not box:
                        self._log("ERROR: Sandwich button bounding box not found. Cannot calculate click point.")
                        raise Exception("Sandwich button not found for popup close reference.")

                    # Calculate click coordinates: 100 pixels below the center
                    click_x = box['x'] + box['width'] / 2
                    click_y = box['y'] + box['height'] / 2 + 100
                    
                    self._log(f"Calculated click coordinates: x={click_x}, y={click_y}")

                    # Perform the double-click at the calculated coordinates on the body
                    self.page.dblclick('body', position={'x': click_x, 'y': click_y}, timeout=5000)

                    # 2. Confirm popup is hidden (using the popup's actual HTML element)
                    self._log("Waiting for popup (div.animated.edit-pane.slide-in) to be hidden (max 1 seconds)...")
                    self.page.wait_for_selector(popup_container_selector, state='hidden', timeout=1000)
                    
                    self._log("Discount popup successfully closed and confirmed hidden.")
                    time.sleep(0.5) # Small buffer after successful close
                    return # Exit function on success

                except PlaywrightTimeoutError:
                    self._log(f"WARN: Attempt {attempt} - Popup container '{popup_container_selector}' did not hide after 3 seconds. Retrying...")
                    # Continue to the next iteration of the loop for a retry
                except Exception as e:
                    self._log(f"ERROR: Could not close discount popup on attempt {attempt}: {e}")
                    self._log(traceback.format_exc())
                    if attempt == max_retries: # If this is the last attempt, re-raise the error
                        raise Exception(f"Failed to close discount popup after {max_retries} attempts due to an unexpected error.")
            
            # If the loop finishes without returning, it means all retries failed
            self._log(f"CRITICAL: Failed to close discount popup after {max_retries} attempts. Popup might still be open.")
            raise Exception(f"Failed to close discount popup after {max_retries} attempts.")


        def _click_new_discount_button(self):
            """Clicks the 'NEW DISCOUNT BUTTON' (yellow button)"""
            self._log("Clicking 'NEW DISCOUNT BUTTON'...")
            try:
                self.page.click('div.yellow-plus.unselectable', timeout=30000)
                self._log("'NEW DISCOUNT BUTTON' clicked.")
                self.page.wait_for_selector('div.animated.edit-pane.slide-in', state='visible', timeout=30000)
                self._log("Discount creation popup appeared.")
                time.sleep(1)
            except PlaywrightTimeoutError:
                self._log("ERROR: Timeout waiting for 'NEW DISCOUNT BUTTON' or discount creation popup.")
                raise Exception("Failed to open new discount creation popup.")
            except Exception as e:
                self._log(f"ERROR clicking 'NEW DISCOUNT BUTTON': {e}")
                raise

        def _enter_discount_title(self, title_value):
            """Enters the discount title into the 'DISCOUNT TITLE TEXT FIELD'."""
            self._log(f"Entering Discount Title: '{title_value}'")
            try:
                # Locator for the input field
                discount_title_field = self.page.locator('input[id*="DISCOUNTTITLE"]')
                # Explicitly wait for the field to be visible before filling
                self._log("Waiting for Discount Title field to be visible...")
                discount_title_field.wait_for(state='visible', timeout=15000)
                discount_title_field.fill(title_value, timeout=30000)
                self._log("Discount Title entered.")
            except PlaywrightTimeoutError:
                self._log(f"ERROR: Timeout waiting for 'DISCOUNT TITLE TEXT FIELD' to be visible.")
                raise Exception(f"Failed to enter discount title: {title_value}")
            except Exception as e:
                self.log(f"ERROR entering discount title: {e}")
                raise

        def _select_discount_method(self, method_name):
            """Activates 'DISCOUNT METHOD SELECT' and selects the specified method."""
            self._log(f"Selecting Discount Method: '{method_name}'")
            try:
                # Wait for the button to be visible/enabled before clicking
                discount_method_selector_button = self.page.locator('label:has-text("DISCOUNT METHOD") + div button')
                self._log("Waiting for Discount Method dropdown button to be visible...")
                discount_method_selector_button.wait_for(state='visible', timeout=15000)
                discount_method_selector_button.click(timeout=15000) # Click to open dropdown
                self._log("Discount Method Select dropdown opened.")
                
                # Add a tiny delay to allow options to fully render
                time.sleep(0.2) # Small delay for UI rendering

                # Use get_by_text to locate the specific option and wait for it to be clickable
                # The method_name here will be the exact text from the dropdown (e.g., "BOGO", "Percent Discount")
                target_option = self.page.get_by_text(method_name, exact=True)
                self._log(f"Waiting for option '{method_name}' to be visible in dropdown...")
                target_option.wait_for(state='visible', timeout=15000) # Ensure the option is visible
                target_option.click(timeout=15000) # Click the target option
                self._log(f"Selected discount method: '{method_name}'.")
            except PlaywrightTimeoutError:
                self._log(f"ERROR: Timeout waiting to select discount method: '{method_name}'. The dropdown or option might not have appeared/been clickable.")
                raise Exception(f"Failed to select discount method: {method_name}")
            except Exception as e:
                self._log(f"ERROR selecting discount method: {e}")
                raise

        def _select_bogo_discount_value_type(self, value_type_name):
            """
            Activates the 'BOGO DISCOUNT - SELECT DISCOUNT VALUE TYPE' dropdown
            and selects the specified value type (e.g., '$ Off', '% Off', 'Price At').
            """
            self._log(f"Selecting BOGO Discount Value Type: '{value_type_name}'")
            try:
                # Locator for the dropdown button. It's inside a div with id containing "PercentOrDollar"
                # The button itself is a generic button with an SVG inside that div
                value_type_dropdown_button = self.page.locator('div[id*="PercentOrDollar"] button')
                self._log("Waiting for BOGO Discount Value Type dropdown button to be visible...")
                value_type_dropdown_button.wait_for(state='visible', timeout=15000)
                value_type_dropdown_button.click(timeout=15000)
                self._log("BOGO Discount Value Type dropdown opened.")

                # Add a tiny delay to allow options to fully render
                time.sleep(0.2)

                # Locate and click the specific option (e.g., "$ Off")
                target_value_type_option = self.page.get_by_text(value_type_name, exact=True)
                self._log(f"Waiting for BOGO option '{value_type_name}' to be visible in dropdown...")
                target_value_type_option.wait_for(state='visible', timeout=15000)
                target_value_type_option.click(timeout=15000)
                self._log(f"Selected BOGO Discount Value Type: '{value_type_name}'.")
            except PlaywrightTimeoutError:
                self._log(f"ERROR: Timeout waiting to select BOGO Discount Value Type: '{value_type_name}'.")
                raise Exception(f"Failed to select BOGO Discount Value Type: {value_type_name}")
            except Exception as e:
                self._log(f"ERROR selecting BOGO Discount Value Type: {e}")
                raise

        def _create_dollar_discount(self, deal_row, headers):
            self._log("Initiating Dollar Discount creation flow...")
            
            discount_title = deal_row[headers.index("DEAL TITLE")].strip()
            dollar_value = deal_row[headers.index("DISCOUNT VALUE")].strip()
            
            try:
                self._click_new_discount_button()
                self._enter_discount_title(discount_title)
                self._select_discount_method("Dollar Amount Discount") # Corrected text
                
                self._log(f"Entering Dollar Discount value: '{dollar_value}'")
                # Fix: Use a more specific locator for Dollar Off value input
                # Target the input that comes after the label containing "$ OFF"
                dollar_value_field = self.page.locator('label:has-text("$ OFF") + input[type="number"]')
                
                # Explicitly wait for the field to be visible before filling
                self._log("Waiting for Dollar Discount value field to be visible...")
                dollar_value_field.wait_for(state='visible', timeout=15000)
                dollar_value_field.fill(dollar_value, timeout=30000)
                self._log("Dollar Discount value entered.")
                
                self._close_discount_popup_window()
                self._log("Dollar Discount creation completed for this row.")
            except Exception as e:
                self._log(f"ERROR during Dollar Discount creation: {e}")
                raise


        def _create_percent_discount(self, deal_row, headers):
            self._log("Initiating Percent Discount creation flow...")
            
            discount_title = deal_row[headers.index("DEAL TITLE")].strip()
            percent_value = deal_row[headers.index("DISCOUNT VALUE")].strip()

            try:
                self._click_new_discount_button()
                self._enter_discount_title(discount_title)
                self._select_discount_method("Percent Discount") # Corrected text

                self._log(f"Entering Percent Discount value: '{percent_value}'")
                # Fix: Use a more specific locator for Percent Off value input
                # Target the input that comes after the label containing "% OFF"
                percent_value_field = self.page.locator('label:has-text("% OFF") + input[type="number"]')
                
                # Explicitly wait for the field to be visible before filling
                self._log("Waiting for Percent Discount value field to be visible...")
                percent_value_field.wait_for(state='visible', timeout=15000)
                percent_value_field.fill(percent_value, timeout=30000)
                self._log("Percent Discount value entered.")

                self._close_discount_popup_window()
                self._log("Percent Discount creation completed for this row.")
            except Exception as e:
                self._log(f"ERROR during Percent Discount creation: {e}")
                raise

        def _create_bogo_discount(self, deal_row, headers):
            self._log("Initiating BOGO Discount creation flow...")
            
            discount_title = deal_row[headers.index("DEAL TITLE")].strip()
            bin1_value = deal_row[headers.index("BIN 1")].strip()
            bin2_value = deal_row[headers.index("BIN 2")].strip()
            # Assuming "DISCOUNT VALUE" column from sheet also holds the value for BOGO's $ Off / % Off
            bogo_discount_value = deal_row[headers.index("DISCOUNT VALUE")].strip()

            try:
                self._click_new_discount_button()
                self._enter_discount_title(discount_title)
                self._select_discount_method("BOGO") # Corrected text
                
                self._log(f"Entering BIN 1 value: '{bin1_value}'")
                # Locator for the input field: uses id containing "REQUIREDBUYCOUNT"
                bin1_value_field = self.page.locator('input[id*="REQUIREDBUYCOUNT"]')
                # Explicitly wait for the field to be visible before filling
                self._log("Waiting for BIN 1 value field to be visible...")
                bin1_value_field.wait_for(state='visible', timeout=15000)
                bin1_value_field.fill(bin1_value, timeout=30000)
                self._log("BIN 1 value entered.")

                self._log(f"Entering BIN 2 value: '{bin2_value}'")
                # Locator for the input field: uses id containing "CUSTOMEREARNSNUMBER"
                bin2_value_field = self.page.locator('input[id*="CUSTOMEREARNSNUMBER"]')
                # Explicitly wait for the field to be visible before filling
                self._log("Waiting for BIN 2 value field to be visible...")
                bin2_value_field.wait_for(state='visible', timeout=15000)
                bin2_value_field.fill(bin2_value, timeout=30000)
                self._log("BIN 2 value entered.")

                # NEW: Select BOGO Discount Value Type and enter value
                # This calls a new helper function to manage the specific BOGO value type dropdown
                self._select_bogo_discount_value_type("$ Off") # As requested by user for this part
                
                self._log(f"Entering BOGO Discount Value: '{bogo_discount_value}'")
                # Locator for the input field where BOGO discount value (e.g., 10 for $10 Off) is entered
                bogo_discount_amount_field = self.page.locator('input[id*="DiscountAmount"]')
                self._log("Waiting for BOGO Discount Amount field to be visible...")
                bogo_discount_amount_field.wait_for(state='visible', timeout=15000)
                bogo_discount_amount_field.fill(bogo_discount_value, timeout=30000)
                self._log("BOGO Discount Amount entered.")
                
                self._close_discount_popup_window()
                self._log("BOGO Discount creation completed for this row.")
            except Exception as e:
                self._log(f"ERROR during BOGO Discount creation: {e}")
                raise

        def run_discount_creation(self):
            self.running_event.set()
            try:
                if not self.gs_manager.authenticate():
                    self._status("Google Sheets authentication failed. Aborting.")
                    messagebox.showerror("Error", "Failed to authenticate with Google Sheets. Check credentials.")
                    return

                self._log("Launching browser...")
                self.playwright = sync_playwright().start()
                self.browser = self.playwright.chromium.launch(headless=False)
                browser_width = self.screen_width // 2
                self.context = self.browser.new_context(viewport={'width': browser_width, 'height': self.screen_height})
                self.page = self.context.new_page()
                self.page.goto("about:blank")
                self._log("Browser launched. Attempting to auto-position window...")

                try:
                    time.sleep(1) 
                    browser_window = None
                    all_windows = pygetwindow.getAllWindows()
                    for window in all_windows:
                        if "chromium" in window.title.lower() or "chrome" in window.title.lower():
                            browser_window = window
                            break
                    if browser_window:
                        x_pos = self.screen_width // 2
                        browser_window.moveTo(x_pos, 0)
                        browser_window.resizeTo(browser_width, self.screen_height - 50)
                        self._log("Browser window positioned successfully.")
                    else:
                        self._log("Could not find browser window to position. Please drag it manually.")
                except Exception as e:
                    self._log(f"Could not auto-position browser: {e}. Please drag it manually.")

                self._generate_session_id()
                total_stores = len(self.stores)
                
                selected_tabs = {
                    "H80": self.settings["H80"]["selected_tab"],
                    "FSD": self.settings["FSD"]["selected_tab"]
                }

                for store_idx, (store_key, store_fragment) in enumerate(self.stores.items()):
                    if not self.running_event.is_set(): break
                    
                    selected_tab_for_store = selected_tabs[store_key]
                    if not selected_tab_for_store or selected_tab_for_store == "Select a tab":
                        self._log(f"Skipping {store_key}: No tab selected for discount creation.")
                        self.gui_update_progress(store_idx + 1, total_stores)
                        continue

                    self.gui_update_progress(store_idx, total_stores)
                    self._log(f"--- Starting discount creation for store: {store_key} using tab: '{selected_tab_for_store}' ---")
                    
                    # Ensure login for the current store before processing its deals
                    self._log(f"Ensuring login for {store_key}...")
                    login_successful = self._login(store_fragment)
                    
                    if not login_successful:
                        # User's defined "bot detection page" is the login page itself when login fails.
                        # We check if we are still on the login page URL after the failed attempt.
                        current_url = self.page.url
                        expected_login_url_part = f"{store_fragment}.treez.io/portalDispensary/portal/login"

                        if expected_login_url_part in current_url:
                            self._log(f"ALERT: Login failed for {store_key} AND bot appears stuck on login page ({current_url}). Attempting bypass to Discounts page.")
                            discounts_url = f"https://{store_fragment}.treez.io/portalDispensary/portal/DiscountManagement/Discounts"
                            # Force navigate to the discounts page directly
                            if self._navigate_to(discounts_url, f"[{store_key}] Bot Detection Bypass to Discounts Page"):
                                self._log(f"Bypass successful for {store_key}. Landed on: {self.page.url}")
                                # If bypass succeeded, treat as if login was successful for this step
                                login_successful = True
                            else:
                                self._log(f"CRITICAL: Bypass failed for {store_key}. Still stuck or navigation failed. Skipping this store.")
                                messagebox.showerror("Login/Bypass Failed", f"Failed to log in or bypass detection for {store_key}. Check credentials, network, or if Treez portal is accessible.")
                                self.gui_update_progress(store_idx + 1, total_stores)
                                continue # Skip to the next store
                        else:
                            # Login failed for another reason (e.g., landed on unexpected page not login)
                            self._log(f"CRITICAL: Login failed for {store_key} (not on login page URL after attempt). Skipping discount creation for this store. Current URL: {current_url}")
                            messagebox.showerror("Login Failed", f"Failed to log in to {store_key}. Please check credentials in config.json and try again.")
                            self.gui_update_progress(store_idx + 1, total_stores)
                            continue # Skip to the next store if login failed

                    # ONLY if login (or bypass) was successful, proceed to ensure we are on the Discounts page
                    if login_successful:
                        self._log(f"Ensuring bot is on Discounts page for {store_key}...")
                        discounts_url = f"https://{store_fragment}.treez.io/portalDispensary/portal/DiscountManagement/Discounts"
                        if not self._navigate_to(discounts_url, f"[{store_key}] Final Navigation to Discounts Page"):
                            self._log(f"CRITICAL: Failed to navigate to Discounts page for {store_key} after login/bypass. Skipping discount creation for this store.")
                            messagebox.showerror("Navigation Failed", f"Failed to navigate to the Discounts page for {store_key}. Check internet connection or Treez portal status.")
                            self.gui_update_progress(store_idx + 1, total_stores)
                            continue # Skip to the next store if navigation to discounts page fails
                    else:
                        # This 'else' catches cases where bypass also failed, or general login_successful was False
                        self._log(f"CRITICAL: Skipping discount creation for {store_key} as login (or bypass) was not successful.")
                        self.gui_update_progress(store_idx + 1, total_stores)
                        continue

                    self._log(f"Retrieving discount data from Google Sheet tab: '{selected_tab_for_store}' for {store_key}")
                    discount_data_rows = self.gs_manager.get_worksheet_data(GOOGLE_SHEET_URL, selected_tab_for_store)

                    if not discount_data_rows or len(discount_data_rows) <= 1:
                        self._log(f"No valid discount data found in tab '{selected_tab_for_store}' for {store_key}. Skipping.")
                        self.gui_update_progress(store_idx + 1, total_stores)
                        continue
                    
                    headers = [h.strip() for h in discount_data_rows[0]]
                    deals_to_create = discount_data_rows[1:]

                    self._log(f"Found {len(deals_to_create)} deals to process for {store_key} from tab '{selected_tab_for_store}'.")
                    
                    self._log(f"Starting discount creation process for {store_key}...")
                    for deal_idx, deal_row in enumerate(deals_to_create):
                        if not self.running_event.is_set(): break
                        self._status(f"[{store_key}] Creating discount {deal_idx+1} of {len(deals_to_create)}")
                        
                        # --- START OF MAIN TRY BLOCK FOR EACH DEAL ROW ---
                        try:
                            if not deal_row or not deal_row[0].strip():
                                self._log(f"  > Skipping empty or invalid row {deal_idx+2} in sheet (no DEAL TYPE).")
                                continue

                            deal_type_raw = deal_row[headers.index("DEAL TYPE")].strip()

                            # Check for "END" signal - highest priority
                            if deal_type_raw.upper() == "END":
                                self._log(f"  > Detected 'END' in Column A for {store_key}. Stopping discount creation for this store and moving to the next.")
                                break # Exit the inner loop (deals for current store)

                            self._log(f"  > Processing deal (Raw Type: '{deal_type_raw}') from row {deal_idx+2} (Sheet Row {deal_idx+2})")
                            self._log(f"    Deal Data: {deal_row}")

                            is_numeric_deal = False
                            # This internal try-except handles the float conversion specifically.
                            try:
                                # Attempt to convert to float to check if it's a number (for numeric BOGO, e.g., '3' for '3 for 2')
                                numeric_check = float(deal_type_raw)
                                if numeric_check.is_integer(): # Treat integers as numeric BOGO
                                    is_numeric_deal = True
                            except ValueError:
                                pass # Not a number, continue to string comparisons

                            if is_numeric_deal:
                                self._log(f"      -> Detected numeric deal '{deal_type_raw}'. Calling BOGO creation logic.")
                                self._create_bogo_discount(deal_row, headers)
                            elif "BOGO" in deal_type_raw.upper() or \
                                 "B2G1" in deal_type_raw.upper() or \
                                 "B1G2" in deal_type_raw.upper():
                                self._log(f"      -> Detected BOGO-type deal ('{deal_type_raw}'). Calling BOGO creation logic.")
                                self._create_bogo_discount(deal_row, headers)
                            elif "% OFF" in deal_type_raw.upper():
                                self._log("      -> Detected Percent Discount. Calling creation logic.")
                                self._create_percent_discount(deal_row, headers)
                            elif "$ OFF" in deal_type_raw.upper():
                                self._log("      -> Detected Dollar Discount. Calling creation logic.")
                                self._create_dollar_discount(deal_row, headers)
                            else:
                                self._log(f"      -> Unknown discount type: '{deal_type_raw}'. Skipping this row.")
                                messagebox.showwarning("Unknown Discount Type", f"Skipping row {deal_idx+2} for {store_key}: Unknown discount type '{deal_type_raw}'.")
                                    
                            time.sleep(1)

                        except ValueError as ve: # Catches errors related to data extraction (e.g., missing column)
                            self._log(f"ERROR: Missing expected column for row {deal_idx+2}: {ve}")
                            messagebox.showerror("Data Error", f"Missing data for row {deal_idx+2} in {selected_tab_for_store}: {ve}")
                        except Exception as row_e: # Catches any other unexpected errors during row processing
                            self._log(f"ERROR processing row {deal_idx+2} for {store_key}: {row_e}")
                            self._log(traceback.format_exc())
                            messagebox.showerror("Automation Error", f"Failed to process row {deal_idx+2} for {store_key}: {row_e}")
                        # --- END OF MAIN TRY BLOCK FOR EACH DEAL ROW ---
                            
                    self._log(f"Finished processing all deals for {store_key}.")
                    self.gui_update_progress(store_idx + 1, total_stores)

                self._status("Discount Creation Complete.")
                messagebox.showinfo("Success", "The discount creation process has completed successfully.")
            except PlaywrightError as e:
                self._status("A critical browser error occurred.")
                self._log(f"FATAL PLAYWRIGHT ERROR: {e}\n{traceback.format_exc()}")
                messagebox.showerror("Critical Browser Error", f"The browser automation encountered a fatal fatal error: {e}")
            except Exception as e:
                self._status("An unexpected error occurred.")
                self._log(f"FATAL BOT ERROR: {e}\n{traceback.format_exc()}")
                messagebox.showerror("Fatal Application Error", f"An unexpected error occurred: {e}")
            finally:
                self.stop()

        def stop(self):
            self._log("Stop signal received by bot.")
            self.running_event.clear()
            # Safely close Playwright components
            if self.page and not self.page.is_closed():
                try:
                    self._log("Closing Playwright page...")
                    self.page.close()
                except Exception as e:
                    self._log(f"WARN: Error closing page: {e}")
            if self.context and not self.context.is_closed():
                try:
                    self._log("Closing Playwright context...")
                    self.context.close()
                except Exception as e:
                    self._log(f"WARN: Error closing context: {e}")
            if self.browser and not self.browser.is_closed():
                try:
                    self._log("Closing Playwright browser...")
                    self.browser.close()
                except Exception as e:
                    self._log(f"WARN: Error closing browser: {e}")
            if self.playwright:
                try:
                    self._log("Stopping Playwright instance...")
                    self.playwright.stop()
                except Exception as e:
                    self._log(f"WARN: Error stopping playwright instance: {e}")
            self._log("Bot cleanup complete.")


    class TreezAuditorApp:
        def __init__(self, root_window):
            self.root = root_window
            self.root.title(f"{APP_NAME} - Discount Creator v1.0")
            
            self.screen_width = self.root.winfo_screenwidth()
            self.screen_height = self.root.winfo_screenheight()
            gui_width = self.screen_width // 2
            self.root.geometry(f"{gui_width}x{self.screen_height - 50}+0+0")
            
            self.style = ttk.Style(self.root)
            self.style.theme_use('clam')
            self.is_bot_running_gui_state, self.bot_thread, self.bot_instance = False, None, None
            self.config_manager = ConfigManager(self.add_log_message_gui)
            self.config = self.config_manager.load_config()
            self.gs_manager = GoogleSheetManager(self.add_log_message_gui)
            self.google_sheet_tabs = []
            
            self._create_widgets()
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self._load_google_sheet_tabs()

        def _load_google_sheet_tabs(self):
            self.add_log_message_gui("[GUI] Attempting to load Google Sheet tabs...")
            if self.gs_manager.authenticate():
                self.google_sheet_tabs = []
                try:
                    self.add_log_message_gui(f"[GUI] Authenticated. Fetching tabs from URL: {GOOGLE_SHEET_URL}")
                    spreadsheet = self.gs_manager.gc.open_by_url(GOOGLE_SHEET_URL)
                    titles = [ws.title for ws in spreadsheet.worksheets()]
                    self.google_sheet_tabs = titles
                    if self.google_sheet_tabs:
                        self.google_sheet_tabs.insert(0, "Select a tab")
                        self.h80_tab_dropdown['values'] = self.google_sheet_tabs
                        self.fsd_tab_dropdown['values'] = self.google_sheet_tabs
                        self.h80_selected_tab.set("Select a tab")
                        self.fsd_selected_tab.set("Select a tab")
                        self.add_log_message_gui(f"[GUI] Successfully loaded tabs: {', '.join(titles)}")
                    else:
                        self.add_log_message_gui("WARN: No tabs found in the Google Sheet at the specified URL.")
                except gspread.exceptions.SpreadsheetNotFound:
                    self.add_log_message_gui(f"ERROR: Spreadsheet not found at URL: {GOOGLE_SHEET_URL}. Please ensure the URL is correct and the service account has access.")
                    self.add_log_message_gui(traceback.format_exc())
                except Exception as e:
                    self.add_log_message_gui(f"ERROR fetching worksheet titles: {e}")
                    self.add_log_message_gui(traceback.format_exc())
            else:
                self.add_log_message_gui("ERROR: Failed to authenticate with Google Sheets. Tab list will be empty.")


        def _create_widgets(self):
            main_frame = ttk.Frame(self.root, padding="10")
            main_frame.pack(expand=True, fill=tk.BOTH)
            main_frame.rowconfigure(2, weight=1) 
            main_frame.columnconfigure(0, weight=1)

            options_container = ttk.LabelFrame(main_frame, text="Discount Creation Options", padding="10")
            options_container.grid(row=0, column=0, sticky="ew", pady=(0, 10))
            options_container.columnconfigure(0, weight=1)
            options_container.columnconfigure(1, weight=1)

            dixon_frame = ttk.LabelFrame(options_container, text="Dixon (H80)", padding="5")
            dixon_frame.grid(row=0, column=0, sticky="nsew", padx=5)
            ttk.Label(dixon_frame, text="Select Tab:").pack(anchor="w")
            self.h80_selected_tab = tk.StringVar(value="Select a tab")
            self.h80_tab_dropdown = ttk.Combobox(dixon_frame, textvariable=self.h80_selected_tab, state="readonly")
            self.h80_tab_dropdown.pack(anchor="w", fill="x", pady=2)
            
            davis_frame = ttk.LabelFrame(options_container, text="Davis (FSD)", padding="5")
            davis_frame.grid(row=0, column=1, sticky="nsew", padx=5)
            ttk.Label(davis_frame, text="Select Tab:").pack(anchor="w")
            self.fsd_selected_tab = tk.StringVar(value="Select a tab")
            self.fsd_tab_dropdown = ttk.Combobox(davis_frame, textvariable=self.fsd_selected_tab, state="readonly")
            self.fsd_tab_dropdown.pack(anchor="w", fill="x", pady=2)


            controls_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
            controls_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
            controls_frame.columnconfigure(0, weight=1)
            self.start_button = ttk.Button(controls_frame, text="Start Discount Creation", command=self._toggle_audit)
            self.start_button.grid(row=0, column=0, ipady=5, sticky="ew")
            if not self.config or not self.config.get("username") or self.config.get("username") == "your_email@example.com":
                self.start_button.config(state="disabled")
                self.add_log_message_gui("[GUI] Please update config.json with your credentials before starting.")
            
            status_log_frame = ttk.Frame(main_frame)
            status_log_frame.grid(row=2, column=0, sticky="nsew", pady=(10, 0))
            status_log_frame.columnconfigure(0, weight=1)
            status_log_frame.rowconfigure(1, weight=1)
            status_frame = ttk.LabelFrame(status_log_frame, text="Status", padding="10")
            status_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
            status_frame.columnconfigure(1, weight=1)
            self.status_var = tk.StringVar(value="Idle. Ready to start discount creation.")
            ttk.Label(status_frame, text="Current Task:").grid(row=0, column=0, sticky="w")
            ttk.Label(status_frame, textvariable=self.status_var).grid(row=0, column=1, sticky="ew", padx=5)
            self.progress_bar = ttk.Progressbar(status_frame, orient='horizontal', mode='determinate')
            self.progress_bar.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(5,0))
            log_frame = ttk.LabelFrame(status_log_frame, text="Logs", padding="10")
            log_frame.grid(row=1, column=0, sticky="nsew")
            log_frame.rowconfigure(0, weight=1)
            log_frame.columnconfigure(0, weight=1)
            self.log_text_widget = scrolledtext.ScrolledText(log_frame, state=tk.DISABLED, wrap=tk.WORD, font=("Segoe UI", 9))
            self.log_text_widget.grid(row=0, column=0, sticky="nsew")

        def _toggle_audit(self):
            if self.is_bot_running_gui_state:
                self.add_log_message_gui("[GUI] Stop requested by user.")
                if self.bot_instance: self.bot_instance.stop()
                self.start_button.config(text="Stopping...", state="disabled")
            else:
                self.config = self.config_manager.load_config()
                if not self.config:
                    messagebox.showerror("Config Error", "Configuration is missing or invalid.")
                    return
                
                h80_tab = self.h80_selected_tab.get()
                fsd_tab = self.fsd_selected_tab.get()

                if h80_tab == "Select a tab" and fsd_tab == "Select a tab":
                    messagebox.showerror("Selection Error", "Please select at least one Google Sheet tab for Dixon or Davis.")
                    return

                self.add_log_message_gui("[GUI] Starting discount creation...")
                self.is_bot_running_gui_state = True
                self.start_button.config(text="Stop Discount Creation")
                
                settings = {
                    "FSD": {"selected_tab": fsd_tab},
                    "H80": {"selected_tab": h80_tab}
                }

                callbacks = {"add_log": self.add_log_message_gui, "update_status": self.update_status, "update_progress": self.update_progress}
                screen_size = {'width': self.screen_width, 'height': self.screen_height}
                self.bot_instance = TreezAuditorBot(self.config, callbacks, screen_size, settings)
                self.bot_thread = threading.Thread(target=self.bot_instance.run_discount_creation, daemon=True)
                self.bot_thread.start()
                self.root.after(100, self._check_bot_thread)
                
        def _check_bot_thread(self):
            if self.bot_thread and not self.bot_thread.is_alive():
                self.add_log_message_gui("[GUI] Bot thread finished or was stopped.")
                self.is_bot_running_gui_state = False
                self.start_button.config(text="Start Discount Creation", state="normal")
                self.update_progress(0, 1)
            elif self.is_bot_running_gui_state:
                self.root.after(500, self._check_bot_thread)

        def _safe_update_gui(self, update_func, *args):
            if self.root.winfo_exists(): self.root.after(0, lambda: update_func(*args))

        def add_log_message_gui(self, message):
            def _update():
                self.log_text_widget.config(state=tk.NORMAL)
                self.log_text_widget.insert(tk.END, f"{message}\n")
                self.log_text_widget.see(tk.END)
                self.log_text_widget.config(state=tk.DISABLED)
            self._safe_update_gui(_update)
            
        def update_status(self, text): self._safe_update_gui(self.status_var.set, text)
        def update_progress(self, current, total):
            def _update():
                self.progress_bar['maximum'] = total
                self.progress_bar['value'] = current
            self._safe_update_gui(_update)
            
        def on_closing(self):
            if self.is_bot_running_gui_state:
                if messagebox.askyesno(f"{APP_NAME}", "Discount creation is running. Are you sure you want to exit?"):
                    if self.bot_instance: self.bot_instance.stop()
                    if self.bot_thread: self.bot_thread.join(timeout=5)
                    self.root.destroy()
            else:
                if self.bot_instance: self.bot_instance.stop()
                self.root.destroy()

    root = tk.Tk()
    app = TreezAuditorApp(root)
    root.mainloop()

# --- Main Execution Block (Bootstrapper) ---
if __name__ == '__main__':
    launched_from_venv_arg = "--launched-from-venv"
    current_venv_python_exe, _ = get_venv_python_pip_paths(VENV_PATH)
    is_in_target_venv = (Path(sys.executable).resolve() == current_venv_python_exe.resolve())

    if not is_in_target_venv and launched_from_venv_arg not in sys.argv:
        print(f"[{datetime.now().strftime('%I:%M:%S %p')} Main] Initializing environment...")
        setup_mgr = SetupManager(print) 
        if not setup_mgr.check_and_perform_setup():
             print(f"[{datetime.now().strftime('%I:%M:%S %p')} Main] Setup failed. The program will now exit.")
             input("Press Enter to exit...")
             sys.exit(1)
        
        print(f"[{datetime.now().strftime('%I:%M:%S %p')} Main] Setup successful. Re-launching the application from the venv...")
        try:
            subprocess.Popen([str(current_venv_python_exe), __file__, launched_from_venv_arg] + sys.argv[1:], creationflags=subprocess.CREATE_NO_WINDOW)
            sys.exit(0)
        except Exception as e:
            print(f"[{datetime.now().strftime('%I:%M:%S %p')} Main] CRITICAL ERROR: Could not re-launch from venv: {e}")
            sys.exit(1)
    
    start_application()
