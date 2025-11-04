"""Embedding utilities for the vector search service."""

from __future__ import annotations

import hashlib
import math
from typing import Iterable, List


class EmbeddingClient:
    """Lightweight text embedding helper.

    The implementation deliberately avoids external network calls so unit
    tests can exercise the code without depending on a hosted model.  The
    embedding strategy is deterministic which makes it straightforward to
    assert against in tests, while still producing dense vectors that mimic
    the behaviour of a production grade embedder.
    """

    def __init__(self, dimensions: int = 1536) -> None:
        if dimensions <= 0:
            raise ValueError("Embedding dimensionality must be positive")
        self._dimensions = dimensions

    @property
    def dimensions(self) -> int:
        return self._dimensions

    async def embed(self, text: str) -> List[float]:
        """Generate a pseudo-embedding for *text*.

        The embedding is computed by hashing individual tokens into the
        embedding space which gives us a repeatable representation.  The
        resulting vector is l2 normalised to mirror typical embedding
        outputs used with pgvector's cosine distance operator.
        """

        buckets = [0.0] * self._dimensions
        tokens = self._tokenise(text)
        if not tokens:
            return buckets

        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            # Use the first four bytes of the digest to pick a bucket.  This
            # keeps the behaviour deterministic without requiring any heavy
            # dependencies.
            bucket_index = int.from_bytes(digest[:4], "big") % self._dimensions
            buckets[bucket_index] += 1.0

        # Normalise to unit length so that cosine distance works as expected.
        norm = math.sqrt(sum(component * component for component in buckets))
        if norm:
            buckets = [component / norm for component in buckets]

        return buckets

    def _tokenise(self, text: str) -> Iterable[str]:
        for token in text.lower().split():
            stripped = token.strip()
            if stripped:
                yield stripped
