"""Shannon Entropy and Information Theory Metrics (Modul 1 & 2).

Calculates:
- Theoretical Shannon Entropy H(S) in bits/symbol
- Image spatial entropy for 8-bit grayscale medical radiographs
- Compression metrics (Compression Ratio, Space Saving, Redundancy)
"""

import math
from collections import Counter
from typing import TypedDict
import numpy as np


class CompressionMetrics(TypedDict):
    original_size_bytes: int
    compressed_size_bytes: int
    compression_ratio: float
    space_saving_percent: float
    original_entropy: float
    compressed_entropy: float


def calculate_shannon_entropy(data: bytes) -> float:
    """Calculates the theoretical Shannon Entropy of a byte sequence.

    Formula:
        H(S) = - SUM( p(s_i) * log2(p(s_i)) )

    Args:
        data (bytes): Input byte array.

    Returns:
        float: Entropy value in bits per byte (0.0 to 8.0).

    Raises:
        ValueError: If input byte sequence is empty.

    Example:
        >>> calculate_shannon_entropy(b"AAAA")
        0.0
    """
    if not data:
        raise ValueError("Cannot calculate entropy of an empty byte array.")

    total_len = len(data)
    counts = Counter(data)

    entropy = 0.0
    for count in counts.values():
        p = count / total_len
        if p > 0.0:
            entropy -= p * math.log2(p)

    return float(entropy)


def calculate_image_entropy(image: np.ndarray) -> float:
    """Calculates the first-order Shannon Entropy of a 2D grayscale image.

    Args:
        image (np.ndarray): 2D numpy array of uint8 pixels (e.g. 512x512 X-Ray).

    Returns:
        float: Entropy in bits per pixel (0.0 to 8.0).

    Raises:
        ValueError: If input image is empty or has invalid dimensions.
    """
    if image is None or image.size == 0:
        raise ValueError("Image array is empty.")

    # Flatten image to 1D
    flat = image.ravel()
    hist, _ = np.histogram(flat, bins=256, range=(0, 256))
    prob = hist / hist.sum()

    # Filter non-zero probabilities
    non_zero = prob[prob > 0]
    entropy = -np.sum(non_zero * np.log2(non_zero))

    return float(entropy)


def evaluate_compression(original_bytes: bytes, compressed_bytes: bytes) -> CompressionMetrics:
    """Evaluates the efficiency and entropy delta of compression.

    Args:
        original_bytes (bytes): Uncompressed input bytes.
        compressed_bytes (bytes): Output compressed bitstream bytes.

    Returns:
        CompressionMetrics: Structured dictionary with ratios and entropy values.
    """
    orig_len = len(original_bytes)
    comp_len = len(compressed_bytes)

    if orig_len == 0:
        raise ValueError("Original data size cannot be zero.")

    cr = orig_len / comp_len if comp_len > 0 else 0.0
    space_saving = ((orig_len - comp_len) / orig_len) * 100.0

    orig_entropy = calculate_shannon_entropy(original_bytes)
    comp_entropy = calculate_shannon_entropy(compressed_bytes) if comp_len > 0 else 0.0

    return {
        "original_size_bytes": orig_len,
        "compressed_size_bytes": comp_len,
        "compression_ratio": round(cr, 4),
        "space_saving_percent": round(space_saving, 2),
        "original_entropy": round(orig_entropy, 4),
        "compressed_entropy": round(comp_entropy, 4),
    }
