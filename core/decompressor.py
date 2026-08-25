"""
core/decompressor.py
=====================
HuffmanDecompressor reverses the pipeline implemented in
core/compressor.py:

    read .huff header -> rebuild Huffman tree -> read compressed bits ->
    walk tree bit-by-bit -> reconstruct original bytes -> write output file
"""

from __future__ import annotations

import os
import time
from typing import Callable, Optional

from core.file_format import InvalidHuffFileError, read_header
from core.huffman import BitReader, HuffmanNode, HuffmanTree
from core.statistics import DecompressionStatistics
from core.utils import CHUNK_SIZE

ProgressCallback = Optional[Callable[[str, float], None]]

# How many decoded bytes to buffer before flushing to disk.
WRITE_FLUSH_THRESHOLD = 1024 * 1024  # 1 MB


class DecompressionError(Exception):
    """Raised when decompression cannot be completed."""


class HuffmanDecompressor:
    """Encapsulates the Huffman decompression algorithm end-to-end."""

    def __init__(self, progress_callback: ProgressCallback = None):
        self.progress_callback = progress_callback

    def _report(self, stage: str, fraction: float) -> None:
        if self.progress_callback:
            self.progress_callback(stage, max(0.0, min(1.0, fraction)))

    def get_original_filename(self, input_path: str) -> str:
        """Peek at a .huff file's header to retrieve the stored original filename."""
        try:
            with open(input_path, "rb") as f:
                header = read_header(f)
            return header.original_filename
        except (InvalidHuffFileError, OSError):
            return ""

    def decompress(self, input_path: str, output_path: str) -> DecompressionStatistics:
        """
        Decompress a .huff file at `input_path` into `output_path`.

        :raises DecompressionError: on any I/O, format, or validation failure.
        :return: DecompressionStatistics describing the result.
        """
        start_time = time.perf_counter()

        if not os.path.isfile(input_path):
            raise DecompressionError(f"Compressed file not found: {input_path}")

        compressed_size = os.path.getsize(input_path)

        # ---- Step 1: read header ----
        self._report("Reading compressed file...", 0.0)
        try:
            with open(input_path, "rb") as f:
                header = read_header(f)
                compressed_payload = f.read()
        except InvalidHuffFileError as exc:
            raise DecompressionError(str(exc)) from exc
        except PermissionError as exc:
            raise DecompressionError(f"Permission denied while reading: {exc}") from exc
        except OSError as exc:
            raise DecompressionError(f"Error reading compressed file: {exc}") from exc

        # ---- Edge case: originally empty file ----
        if header.original_size == 0 or not header.frequency_table:
            try:
                with open(output_path, "wb"):
                    pass
            except OSError as exc:
                raise DecompressionError(f"Could not write output file: {exc}") from exc
            elapsed = time.perf_counter() - start_time
            self._report("Done", 1.0)
            return DecompressionStatistics(
                compressed_size=compressed_size,
                restored_size=0,
                processing_time_seconds=elapsed,
                output_path=output_path,
            )

        # ---- Step 2: reconstruct the Huffman tree from the stored frequency table ----
        self._report("Reconstructing Huffman tree...", 0.5)
        try:
            tree = HuffmanTree(header.frequency_table)
        except ValueError as exc:
            raise DecompressionError(f"Corrupted frequency table: {exc}") from exc

        # ---- Step 3 & 4: decode compressed bits back into original bytes ----
        self._report("Decoding data...", 0.0)
        reader = BitReader(compressed_payload, header.padding_bits)

        try:
            with open(output_path, "wb") as out:
                output_buffer = bytearray()
                bytes_written = 0
                node: HuffmanNode = tree.root

                while bytes_written < header.original_size:
                    bit = reader.read_bit()
                    if bit is None:
                        raise DecompressionError(
                            "Compressed data ended unexpectedly before the full file could be "
                            "restored. The .huff file appears to be corrupted or truncated."
                        )
                    node = node.left if bit == 0 else node.right
                    if node is None:
                        raise DecompressionError(
                            "Invalid bit sequence encountered while decoding. "
                            "The .huff file appears to be corrupted."
                        )
                    if node.is_leaf():
                        output_buffer.append(node.byte)
                        bytes_written += 1
                        node = tree.root

                        if len(output_buffer) >= WRITE_FLUSH_THRESHOLD:
                            out.write(output_buffer)
                            output_buffer.clear()
                            self._report("Decoding data...", bytes_written / header.original_size)
                            self._report("Writing output file...", bytes_written / header.original_size)

                if output_buffer:
                    out.write(output_buffer)
        except OSError as exc:
            raise DecompressionError(f"Could not write output file: {exc}") from exc

        restored_size = os.path.getsize(output_path)
        if restored_size != header.original_size:
            raise DecompressionError(
                "Restored file size does not match the size recorded in the .huff header. "
                "The compressed file may be corrupted."
            )

        elapsed = time.perf_counter() - start_time
        self._report("Done", 1.0)
        return DecompressionStatistics(
            compressed_size=compressed_size,
            restored_size=restored_size,
            processing_time_seconds=elapsed,
            output_path=output_path,
        )
