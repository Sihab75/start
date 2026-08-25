"""
core/file_format.py
====================
Defines and implements the custom ".huff" binary file format used by
this project.

FILE FORMAT LAYOUT
-------------------
All multi-byte integers are stored big-endian ("network byte order").

+--------------------------+--------------------------------------------+
| Field                    | Size                                       |
+--------------------------+--------------------------------------------+
| Magic number "HUFF"      | 4 bytes  (ASCII)                           |
| Format version           | 1 byte   (unsigned)                        |
| Original filename length | 2 bytes  (unsigned short)                  |
| Original filename        | variable (UTF-8, length given above)       |
| Original file size       | 8 bytes  (unsigned long long, in bytes)    |
| Number of unique bytes   | 2 bytes  (unsigned short, 0-256)           |
| Frequency table entries  | 9 bytes each: 1 byte value + 8 byte count  |
| Padding bit count        | 1 byte   (0-7, bits added to last byte)    |
| Compressed data          | variable (rest of file)                    |
+--------------------------+--------------------------------------------+

The frequency table doubles as the metadata needed to reconstruct the
*exact* Huffman tree used during compression (see core/huffman.py -
tree construction is deterministic given the same frequency table).

This header design keeps the format simple, human-explainable (useful
for a Computer Architecture viva) and fully self-describing: a .huff
file contains everything needed to restore the original file, with no
external dependency.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass, field
from typing import BinaryIO, Dict

MAGIC_NUMBER = b"HUFF"
FORMAT_VERSION = 1


class InvalidHuffFileError(Exception):
    """Raised when a file does not conform to the expected .huff format."""


@dataclass
class FileHeader:
    """In-memory representation of a parsed .huff file header."""

    original_filename: str
    original_size: int
    frequency_table: Dict[int, int]
    padding_bits: int
    version: int = FORMAT_VERSION


def write_header(f: BinaryIO, original_filename: str, original_size: int,
                  frequency_table: Dict[int, int], padding_bits: int) -> None:
    """Write the .huff header (everything except the compressed payload) to `f`."""
    f.write(MAGIC_NUMBER)
    f.write(struct.pack(">B", FORMAT_VERSION))

    name_bytes = original_filename.encode("utf-8")
    f.write(struct.pack(">H", len(name_bytes)))
    f.write(name_bytes)

    f.write(struct.pack(">Q", original_size))

    f.write(struct.pack(">H", len(frequency_table)))
    for byte_value in sorted(frequency_table.keys()):
        f.write(struct.pack(">B", byte_value))
        f.write(struct.pack(">Q", frequency_table[byte_value]))

    f.write(struct.pack(">B", padding_bits))


def read_header(f: BinaryIO) -> FileHeader:
    """Read and validate a .huff header from `f`. Raises InvalidHuffFileError on failure."""
    magic = f.read(4)
    if magic != MAGIC_NUMBER:
        raise InvalidHuffFileError(
            "This does not look like a valid .huff file (magic number mismatch). "
            "The file may be corrupted or was not produced by this application."
        )

    version_bytes = f.read(1)
    if len(version_bytes) != 1:
        raise InvalidHuffFileError("Corrupted .huff file: missing version field.")
    (version,) = struct.unpack(">B", version_bytes)
    if version != FORMAT_VERSION:
        raise InvalidHuffFileError(f"Unsupported .huff format version: {version}")

    name_len_bytes = f.read(2)
    if len(name_len_bytes) != 2:
        raise InvalidHuffFileError("Corrupted .huff file: missing filename length.")
    (name_len,) = struct.unpack(">H", name_len_bytes)

    name_bytes = f.read(name_len)
    if len(name_bytes) != name_len:
        raise InvalidHuffFileError("Corrupted .huff file: filename truncated.")
    original_filename = name_bytes.decode("utf-8", errors="replace")

    size_bytes = f.read(8)
    if len(size_bytes) != 8:
        raise InvalidHuffFileError("Corrupted .huff file: missing original size field.")
    (original_size,) = struct.unpack(">Q", size_bytes)

    count_bytes = f.read(2)
    if len(count_bytes) != 2:
        raise InvalidHuffFileError("Corrupted .huff file: missing frequency table size.")
    (num_unique,) = struct.unpack(">H", count_bytes)

    frequency_table: Dict[int, int] = {}
    for _ in range(num_unique):
        entry = f.read(9)
        if len(entry) != 9:
            raise InvalidHuffFileError("Corrupted .huff file: frequency table truncated.")
        byte_value, freq = struct.unpack(">BQ", entry)
        frequency_table[byte_value] = freq

    padding_bytes = f.read(1)
    if len(padding_bytes) != 1:
        raise InvalidHuffFileError("Corrupted .huff file: missing padding field.")
    (padding_bits,) = struct.unpack(">B", padding_bytes)
    if not (0 <= padding_bits <= 7):
        raise InvalidHuffFileError("Corrupted .huff file: invalid padding value.")

    return FileHeader(
        original_filename=original_filename,
        original_size=original_size,
        frequency_table=frequency_table,
        padding_bits=padding_bits,
        version=version,
    )
