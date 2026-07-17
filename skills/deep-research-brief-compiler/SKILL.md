---
name: deep-research-brief-compiler
description: >
  Use when asked to research a consequential question, compare strategic options,
  investigate a topic across multiple sources, or compile research into an
  evidence-backed decision brief. Decomposes the question, uses approved search
  tools or supplied sources, maintains a source and claim ledger, scores confidence,
  resolves contradictions, and adds inline citations to material claims. Do not use
  for quick factual lookups, unsourced brainstorming, or decisions requiring only
  one authoritative document.
tags: [deep-research, decision-support, source-analysis, evidence-synthesis]
domain: research
---

# Deep Research Brief Compiler

Turn multi-source research into a decision-ready brief with traceable evidence.

## Critical rules

- Ask what decision the research must support before optimizing for topic coverage.
- Inspect available tools before asking the user to configure anything.
- Never invoke a named, paid, external, or internal search provider unless the user
  requested it or confirmed it is approved in the current environment.
- If tool availability is unclear, ask which search, browser, academic, news, filing,
  internal-knowledge, or URL-extraction plugins are configured and permitted.
- Continue with supplied files and public sources when no research plugin is available;
  state the resulting coverage limits.
- Treat search snippets as discovery leads, not final evidence.
- Cite the source that directly supports each material claim.
- Never invent a citation, URL, quote, author, publication date, or access result.
- Separate observed evidence, inference, assumption, and recommendation.
- Surface credible contradictory evidence; do not average it away.
- A confidence score is an evidence-quality score, not a statistical probability.
- Do not send confidential inputs to external tools without explicit authorization.

## Select the research mode

Infer the mode from the request. Ask only if depth materially affects time or coverage.

### Focused brief

Use for a bounded decision with a small number of options.

Defaults:

- Five to ten strong sources
- Current evidence unless historical context is required
- One primary market or jurisdiction
- Concise decision brief

### Deep brief

Use for high-impact, contested, cross-market, technical, regulatory, or long-horizon decisions.

Include:

- Broader source diversity
- Primary-source retrieval
- Contradiction analysis
- Alternative explanations
- Explicit stop conditions and residual unknowns

## Intake

Inspect the request and supplied context. Batch only unresolved questions:

1. What decision must be made, by whom, and by when?
2. Which options, constraints, evaluation criteria, markets, and time horizon matter?
3. What output depth and audience are required?
4. May configured external and internal research tools be used?
5. Are any sources, data classes, or providers prohibited?

Use `assets/research-intake-template.yaml` when the decision context is incomplete.

## Detect research capabilities

Read `references/tool-integration.md`.

Build a capability inventory before researching:

- General web search
- News search
- Academic or patent search
- Regulatory filings and official records
- URL extraction or site crawling
- Browser access
- Internal knowledge/search
- Document and spreadsheet reading
- Image/OCR or transcript extraction

If configured tools are visible, summarize the relevant options and use only approved
capabilities. If visibility is unavailable, ask the user whether plugins are configured
and provide `assets/tool-capability-template.yaml`.

Do not require a plugin. A plugin amplifies discovery and retrieval; it does not replace
source evaluation or citation validation.

## Frame the decision

Write a research charter:

```yaml
decision: "<decision to make>"
decision_owner: "<role>"
deadline: "<date or null>"
options: ["<option>"]
criteria: ["<criterion>"]
constraints: ["<constraint>"]
scope:
  markets: ["<market>"]
  time_window: "<window>"
  excluded_topics: ["<exclusion>"]
required_evidence: ["<evidence needed>"]
stop_conditions: ["<condition>"]
```

Confirm ambiguous decision criteria before collecting large amounts of evidence.

## Build the search plan

Read `references/source-strategy.md`.

Decompose the decision into research questions:

1. Baseline facts and definitions
2. Option-specific benefits and costs
3. Market, customer, technical, operational, financial, legal, or regulatory constraints
4. Failure modes and counterarguments
5. Comparative evidence and precedents
6. Unknowns that could change the decision

For each question, define the preferred source type, query variants, geography, date range,
and stopping condition. Search in parallel only when questions are independent.

## Collect and register sources

Prefer primary and authoritative evidence:

- Laws, regulations, standards, filings, official statistics, product documentation,
  original research, datasets, and direct company statements
- Then high-quality independent analysis with transparent methods
- Use news, commentary, forums, and social sources for leads, sentiment, or reported events,
  not as substitutes for stronger evidence

For every source, create a record in the evidence ledger using
`assets/evidence-ledger-template.json`:

- Stable source ID
- Title, publisher, author, URL, publication date, and access date
- Source type and scope
- Relevant excerpt or data location
- Known limitations, conflicts, sponsorship, and methodology
- Whether the full source was retrieved

Open and verify the underlying page. Do not cite a search-result snippet when the source
itself can be retrieved.

## Extract atomic claims

Break evidence into claims that can be supported or challenged independently.

Each claim record must contain:

- Stable claim ID
- One precise claim statement
- Claim type: `fact`, `estimate`, `causal`, `forecast`, `interpretation`, or `assumption`
- Supporting source IDs and exact evidence locations
- Contradicting source IDs
- Scope, date, population, geography, and qualifiers
- Confidence dimensions and rationale
- Decision relevance

Do not combine several propositions under one citation. Split compound statements.

## Triangulate and score confidence

Read `references/confidence-scoring.md`.

For every material claim:

1. Check whether cited sources directly support the exact wording.
2. Detect circular sourcing and count dependent sources once.
3. Seek an independent corroborating source for consequential claims.
4. Search for credible disconfirming evidence.
5. Reconcile differences in definitions, dates, samples, and jurisdictions.
6. Score authority, directness, corroboration, timeliness/fit, and consistency.
7. Apply contradiction or missing-method penalties.
8. Record both the score and a short rationale.

Label unresolved credible conflicts `disputed` regardless of numerical score.

## Synthesize for the decision

Organize findings by decision criterion, not by source.

For each option:

- Evidence-backed benefits
- Costs and implementation requirements
- Risks and reversibility
- Dependencies and assumptions
- Evidence gaps
- Conditions under which the option is preferable

Form a recommendation only when the evidence and decision criteria justify one. Otherwise
recommend a next experiment, data request, or decision gate.

## Cite every material claim

Read `references/citation-rules.md`.

Use inline source IDs immediately after the supported claim:

```markdown
Adoption increased from 18% to 27% in the measured cohort. [S03]
The result may not generalize beyond large enterprises. [S03][S11]
```

Include confidence after consequential claims:

```markdown
The proposed change is likely to reduce processing time under the tested workflow.
[S03][S11] **Confidence: high (8/10).**
```

Do not place one citation at the end of a paragraph containing multiple unsupported claims.

## Produce the decision brief

Follow `assets/decision-brief-template.md`.

Deliver:

1. Decision and recommendation
2. Executive evidence summary
3. Options assessed against decision criteria
4. Material claim ledger with confidence
5. Risks, contradictions, assumptions, and unknowns
6. What would change the recommendation
7. Recommended next actions
8. Source register

If the research cannot support a recommendation, say so directly.

## Validate

If scripts can run, execute:

```bash
python scripts/validate-evidence.py evidence-ledger.json decision-brief.md
```

Fix all validation errors before delivery. Then manually verify:

- Every material claim has an inline citation.
- Every source ID resolves to a real ledger record.
- Quotes and statistics match the source and scope.
- Confidence scores follow the rubric.
- Search snippets are not used as evidence.
- Contradictions and negative evidence are visible.
- The recommendation follows stated criteria.
- Tool and source coverage limitations are explicit.
- No confidential data was sent to an unauthorized provider.
