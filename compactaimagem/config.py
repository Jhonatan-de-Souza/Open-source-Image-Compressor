"""
Configuration constants for CompactaImagem
"""

# UI Configuration
UI_TITLE = "Compressor de Imagens"
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
OUTPUT_DIR_NAME = "comprimidas"

# File Dialog
FILE_DIALOG_TYPES = [
    ("Imagens", "*.jpg;*.jpeg;*.png;*.heic"),
    ("Todos os arquivos", "*.*")
]
