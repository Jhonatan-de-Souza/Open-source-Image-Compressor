"""
Build a single-file Windows executable with PyInstaller.

Usage:
    python build_exe.py

Output: dist/ImageCompressor.exe
"""

import os

import PyInstaller.__main__

ROOT = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    os.path.join(ROOT, "main.py"),
    "--name=ImageCompressor",
    "--onefile",
    "--windowed",
    "--noconfirm",
    "--clean",
    f"--icon={os.path.join(ROOT, 'app.ico')}",
    # ui.py looks for app.ico next to the package, i.e. the bundle root
    f"--add-data={os.path.join(ROOT, 'app.ico')}{os.pathsep}.",
    # customtkinter ships JSON themes and fonts that must be bundled
    "--collect-data=customtkinter",
    "--collect-all=pillow_heif",
    f"--distpath={os.path.join(ROOT, 'dist')}",
    f"--workpath={os.path.join(ROOT, 'build', 'pyinstaller')}",
    f"--specpath={os.path.join(ROOT, 'build', 'pyinstaller')}",
])
