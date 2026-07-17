# Company Clause Library Schema

The clause library is the sole authority for deciding whether an NDA position is standard.
The bundled template contains placeholders only and is not approved legal guidance.

## Library metadata

Require:

- `library_id` and `version`
- `status`: only `approved` permits standard routing
- Legal owner and approver
- Effective and expiry dates
- Applicable entities, NDA directions, jurisdictions, and transaction types
- Source document or policy reference

An expired, draft, or unmatched library routes the NDA to legal.

## Rule structure

Each rule needs:

- Stable `rule_id`
- Clause `category`
- Applicability conditions
- Required elements
- Approved position description
- Approved text fingerprints or examples
- Acceptable semantic variations and their boundaries
- Prohibited positions
- Business facts that affect classification
- Approved fallback text, if any
- Escalation route and owner

The model must compare meaning, qualifiers, exceptions, duration, scope, and affected parties.
Keyword overlap alone is insufficient.

## Applicability

Applicability may depend on:

- Company legal entity
- Mutual or one-way NDA direction
- Receiving or disclosing posture
- Governing jurisdiction
- Counterparty or transaction type
- Data sensitivity
- Purpose and deal stage
- Affiliate or representative access
- Effective date

If two applicable rules conflict, route to legal and cite both.

## Acceptable variation boundaries

Write boundaries as reviewable conditions, not vague labels.

Weak:

```yaml
acceptable_variations:
  - reasonable changes
```

Better schema:

```yaml
acceptable_variations:
  - id: "<VARIATION_ID>"
    description: "<LEGAL_APPROVED_DESCRIPTION>"
    required_elements:
      - "<ELEMENT_THAT_MUST_REMAIN>"
    disallowed_qualifiers:
      - "<QUALIFIER_THAT_CHANGES_THE_POSITION>"
    applies_when:
      - field: "<INTAKE_FIELD>"
        operator: "<equals|includes>"
        value: "<EXPECTED_VALUE>"
```

All actual content must be authored and approved by the organization's legal team.

## Fallback language

Fallback text must include:

- Stable fallback ID
- Verbatim approved text
- Applicable conditions
- Approval owner
- Effective/expiry dates
- Whether business confirmation is required

The skill may quote applicable fallback text. It must not edit or blend fallbacks.

## Escalation

Each rule should define:

- Status for exact/semantic matches
- Status for an allowed variation
- Status for missing business facts
- Status for prohibited or unknown positions
- Legal queue or owner
- Optional urgency/SLA metadata

Do not use numeric risk averaging to override a mandatory escalation.

## Change control

- Version every approved update.
- Preserve prior versions for auditability.
- Record approval date and owner.
- Retire superseded rules explicitly.
- Do not silently mutate rules used in completed reviews.
- Include the library version in every triage report.

## Placeholder safety

The included template uses angle-bracket placeholders and
`status: placeholder-not-approved`. A placeholder library can validate data shape but can
never produce `standard-process`.
