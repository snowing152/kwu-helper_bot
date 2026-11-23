# kwu_helper

Telegram RAG bot that answers Kwangwoon University rule and procedure questions for
Russian-speaking foreign students. Answers come only from official university documents,
in Russian, with source link, source date and the original passage.

This is a learning project for the owner's AI-engineering career: explain non-obvious
decisions (concept first, then code, then how it works).

- Design spec: `docs/superpowers/specs/2026-11-23-kwu-helper-design.md`
- Decisions and their reasons: `docs/adr/` (add a new ADR when a decision changes)
- Current plan: `docs/superpowers/plans/` (latest file)

## Commands

```bash
uv sync                                  # install deps from uv.lock
uv run pytest                            # tests
uv run ruff check . && uv run ruff format --check .
uv run mypy src tests                    # strict type check
uv run python -m kwu_helper.crawler      # crawl sources into data/ (milestone 1)
```

All four checks must pass before a task is called done.

## Layout

- `src/kwu_helper/crawler/` - source registry, rate-limited fetcher, HTML-to-text
  extraction, notice-list parsing, file store with change detection, CLI.
- `tests/` mirrors `src/`. Fixtures are small hand-written HTML, never copies of real pages.
- `data/` - scraped content and manifest. Git-ignored. Never commit it.

Later milestones add: chunking and embeddings (pgvector), eval, answer generation,
Telegram bot (aiogram 3 via FastAPI webhook), Railway deploy.

## Hard rules

- Never commit `data/`, `.env`, or real page content (university's content).
- Crawler: max 1 request/second per host, User-Agent `kwu-helper-crawler/0.1 (student project)`,
  no personal data in requests.
- The bot answers only from retrieved passages; with no supporting passage it says it does
  not know and points to the Office of International Affairs. Never interpret immigration law.
- API keys and model IDs come from environment variables. Answer model `claude-haiku-5-5`,
  eval judge `claude-opus-5-5`, via an Anthropic API key (never a Claude subscription token).
- Logs hold question, answer, sources and feedback only. No Telegram user IDs or usernames.
- KLAS and anything behind a student login are out of scope. Never store student passwords.
- New dependencies need the owner's approval.

## Task tracking (Jira)

- Jira project `KWU` on maksimtyan152.atlassian.net (Atlassian MCP server). Epics KWU-1..9 = milestones M0..M8.
- Flow: To Do -> In Progress (work started) -> In Review (checks green, commit awaits owner OK) -> Done (committed).
- Put the issue key at the end of the commit subject: `feat(crawler): add fetcher (KWU-12)`.

## Gotchas

- Development is on Windows, deployment on Linux (Railway). Use `pathlib`, open files with
  `encoding="utf-8"`, keep LF line endings (`.gitattributes`).
- Some kw.ac.kr pages may be EUC-KR; always decode through `crawler.extract.decode_html`.
- `rule.kw.ac.kr` is a JavaScript app; plain HTTP fetch returns a loading screen
  (handled in milestone 7 with Playwright).
- ruff excludes `docs/` because it would reformat code snippets inside Markdown.
