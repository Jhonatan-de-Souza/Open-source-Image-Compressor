"""
GUI for Open-source Image Compressor using CustomTkinter
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import time
import os
import subprocess
import pathlib
from .core import compress_single_image, get_estimated_size, format_file_size
from .config import (
    UI_TITLE, UI_WIDTH, UI_HEIGHT, APPEARANCE_MODE, COLOR_THEME,
    DEFAULT_COMPRESSION_LEVEL, MIN_COMPRESSION_LEVEL, MAX_COMPRESSION_LEVEL,
    FILE_DIALOG_TYPES, OUTPUT_DIR_NAME
)

ctk.set_appearance_mode(APPEARANCE_MODE)
ctk.set_default_color_theme(COLOR_THEME)


class ImageCompressorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(UI_TITLE)
        self.geometry(f"{UI_WIDTH}x520")
        self.resizable(False, False)

        self.selected_files = []
        self.compression_level = DEFAULT_COMPRESSION_LEVEL
        self.progress = 0
        self.estimated_time = "--"
        self.output_dir = self.get_desktop_path()  # Default to desktop
        self.custom_output_selected = False

        self.create_widgets()
        self.center_window()

    def get_desktop_path(self):
        """Get the desktop directory path"""
        return os.path.join(str(pathlib.Path.home()), "Desktop")

    def center_window(self):
        """Center the window on the screen"""
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - UI_WIDTH) // 2
        y = (screen_height - 520) // 2
        self.geometry(f"{UI_WIDTH}x520+{x}+{y}")

    def create_widgets(self):
        """Create all UI widgets"""
        self.label = ctk.CTkLabel(self, text="Select images for compression:")
        self.label.pack(pady=10)

        self.select_button = ctk.CTkButton(self, text="Select Images", command=self.select_files)
        self.select_button.pack(pady=5)

        # Status label for selected files
        self.selected_status_label = ctk.CTkLabel(self, text="No images selected", text_color="gray")
        self.selected_status_label.pack(pady=5)

        # Output folder selection
        output_folder_frame = ctk.CTkFrame(self)
        output_folder_frame.pack(pady=10, padx=20, fill="x")
        
        self.output_folder_button = ctk.CTkButton(output_folder_frame, text="📁 Set Output Folder", command=self.select_output_folder, width=150)
        self.output_folder_button.pack(side="left", padx=5)
        
        self.output_folder_label = ctk.CTkLabel(output_folder_frame, text=f"Default: Desktop", text_color="gray", wraplength=250, justify="left")
        self.output_folder_label.pack(side="left", padx=10, fill="x", expand=True)

        self.slider_label = ctk.CTkLabel(self, text="Compression Level (1=Min, 10=Max):")
        self.slider_label.pack(pady=5)
        self.slider = ctk.CTkSlider(
            self, 
            from_=MIN_COMPRESSION_LEVEL, 
            to=MAX_COMPRESSION_LEVEL, 
            number_of_steps=MAX_COMPRESSION_LEVEL - MIN_COMPRESSION_LEVEL,
            command=self.update_compression_level
        )
        self.slider.set(DEFAULT_COMPRESSION_LEVEL)
        self.slider.pack(pady=5)

        # Size estimation label
        self.size_estimate_label = ctk.CTkLabel(self, text="", text_color="#FFAA00", wraplength=500, justify="center")
        self.size_estimate_label.pack(pady=5)

        self.compress_button = ctk.CTkButton(self, text="Compress", command=self.start_compression)
        self.compress_button.pack(pady=10)

        self.progressbar = ctk.CTkProgressBar(self)
        self.progressbar.set(0)
        self.progressbar.pack(pady=10, fill="x", padx=40)

        self.status_label = ctk.CTkLabel(self, text="Progress: 0% | Estimated time: --")
        self.status_label.pack(pady=5)

        # Output location label (hidden by default)
        self.output_label = ctk.CTkLabel(self, text="", text_color="#00CC00", wraplength=500, justify="center")
        self.output_label.pack(pady=5)

        # Open folder button (hidden by default)
        self.open_folder_button = ctk.CTkButton(self, text="📂 Open Output Folder", command=self.open_output_folder, fg_color="gray", state="disabled")
        self.open_folder_button.pack(pady=5)

    def select_output_folder(self):
        """Let user select a custom output folder"""
        folder = filedialog.askdirectory(title="Select output folder for compressed images")
        if folder:
            self.output_dir = os.path.normpath(folder)
            self.custom_output_selected = True
            folder_name = os.path.basename(self.output_dir)
            self.output_folder_label.configure(text=f"Selected: {folder_name}", text_color="#00CC00")

    def select_files(self):
        """Open file dialog to select images"""
        files = filedialog.askopenfilenames(title="Select images", filetypes=FILE_DIALOG_TYPES)
        if files:
            self.selected_files = list(files)
            count = len(files)
            self.selected_status_label.configure(text=f"✓ {count} image(s) selected", text_color="#00CC00")
            
            # If user didn't select a custom output folder, use the first file's directory
            if not self.custom_output_selected:
                first_file_dir = os.path.dirname(files[0])
                self.output_dir = os.path.normpath(os.path.join(first_file_dir, OUTPUT_DIR_NAME))
            
            # Update size estimation
            self.update_size_estimate()

    def update_compression_level(self, value):
        """Update compression level from slider"""
        self.compression_level = int(value)
        # Update size estimation when compression level changes
        self.update_size_estimate()

    def update_size_estimate(self):
        """Update the size estimation display"""
        if not self.selected_files:
            self.size_estimate_label.configure(text="")
            return
        
        total_original = 0
        total_estimated = 0
        
        for filepath in self.selected_files:
            try:
                est_size, orig_size = get_estimated_size(filepath, self.compression_level)
                total_original += orig_size
                total_estimated += est_size
            except Exception:
                # If we can't estimate, skip
                continue
        
        if total_original > 0:
            if len(self.selected_files) == 1:
                # Single file - show before and after
                savings = total_original - total_estimated
                savings_percent = (savings / total_original) * 100
                estimate_text = f"Estimated size: {format_file_size(total_estimated)} (saves ~{savings_percent:.0f}%)"
            else:
                # Multiple files - show total savings
                savings = total_original - total_estimated
                savings_percent = (savings / total_original) * 100
                estimate_text = f"{len(self.selected_files)} files: saves ~{savings_percent:.0f}% ({format_file_size(savings)})"
            
            self.size_estimate_label.configure(text=estimate_text)

    def start_compression(self):
        """Start compression in a separate thread"""
        if not self.selected_files:
            messagebox.showwarning("Warning", "Please select at least one image.")
            self.center_popup()
            return
        thread = threading.Thread(target=self.compress_images)
        thread.start()

    def compress_images(self):
        """Compress all selected images"""
        total = len(self.selected_files)
        start_time = time.time()
        for idx, file in enumerate(self.selected_files):
            try:
                compress_single_image(file, self.compression_level, self.output_dir)
            except Exception as e:
                self.progressbar.set(0)
                self.status_label.configure(text="Compression error!")
                messagebox.showerror("Error", f"Failed to compress {file}: {e}")
                self.center_popup()
                return
            self.progress = (idx + 1) / total
            elapsed = time.time() - start_time
            if idx + 1 < total:
                est_total = elapsed / (idx + 1) * total
                self.estimated_time = f"{int(est_total - elapsed)}s"
            else:
                self.estimated_time = "Complete"
            self.update_progress()
        
        # Show success message - green label instead of popup
        self.status_label.configure(text="✓ Compression complete!", text_color="#00CC00")
        self.output_label.configure(text=f"✓ Images saved to:\n{self.output_dir}", text_color="#00CC00")
        self.open_folder_button.configure(state="normal", fg_color="#0066FF")

    def open_output_folder(self):
        """Open the output folder in file explorer"""
        if self.output_dir:
            try:
                if os.name == 'nt':  # Windows
                    # Use subprocess for more reliable opening
                    subprocess.Popen(f'explorer "{os.path.normpath(self.output_dir)}"')
                elif os.name == 'posix':  # macOS and Linux
                    subprocess.Popen(['open', self.output_dir])
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open folder: {e}")

    def center_popup(self):
        """Center messagebox dialogs (called after creating them)"""
        # This centers pending messageboxes - works through geometry update
        self.update_idletasks()

    def update_progress(self):
        """Update progress bar and status label"""
        self.progressbar.set(self.progress)
        percent = int(self.progress * 100)
        self.status_label.configure(text=f"Progress: {percent}% | Estimated time: {self.estimated_time}", text_color="white")
        self.update_idletasks()
