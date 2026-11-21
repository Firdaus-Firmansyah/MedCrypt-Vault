"""Adaptive Two-stage Hybrid Compression Pipeline: LZ77 + Canonical Huffman.

Stage 1: LZ77 Sliding Window (32 KB Search Buffer, Hash Chaining) removes long repeated patterns.
Stage 2: Canonical Huffman Coding (Min-Heap, Prefix Free) removes symbol frequency redundancy.

Adaptively selects the most compact encoding scheme:
- Mode 0x01: LZ77 + Canonical Huffman (Best for repetitive text, JSON, logs, >4 KB)
- Mode 0x02: Pure Canonical Huffman (Best for short texts with symbol frequency skew)
- Mode 0x03: Pure Packed LZ77 (When Huffman tree overhead exceeds savings)
- Mode 0x00: Raw Passthrough (When payload is already high-entropy random data)

Guarantees 100% exact lossless reconstruction (BER = 0.00%).
"""

from typing import Tuple, Dict, Any, List
from .entropy import calculate_shannon_entropy, evaluate_compression, CompressionMetrics
from .lz77 import LZ77Compressor
from .huffman import CanonicalHuffman


class HybridCompressor:
    """Orchestrates adaptive LZ77 + Canonical Huffman compression pipeline."""

    def __init__(
        self,
        search_window: int = LZ77Compressor.DEFAULT_SEARCH_WINDOW,
        lookahead_window: int = LZ77Compressor.DEFAULT_LOOKAHEAD_WINDOW,
    ) -> None:
        self.lz77 = LZ77Compressor(search_window=search_window, lookahead_window=lookahead_window)
        self.huffman = CanonicalHuffman()

    def compress(self, raw_data: bytes) -> Tuple[bytes, CompressionMetrics]:
        """Compresses raw bytes through the adaptive pipeline.

        Returns:
            Tuple[bytes, CompressionMetrics]: (compressed_package, metrics)
        """
        if not raw_data:
            return b"", {
                "original_size_bytes": 0,
                "compressed_size_bytes": 0,
                "compression_ratio": 1.0,
                "space_saving_percent": 0.0,
                "original_entropy": 0.0,
                "compressed_entropy": 0.0,
            }

        candidates: List[Tuple[int, bytes]] = []

        # Candidate 0: Raw fallback
        candidates.append((0x00, raw_data))

        # Candidate 1: Pure Huffman
        try:
            huff_raw = self.huffman.encode(raw_data)
            candidates.append((0x02, huff_raw))
        except Exception:
            pass

        # Candidate 2: Pure LZ77
        try:
            lz_packed = self.lz77.compress(raw_data)
            candidates.append((0x03, lz_packed))

            # Candidate 3: LZ77 + Huffman
            huff_on_lz = self.huffman.encode(lz_packed)
            candidates.append((0x01, huff_on_lz))
        except Exception:
            pass

        # Pick candidate with minimum length (including 1-byte mode flag)
        best_mode, best_payload = min(candidates, key=lambda c: len(c[1]))
        final_package = bytes([best_mode]) + best_payload

        metrics = evaluate_compression(raw_data, final_package)
        return final_package, metrics

    def decompress(self, package: bytes) -> bytes:
        """Decompresses package back to original raw bytes."""
        if not package:
            return b""

        mode = package[0]
        body = package[1:]

        if mode == 0x01:
            # Mode 1: Huffman decode -> LZ77 decompress
            lz77_stream = self.huffman.decode(body)
            return self.lz77.decompress(lz77_stream)
        elif mode == 0x02:
            # Mode 2: Pure Huffman decode
            return self.huffman.decode(body)
        elif mode == 0x03:
            # Mode 3: Pure LZ77 decompress
            return self.lz77.decompress(body)
        elif mode == 0x00:
            # Mode 0: Raw bytes
            return body
        else:
            raise ValueError(f"Unknown compression pipeline mode flag: 0x{mode:02X}")


# Global singleton instance for easy import
default_compressor = HybridCompressor()


def compress_payload(raw_data: bytes) -> Tuple[bytes, CompressionMetrics]:
    """Helper function to compress byte payload using default hybrid engine."""
    return default_compressor.compress(raw_data)


def decompress_payload(package: bytes) -> bytes:
    """Helper function to decompress hybrid package back to exact bytes."""
    return default_compressor.decompress(package)
