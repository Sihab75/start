"""
gui/app_state.py
=================
A small shared-state container so that different pages (Compress,
Huffman Tree, Statistics) can access the results of the most recent
operation without tight coupling between page classes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional

from core.huffman import HuffmanTree
from core.statistics import CompressionStatistics, DecompressionStatistics


@dataclass
class AppState:
    last_input_path: Optional[str] = None
    last_output_path: Optional[str] = None
    last_frequency_table: Optional[Dict[int, int]] = None
    last_tree: Optional[HuffmanTree] = None
    last_compression_stats: Optional[CompressionStatistics] = None
    last_decompression_stats: Optional[DecompressionStatistics] = None
    last_source_label: str = ""  # e.g. "compressed file" or "demo string"
    last_directory: Optional[str] = None

    # Simple pub/sub so pages can react when new results arrive.
    _listeners: list = field(default_factory=list)

    def subscribe(self, callback) -> None:
        self._listeners.append(callback)

    def notify(self) -> None:
        for cb in list(self._listeners):
            cb()
