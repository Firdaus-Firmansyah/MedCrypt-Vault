"""Canonical Huffman Coding Engine (Modul 3 & 4).

Implements:
- Min-Heap Priority Queue for binary prefix tree construction
- Mathematical Prefix Property verification
- Canonical Huffman Transformation (RFC 1951 style):
  * Code lengths are sorted by length ascending, then lexicographically by symbol
  * Deterministic canonical code derivation: code = (prev_code + 1) << (curr_len - prev_len)
- Compact canonical header serialization
- Bit-level stream packer and unpacker
"""

import heapq
from collections import Counter
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass(order=True)
class HuffmanNode:
    """Node in the Huffman prefix tree, orderable by frequency for min-heap."""
    freq: int
    symbol: Optional[int] = field(compare=False, default=None)
    left: Optional["HuffmanNode"] = field(compare=False, default=None)
    right: Optional["HuffmanNode"] = field(compare=False, default=None)

    @property
    def is_leaf(self) -> bool:
        return self.left is None and self.right is None


class CanonicalHuffman:
    """Pure Python Canonical Huffman Encoder and Decoder."""

    @staticmethod
    def verify_prefix_property(codebook: Dict[int, str]) -> bool:
        """Verifies mathematically that no codeword is a prefix of another codeword."""
        codes = list(codebook.values())
        for i, c1 in enumerate(codes):
            for j, c2 in enumerate(codes):
                if i != j and c2.startswith(c1):
                    return False
        return True

    @staticmethod
    def build_tree_lengths(data: bytes) -> Dict[int, int]:
        """Builds standard Huffman tree and extracts codeword lengths for each symbol."""
        if not data:
            return {}

        counts = Counter(data)
        if len(counts) == 1:
            # Single symbol corner case: 1 bit length
            sym = next(iter(counts))
            return {sym: 1}

        # Min-heap priority queue
        heap: List[HuffmanNode] = [
            HuffmanNode(freq=cnt, symbol=sym) for sym, cnt in counts.items()
        ]
        heapq.heapify(heap)

        while len(heap) > 1:
            n1 = heapq.heappop(heap)
            n2 = heapq.heappop(heap)
            parent = HuffmanNode(freq=n1.freq + n2.freq, left=n1, right=n2)
            heapq.heappush(heap, parent)

        root = heap[0]
        lengths: Dict[int, int] = {}

        def traverse(node: HuffmanNode, depth: int) -> None:
            if node.is_leaf:
                lengths[node.symbol] = depth
                return
            if node.left:
                traverse(node.left, depth + 1)
            if node.right:
                traverse(node.right, depth + 1)

        traverse(root, 0)
        return lengths

    @classmethod
    def generate_canonical_codes(cls, lengths: Dict[int, int]) -> Dict[int, str]:
        """Derives Canonical Huffman codewords from symbol lengths.

        Algorithm:
        1. Sort symbols by length (ascending), then by symbol byte value (ascending).
        2. First symbol gets integer code 0.
        3. Next code: (prev_code + 1) << (curr_len - prev_len).
        """
        if not lengths:
            return {}

        # Sort: primary key = length, secondary key = symbol byte value
        sorted_symbols = sorted(lengths.keys(), key=lambda s: (lengths[s], s))

        canonical_codes: Dict[int, str] = {}
        code = 0
        prev_len = lengths[sorted_symbols[0]]

        # Assign first symbol code
        canonical_codes[sorted_symbols[0]] = format(code, f"0{prev_len}b")

        for sym in sorted_symbols[1:]:
            curr_len = lengths[sym]
            code = (code + 1) << (curr_len - prev_len)
            canonical_codes[sym] = format(code, f"0{curr_len}b")
            prev_len = curr_len

        # Mathematically verify prefix property
        assert cls.verify_prefix_property(canonical_codes), "Canonical code prefix property violation!"
        return canonical_codes

    def encode(self, data: bytes) -> bytes:
        """Encodes raw byte sequence into canonical Huffman compressed byte stream.

        Binary Package Layout:
        - Original Length (4 bytes uint32 big-endian)
        - Alphabet Count M (2 bytes uint16 big-endian, 1..256)
        - M pairs of:
            * Symbol (1 byte uint8)
            * Bit Length (1 byte uint8)
        - Bitstream: packed bit sequences
        """
        if not data:
            return b""

        orig_len = len(data)
        lengths = self.build_tree_lengths(data)
        canonical_codes = self.generate_canonical_codes(lengths)

        # 1. Build Header
        header = bytearray()
        header.extend(orig_len.to_bytes(4, "big"))
        header.extend(len(lengths).to_bytes(2, "big"))

        # Sort symbols for deterministic serialization
        sorted_symbols = sorted(lengths.keys(), key=lambda s: (lengths[s], s))
        for sym in sorted_symbols:
            header.append(sym)
            header.append(lengths[sym])

        # 2. Build Bitstream
        # Concatenate bit strings
        bit_chunks: List[str] = [canonical_codes[b] for b in data]
        all_bits = "".join(bit_chunks)

        # Pack bits into bytes
        payload = bytearray()
        for i in range(0, len(all_bits), 8):
            byte_bits = all_bits[i : i + 8]
            # Pad last byte with zeros if needed
            if len(byte_bits) < 8:
                byte_bits = byte_bits.ljust(8, "0")
            payload.append(int(byte_bits, 2))

        return bytes(header + payload)

    def decode(self, package: bytes) -> bytes:
        """Decompresses a canonical Huffman package back to exact original bytes."""
        if not package:
            return b""

        if len(package) < 6:
            raise ValueError("Corrupt Huffman package: Header too short.")

        # 1. Parse Header
        orig_len = int.from_bytes(package[0:4], "big")
        alpha_count = int.from_bytes(package[4:6], "big")

        header_len = 6 + (alpha_count * 2)
        if len(package) < header_len:
            raise ValueError("Corrupt Huffman package: Incomplete alphabet table.")

        lengths: Dict[int, int] = {}
        idx = 6
        for _ in range(alpha_count):
            sym = package[idx]
            l = package[idx + 1]
            lengths[sym] = l
            idx += 2

        # 2. Reconstruct Canonical Codes directly from lengths
        canonical_codes = self.generate_canonical_codes(lengths)
        reverse_map = {code: sym for sym, code in canonical_codes.items()}

        # 3. Read bitstream and decode
        bitstream_bytes = package[header_len:]
        out = bytearray()
        current_code = ""

        decoded_count = 0
        for b in bitstream_bytes:
            # Unpack 8 bits from byte
            bits = format(b, "08b")
            for bit in bits:
                current_code += bit
                if current_code in reverse_map:
                    out.append(reverse_map[current_code])
                    current_code = ""
                    decoded_count += 1
                    if decoded_count == orig_len:
                        break
            if decoded_count == orig_len:
                break

        if len(out) != orig_len:
            raise ValueError(f"Decompression size mismatch: expected {orig_len}, got {len(out)}")

        return bytes(out)
