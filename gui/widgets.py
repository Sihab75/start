"""
gui/widgets.py
===============
Small reusable CustomTkinter widgets shared across pages: rounded
cards, stat tiles, section headers, and a labeled progress bar with
status text.
"""

from __future__ import annotations

import customtkinter as ctk

from gui import theme


class Card(ctk.CTkFrame):
    """A rounded 'card' container with consistent styling."""

    def __init__(self, master, **kwargs):
        kwargs.setdefault("fg_color", theme.BG_CARD)
        kwargs.setdefault("corner_radius", theme.CORNER_RADIUS)
        kwargs.setdefault("border_width", 1)
        kwargs.setdefault("border_color", theme.BORDER)
        super().__init__(master, **kwargs)


class SectionHeader(ctk.CTkFrame):
    """A page title + subtitle header block."""

    def __init__(self, master, title: str, subtitle: str = "", **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.title_label = ctk.CTkLabel(
            self, text=title, font=theme.HEADING_FONT, text_color=theme.TEXT_PRIMARY, anchor="w"
        )
        self.title_label.pack(anchor="w")
        if subtitle:
            self.subtitle_label = ctk.CTkLabel(
                self, text=subtitle, font=theme.BODY_FONT, text_color=theme.TEXT_SECONDARY, anchor="w"
            )
            self.subtitle_label.pack(anchor="w", pady=(4, 0))


class StatTile(Card):
    """A small metric tile: big value on top, label underneath."""

    def __init__(self, master, label: str, value: str = "--", accent: str = theme.ACCENT, **kwargs):
        super().__init__(master, **kwargs)
        self.value_label = ctk.CTkLabel(
            self, text=value, font=theme.STAT_VALUE_FONT, text_color=accent
        )
        self.value_label.pack(padx=18, pady=(16, 2), anchor="w")
        self.name_label = ctk.CTkLabel(
            self, text=label, font=theme.SMALL_FONT, text_color=theme.TEXT_SECONDARY
        )
        self.name_label.pack(padx=18, pady=(0, 14), anchor="w")

    def set_value(self, value: str) -> None:
        self.value_label.configure(text=value)


class ProgressStatus(ctk.CTkFrame):
    """A progress bar paired with a status message label, updated together."""

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.status_label = ctk.CTkLabel(
            self, text="Ready", font=theme.BODY_FONT, text_color=theme.TEXT_SECONDARY, anchor="w"
        )
        self.status_label.pack(fill="x", anchor="w")
        self.progress_bar = ctk.CTkProgressBar(
            self, height=14, corner_radius=7, progress_color=theme.ACCENT, fg_color=theme.BG_SECONDARY
        )
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", pady=(8, 0))

    def update_status(self, message: str, fraction: float) -> None:
        self.status_label.configure(text=message)
        self.progress_bar.set(fraction)

    def reset(self) -> None:
        self.update_status("Ready", 0)


class PrimaryButton(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        kwargs.setdefault("fg_color", theme.ACCENT)
        kwargs.setdefault("hover_color", theme.ACCENT_HOVER)
        kwargs.setdefault("corner_radius", 10)
        kwargs.setdefault("font", (theme.FONT_FAMILY, 13, "bold"))
        kwargs.setdefault("height", 40)
        super().__init__(master, **kwargs)


class SecondaryButton(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        kwargs.setdefault("fg_color", theme.BG_SECONDARY)
        kwargs.setdefault("hover_color", theme.BG_CARD_HOVER)
        kwargs.setdefault("text_color", theme.TEXT_PRIMARY)
        kwargs.setdefault("border_width", 1)
        kwargs.setdefault("border_color", theme.BORDER)
        kwargs.setdefault("corner_radius", 10)
        kwargs.setdefault("font", (theme.FONT_FAMILY, 13))
        kwargs.setdefault("height", 40)
        super().__init__(master, **kwargs)
