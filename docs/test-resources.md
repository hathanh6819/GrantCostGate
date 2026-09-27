# Test source and fixture

## Authoritative source

GrantCostGate uses the official Electronic Code of Federal Regulations API operated by the U.S. Government Publishing Office and Office of the Federal Register.

- API documentation: <https://www.ecfr.gov/developers/documentation/api/v1>
- Fixed fixture: <https://www.ecfr.gov/api/versioner/v1/full/2025-01-01/title-2.xml?part=200&section=200.423>
- Human-readable section: <https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-E/section-200.423>

The API is publicly readable without an account or API key. The contract constructs URLs from an allowlisted section; user-provided URLs are never accepted.

## Pinned fixture

Verified on 2026-09-27:

```json
{
  "date": "2025-01-01",
  "title": 2,
  "part": 200,
  "section": "200.423",
  "http_status": 200,
  "utf8_bytes": 327,
  "sha256": "5a437e9ac239b72a224ac07d9ad99668bb37de0a9b25111078eb687534cfb6db",
  "heading": "200.423 Alcoholic beverages.",
  "operative_text": "The cost of alcoholic beverages is unallowable."
}
```

Validators hash the exact response bytes they fetch. Any source outage, wrong citation, unexpected section, invalid UTF-8, or response outside the byte bound produces `UNRESOLVED` rather than an allowability decision.

## Scope and legal status

eCFR is an authoritative but unofficial, continuously updated presentation of the CFR. GrantCostGate pins a historical eCFR date for reproducibility and does not claim to provide a current legal opinion. Reviewers should compare the pinned response and the on-chain `source_digest` directly.
