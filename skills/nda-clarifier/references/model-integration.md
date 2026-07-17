# Model Integration Placeholder

This bundle intentionally contains no model SDK call, endpoint, model ID, or credential.
Connect it to an approved model gateway at runtime.

## Important Bedrock note

Amazon Bedrock commonly authenticates AWS API requests with IAM credentials and SigV4,
although an organization may expose Bedrock through an internal gateway or another
credential mechanism. Do not assume an API-key format. Let the deployment environment
provide authentication through its approved secret and identity system.

## Integration boundary

The skill expects one logical operation:

```text
analyze_nda_against_clause_library(request) -> structured_response
```

The host implementation may use:

- An approved Amazon Bedrock model
- An internal legal-AI gateway
- An approved model exposed through MCP
- The host model in an authorized workspace

Provider selection belongs to deployment configuration, not `SKILL.md`.

## Request construction

Start from `assets/model-request-template.json`. At runtime replace placeholders with:

- NDA text plus page/section boundaries
- Intake facts
- Applicable approved clause rules only
- Required output schema
- Document and library identifiers

Do not include irrelevant internal policy or unrelated contracts. Minimize sensitive data.

The system instruction must require:

- Evidence quotes and locations
- Library rule IDs and versions
- One allowed status per clause
- `not-found` or `unknown-position` instead of guessed content
- No legal conclusions
- No novel fallback drafting
- Structured JSON only

## Response validation

Reject the model response unless:

- It parses as the expected JSON schema
- Every comparison maps to an extracted clause or expected missing category
- Every NDA quote exists at the cited location
- Every rule ID/version exists in the supplied applicable library
- Every status is allowed by `references/review-rubric.md`
- Approved fallback text exactly matches the cited library fallback
- The overall route follows the routing order

On validation failure, retry only through the approved gateway with a correction request or
route to legal. Never repair unsupported legal findings silently.

## Credential placeholders

The template contains:

```json
{
  "provider": "<MODEL_PROVIDER>",
  "model": "<MODEL_ID>",
  "endpoint": "<APPROVED_MODEL_GATEWAY>",
  "credentials_source": "<HOST_MANAGED_SECRET_OR_IDENTITY_REFERENCE>"
}
```

These are configuration labels, not values to commit.

Do not put any of the following in the skill bundle:

- AWS access key ID or secret access key
- AWS session token
- API key
- Bearer token
- Private endpoint credentials
- Customer NDA text
- Production clause library

## Suggested deployment contract

The deployment team should own:

- Region and model selection
- IAM role, SigV4 signing, or gateway authentication
- Encryption and data residency
- Logging and retention controls
- Model invocation timeout and retry policy
- Model-version pinning
- Audit record storage
- Human-review policy

The legal team should own:

- Clause library content and approval
- Applicability rules
- Fallback text
- Escalation policy
- Acceptance tests and review samples

## Failure behavior

If the gateway is unavailable, credentials are missing, access is denied, or the model
response is invalid:

1. Do not fall back to an unapproved external model.
2. Preserve the document and partial deterministic extraction.
3. Return `unable-to-triage` or `legal-review-required`.
4. Report the technical failure without exposing secret values.
