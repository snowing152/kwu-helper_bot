# 0003. Claude Haiku answers, Claude Opus judges

- Status: Accepted
- Date: 2026-11-23

## Context
The budget is near zero. Answers must be faithful to retrieved Korean and English
passages and written in Russian. We need an automatic way to grade answer quality.

## Decision
- Student answers: `claude-haiku-5-5` ($0.10 / $0.50 per 1M input/output tokens as of
  2026-11-03; about $1 per 1,000 answers).
- Eval grading: `claude-opus-5-5` as LLM judge on the small eval set.
- Calls go through an Anthropic API key from the environment, behind one small
  `generate()` interface so the model can be swapped by config.
- A Claude subscription (Pro/Max) is not used for the bot: it covers personal use of
  Claude Code and claude.ai, not serving other users.

## Alternatives considered
- Opus or Sonnet for answers: higher quality, many times the cost. The eval will show
  how much quality Haiku loses; that comparison decides any upgrade.
- Free-tier models from other providers: free tiers change often and complicate the
  provider-agnostic interface early.

## Consequences
- Very low running cost.
- If Haiku fails the eval bar on hard questions, we try routing those to a stronger model.
