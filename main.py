"""
main.py
=======
Entry point for the Huffman File Compressor desktop application.

Run with:
    python main.py
"""

from __future__ import annotations

import sys
import traceback
from tkinter import messagebox

from gui.main_window import MainWindow


def main() -> int:
    try:
        app = MainWindow()
        app.mainloop()
        return 0
    except Exception as exc:  
        traceback.print_exc()
        try:
            messagebox.showerror("Huffman File Compressor - Fatal Error", f"The application failed to start:\n\n{exc}")
        except Exception:
            pass
        return 1


if __name__ == "__main__":
    sys.exit(main())
