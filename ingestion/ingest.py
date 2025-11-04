"""Utilities to ingest PDF documents into the Karkinos datastore."""

from __future__ import annotations

import hashlib
import io
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import psycopg
from pypdf import PdfReader

from .text import chunk_text
from .vector import EmbeddingClient


@dataclass
class DocumentPayload:
  source_id: str
  cancer_id: str
  title: str
  url: str | None
  path: Path


@dataclass
class ChunkPayload:
  document_id: str
  text: str
  embedding: Sequence[float]
  chunk_ix: int


def sha256_digest(buffer: bytes) -> str:
  return hashlib.sha256(buffer).hexdigest()


def load_pdf_text(path: Path) -> str:
  reader = PdfReader(path)
  buffer = io.StringIO()
  for page in reader.pages:
    buffer.write(page.extract_text() or "")
    buffer.write("\n")
  return buffer.getvalue()


def ingest_documents(
  connection_string: str,
  documents: Iterable[DocumentPayload],
  embedding_client: EmbeddingClient,
  chunk_size: int = 500,
  chunk_overlap: int = 50
) -> None:
  with psycopg.connect(connection_string) as conn:
    with conn.cursor() as cur:
      for doc in documents:
        raw_bytes = doc.path.read_bytes()
        sha256 = sha256_digest(raw_bytes)
        cur.execute(
          """
          INSERT INTO documents (source_id, cancer_id, title, url, sha256)
          VALUES (%s, %s, %s, %s, %s)
          ON CONFLICT (sha256) DO UPDATE SET title = EXCLUDED.title
          RETURNING id
          """,
          (doc.source_id, doc.cancer_id, doc.title, doc.url, sha256)
        )
        document_id = cur.fetchone()[0]
        text = load_pdf_text(doc.path)
        for ix, chunk in enumerate(chunk_text(text, chunk_size, chunk_overlap)):
          embedding = embedding_client.embed(chunk)
          cur.execute(
            """
            INSERT INTO chunks (document_id, text, embedding, chunk_ix)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (document_id, chunk_ix) DO UPDATE
              SET text = EXCLUDED.text,
                  embedding = EXCLUDED.embedding
            """,
            (document_id, chunk, embedding, ix)
          )
    conn.commit()
