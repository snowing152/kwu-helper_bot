# kwu_helper

A Telegram bot that answers questions from Russian-speaking foreign students at
Kwangwoon University about official university rules and procedures (credits,
course registration, leave of absence, scholarships, university-side visa
procedures). Answers come only from official documents (RAG), in Russian, with a
source link and the original Korean or English passage.

## Roadmap

| # | Milestone | Status |
|---|---|---|
| 0 | Student survey | In progress |
| 1 | Crawler: official pages to text, with change detection | In progress |
| 2 | Chunking, embedding benchmark, pgvector search | Planned |
| 3 | Eval set and retrieval metrics | Planned |
| 4 | Answer generation in Russian with citations | Planned |
| 5 | Telegram bot with inline buttons | Planned |
| 6 | Deploy to Railway with spend limits | Planned |
| 7 | Regulations (학칙) crawler with Playwright | Planned |
| 8 | Graduation-credits calculator widget | Planned |

## Documentation

- [Design spec](docs/superpowers/specs/2026-11-23-kwu-helper-design.md): scope, sources, architecture
- [Architecture Decision Records](docs/adr/README.md): why each major choice was made
- [Implementation plans](docs/superpowers/plans/): step-by-step plans per milestone
- [Survey](docs/survey.md): the student survey that feeds the eval set

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

## License

[MIT](LICENSE). The license covers this code only, not university content.
