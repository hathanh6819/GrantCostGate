# GrantCostGate v2 verification matrix

Deploy with no constructor inputs. Any reviewer wallet can create its own commitment and set itself as executor to test the complete lifecycle. The release evidence should additionally use two wallets to demonstrate separation of authority and executor.

## Required live lifecycle

1. Authority creates an audit-cost commitment; confirm `PENDING`, revision 1 and the exact sealed recipient/amount/action digest.
2. Assess it; confirm `AUTHORIZED`, revision 2, a source digest and an evidence digest.
3. Executor tries a wrong recipient, amount and action digest separately; every rejection must leave the full record unchanged.
4. Executor consumes the exact action; confirm `CONSUMED`, revision 3 and nonzero `consumed_at`.
5. Replay consumption; confirm rejection and no mutation.
6. Create and assess alcohol expense; confirm `BLOCKED` and no consumable authority.
7. Create and assess an expense needing documentation; confirm `CONDITIONAL`, never `AUTHORIZED`.
8. Exercise `UNRESOLVED` and authority-only retry where practical.
9. Create an authorization and revoke it; confirm it can no longer be consumed.
10. Confirm an expired commitment cannot be assessed or consumed.

## Local adversarial coverage

- Unauthorized create, retry, revoke and consume.
- Stale revision and duplicate commitment.
- Invalid amount, recipient, digest, expiry and section.
- Source unavailable, size invalid and identity mismatch.
- Malformed or contradictory model output and consensus conflict.
- Payload substitution and replay with complete pre/post no-mutation assertions.

## Proof obligations

- No non-`ALLOWABLE` outcome grants a capability.
- AI cannot consume, revoke or alter the sealed action.
- Executor cannot substitute recipient, amount or payload.
- Capability is single-use, expiring, revision-bound and revocable.
- Rejected calls do not partially mutate consequential state.
- Deployment ownership is distinct from operational authorization.
