# tangem_skills

Central, versioned store for Tangem internal skills (Anthropic `SKILL.md` format).
Skills are published by the
[Skills Portal](https://github.com/1carlito/tangem-internal-skills-portal): the portal
scans each submission with an LLM (gpt-5.4-mini via OpenRouter) and, on a passing verdict,
commits the file directly to `main`. There is no PR/merge step.

## Layout
```
skills/
  <kebab-name>/
    SKILL.md          # required: YAML frontmatter + Markdown body
    references/       # optional: deeper docs, loaded on demand
    scripts/          # optional: helper scripts
```

## SKILL.md rules
- `name` (frontmatter) must be kebab-case and match the folder name.
- `description` <= 1024 chars, says what the skill does AND when to use it.
- Body kept under 500 lines; move detail into `references/`.

## Security
Skills are scanned **before** they are written, inside the portal API:
a regex pre-filter plus an OpenRouter classifier (gpt-5.4-mini) for
prompt-injection / data-exfiltration risks.
- High risk -> submission is rejected (HTTP 422) and nothing is committed.
- Pass -> the file is committed directly to `main`.

Because the gate runs before the write, there is no GitHub Actions check and no
PR/merge flow. Restrict direct write access to `main` to the portal's GitHub
identity so the scan cannot be bypassed.
