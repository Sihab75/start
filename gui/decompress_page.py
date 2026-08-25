"""
gui/decompress_page.py
========================
The Decompress page: choose a .huff file, restore it, and optionally
verify the restored file's integrity via SHA-256 against a reference
(original) file.
"""

from __future__ import annotations

import os
import queue
import threading
from tkinter import filedialog, messagebox
from typing import Optional

import customtkinter as ctk

from core.decompressor import DecompressionError, HuffmanDecompressor
from core.utils import compute_sha256, ensure_unique_path, format_size
from gui import theme
from gui.app_state import AppState
from gui.widgets import Card, PrimaryButton, ProgressStatus, SecondaryButton, SectionHeader, StatTile


class DecompressPage(ctk.CTkFrame):
    def __init__(self, master, app_state: AppState, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.app_state = app_state
        self.input_path: Optional[str] = None
        self.output_dir: Optional[str] = None
        self.reference_path: Optional[str] = None
        self._queue: "queue.Queue" = queue.Queue()
        self._worker: Optional[threading.Thread] = None

        SectionHeader(
            self, "Decompress a File", "Select a .huff file produced by this application to restore it."
        ).pack(fill="x", padx=theme.PAD, pady=(theme.PAD, 10))

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=theme.PAD, pady=(0, theme.PAD))
        body.grid_columnconfigure(0, weight=3)
        body.grid_columnconfigure(1, weight=2)
        body.grid_rowconfigure(0, weight=1)

        left = Card(body)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_inner = ctk.CTkFrame(left, fg_color="transparent")
        left_inner.pack(fill="both", expand=True, padx=22, pady=20)

        self.drop_label = ctk.CTkLabel(
            left_inner,
            text="📦\n\nNo .huff file selected\nClick \"Select .huff File\" to choose one",
            font=theme.BODY_FONT,
            text_color=theme.TEXT_SECONDARY,
            justify="center",
        )
        self.drop_label.pack(fill="x", pady=(10, 16))

        btn_row = ctk.CTkFrame(left_inner, fg_color="transparent")
        btn_row.pack(fill="x")
        SecondaryButton(btn_row, text="Select .huff File", command=self.select_file).pack(side="left")
        SecondaryButton(btn_row, text="Choose Output Folder", command=self.select_output_dir).pack(side="left", padx=(10, 0))

        info_frame = ctk.CTkFrame(left_inner, fg_color="transparent")
        info_frame.pack(fill="x", pady=(18, 10))
        self.info_vars = {}
        for key, label in [
            ("name", "File Name"),
            ("size", "Compressed Size"),
            ("output", "Output Folder"),
        ]:
            row = ctk.CTkFrame(info_frame, fg_color="transparent")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=f"{label}:", font=theme.BODY_FONT, text_color=theme.TEXT_SECONDARY, width=140, anchor="w").pack(side="left")
            value = ctk.CTkLabel(row, text="--", font=theme.BODY_FONT, text_color=theme.TEXT_PRIMARY, anchor="w")
            value.pack(side="left", fill="x", expand=True)
            self.info_vars[key] = value

        verify_row = ctk.CTkFrame(left_inner, fg_color="transparent")
        verify_row.pack(fill="x", pady=(4, 4))
        self.verify_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            verify_row, text="Verify integrity against original file (SHA-256)",
            variable=self.verify_var, command=self._toggle_reference_btn,
            font=theme.SMALL_FONT, text_color=theme.TEXT_SECONDARY,
        ).pack(side="left")
        self.reference_btn = SecondaryButton(verify_row, text="Choose Original...", command=self.select_reference, state="disabled", width=140, height=28)
        self.reference_btn.pack(side="left", padx=(10, 0))

        self.decompress_btn = PrimaryButton(left_inner, text="Decompress", command=self.start_decompression, state="disabled")
        self.decompress_btn.pack(fill="x", pady=(14, 10))

        self.progress = ProgressStatus(left_inner)
        self.progress.pack(fill="x")

        right = Card(body)
        right.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        right_inner = ctk.CTkFrame(right, fg_color="transparent")
        right_inner.pack(fill="both", expand=True, padx=20, pady=20)
        ctk.CTkLabel(right_inner, text="Decompression Results", font=theme.CARD_TITLE_FONT, text_color=theme.TEXT_PRIMARY, anchor="w").pack(anchor="w")

        self.result_status = ctk.CTkLabel(right_inner, text="Run a decompression to see results here.", font=theme.BODY_FONT, text_color=theme.TEXT_SECONDARY, anchor="w", justify="left", wraplength=260)
        self.result_status.pack(anchor="w", pady=(6, 14))

        stats_grid = ctk.CTkFrame(right_inner, fg_color="transparent")
        stats_grid.pack(fill="x")
        stats_grid.grid_columnconfigure((0, 1), weight=1)
        self.tile_restored = StatTile(stats_grid, "Restored Size")
        self.tile_restored.grid(row=0, column=0, sticky="nsew", padx=(0, 6), pady=6)
        self.tile_time = StatTile(stats_grid, "Processing Time")
        self.tile_time.grid(row=0, column=1, sticky="nsew", padx=(6, 0), pady=6)
        self.tile_integrity = StatTile(stats_grid, "Integrity Check", value="Not run")
        self.tile_integrity.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=0, pady=6)

    # ------------------------------------------------------------------
    def _toggle_reference_btn(self) -> None:
        self.reference_btn.configure(state="normal" if self.verify_var.get() else "disabled")

    def select_reference(self) -> None:
        path = filedialog.askopenfilename(title="Select the original file to compare against")
        if path:
            self.reference_path = path
            self.reference_btn.configure(text=os.path.basename(path))

    def select_file(self) -> None:
        initialdir = self.app_state.last_directory or os.path.expanduser("~")
        path = filedialog.askopenfilename(
            title="Select a .huff file", initialdir=initialdir,
            filetypes=[("Huffman compressed files", "*.huff"), ("All files", "*.*")],
        )
        if not path:
            return
        self.input_path = path
        self.app_state.last_directory = os.path.dirname(path)

        try:
            size = os.path.getsize(path)
        except OSError as exc:
            messagebox.showerror("Error", f"Could not read the selected file:\n{exc}")
            return

        self.drop_label.configure(text=f"📦\n\n{os.path.basename(path)}\n({format_size(size)})")
        self.info_vars["name"].configure(text=os.path.basename(path))
        self.info_vars["size"].configure(text=format_size(size))

        if not self.output_dir:
            self.output_dir = os.path.dirname(path)
            self.info_vars["output"].configure(text=self.output_dir)

        self.decompress_btn.configure(state="normal")
        self.progress.reset()

    def select_output_dir(self) -> None:
        initialdir = self.output_dir or os.path.expanduser("~")
        directory = filedialog.askdirectory(title="Select output folder", initialdir=initialdir)
        if directory:
            self.output_dir = directory
            self.info_vars["output"].configure(text=directory)

    # ------------------------------------------------------------------
    def start_decompression(self) -> None:
        if not self.input_path or not os.path.isfile(self.input_path):
            messagebox.showerror("Error", "The selected .huff file no longer exists.")
            return

        decompressor = HuffmanDecompressor()
        original_name = decompressor.get_original_filename(self.input_path) or "restored_file"
        out_dir = self.output_dir or os.path.dirname(self.input_path)
        target_path = ensure_unique_path(os.path.join(out_dir, original_name))

        self.decompress_btn.configure(state="disabled")
        self.progress.update_status("Starting...", 0.0)
        self.result_status.configure(text="Decompressing, please wait...", text_color=theme.TEXT_SECONDARY)
        self.tile_integrity.set_value("Not run")

        verify = self.verify_var.get()
        reference = self.reference_path if verify else None

        self._worker = threading.Thread(
            target=self._run_decompression, args=(self.input_path, target_path, reference), daemon=True
        )
        self._worker.start()
        self.after(50, self._poll_queue)

    def _run_decompression(self, input_path: str, output_path: str, reference_path: Optional[str]) -> None:
        def progress_callback(stage: str, fraction: float) -> None:
            self._queue.put(("progress", stage, fraction))

        try:
            decompressor = HuffmanDecompressor(progress_callback=progress_callback)
            stats = decompressor.decompress(input_path, output_path)

            integrity_result = None
            if reference_path and os.path.isfile(reference_path):
                self._queue.put(("progress", "Verifying integrity (SHA-256)...", 1.0))
                original_hash = compute_sha256(reference_path)
                restored_hash = compute_sha256(output_path)
                integrity_result = original_hash == restored_hash

            self._queue.put(("done", stats, integrity_result))
        except DecompressionError as exc:
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
                    _, stats, integrity_result = item
                    self._on_decompression_done(stats, integrity_result)
                elif kind == "error":
                    _, message = item
                    self._on_decompression_error(message)
        except queue.Empty:
            pass

        if self._worker is not None and self._worker.is_alive():
            self.after(50, self._poll_queue)

    def _on_decompression_done(self, stats, integrity_result) -> None:
        self.decompress_btn.configure(state="normal")
        self.progress.update_status("✓ Decompression Completed Successfully", 1.0)
        self.result_status.configure(text=f"✓ Restored to:\n{stats.output_path}", text_color=theme.SUCCESS)

        self.tile_restored.set_value(format_size(stats.restored_size))
        self.tile_time.set_value(f"{stats.processing_time_seconds:.2f}s")

        if integrity_result is None:
            self.tile_integrity.set_value("Not verified")
        elif integrity_result:
            self.tile_integrity.set_value("✓ Verified")
            self.tile_integrity.value_label.configure(text_color=theme.SUCCESS)
        else:
            self.tile_integrity.set_value("✗ Mismatch")
            self.tile_integrity.value_label.configure(text_color=theme.DANGER)
            messagebox.showwarning("Integrity Check Failed", "The restored file's SHA-256 hash does not match the original file.")

        self.app_state.last_decompression_stats = stats
        self.app_state.notify()

    def _on_decompression_error(self, message: str) -> None:
        self.decompress_btn.configure(state="normal")
        self.progress.update_status("✗ Decompression Failed", 0.0)
        self.result_status.configure(text=f"✗ {message}", text_color=theme.DANGER)
        messagebox.showerror("Decompression Failed", message)
