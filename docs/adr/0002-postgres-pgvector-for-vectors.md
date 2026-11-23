# 0002. PostgreSQL with pgvector for vectors

- Status: Accepted
- Date: 2026-11-23

## Context
We need to store a few thousand text chunks with embeddings, plus metadata (source URL,
date, language) and anonymous logs. Hosting is Railway, where every running service
costs memory.

## Decision
Use one PostgreSQL database with the pgvector extension for chunks, embeddings, metadata
and logs.

## Alternatives considered
- Chroma or another dedicated vector DB: simpler start, but a second service to run, and
  less transferable knowledge than Postgres.
- Pinecone (hosted): no infrastructure, but a vendor account and limits for a small project.
- In-memory search (NumPy): fine at this size, but no persistence and no SQL filters.

## Consequences
- One database for everything; metadata filters are plain SQL.
- Exact search is fast enough at our size; add an HNSW index if chunks reach the
  hundreds of thousands.
- Revisit if retrieval needs hybrid search that Postgres full-text search cannot cover.
