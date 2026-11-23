# 0006. Rules-only MVP, no KLAS access

- Status: Accepted
- Date: 2026-11-23

## Context
Students also want help with assignments and deadlines, which live in KLAS, the
university portal. KLAS requires a student login, and from non-Korean servers it adds
an email verification step. Wrong answers about rules can cost a student a scholarship,
a semester or a visa.

## Decision
The MVP answers only questions about official rules and procedures. It does not access
KLAS, does not store student credentials, and does not help with homework content.
Immigration-law questions are redirected to HiKorea and the 1345 call center.

## Alternatives considered
- Scraping KLAS with student passwords: a security and legal risk, breaks whenever KLAS
  changes, and is blocked from our non-Korean servers.
- Homework help: an academic-integrity problem that general chatbots already cover.

## Consequences
- Smaller, safer scope that uses only public documents.
- A later deadline feature must use manual input or a calendar import, never passwords.
