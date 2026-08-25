"""
tests/gui_smoke_test.py
========================
Drives the ACTUAL MainWindow GUI (under a virtual display) end-to-end:
navigates every page, runs a real compress operation and a real
decompress operation through the widget callbacks (not just the core
API), and checks the resulting files match. This exercises widget
construction, threading/queue polling, and page wiring exactly as a
real user session would.
"""

import os
import sys
import tempfile
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from gui.main_window import MainWindow


def pump(app, seconds: float) -> None:
    end = time.time() + seconds
    while time.time() < end:
        app.update()
        time.sleep(0.02)


def main() -> int:
    workdir = tempfile.mkdtemp(prefix="huffman_gui_test_")
    src_path = os.path.join(workdir, "sample.txt")
    with open(src_path, "wb") as f:
        f.write((b"the quick brown fox jumps over the lazy dog. " * 3000))

    app = MainWindow()
    app.update()

    # Visit every nav page to make sure they all construct/render without error.
    for key in ["dashboard", "compress", "decompress", "tree", "statistics", "about"]:
        app.show_page(key)
        app.update()
    print("[OK] All pages constructed and navigable")

    # --- Drive the Compress page exactly like a user would ---
    app.show_page("compress")
    compress_page = app.pages["compress"]
    compress_page.input_path = src_path
    compress_page.output_path = workdir
    size = os.path.getsize(src_path)
    compress_page.drop_label.configure(text="test")
    compress_page.info_vars["name"].configure(text="sample.txt")
    compress_page.info_vars["type"].configure(text="TXT file")
    compress_page.info_vars["size"].configure(text=str(size))
    compress_page.compress_btn.configure(state="normal")
    compress_page.start_compression()

    huff_path = None
    deadline = time.time() + 15
    while time.time() < deadline:
        app.update()
        time.sleep(0.02)
        if app.app_state.last_compression_stats is not None:
            huff_path = app.app_state.last_output_path
            break
    assert huff_path is not None, "Compression via GUI did not complete in time"
    assert os.path.isfile(huff_path), "Compressed .huff file was not created"
    print(f"[OK] Compress page produced: {huff_path}")
    print(f"     Stats: {app.app_state.last_compression_stats.summary_lines()}")

    # Tree page should now have data (subscribed to app_state)
    app.show_page("tree")
    app.update()
    assert app.pages["tree"].tree_canvas._tree is not None, "Tree page did not receive tree data"
    print("[OK] Huffman Tree page rendered tree from compression result")

    # Statistics page should now show content
    app.show_page("statistics")
    app.update()
    assert app.pages["statistics"].content_frame is not None, "Statistics page did not populate"
    print("[OK] Statistics page populated")

    # --- Drive the Decompress page ---
    app.show_page("decompress")
    decompress_page = app.pages["decompress"]
    decompress_page.input_path = huff_path
    decompress_page.output_dir = workdir
    decompress_page.reference_path = src_path
    decompress_page.verify_var.set(True)
    decompress_page.decompress_btn.configure(state="normal")
    decompress_page.start_decompression()

    restored_ok = False
    deadline = time.time() + 15
    while time.time() < deadline:
        app.update()
        time.sleep(0.02)
        if app.app_state.last_decompression_stats is not None:
            restored_ok = True
            break
    assert restored_ok, "Decompression via GUI did not complete in time"

    dstats = app.app_state.last_decompression_stats
    with open(src_path, "rb") as f:
        original = f.read()
    with open(dstats.output_path, "rb") as f:
        restored = f.read()
    assert original == restored, "Restored file does not match original!"
    print(f"[OK] Decompress page restored file identical to original: {dstats.output_path}")
    print(f"     Integrity tile shows: {decompress_page.tile_integrity.value_label.cget('text')}")

    # --- Demo mode on the tree page ---
    app.show_page("tree")
    tree_page = app.pages["tree"]
    tree_page.demo_entry.insert(0, "ABRACADABRA")
    tree_page.build_from_demo_text()
    app.update()
    assert tree_page.tree_canvas._tree is not None
    print("[OK] Demo Mode built a tree from custom text 'ABRACADABRA'")

    app.destroy()
    print("\nALL GUI SMOKE TESTS PASSED ✔")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


"""
tests/gui_smoke_test.py
========================
Drives the ACTUAL MainWindow GUI (under a virtual display) end-to-end:
navigates every page, runs a real compress operation and a real
decompress operation through the widget callbacks (not just the core
API), and checks the resulting files match. This exercises widget
construction, threading/queue polling, and page wiring exactly as a
real user session would.
"""

import os
import sys
import tempfile
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from gui.main_window import MainWindow


def pump(app, seconds: float) -> None:
    end = time.time() + seconds
    while time.time() < end:
        app.update()
        time.sleep(0.02)


def main() -> int:
    workdir = tempfile.mkdtemp(prefix="huffman_gui_test_")
    src_path = os.path.join(workdir, "sample.txt")
    with open(src_path, "wb") as f:
        f.write((b"the quick brown fox jumps over the lazy dog. " * 3000))

    app = MainWindow()
    app.update()

    # Visit every nav page to make sure they all construct/render without error.
    for key in ["dashboard", "compress", "decompress", "tree", "statistics", "about"]:
        app.show_page(key)
        app.update()
    print("[OK] All pages constructed and navigable")

    # --- Drive the Compress page exactly like a user would ---
    app.show_page("compress")
    compress_page = app.pages["compress"]
    compress_page.input_path = src_path
    compress_page.output_path = workdir
    size = os.path.getsize(src_path)
    compress_page.drop_label.configure(text="test")
    compress_page.info_vars["name"].configure(text="sample.txt")
    compress_page.info_vars["type"].configure(text="TXT file")
    compress_page.info_vars["size"].configure(text=str(size))
    compress_page.compress_btn.configure(state="normal")
    compress_page.start_compression()

    huff_path = None
    deadline = time.time() + 15
    while time.time() < deadline:
        app.update()
        time.sleep(0.02)
        if app.app_state.last_compression_stats is not None:
            huff_path = app.app_state.last_output_path
            break
    assert huff_path is not None, "Compression via GUI did not complete in time"
    assert os.path.isfile(huff_path), "Compressed .huff file was not created"
    print(f"[OK] Compress page produced: {huff_path}")
    print(f"     Stats: {app.app_state.last_compression_stats.summary_lines()}")

    # Tree page should now have data (subscribed to app_state)
    app.show_page("tree")
    app.update()
    assert app.pages["tree"].tree_canvas._tree is not None, "Tree page did not receive tree data"
    print("[OK] Huffman Tree page rendered tree from compression result")

    # Statistics page should now show content
    app.show_page("statistics")
    app.update()
    assert app.pages["statistics"].content_frame is not None, "Statistics page did not populate"
    print("[OK] Statistics page populated")

    # --- Drive the Decompress page ---
    app.show_page("decompress")
    decompress_page = app.pages["decompress"]
    decompress_page.input_path = huff_path
    decompress_page.output_dir = workdir
    decompress_page.reference_path = src_path
    decompress_page.verify_var.set(True)
    decompress_page.decompress_btn.configure(state="normal")
    decompress_page.start_decompression()

    restored_ok = False
    deadline = time.time() + 15
    while time.time() < deadline:
        app.update()
        time.sleep(0.02)
        if app.app_state.last_decompression_stats is not None:
            restored_ok = True
            break
    assert restored_ok, "Decompression via GUI did not complete in time"

    dstats = app.app_state.last_decompression_stats
    with open(src_path, "rb") as f:
        original = f.read()
    with open(dstats.output_path, "rb") as f:
        restored = f.read()
    assert original == restored, "Restored file does not match original!"
    print(f"[OK] Decompress page restored file identical to original: {dstats.output_path}")
    print(f"     Integrity tile shows: {decompress_page.tile_integrity.value_label.cget('text')}")

    # --- Demo mode on the tree page ---
    app.show_page("tree")
    tree_page = app.pages["tree"]
    tree_page.demo_entry.insert(0, "ABRACADABRA")
    tree_page.build_from_demo_text()
    app.update()
    assert tree_page.tree_canvas._tree is not None
    print("[OK] Demo Mode built a tree from custom text 'ABRACADABRA'")

    app.destroy()
    print("\nALL GUI SMOKE TESTS PASSED ✔")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
