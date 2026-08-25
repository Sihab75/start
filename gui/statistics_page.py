"""
gui/statistics_page.py
========================
A dedicated statistics dashboard summarizing the most recent
compression run in detail, including a simple visual bar comparing
original vs. compressed size.
"""

from __future__ import annotations

import customtkinter as ctk

from core.utils import format_size
from gui import theme
from gui.app_state import AppState
from gui.widgets import Card, SectionHeader, StatTile


class SizeBar(ctk.CTkFrame):
    """A horizontal bar chart comparing original vs compressed size."""

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.original_row = self._make_row("Original", theme.TEXT_SECONDARY)
        self.compressed_row = self._make_row("Compressed", theme.ACCENT)

    def _make_row(self, label: str, color: str):
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", pady=6)
        ctk.CTkLabel(row, text=label, font=theme.SMALL_FONT, text_color=theme.TEXT_SECONDARY, width=90, anchor="w").pack(side="left")
        bar_bg = ctk.CTkFrame(row, fg_color=theme.BG_SECONDARY, height=22, corner_radius=6)
        bar_bg.pack(side="left", fill="x", expand=True, padx=(0, 10))
        bar_fill = ctk.CTkFrame(bar_bg, fg_color=color, height=22, corner_radius=6, width=1)
        bar_fill.place(x=0, y=0, relheight=1)
        value_label = ctk.CTkLabel(row, text="--", font=theme.SMALL_FONT, text_color=theme.TEXT_PRIMARY, width=90, anchor="e")
        value_label.pack(side="left")
        return {"bg": bar_bg, "fill": bar_fill, "value": value_label}

    def update_sizes(self, original: int, compressed: int) -> None:
        largest = max(original, compressed, 1)

        def set_row(row, size):
            row["value"].configure(text=format_size(size))
            fraction = size / largest
            self.after(10, lambda: row["bg"].update_idletasks() or row["fill"].place(relwidth=max(fraction, 0.01)))

        set_row(self.original_row, original)
        set_row(self.compressed_row, compressed)


class StatisticsPage(ctk.CTkFrame):
    def __init__(self, master, app_state: AppState, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.app_state = app_state
        app_state.subscribe(self.refresh)

        SectionHeader(
            self, "Compression Statistics", "Detailed metrics from your most recent compression."
        ).pack(fill="x", padx=theme.PAD, pady=(theme.PAD, 10))

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=theme.PAD, pady=(0, theme.PAD))

        self.empty_label = ctk.CTkLabel(
            self.scroll, text="Compress a file first to see statistics here.",
            font=theme.BODY_FONT, text_color=theme.TEXT_MUTED
        )
        self.empty_label.pack(pady=40)

        self.content_frame = None

    def refresh(self) -> None:
        stats = self.app_state.last_compression_stats
        if not stats:
            return

        self.empty_label.pack_forget()
        if self.content_frame:
            self.content_frame.destroy()

        self.content_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True)

        top_card = Card(self.content_frame)
        top_card.pack(fill="x", pady=(0, 14))
        top_inner = ctk.CTkFrame(top_card, fg_color="transparent")
        top_inner.pack(fill="x", padx=20, pady=16)
        ctk.CTkLabel(top_inner, text=f"File: {stats.file_name}  •  {stats.file_type}", font=theme.CARD_TITLE_FONT, text_color=theme.TEXT_PRIMARY, anchor="w").pack(anchor="w")

        bar = SizeBar(top_inner)
        bar.pack(fill="x", pady=(16, 0))
        bar.update_sizes(stats.original_size, stats.compressed_size)

        grid = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        grid.pack(fill="x")
        for col in range(4):
            grid.grid_columnconfigure(col, weight=1, uniform="stats")

        tiles = [
            ("Original Size", format_size(stats.original_size), theme.TEXT_PRIMARY),
            ("Compressed Size", format_size(stats.compressed_size), theme.ACCENT),
            ("Compression Ratio", f"{stats.compression_ratio_percent:.2f}%", theme.ACCENT),
            ("Space Saved", f"{stats.space_saved_percent:.2f}%", theme.SUCCESS),
            ("Unique Byte Values", str(stats.unique_byte_count), theme.TEXT_PRIMARY),
            ("Average Code Length", f"{stats.average_code_length:.2f} bits", theme.TEXT_PRIMARY),
            ("Maximum Code Length", f"{stats.max_code_length} bits", theme.TEXT_PRIMARY),
            ("Processing Time", f"{stats.processing_time_seconds:.2f} s", theme.TEXT_PRIMARY),
        ]
        for i, (label, value, color) in enumerate(tiles):
            tile = StatTile(grid, label, value, accent=color)
            tile.grid(row=i // 4, column=i % 4, sticky="nsew", padx=6, pady=6)

        formula_card = Card(self.content_frame)
        formula_card.pack(fill="x", pady=(14, 0))
        formula_inner = ctk.CTkFrame(formula_card, fg_color="transparent")
        formula_inner.pack(fill="x", padx=20, pady=16)
        ctk.CTkLabel(formula_inner, text="Formulas Used", font=theme.CARD_TITLE_FONT, text_color=theme.TEXT_PRIMARY, anchor="w").pack(anchor="w")
        ctk.CTkLabel(
            formula_inner,
            text=(
                "Compression Ratio = (Compressed Size / Original Size) x 100\n"
                "Space Saved = (1 - Compressed Size / Original Size) x 100"
            ),
            font=theme.MONO_FONT, text_color=theme.TEXT_SECONDARY, justify="left", anchor="w",
        ).pack(anchor="w", pady=(6, 0))
