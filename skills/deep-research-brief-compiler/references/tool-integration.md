# Research Tool Integration

This skill is provider-neutral. Map available host tools to capabilities at runtime.

## Capability inventory

Look for:

- `web-search`: broad web discovery
- `news-search`: date-filtered reporting and event coverage
- `academic-search`: papers, citations, and scholarly metadata
- `official-record-search`: legislation, regulation, filings, tenders, and statistics
- `url-extract`: retrieve clean content from known URLs
- `site-crawl`: discover or retrieve multiple pages from an approved domain
- `browser`: inspect dynamic public pages
- `internal-search`: approved company documents, messages, datasets, or knowledge bases
- `document-read`: PDF, spreadsheet, presentation, image, and transcript processing

Tool names differ across hosts. Use capabilities, not hardcoded provider names.

## Ask only when needed

If tool availability is not visible, ask:

> Are any web-search, news, academic, filings, crawling, browser, or internal-knowledge
> plugins configured and approved in this environment? If yes, which may I use?

Do not ask when the user already named an approved tool or supplied sufficient sources.

## Provider authorization

- Never select a named paid provider merely because it is installed.
- Ask before using a provider the user did not request.
- Confirm whether external tools may receive the query and supplied context.
- Keep confidential company context out of external queries unless explicitly authorized.
- Never place API keys, tokens, credentials, or private endpoints in skill files or reports.

Use `assets/tool-capability-template.yaml` to record runtime choices.

## Search tools

Search plugins improve query breadth, freshness, result ranking, and domain filtering. They
are discovery systems, not evidence authorities.

For each useful result:

1. Open or extract the underlying source.
2. Confirm title, publisher, author, date, and URL.
3. Read the relevant section in context.
4. Register the source before citing it.

Do not cite generated search answers unless they are explicitly treated as an analysis
artifact and all underlying sources are independently verified.

## Extraction and crawling

Use URL extraction for known pages and crawling only when:

- The domain and path scope are approved
- Multiple pages are necessary
- Terms, rate limits, and access restrictions are respected
- The crawl has a clear stopping condition

Never bypass authentication, CAPTCHAs, robots directives, or access controls.

## Internal connectors

Internal search can add decision-critical context unavailable publicly. Before use:

- Confirm the connector is approved for the data class
- Restrict queries to the minimum relevant scope
- Preserve document identifiers and access-controlled links
- Mark internal evidence so distribution controls can be applied
- Do not reproduce sensitive content unnecessarily

An internal source may be authoritative for company policy but not for external market facts.

## No-plugin fallback

When no plugin is available:

- Use user-supplied documents and URLs
- Use permitted browser access if available
- Ask the user for specific missing source categories
- Narrow the scope rather than fabricating coverage
- State which capabilities were unavailable

The brief remains valid only for its documented source set.

## Capability record

Record:

```yaml
capability: "<capability>"
tool: "<host tool or manual>"
approved: true
data_class: "<public|internal|confidential>"
query_scope: "<scope>"
limitations:
  - "<limitation>"
```

This record supports reproducibility and explains coverage gaps.
