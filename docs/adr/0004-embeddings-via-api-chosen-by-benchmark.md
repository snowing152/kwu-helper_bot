# 0004. Embeddings via API, chosen by benchmark

- Status: Proposed (decided in milestone 2)
- Date: 2026-11-23

## Context
Questions are in Russian; sources are in Korean and English, so embeddings must be
strongly multilingual. On Railway, memory costs about $10 per GB-month, and a local
model such as BGE-M3 needs 2-3 GB of RAM, which is several times the whole budget.
Switching embedding models later requires re-embedding every document.

## Decision
Use a hosted embedding API. Choose the provider by recall@5 on about 20 real survey
questions against our chunks. Candidates: Voyage multilingual, OpenAI
text-embedding-3-small, Cohere multilingual.

## Alternatives considered
- Local BGE-M3: free per call and strong on Korean, but too expensive to keep in memory
  on Railway.
- Picking a provider without measuring: cheaper in time, but the choice could not be
  defended.

## Consequences
- One more external account and SDK (added only with owner approval).
- The benchmark result is recorded here when this ADR becomes Accepted.
