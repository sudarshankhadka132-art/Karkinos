"""CLI utilities for ingesting documents into the vector store."""
from __future__ import annotations

import argparse
import hashlib
import os
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence
from uuid import uuid4

VECTOR_DIMENSION = 1536


@dataclass
class ChunkRecord:
    """A structured representation of a chunk ready for persistence."""

    id: str
    document_path: str
    chunk_index: int
    content: str
    embedding: List[float]


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Split text into overlapping chunks suitable for embeddings."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    normalized = " ".join(text.split())
    if not normalized:
        return []

    chunks: List[str] = []
    start = 0
    while start < len(normalized):
        end = start + chunk_size
        chunk = normalized[start:end]
        chunks.append(chunk)
        if end >= len(normalized):
            break
        start = max(0, end - overlap)
    return chunks


def generate_embedding(text: str, dimension: int = VECTOR_DIMENSION) -> List[float]:
    """Return a deterministic pseudo-random embedding vector for the text."""
    seed = int(hashlib.sha256(text.encode("utf-8")).hexdigest(), 16) % (2**32)
    rng = random.Random(seed)
    return [rng.uniform(-1.0, 1.0) for _ in range(dimension)]


def vector_literal(values: Sequence[float]) -> str:
    """Format a Python sequence into a pgvector literal."""
    return "[" + ",".join(f"{value:.6f}" for value in values) + "]"


def upsert_embeddings(records: Iterable[ChunkRecord], db_url: str | None) -> None:
    """Persist embeddings into a pgvector-enabled PostgreSQL database."""
    records = list(records)
    if not records:
        print("No records to upsert.")
        return

    if not db_url:
        print("DATABASE_URL not provided; skipping database upsert.")
        return

    try:
        import psycopg
    except ImportError:  # pragma: no cover - optional dependency
        print("psycopg is not installed; skipping database upsert.")
        return

    with psycopg.connect(db_url) as conn:  # pragma: no cover - requires database
        with conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
            cur.execute(
                f"""
                CREATE TABLE IF NOT EXISTS document_chunks (
                    id UUID PRIMARY KEY,
                    document_path TEXT NOT NULL,
                    chunk_index INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    embedding vector({VECTOR_DIMENSION})
                )
                """
            )

            for record in records:
                cur.execute(
                    """
                    INSERT INTO document_chunks (id, document_path, chunk_index, content, embedding)
                    VALUES (%s, %s, %s, %s, %s::vector)
                    ON CONFLICT (id) DO UPDATE SET
                        document_path = EXCLUDED.document_path,
                        chunk_index = EXCLUDED.chunk_index,
                        content = EXCLUDED.content,
                        embedding = EXCLUDED.embedding
                    """,
                    (
                        record.id,
                        record.document_path,
                        record.chunk_index,
                        record.content,
                        vector_literal(record.embedding),
                    ),
                )
        conn.commit()

    print(f"Upserted {len(records)} chunk(s) into pgvector store.")


def ingest_file(path: Path, chunk_size: int, overlap: int) -> List[ChunkRecord]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
    records: List[ChunkRecord] = []
    for index, chunk in enumerate(chunks):
        records.append(
            ChunkRecord(
                id=str(uuid4()),
                document_path=str(path),
                chunk_index=index,
                content=chunk,
                embedding=generate_embedding(chunk),
            )
        )
    return records


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest documents into pgvector")
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="One or more document paths to ingest",
    )
    parser.add_argument(
        "--db-url",
        default=os.environ.get("DATABASE_URL"),
        help="PostgreSQL connection string (defaults to DATABASE_URL env variable)",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=1000,
        help="Maximum characters per chunk",
    )
    parser.add_argument(
        "--overlap",
        type=int,
        default=200,
        help="Number of characters of overlap between chunks",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    all_records: List[ChunkRecord] = []

    for file_path in args.files:
        path = Path(file_path)
        if not path.exists():
            print(f"Skipping missing file: {path}")
            continue
        if path.is_dir():
            print(f"Skipping directory (files only): {path}")
            continue

        file_records = ingest_file(path, chunk_size=args.chunk_size, overlap=args.overlap)
        if not file_records:
            print(f"No content extracted from {path}; skipping.")
            continue
        print(f"Prepared {len(file_records)} chunk(s) from {path}.")
        all_records.extend(file_records)

    if not all_records:
        print("No records generated from provided files.")
        return

    upsert_embeddings(all_records, db_url=args.db_url)


if __name__ == "__main__":
    main()
