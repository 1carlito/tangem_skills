---
name: pr-summary
description: Generate a concise, reviewer-friendly pull request summary from a git diff. Use when opening a PR or asked to summarize code changes for review.
tags: [git, code-review, productivity]
category: engineering
version: "1.0"
---

# PR Summary

Generate a clear pull request description from a set of code changes.

## Instructions
1. Read the provided diff or list of changed files.
2. Group changes by intent (feature, fix, refactor, test, docs).
3. Write the summary using this structure:
   - **What changed** — 1-3 bullet points focused on the "why".
   - **Risk / impact** — anything reviewers should watch for.
   - **Test plan** — how the change was or should be verified.
4. Keep it under 200 words. Prefer plain language over jargon.

## Example
Input: a diff adding rate limiting to the login endpoint.

Output:
- **What changed**: Added IP-based rate limiting to `POST /login` to slow credential-stuffing attempts.
- **Risk / impact**: Legitimate users behind shared NAT could hit the limit; threshold is configurable.
- **Test plan**: Unit tests for the limiter; manual check that the 6th attempt within 60s returns 429.
