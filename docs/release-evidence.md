# Release evidence

## v2 local verification

| Check | Result |
|---|---|
| `GrantCostGate` GenVM lint/validation | PASS — 9 methods: 4 view, 5 write |
| `EcfrSourceProbe` GenVM lint/validation | PASS — 3 methods: 2 view, 1 write |
| Production-source tests | PASS — 14/14 |
| Authorization boundary | PASS — judgment separated from deterministic consumption |
| Reviewer accessibility | PASS — permissionless per-record roles; no constructor allowlist |
| Last-mile binding | PASS — recipient, amount, action digest, revision, role and expiry |
| Replay/revocation | PASS — terminal state prevents reuse |
| Custody review | PASS — no payable methods and no balance transfers |

## v2 Studio Next evidence

| Item | Address / transaction | Result |
|---|---|---|
| v2 deployment | [`0xC77f...324e`](https://explorer-studio-dev.genlayer.com/address/0xC77f493221cD2ac65CcADb4AA9f3505A0553324e) | Finalized readback: version `2`, architecture `permissionless-sealed-spend-capability`, per-commitment roles, total `0` |
| Create allowable commitment | [`0x49e2...cfa1`](https://explorer-studio-dev.genlayer.com/tx/0x49e23ddb4406e961a7883f8dbb5f021c47c6d06595d4bedbd4a3702ed00ecfa1) | `MAJORITY_AGREE`; record `1`, `PENDING`, revision `1`; authority and executor are distinct wallets |
| Assess allowable commitment | [`0x6186...17ff`](https://explorer-studio-dev.genlayer.com/tx/0x6186b2bb2e4317f1e34bfc3ec1b4752d060d2d84ada15dd858b17b4829df17ff) | `MAJORITY_AGREE`; `AUTHORIZED / ALLOWABLE / AUDIT_COST_ALLOWED`, revision `2` |
| Reject substituted amount | [`0x8dd9...d54f`](https://explorer-studio-dev.genlayer.com/tx/0x8dd9b15df81931e6aad2ac2644c5aaeb871d5af6827ed0e77b34c59d6fb8d54f) | `MAJORITY_AGREE`; wrong amount rejected, record remained `AUTHORIZED`, revision `2` |
| Consume exact capability | [`0x3a8e...0f15`](https://explorer-studio-dev.genlayer.com/tx/0x3a8e68f8a1bb91769df40632f779b7b7281c171328e21c07f2bf59a2c1500f15) | `MAJORITY_AGREE`; bound executor consumed exact payload, `CONSUMED`, revision `3` |
| Reject replay | [`0xd406...40b6`](https://explorer-studio-dev.genlayer.com/tx/0xd40633b604f9807551ba8afe0a43adacd08627b10966811c579184a962eb40b6) | `MAJORITY_AGREE`; replay rejected and record remained `CONSUMED`, revision `3` |
| Create prohibited commitment | [`0xa837...9a67`](https://explorer-studio-dev.genlayer.com/tx/0xa8375315f9ff1230b30a1f8480f883eb3f2903fb600847d8c76a472da6b89a67) | `MAJORITY_AGREE`; record `2` created |
| Assess prohibited commitment | [`0x4a0b...db06`](https://explorer-studio-dev.genlayer.com/tx/0x4a0b72ec1fdf7bdd77face998e68bf61e6b03eb0a89e6500e2708d905f8adb06) | `MAJORITY_AGREE`; `BLOCKED / UNALLOWABLE / ALCOHOL_PROHIBITED`, revision `2`; no capability issued |
| Reject unsupported section | [`0x0b33...58ee`](https://explorer-studio-dev.genlayer.com/tx/0x0b335ce3931a145e76f718a469ce626e971a89e97e2ed6ffed8e2baab7b258ee) | `MAJORITY_AGREE`; total stayed `2`, no record created |
| Reject malformed action digest | [`0xe808...9de0`](https://explorer-studio-dev.genlayer.com/tx/0xe8080f6920eb82d4fd60f2e1d136f5229828123ddb0584b69ddbd5776d1f9de0) | `MAJORITY_AGREE`; total stayed `2`, no record created |
| Reject invalid expiry | [`0x36f4...e53b`](https://explorer-studio-dev.genlayer.com/tx/0x36f408232346dd8942e319d77ad395539f741d2b68c9b2a851df4f7eb61ae53b) | `MAJORITY_AGREE`; total stayed `2`, no record created |
| Reject wrong-role consumption | [`0xcfbe...1b50`](https://explorer-studio-dev.genlayer.com/tx/0xcfbedf07ce88e82a0c5acddad3a2fe937c57d56b070f657ea674186a63271b50) | `MAJORITY_AGREE`; authority could not act as bound executor; total/state unchanged |
| Reject consumption of blocked record | [`0x05e9...7c04`](https://explorer-studio-dev.genlayer.com/tx/0x05e9746b8b30b7559922269a43be877caedeecb711c285241395d32c59dc7c04) | `MAJORITY_AGREE`; correct executor received no capability from `BLOCKED`; state unchanged |
| Reject stale revision | [`0x1ada...0e0c`](https://explorer-studio-dev.genlayer.com/tx/0x1ada863bad885c97e08a94f8b8f95076e84f6731a4d59abe12a9238070a80e0c) | `MAJORITY_AGREE`; stale revision rejected; state unchanged |
| Reject unauthorized revoke | [`0x0ff1...3f71`](https://explorer-studio-dev.genlayer.com/tx/0x0ff1bd4e647f65cf6e4bbff942eacd8a82bc68d66005573262eea92211353f71) | `MAJORITY_AGREE`; executor is not record authority; state unchanged |
| Create conditional candidate | [`0x8b86...a4f7`](https://explorer-studio-dev.genlayer.com/tx/0x8b860fc02b44c440f40d6ed4fb3d000ec4737f3d733f4ab346a4f5673f6ea4f7) | `MAJORITY_AGREE`; record `3`, `PENDING`, revision `1` |
| Conditional assessment conflict | [`0x3b17...4766`](https://explorer-studio-dev.genlayer.com/tx/0x3b17b047f0c7fd9265cf11fdc885a3f94aba4a6e9027317e5ab70548c6344766) | `MAJORITY_DISAGREE`; no state committed; record stayed `PENDING`, revision `1`, no capability issued |

The primary happy, payload-substitution, replay, prohibited-expense, input-gate, role, stale-revision and real validator-conflict paths are finalized on v2. Actual passage-of-time expiry, successful authority revocation and forced source outage remain local-test evidence until separately executed live. Do not present any v1 address or transaction as proof of the v2 capability lifecycle.

## Superseded v1 classifier

The old deployment `0x06c7afb39688C1FFF31318FFe1ceE202119a9a70` and its transactions demonstrate only regulatory classification. They are preserved in Git history for auditability but are explicitly superseded because they do not issue or consume a consequential on-chain capability.
