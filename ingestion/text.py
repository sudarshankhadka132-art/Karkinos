"""Text utilities for chunking documents."""

from __future__ import annotations

from typing import Iterable


def chunk_text(text: str, window: int = 500, overlap: int = 50) -> Iterable[str]:
  tokens = text.split()
  if window <= 0:
    raise ValueError("window must be positive")
  if overlap >= window:
    raise ValueError("overlap must be smaller than window")

  start = 0
  step = window - overlap
  while start < len(tokens):
    end = min(start + window, len(tokens))
    yield " ".join(tokens[start:end])
    if end == len(tokens):
      break
    start += step
