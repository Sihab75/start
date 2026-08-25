"""
tests/test_core.py
===================
Correctness test suite for the Huffman compression core.

For every test case this verifies:
    1. compress() succeeds
    2. decompress() succeeds
    3. original bytes == decompressed bytes (byte-for-byte)
    4. SHA-256(original) == SHA-256(decompressed)

Run with:
    python -m tests.test_core
"""

from __future__ import annotations

import os
import random
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.compressor import HuffmanCompressor
from core.decompressor import HuffmanDecompressor
from core.utils import compute_sha256, format_size


def run_case(name: str, data: bytes, workdir: str) -> bool:
    original_path = os.path.join(workdir, f"{name}.bin")
    compressed_path = os.path.join(workdir, f"{name}.huff")
    restored_path = os.path.join(workdir, f"{name}.restored")

    with open(original_path, "wb") as f:
        f.write(data)

    compressor = HuffmanCompressor()
    stats = compressor.compress(original_path, compressed_path)

    decompressor = HuffmanDecompressor()
    dstats = decompressor.decompress(compressed_path, restored_path)

    with open(original_path, "rb") as f:
        original_bytes = f.read()
    with open(restored_path, "rb") as f:
        restored_bytes = f.read()

    bytes_match = original_bytes == restored_bytes
    hash_match = compute_sha256(original_path) == compute_sha256(restored_path)

    ok = bytes_match and hash_match
    status = "PASS" if ok else "FAIL"
    ratio = f"{stats.compression_ratio_percent:.2f}%" if stats.original_size else "n/a"
    print(
        f"[{status}] {name:28s} orig={format_size(stats.original_size):>10s}  "
        f"comp={format_size(stats.compressed_size):>10s}  ratio={ratio:>8s}  "
        f"bytes_match={bytes_match}  sha256_match={hash_match}"
    )
    return ok


def main() -> int:
    workdir = tempfile.mkdtemp(prefix="huffman_test_")
    print(f"Working directory: {workdir}\n")
    random.seed(42)

    cases = {}

    # 1. Empty file
    cases["empty_file"] = b""

    # 2. Single-character file (single unique byte, repeated)
    cases["single_char"] = b"A" * 500

    # 3. Small text file
    cases["small_text"] = b"ABRACADABRA"

    # 4. Larger text file (natural language-like distribution)
    sample_sentence = (
        b"the quick brown fox jumps over the lazy dog. "
        b"the five boxing wizards jump quickly. "
    )
    cases["large_text"] = sample_sentence * 2000

    # 5. "Binary file" simulation - pseudo-random bytes with skewed distribution
    skewed = bytearray()
    for _ in range(200_000):
        skewed.append(random.choice([0, 0, 0, 1, 2, 255, 254, 128, 64, 10]))
    cases["binary_skewed"] = bytes(skewed)

    # 6. Fully random data (worst case for compression, must still round-trip)
    cases["random_data"] = bytes(random.randint(0, 255) for _ in range(100_000))

    # 7. Repeated pattern data
    cases["repeated_pattern"] = (b"XY" * 50 + b"Z" * 10) * 1000

    # 8. All 256 possible byte values, each appearing multiple times
    all_bytes = bytearray()
    for _ in range(50):
        all_bytes.extend(range(256))
    cases["all_256_values"] = bytes(all_bytes)

    # 9. Two unique bytes only
    cases["two_unique_bytes"] = b"01" * 10000

    # 10. Single byte, single occurrence
    cases["tiny_single_byte"] = b"Q"

    all_passed = True
    for name, data in cases.items():
        try:
            passed = run_case(name, data, workdir)
        except Exception as exc:  # noqa: BLE001
            print(f"[FAIL] {name:28s} raised an exception: {exc}")
            passed = False
        all_passed = all_passed and passed

    shutil.rmtree(workdir, ignore_errors=True)

    print()
    if all_passed:
        print("ALL TESTS PASSED ✔")
    else:
        print("SOME TESTS FAILED ✘")
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

"""
tests/test_core.py
===================
Correctness test suite for the Huffman compression core.

For every test case this verifies:
    1. compress() succeeds
    2. decompress() succeeds
    3. original bytes == decompressed bytes (byte-for-byte)
    4. SHA-256(original) == SHA-256(decompressed)

Run with:
    python -m tests.test_core
"""

from __future__ import annotations

import os
import random
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.compressor import HuffmanCompressor
from core.decompressor import HuffmanDecompressor
from core.utils import compute_sha256, format_size


def run_case(name: str, data: bytes, workdir: str) -> bool:
    original_path = os.path.join(workdir, f"{name}.bin")
    compressed_path = os.path.join(workdir, f"{name}.huff")
    restored_path = os.path.join(workdir, f"{name}.restored")

    with open(original_path, "wb") as f:
        f.write(data)

    compressor = HuffmanCompressor()
    stats = compressor.compress(original_path, compressed_path)

    decompressor = HuffmanDecompressor()
    dstats = decompressor.decompress(compressed_path, restored_path)

    with open(original_path, "rb") as f:
        original_bytes = f.read()
    with open(restored_path, "rb") as f:
        restored_bytes = f.read()

    bytes_match = original_bytes == restored_bytes
    hash_match = compute_sha256(original_path) == compute_sha256(restored_path)

    ok = bytes_match and hash_match
    status = "PASS" if ok else "FAIL"
    ratio = f"{stats.compression_ratio_percent:.2f}%" if stats.original_size else "n/a"
    print(
        f"[{status}] {name:28s} orig={format_size(stats.original_size):>10s}  "
        f"comp={format_size(stats.compressed_size):>10s}  ratio={ratio:>8s}  "
        f"bytes_match={bytes_match}  sha256_match={hash_match}"
    )
    return ok


def main() -> int:
    workdir = tempfile.mkdtemp(prefix="huffman_test_")
    print(f"Working directory: {workdir}\n")
    random.seed(42)

    cases = {}

    # 1. Empty file
    cases["empty_file"] = b""

    # 2. Single-character file (single unique byte, repeated)
    cases["single_char"] = b"A" * 500

    # 3. Small text file
    cases["small_text"] = b"ABRACADABRA"

    # 4. Larger text file (natural language-like distribution)
    sample_sentence = (
        b"the quick brown fox jumps over the lazy dog. "
        b"the five boxing wizards jump quickly. "
    )
    cases["large_text"] = sample_sentence * 2000

    # 5. "Binary file" simulation - pseudo-random bytes with skewed distribution
    skewed = bytearray()
    for _ in range(200_000):
        skewed.append(random.choice([0, 0, 0, 1, 2, 255, 254, 128, 64, 10]))
    cases["binary_skewed"] = bytes(skewed)

    # 6. Fully random data (worst case for compression, must still round-trip)
    cases["random_data"] = bytes(random.randint(0, 255) for _ in range(100_000))

    # 7. Repeated pattern data
    cases["repeated_pattern"] = (b"XY" * 50 + b"Z" * 10) * 1000

    # 8. All 256 possible byte values, each appearing multiple times
    all_bytes = bytearray()
    for _ in range(50):
        all_bytes.extend(range(256))
    cases["all_256_values"] = bytes(all_bytes)

    # 9. Two unique bytes only
    cases["two_unique_bytes"] = b"01" * 10000

    # 10. Single byte, single occurrence
    cases["tiny_single_byte"] = b"Q"

    all_passed = True
    for name, data in cases.items():
        try:
            passed = run_case(name, data, workdir)
        except Exception as exc:  # noqa: BLE001
            print(f"[FAIL] {name:28s} raised an exception: {exc}")
            passed = False
        all_passed = all_passed and passed

    shutil.rmtree(workdir, ignore_errors=True)

    print()
    if all_passed:
        print("ALL TESTS PASSED ✔")
    else:
        print("SOME TESTS FAILED ✘")
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

"""
tests/test_core.py
===================
Correctness test suite for the Huffman compression core.

For every test case this verifies:
    1. compress() succeeds
    2. decompress() succeeds
    3. original bytes == decompressed bytes (byte-for-byte)
    4. SHA-256(original) == SHA-256(decompressed)

Run with:
    python -m tests.test_core
"""

from __future__ import annotations

import os
import random
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.compressor import HuffmanCompressor
from core.decompressor import HuffmanDecompressor
from core.utils import compute_sha256, format_size


def run_case(name: str, data: bytes, workdir: str) -> bool:
    original_path = os.path.join(workdir, f"{name}.bin")
    compressed_path = os.path.join(workdir, f"{name}.huff")
    restored_path = os.path.join(workdir, f"{name}.restored")

    with open(original_path, "wb") as f:
        f.write(data)

    compressor = HuffmanCompressor()
    stats = compressor.compress(original_path, compressed_path)

    decompressor = HuffmanDecompressor()
    dstats = decompressor.decompress(compressed_path, restored_path)

    with open(original_path, "rb") as f:
        original_bytes = f.read()
    with open(restored_path, "rb") as f:
        restored_bytes = f.read()

    bytes_match = original_bytes == restored_bytes
    hash_match = compute_sha256(original_path) == compute_sha256(restored_path)

    ok = bytes_match and hash_match
    status = "PASS" if ok else "FAIL"
    ratio = f"{stats.compression_ratio_percent:.2f}%" if stats.original_size else "n/a"
    print(
        f"[{status}] {name:28s} orig={format_size(stats.original_size):>10s}  "
        f"comp={format_size(stats.compressed_size):>10s}  ratio={ratio:>8s}  "
        f"bytes_match={bytes_match}  sha256_match={hash_match}"
    )
    return ok


def main() -> int:
    workdir = tempfile.mkdtemp(prefix="huffman_test_")
    print(f"Working directory: {workdir}\n")
    random.seed(42)

    cases = {}

    # 1. Empty file
    cases["empty_file"] = b""

    # 2. Single-character file (single unique byte, repeated)
    cases["single_char"] = b"A" * 500

    # 3. Small text file
    cases["small_text"] = b"ABRACADABRA"

    # 4. Larger text file (natural language-like distribution)
    sample_sentence = (
        b"the quick brown fox jumps over the lazy dog. "
        b"the five boxing wizards jump quickly. "
    )
    cases["large_text"] = sample_sentence * 2000

    # 5. "Binary file" simulation - pseudo-random bytes with skewed distribution
    skewed = bytearray()
    for _ in range(200_000):
        skewed.append(random.choice([0, 0, 0, 1, 2, 255, 254, 128, 64, 10]))
    cases["binary_skewed"] = bytes(skewed)

    # 6. Fully random data (worst case for compression, must still round-trip)
    cases["random_data"] = bytes(random.randint(0, 255) for _ in range(100_000))

    # 7. Repeated pattern data
    cases["repeated_pattern"] = (b"XY" * 50 + b"Z" * 10) * 1000

    # 8. All 256 possible byte values, each appearing multiple times
    all_bytes = bytearray()
    for _ in range(50):
        all_bytes.extend(range(256))
    cases["all_256_values"] = bytes(all_bytes)

    # 9. Two unique bytes only
    cases["two_unique_bytes"] = b"01" * 10000

    # 10. Single byte, single occurrence
    cases["tiny_single_byte"] = b"Q"

    all_passed = True
    for name, data in cases.items():
        try:
            passed = run_case(name, data, workdir)
        except Exception as exc:  # noqa: BLE001
            print(f"[FAIL] {name:28s} raised an exception: {exc}")
            passed = False
        all_passed = all_passed and passed

    shutil.rmtree(workdir, ignore_errors=True)

    print()
    if all_passed:
        print("ALL TESTS PASSED ✔")
    else:
        print("SOME TESTS FAILED ✘")
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
