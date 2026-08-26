# 🗜 Huffman File Compressor

**Efficient File Compression and Decompression Using Huffman Coding Algorithm**

A complete, professional desktop GUI application built for a Computer Architecture
academic project. It compresses and decompresses *any* file type using a
from-scratch implementation of the Huffman Coding algorithm — no `zipfile`,
`gzip`, `bz2`, `lzma`, or `zlib` involved in the actual compression logic.

---

## 1. Project Overview

This project demonstrates how lossless data compression works at the byte
level, using the classic greedy Huffman Coding algorithm, wrapped in a
modern, dark-themed desktop application built with **CustomTkinter**.

You can compress any file (text, image, PDF, audio, executable, source code,
etc.), inspect the exact Huffman tree and code table that was built for it,
decompress the result back to a byte-identical copy of the original, and
verify that with a SHA-256 integrity check.

---

## 2. Features

-  **Real Huffman compression** for arbitrary binary files, implemented manually
-  **Decompression** that reconstructs the file byte-for-byte
-  **Live Huffman Tree Visualization** — zoomable / scrollable canvas showing
  actual nodes, frequencies, and 0/1 edge labels for your file
-  **Huffman Code Table** — scrollable byte → frequency → code listing
-  **Statistics dashboard** — compression ratio, space saved, average/max
  code length, unique byte count, processing time, size comparison bar
-  **Demo Mode** — type any string (e.g. `ABRACADABRA`) and instantly see
  its frequencies, tree, and codes — perfect for a live viva demonstration
-  **SHA-256 integrity verification** between original and restored files
- **Fully responsive GUI** — compression/decompression run on background
  threads with a live progress bar, so the interface never freezes
- **Robust error handling** — empty files, single-byte files, corrupted
  `.huff` files, permission errors, etc. are all handled gracefully with
  friendly messages (no raw Python tracebacks)
-  **Modern dark UI** — sidebar navigation, rounded cards, consistent
  typography and spacing, hover effects

---

## 3. Technologies

- **Python 3.9+**
- **CustomTkinter** (GUI)
- **Standard library only** for everything else: `heapq`, `struct`, `hashlib`,
  `threading`, `queue`, `os`, `time`, `tkinter.filedialog`

No internet connection or external/cloud service is required — the
application runs completely offline.

---

## 4. Huffman Algorithm Explanation

Huffman Coding is a **greedy, lossless compression algorithm**. The core
idea: bytes that occur *more often* in the file get *shorter* binary codes,
and bytes that occur *rarely* get *longer* codes. Because the resulting
codes form a **prefix-free code** (no code is a prefix of another), the
encoded bit stream can be decoded unambiguously with no separators.

### Algorithm steps

1. **Count frequency** of every byte value (0–255) in the input file.
2. **Create a leaf node** for each distinct byte, holding its frequency.
3. **Build a min-heap (priority queue)** of all leaf nodes.
4. **Repeat** until one node remains:
   - Pop the two nodes with the *smallest* frequency.
   - Merge them under a new internal node whose frequency is their sum.
   - Push the new node back onto the heap.
5. The last remaining node is the **root of the Huffman tree**.
6. **Generate codes**: walk from the root to every leaf; append `'0'` for
   every left branch and `'1'` for every right branch. The path to a leaf
   *is* that byte's code.
7. **Encode**: replace every byte of the input with its code and pack the
   resulting bit stream into bytes (8 bits per output byte, zero-padded at
   the end if needed).

---

## 5. How Compression Works (this app)

1. Read the input file in 1 MB chunks and count byte frequencies (`core/compressor.py`).
2. Build the Huffman tree and generate codes (`core/huffman.py`).
3. Write a `.huff` header containing the original filename, original size,
   the frequency table (which doubles as the metadata needed to rebuild
   the *exact same* tree later), and padding info (`core/file_format.py`).
4. Stream-encode the file a second time, packing bits into bytes and
   writing them straight to the output file (keeps memory usage bounded
   even for very large files).
5. Patch the padding-bit-count field once the final byte is known.

## 6. How Decompression Works

1. Read and validate the `.huff` header (magic number `HUFF`, version,
   filename, original size, frequency table, padding).
2. Rebuild the Huffman tree from the stored frequency table — tree
   construction is **deterministic**, so this produces an identical tree
   to the one used during compression.
3. Read the compressed bit stream and walk the tree bit-by-bit: `0` → go
   left, `1` → go right. Every time a leaf is reached, emit that byte and
   reset to the root.
4. Stop once the number of emitted bytes equals the original file size
   stored in the header.
5. Write the restored bytes to the chosen output file.

---

## 7. Project Architecture

```
huffman_compressor/
│
├── main.py                    # Application entry point
├── requirements.txt
├── README.md
│
├── core/                      # Pure algorithm / file-I/O layer (no GUI code)
│   ├── __init__.py
│   ├── huffman.py             # HuffmanNode, HuffmanTree, BitWriter, BitReader
│   ├── compressor.py          # HuffmanCompressor (full compress pipeline)
│   ├── decompressor.py        # HuffmanDecompressor (full decompress pipeline)
│   ├── file_format.py         # .huff header read/write (FileHeader)
│   ├── statistics.py          # CompressionStatistics / DecompressionStatistics
│   └── utils.py                # size formatting, SHA-256, path helpers
│
├── gui/                       # CustomTkinter presentation layer
│   ├── __init__.py
│   ├── main_window.py         # MainWindow: sidebar navigation + page routing
│   ├── app_state.py           # Shared state passed between pages
│   ├── theme.py                # Colors / fonts / spacing constants
│   ├── widgets.py               # Reusable Card / StatTile / ProgressStatus / buttons
│   ├── dashboard.py            # Dashboard / home page
│   ├── compress_page.py        # Compress page (threaded)
│   ├── decompress_page.py      # Decompress page (threaded, SHA-256 verify)
│   ├── tree_view.py             # Huffman Tree Visualization + Demo Mode + code table
│   ├── statistics_page.py       # Statistics dashboard
│   └── about.py                 # About / educational page
│
├── tests/
│   ├── test_core.py             # Correctness test suite (10 edge cases)
│   └── gui_smoke_test.py        # End-to-end test that drives the real GUI
│
├── assets/icons/                # (reserved for future icon assets)
└── output/                      # (reserved default output folder)
```

**Design principle:** `core/` contains zero GUI imports and can be reused,
unit tested, or driven from a CLI independently of the GUI. `gui/` only
orchestrates `core/` and never re-implements algorithm logic.

---

## 8. Custom `.huff` File Format

All multi-byte integers are big-endian.

| Field                     | Size                                   |
|---------------------------|-----------------------------------------|
| Magic number `"HUFF"`     | 4 bytes (ASCII)                        |
| Format version            | 1 byte                                 |
| Original filename length  | 2 bytes                                |
| Original filename         | variable (UTF-8)                       |
| Original file size        | 8 bytes                                |
| Number of unique bytes    | 2 bytes (0–256)                        |
| Frequency table entries   | 9 bytes each (1 byte value + 8 byte count) |
| Padding bit count         | 1 byte (0–7)                           |
| Compressed data           | remainder of file                      |

The frequency table is all the metadata needed to deterministically
rebuild the exact Huffman tree used at compression time — no separate
tree serialization is required.

---

## 9. Installation

### Windows 10/11 + VS Code

1. **Create the project folder** (or unzip the provided archive) and open
   it in VS Code: `File → Open Folder…` → select `huffman_compressor`.
2. **Open a terminal** in VS Code: `` Terminal → New Terminal `` (make sure
   it's using PowerShell or Command Prompt).
3. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   ```
4. **Activate it**:
   ```bash
   .venv\Scripts\activate
   ```
   (If PowerShell blocks the script, run
   `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first.)
5. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
6. In VS Code, select the `.venv` interpreter: `Ctrl+Shift+P` →
   *Python: Select Interpreter* → choose the one inside `.venv`.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 10. How to Run

```bash
python main.py
```

A window titled **"Huffman File Compressor"** should open with a sidebar
and a Dashboard page.

---

## 11. Usage Guide

### Compress a file
1. Sidebar → **Compress**.
2. Click **Select File**, choose any file.
3. (Optional) **Choose Output Folder**.
4. Click **Compress**. Watch the progress bar move through each stage.
5. Results (ratio, space saved, timing, compressed size) appear on the right.

### Decompress a file
1. Sidebar → **Decompress**.
2. Click **Select .huff File**, pick a file produced by this app.
3. (Optional) tick **Verify integrity against original file (SHA-256)** and
   choose the original file to compare against.
4. Click **Decompress**. Results appear on the right, including
   "✓ Verified" if you enabled integrity checking.

### Visualize the Huffman Tree
1. Sidebar → **Huffman Tree**.
2. After a compression, the tree for that file is shown automatically.
3. Or, use **Demo Mode**: type a string (e.g. `ABRACADABRA`) and click
   **Build Tree** to see its tree and code table instantly.
4. Scroll to pan, use the mouse wheel to zoom, or click **Fit to Screen**.

### View statistics
Sidebar → **Statistics** — shows the full metrics dashboard for the most
recent compression, plus a size-comparison bar chart.

---

## 12. Complexity Analysis

Let `n` = number of input bytes, `k` = number of distinct byte values
(`k ≤ 256`), `m` = number of encoded bits.

| Operation                | Time complexity | Notes |
|---------------------------|-----------------|-------|
| Frequency counting         | O(n)            | single pass over the file |
| Building the Huffman tree | O(k log k)      | k−1 heap pop/push pairs, each O(log k) |
| Generating codes           | O(k)            | tree has at most 2k−1 nodes |
| Encoding                   | O(n)            | one code lookup + bit-write per byte |
| Decoding                   | O(m)            | one tree step per bit; m = O(n) in practice |
| SHA-256 verification       | O(n)            | one pass per file |

**Space complexity:** O(k) for the tree and code table, O(1) additional
buffered memory during streaming encode/decode (chunked I/O), independent
of file size.

**Computer Architecture relevance:** compression trades extra CPU cycles
(building the tree, encoding/decoding bits) for fewer bytes moved through
memory, storage, and I/O buses — illustrating the classic time/space and
compute/bandwidth trade-off central to system design.

---

## 13. Testing

Run the full correctness suite (10 cases: empty file, single-byte file,
small text, large text, skewed "binary" data, fully random data, repeated
patterns, all 256 byte values, two-unique-byte file, tiny single-byte
file). Each case compresses, decompresses, and checks `original ==
decompressed` plus SHA-256 equality:

```bash
python -m tests.test_core
```

There is also an end-to-end GUI smoke test that drives the actual
application widgets (file selection, threaded compression/decompression,
tree visualization, statistics, Demo Mode) headlessly:

```bash
python -m tests.gui_smoke_test
```

---

## 14. Limitations

- Decompression currently loads the compressed payload into memory in one
  read (the *original* file is streamed in chunks during compression, and
  output is streamed in chunks during decompression, but the compressed
  bytes themselves are read as one block). For files where the compressed
  size is very large (multi-GB), this could be optimized further.
- The frequency table stores one 9-byte entry per distinct byte, so very
  tiny files can end up larger after "compression" — this is expected and
  explained in-app (header/metadata overhead can exceed the savings when
  there isn't enough redundancy to exploit).
- Only one file can be compressed/decompressed at a time (no batch mode).

## 15. Future Improvements

- Fully streaming decompression (bounded memory even for huge `.huff` files)
- Batch compression of multiple files / folders
- Canonical Huffman codes to shrink the stored code-length metadata further
- Drag-and-drop file selection
- Adaptive/dynamic Huffman coding (single-pass, no stored frequency table)

## 16. Screenshots

*(Add screenshots here when preparing your submission)*

- `docs/screenshots/dashboard.png`
- `docs/screenshots/compress.png`
- `docs/screenshots/tree.png`
- `docs/screenshots/statistics.png`
- `docs/screenshots/decompress.png`

## 17. Academic Project Information

- **Project Title:** Efficient File Compression and Decompression Using
  Huffman Coding Algorithm
- **Course:** Computer Architecture
- **Technology:** Python 3 + CustomTkinter
- **Algorithm:** Huffman Coding (greedy algorithm, min-heap, binary
  prefix-free tree)
- **Developed for:** University Academic Project
