"""
GUI for CompactaImagem using CustomTkinter
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import time
from .core import compress_single_image
from .config import (
    UI_TITLE, UI_WIDTH, UI_HEIGHT, APPEARANCE_MODE, COLOR_THEME,
    DEFAULT_COMPRESSION_LEVEL, MIN_COMPRESSION_LEVEL, MAX_COMPRESSION_LEVEL,
    FILE_DIALOG_TYPES
)

ctk.set_appearance_mode(APPEARANCE_MODE)
ctk.set_default_color_theme(COLOR_THEME)


class ImageCompressorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(UI_TITLE)
        self.geometry(f"{UI_WIDTH}x{UI_HEIGHT}")
        self.resizable(False, False)

        self.selected_files = []
        self.compression_level = DEFAULT_COMPRESSION_LEVEL
        self.progress = 0
        self.estimated_time = "--"

        self.create_widgets()

    def create_widgets(self):
        """Create all UI widgets"""
        self.label = ctk.CTkLabel(self, text="Selecione as imagens para compressão:")
        self.label.pack(pady=10)

        self.select_button = ctk.CTkButton(self, text="Selecionar Imagens", command=self.select_files)
        self.select_button.pack(pady=5)

        self.slider_label = ctk.CTkLabel(self, text="Nível de Compressão (1=Mínimo, 10=Máximo):")
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

        self.compress_button = ctk.CTkButton(self, text="Comprimir", command=self.start_compression)
        self.compress_button.pack(pady=10)

        self.progressbar = ctk.CTkProgressBar(self)
        self.progressbar.set(0)
        self.progressbar.pack(pady=10, fill="x", padx=40)

        self.status_label = ctk.CTkLabel(self, text="Progresso: 0% | Tempo estimado: --")
        self.status_label.pack(pady=5)

    def select_files(self):
        """Open file dialog to select images"""
        files = filedialog.askopenfilenames(title="Selecione as imagens", filetypes=FILE_DIALOG_TYPES)
        if files:
            self.selected_files = list(files)
            messagebox.showinfo("Selecionado", f"{len(files)} arquivo(s) selecionado(s)")

    def update_compression_level(self, value):
        """Update compression level from slider"""
        self.compression_level = int(value)

    def start_compression(self):
        """Start compression in a separate thread"""
        if not self.selected_files:
            messagebox.showwarning("Aviso", "Selecione pelo menos uma imagem.")
            return
        thread = threading.Thread(target=self.compress_images)
        thread.start()

    def compress_images(self):
        """Compress all selected images"""
        total = len(self.selected_files)
        start_time = time.time()
        for idx, file in enumerate(self.selected_files):
            try:
                compress_single_image(file, self.compression_level)
            except Exception as e:
                self.progressbar.set(0)
                self.status_label.configure(text="Erro na compressão!")
                messagebox.showerror("Erro", f"Erro ao comprimir {file}: {e}")
                return
            self.progress = (idx + 1) / total
            elapsed = time.time() - start_time
            if idx + 1 < total:
                est_total = elapsed / (idx + 1) * total
                self.estimated_time = f"{int(est_total - elapsed)}s"
            else:
                self.estimated_time = "Finalizado"
            self.update_progress()
        messagebox.showinfo("Concluído", "Compressão finalizada!")

    def update_progress(self):
        """Update progress bar and status label"""
        self.progressbar.set(self.progress)
        percent = int(self.progress * 100)
        self.status_label.configure(text=f"Progresso: {percent}% | Tempo estimado: {self.estimated_time}")
        self.update_idletasks()
