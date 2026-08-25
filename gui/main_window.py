"""
gui/main_window.py
====================
The top-level application window: sets up the CustomTkinter theme,
builds a sidebar for navigation, and hosts each page in a shared
content area, swapping the visible page as the user clicks around.
"""

from __future__ import annotations

import customtkinter as ctk

from gui import theme
from gui.about import AboutPage
from gui.app_state import AppState
from gui.compress_page import CompressPage
from gui.dashboard import DashboardPage
from gui.decompress_page import DecompressPage
from gui.statistics_page import StatisticsPage
from gui.tree_view import TreeVisualizationPage

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

NAV_ITEMS = [
    ("dashboard", "🏠", "Dashboard"),
    ("compress", "🗜", "Compress"),
    ("decompress", "📦", "Decompress"),
    ("tree", "🌳", "Huffman Tree"),
    ("statistics", "📊", "Statistics"),
    ("about", "ℹ", "About"),
]


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Huffman File Compressor")
        self.geometry("1180x760")
        self.minsize(980, 640)
        self.configure(fg_color=theme.BG_PRIMARY)

        self.app_state = AppState()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_content_area()

        self.pages = {}
        self._build_pages()
        self.show_page("dashboard")

    # ------------------------------------------------------------------
    def _build_sidebar(self) -> None:
        sidebar = ctk.CTkFrame(self, width=220, fg_color=theme.BG_SECONDARY, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsw")
        sidebar.grid_propagate(False)

        brand = ctk.CTkFrame(sidebar, fg_color="transparent")
        brand.pack(fill="x", padx=20, pady=(24, 30))
        ctk.CTkLabel(brand, text="🗜 Huffman", font=(theme.FONT_FAMILY, 19, "bold"), text_color=theme.TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(brand, text="File Compressor", font=theme.SMALL_FONT, text_color=theme.TEXT_MUTED).pack(anchor="w")

        self.nav_buttons = {}
        for key, emoji, label in NAV_ITEMS:
            btn = ctk.CTkButton(
                sidebar,
                text=f"  {emoji}   {label}",
                anchor="w",
                fg_color="transparent",
                hover_color=theme.BG_CARD_HOVER,
                text_color=theme.TEXT_SECONDARY,
                font=theme.BODY_FONT,
                corner_radius=10,
                height=42,
                command=lambda k=key: self.show_page(k),
            )
            btn.pack(fill="x", padx=14, pady=3)
            self.nav_buttons[key] = btn

        footer = ctk.CTkLabel(
            sidebar, text="Algorithm\nAcademic Project", font=theme.SMALL_FONT,
            text_color=theme.TEXT_MUTED, justify="left"
        )
        footer.pack(side="bottom", padx=20, pady=20, anchor="w")

    def _build_content_area(self) -> None:
        self.content_area = ctk.CTkFrame(self, fg_color=theme.BG_PRIMARY, corner_radius=0)
        self.content_area.grid(row=0, column=1, sticky="nsew")
        self.content_area.grid_rowconfigure(0, weight=1)
        self.content_area.grid_columnconfigure(0, weight=1)

    def _build_pages(self) -> None:
        self.pages["dashboard"] = DashboardPage(self.content_area, navigate=self.show_page)
        self.pages["compress"] = CompressPage(self.content_area, app_state=self.app_state)
        self.pages["decompress"] = DecompressPage(self.content_area, app_state=self.app_state)
        self.pages["tree"] = TreeVisualizationPage(self.content_area, app_state=self.app_state)
        self.pages["statistics"] = StatisticsPage(self.content_area, app_state=self.app_state)
        self.pages["about"] = AboutPage(self.content_area)

        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")

    # ------------------------------------------------------------------
    def show_page(self, key: str) -> None:
        if key not in self.pages:
            return
        self.pages[key].tkraise()
        for nav_key, btn in self.nav_buttons.items():
            if nav_key == key:
                btn.configure(fg_color=theme.ACCENT_SOFT, text_color=theme.TEXT_PRIMARY)
            else:
                btn.configure(fg_color="transparent", text_color=theme.TEXT_SECONDARY)
