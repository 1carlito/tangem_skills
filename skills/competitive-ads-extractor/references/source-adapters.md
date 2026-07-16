# Source Adapters

Select sources by capability and authorization, not by a hardcoded provider preference.
Confirm current platform documentation and organizational approval before use.

## Source priority

1. User-provided exports, URLs, screenshots, or media
2. Approved official transparency library or API
3. Approved organization connector
4. Explicitly authorized third-party connector
5. Public browser collection when permitted

Do not use a paid or named third-party provider merely because its tool is available.
Ask first unless the user explicitly requested it.

## Capability detection

Look for these capabilities in the host:

- `ad-library-search`: query ads by advertiser, keyword, market, status, or date
- `read-webpage`: inspect public ad and landing-page pages
- `web-search`: discover advertiser aliases and landing pages
- `image-vision-or-ocr`: extract on-image text and observable creative cues
- `video-transcription`: recover spoken and on-screen messaging
- `read-files`: process CSV, JSON, screenshots, and company context
- `run-script`: normalize and deduplicate exports
- `internal-marketing-data`: retrieve approved brand and campaign context

Use the closest host-specific tools. If a capability is missing, continue with reduced
coverage and state the limitation.

## Platform considerations

### Meta Ad Library

The public library can expose commercial ads, while official API coverage and eligibility
may differ by ad category and region. Do not assume an available official endpoint covers
all commercial competitor ads.

Preferred inputs:

- User-provided Ad Library URLs or exports
- Approved official API results where the requested category is supported
- Explicitly approved third-party connector

Record country, platform placement, active status, dates, advertiser/page identity, and
creative variants when available.

### Google Ads Transparency Center

The public Transparency Center can expose ads across Google properties. General
programmatic access may require an approved third-party connector or user-provided export.

Do not invoke a third-party search/API provider unless the user explicitly requests or
approves it. Preserve advertiser identity, region, format, date range, and source URL.

### TikTok Commercial Content Library

Official commercial-content access may require application approval and OAuth. Public
coverage can vary by market.

Use:

- An approved official connector
- User-provided library URLs or exports
- An explicitly approved third-party connector

Video analysis is incomplete without transcript or on-screen text extraction.

### LinkedIn Ad Library

The public Ad Library is useful for manual research. Access to an advertiser's own
campaign data does not imply API access to competitors' ads.

Use user-provided results, permitted public browsing, or an explicitly approved connector.
Keep paid-media metadata separate from inferences about account targeting.

### Search engines and research connectors

Web search is useful for:

- Discovering official advertiser names and aliases
- Finding campaign announcements and landing pages
- Verifying claims against first-party sources
- Locating public ad-library pages

Search results are not a complete ad inventory. Never calculate channel share or campaign
frequency from ordinary search-result counts.

## Adapter output contract

Convert each source result to:

```json
{
  "record_id": "source:advertiser:ad-or-content-hash",
  "source": "human-readable-source",
  "source_url": "public-or-approved-reference",
  "retrieved_at": "2026-01-01T00:00:00Z",
  "advertiser": "Name shown by source",
  "advertiser_id": null,
  "ad_id": null,
  "platform": "platform",
  "markets": [],
  "languages": [],
  "status": null,
  "first_seen": null,
  "last_seen": null,
  "format": null,
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

Rules:

- Keep source-provided fields verbatim before normalization.
- Use `source_metrics` only for metrics explicitly returned by the source.
- Do not reinterpret estimated ranges as exact values.
- Keep OCR and transcripts in `derived_text`; do not merge them invisibly into source copy.
- Store retrieval failures in the coverage log, not as empty ads.

## Coverage statement template

```markdown
## Coverage
- Competitors:
- Sources used:
- Sources unavailable:
- Markets/languages:
- Date window:
- Ad status:
- Media processed:
- Collection timestamp:
- Important source limitations:
```

## Access and compliance

- Follow platform terms, robots directives, rate limits, and organizational policy.
- Stop when authentication, CAPTCHA, or access approval is required.
- Never request that a user paste an API secret into the skill or report.
- Configure secrets in the host's approved secret manager or connector.
- Minimize retention of media and internal data.
- Mark third-party-derived results so reviewers can assess source reliability.
