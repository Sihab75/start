"""
core/utils.py
=============
General-purpose helper functions used across the Huffman Compressor
project: human-readable size formatting, SHA-256 hashing for integrity
verification, and small filesystem helpers.
"""

from __future__ import annotations

import hashlib
import os
from typing import Callable, Optional

# Size of the chunks used when streaming files to/from disk. Using a
# fixed chunk size keeps memory usage bounded regardless of file size.
CHUNK_SIZE = 1024 * 1024  # 1 MB


def format_size(num_bytes: int) -> str:
    """Convert a byte count into a human readable string (e.g. '3.42 MB')."""
    if num_bytes < 0:
        raise ValueError("Size cannot be negative")

    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(num_bytes)
    unit_index = 0
    while size >= 1024.0 and unit_index < len(units) - 1:
        size /= 1024.0
        unit_index += 1

    if unit_index == 0:
        return f"{int(size)} {units[unit_index]}"
    return f"{size:.2f} {units[unit_index]}"


def compute_sha256(file_path: str, progress_callback: Optional[Callable[[int, int], None]] = None) -> str:
    """
    Compute the SHA-256 hash of a file, reading it in chunks so that large
    files do not need to be loaded entirely into memory.

    :param file_path: Path to the file to hash.
    :param progress_callback: Optional callable(bytes_read, total_bytes).
    :return: Hex digest string.
    """
    sha256 = hashlib.sha256()
    total_size = os.path.getsize(file_path)
    bytes_read = 0

    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            sha256.update(chunk)
            bytes_read += len(chunk)
            if progress_callback:
                progress_callback(bytes_read, total_size)

    return sha256.hexdigest()


def suggest_compressed_name(original_path: str) -> str:
    """Given an input file path, suggest an output '.huff' filename."""
    base = os.path.basename(original_path)
    return base + ".huff"


def ensure_unique_path(path: str) -> str:
    """
    If `path` already exists, append ' (1)', ' (2)', ... before the
    extension until a free path is found. Returns the (possibly modified)
    path that is guaranteed not to already exist.
    """
    if not os.path.exists(path):
        return path

    directory, filename = os.path.split(path)
    name, ext = os.path.splitext(filename)
    counter = 1
    while True:
        candidate = os.path.join(directory, f"{name} ({counter}){ext}")
        if not os.path.exists(candidate):
            return candidate
        counter += 1


def get_file_extension_label(path: str) -> str:
    """Return a friendly file-type label based on extension, e.g. 'TXT file'."""
    ext = os.path.splitext(path)[1].lstrip(".").upper()
    return f"{ext} file" if ext else "Unknown file"
