# GrantCostGate v2 — sealed grant-spend capability

GrantCostGate is a contract-only GenLayer Intelligent Contract. Validators answer one bounded semantic question from a pinned official eCFR source: whether a sealed expense is allowable under a cited 2 CFR Part 200 cost principle. Deterministic contract code alone controls the consequential result: issuance, revocation, expiry and one-time consumption of an exact spend capability.

## Roles and authority boundary

- Any wallet can create an immutable commitment. That wallet becomes the authority for that record and may revoke or retry it.
- Validators independently assess the cited regulation. They never execute a spend.
- The creator selects a `spend_executor` per commitment. It may be the creator itself for simple reviewer testing, or a second wallet to demonstrate role separation.
- The deployment wallet receives no owner or operational privilege. The constructor has no inputs.

The contract is non-custodial. Consumption is an on-chain authorization receipt for an external treasury adapter; it does not claim that an off-chain or cross-chain payment occurred.

## Lifecycle

1. `create_commitment(...)` seals the expense, section, recipient, amount and action digest.
2. `assess_commitment(id, revision)` obtains pinned eCFR evidence and substantive validator consensus.
3. Only an `ALLOWABLE` judgment becomes `AUTHORIZED`. `CONDITIONAL`, `UNALLOWABLE`, source failure and disagreement never grant authority.
4. `consume_authorization(...)` rechecks the complete sealed action and atomically changes `AUTHORIZED` to `CONSUMED`.
5. The authority can call `revoke_authorization(...)` before consumption. `UNRESOLVED` records have an explicit retry path.

```text
PENDING -> AUTHORIZED -> CONSUMED
                      \-> REVOKED
        -> BLOCKED
        -> CONDITIONAL
        -> UNRESOLVED -> PENDING (authorized retry)
```

The contract constructs the official eCFR URL itself and pins the source snapshot to `2025-01-01`. Callers cannot inject an arbitrary evidence URL. Supported sections are 200.421, 200.423, 200.425, 200.445 and 200.475.

## Verify

```powershell
powershell -ExecutionPolicy Bypass -File scripts/verify_local.ps1
```

See `docs/test-plan.md` for the live matrix. Existing v1 explorer transactions in `docs/release-evidence.md` prove only the superseded classifier and are not evidence for v2.

This is a bounded technical demonstration, not legal, accounting or grants-management advice.
