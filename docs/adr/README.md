# Architecture Decision Records

An ADR records one significant decision: the situation, what was chosen, what was
rejected, and what it costs. ADRs are never edited to change a decision. A new ADR
supersedes the old one, and the old one's status changes to "Superseded by NNNN".

| ADR | Title | Status |
|---|---|---|
| [0001](0001-hand-written-rag-pipeline.md) | Hand-written RAG pipeline | Accepted |
| [0002](0002-postgres-pgvector-for-vectors.md) | PostgreSQL with pgvector for vectors | Accepted |
| [0003](0003-claude-haiku-answers-opus-judge.md) | Claude Haiku answers, Claude Opus judges | Accepted |
| [0004](0004-embeddings-via-api-chosen-by-benchmark.md) | Embeddings via API, chosen by benchmark | Proposed |
| [0005](0005-telegram-aiogram-webhook-on-railway.md) | Telegram bot with aiogram, webhook on Railway | Accepted |
| [0006](0006-rules-only-mvp-no-klas.md) | Rules-only MVP, no KLAS access | Accepted |

## Template

Copy into `NNNN-short-title.md`:

```markdown
# NNNN. Title

- Status: Proposed | Accepted | Superseded by NNNN
- Date: YYYY-MM-DD

## Context
What situation or problem forces a decision. Facts and constraints only.

## Decision
What we do, stated in one or two sentences.

## Alternatives considered
- Option: why it was rejected.

## Consequences
What gets easier, what gets harder, and what would make us revisit this.
```
