# Citation Rules

Inline citations make each material claim traceable to the evidence that supports it.

## Citation form

Assign stable source IDs in order of registration: `S01`, `S02`, and so on.

Place citations immediately after the supported statement:

```markdown
The policy applies to organizations above the stated threshold. [S04]
```

For several independent sources:

```markdown
Two independent datasets show the same directional change. [S03][S08]
```

## Material claims

Cite:

- Numbers, dates, thresholds, and rankings
- Laws, policies, standards, and product capabilities
- Market-size, adoption, cost, and performance statements
- Causal claims and forecasts
- Attributed opinions
- Comparative statements
- Claims that materially affect the recommendation

Common knowledge does not need a citation unless its definition or scope matters to the decision.

## Atomic support

A citation must support the exact nearby claim.

Bad:

```markdown
The market is growing rapidly, customers prefer option A, and regulation will tighten. [S01]
```

Good:

```markdown
The measured market grew 12% in the reported period. [S01]
In the surveyed segment, option A was preferred by 54% of respondents. [S02]
The regulator has proposed a new reporting requirement, but it is not yet final. [S03]
```

## Source register

For each source include:

- Source ID
- Title
- Author and publisher
- Publication date
- Access date
- URL or controlled internal identifier
- Source type
- Relevant pages, sections, tables, or timestamps
- Limitations and conflicts

Never fabricate missing metadata. Use `not available`.

## Quotes

- Quote exactly and preserve qualifiers.
- Cite page, section, paragraph, table, or timestamp when available.
- Keep quotes short enough to preserve analysis and respect source rights.
- Mark translated, OCR-derived, or transcript-derived text.
- Do not use quotation marks around a paraphrase.

## Secondary and primary sources

If a secondary source cites primary evidence, cite the primary source for the factual claim
after verifying it. Cite the secondary source only for its unique interpretation.

## Search snippets

Search snippets can be truncated, stale, or generated. They are not sufficient evidence.
Open the underlying source. If it cannot be retrieved, register the lead as unverified and
exclude it from recommendation-driving claims.

## Internal sources

Use controlled document IDs or access-controlled links. Mark the distribution level. Do not
copy confidential content into a broadly distributed brief when a citation is sufficient.

## Broken or inaccessible sources

If a source becomes inaccessible:

- Preserve its metadata and the date it was accessed
- Do not claim it was reverified
- Find an archived or replacement authoritative source when permitted
- Reduce confidence if support can no longer be checked

## Citation audit

Before delivery:

1. Resolve every inline source ID.
2. Confirm every source is cited at least once or remove it.
3. Confirm every recommendation-driving claim is cited.
4. Check that no citation supports a broader claim than the source.
5. Verify statistics, units, dates, scope, and qualifiers.
