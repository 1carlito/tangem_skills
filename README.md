# tangem_skills

Central, versioned store for Tangem internal skills (Anthropic `SKILL.md` format).
Skills are contributed via pull requests (usually opened automatically by the
[Skills Portal](https://github.com/1carlito/tangem-internal-skills-portal)).

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
Every PR that touches `skills/**/SKILL.md` runs the **Skill Security Scan**
(`.github/workflows/skill-scan.yml`): a regex pre-filter plus an OpenRouter
classifier for prompt-injection / data-exfiltration risks.
- High risk -> the check fails and merge is blocked (under branch protection).
- Medium risk -> a warning annotation for human review.

Set the repo secret `OPENROUTER_API_KEY` for the classifier; without it the scan
falls back to regex-only.

## Branch protection (recommended)
Protect `main`: require the `Skill Security Scan` check to pass and require at
least one review before merge.
