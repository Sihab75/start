"""
gui/dashboard.py
=================
The landing page of the application: a friendly overview with quick
navigation cards into the main features.
"""

from __future__ import annotations

from typing import Callable

import customtkinter as ctk

from gui import theme
from gui.widgets import Card, SectionHeader


class NavCard(Card):
    """A clickable dashboard card that jumps to another page."""

    def __init__(self, master, emoji: str, title: str, description: str, on_click: Callable, **kwargs):
        super().__init__(master, **kwargs)
        self._on_click = on_click

        inner = ctk.CTkFrame(self, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=20, pady=18)

        ctk.CTkLabel(inner, text=emoji, font=(theme.FONT_FAMILY, 30)).pack(anchor="w")
        ctk.CTkLabel(
            inner, text=title, font=theme.CARD_TITLE_FONT, text_color=theme.TEXT_PRIMARY, anchor="w"
        ).pack(anchor="w", pady=(10, 2))
        ctk.CTkLabel(
            inner,
            text=description,
            font=theme.SMALL_FONT,
            text_color=theme.TEXT_SECONDARY,
            anchor="w",
            justify="left",
            wraplength=220,
        ).pack(anchor="w")

        for widget in (self, inner, *inner.winfo_children()):
            widget.bind("<Button-1>", lambda _e: self._on_click())
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)
            try:
                widget.configure(cursor="hand2")
            except Exception:
                pass

    def _on_enter(self, _e=None):
        self.configure(fg_color=theme.BG_CARD_HOVER, border_color=theme.ACCENT)

    def _on_leave(self, _e=None):
        self.configure(fg_color=theme.BG_CARD, border_color=theme.BORDER)


class DashboardPage(ctk.CTkFrame):
    def __init__(self, master, navigate: Callable[[str], None], **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.navigate = navigate

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=theme.PAD, pady=(theme.PAD, 8))
        ctk.CTkLabel(
            header, text="Huffman File Compressor", font=theme.TITLE_FONT, text_color=theme.TEXT_PRIMARY
        ).pack(anchor="w")
        ctk.CTkLabel(
            header,
            text="Efficient File Compression and Decompression Using Huffman Coding",
            font=theme.SUBTITLE_FONT,
            text_color=theme.TEXT_SECONDARY,
        ).pack(anchor="w", pady=(4, 0))

        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=theme.PAD, pady=theme.PAD)
        for col in range(4):
            grid.grid_columnconfigure(col, weight=1, uniform="cards")

        cards = [
            ("🗜", "Compress", "Select any file and shrink it with the Huffman\nalgorithm.", "compress"),
            ("📦", "Decompress", "Restore a .huff file back to its original\nform.", "decompress"),
            ("🌳", "Huffman Tree", "Visualize the tree and code table built from\nyour last file.", "tree"),
            ("📊", "Statistics", "Inspect detailed metrics from your last\noperation.", "statistics"),
        ]
        for i, (emoji, title, desc, page) in enumerate(cards):
            card = NavCard(grid, emoji, title, desc, on_click=lambda p=page: self.navigate(p))
            card.grid(row=0, column=i, sticky="nsew", padx=8, pady=8)

        info_card = Card(self)
        info_card.pack(fill="x", padx=theme.PAD, pady=(0, theme.PAD))
        inner = ctk.CTkFrame(info_card, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=16)
        ctk.CTkLabel(
            inner, text="Quick Start", font=theme.CARD_TITLE_FONT, text_color=theme.TEXT_PRIMARY, anchor="w"
        ).pack(anchor="w")
        steps = (
            "1. Go to Compress, choose any file, and click Compress.\n"
            "2. Open Huffman Tree to see the frequency table, tree, and codes for that file.\n"
            "3. Go to Decompress, select the generated .huff file, and restore it.\n"
            "4. Check Statistics for compression ratio, space saved, and timing details."
        )
        ctk.CTkLabel(
            inner, text=steps, font=theme.BODY_FONT, text_color=theme.TEXT_SECONDARY, justify="left", anchor="w"
        ).pack(anchor="w", pady=(6, 0))
