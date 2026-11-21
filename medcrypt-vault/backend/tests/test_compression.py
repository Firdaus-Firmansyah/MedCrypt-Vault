"""Unit & Integration Test Suite for Compression Engine (Modul 1, 2, 4, 6).

Verifies:
- Shannon Entropy theoretical boundaries [0.0 to 8.0 bits/symbol]
- LZ77 Sliding Window dictionary tokenization and hash-chaining
- Canonical Huffman tree generation and Prefix Property compliance
- Full hybrid pipeline round-trip on medical EHR records with 0.00% BER
"""

import json
from pathlib import Path
import pytest
import numpy as np

from backend.core.compression.entropy import (
    calculate_shannon_entropy,
    calculate_image_entropy,
    evaluate_compression,
)
from backend.core.compression.lz77 import LZ77Compressor, LZ77Token
from backend.core.compression.huffman import CanonicalHuffman
from backend.core.compression.pipeline import (
    HybridCompressor,
    compress_payload,
    decompress_payload,
)


# =====================================================================
# 1. Shannon Entropy Tests (Modul 1 & 2)
# =====================================================================

def test_entropy_zero_for_uniform_data():
    """Entropy must be 0.0 when all symbols are identical."""
    data = b"AAAAAAAAAAAAAAAAAAAA"
    h = calculate_shannon_entropy(data)
    assert h == 0.0


def test_entropy_maximum_for_full_alphabet():
    """Entropy must equal 8.0 bits/byte for a perfectly uniform distribution of 256 bytes."""
    data = bytes(range(256)) * 100
    h = calculate_shannon_entropy(data)
    assert pytest.approx(h, 0.001) == 8.0


def test_entropy_empty_raises_error():
    """Empty data must raise ValueError."""
    with pytest.raises(ValueError):
        calculate_shannon_entropy(b"")


def test_image_entropy():
    """Test entropy computation on 2D image array."""
    # Flat image (zero entropy)
    flat_img = np.full((128, 128), 100, dtype=np.uint8)
    assert calculate_image_entropy(flat_img) == 0.0

    # High entropy random noise image
    noise_img = np.random.randint(0, 256, (128, 128), dtype=np.uint8)
    h_noise = calculate_image_entropy(noise_img)
    assert h_noise > 7.5


# =====================================================================
# 2. Pure LZ77 Compressor Tests (Modul 6)
# =====================================================================

def test_lz77_finds_repetitions():
    """LZ77 should detect repeated sequences and emit Match tokens."""
    compressor = LZ77Compressor(search_window=4096, lookahead_window=256)
    text = b"PATIENT_NAME:AHMAD_PATIENT_NAME:AHMAD_PATIENT_NAME:AHMAD"
    tokens = compressor.tokenize(text)

    # Must contain match tokens
    matches = [t for t in tokens if t.is_match]
    assert len(matches) >= 1
    # Match should capture the repeated phrase
    assert matches[0].length >= 19

    # Untokenize must return exact original string
    restored = compressor.untokenize(tokens)
    assert restored == text


def test_lz77_pack_and_decompress():
    """LZ77 packed binary stream should decompress losslessly."""
    compressor = LZ77Compressor()
    data = b"Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 30

    packed = compressor.compress(data)
    # Compressed packed stream should be significantly smaller than raw repeated text
    assert len(packed) < len(data)

    restored = compressor.decompress(packed, original_size=len(data))
    assert restored == data


def test_lz77_empty_data():
    """LZ77 handles empty bytes cleanly."""
    compressor = LZ77Compressor()
    assert compressor.tokenize(b"") == []
    assert compressor.compress(b"") == b""
    assert compressor.decompress(b"") == b""


# =====================================================================
# 3. Canonical Huffman Tests (Modul 3 & 4)
# =====================================================================

def test_huffman_prefix_property():
    """Canonical Huffman must satisfy the prefix property strictly."""
    data = b"MEDCRYPT_VAULT_FREQUENCY_DOMAIN_STEGANOGRAPHY"
    lengths = CanonicalHuffman.build_tree_lengths(data)
    canonical_codes = CanonicalHuffman.generate_canonical_codes(lengths)

    # Verify no codeword is a prefix of any other codeword
    assert CanonicalHuffman.verify_prefix_property(canonical_codes) is True


def test_canonical_huffman_round_trip():
    """Canonical Huffman encode and decode must return exact bytes."""
    huffman = CanonicalHuffman()
    text = b"The quick brown fox jumps over the lazy dog. 1234567890 !@#$%^&*()" * 10

    encoded = huffman.encode(text)
    decoded = huffman.decode(encoded)
    assert decoded == text


def test_canonical_huffman_single_character():
    """Canonical Huffman handles single-character repetition corner case."""
    huffman = CanonicalHuffman()
    text = b"ZZZZZZZZZZZZZZZZ"
    encoded = huffman.encode(text)
    decoded = huffman.decode(encoded)
    assert decoded == text


# =====================================================================
# 4. Hybrid Pipeline & Medical EHR Dataset Tests
# =====================================================================

def test_hybrid_pipeline_on_ehr_sample():
    """Test full adaptive pipeline on real medical record JSON."""
    sample_path = (
        Path(__file__).resolve().parent.parent
        / "sample_data"
        / "patient_records"
        / "sample_ehr_01.json"
    )
    with open(sample_path, "rb") as f:
        raw_ehr = f.read()

    # 1. Single encounter file
    compressed_package, metrics = compress_payload(raw_ehr)
    assert len(compressed_package) < len(raw_ehr)
    assert metrics["space_saving_percent"] > 25.0

    restored_ehr = decompress_payload(compressed_package)
    assert restored_ehr == raw_ehr

    # 2. Multi-record medical bundle (simulating visit history)
    multi_ehr = raw_ehr * 5
    compressed_multi, metrics_multi = compress_payload(multi_ehr)
    assert metrics_multi["space_saving_percent"] > 75.0
    assert metrics_multi["compression_ratio"] > 4.0

    restored_multi = decompress_payload(compressed_multi)
    assert restored_multi == multi_ehr

    # Verify valid JSON deserialization
    restored_json = json.loads(restored_ehr.decode("utf-8"))
    assert restored_json["patient_identity"]["nik"] == "3175061904990003"
    assert restored_json["clinical_records"]["primary_diagnosis"]["icd10_code"] == "J18.9"


def test_hybrid_pipeline_on_binary_random_bytes():
    """Test hybrid pipeline on high-entropy binary bytes."""
    import os
    random_bytes = os.urandom(2048)

    compressed, _ = compress_payload(random_bytes)
    restored = decompress_payload(compressed)
    assert restored == random_bytes
