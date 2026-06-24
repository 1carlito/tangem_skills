# Anti-Patterns: Detailed Catalog

Each entry shows a concrete bad example, why it fails in practice, and the corrected form. Use this file as a checklist when reviewing a draft SKILL.md.

## Contents

1. Workflow summary in description
2. Generic description
3. Documentation-style body
4. Monolithic skill
5. First/second person in description
6. Critical rules buried in the middle
7. Multiple tool options without a default
8. Deeply nested file references
9. Non-standard frontmatter keys
10. Broken file references
11. Time-sensitive content
12. Secrets in skill files

---

## 1. Workflow summary in description

**Bad**:
```yaml
description: >
  Reads the schema file, diffs it against the latest migration, generates
  SQL with drizzle-kit, scans the SQL for destructive operations, prompts
  the user if any are found, runs the migration, then runs the test suite
  to verify.
```

**Why it fails**: The agent now has a complete-enough picture of the procedure from the description alone (~100 tokens loaded at startup). It may skip reading the body, where the actual constraints and edge cases live, and improvise the workflow.

**Good**:
```yaml
description: >
  Use when creating database migrations or modifying schemas with Drizzle
  ORM. Handles migration generation, destructive operation detection, and
  rollback scripts.
```

The description signals **when** to activate and **what surface** the skill covers. The agent must read SKILL.md to learn the procedure.

---

## 2. Generic description

**Bad**:
```yaml
description: >
  Helps with database stuff.
```

**Why it fails**: No trigger keywords, no scope boundary. The agent either activates this for unrelated queries ("can you read the config?") or never activates it because nothing about the user's phrasing matches.

**Good**:
```yaml
description: >
  Use when creating or modifying database migrations with Drizzle ORM,
  reviewing schema changes, or troubleshooting migration failures.
  Do NOT use for runtime SQL queries or ORM model design discussions.
```

Specific verbs (`creating`, `modifying`, `reviewing`, `troubleshooting`), the named tool (`Drizzle ORM`), and a negative trigger that excludes adjacent-but-different requests.

---

## 3. Documentation-style body

**Bad**:
```markdown
## About Our Migrations

The project uses Drizzle ORM with SQLite. Migrations are stored in
`migrations/` and are applied in lexical order. Each migration has a
numeric prefix that determines its position in the sequence. Migrations
should be idempotent where possible...
```

**Why it fails**: The agent already knows what migrations are. Prose like this consumes context without telling the agent what to **do** when a user asks it to add a migration. The agent ends up improvising the steps.

**Good**:
```markdown
## Workflow

1. Read the current schema from `src/db/schema.ts`
2. Run: `npx drizzle-kit generate`
3. Inspect the generated SQL in `migrations/`
4. If the diff contains DROP or ALTER COLUMN TYPE, stop and ask the user
   before continuing
5. Run: `npx drizzle-kit migrate`
6. Verify: `npm test`
```

Same domain, but every line tells the agent what to execute. Drop facts the agent already knows; keep your team's specific commands, paths, and constraints.

---

## 4. Monolithic skill

**Bad**: A single SKILL.md of 1,200 lines covering "everything about our backend": auth, migrations, routing, testing, deployment, monitoring.

**Why it fails**: Two problems. First, the description has to be vague enough to cover all six topics, so it triggers for vague requests and misses specific ones. Second, the agent loads the whole file when only one section is relevant, wasting context.

**Good**: Split into focused skills with sharp descriptions:
```
skills/
├── reviewing-migrations/
├── creating-api-endpoint/
├── deploying-to-staging/
└── debugging-auth-flow/
```

If two skills share reference material, factor it into a small shared `references/` file inside each (or accept the duplication — skills are leaf nodes, not a dependency graph).

---

## 5. First/second person in description

**Bad**:
```yaml
description: >
  I can help you write database migrations. You just tell me what schema
  change you want and I'll handle the rest.
```

**Why it fails**: The description is concatenated into a system-prompt-style context. First/second person breaks the voice and reads as a character note rather than a routing instruction. It also tends to invite over-triggering ("I can help with anything" → activates constantly).

**Good**:
```yaml
description: >
  Use when creating or modifying Drizzle ORM migrations. Generates SQL,
  flags destructive operations, and runs verification tests.
```

Third person, imperative voice, scoped capabilities.

---

## 6. Critical rules buried in the middle

**Bad**:
```markdown
# Migrations

## Background
[300 lines of context]

## Step-by-step
[...]

## Final notes
NEVER drop a production column without a two-phase migration.
```

**Why it fails**: The agent may summarize or skim long bodies and miss the rule that matters most. Buried constraints get violated.

**Good**: Put a `## Critical Rules` block immediately after the title:
```markdown
# Migrations

## Critical Rules
- Never drop a production column without a two-phase migration (deploy
  read-from-old-write-to-both, then deploy drop in the next release).
- Migrations must be reversible; provide a `down` for every `up`.

## Workflow
[...]
```

---

## 7. Multiple tool options without a default

**Bad**:
```markdown
Generate the migration using one of:
- `npx drizzle-kit generate`
- `pnpm db:migrate:gen`
- `npm run gen:migration`
```

**Why it fails**: The agent picks randomly each run, producing inconsistent output. Different team members invoke the skill and get different commands in their logs.

**Good**:
```markdown
Generate the migration: `pnpm db:migrate:gen`

(Equivalent commands `npx drizzle-kit generate` and `npm run gen:migration`
exist; use them only if pnpm is unavailable on the host.)
```

One default. Alternatives are documented as fallbacks, not equal options.

---

## 8. Deeply nested file references

**Bad**:
```
my-skill/
├── SKILL.md
└── references/
    └── db/
        └── v2/
            └── schema-conventions.md
```

SKILL.md says: `See references/db/v2/schema-conventions.md`.

**Why it fails**: Some runtimes resolve only the first level under `references/`. The agent fetches a partial path, gets nothing, and substitutes plausible-sounding invented content.

**Good**: Keep references one level deep. Use longer filenames if you need namespacing:
```
my-skill/
└── references/
    ├── db-schema-conventions-v2.md
    └── db-migration-procedure.md
```

---

## 9. Non-standard frontmatter keys

**Bad**:
```yaml
---
name: create-skill
description: ...
metadata:
  author: Anton Vanin
  version: 1.2
tags: [skill, prompt-engineering]
---
```

**Why it fails**: Top-level keys outside the spec (`metadata`, `tags`, `author`, `version`, etc.) may be rejected outright by stricter runtimes, or silently ignored — leading to false confidence that metadata is being used.

**Good**: Keep top-level frontmatter to documented keys (`name`, `description`, optional `license`, `compatibility`, `allowed-tools`). Put authorship and version notes in a `## Credits` section in the body or in a sibling `CHANGELOG.md`.

---

## 10. Broken file references

**Bad**: SKILL.md says `See references/error-codes.md` — but the file doesn't exist in the skill.

**Why it fails**: The agent treats the reference as authoritative, can't find the file, and either (a) silently fabricates content matching the path's implied topic, or (b) hallucinates an error message it never received. Both are worse than no reference.

**Good**: Audit every `references/...`, `scripts/...`, and `assets/...` mention before shipping. If a referenced file isn't ready, either inline the content or remove the reference until the file exists.

---

## 11. Time-sensitive content

**Bad**:
```markdown
## Latest API version
We are currently on v3.2 (released March 2025). Migration to v4 is
expected next quarter.
```

**Why it fails**: Skills are loaded into context for months or years after they're written. The agent presents stale information as current fact.

**Good**: State only durable rules:
```markdown
## API versioning
Read the current API version from `package.json` → `"@vendor/api"` before
generating client code. Do not hardcode version assumptions.
```

If the skill genuinely needs a current value, fetch it at runtime from a file or command — don't embed it.

---

## 12. Secrets in skill files

**Bad**:
```markdown
## Auth
Use bearer token `sk-prod-9f8a...` when calling the staging API.
```

**Why it fails**: Skills are designed to be shared — across machines, into repos, into screenshots. Any secret committed to a SKILL.md becomes public the moment the skill is shared.

**Good**:
```markdown
## Auth
The staging API requires a bearer token. Read it from the `STAGING_TOKEN`
environment variable. If unset, stop and ask the user to export it.
```
