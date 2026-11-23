# 0005. Telegram bot with aiogram, webhook on Railway

- Status: Accepted
- Date: 2026-11-23

## Context
The target users (Russian-speaking students) use Telegram daily. The owner has a Railway
Hobby plan ($5/month, which includes $5 of usage). Telegram Widgets (Bot API 10.4) are new
and not yet supported by aiogram (latest release supports Bot API 10.3).

## Decision
- Telegram bot built with aiogram 3, receiving updates by webhook in a FastAPI service.
- One Railway web service plus Railway PostgreSQL. The crawler runs as a weekly cron job.
- Answers use normal messages with inline keyboard buttons. A Telegram widget (graduation
  credits calculator) comes later, sent through a small hand-written Bot API call.

## Alternatives considered
- KakaoTalk channel: everyone in Korea has it, but it needs a business channel, approval
  and Korean-only tooling.
- Web app first: best for a portfolio, but students rarely return to a website.
- Long polling: simpler locally, but a process that is always awake costs more than a
  webhook service on Railway.
- python-telegram-bot: good library, but aiogram is async-first and the most common
  choice in the Russian-speaking developer community.

## Consequences
- The core RAG logic sits behind our own API, so a web or Kakao front end can be added.
- A webhook needs a public HTTPS URL and a secret token check on each request.
