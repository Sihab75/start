"""
core/statistics.py
===================
Holds compression/decompression result statistics and the formulas used
to compute them. Kept separate from compressor/decompressor so the GUI
layer can import just this lightweight module for display purposes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from core.utils import format_size


@dataclass
class CompressionStatistics:
    """All numbers a user would want to see after a compression run."""

    original_size: int
    compressed_size: int
    processing_time_seconds: float
    unique_byte_count: int
    average_code_length: float
    max_code_length: int
    file_name: str = ""
    file_type: str = ""

    @property
    def compression_ratio_percent(self) -> float:
        """Compression Ratio = Compressed Size / Original Size x 100."""
        if self.original_size == 0:
            return 0.0
        return (self.compressed_size / self.original_size) * 100

    @property
    def space_saved_percent(self) -> float:
        """Space Saved = (1 - Compressed Size / Original Size) x 100."""
        if self.original_size == 0:
            return 0.0
        return (1 - (self.compressed_size / self.original_size)) * 100

    def summary_lines(self) -> list[str]:
        return [
            f"Original Size: {format_size(self.original_size)}",
            f"Compressed Size: {format_size(self.compressed_size)}",
            f"Compression Ratio: {self.compression_ratio_percent:.2f}%",
            f"Space Saved: {self.space_saved_percent:.2f}%",
            f"Unique Bytes: {self.unique_byte_count}",
            f"Average Code Length: {self.average_code_length:.2f} bits",
            f"Maximum Code Length: {self.max_code_length} bits",
            f"Processing Time: {self.processing_time_seconds:.2f} seconds",
        ]


@dataclass
class DecompressionStatistics:
    """Numbers to show after a decompression run."""

    compressed_size: int
    restored_size: int
    processing_time_seconds: float
    output_path: str
    integrity_verified: Optional[bool] = None
