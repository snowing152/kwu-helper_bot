# 0001. Hand-written RAG pipeline

- Status: Accepted
- Date: 2026-11-23

## Context
The bot must answer only from official documents, with citations. The project's main
goal is learning AI engineering, so the owner must be able to explain each stage
(chunking, embedding, retrieval, prompt building) in an interview.

## Decision
Build the RAG pipeline directly on the provider SDKs and our own code (about a few hundred
lines), without an orchestration framework.

## Alternatives considered
- LangChain / LlamaIndex: faster first demo, but they hide the stages we want to learn
  and tune, add many transitive dependencies, and change their APIs often.

## Consequences
- Every stage is visible, testable and measurable by the eval set.
- We write our own chunking and prompt code, and fix our own bugs in it.
- Revisit if we need features that are expensive to build ourselves (for example
  complex agent workflows).
