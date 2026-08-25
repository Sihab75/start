"""
core/huffman.py
================
A from-scratch, manual implementation of the Huffman Coding algorithm.

This module intentionally does NOT use any built-in compression library
(zipfile, gzip, bz2, lzma, zlib). It only uses `heapq` as a priority
queue (min-heap) to implement the classic greedy Huffman tree-building
algorithm.

Classes
-------
HuffmanNode   - a single node of the Huffman binary tree.
HuffmanTree   - builds the tree from a frequency table and produces the
                canonical byte -> bitstring code mapping.
BitWriter     - packs a stream of individual bits into bytes (MSB first).
BitReader     - unpacks bits from bytes (MSB first), aware of padding.

Time complexity
----------------
Let k = number of distinct byte values (k <= 256).

- Building the tree: O(k log k)   (k-1 heap pops/pushes, each O(log k))
- Generating codes:  O(k)          (tree has at most 2k - 1 nodes)
"""

from __future__ import annotations

import heapq
from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class HuffmanNode:
    """
    A node in the Huffman tree.

    `byte` is not None only for leaf nodes (it holds the actual byte
    value, 0-255). Internal nodes have `byte = None` and two children.

    `order` is a strictly increasing tie-breaker used so that nodes with
    equal frequency compare deterministically. This guarantees that the
    compressor and decompressor - given the same frequency table and the
    same construction order - always build an *identical* tree, which is
    essential for correct decoding.
    """

    freq: int
    byte: Optional[int] = None
    order: int = 0
    left: Optional["HuffmanNode"] = None
    right: Optional["HuffmanNode"] = None

    def is_leaf(self) -> bool:
        return self.left is None and self.right is None

    def __lt__(self, other: "HuffmanNode") -> bool:
        # heapq needs a total order. Compare by frequency first, then by
        # the deterministic insertion order to break ties.
        if self.freq != other.freq:
            return self.freq < other.freq
        return self.order < other.order


class HuffmanTree:
    """
    Builds a Huffman tree from a byte-frequency table and exposes the
    resulting prefix-free binary codes.
    """

    def __init__(self, frequency_table: Dict[int, int]):
        if not frequency_table:
            raise ValueError("Cannot build a Huffman tree from an empty frequency table")
        self.frequency_table = frequency_table
        self.root: HuffmanNode = self._build_tree(frequency_table)
        self.codes: Dict[int, str] = {}
        self._generate_codes(self.root, "")

    @staticmethod
    def _build_tree(frequency_table: Dict[int, int]) -> HuffmanNode:
        """
        Classic greedy Huffman construction using a min-heap:

        1. Create a leaf node for every distinct byte.
        2. Repeatedly pop the two lowest-frequency nodes, merge them into
           a new internal node whose frequency is the sum, and push it
           back onto the heap.
        3. Stop when only one node (the root) remains.

        Special case: if there is only ONE distinct byte value, a
        single-leaf "tree" would produce an empty code (0 bits), which is
        invalid for a prefix code. We fix this by wrapping the single
        leaf under a dummy root so that the leaf is still reachable via a
        single '0' bit.
        """
        heap: list[HuffmanNode] = []
        counter = 0
        for byte_value in sorted(frequency_table.keys()):
            heapq.heappush(
                heap, HuffmanNode(freq=frequency_table[byte_value], byte=byte_value, order=counter)
            )
            counter += 1

        if len(heap) == 1:
            only_leaf = heapq.heappop(heap)
            dummy_root = HuffmanNode(freq=only_leaf.freq, byte=None, order=counter, left=only_leaf, right=None)
            return dummy_root

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            merged = HuffmanNode(freq=left.freq + right.freq, byte=None, order=counter, left=left, right=right)
            counter += 1
            heapq.heappush(heap, merged)

        return heap[0]

    def _generate_codes(self, node: Optional[HuffmanNode], prefix: str) -> None:
        """Recursively walk the tree; left edges add '0', right edges add '1'."""
        if node is None:
            return
        if node.is_leaf():
            # A root that is itself a leaf (single-symbol file, without the
            # dummy-root wrapping) would get an empty code; guard against it.
            self.codes[node.byte] = prefix if prefix else "0"
            return
        self._generate_codes(node.left, prefix + "0")
        self._generate_codes(node.right, prefix + "1")

    def average_code_length(self) -> float:
        """Weighted average code length in bits, weighted by frequency."""
        total_freq = sum(self.frequency_table.values())
        if total_freq == 0:
            return 0.0
        weighted_sum = sum(self.frequency_table[b] * len(self.codes[b]) for b in self.frequency_table)
        return weighted_sum / total_freq

    def max_code_length(self) -> int:
        return max((len(c) for c in self.codes.values()), default=0)


class BitWriter:
    """
    Accumulates individual bits (0/1) and packs them into bytes, most
    significant bit first. Call `finish()` at the end to flush any
    partial trailing byte (zero-padded) and learn how many padding bits
    were added.
    """

    def __init__(self):
        self._buffer = bytearray()
        self._current_byte = 0
        self._bit_count = 0

    def write_bit(self, bit: int) -> None:
        self._current_byte = (self._current_byte << 1) | (bit & 1)
        self._bit_count += 1
        if self._bit_count == 8:
            self._buffer.append(self._current_byte)
            self._current_byte = 0
            self._bit_count = 0

    def write_bits(self, bitstring: str) -> None:
        for ch in bitstring:
            self.write_bit(1 if ch == "1" else 0)

    def take_bytes(self) -> bytes:
        """Return and clear whatever complete bytes have been accumulated so far."""
        data = bytes(self._buffer)
        self._buffer.clear()
        return data

    def finish(self) -> tuple[bytes, int]:
        """
        Flush the final (possibly partial) byte, left-padded... actually
        left-justified with zero bits on the right, and return
        (remaining_bytes, padding_bit_count).
        """
        padding = 0
        if self._bit_count > 0:
            padding = 8 - self._bit_count
            self._current_byte <<= padding
            self._buffer.append(self._current_byte)
            self._current_byte = 0
            self._bit_count = 0
        data = bytes(self._buffer)
        self._buffer.clear()
        return data, padding


class BitReader:
    """
    Reads individual bits (most significant bit first) from a bytes
    buffer, aware of how many trailing padding bits should be ignored.
    """

    def __init__(self, data: bytes, padding_bits: int = 0):
        self.data = data
        self.total_bits = len(data) * 8 - padding_bits
        self.pos = 0

    def has_more(self) -> bool:
        return self.pos < self.total_bits

    def read_bit(self) -> Optional[int]:
        if self.pos >= self.total_bits:
            return None
        byte_index = self.pos // 8
        bit_index = 7 - (self.pos % 8)
        bit = (self.data[byte_index] >> bit_index) & 1
        self.pos += 1
        return bit
