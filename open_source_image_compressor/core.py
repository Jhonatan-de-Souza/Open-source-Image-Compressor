"""
Core compression logic for Open-source Image Compressor
"""

import os
from PIL import Image
import pillow_heif


def get_estimated_size(filepath, compression_level):
    """
    Estimate the compressed file size.
    
    Args:
        filepath (str): Path to the image file
        compression_level (int): Compression level (1-10)
    
    Returns:
        Tuple of (estimated_size_bytes, original_size_bytes)
    """
    original_size = os.path.getsize(filepath)
    ext = os.path.splitext(filepath)[1].lower()
    
    # Estimate compression ratio based on format and compression level
    # compression_level 1 = 10-20% reduction, 10 = 70-80% reduction
    compression_ratio = 0.1 + (compression_level * 0.07)  # 0.1 to 0.8
    
    if ext in [".jpg", ".jpeg"]:
        # JPEG compression is more effective at higher levels
        compression_ratio = 0.15 + (compression_level * 0.08)
    elif ext == ".png":
        # PNG compression is less aggressive
        compression_ratio = 0.05 + (compression_level * 0.04)
    elif ext == ".heic":
        # HEIC to JPEG conversion with compression
        compression_ratio = 0.2 + (compression_level * 0.07)
    
    estimated_size = int(original_size * (1 - compression_ratio))
    return estimated_size, original_size


def format_file_size(size_bytes):
    """Format bytes to human-readable size."""
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f}KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f}MB"


def _add_small_suffix(filepath):
    """Add '_small' suffix before file extension."""
    name, ext = os.path.splitext(filepath)
    return f"{name}_small{ext}"


def compress_single_image(filepath, compression_level, output_dir=None):
    """
    Compress a single image file.
    
    Args:
        filepath (str): Path to the image file
        compression_level (int): Compression level (1-10, where 1 is minimum, 10 is maximum)
        output_dir (str, optional): Output directory for compressed images. If None, uses same directory as input.
    
    Raises:
        ValueError: If file format is not supported
        RuntimeError: If compression fails
    """
    ext = os.path.splitext(filepath)[1].lower()
    
    # Determine output directory
    if output_dir is None:
        out_dir = os.path.join(os.path.dirname(filepath), "compressed")
    else:
        out_dir = output_dir
    
    os.makedirs(out_dir, exist_ok=True)
    
    # Create output path with _small suffix
    filename_with_suffix = _add_small_suffix(os.path.basename(filepath))
    out_path = os.path.join(out_dir, filename_with_suffix)
    
    if ext in [".jpg", ".jpeg"]:
        _compress_jpeg(filepath, out_path, compression_level)
    elif ext == ".png":
        _compress_png(filepath, out_path, compression_level)
    elif ext == ".heic":
        _compress_heic(filepath, out_path, compression_level)
    else:
        raise ValueError(f"Unsupported file format: {ext}")


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
        raise RuntimeError(f"Failed to compress PNG with Pillow: {e}")


def _compress_heic(filepath, out_path, compression_level):
    """Compress HEIC image and convert to JPEG"""
    heif_file = pillow_heif.open_heif(filepath)
    img = heif_file[0].to_pillow()
    quality = 100 - (compression_level * 9)
    # Replace extension with .jpg for HEIC files
    out_path_jpg = os.path.splitext(out_path)[0] + ".jpg"
    img.save(out_path_jpg, "JPEG", quality=quality, optimize=True)
