# Messaging Tag Taxonomy

Use this taxonomy to describe the argument an ad makes, not merely its keywords.

## Tag object

Each analytical tag uses:

```json
{
  "value": "normalized-kebab-case-label",
  "evidence": "Direct quote or observable creative detail",
  "confidence": "high"
}
```

Confidence:

- `high`: directly stated in text or unmistakably shown
- `medium`: strongly implied by copy and creative together
- `low`: plausible but ambiguous; use sparingly
- Use `not-observed` instead of inventing a weak interpretation

## Core tags

### Audience/persona

The person, team, role, or customer segment being addressed.

Evidence: explicit role names, industry terms, depicted context, or direct address.

Examples: `finance-leaders`, `first-time-buyers`, `distributed-engineering-teams`.

Do not infer demographics from appearance.

### Job-to-be-done

The progress the audience wants to make in a situation.

Use an action-oriented label: `prepare-board-report`, `launch-campaign-faster`,
`reduce-checkout-abandonment`.

### Pain/problem

The obstacle, cost, risk, or frustration emphasized.

Examples: `manual-reporting`, `unpredictable-costs`, `slow-implementation`.

### Promise/outcome

The desired result promised by the ad.

Examples: `faster-time-to-value`, `lower-operating-cost`, `greater-control`.

Keep the promise separate from the mechanism used to achieve it.

### Product mechanism

The feature, process, or distinctive method claimed to produce the outcome.

Examples: `automated-data-sync`, `expert-review`, `one-click-setup`.

### Proof type

How the ad supports its promise:

- `customer-testimonial`
- `customer-logo`
- `quantified-result`
- `product-demonstration`
- `independent-rating`
- `certification-or-award`
- `case-study`
- `specificity-without-source`
- `no-proof-observed`

Record the actual proof in evidence. A precise number is not automatically credible proof.

### Objection addressed

The concern the message attempts to remove.

Examples: `too-expensive`, `hard-to-switch`, `security-risk`, `requires-training`.

### Offer/incentive

The commercial reason to act now.

Examples: `free-trial`, `limited-discount`, `free-consultation`, `guarantee`,
`no-offer-observed`.

### CTA

Normalize the requested action while retaining the original CTA text separately.

Examples: `start-trial`, `book-demo`, `learn-more`, `shop-now`, `download-guide`.

### Funnel stage

- `awareness`: frames a category, problem, or identity
- `consideration`: explains capabilities, comparisons, or proof
- `conversion`: presents an offer or immediate action
- `retention`: targets existing customers or expanded use
- `unclear`

### Emotional frame

The primary emotional angle:

- `relief`
- `confidence`
- `control`
- `urgency`
- `fear-of-loss`
- `status`
- `belonging`
- `curiosity`
- `simplicity`
- `aspiration`
- `neutral`

### Creative format

Describe the execution:

- `product-demo`
- `customer-testimonial`
- `founder-led`
- `comparison`
- `problem-solution`
- `before-after`
- `educational`
- `social-proof`
- `offer-led`
- `static-product`
- `user-generated-style`
- `other`

### Claim/risk flag

Flag claims for review without making a legal conclusion:

- `absolute-claim`
- `comparative-superiority`
- `quantified-performance`
- `guarantee`
- `health-or-safety`
- `financial-outcome`
- `unverifiable-proof`
- `regulated-topic`
- `none-observed`

## Message signature

Create a signature for clustering:

```text
audience + pain + promise + mechanism + proof-type
```

Two ads belong in the same cluster when the underlying argument is materially the same,
even if wording and visual execution differ. Keep separate clusters when the audience,
problem, offer, or reason-to-believe changes.

## Example

Observed ad:

> Stop wasting Mondays building reports. Acme turns CRM data into a board-ready
> dashboard in five minutes. Start free.

Tags:

```json
{
  "audience": {
    "value": "operations-leaders",
    "evidence": "Board-ready dashboard and weekly reporting context",
    "confidence": "medium"
  },
  "pain": {
    "value": "manual-reporting",
    "evidence": "Stop wasting Mondays building reports",
    "confidence": "high"
  },
  "promise": {
    "value": "faster-board-reporting",
    "evidence": "board-ready dashboard in five minutes",
    "confidence": "high"
  },
  "mechanism": {
    "value": "automated-crm-data-transformation",
    "evidence": "turns CRM data into a ... dashboard",
    "confidence": "high"
  },
  "proof_type": {
    "value": "specificity-without-source",
    "evidence": "in five minutes",
    "confidence": "high"
  },
  "offer": {
    "value": "free-trial",
    "evidence": "Start free",
    "confidence": "high"
  },
  "cta": {
    "value": "start-trial",
    "evidence": "Start free",
    "confidence": "high"
  },
  "funnel_stage": {
    "value": "conversion",
    "evidence": "Immediate free-start CTA",
    "confidence": "high"
  },
  "emotional_frame": {
    "value": "relief",
    "evidence": "Stop wasting Mondays",
    "confidence": "medium"
  }
}
```
