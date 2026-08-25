"""
gui/about.py
============
The About page: static project/academic information plus a beginner
friendly explanation of Huffman Coding, useful to read from during a
viva/presentation.
"""

from __future__ import annotations

import customtkinter as ctk

from gui import theme
from gui.widgets import Card, SectionHeader


class AboutPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        SectionHeader(self, "About This Project").pack(fill="x", padx=theme.PAD, pady=(theme.PAD, 10))

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=theme.PAD, pady=(0, theme.PAD))

        info_card = Card(scroll)
        info_card.pack(fill="x", pady=(0, 14))
        info_inner = ctk.CTkFrame(info_card, fg_color="transparent")
        info_inner.pack(fill="x", padx=20, pady=18)

        fields = [
            ("Project Title", "Efficient File Compression and Decompression Using Huffman Coding Algorithm"),
            ("Course", "Algorithm"),
            ("Technology", "Python 3 + CustomTkinter"),
            ("Algorithm", "Huffman Coding (greedy, prefix-free binary codes)"),
            ("Developed For", "University Academic Project"),
        ]
        for label, value in fields:
            row = ctk.CTkFrame(info_inner, fg_color="transparent")
            row.pack(fill="x", pady=4)
            ctk.CTkLabel(row, text=f"{label}:", font=(theme.FONT_FAMILY, 13, "bold"), text_color=theme.TEXT_PRIMARY, width=150, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=value, font=theme.BODY_FONT, text_color=theme.TEXT_SECONDARY, anchor="w", justify="left", wraplength=520).pack(side="left", fill="x", expand=True)

        self._add_explainer(
            scroll, "What is Huffman Coding?",
            "Huffman Coding is a lossless data compression algorithm. It assigns shorter binary "
            "codes to bytes that appear more frequently in a file, and longer codes to bytes that "
            "appear rarely. Because no code is ever a prefix of another code (a 'prefix-free' or "
            "'prefix' code), a stream of these codes can be decoded unambiguously, one symbol at a "
            "time, without any separators between codes.",
        )
        self._add_explainer(
            scroll, "Why is Compression Useful?",
            "Compression reduces the number of bits needed to store or transmit data. Smaller files "
            "use less disk space, transfer faster over networks, and reduce storage/bandwidth costs. "
            "In Algorithm terms, compression trades a small amount of extra CPU work "
            "(encoding/decoding) for a reduction in the amount of data that must move through memory, "
            "storage, and I/O buses - which are often the real bottleneck in a system.",
        )
        self._add_explainer(
            scroll, "How Does Huffman Coding Work?",
            "1. Count how often each byte value occurs in the file (the frequency table).\n"
            "2. Create one leaf tree-node per distinct byte, holding its frequency.\n"
            "3. Repeatedly take the two nodes with the smallest frequency and merge them under a "
            "new parent node whose frequency is their sum - this is the 'greedy' step.\n"
            "4. Keep merging until only one node remains: the root of the Huffman tree.\n"
            "5. Walk the tree from the root to every leaf, appending '0' for every left branch and "
            "'1' for every right branch. The resulting bit string for each leaf is that byte's code.\n"
            "6. Replace every byte in the original file with its code and pack the resulting bit "
            "stream into bytes to produce the compressed output.",
        )

    def _add_explainer(self, parent, title: str, body: str) -> None:
        card = Card(parent)
        card.pack(fill="x", pady=(0, 14))
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=16)
        ctk.CTkLabel(inner, text=title, font=theme.CARD_TITLE_FONT, text_color=theme.TEXT_PRIMARY, anchor="w").pack(anchor="w")
        ctk.CTkLabel(inner, text=body, font=theme.BODY_FONT, text_color=theme.TEXT_SECONDARY, anchor="w", justify="left", wraplength=760).pack(anchor="w", pady=(8, 0))
