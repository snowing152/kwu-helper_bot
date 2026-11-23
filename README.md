# kwu_helper

A Telegram bot that answers questions from Russian-speaking foreign students at
Kwangwoon University about official university rules and procedures (credits,
course registration, leave of absence, scholarships, university-side visa
procedures). Answers come only from official documents (RAG), in Russian, with a
source link and the original Korean or English passage.

Status: milestone 1 (crawler). See `docs/superpowers/specs/` for the design.

## Setup

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

## Checks

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy src tests
```

## Data

The crawler writes scraped university content to `data/`. This folder is in
`.gitignore` and is never committed: the content belongs to the university, and
the crawler can rebuild it at any time.
