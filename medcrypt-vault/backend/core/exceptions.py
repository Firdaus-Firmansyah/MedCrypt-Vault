"""Custom domain exceptions for MedCrypt-Vault.

Clean, explicit exception hierarchy mapping cleanly to RFC 7807 problem details.
"""


class MedCryptError(Exception):
    """Base exception for all MedCrypt-Vault domain errors."""

    def __init__(self, message: str, details: dict | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}


class CapacityExceededError(MedCryptError):
    """Raised when the compressed payload length exceeds cover image capacity."""
    pass


class AuthenticationFailedError(MedCryptError):
    """Raised when decryption fails due to invalid secret passphrase or tampered data."""
    pass


class CorruptFrameHeaderError(MedCryptError):
    """Raised when extracted binary stream does not match the MCVT magic header."""
    pass


class CompressionError(MedCryptError):
    """Raised when LZ77 or Huffman compression/decompression fails."""
    pass


class InvalidImageFormatError(MedCryptError):
    """Raised when cover image format, channels, or dimensions are invalid."""
    pass
