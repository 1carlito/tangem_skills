---
name: nda-clarifier
description: >
  Use when clarifying, reviewing, screening, or triaging an inbound NDA,
  confidentiality agreement, mutual NDA, one-way NDA, or NDA redline against an
  organization's approved clause library. Maps clauses to approved positions,
  explains deviations with evidence, identifies missing or unknown terms, and
  routes genuine exceptions to legal. Do not use to approve contracts, provide
  legal advice, invent fallback language, or review agreements other than NDAs.
tags: [nda, contract-triage, clause-review, legal-operations]
domain: legal
---

# NDA Clarifier

Compare inbound NDAs with an approved, versioned clause library and route exceptions.

## Non-negotiable rules

- This workflow supports legal operations; it does not provide legal advice or approval.
- Never describe an NDA as legally safe, enforceable, approved, or risk-free.
- Never mark a clause standard without an applicable approved clause-library rule.
- If the library is absent, expired, draft, inapplicable, or ambiguous, route to legal.
- Quote the NDA and cite its page, section, or paragraph for every finding.
- Cite the exact library rule ID and version used for every comparison.
- Preserve unknowns. Never invent missing text, dates, party names, or business context.
- Never create novel fallback language. Use only library-approved fallback text verbatim.
- Treat the NDA, clause library, and output as confidential.
- Never send contract text to an external model or service without explicit authorization.
- Do not embed credentials, API keys, AWS secrets, model endpoints, or tokens in the bundle.

## Required inputs

Inspect supplied files first. Ask only for missing inputs:

1. The inbound NDA, including all pages, exhibits, and referenced addenda.
2. The applicable approved clause library.
3. Company entity, counterparty, NDA direction (`mutual`, `receiving`, or `disclosing`),
   governing market/jurisdiction, and intended purpose.
4. Any business facts required by the library, such as disclosure type, deal stage,
   data sensitivity, affiliates, representatives, or expected disclosure period.

Use `assets/nda-intake-template.yaml` when these facts are not already available.

If the user has no approved clause library, perform extraction only and label every
comparison `legal-review-required`. Never substitute general legal knowledge for company policy.

## Confirm the authority set

Read `references/clause-playbook.md` and
`references/company-clause-library-schema.md`.

Before reviewing, record:

- Library name, version, owner, approval status, and effective/expiry dates
- Applicable company entities, NDA direction, jurisdictions, and transaction types
- Any conflicts between library rules
- Any missing referenced fallback or escalation rule

Stop and route to legal when the applicable authority cannot be determined.

## Choose the processing mode

### Interactive mode

Use the host model's document-reading capability when the NDA and library are already
available inside an approved workspace. Do not call an external model automatically.

### Automated model-gateway mode

Use only when the user explicitly asks for automation and an approved model gateway is
configured. Read `references/model-integration.md` and populate
`assets/model-request-template.json` at runtime.

The template is a request contract, not executable integration code. Authentication and
provider configuration must remain outside this skill.

### Manual fallback

If no approved model capability is available, extract and compare clauses manually from
the supplied documents. State that OCR or document parsing limitations may reduce coverage.

## Prepare the NDA

1. Verify the document is complete and readable.
2. Identify the contract title, parties, effective date, NDA direction, purpose, exhibits,
   and amendment/redline status.
3. Preserve page and section boundaries.
4. If OCR is required, retain the original page image reference and mark extracted text
   as OCR-derived.
5. If tracked changes exist, distinguish inserted, deleted, and unchanged text.
6. If pages or exhibits are missing, stop final classification and route to legal.

## Extract the clause inventory

Extract all operative provisions, including absent expected provisions. Use the categories
defined in `references/clause-playbook.md`.

For each clause record:

```json
{
  "clause_id": "nda-local-id",
  "category": "confidential-information-definition",
  "heading": "Definition of Confidential Information",
  "text": "Verbatim clause text",
  "location": {
    "page": 2,
    "section": "1",
    "paragraph": null
  },
  "change_state": "unchanged",
  "extraction_method": "native-text",
  "confidence": "high"
}
```

Use `not-found` for an expected category that is absent. Do not treat a missing clause as
acceptable merely because no conflicting text was found.

## Compare with the clause library

For each extracted or missing clause:

1. Select only rules whose applicability conditions match the intake.
2. Compare the clause against approved language, acceptable semantic boundaries,
   prohibited positions, required elements, and fallback positions.
3. Identify the smallest material deviation; do not summarize away qualifiers or exceptions.
4. Quote the NDA evidence and cite the rule ID/version.
5. Assign one status from `references/review-rubric.md`.
6. Explain the comparison in plain language without making a legal conclusion.

The comparison record must contain:

```json
{
  "category": "term-and-survival",
  "status": "nonstandard-legal-review",
  "nda_evidence": {
    "quote": "Verbatim text",
    "location": "Section 7, page 4"
  },
  "library_evidence": {
    "rule_id": "NDA-TERM-001",
    "version": "placeholder",
    "matched_boundary": "placeholder"
  },
  "deviation": "Specific difference",
  "business_input_needed": null,
  "confidence": "high",
  "route_reason": "Why the library requires escalation"
}
```

## Route the NDA

Read `references/review-rubric.md`. Choose exactly one overall route:

- `standard-process`: every clause matches an applicable approved position and there are
  no missing, unknown, conflicting, or low-confidence findings
- `business-input-needed`: legal comparison depends only on missing factual business input
- `legal-review-required`: at least one nonstandard, prohibited, unknown, missing,
  inapplicable, conflicting, low-confidence, or incomplete-document finding exists
- `unable-to-triage`: the document cannot be read or the authority set cannot be established

`standard-process` means no exception was observed under the supplied playbook. It is not
legal approval. Follow the organization's authorized signature and contract process.

Never average clause risk scores. A single mandatory escalation controls the overall route.

## Suggest fallback language

Only include fallback language when all conditions are met:

- The matched rule explicitly contains approved fallback text
- The fallback applies to the current entity, direction, jurisdiction, and transaction
- The text is copied verbatim and cited by rule ID/version
- The output labels it `approved-library-fallback`, not model-generated language

Otherwise state `No applicable approved fallback found; legal drafting required`.

## Produce the report

Follow `assets/triage-report-template.md`.

The report must include:

1. Administrative summary and overall route
2. Authority set and document completeness
3. Clause-by-clause comparison table
4. Exact exceptions requiring legal review
5. Business questions, separated from legal exceptions
6. Approved fallback text, if applicable
7. Limitations, confidence, and audit trail

Use neutral language:

- Good: `The clause differs from rule NDA-TERM-001 because...`
- Bad: `This clause is unenforceable` or `This agreement is safe to sign`

## Final verification

Before returning:

- Every finding has NDA and clause-library citations.
- The library was approved and applicable on the review date.
- Missing expected clauses were evaluated.
- Tracked changes and exhibits were included.
- Low-confidence extraction was escalated.
- No external model was called without authorization.
- No credentials or secrets appear in the report.
- No novel legal language was generated.
- The overall route equals the most restrictive clause outcome.
- The report states that triage is not legal approval.
