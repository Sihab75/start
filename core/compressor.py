"""
core/compressor.py
===================
HuffmanCompressor drives the full compression pipeline:

    read file -> frequency table -> Huffman tree -> codes ->
    encode -> write .huff file

Every stage reports progress through an optional callback so the GUI
(run in a background thread) can update a progress bar / status label
without freezing.
"""

from __future__ import annotations

import os
import time
from typing import Callable, Optional

from core.file_format import write_header
from core.huffman import BitWriter, HuffmanTree
from core.statistics import CompressionStatistics
from core.utils import CHUNK_SIZE, get_file_extension_label

# progress_callback signature: (stage_name: str, fraction_complete: float)
ProgressCallback = Optional[Callable[[str, float], None]]


class CompressionError(Exception):
    """Raised when compression cannot be completed."""


class HuffmanCompressor:
    """Encapsulates the Huffman compression algorithm end-to-end."""

    def __init__(self, progress_callback: ProgressCallback = None):
        self.progress_callback = progress_callback

    def _report(self, stage: str, fraction: float) -> None:
        if self.progress_callback:
            self.progress_callback(stage, max(0.0, min(1.0, fraction)))

    def compress(self, input_path: str, output_path: str) -> CompressionStatistics:
        """
        Compress `input_path` into a new .huff file at `output_path`.

        :raises CompressionError: on any I/O or validation failure.
        :return: CompressionStatistics describing the result.
        """
        start_time = time.perf_counter()

        if not os.path.isfile(input_path):
            raise CompressionError(f"Input file not found: {input_path}")

        try:
            original_size = os.path.getsize(input_path)
        except OSError as exc:
            raise CompressionError(f"Could not read file size: {exc}") from exc

        # ---- Step 1 & 2: read file in chunks, calculate byte frequencies ----
        self._report("Reading file...", 0.0)
        frequency_table: dict[int, int] = {}
        try:
            with open(input_path, "rb") as f:
                bytes_read = 0
                while True:
                    chunk = f.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    for b in chunk:
                        frequency_table[b] = frequency_table.get(b, 0) + 1
                    bytes_read += len(chunk)
                    if original_size > 0:
                        self._report("Building frequency table...", bytes_read / original_size)
        except PermissionError as exc:
            raise CompressionError(f"Permission denied while reading: {exc}") from exc
        except OSError as exc:
            raise CompressionError(f"Error reading input file: {exc}") from exc

        original_filename = os.path.basename(input_path)

        # ---- Edge case: empty file ----
        if original_size == 0:
            self._report("Writing compressed file...", 0.5)
            try:
                with open(output_path, "wb") as out:
                    write_header(out, original_filename, 0, {}, 0)
            except OSError as exc:
                raise CompressionError(f"Could not write output file: {exc}") from exc
            elapsed = time.perf_counter() - start_time
            compressed_size = os.path.getsize(output_path)
            self._report("Done", 1.0)
            return CompressionStatistics(
                original_size=0,
                compressed_size=compressed_size,
                processing_time_seconds=elapsed,
                unique_byte_count=0,
                average_code_length=0.0,
                max_code_length=0,
                file_name=original_filename,
                file_type=get_file_extension_label(input_path),
            )

        # ---- Step 3 & 4: build the Huffman tree from the frequency table ----
        self._report("Building Huffman tree...", 0.0)
        tree = HuffmanTree(frequency_table)

        # ---- Step 5: codes were generated as part of tree construction ----
        self._report("Generating Huffman codes...", 1.0)
        codes = tree.codes

        # ---- Step 6, 7, 8, 9: encode data, pack bits, write header + payload ----
        try:
            with open(output_path, "wb") as out:
                write_header(out, original_filename, original_size, frequency_table, padding_bits=0)
                # Reserve a placeholder byte for padding; we'll patch it after
                # we know the true padding, to avoid buffering the whole
                # encoded payload in memory for large files.
                padding_field_offset = out.tell() - 1

                writer = BitWriter()
                bytes_processed = 0
                with open(input_path, "rb") as f:
                    while True:
                        chunk = f.read(CHUNK_SIZE)
                        if not chunk:
                            break
                        for b in chunk:
                            writer.write_bits(codes[b])
                        ready = writer.take_bytes()
                        if ready:
                            out.write(ready)
                        bytes_processed += len(chunk)
                        self._report("Encoding data...", bytes_processed / original_size)

                final_bytes, padding = writer.finish()
                if final_bytes:
                    out.write(final_bytes)

                self._report("Writing compressed file...", 1.0)
                out.seek(padding_field_offset)
                out.write(bytes([padding]))
        except OSError as exc:
            raise CompressionError(f"Could not write output file: {exc}") from exc

        compressed_size = os.path.getsize(output_path)
        elapsed = time.perf_counter() - start_time

        stats = CompressionStatistics(
            original_size=original_size,
            compressed_size=compressed_size,
            processing_time_seconds=elapsed,
            unique_byte_count=len(frequency_table),
            average_code_length=tree.average_code_length(),
            max_code_length=tree.max_code_length(),
            file_name=original_filename,
            file_type=get_file_extension_label(input_path),
        )
        self._report("Done", 1.0)
        return stats
