"""Scaffolding and Environment Verification Tests for MedCrypt-Vault."""

import json
from pathlib import Path
import pytest


def test_core_dependencies_importable():
    """Verify all heavy signal processing, cryptographic, and API libraries import cleanly."""
    import numpy as np
    import pywt
    import cv2
    import cryptography
    import pydantic
    import fastapi
    import scipy
    import skimage

    assert np.__version__ is not None
    assert pywt.__version__ is not None
    assert cv2.__version__ is not None
    assert cryptography.__version__ is not None
    assert pydantic.__version__ is not None
    assert fastapi.__version__ is not None
    assert scipy.__version__ is not None
    assert skimage.__version__ is not None


def test_sample_patient_record_valid():
    """Verify sample EHR JSON is well-formed and contains required clinical keys."""
    sample_path = (
        Path(__file__).resolve().parent.parent
        / "sample_data"
        / "patient_records"
        / "sample_ehr_01.json"
    )
    assert sample_path.exists(), f"Sample record not found at {sample_path}"

    with open(sample_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "patient_identity" in data
    assert "clinical_records" in data
    assert data["patient_identity"]["nik"] == "3175061904990003"
    assert "Chest X-Ray" in data["clinical_records"]["exam_type"]


def test_sample_synthetic_xray_valid():
    """Verify synthetic medical chest phantom image exists and has valid properties."""
    import cv2

    img_path = (
        Path(__file__).resolve().parent.parent
        / "sample_data"
        / "medical_images"
        / "chest_xray_512.png"
    )
    assert img_path.exists(), f"Synthetic X-Ray image not found at {img_path}"

    img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
    assert img is not None
    assert img.shape == (512, 512)
    assert img.dtype.name == "uint8"
    assert img.min() >= 0
    assert img.max() <= 255


def test_custom_exceptions():
    """Verify domain exceptions can be raised and carry details."""
    from backend.core.exceptions import (
        MedCryptError,
        CapacityExceededError,
        AuthenticationFailedError,
        CorruptFrameHeaderError,
    )

    err = CapacityExceededError("Payload too large", details={"capacity": 100, "required": 150})
    assert isinstance(err, MedCryptError)
    assert err.details["capacity"] == 100
