import sys
import os
from cx_Freeze import setup, Executable

# Get the path to customtkinter assets
import customtkinter
customtkinter_path = os.path.dirname(customtkinter.__file__)
customtkinter_assets = os.path.join(customtkinter_path, "assets")

# Include necessary packages and modules
build_exe_options = {
    "packages": [
        "customtkinter",
        "PIL",
        "pillow_heif",
        "tqdm",
        "tkinter",
    ],
    "include_files": [
        "open_source_image_compressor/",
        (customtkinter_assets, "customtkinter/assets"),
    ],
    "excludes": [
        "tkinter.test",
        "unittest",
    ],
    "zip_include_packages": ["*"],
    "zip_exclude_packages": ["customtkinter"],  # Don't zip customtkinter
}

# Choose icon file if available
icon_file = "app.ico" if os.path.exists("app.ico") else None

# Create the executable
executables = [
    Executable(
        "main.py",
        base="Win32GUI" if sys.platform == "win32" else None,
        target_name="ImageCompressor",
        icon=icon_file,
    )
]

setup(
    name="Open-source Image Compressor",
    version="0.1.0",
    description="A simple and efficient tool to compress and optimize images",
    author="Jhonatan de Souza",
    options={"build_exe": build_exe_options},
    executables=executables,
)
