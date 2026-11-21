"""LZ77 Sliding Window Dictionary Compression Engine (Modul 6).

Implements:
- 32 KB Search Buffer (W_s = 32,768 bytes)
- 256 B Lookahead Buffer (W_l = 256 bytes)
- Minimum match length = 3 bytes
- Hash-chaining 3-gram index for O(N) average time search
- Binary token pack/unpack using 8-token flag bytes (LZSS-style)
"""

from dataclasses import dataclass
from typing import List, Tuple
from collections import defaultdict


@dataclass(slots=True, frozen=True)
class LZ77Token:
    """Represents a single LZ77 token.

    Either a Literal (is_match=False, literal=byte)
    or a Match (is_match=True, offset=distance, length=count).
    """
    is_match: bool
    offset: int = 0
    length: int = 0
    literal: int = 0

    def __repr__(self) -> str:
        if self.is_match:
            return f"<Match offset={self.offset} len={self.length}>"
        return f"<Literal byte=0x{self.literal:02X} '{chr(self.literal) if 32 <= self.literal <= 126 else '.'}'>"


class LZ77Compressor:
    """Pure Python LZ77 Engine with 32 KB sliding window and hash-chaining."""

    DEFAULT_SEARCH_WINDOW: int = 32768   # 32 KB
    DEFAULT_LOOKAHEAD_WINDOW: int = 256  # 256 B
    MIN_MATCH_LEN: int = 3

    def __init__(
        self,
        search_window: int = DEFAULT_SEARCH_WINDOW,
        lookahead_window: int = DEFAULT_LOOKAHEAD_WINDOW,
        min_match: int = MIN_MATCH_LEN,
    ) -> None:
        self.search_window = min(search_window, 65535)
        self.lookahead_window = min(lookahead_window, 255)
        self.min_match = min_match

    def tokenize(self, data: bytes) -> List[LZ77Token]:
        """Tokenizes a byte sequence into a list of LZ77 tokens using hash chaining."""
        if not data:
            return []

        tokens: List[LZ77Token] = []
        n = len(data)
        pos = 0

        # Hash-chain table: maps 3-byte sequence -> list of occurrences
        # Limits chain length to 32 to guarantee fast O(N) performance
        hash_table = defaultdict(list)
        max_chain = 32

        while pos < n:
            max_len = 0
            best_offset = 0

            # Only search if enough lookahead remains
            if pos + self.min_match <= n:
                triplet = data[pos : pos + 3]
                candidates = hash_table[triplet]

                # Purge occurrences outside sliding window
                min_valid_pos = pos - self.search_window
                valid_candidates = [p for p in candidates if p >= min_valid_pos]
                hash_table[triplet] = valid_candidates

                # Check recent occurrences for longest common match
                max_lookahead = min(self.lookahead_window, n - pos)
                for candidate in reversed(valid_candidates[-max_chain:]):
                    match_len = 0
                    while (
                        match_len < max_lookahead
                        and data[candidate + match_len] == data[pos + match_len]
                    ):
                        match_len += 1

                    if match_len > max_len:
                        max_len = match_len
                        best_offset = pos - candidate
                        if max_len == max_lookahead:
                            break

            # Decide whether to emit Match or Literal
            if max_len >= self.min_match:
                tokens.append(LZ77Token(is_match=True, offset=best_offset, length=max_len))
                # Index the consumed positions into hash table
                for k in range(max_len):
                    if pos + k + 3 <= n:
                        hash_table[data[pos + k : pos + k + 3]].append(pos + k)
                pos += max_len
            else:
                tokens.append(LZ77Token(is_match=False, literal=data[pos]))
                if pos + 3 <= n:
                    hash_table[data[pos : pos + 3]].append(pos)
                pos += 1

        return tokens

    def untokenize(self, tokens: List[LZ77Token]) -> bytes:
        """Reconstructs original byte sequence from a list of LZ77 tokens."""
        out = bytearray()
        for tok in tokens:
            if tok.is_match:
                start = len(out) - tok.offset
                for k in range(tok.length):
                    out.append(out[start + k])
            else:
                out.append(tok.literal)
        return bytes(out)

    def compress(self, data: bytes) -> bytes:
        """Compresses byte sequence into packed LZ77 binary stream.

        Binary Format:
        Uses an 8-item control flag byte:
        - Bit 0: item is Literal (1 byte)
        - Bit 1: item is Match (2 bytes offset uint16 + 1 byte length uint8)
        """
        if not data:
            return b""

        tokens = self.tokenize(data)
        out = bytearray()

        # Group tokens in chunks of 8
        for i in range(0, len(tokens), 8):
            chunk = tokens[i : i + 8]
            flag = 0
            chunk_body = bytearray()

            for bit_idx, tok in enumerate(chunk):
                if tok.is_match:
                    flag |= (1 << bit_idx)
                    # Offset (2 bytes big endian) and Length (1 byte)
                    chunk_body.extend(tok.offset.to_bytes(2, "big"))
                    chunk_body.append(tok.length)
                else:
                    # Literal (1 byte)
                    chunk_body.append(tok.literal)

            out.append(flag)
            out.extend(chunk_body)

        return bytes(out)

    def decompress(self, packed_data: bytes, original_size: int | None = None) -> bytes:
        """Decompresses packed LZ77 binary stream back to exact original bytes."""
        if not packed_data:
            return b""

        out = bytearray()
        idx = 0
        total_len = len(packed_data)

        while idx < total_len:
            flag = packed_data[idx]
            idx += 1

            for bit_idx in range(8):
                if idx >= total_len:
                    break
                if original_size is not None and len(out) >= original_size:
                    break

                is_match = (flag >> bit_idx) & 1
                if is_match:
                    if idx + 3 > total_len:
                        break
                    offset = int.from_bytes(packed_data[idx : idx + 2], "big")
                    length = packed_data[idx + 2]
                    idx += 3

                    start = len(out) - offset
                    for k in range(length):
                        out.append(out[start + k])
                else:
                    out.append(packed_data[idx])
                    idx += 1

        return bytes(out)
