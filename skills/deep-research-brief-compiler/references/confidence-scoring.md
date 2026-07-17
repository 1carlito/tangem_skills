# Confidence Scoring

Score the quality of evidence supporting each material claim. The score is not a probability
that the claim is true.

## Dimensions

### Authority: 0–3

- `3`: authoritative primary source or original research with suitable methods
- `2`: credible independent secondary analysis or reporting with transparent sourcing
- `1`: relevant expert commentary, trade source, or limited-method evidence
- `0`: anonymous, unverifiable, promotional-only, or unknown provenance

Judge authority for the specific claim. A company is authoritative about its announced
features, but not necessarily about comparative superiority.

### Directness: 0–2

- `2`: source directly measures, states, or documents the claim
- `1`: claim is a bounded inference from relevant evidence
- `0`: evidence is indirect, anecdotal, or does not support the wording

### Independent corroboration: 0–2

- `2`: at least two materially independent evidence chains support the claim
- `1`: one strong source or dependent corroboration
- `0`: no supporting source

Do not count syndicated or circular sources independently.

### Timeliness and scope fit: 0–2

- `2`: date, population, geography, definitions, and decision context fit
- `1`: partially applicable with explicit caveats
- `0`: stale for the question, materially mismatched, or unspecified

### Consistency: 0–1

- `1`: no credible unresolved contradiction
- `0`: material conflict, unstable estimate, or inconsistent definitions

## Penalties

Subtract:

- `2`: credible contradictory evidence is unresolved
- `1`: material methodology is unavailable
- `1`: the claim relies on a source with a direct undisclosed or unmanaged conflict
- `1`: exact evidence location cannot be verified

Minimum score is zero.

## Labels

- `high`: 8–10
- `medium`: 5–7
- `low`: 2–4
- `unsupported`: 0–1
- `disputed`: credible sources materially conflict; use regardless of numerical score

Only high- and medium-confidence claims should drive a recommendation. Low-confidence claims
may identify risks or research needs. Unsupported claims must not appear as facts.

## Claim score object

```json
{
  "authority": 3,
  "directness": 2,
  "corroboration": 2,
  "timeliness_scope_fit": 1,
  "consistency": 1,
  "penalties": 1,
  "total": 8,
  "label": "high",
  "rationale": "Primary data and independent analysis agree; geography only partially matches."
}
```

Validate:

```text
total = max(0, authority + directness + corroboration
               + timeliness_scope_fit + consistency - penalties)
```

## Forecasts and causal claims

Apply extra caution:

- Distinguish forecasts from observed outcomes
- Record assumptions and forecast date
- Prefer ranges over false precision
- Require a causal design or strong mechanism evidence before using causal language
- Downgrade claims that merely convert correlation into causation

## Updating confidence

Recalculate when:

- A new independent source is verified
- A source is corrected, retracted, or superseded
- Scope or decision criteria change
- Contradictory evidence is resolved
- An assumption becomes observed data

Preserve the earlier rationale in the audit record when the brief is versioned.
