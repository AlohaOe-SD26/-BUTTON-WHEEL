import os
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image
import threading

# Hide console window on Windows
if os.name == 'nt':
    try:
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass  # Fallback silently if it doesn't work

class MediaConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Format Converter")
        self.root.geometry("600x520")
        self.root.resizable(False, False)
        
        # Try to set app icon (creates blank icon if file doesn't exist)
        try:
            self.root.iconbitmap(default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "converter.ico"))
        except:
            pass
        
        # Available image formats
        self.image_formats = {
            "WEBP": "WEBP",
            "PNG": "PNG",
            "JPEG": "JPEG",
            "GIF": "GIF",
            "BMP": "BMP",
            "TIFF": "TIFF"
        }
        
        # Available video formats
        self.video_formats = {
            "MP4": "MP4",
            "AVI": "AVI",
            "MKV": "MKV",
            "MOV": "MOV",
            "WEBM": "WEBM",
            "GIF": "GIF"  # Animated GIF
        }
        
        # Default formats
        self.selected_image_format = tk.StringVar(value="WEBP")
        self.selected_video_format = tk.StringVar(value="MP4")
        
        # Recursive processing toggles
        self.image_recursive_var = tk.BooleanVar(value=False)
        self.video_recursive_var = tk.BooleanVar(value=False)
        
        # Folder paths
        self.image_folder_var = tk.StringVar()
        self.video_folder_var = tk.StringVar()
        
        # Current conversion state
        self.is_converting = False
        
        # Set up the UI elements
        self.setup_ui()
        
        # Check for dependencies when starting
        self.check_dependencies()
    
    def setup_ui(self):
        # Create menu
        self.setup_menu()
        
        # Create tabbed interface
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.image_tab = ttk.Frame(self.notebook)
        self.video_tab = ttk.Frame(self.notebook)
        
        # Add tabs to notebook
        self.notebook.add(self.image_tab, text="Image Converter")
        self.notebook.add(self.video_tab, text="Video Converter")
        
        # Set up each tab
        self.setup_image_tab()
        self.setup_video_tab()
        
        # Add a status bar at bottom
        self.status_frame = tk.Frame(self.root)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10)
        
        self.status_var = tk.StringVar(value="Ready")
        status_label = tk.Label(self.status_frame, textvariable=self.status_var, 
                               font=("Helvetica", 8), anchor=tk.W)
        status_label.pack(side=tk.LEFT, padx=5, pady=2)
        
        # Credits
        credits_label = tk.Label(self.status_frame, text="Created with Python", 
                                font=("Helvetica", 8), anchor=tk.E)
        credits_label.pack(side=tk.RIGHT, padx=5, pady=2)
    
    def setup_menu(self):
        """Set up the application menu."""
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Check Dependencies", command=self.check_dependencies)
        
        if getattr(sys, 'frozen', False):
            # Running as executable
            help_menu.add_command(label="Create Desktop Shortcut", command=self.create_shortcut)
    
    def setup_image_tab(self):
        """Set up the image conversion tab."""
        # Title
        title_label = tk.Label(self.image_tab, text="Image Format Converter", font=("Helvetica", 14, "bold"))
        title_label.pack(pady=10)
        
        # Folder selection frame
        folder_frame = tk.Frame(self.image_tab)
        folder_frame.pack(pady=5, fill=tk.X, padx=20)
        
        folder_label = tk.Label(folder_frame, text="Image Folder:")
        folder_label.pack(anchor=tk.W)
        
        folder_select_frame = tk.Frame(folder_frame)
        folder_select_frame.pack(fill=tk.X, pady=5)
        
        folder_entry = tk.Entry(folder_select_frame, textvariable=self.image_folder_var, width=50)
        folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        browse_btn = tk.Button(folder_select_frame, text="Browse", 
                              command=lambda: self.browse_folder(self.image_folder_var))
        browse_btn.pack(side=tk.RIGHT, padx=5)
        
        # Recursive option
        recursive_frame = tk.Frame(self.image_tab)
        recursive_frame.pack(pady=5, fill=tk.X, padx=20)
        
        recursive_cb = ttk.Checkbutton(recursive_frame, text="Process subfolders (recursive)", 
                                     variable=self.image_recursive_var)
        recursive_cb.pack(anchor=tk.W)
        
        recursive_info = tk.Label(recursive_frame, 
                               text="When enabled, processes images in all subfolders\nand creates '[FolderName] - [Format]' folders in each location",
                               font=("Helvetica", 8), fg="gray")
        recursive_info.pack(anchor=tk.W, padx=20)
        
        # Format selection frame
        format_frame = tk.Frame(self.image_tab)
        format_frame.pack(pady=10, fill=tk.X, padx=20)
        
        format_label = tk.Label(format_frame, text="Output Format:", font=("Helvetica", 10, "bold"))
        format_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Create a frame for the format toggles arranged in a grid
        toggle_frame = tk.Frame(format_frame)
        toggle_frame.pack(fill=tk.X, pady=5)
        
        # Add radio buttons for each format in a 3x2 grid
        row, col = 0, 0
        for format_key, format_name in self.image_formats.items():
            radio_btn = tk.Radiobutton(
                toggle_frame, 
                text=format_name, 
                variable=self.selected_image_format,
                value=format_key,
                font=("Helvetica", 10),
                padx=10
            )
            radio_btn.grid(row=row, column=col, sticky=tk.W, pady=2)
            col += 1
            if col > 2:  # 3 columns (0, 1, 2)
                col = 0
                row += 1
        
        # Progress bar
        self.image_progress_frame = tk.Frame(self.image_tab)
        self.image_progress_frame.pack(pady=10, fill=tk.X, padx=20)
        
        self.image_progress_var = tk.DoubleVar()
        self.image_progress_bar = ttk.Progressbar(self.image_progress_frame, variable=self.image_progress_var, maximum=100)
        self.image_progress_bar.pack(fill=tk.X)
        
        # Status label
        self.image_status_var = tk.StringVar()
        self.image_status_var.set("Ready to convert")
        image_status_label = tk.Label(self.image_tab, textvariable=self.image_status_var, font=("Helvetica", 9, "italic"))
        image_status_label.pack(pady=5)
        
        # Convert button
        self.image_convert_btn = tk.Button(
            self.image_tab, 
            text="Convert Images", 
            command=self.start_image_conversion, 
            height=2, 
            width=15, 
            bg="#4CAF50", 
            fg="white", 
            font=("Helvetica", 10, "bold")
        )
        self.image_convert_btn.pack(pady=10)
        
        # Preview of naming convention
        self.image_preview_var = tk.StringVar()
        self.image_preview_var.set("Output example: image - WEBP.webp")
        preview_label = tk.Label(self.image_tab, textvariable=self.image_preview_var, font=("Helvetica", 9))
        preview_label.pack(pady=5)
        
        # Update preview when format changes
        self.selected_image_format.trace_add("write", self.update_image_preview)
    
    def setup_video_tab(self):
        """Set up the video conversion tab."""
        # Title
        title_label = tk.Label(self.video_tab, text="Video Format Converter", font=("Helvetica", 14, "bold"))
        title_label.pack(pady=10)
        
        # Folder selection frame
        folder_frame = tk.Frame(self.video_tab)
        folder_frame.pack(pady=5, fill=tk.X, padx=20)
        
        folder_label = tk.Label(folder_frame, text="Video Folder:")
        folder_label.pack(anchor=tk.W)
        
        folder_select_frame = tk.Frame(folder_frame)
        folder_select_frame.pack(fill=tk.X, pady=5)
        
        folder_entry = tk.Entry(folder_select_frame, textvariable=self.video_folder_var, width=50)
        folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        browse_btn = tk.Button(folder_select_frame, text="Browse", 
                              command=lambda: self.browse_folder(self.video_folder_var))
        browse_btn.pack(side=tk.RIGHT, padx=5)
        
        # Recursive option
        recursive_frame = tk.Frame(self.video_tab)
        recursive_frame.pack(pady=5, fill=tk.X, padx=20)
        
        recursive_cb = ttk.Checkbutton(recursive_frame, text="Process subfolders (recursive)", 
                                     variable=self.video_recursive_var)
        recursive_cb.pack(anchor=tk.W)
        
        recursive_info = tk.Label(recursive_frame, 
                               text="When enabled, processes videos in all subfolders\nand creates '[FolderName] - [Format]' folders in each location",
                               font=("Helvetica", 8), fg="gray")
        recursive_info.pack(anchor=tk.W, padx=20)
        
        # Format selection frame
        format_frame = tk.Frame(self.video_tab)
        format_frame.pack(pady=10, fill=tk.X, padx=20)
        
        format_label = tk.Label(format_frame, text="Output Format:", font=("Helvetica", 10, "bold"))
        format_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Create a frame for the format toggles arranged in a grid
        toggle_frame = tk.Frame(format_frame)
        toggle_frame.pack(fill=tk.X, pady=5)
        
        # Add radio buttons for each format in a 3x2 grid
        row, col = 0, 0
        for format_key, format_name in self.video_formats.items():
            radio_btn = tk.Radiobutton(
                toggle_frame, 
                text=format_name, 
                variable=self.selected_video_format,
                value=format_key,
                font=("Helvetica", 10),
                padx=10
            )
            radio_btn.grid(row=row, column=col, sticky=tk.W, pady=2)
            col += 1
            if col > 2:  # 3 columns (0, 1, 2)
                col = 0
                row += 1
        
        # Video quality options
        quality_frame = tk.Frame(self.video_tab)
        quality_frame.pack(pady=5, fill=tk.X, padx=20)
        
        quality_label = tk.Label(quality_frame, text="Video Quality:", font=("Helvetica", 10, "bold"))
        quality_label.pack(anchor=tk.W)
        
        self.video_quality_var = tk.StringVar(value="medium")
        
        quality_opts = tk.Frame(quality_frame)
        quality_opts.pack(fill=tk.X, pady=5)
        
        qualities = [("Low", "low"), ("Medium", "medium"), ("High", "high")]
        
        for i, (text, value) in enumerate(qualities):
            rb = tk.Radiobutton(
                quality_opts,
                text=text,
                variable=self.video_quality_var,
                value=value,
                font=("Helvetica", 10),
                padx=10
            )
            rb.grid(row=0, column=i, sticky=tk.W)
        
        # Progress bar
        self.video_progress_frame = tk.Frame(self.video_tab)
        self.video_progress_frame.pack(pady=10, fill=tk.X, padx=20)
        
        self.video_progress_var = tk.DoubleVar()
        self.video_progress_bar = ttk.Progressbar(self.video_progress_frame, variable=self.video_progress_var, maximum=100)
        self.video_progress_bar.pack(fill=tk.X)
        
        # Status label
        self.video_status_var = tk.StringVar()
        self.video_status_var.set("Ready to convert")
        video_status_label = tk.Label(self.video_tab, textvariable=self.video_status_var, font=("Helvetica", 9, "italic"))
        video_status_label.pack(pady=5)
        
        # Convert button
        self.video_convert_btn = tk.Button(
            self.video_tab, 
            text="Convert Videos", 
            command=self.start_video_conversion, 
            height=2, 
            width=15, 
            bg="#4CAF50", 
            fg="white", 
            font=("Helvetica", 10, "bold")
        )
        self.video_convert_btn.pack(pady=10)
        
        # Preview of naming convention
        self.video_preview_var = tk.StringVar()
        self.video_preview_var.set("Output example: video - MP4.mp4")
        preview_label = tk.Label(self.video_tab, textvariable=self.video_preview_var, font=("Helvetica", 9))
        preview_label.pack(pady=5)
        
        # Update preview when format changes
        self.selected_video_format.trace_add("write", self.update_video_preview)
        
        # Dependency warning label
        self.video_dependency_warning = tk.Label(
            self.video_tab,
            text="Note: FFmpeg is required for video conversion. Click 'Check Dependencies' in the Help menu.",
            font=("Helvetica", 8, "italic"),
            fg="red"
        )
        self.video_dependency_warning.pack(pady=5)
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About Media Format Converter", 
            "Media Format Converter\n\n"
            "A simple tool to convert images and videos between different formats.\n\n"
            "Created with Python, Pillow and FFmpeg."
        )
    
    def create_shortcut(self):
        """Create desktop shortcut for the executable"""
        if os.name == 'nt' and getattr(sys, 'frozen', False):
            try:
                import win32com.client
                
                # Get paths
                desktop = os.path.join(os.path.expanduser("~"), "Desktop")
                executable_path = sys.executable
                
                # Create shortcut
                shell = win32com.client.Dispatch("WScript.Shell")
                shortcut = shell.CreateShortCut(os.path.join(desktop, "Media Converter.lnk"))
                shortcut.Targetpath = executable_path
                shortcut.WorkingDirectory = os.path.dirname(executable_path)
                shortcut.IconLocation = executable_path
                shortcut.save()
                
                messagebox.showinfo("Shortcut Created", "Desktop shortcut created successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create shortcut: {str(e)}")
    
    def update_image_preview(self, *args):
        """Update the image filename preview based on selected format"""
        format_key = self.selected_image_format.get()
        file_ext = format_key.lower()
        self.image_preview_var.set(f"Output example: image - {format_key}.{file_ext}")
    
    def update_video_preview(self, *args):
        """Update the video filename preview based on selected format"""
        format_key = self.selected_video_format.get()
        file_ext = format_key.lower()
        self.video_preview_var.set(f"Output example: video - {format_key}.{file_ext}")
    
    def check_dependencies(self):
        """Check and install required dependencies."""
        self.status_var.set("Checking dependencies...")
        self.root.update()
        
        # Image dependencies
        has_pillow = self.check_pillow()
        
        # Video dependencies
        has_ffmpeg = self.check_ffmpeg()
        
        if has_pillow and has_ffmpeg:
            self.video_dependency_warning.config(text="FFmpeg detected. Video conversion is ready to use.", fg="green")
            self.status_var.set("All dependencies installed. Ready to use.")
        elif has_pillow:
            self.video_dependency_warning.config(
                text="FFmpeg not found. Video conversion unavailable. See Help > Check Dependencies.", 
                fg="red"
            )
            self.status_var.set("Pillow installed. FFmpeg missing for video conversion.")
        else:
            self.status_var.set("Missing dependencies. See Help > Check Dependencies.")
    
    def check_pillow(self):
        """Check if Pillow is installed and install if needed."""
        try:
            __import__("PIL")
            return True
        except ImportError:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
                return True
            except subprocess.CalledProcessError:
                messagebox.showerror(
                    "Missing Dependency", 
                    "Pillow is required for image conversion but could not be installed.\n"
                    "Please install it manually: pip install pillow"
                )
                return False
    
    def check_ffmpeg(self):
        """Check if FFmpeg is installed and available."""
        try:
            # Try to find ffmpeg in system path
            if os.name == 'nt':  # Windows
                ffmpeg_present = subprocess.call(['where', 'ffmpeg'], 
                                              stdout=subprocess.DEVNULL, 
                                              stderr=subprocess.DEVNULL) == 0
            else:  # Unix-like
                ffmpeg_present = subprocess.call(['which', 'ffmpeg'], 
                                               stdout=subprocess.DEVNULL, 
                                               stderr=subprocess.DEVNULL) == 0
            
            if not ffmpeg_present:
                messagebox.showinfo(
                    "FFmpeg Required", 
                    "FFmpeg is required for video conversion.\n\n"
                    "Please install FFmpeg:\n"
                    "- Windows: Download from https://ffmpeg.org/download.html\n"
                    "- Mac: Use Homebrew: brew install ffmpeg\n"
                    "- Linux: Use your package manager: apt install ffmpeg\n\n"
                    "After installing, restart this application."
                )
                return False
            return True
        except Exception:
            messagebox.showinfo(
                "FFmpeg Required", 
                "FFmpeg is required for video conversion.\n\n"
                "Please install FFmpeg:\n"
                "- Windows: Download from https://ffmpeg.org/download.html\n"
                "- Mac: Use Homebrew: brew install ffmpeg\n"
                "- Linux: Use your package manager: apt install ffmpeg\n\n"
                "After installing, restart this application."
            )
            return False
    
    def browse_folder(self, folder_var):
        """Open dialog to select a folder and update the relevant variable."""
        folder_path = filedialog.askdirectory(title="Select Folder")
        if folder_path:
            folder_var.set(folder_path)
    
    def start_image_conversion(self):
        """Start the image conversion process."""
        if self.is_converting:
            messagebox.showinfo("Process Running", "A conversion process is already running. Please wait.")
            return
        
        folder_path = self.image_folder_var.get()
        if not folder_path:
            messagebox.showwarning("Warning", "Please select a folder first.")
            return
        
        # Set conversion state
        self.is_converting = True
        
        # Disable tab switching
        self.notebook.tab(1, state="disabled")  # Disable video tab
        
        # Disable the convert button
        self.image_convert_btn.config(state=tk.DISABLED)
        
        # Start conversion in a separate thread
        conversion_thread = threading.Thread(target=self.convert_images, args=(folder_path,))
        conversion_thread.daemon = True
        conversion_thread.start()
    
    def start_video_conversion(self):
        """Start the video conversion process."""
        if self.is_converting:
            messagebox.showinfo("Process Running", "A conversion process is already running. Please wait.")
            return
        
        folder_path = self.video_folder_var.get()
        if not folder_path:
            messagebox.showwarning("Warning", "Please select a folder first.")
            return
        
        # Check FFmpeg
        if not self.check_ffmpeg():
            return
        
        # Set conversion state
        self.is_converting = True
        
        # Disable tab switching
        self.notebook.tab(0, state="disabled")  # Disable image tab
        
        # Disable the convert button
        self.video_convert_btn.config(state=tk.DISABLED)
        
        # Start conversion in a separate thread
        conversion_thread = threading.Thread(target=self.convert_videos, args=(folder_path,))
        conversion_thread.daemon = True
        conversion_thread.start()
    
    def find_media_files(self, root_folder, extensions, recursive=False):
        """Find all media files with given extensions in the folder and optionally in subfolders.
        
        Returns a dictionary where:
        - Keys are folder paths
        - Values are lists of media files in that folder
        """
        result = {}
        
        def has_extension(filename):
            return os.path.splitext(filename.lower())[1] in extensions
        
        if recursive:
            # Set a counter to prevent infinite recursion
            folder_count = 0
            max_folders = 10000
            
            # Walk through directory tree
            for folder_path, _, files in os.walk(root_folder):
                folder_count += 1
                if folder_count > max_folders:
                    messagebox.showwarning("Warning", f"Reached maximum folder count ({max_folders}). Some folders may be skipped.")
                    break
                
                # Filter for media files in this folder
                media_files = [f for f in files if has_extension(f)]
                if media_files:
                    result[folder_path] = media_files
        else:
            # Just process the root folder
            try:
                files = [f for f in os.listdir(root_folder) if os.path.isfile(os.path.join(root_folder, f))]
                media_files = [f for f in files if has_extension(f)]
                if media_files:
                    result[root_folder] = media_files
            except Exception as e:
                messagebox.showerror("Error", f"Could not read folder: {str(e)}")
        
        return result
    
    def convert_images(self, root_folder):
        """Convert images in the selected folder and optionally subfolders."""
        try:
            # Get selected format
            output_format = self.selected_image_format.get()
            output_ext = output_format.lower()
            is_recursive = self.image_recursive_var.get()
            
            # Find all image files
            image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.gif', '.webp']
            folder_image_map = self.find_media_files(root_folder, image_extensions, recursive=is_recursive)
            
            if not folder_image_map:
                self.image_status_var.set("No images found")
                messagebox.showinfo("Info", "No images found in the selected folder" + 
                                   (" and subfolders" if is_recursive else ""))
                return
            
            # Calculate total images to process
            total_images = sum(len(files) for files in folder_image_map.values())
            successful_conversions = 0
            failed_conversions = []
            processed_count = 0
            
            # Process each folder and its images
            for folder_path, image_files in folder_image_map.items():
                # Get the parent folder name
                parent_folder_name = os.path.basename(folder_path)
                
                # Create the output folder name using both parent folder name and format
                output_folder_name = f"{parent_folder_name} - {output_format}"
                
                # Create the output folder if it doesn't exist
                output_folder = os.path.join(folder_path, output_folder_name)
                os.makedirs(output_folder, exist_ok=True)
                
                # Process each image in this folder
                for file in image_files:
                    try:
                        # Update UI
                        processed_count += 1
                        progress_percent = (processed_count / total_images) * 100
                        self.image_progress_var.set(progress_percent)
                        self.image_status_var.set(f"Converting: {file} ({processed_count}/{total_images})")
                        self.root.update_idletasks()
                        
                        # Extract filename and extension
                        file_path = os.path.join(folder_path, file)
                        filename, _ = os.path.splitext(file)
                        
                        # Open the image
                        img = Image.open(file_path)
                        
                        # Convert to RGB if saving as JPEG (doesn't support RGBA)
                        if output_format == "JPEG" and img.mode in ("RGBA", "LA"):
                            # Create white background
                            background = Image.new("RGB", img.size, (255, 255, 255))
                            background.paste(img, mask=img.split()[3] if img.mode == "RGBA" else img.split()[1])
                            img = background
                        
                        # Create output path with format added
                        output_path = os.path.join(output_folder, f"{filename} - {output_format}.{output_ext}")
                        
                        # Save with the selected format
                        if output_format == "JPEG":
                            img.save(output_path, output_format, quality=90)
                        else:
                            img.save(output_path, output_format)
                        
                        successful_conversions += 1
                        
                    except Exception as e:
                        relative_path = os.path.relpath(os.path.join(folder_path, file), root_folder)
                        failed_conversions.append(relative_path)
                        print(f"Error converting {file}: {str(e)}")
                        continue
            
            # Update UI after completion
            self.image_progress_var.set(100)
            self.image_status_var.set(f"Conversion complete: {successful_conversions}/{total_images} images converted")
            
            # Show completion message
            mode_text = "recursive" if is_recursive else "standard"
            message = f"Successfully converted {successful_conversions} out of {total_images} images to {output_format} format using {mode_text} mode."
            
            if is_recursive:
                folder_count = len(folder_image_map)
                message += f"\n\nProcessed {folder_count} folders with images."
            else:
                root_folder_name = os.path.basename(root_folder)
                output_folder_name = f"{root_folder_name} - {output_format}"
                message += f"\n\nThe converted images are saved in:\n{os.path.join(root_folder, output_folder_name)}"
            
            if failed_conversions:
                if len(failed_conversions) <= 5:
                    failed_list = "\n".join(failed_conversions)
                    message += f"\n\nFailed to convert {len(failed_conversions)} images:\n{failed_list}"
                else:
                    message += f"\n\nFailed to convert {len(failed_conversions)} images."
            
            messagebox.showinfo("Conversion Complete", message)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during conversion: {str(e)}")
        
        finally:
            # Always ensure we reset state and enable controls
            self.is_converting = False
            self.image_convert_btn.config(state=tk.NORMAL)
            self.notebook.tab(1, state="normal")  # Re-enable video tab
    
    def convert_videos(self, root_folder):
        """Convert videos in the selected folder and optionally subfolders."""
        try:
            # Get selected format
            output_format = self.selected_video_format.get()
            output_ext = output_format.lower()
            is_recursive = self.video_recursive_var.get()
            quality = self.video_quality_var.get()
            
            # Find all video files
            video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v', '.3gp']
            folder_video_map = self.find_media_files(root_folder, video_extensions, recursive=is_recursive)
            
            if not folder_video_map:
                self.video_status_var.set("No videos found")
                messagebox.showinfo("Info", "No videos found in the selected folder" + 
                                   (" and subfolders" if is_recursive else ""))
                return
            
            # Quality settings for FFmpeg
            quality_settings = {
                'low': {'crf': '28', 'preset': 'fast'},
                'medium': {'crf': '23', 'preset': 'medium'},
                'high': {'crf': '18', 'preset': 'slow'}
            }[quality]
            
            # Calculate total videos to process
            total_videos = sum(len(files) for files in folder_video_map.values())
            successful_conversions = 0
            failed_conversions = []
            processed_count = 0
            
            # Process each folder and its videos
            for folder_path, video_files in folder_video_map.items():
                # Get the parent folder name
                parent_folder_name = os.path.basename(folder_path)
                
                # Create the output folder name using both parent folder name and format
                output_folder_name = f"{parent_folder_name} - {output_format}"
                
                # Create the output folder if it doesn't exist
                output_folder = os.path.join(folder_path, output_folder_name)
                os.makedirs(output_folder, exist_ok=True)
                
                # Process each video in this folder
                for file in video_files:
                    try:
                        # Update UI
                        processed_count += 1
                        self.video_status_var.set(f"Converting: {file} ({processed_count}/{total_videos})")
                        self.root.update_idletasks()
                        
                        # Extract filename and extension
                        file_path = os.path.join(folder_path, file)
                        filename, _ = os.path.splitext(file)
                        
                        # Create output path with format added
                        output_path = os.path.join(output_folder, f"{filename} - {output_format}.{output_ext}")
                        
                        # Run FFmpeg conversion
                        # Command varies based on output format
                        if output_format == "GIF":
                            # Generate palette for high-quality GIF
                            palette_path = os.path.join(output_folder, f"{filename}_palette.png")
                            
                            # Create palette
                            palette_cmd = [
                                'ffmpeg', '-i', file_path, '-vf', 
                                'fps=10,scale=320:-1:flags=lanczos,palettegen', 
                                palette_path
                            ]
                            
                            subprocess.run(palette_cmd, check=True, 
                                         stdout=subprocess.DEVNULL, 
                                         stderr=subprocess.DEVNULL)
                            
                            # Create GIF using palette
                            cmd = [
                                'ffmpeg', '-i', file_path, '-i', palette_path, 
                                '-filter_complex', 'fps=10,scale=320:-1:flags=lanczos[x];[x][1:v]paletteuse', 
                                '-y', output_path
                            ]
                        else:
                            # Standard video conversion
                            cmd = [
                                'ffmpeg', '-i', file_path,
                                '-c:v', 'libx264' if output_format != 'WEBM' else 'libvpx-vp9',
                                '-crf', quality_settings['crf'],
                                '-preset', quality_settings['preset'],
                                '-c:a', 'aac' if output_format != 'WEBM' else 'libopus',
                                '-y', output_path
                            ]
                        
                        # Run the conversion
                        process = subprocess.Popen(
                            cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            universal_newlines=True
                        )
                        
                        # Monitor progress
                        duration_seconds = None
                        
                        for line in process.stdout:
                            # Look for duration info in the output
                            if "Duration:" in line and duration_seconds is None:
                                time_parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
                                duration_seconds = float(time_parts[0]) * 3600 + float(time_parts[1]) * 60 + float(time_parts[2])
                            
                            # Look for progress info
                            if "time=" in line and duration_seconds:
                                time_parts = line.split("time=")[1].split(" ")[0].strip().split(":")
                                current_seconds = float(time_parts[0]) * 3600 + float(time_parts[1]) * 60 + float(time_parts[2])
                                progress = (current_seconds / duration_seconds) * 100
                                
                                # Update individual file progress
                                self.video_progress_var.set(progress)
                                self.root.update_idletasks()
                        
                        # Wait for process to complete
                        process.wait()
                        
                        # Check if conversion was successful
                        if process.returncode == 0:
                            successful_conversions += 1
                            
                            # Clean up palette file if created
                            if output_format == "GIF" and os.path.exists(palette_path):
                                os.remove(palette_path)
                        else:
                            relative_path = os.path.relpath(file_path, root_folder)
                            failed_conversions.append(relative_path)
                            
                        # Update overall progress
                        overall_progress = (processed_count / total_videos) * 100
                        self.video_progress_var.set(overall_progress)
                        
                    except Exception as e:
                        relative_path = os.path.relpath(os.path.join(folder_path, file), root_folder)
                        failed_conversions.append(relative_path)
                        print(f"Error converting {file}: {str(e)}")
                        continue
            
            # Update UI after completion
            self.video_progress_var.set(100)
            self.video_status_var.set(f"Conversion complete: {successful_conversions}/{total_videos} videos converted")
            
            # Show completion message
            mode_text = "recursive" if is_recursive else "standard"
            message = f"Successfully converted {successful_conversions} out of {total_videos} videos to {output_format} format using {mode_text} mode."
            
            if is_recursive:
                folder_count = len(folder_video_map)
                message += f"\n\nProcessed {folder_count} folders with videos."
            else:
                root_folder_name = os.path.basename(root_folder)
                output_folder_name = f"{root_folder_name} - {output_format}"
                message += f"\n\nThe converted videos are saved in:\n{os.path.join(root_folder, output_folder_name)}"
            
            if failed_conversions:
                if len(failed_conversions) <= 5:
                    failed_list = "\n".join(failed_conversions)
                    message += f"\n\nFailed to convert {len(failed_conversions)} videos:\n{failed_list}"
                else:
                    message += f"\n\nFailed to convert {len(failed_conversions)} videos."
            
            messagebox.showinfo("Conversion Complete", message)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during video conversion: {str(e)}")
        
        finally:
            # Always ensure we reset state and enable controls
            self.is_converting = False
            self.video_convert_btn.config(state=tk.NORMAL)
            self.notebook.tab(0, state="normal")  # Re-enable image tab

# Create a .pyw version if running as .py
def create_pyw_version():
    """Create a .pyw version of this script"""
    if sys.argv[0].endswith('.py') and os.name == 'nt':
        try:
            # Get the current script path
            script_path = os.path.abspath(sys.argv[0])
            pyw_path = script_path.replace('.py', '.pyw')
            
            # If .pyw doesn't exist, create it
            if not os.path.exists(pyw_path):
                with open(script_path, 'r') as src_file:
                    content = src_file.read()
                
                with open(pyw_path, 'w') as pyw_file:
                    pyw_file.write(content)
                
                print(f"\nCreated windowless version: {os.path.basename(pyw_path)}")
                print("Use this file instead to run without showing the console window.")
        except:
            pass  # Silently fail if can't create .pyw

if __name__ == "__main__":
    # Create a .pyw version for future use (only needed once)
    create_pyw_version()
    
    # Start the application
    root = tk.Tk()
    app = MediaConverter(root)
    root.mainloop()
