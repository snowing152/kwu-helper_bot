# kwu_helper - Design

Date: 2026-11-23. Status: agreed in a design interview.

## Purpose

A Telegram bot that answers questions from Russian-speaking foreign students at
Kwangwoon University about official university rules and procedures. It is a
learning and portfolio project for an AI-engineering career, with real users
from the student community.

## Scope

In scope (MVP): graduation and credit requirements, course registration,
leave of absence and return, grading, scholarships, university-side visa
procedures (enrollment certificates, part-time work approval).

Out of scope for now:
- Assignments and anything that needs KLAS. KLAS rejects logins from non-Korean
  servers. A future version must never store student passwords.
- Immigration law. The bot links to HiKorea (hikorea.go.kr) and the 1345 call
  center instead of interpreting it.
- Languages other than Russian.

## Answer rules

- Answers are generated only from retrieved official documents (RAG).
- Every answer is in Russian and shows the source link and the source date.
- A "Show original" button shows the Korean or English source passage.
- If no source passage supports an answer, the bot says it does not know and
  points to the Office of International Affairs.

## Sources

| Source | URL | Format | Language | Milestone |
|---|---|---|---|---|
| Office of International Affairs | https://oia.kw.ac.kr/campus/*.php | HTML | en | 1 |
| Academic info pages | https://www.kw.ac.kr/ko/life/bachelor_info*.jsp | HTML | ko | 1 |
| Scholarship guide | https://www.kw.ac.kr/ko/life/summary.jsp | HTML | ko | 1 |
| International notices | https://www.kw.ac.kr/ko/life/notice.jsp?srCategoryId=10 | HTML list + posts | ko | 1 |
| Regulations (학칙) | https://rule.kw.ac.kr/ | JS app | ko | 7 (Playwright) |

- Sources are re-crawled weekly. Only changed documents are re-processed.
- Scraped content is never committed. The public repo contains code only.

## Architecture

- Python, managed with uv. Tooling: ruff, mypy (strict), pytest.
- FastAPI service receives Telegram updates by webhook; aiogram 3 handles the bot.
- PostgreSQL with pgvector stores chunks, embeddings and anonymous logs.
- The RAG pipeline is written by hand (no LangChain or LlamaIndex).
- Answer model: `claude-haiku-5-5`. Eval judge: `claude-opus-5-5`. Both are
  called through an Anthropic API key from the environment, never through a
  Claude subscription.
- Embedding API chosen by a recall@5 benchmark on survey questions
  (candidates: Voyage multilingual, OpenAI text-embedding-3-small, Cohere multilingual).
- Hosting: Railway Hobby. One web service, Postgres, weekly crawler cron job.

## Safety, cost and privacy

- Spend limits: Anthropic Console monthly limit, Railway usage limit, and a
  per-user daily question cap in the bot.
- Logs store question, answer, sources and feedback only. No Telegram user
  IDs or usernames. The bot's first message states this.

## Quality

- Eval set built from real survey questions: expected answer plus source document.
- Metrics: retrieval recall@5 and answer correctness (LLM judge). Re-run after
  every change.

## Milestones

0. Survey (Google Form, Russian)
1. Crawler for milestone-1 sources: raw text plus a manifest with change detection
2. Chunking, embedding benchmark, pgvector, command-line search
3. Eval set and retrieval metrics
4. Answer generation in Russian with citations
5. Telegram bot with inline buttons
6. Deploy to Railway with spend limits
7. Regulations crawler with Playwright
8. Graduation-credits calculator as a Telegram widget (Bot API 10.4)
