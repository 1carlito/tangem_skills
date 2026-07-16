# Company Context Schema

Company context turns a competitor landscape into a company-specific positioning analysis.
It is optional and must be supplied at runtime.

## Data handling

- Do not place real company data inside the distributed skill bundle.
- Use an approved local file, redacted paste, or authorized internal connector.
- Do not send internal data to an external provider without explicit approval.
- Exclude personal customer data and credentials.
- Quote only the minimum internal evidence needed in the final report.

## Minimum useful context

For a positioning comparison, request:

- Company and product names
- Target markets and languages
- Priority personas
- Jobs-to-be-done and customer problems
- Current positioning pillars
- Approved and prohibited claims
- Available proof points
- Current campaign messages and channels

Performance data is optional. Without it, compare message presence and strategic fit—not
effectiveness.

## YAML structure

Use `assets/company-context-template.yaml`.

### Company

Basic organization, market, language, and analysis-owner information.

### Products

For each product:

- Name and category
- Intended markets
- Capabilities the company can substantiate
- Limitations that must not be hidden

### Personas

For each priority audience:

- Role or segment
- Jobs-to-be-done
- Pains
- Desired outcomes
- Common objections

### Positioning

Include current pillars and messages, each with:

- Short label
- Intended audience
- Message
- Supporting proof-point IDs
- Approved channels

### Claims policy

- `approved`: wording or claim families marketing may use
- `prohibited`: statements that must not be recommended
- `requires_review`: claim categories requiring legal/compliance approval

### Proof points

Each proof point needs an ID, statement, source, approval status, applicable markets, and
expiration/review date when relevant. Unsupported internal assertions are not proof.

### Campaign inventory

For each current or recent campaign:

- Campaign ID
- Product and channel
- Audience
- Headline/body/CTA
- Landing URL
- Formats, markets, languages, and dates
- Positioning pillar IDs

### Performance

Optional records may include impressions, spend, CTR, CVR, CPA/CAC, and revenue. Every
record must include its attribution model, window, currency, and known caveats.

Do not compare metrics across channels or attribution models as though they are equivalent.

## Validation questions

Before using the context, confirm:

1. Which fields are authoritative versus drafts?
2. Which markets and date ranges are current?
3. Are claims and proof points approved for external marketing?
4. Is performance data comparable across included campaigns?
5. Are any products, launches, or results confidential?

If answers are unavailable, lower confidence and name the validation required.

## Analysis boundary

Company context supports conclusions such as:

> The company has an approved proof point for an outcome that was not evidenced in the
> covered competitor ads.

It does not support:

> Competitors cannot provide that outcome.

Absence from the collected ads is evidence of absence in the covered sample only.
