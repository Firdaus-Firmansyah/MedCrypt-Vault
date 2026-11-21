"""Compression engine package."""

from .entropy import (
    calculate_shannon_entropy,
    calculate_image_entropy,
    evaluate_compression,
    CompressionMetrics,
)
from .lz77 import LZ77Compressor, LZ77Token
from .huffman import CanonicalHuffman, HuffmanNode
from .pipeline import (
    HybridCompressor,
    compress_payload,
    decompress_payload,
    default_compressor,
)

__all__ = [
    "calculate_shannon_entropy",
    "calculate_image_entropy",
    "evaluate_compression",
    "CompressionMetrics",
    "LZ77Compressor",
    "LZ77Token",
    "CanonicalHuffman",
    "HuffmanNode",
    "HybridCompressor",
    "compress_payload",
    "decompress_payload",
    "default_compressor",
]
