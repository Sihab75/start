"""
gui/compress_page.py
=====================
The Compress page: choose an input file, pick an output location, run
Huffman compression on a background thread (so the GUI never freezes),
and display live progress plus final statistics.
"""

from __future__ import annotations

import os
import queue
import threading
from tkinter import filedialog, messagebox
from typing import Optional

import customtkinter as ctk

from core.compressor import CompressionError, HuffmanCompressor
from core.huffman import HuffmanTree
from core.utils import ensure_unique_path, format_size, get_file_extension_label, suggest_compressed_name
from gui import theme
from gui.app_state import AppState
from gui.widgets import Card, PrimaryButton, ProgressStatus, SecondaryButton, SectionHeader, StatTile


class CompressPage(ctk.CTkFrame):
    def __init__(self, master, app_state: AppState, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.app_state = app_state
        self.input_path: Optional[str] = None
        self.output_path: Optional[str] = None
        self._queue: "queue.Queue" = queue.Queue()
        self._worker: Optional[threading.Thread] = None

        SectionHeader(
            self, "Compress a File", "Select any file on your computer to compress it with Huffman coding."
        ).pack(fill="x", padx=theme.PAD, pady=(theme.PAD, 10))

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=theme.PAD, pady=(0, theme.PAD))
        body.grid_columnconfigure(0, weight=3)
        body.grid_columnconfigure(1, weight=2)
        body.grid_rowconfigure(0, weight=1)

        # ---- Left: file selection + actions ----
        left = Card(body)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_inner = ctk.CTkFrame(left, fg_color="transparent")
        left_inner.pack(fill="both", expand=True, padx=22, pady=20)

        self.drop_label = ctk.CTkLabel(
            left_inner,
            text="📁\n\nNo file selected\nClick \"Select File\" to choose a file to compress",
            font=theme.BODY_FONT,
            text_color=theme.TEXT_SECONDARY,
            justify="center",
        )
        self.drop_label.pack(fill="x", pady=(10, 16))

        btn_row = ctk.CTkFrame(left_inner, fg_color="transparent")
        btn_row.pack(fill="x")
        SecondaryButton(btn_row, text="Select File", command=self.select_file).pack(side="left")
        self.output_btn = SecondaryButton(btn_row, text="Choose Output Folder", command=self.select_output_dir)
        self.output_btn.pack(side="left", padx=(10, 0))

        info_frame = ctk.CTkFrame(left_inner, fg_color="transparent")
        info_frame.pack(fill="x", pady=(18, 10))
        self.info_vars = {}
        for key, label in [
            ("name", "File Name"),
            ("type", "File Type"),
            ("size", "Original Size"),
            ("output", "Output Location"),
        ]:
            row = ctk.CTkFrame(info_frame, fg_color="transparent")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=f"{label}:", font=theme.BODY_FONT, text_color=theme.TEXT_SECONDARY, width=140, anchor="w").pack(side="left")
            value = ctk.CTkLabel(row, text="--", font=theme.BODY_FONT, text_color=theme.TEXT_PRIMARY, anchor="w")
            value.pack(side="left", fill="x", expand=True)
            self.info_vars[key] = value

        self.compress_btn = PrimaryButton(left_inner, text="Compress", command=self.start_compression, state="disabled")
        self.compress_btn.pack(fill="x", pady=(14, 10))

        self.progress = ProgressStatus(left_inner)
        self.progress.pack(fill="x")

        # ---- Right: results ----
        right = Card(body)
        right.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        right_inner = ctk.CTkFrame(right, fg_color="transparent")
        right_inner.pack(fill="both", expand=True, padx=20, pady=20)
        ctk.CTkLabel(right_inner, text="Compression Results", font=theme.CARD_TITLE_FONT, text_color=theme.TEXT_PRIMARY, anchor="w").pack(anchor="w")

        self.result_status = ctk.CTkLabel(right_inner, text="Run a compression to see results here.", font=theme.BODY_FONT, text_color=theme.TEXT_SECONDARY, anchor="w", justify="left", wraplength=260)
        self.result_status.pack(anchor="w", pady=(6, 14))

        stats_grid = ctk.CTkFrame(right_inner, fg_color="transparent")
        stats_grid.pack(fill="x")
        stats_grid.grid_columnconfigure((0, 1), weight=1)
        self.tile_ratio = StatTile(stats_grid, "Compression Ratio")
        self.tile_ratio.grid(row=0, column=0, sticky="nsew", padx=(0, 6), pady=6)
        self.tile_saved = StatTile(stats_grid, "Space Saved", accent=theme.SUCCESS)
        self.tile_saved.grid(row=0, column=1, sticky="nsew", padx=(6, 0), pady=6)
        self.tile_time = StatTile(stats_grid, "Processing Time")
        self.tile_time.grid(row=1, column=0, sticky="nsew", padx=(0, 6), pady=6)
        self.tile_compressed = StatTile(stats_grid, "Compressed Size")
        self.tile_compressed.grid(row=1, column=1, sticky="nsew", padx=(6, 0), pady=6)

    # ------------------------------------------------------------------
    # File selection
    # ------------------------------------------------------------------
    def select_file(self) -> None:
        initialdir = self.app_state.last_directory or os.path.expanduser("~")
        path = filedialog.askopenfilename(title="Select a file to compress", initialdir=initialdir)
        if not path:
            return
        self.input_path = path
        self.app_state.last_directory = os.path.dirname(path)

        try:
            size = os.path.getsize(path)
        except OSError as exc:
            messagebox.showerror("Error", f"Could not read the selected file:\n{exc}")
            return

        self.drop_label.configure(text=f"📄\n\n{os.path.basename(path)}\n({format_size(size)})")
        self.info_vars["name"].configure(text=os.path.basename(path))
        self.info_vars["type"].configure(text=get_file_extension_label(path))
        self.info_vars["size"].configure(text=format_size(size))

        if not self.output_path:
            suggested_dir = os.path.dirname(path)
            self.output_path = suggested_dir
            self.info_vars["output"].configure(text=suggested_dir)

        self.compress_btn.configure(state="normal")
        self.progress.reset()

    def select_output_dir(self) -> None:
        initialdir = self.output_path or os.path.expanduser("~")
        directory = filedialog.askdirectory(title="Select output folder", initialdir=initialdir)
        if directory:
            self.output_path = directory
            self.info_vars["output"].configure(text=directory)

    # ------------------------------------------------------------------
    # Compression (background thread)
    # ------------------------------------------------------------------
    def start_compression(self) -> None:
        if not self.input_path:
            return
        if not os.path.isfile(self.input_path):
            messagebox.showerror("Error", "The selected file no longer exists.")
            return

        out_dir = self.output_path or os.path.dirname(self.input_path)
        target_name = suggest_compressed_name(self.input_path)
        target_path = ensure_unique_path(os.path.join(out_dir, target_name))

        self.compress_btn.configure(state="disabled")
        self.progress.update_status("Starting...", 0.0)
        self.result_status.configure(text="Compressing, please wait...")

        self._worker = threading.Thread(target=self._run_compression, args=(self.input_path, target_path), daemon=True)
        self._worker.start()
        self.after(50, self._poll_queue)

    def _run_compression(self, input_path: str, output_path: str) -> None:
        def progress_callback(stage: str, fraction: float) -> None:
            self._queue.put(("progress", stage, fraction))

        try:
            compressor = HuffmanCompressor(progress_callback=progress_callback)
            stats = compressor.compress(input_path, output_path)

            # Rebuild the tree/frequency table for the visualization & tree pages.
            tree = None
            if stats.original_size > 0:
                with open(input_path, "rb") as f:
                    data = f.read()
                freq: dict[int, int] = {}
                for b in data:
                    freq[b] = freq.get(b, 0) + 1
                tree = HuffmanTree(freq)
            else:
                freq = {}

            self._queue.put(("done", stats, freq, tree, output_path))
        except CompressionError as exc:
            self._queue.put(("error", str(exc)))
        except Exception as exc:  # noqa: BLE001
            self._queue.put(("error", f"An unexpected error occurred: {exc}"))

    def _poll_queue(self) -> None:
        try:
            while True:
                item = self._queue.get_nowait()
                kind = item[0]
                if kind == "progress":
                    _, stage, fraction = item
                    self.progress.update_status(stage, fraction)
                elif kind == "done":
                    _, stats, freq, tree, output_path = item
                    self._on_compression_done(stats, freq, tree, output_path)
                elif kind == "error":
                    _, message = item
                    self._on_compression_error(message)
        except queue.Empty:
            pass

        if self._worker is not None and self._worker.is_alive():
            self.after(50, self._poll_queue)

    def _on_compression_done(self, stats, freq, tree, output_path: str) -> None:
        self.compress_btn.configure(state="normal")
        self.progress.update_status("✓ Compression Completed Successfully", 1.0)

        self.result_status.configure(
            text=f"✓ Saved to:\n{output_path}", text_color=theme.SUCCESS
        )
        self.tile_ratio.set_value(f"{stats.compression_ratio_percent:.2f}%")
        self.tile_saved.set_value(f"{stats.space_saved_percent:.2f}%")
        self.tile_time.set_value(f"{stats.processing_time_seconds:.2f}s")
        self.tile_compressed.set_value(format_size(stats.compressed_size))

        if stats.compressed_size >= stats.original_size and stats.original_size > 0:
            messagebox.showinfo(
                "Note",
                "The compressed file is not smaller than the original.\n\n"
                "This is expected for very small files or already-random data: the "
                ".huff header (frequency table + metadata) adds overhead that can "
                "outweigh the savings when there isn't enough redundancy to exploit.",
            )

        self.app_state.last_input_path = self.input_path
        self.app_state.last_output_path = output_path
        self.app_state.last_frequency_table = freq
        self.app_state.last_tree = tree
        self.app_state.last_compression_stats = stats
        self.app_state.last_source_label = os.path.basename(self.input_path)
        self.app_state.notify()

    def _on_compression_error(self, message: str) -> None:
        self.compress_btn.configure(state="normal")
        self.progress.update_status("✗ Compression Failed", 0.0)
        self.result_status.configure(text=f"✗ {message}", text_color=theme.DANGER)
        messagebox.showerror("Compression Failed", message)
