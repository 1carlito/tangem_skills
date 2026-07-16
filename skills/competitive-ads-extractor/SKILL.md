---
name: competitive-ads-extractor
description: >
  Use when asked to collect, classify, compare, or analyze competitors' live
  advertising, ad-library exports, campaign creative, messaging themes, or
  positioning gaps. Handles source-aware ad collection, provenance, messaging
  tags, clustering, internal-positioning comparison, and opportunity briefs.
  Do not use for general market research, writing ads from scratch, or analyzing
  the user's own campaign performance without a competitive-ad component.
tags: [competitive-intelligence, advertising, positioning, messaging-analysis]
domain: marketing
---

# Competitive Ads Extractor

Analyze competitor advertising without overstating what the available data proves.

## Critical rules

- Ask only for missing information that would materially change the analysis.
- Never invoke a named third-party provider unless the user explicitly requests or approves it.
- Prefer user-provided exports and approved official connectors over scraping.
- Do not bypass authentication, CAPTCHAs, access controls, rate limits, or platform restrictions.
- Preserve a source URL and retrieval date for every ad. Exclude unsourced ads from findings.
- Separate observed copy and metadata from model-derived tags and interpretations.
- Never infer spend, targeting, reach, conversion, or performance unless the source provides it.
- Ad longevity and variant count are activity signals, not proof of performance.
- Never copy a competitor's creative verbatim into a recommendation.
- Treat company context and campaign performance as confidential. Use only approved files or connectors.

## Choose an analysis mode

Infer the mode from the request. Ask only if the intended depth is unclear.

### Quick scan

Use when the user wants a fast competitor overview.

Defaults:

- Active ads or the most recent 90 days
- The user's primary market and language
- Text and image ads first
- Up to 50 ads per competitor
- Competitor-only landscape when company context is absent

### Full analysis

Use when the user wants company-specific positioning gaps, channel comparisons,
or testable campaign opportunities. Request company context using
`assets/company-context-template.yaml`. Performance data is optional.

## Intake

First inspect the request and supplied files. Batch only unresolved required questions:

1. Which competitors or advertiser aliases should be included?
2. Which markets, languages, channels, and date range matter?
3. What source access exists: uploaded export, ad-library URLs, browser, or approved connector?
4. Is approved company marketing context available?

Do not block a competitor-only scan because company context is unavailable. State that
the result will contain market hypotheses rather than company-specific gaps.

Use `assets/competitor-seed-template.csv` when the competitor list is ambiguous.
Use `references/company-context-schema.md` before requesting internal data.

## Detect capabilities and establish coverage

Read `references/source-adapters.md` before collecting live data.

Create a short coverage statement containing:

- Sources available and inaccessible
- Markets, channels, languages, and dates covered
- Media extraction available: text, image vision/OCR, video transcription
- Known source limitations

Ask for approval before using a paid, provider-specific, or third-party connector that
the user did not name. Web search can discover advertisers and landing pages, but must
not be represented as a complete ad inventory.

## Collect ad records

For every ad, preserve these fields when available:

```json
{
  "record_id": "stable-local-id",
  "source": "source-name",
  "source_url": "https://...",
  "retrieved_at": "ISO-8601 timestamp",
  "advertiser": "Advertiser name",
  "advertiser_id": null,
  "ad_id": null,
  "platform": "platform-name",
  "markets": ["US"],
  "languages": ["en"],
  "status": "active",
  "first_seen": null,
  "last_seen": null,
  "format": "video",
  "headline": null,
  "body": null,
  "cta": null,
  "landing_url": null,
  "media_urls": [],
  "derived_text": null,
  "source_metrics": {},
  "source_notes": null
}
```

Keep unknown values as `null` or empty arrays. Never manufacture missing metadata.

If image vision/OCR is available, store extracted on-image text in `derived_text` and
label it as derived. If transcription is available, append spoken and on-screen text
with timestamps when possible. Continue without those fields when unavailable.

For JSON or CSV exports, execute `scripts/normalize-ads.py` to canonicalize URLs,
normalize values, and deduplicate exact records:

```bash
python scripts/normalize-ads.py input.json normalized-ads.json
```

The script accepts JSON arrays or CSV files. Review its warnings; do not silently drop
records that differ in hook, offer, CTA, format, market, or active dates.

## Tag the messaging

Read `references/tag-taxonomy.md` before tagging.

Tagging means assigning structured analytical labels to the argument each ad makes.
For each ad, extract:

- Audience/persona
- Job-to-be-done
- Pain/problem
- Promise/outcome
- Product mechanism
- Proof type
- Objection addressed
- Offer/incentive
- CTA
- Funnel stage
- Emotional frame
- Creative format
- Claim/risk flag

Every tag must include:

- `value`: concise normalized label
- `evidence`: a direct quote or observable creative detail
- `confidence`: `high`, `medium`, or `low`

Use `not-observed` when the ad provides no evidence. Do not force a tag.

## Cluster messages

Group ads by the combination of audience, problem, promise, mechanism, and proof.

For each cluster:

1. Count unique advertisers, ads, variants, formats, and markets.
2. Record earliest and latest observed dates when supplied.
3. Identify the repeated message using representative sourced evidence.
4. Distinguish persistent themes from isolated experiments.
5. Note whether apparent repetition may result from incomplete source coverage.

Do not call a theme successful, winning, or high-performing without actual performance data.

## Compare against company context

When approved company context exists, compare competitor clusters against:

- Target personas and jobs-to-be-done
- Current positioning pillars and product capabilities
- Approved and prohibited claims
- Available proof points
- Current campaign messages, channels, and formats
- Optional performance data and attribution limitations

Classify each evidence-backed observation as one of:

- `saturated-territory`: many competitors use substantially the same message
- `defensible-differentiation`: company has a supported capability or proof competitors do not show
- `unclaimed-audience-problem`: an important approved segment or problem is weakly addressed
- `missing-proof`: a message exists, but credible substantiation is absent
- `channel-format-gap`: a relevant message or format is absent in a covered channel
- `risky-claim-territory`: an attractive message lacks approval, evidence, or legal safety

Without company context, never use these classifications as conclusions. Present them as
`hypothesis-for-validation` and state what internal evidence is needed.

## Produce the report

Follow `assets/report-template.md`. Deliver:

1. Executive summary
2. Scope and coverage
3. Sourced ad inventory
4. Messaging cluster map
5. Positioning comparison or competitor-only hypotheses
6. Three to five opportunity briefs
7. Limitations and validation needs

Each important finding must cite record IDs and source URLs. Each opportunity brief must
include the audience, observed gap, company evidence required, test concept, success
metric, and risk. Keep observation, interpretation, and recommendation visibly separate.

## Final verification

Before returning the report, verify:

- Every included ad has provenance and a retrieval date.
- Derived OCR/transcript text is distinguishable from source metadata.
- Tags have evidence and confidence.
- Claims about activity are not presented as performance claims.
- Company-specific gaps use approved company context.
- Recommendations do not reproduce competitor copy.
- Missing channels and inaccessible sources are explicit.
- Sensitive internal data is not reproduced unnecessarily.
