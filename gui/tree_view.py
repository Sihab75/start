"""
gui/tree_view.py
=================
The Huffman Tree Visualization page. Draws the actual Huffman tree built
from the most recently compressed file (or from custom "Demo Mode" text)
on a zoomable/scrollable Canvas, and lists the resulting byte -> code
table alongside it.
"""

from __future__ import annotations

from typing import Dict, Optional

import customtkinter as ctk
import tkinter as tk

from core.huffman import HuffmanNode, HuffmanTree
from gui import theme
from gui.app_state import AppState
from gui.widgets import Card, PrimaryButton, SecondaryButton, SectionHeader

NODE_RADIUS = 20
LEVEL_HEIGHT = 90
LEAF_SPACING = 70


def byte_label(byte_value: int) -> str:
    """Format a byte value for display: printable ASCII shown as char, else hex."""
    if 32 <= byte_value <= 126:
        return f"'{chr(byte_value)}'"
    return f"0x{byte_value:02X}"


class TreeCanvas(ctk.CTkFrame):
    """Scrollable + zoomable canvas that draws a HuffmanTree."""

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=theme.BG_SECONDARY, **kwargs)
        self.canvas = tk.Canvas(self, bg=theme.BG_SECONDARY, highlightthickness=0)
        h_scroll = ctk.CTkScrollbar(self, orientation="horizontal", command=self.canvas.xview)
        v_scroll = ctk.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.canvas.bind("<MouseWheel>", self._on_mousewheel)  # Windows / macOS
        self.canvas.bind("<Button-4>", lambda e: self._zoom(1.1, e))  # Linux scroll up
        self.canvas.bind("<Button-5>", lambda e: self._zoom(0.9, e))  # Linux scroll down

        self._scale = 1.0
        self._tree: Optional[HuffmanTree] = None

    def _on_mousewheel(self, event) -> None:
        factor = 1.1 if event.delta > 0 else 0.9
        self._zoom(factor, event)

    def _zoom(self, factor: float, event=None) -> None:
        self._scale *= factor
        self._scale = max(0.2, min(self._scale, 4.0))
        self.canvas.scale("all", 0, 0, factor, factor)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def fit_to_screen(self) -> None:
        bbox = self.canvas.bbox("all")
        if not bbox:
            return
        canvas_w = max(self.canvas.winfo_width(), 1)
        canvas_h = max(self.canvas.winfo_height(), 1)
        content_w = max(bbox[2] - bbox[0], 1)
        content_h = max(bbox[3] - bbox[1], 1)
        factor = min(canvas_w / content_w, canvas_h / content_h, 1.5) * 0.92
        self.canvas.scale("all", 0, 0, factor, factor)
        self._scale *= factor
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

    def draw_tree(self, tree: HuffmanTree) -> None:
        self.canvas.delete("all")
        self._tree = tree
        self._scale = 1.0

        # Assign each leaf an x-slot via in-order traversal so the tree
        # never has overlapping subtrees.
        leaf_positions: Dict[int, int] = {}
        counter = [0]

        def assign_x(node: HuffmanNode) -> float:
            if node is None:
                return 0
            if node.is_leaf():
                x = counter[0] * LEAF_SPACING + LEAF_SPACING
                leaf_positions[id(node)] = x
                counter[0] += 1
                return x
            left_x = assign_x(node.left) if node.left else None
            right_x = assign_x(node.right) if node.right else None
            if left_x is not None and right_x is not None:
                x = (left_x + right_x) / 2
            else:
                x = left_x if left_x is not None else right_x
            leaf_positions[id(node)] = x
            return x

        assign_x(tree.root)

        max_depth = self._max_depth(tree.root)
        top_margin = 40

        def draw_node(node: HuffmanNode, depth: int, edge_label: str = ""):
            if node is None:
                return
            x = leaf_positions[id(node)]
            y = top_margin + depth * LEVEL_HEIGHT

            if node.left:
                self._draw_edge(x, y, leaf_positions[id(node.left)], top_margin + (depth + 1) * LEVEL_HEIGHT, "0")
                draw_node(node.left, depth + 1)
            if node.right:
                self._draw_edge(x, y, leaf_positions[id(node.right)], top_margin + (depth + 1) * LEVEL_HEIGHT, "1")
                draw_node(node.right, depth + 1)

            self._draw_node_circle(x, y, node)

        draw_node(tree.root, 0)

        bbox = self.canvas.bbox("all")
        if bbox:
            padded = (bbox[0] - 30, bbox[1] - 30, bbox[2] + 30, bbox[3] + 30)
            self.canvas.configure(scrollregion=padded)
        self.after(50, self.fit_to_screen)

    @staticmethod
    def _max_depth(node: Optional[HuffmanNode]) -> int:
        if node is None or node.is_leaf():
            return 0
        return 1 + max(TreeCanvas._max_depth(node.left), TreeCanvas._max_depth(node.right))

    def _draw_edge(self, x1, y1, x2, y2, bit_label: str) -> None:
        color = theme.ACCENT if bit_label == "0" else theme.SUCCESS
        self.canvas.create_line(x1, y1, x2, y2, fill=theme.BORDER, width=2)
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        self.canvas.create_text(
            mid_x, mid_y, text=bit_label, fill=color, font=(theme.FONT_FAMILY, 11, "bold")
        )

    def _draw_node_circle(self, x, y, node: HuffmanNode) -> None:
        if node.is_leaf():
            fill = theme.ACCENT_SOFT
            outline = theme.ACCENT
            label = byte_label(node.byte)
        else:
            fill = theme.BG_CARD
            outline = theme.BORDER
            label = ""

        r = NODE_RADIUS
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=fill, outline=outline, width=2)
        self.canvas.create_text(x, y - 4, text=str(node.freq), fill=theme.TEXT_PRIMARY, font=(theme.FONT_FAMILY, 10, "bold"))
        if label:
            self.canvas.create_text(x, y + 10, text=label, fill=theme.TEXT_SECONDARY, font=(theme.FONT_FAMILY, 9))


class TreeVisualizationPage(ctk.CTkFrame):
    def __init__(self, master, app_state: AppState, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.app_state = app_state
        app_state.subscribe(self.refresh_from_state)

        SectionHeader(
            self, "Huffman Tree Visualization",
            "See the actual tree and code table built for your most recently compressed file, "
            "or try Demo Mode with your own text.",
        ).pack(fill="x", padx=theme.PAD, pady=(theme.PAD, 10))

        # ---- Demo mode input row ----
        demo_card = Card(self)
        demo_card.pack(fill="x", padx=theme.PAD)
        demo_inner = ctk.CTkFrame(demo_card, fg_color="transparent")
        demo_inner.pack(fill="x", padx=18, pady=14)
        ctk.CTkLabel(demo_inner, text="Demo Mode:", font=theme.BODY_FONT, text_color=theme.TEXT_SECONDARY).pack(side="left")
        self.demo_entry = ctk.CTkEntry(demo_inner, placeholder_text="Type text, e.g. ABRACADABRA", width=280)
        self.demo_entry.pack(side="left", padx=10)
        PrimaryButton(demo_inner, text="Build Tree", width=120, command=self.build_from_demo_text).pack(side="left")
        SecondaryButton(demo_inner, text="Fit to Screen", width=120, command=self.fit_to_screen).pack(side="right")

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=theme.PAD, pady=theme.PAD)
        body.grid_columnconfigure(0, weight=3)
        body.grid_columnconfigure(1, weight=2)
        body.grid_rowconfigure(0, weight=1)

        tree_card = Card(body)
        tree_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        tree_card.grid_rowconfigure(1, weight=1)
        tree_card.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(tree_card, text="Tree (scroll to pan, mouse wheel to zoom)", font=theme.SMALL_FONT, text_color=theme.TEXT_MUTED).grid(row=0, column=0, sticky="w", padx=16, pady=(12, 4))
        self.tree_canvas = TreeCanvas(tree_card)
        self.tree_canvas.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))

        table_card = Card(body)
        table_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        table_card.grid_rowconfigure(1, weight=1)
        table_card.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(table_card, text="Huffman Code Table", font=theme.CARD_TITLE_FONT, text_color=theme.TEXT_PRIMARY).grid(row=0, column=0, sticky="w", padx=16, pady=(14, 6))
        self.table_frame = ctk.CTkScrollableFrame(table_card, fg_color=theme.BG_SECONDARY)
        self.table_frame.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))

        self.empty_label = ctk.CTkLabel(
            self.table_frame, text="Compress a file or use Demo Mode\nto see codes here.",
            font=theme.SMALL_FONT, text_color=theme.TEXT_MUTED, justify="center"
        )
        self.empty_label.pack(pady=30)

    def fit_to_screen(self) -> None:
        self.tree_canvas.fit_to_screen()

    def build_from_demo_text(self) -> None:
        text = self.demo_entry.get()
        if not text:
            return
        data = text.encode("utf-8")
        freq: Dict[int, int] = {}
        for b in data:
            freq[b] = freq.get(b, 0) + 1
        tree = HuffmanTree(freq)
        self._render(tree, freq)

    def refresh_from_state(self) -> None:
        tree = self.app_state.last_tree
        freq = self.app_state.last_frequency_table
        if tree and freq:
            self._render(tree, freq)

    def _render(self, tree: HuffmanTree, freq: Dict[int, int]) -> None:
        self.tree_canvas.draw_tree(tree)
        self._populate_table(tree, freq)

    def _populate_table(self, tree: HuffmanTree, freq: Dict[int, int]) -> None:
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        header = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 4))
        for text, w in (("Byte", 70), ("Freq", 60), ("Code", 140)):
            ctk.CTkLabel(header, text=text, font=(theme.FONT_FAMILY, 12, "bold"), text_color=theme.TEXT_SECONDARY, width=w, anchor="w").pack(side="left")

        for byte_value in sorted(freq.keys(), key=lambda b: (-freq[b], b)):
            row = ctk.CTkFrame(self.table_frame, fg_color="transparent")
            row.pack(fill="x", pady=1)
            ctk.CTkLabel(row, text=byte_label(byte_value), font=theme.MONO_FONT, text_color=theme.TEXT_PRIMARY, width=70, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=str(freq[byte_value]), font=theme.MONO_FONT, text_color=theme.TEXT_PRIMARY, width=60, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=tree.codes.get(byte_value, ""), font=theme.MONO_FONT, text_color=theme.ACCENT, width=140, anchor="w").pack(side="left")
