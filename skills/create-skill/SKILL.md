---
name: create-skill
description: >
  Use when asked to create, author, write, or scaffold a new Agent Skill or
  SKILL.md file, or when asked about skill structure, frontmatter, triggers,
  or best practices for the agentskills.io standard. Handles naming, the
  description trigger, directory layout, progressive disclosure, and
  verification. Do NOT use for non-skill prompt artifacts such as
  platform-specific rule files (e.g., Cursor Rules, AGENTS.md), system
  prompts, or chat-mode instructions.
domain: engineering
---

# Creating Agent Skills

## Critical Rules (read first)

- The `description` field is a **trigger**, not a summary. It tells the agent WHEN to activate, not HOW the workflow works. If the description leaks the procedure, the agent may skip reading the body.
- Write procedures, not documentation. Every section must tell the agent what to DO, not what things ARE.
- Keep SKILL.md body under 500 lines. Move detailed content to `references/` files.
- Always use forward slashes in paths (`scripts/helper.py`, never `scripts\helper.py`).
- Never put secrets (API keys, tokens, passwords) in SKILL.md files or supporting assets.
- The `name` field must exactly match the parent directory name.
- Only reference files you are actually shipping. A broken `references/x.md` link is worse than no link.

---

## Workflow

### Phase 1: Gather Requirements

Before writing any files, collect what you need from the user. If your runtime offers a structured multiple-choice tool (e.g., `AskUserQuestion` or equivalent), batch the closed questions into a single call. Otherwise, ask them conversationally in one message.

**Skip questions you can already answer.** If the user said "create a project skill for code review", the location and category are settled — only ask about what's still unclear. If everything is clear, jump to Phase 2.

**Reserved locations.** Do not write into directories the host platform reserves for its built-in skills. Common reserved locations include any `*/skills-builtin/`, `*/skills-system/`, or vendor-prefixed paths under a tool's config directory. Use the user-skills location for that platform instead.

Closed questions to batch:

```
Q1 — skill_location
  prompt: "Where should this skill be stored?"
  options:
    - "personal" → "Personal — available across all your projects on this machine
                    (typically under your home directory, e.g., ~/.claude/skills/,
                    ~/.cursor/skills/, ~/.config/<tool>/skills/)"
    - "project"  → "Project — shared via version control with your team
                    (typically .<tool>/skills/ at the repo root, e.g.,
                    .claude/skills/, .cursor/skills/)"

Q2 — skill_category
  prompt: "What category best describes this skill?"
  options:
    - "workflow" → "Workflow automation — multi-step process (deploy, review, test)"
    - "creation" → "Document/asset creation — generates consistent output (reports, code, docs)"
    - "mcp"      → "MCP enhancement — adds expertise on top of MCP tool access"
    - "other"    → "Other — none of the above"

Q3 — needs_scripts
  prompt: "Will this skill need executable scripts?"
  options:
    - "yes"    → "Yes — include scripts/ for validation, automation, etc."
    - "no"     → "No — instructions only"
    - "unsure" → "Decide later based on complexity"

Q4 — needs_references
  prompt: "Will this skill need reference documentation files?"
  options:
    - "yes"    → "Yes — include references/ for API docs, style guides, conventions"
    - "no"     → "No — everything fits in SKILL.md"
    - "unsure" → "Decide later based on content size"

Q5 — needs_templates
  prompt: "Will this skill need output templates or asset files?"
  options:
    - "yes" → "Yes — include assets/ for templates, schemas, boilerplate"
    - "no"  → "No — no template files needed"

Q6 — freedom_level
  prompt: "How much freedom should the agent have when following this skill?"
  options:
    - "low"    → "Low — exact scripts/commands; consistency critical (migrations, deploys)"
    - "medium" → "Medium — preferred patterns with acceptable variation (code generation)"
    - "high"   → "High — general guidelines, multiple valid approaches (code review)"
```

Free-text follow-ups (ask only if not already answered in context):

1. **Purpose**: "What specific task or workflow should this skill handle? 1–2 sentences."
2. **Trigger scenarios**: "What would a user type that should activate this skill? 2–3 example phrases."
3. **Domain knowledge**: "What specialized information does the agent need that it wouldn't already know? (Team conventions, internal APIs, in-house tools, etc.)"

### Phase 2: Design the Skill

#### 2a. Choose the name

- 1–64 characters, lowercase letters, numbers, and hyphens only
- Pattern: `^[a-z0-9]+(-[a-z0-9]+)*$` (no consecutive hyphens)
- Must match the parent directory name exactly
- Use gerund form for process skills: `reviewing-code`, `generating-migrations`
- Use verb-noun for action skills: `create-api-endpoint`, `deploy-staging`
- Avoid vague names: `helper`, `utils`, `tools`, `data`

For full naming rules and the rest of the frontmatter spec, see `references/specification-reference.md`.

#### 2b. Write the description (most critical step)

The description is the only thing the agent loads at startup (~100 tokens per skill). It determines whether the skill activates. Get this wrong and nothing else matters.

**Structure**: WHEN to use + WHAT capabilities exist (never HOW).

```yaml
# GOOD: trigger-style description
description: >
  Use when creating database migrations or modifying schemas with Drizzle ORM.
  Handles migration generation, destructive operation detection, and rollback scripts.

# BAD: workflow summary (agent may skip reading the body)
description: >
  Analyzes the current schema, compares against migrations, generates SQL,
  checks for destructive operations, and runs migration with verification.
```

**Rules for descriptions**:

- Write in third person ("Processes...", "Use when...", never "I can help" or "You can use")
- Include specific trigger keywords users would actually type
- Include synonyms to catch variant phrasings
- Add negative triggers when over-triggering is a risk: "Do NOT use for simple formatting"
- Stay under 1,024 characters (aim for 2–4 sentences)
- Include both WHAT it does and WHEN to use it

**Verify the description**: After installing, ask the agent "When would you use the [skill-name] skill?" and compare the response to your intended trigger conditions.

#### 2c. Plan the directory structure

Minimal skill:

```
skill-name/
└── SKILL.md
```

Skill with supporting files:

```
skill-name/
├── SKILL.md              # Required: main instructions (<500 lines)
├── references/           # Optional: docs loaded on demand
│   ├── api-conventions.md
│   └── error-codes.md
├── scripts/              # Optional: executable code
│   └── validate.py
└── assets/               # Optional: templates, schemas
    └── route-template.ts
```

Only these three subdirectories are part of the spec. Keep files one level deep (no nesting like `references/db/v1/schema.md`).

### Phase 3: Write the SKILL.md

#### 3a. Frontmatter

```yaml
---
name: skill-name
description: >
  Use when [trigger conditions].
  Handles [capabilities]. Do NOT use for [exclusions if needed].
---
```

Optional fields (use only when they add genuine value — do not invent custom keys):
- `license`: Standard license name or LICENSE file reference
- `compatibility`: Environment requirements (only if the skill has genuine constraints)
- `allowed-tools`: Restricts agent tool access (support varies by runtime — Claude Code supports it; others partial or none)

Do **not** add non-standard keys like `metadata:` or `author:` at the top level. Put authorship and changelogs in a `## Credits` section in the body or in a separate `CHANGELOG.md`.

Full field list and platform support matrix: `references/specification-reference.md`.

#### 3b. Body content — write procedures, not documentation

Start with the most important constraints, then the workflow.

**Procedural style (correct)**:

```markdown
## Workflow

1. Read the current schema from `src/db/schema.ts`
2. Generate a migration: `npx drizzle-kit generate`
3. Review generated SQL for destructive operations (DROP, ALTER column type)
4. If destructive operations found, add a data migration step first
5. Run the migration: `npx drizzle-kit migrate`
6. Verify: `npm test`

## Rules
- Never drop columns without explicit user confirmation
- Migration files use format: `NNNN_description.sql`
```

**Documentation style (wrong)**:

```markdown
## About Migrations
Our project uses Drizzle ORM with SQLite. Migrations keep the schema
in sync across environments. The migrations directory contains all
historical migration files...
```

The agent already knows what migrations are. Only provide what it doesn't know: your team's specific commands, conventions, and constraints.

#### 3c. Use these patterns

**Workflow pattern** — numbered steps with verification:

```markdown
## Workflow
1. [Action with specific command]
   - If it fails, [how to handle]
2. [Next action]
3. [Verification step]: `command to verify`
   - If verification fails, return to step 2
```

**Conditional workflow** — guide through decision points:

```markdown
## Determine test strategy
- If change modifies a public API:
  - Run full integration test suite
  - Update API contract tests
- If change is internal refactoring only:
  - Run unit tests for affected modules
- If change touches database models:
  - Run migration tests first, then full suite
```

**Template pattern** — provide exact output format:

```markdown
## Output format

Use this template:

# [Title]
## Summary
[One paragraph]
## Findings
- Finding with evidence
## Recommendations
1. Actionable recommendation
```

**Examples pattern** — input/output pairs for quality:

```markdown
## Commit message format

Example 1:
Input: Added JWT authentication
Output: `feat(auth): implement JWT-based authentication`

Example 2:
Input: Fixed date display bug
Output: `fix(reports): correct date formatting in timezone conversion`
```

**Feedback loop** — validate before proceeding:

```markdown
## Validation
1. Run linter: `npm run lint`
2. If lint fails, fix issues before proceeding
3. Run type check: `npx tsc --noEmit`
4. Run tests: `npm test`
5. Only proceed when all checks pass
```

#### 3d. Progressive disclosure

Put essential instructions in SKILL.md. Move detailed reference material to separate files under `references/` with explicit load instructions:

```markdown
## API conventions
Follow the error response conventions in `references/api-conventions.md`.
Read that file before writing any handler.

## Error codes
For the complete error code reference, see `references/error-codes.md`.
```

The agent reads these files only when it reaches that step. For reference files over 100 lines, include a table of contents at the top. Only reference files that actually exist in your skill — broken paths cause the agent to hallucinate substitutes.

#### 3e. Utility scripts

Pre-made scripts are more reliable than generated code, save tokens, and ensure consistency:

````markdown
## Utility scripts

**validate.py**: Check output for errors

```bash
python scripts/validate.py output/
# Returns: "OK" or lists issues
```
````

Make clear whether the agent should **execute** the script or **read** it as reference. Scripts should handle errors explicitly (not punt to the agent) and document their dependencies inline at the top.

### Phase 4: Verify the Skill

Run through this checklist before finalizing:

#### Description quality
- [ ] Describes WHEN to use (trigger), not HOW it works (procedure)
- [ ] Written in third person
- [ ] Includes specific trigger keywords and synonyms
- [ ] Under 1,024 characters
- [ ] Has negative triggers if over-triggering is a risk

#### Body quality
- [ ] Under 500 lines
- [ ] Procedural style (steps to DO), not documentation (what things ARE)
- [ ] Most important constraints appear first
- [ ] Consistent terminology (pick one term, use it everywhere)
- [ ] No time-sensitive information
- [ ] No secrets or credentials

#### Structure
- [ ] `name` field matches directory name exactly
- [ ] No non-standard frontmatter keys
- [ ] File references are one level deep (no nested references)
- [ ] Forward slashes in all paths
- [ ] Every referenced file actually exists in the skill
- [ ] Reference files have a table of contents if >100 lines

#### If including scripts
- [ ] Scripts handle errors explicitly
- [ ] Dependencies documented at the top of each script
- [ ] Constants are justified (no magic numbers)
- [ ] Clear whether the agent should execute the script or read it as reference

---

## Testing the Skill

### Trigger testing

Test with 10–20 queries across three groups:

1. **Should trigger (direct phrasing)**: "Help me [exact task]"
2. **Should trigger (paraphrased)**: Variant wordings of the same request
3. **Should NOT trigger**: Related but out-of-scope requests

Target: 80–90% correct activation. If under-triggering, add more keywords to the description. If over-triggering, add negative triggers.

### Functional testing

Run the same request 3–5 times. Compare outputs:
- Do the steps execute in the correct order?
- Are outputs structurally consistent?
- Does the agent skip any steps? (If yes, check for description leakage or buried instructions.)

### Performance comparison

Compare the same task with and without the skill. Fill in real numbers from your runs:

| Metric                   | Without | With |
|--------------------------|---------|------|
| Back-and-forth messages  | ?       | ?    |
| User corrections needed  | ?       | ?    |
| Failed tool calls        | ?       | ?    |

If the skill doesn't improve at least one metric, simplify or reconsider.

---

## Anti-Patterns Quick Reference

For detailed examples of each anti-pattern, see `references/anti-patterns.md`.

| Anti-Pattern | Why It Fails | Fix |
|---|---|---|
| Workflow summary in description | Agent skips reading the body | Write trigger conditions only |
| Generic description | Matches everything or nothing | Use specific keywords + negative triggers |
| Documentation style body | Agent has no actionable steps | Write numbered procedures |
| Monolithic skill (>500 lines) | Expensive context, imprecise activation | Split into focused skills |
| First/second person in description | Breaks system prompt voice | Use third person: "Processes...", "Use when..." |
| Critical rules buried in the middle | Agent skips them | Frontload constraints at the top |
| Multiple tool options without a default | Agent chooses randomly each time | Pick one default; note alternatives only for edge cases |
| Deeply nested file references | Agent partially reads files | Keep references one level deep |
| Non-standard frontmatter keys | Some runtimes reject the skill | Stick to `name`, `description`, and documented optional keys |
| Broken file references | Agent invents the missing content | Only reference files actually shipped with the skill |

---

## Complete Example

**Directory:**

```
create-api-endpoint/
├── SKILL.md
├── references/
│   ├── api-conventions.md
│   └── error-codes.md
└── assets/
    └── route-template.ts
```

**SKILL.md:**

```markdown
---
name: create-api-endpoint
description: >
  Use when creating new API routes, REST endpoints, or server-side handlers
  in Next.js App Router. Handles route creation, validation, error handling,
  TypeScript types, and test scaffolding.
---

# Create API Endpoint

## Prerequisites
- Confirm endpoint path and HTTP methods with user
- Check no existing route conflicts

## Workflow

### 1. Plan the route
- `/api/users` → `src/app/api/users/route.ts`
- `/api/users/[id]` → `src/app/api/users/[id]/route.ts`

### 2. Define types
Create types in `src/types/api/<resource>.ts`:
- Request body type (POST/PUT/PATCH)
- Response body type
- Query parameter type (GET with filters)

### 3. Create route handler
Use template from `assets/route-template.ts`. Every handler must:
- Validate request body with zod
- Return envelope: `{ data, error, meta }`
- Use appropriate HTTP status codes (see `references/error-codes.md`)

### 4. Create tests
Every endpoint needs:
- Happy path test per HTTP method
- Validation failure test
- Auth test (missing/invalid token)
- Not-found test (for path parameters)
Run: `npm test -- --testPathPattern="api/<resource>"`

### 5. Verify
1. `npm run lint`
2. `npx tsc --noEmit`
3. Run new tests
4. Summarize what was created
```

---

## Additional Resources

- Full specification, frontmatter field reference, and platform support notes: `references/specification-reference.md`
- Anti-pattern catalog with before/after examples: `references/anti-patterns.md`
