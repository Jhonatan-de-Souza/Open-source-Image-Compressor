"""
Configuration constants for Open-source Image Compressor
"""

# UI Configuration
UI_TITLE = "Image Compressor"
UI_WIDTH = 600
UI_HEIGHT = 400
APPEARANCE_MODE = "dark"
COLOR_THEME = "dark-blue"

# Compression Configuration
DEFAULT_COMPRESSION_LEVEL = 5
MIN_COMPRESSION_LEVEL = 1
MAX_COMPRESSION_LEVEL = 10

# File Handling
SUPPORTED_FORMATS = [".jpg", ".jpeg", ".png", ".heic"]
OUTPUT_DIR_NAME = "compressed"

# File Dialog
FILE_DIALOG_TYPES = [
    ("Images", "*.jpg;*.jpeg;*.png;*.heic"),
    ("All files", "*.*")
]
