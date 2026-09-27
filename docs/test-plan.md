# Verification matrix

## Happy paths

| Case | Section | Expected |
|---|---:|---|
| Alcohol for project celebration | 200.423 | `UNALLOWABLE / ALCOHOL_PROHIBITED` |
| Required federal-award audit | 200.425 | `ALLOWABLE / AUDIT_COST_ALLOWED` |
| Recruitment advertising requiring records | 200.421 | `CONDITIONAL / DOCUMENTATION_REQUIRED` |

## Failure paths

- Expense shorter than 20 or longer than 600 characters.
- Unsupported section or arbitrary URL-shaped section.
- Non-200 source response.
- Empty, undersized, oversized, wrongly cited, or invalid UTF-8 source.
- Missing or extra model fields, invalid enums, or non-boolean flags.
- Duplicate normalized expense/section fingerprint.

## Conflict and adversarial paths

- Validator comparison returns a non-schema conflict payload: store `UNRESOLVED / CONSENSUS_INVALID`.
- `ALLOWABLE` without direct support: `MODEL_CONTRADICTION`.
- `ALLOWABLE` paired with a prohibition reason: `MODEL_CONTRADICTION`.
- `CONDITIONAL` without a condition or missing-facts reason: `MODEL_CONTRADICTION`.
- Expense contains prompt-injection text: evidence remains inert and output remains schema-bound.
- Duplicate calls cannot overwrite or create a second determination.

## Audit invariants

- Every accepted request creates exactly one immutable record.
- `determination_digest` binds requester, normalized expense, section, source identity, source digest, outcome, reason and conditions.
- Failed source/model/consensus execution never becomes `ALLOWABLE`.
- No arbitrary URL enters validator fetch logic.
- No funds, administrator role, deletion method, or mutable correction path exists.
