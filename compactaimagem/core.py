"""
Core compression logic for CompactaImagem
"""

import os
from PIL import Image
import pillow_heif


def compress_single_image(filepath, compression_level):
    """
    Compress a single image file.
    
    Args:
        filepath (str): Path to the image file
        compression_level (int): Compression level (1-10, where 1 is minimum, 10 is maximum)
    
    Raises:
        ValueError: If file format is not supported
        RuntimeError: If compression fails
    """
    ext = os.path.splitext(filepath)[1].lower()
    out_dir = os.path.join(os.path.dirname(filepath), "comprimidas")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, os.path.basename(filepath))
    
    if ext in [".jpg", ".jpeg"]:
        _compress_jpeg(filepath, out_path, compression_level)
    elif ext == ".png":
        _compress_png(filepath, out_path, compression_level)
    elif ext == ".heic":
        _compress_heic(filepath, out_path, compression_level)
    else:
        raise ValueError(f"Formato de arquivo não suportado: {ext}")


def _compress_jpeg(filepath, out_path, compression_level):
    """Compress JPEG image"""
    img = Image.open(filepath)
    quality = 100 - (compression_level * 9)
    img.save(out_path, "JPEG", quality=quality, optimize=True)


def _compress_png(filepath, out_path, compression_level):
    """Compress PNG image"""
    img = Image.open(filepath)
    # Convert to paletized mode (P) for better compression
    img_p = img.convert("P", palette=Image.ADAPTIVE, colors=256)
    png_compress_level = 9  # maximum compression
    try:
        img_p.save(out_path, "PNG", optimize=True, compress_level=png_compress_level)
    except Exception as e:
        raise RuntimeError(f"Falha ao comprimir PNG com Pillow: {e}")


def _compress_heic(filepath, out_path, compression_level):
    """Compress HEIC image and convert to JPEG"""
    heif_file = pillow_heif.open_heif(filepath)
    img = heif_file[0].to_pillow()
    quality = 100 - (compression_level * 9)
    img.save(out_path + ".jpg", "JPEG", quality=quality, optimize=True)
