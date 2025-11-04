"""Embedding client abstraction."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np


@dataclass
class EmbeddingClient:
  model_name: str = "sentence-transformers/all-MiniLM-L6-v2"

  def embed(self, text: str) -> Sequence[float]:
    # Placeholder implementation using a deterministic hash to keep the scaffold lightweight.
    rng = np.random.default_rng(abs(hash((self.model_name, text))) % (2**32))
    return rng.normal(size=1536).tolist()
