# Agent Skills Specification Reference

This file documents the agentskills.io open standard as implemented across runtimes. Read it when you need authoritative answers about frontmatter fields, naming rules, directory layout, size limits, or platform-specific behavior.

## Contents

1. File and directory layout
2. Frontmatter — required fields
3. Frontmatter — optional fields
4. Name rules (full pattern)
5. Description rules (full constraints)
6. Body content rules
7. Reference, script, and asset directories
8. Platform support matrix
9. Loading and activation model
10. Versioning and changelogs
11. Common validation errors

---

## 1. File and directory layout

A skill is a directory. The directory name **is** the skill's identifier and must match the `name` field in frontmatter.

```
skill-name/
├── SKILL.md              # Required. The only file the runtime auto-discovers.
├── references/           # Optional. Markdown documents loaded on demand.
├── scripts/              # Optional. Executable code (any language).
└── assets/               # Optional. Templates, schemas, fixtures.
```

Rules:
- Only `references/`, `scripts/`, and `assets/` are part of the spec. Other directory names may be ignored or rejected.
- Subdirectories under those three folders are not portable. Keep all files exactly one level deep.
- Symlinks are not portable; use literal files.
- Filenames should be lowercase-with-hyphens to match the skill name convention.

## 2. Frontmatter — required fields

YAML frontmatter at the top of SKILL.md, fenced by `---` lines.

| Field         | Type   | Constraints                                                                 |
|---------------|--------|------------------------------------------------------------------------------|
| `name`        | string | 1–64 chars; matches `^[a-z0-9]+(-[a-z0-9]+)*$`; must equal directory name.  |
| `description` | string | 1–1024 chars; trigger style (see §5).                                       |

Both fields are required by every known runtime. Skills missing either are rejected at load time.

## 3. Frontmatter — optional fields

Use these only when they add genuine value. Inventing keys outside this list is an anti-pattern (see `anti-patterns.md` §9).

| Field           | Type           | Purpose                                                                                          |
|-----------------|----------------|--------------------------------------------------------------------------------------------------|
| `license`       | string         | SPDX identifier (e.g., `MIT`, `Apache-2.0`) or a path to a LICENSE file relative to the skill.   |
| `compatibility` | string \| list | Free-form environment constraints, e.g., `node>=20`, `requires: ["postgres", "drizzle-kit"]`.    |
| `allowed-tools` | list[string]   | Whitelist of tools the agent may invoke while this skill is active. Support varies (see §8).     |

## 4. Name rules (full pattern)

- Length: 1–64 characters.
- Allowed characters: lowercase `a-z`, digits `0-9`, single hyphens.
- Regex: `^[a-z0-9]+(-[a-z0-9]+)*$`. Consecutive hyphens, leading/trailing hyphens, and underscores are rejected.
- Style guidance (not enforced, but conventional):
  - Gerund form for process skills: `reviewing-code`, `generating-migrations`.
  - Verb-noun for action skills: `create-api-endpoint`, `deploy-staging`.
  - Avoid vague stems: `helper`, `utils`, `tools`, `data`, `stuff`.
- Must equal the parent directory name exactly. Most runtimes refuse to load a skill where these differ.

## 5. Description rules (full constraints)

- Length: 1–1024 characters. Aim for 2–4 sentences (~250–600 characters).
- Voice: third person. First/second person ("I can...", "You can...") is rejected as an anti-pattern.
- Content: WHEN to activate + WHAT capabilities exist. Never HOW the procedure works.
- Negative triggers: add `Do NOT use for ...` when adjacent requests would otherwise pull the skill in.
- Keywords: include the exact terms users are likely to type, plus 1–2 obvious synonyms.

The description is the **only** piece of the skill loaded at agent startup — typically as a routing entry of ~100 tokens. Everything else (body, references, scripts) is fetched lazily after activation.

## 6. Body content rules

- Length: soft limit 500 lines. Most runtimes warn above 500, hard-cap around 1000–1500.
- Style: procedural (steps to DO), not documentary (what things ARE).
- Structure: critical constraints first, then workflow, then references and examples.
- Terminology: pick one term per concept and use it throughout. Do not alternate between synonyms (e.g., "endpoint" vs. "route" vs. "handler").
- No time-sensitive content (dates, "currently", "as of"), no secrets (tokens, keys, passwords), no PII.

## 7. Reference, script, and asset directories

### `references/`

Markdown files loaded on demand when SKILL.md tells the agent to read them. Use for content the agent only needs in specific branches (style guides, error catalogs, full API references).

- Reference each file by its relative path: `references/error-codes.md`.
- For files over 100 lines, start with a `## Contents` table of contents.
- Files in `references/` are not auto-loaded; the agent must be instructed to read them.

### `scripts/`

Executable code in any language the host can run. Use for validation, codegen, formatting, anything where deterministic output beats LLM-generated code.

- Document dependencies inline at the top of each script (`# requires: python>=3.10, pyyaml`).
- Scripts should handle errors explicitly and exit with non-zero status on failure.
- In SKILL.md, state clearly whether the agent should **execute** the script or **read** it as reference.

### `assets/`

Static files the skill emits, copies, or templates from: code templates, schema files, prompt fragments, image assets, fixtures.

- Reference by relative path: `assets/route-template.ts`.
- Treat as read-only inputs; the skill should not modify files inside `assets/`.

## 8. Platform support matrix

Support is approximate and changes; check your runtime's release notes.

| Field / Feature      | Claude Code | Claude Agent SDK | Cursor | Gemini CLI | Generic agentskills.io |
|----------------------|-------------|------------------|--------|------------|------------------------|
| `name`               | yes         | yes              | yes    | yes        | required               |
| `description`        | yes         | yes              | yes    | yes        | required               |
| `license`            | yes         | yes              | yes    | yes        | optional               |
| `compatibility`      | partial     | partial          | partial| partial    | optional, free-form    |
| `allowed-tools`      | yes         | yes              | no     | partial    | optional               |
| `references/`        | yes         | yes              | yes    | yes        | required behavior      |
| `scripts/`           | yes         | yes              | yes    | partial    | required behavior      |
| `assets/`            | yes         | yes              | yes    | yes        | required behavior      |
| Project-level skills | `.claude/skills/` | `.claude/skills/` | `.cursor/skills/` | `.gemini/skills/` | `.<tool>/skills/` |
| User-level skills    | `~/.claude/skills/` | `~/.claude/skills/` | `~/.cursor/skills/` | `~/.gemini/skills/` | `~/.<tool>/skills/` |

Reserved built-in directories vary; never write into a path the host marks as system-managed.

## 9. Loading and activation model

1. At session start, the runtime indexes all skills in the user and project skill directories.
2. For each skill, only the frontmatter (`name` + `description`) is loaded into the routing context.
3. When the user sends a message, the runtime decides whether any skill's description matches.
4. If activated, the full SKILL.md body is loaded into context.
5. Reference, script, and asset files load only when SKILL.md or the agent explicitly requests them.

Implications:
- The description is the routing signal. If it doesn't match the user's phrasing, the skill is invisible.
- Anything in the body that the agent should have *before* deciding what to do must instead live in the description.
- Files in `references/` cost zero context until the agent reads them — exploit this for long content.

## 10. Versioning and changelogs

The spec does not define a `version` field. Conventional practice:
- Maintain a sibling `CHANGELOG.md` in the skill directory if changes are non-trivial.
- For breaking changes to a project-level skill, communicate in your team's normal channels — the agent has no built-in version awareness.
- Do not embed a `version: 1.2` line in frontmatter; use the changelog instead.

## 11. Common validation errors

| Error                                      | Cause                                                              | Fix                                                   |
|--------------------------------------------|--------------------------------------------------------------------|-------------------------------------------------------|
| `name does not match directory`            | Directory renamed without updating frontmatter, or vice versa.     | Make them identical.                                  |
| `name contains invalid characters`         | Uppercase, underscores, dots, or unicode in `name`.                | Use only `[a-z0-9-]`.                                 |
| `description exceeds 1024 characters`      | Description trying to be a tutorial.                               | Strip procedural detail; keep WHEN/WHAT only.         |
| `unknown frontmatter key`                  | Invented key like `metadata`, `tags`, `version`.                   | Remove or move into the body.                         |
| `referenced file not found`                | Path typo or file not shipped.                                     | Audit every relative path before release.             |
| `description uses first/second person`     | "I can help...", "You can use...".                                 | Rewrite in third person.                              |
| `skill not activating on expected phrase`  | Description missing the user's actual keywords.                    | Add synonyms; verify with the "When would you use..." | prompt. |
| `skill over-activating`                    | Description too broad, no negative trigger.                        | Narrow the trigger; add `Do NOT use for ...`.         |
