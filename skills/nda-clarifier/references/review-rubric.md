# NDA Review Rubric

Apply statuses clause by clause. The most restrictive status controls overall routing.

## Clause statuses

### `approved-match`

Use only when:

- An approved, current, applicable rule exists
- All required elements are present
- No prohibited qualifier or position appears
- Meaning is materially equivalent to an approved position
- Extraction and comparison confidence are high

Route contribution: `standard-process`.

### `approved-variation`

Use only when the difference falls entirely within a documented acceptable variation and
all variation conditions are met.

Route contribution: `standard-process`.

### `business-input-needed`

Use when the library provides a clear decision rule but a non-legal fact is missing, such
as the intended disclosure type, affiliate access, technical retention capability, or deal
stage.

Ask a focused factual question. Do not ask the business user to make a legal judgment.

Route contribution: `business-input-needed`, unless another finding requires legal review.

### `nonstandard-legal-review`

Use when the clause differs materially from the approved position or lies outside an
acceptable variation.

Route contribution: `legal-review-required`.

### `prohibited-position`

Use only when an applicable approved rule explicitly marks the observed position
prohibited or mandatory-escalation.

Route contribution: `legal-review-required`.

### `missing-required-clause`

Use when an applicable approved rule requires a provision and the NDA does not contain it.

Route contribution: `legal-review-required`.

### `unknown-position`

Use when no applicable rule addresses the clause, multiple rules conflict, or the clause
cannot be mapped confidently.

Route contribution: `legal-review-required`.

### `low-confidence`

Use when OCR, document quality, cross-references, handwritten changes, or ambiguous drafting
prevents reliable extraction or comparison.

Route contribution: `legal-review-required`.

### `incomplete-document`

Use for missing pages, exhibits, signature sections, referenced policies, or base documents
needed to interpret a redline.

Route contribution: `legal-review-required` or `unable-to-triage` when review cannot proceed.

## Confidence

- `high`: exact location and text are clear; applicable rule and boundary are unambiguous
- `medium`: text is readable but mapping or semantic effect requires interpretation
- `low`: extraction, applicability, or semantic effect is uncertain

Only high-confidence `approved-match` and `approved-variation` findings may contribute to
`standard-process`.

## Overall routing order

Apply the first matching route:

1. `unable-to-triage`: unreadable document or authority set cannot be established
2. `legal-review-required`: any legal-review status exists
3. `business-input-needed`: only unresolved business-input statuses remain
4. `standard-process`: every expected and observed clause is a high-confidence approved match
   or approved variation

Never return `standard-process` when:

- The clause library is a placeholder, draft, expired, or inapplicable
- Any expected category was not checked
- The NDA is incomplete
- Any finding has medium or low confidence
- A model response failed schema or citation validation

## Legal exception format

For every legal exception provide:

1. Clause category and status
2. NDA quote and location
3. Library rule ID/version
4. Exact deviation
5. Why the rule requires escalation
6. Applicable approved fallback ID, or state that none was found

Do not prioritize exceptions using invented risk scores. Use only priority or SLA values
explicitly supplied by the library.
