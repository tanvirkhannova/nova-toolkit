"""File hashing utility for nova-toolkit."""

import hashlib
from pathlib import Path

ALGORITHMS = ("sha256", "sha1", "md5")


def hash_file(path: str, chunk_size: int = 65536) -> dict:
    """Hash a file with several algorithms in a single pass."""
    hashers = {name: hashlib.new(name) for name in ALGORITHMS}
    with Path(path).open("rb") as f:
        while chunk := f.read(chunk_size):
            for h in hashers.values():
                h.update(chunk)
    return {name: h.hexdigest() for name, h in hashers.items()}


def verify(path: str, expected: str) -> bool:
    """Check a file against a published hash (any supported algorithm)."""
    expected = expected.strip().lower()
    return expected in hash_file(path).values()
