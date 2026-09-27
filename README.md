# GrantCostGate

GrantCostGate is a contract-only GenLayer Intelligent Contract that applies a pinned federal grant cost principle to a concrete expense description. It returns `ALLOWABLE`, `CONDITIONAL`, `UNALLOWABLE`, or a fail-closed `UNRESOLVED` record.

It is deliberately narrow: Title 2, Part 200 cost principles only. It is not a policy-diff system, a legal-opinion service, an escrow, or a two-role assessment workflow.

## Architecture

`classify_cost(expense, section)` is a single-shot adjudication:

1. Normalize and validate the expense and allowlisted section.
2. Deduplicate by `sha256(section + normalized expense)`.
3. Construct the official pinned eCFR URL; callers cannot supply a URL.
4. Verify HTTP status, byte bounds, citation, and section identity.
5. Run a schema-bound comparative semantic judgment.
6. Enforce cross-field decision invariants.
7. Persist an immutable determination or a fail-closed `UNRESOLVED` audit record.

No retry mutates an existing determination. A duplicate normalized request returns its existing ID. The contract has no payable method and holds no funds.

## Supported sections

- `200.421` Advertising and public relations
- `200.423` Alcoholic beverages
- `200.425` Audit services
- `200.445` Goods or services for personal use
- `200.475` Travel costs

The source snapshot date is fixed at `2025-01-01`, so validator inputs remain reproducible. See [`docs/test-resources.md`](docs/test-resources.md).

## Verify

```powershell
powershell -ExecutionPolicy Bypass -File scripts/verify_local.ps1
```

This runs GenVM lint/validation on both contracts and 19 direct tests against the exact production source.

## Deploy and test

1. Deploy `contracts/ecfr_source_probe.py` to Studio Next and call `probe`.
2. Confirm validator consensus and compare the returned byte count/digest with the fixture manifest.
3. Deploy `contracts/grant_cost_gate.py` from the main deployment wallet.
4. From either test wallet call:

```text
classify_cost(
  "Purchase alcoholic beverages for the grant-funded project celebration.",
  "200.423"
)
```

5. Read `get_determination(1)`. Expected outcome: `DETERMINED / UNALLOWABLE / ALCOHOL_PROHIBITED`.
6. Run conditional, allowable, malformed, duplicate, source-failure and consensus-conflict cases described in [`docs/test-plan.md`](docs/test-plan.md).

The result is a bounded technical demonstration and not legal, accounting, or grants-management advice.
