# Release evidence

## Local verification

| Check | Result |
|---|---|
| `GrantCostGate` GenVM lint/validation | PASS — 5 methods: 4 view, 1 write |
| `EcfrSourceProbe` GenVM lint/validation | PASS — 3 methods: 2 view, 1 write |
| Production-source tests | PASS — 19/19 |
| Official eCFR fixture | PASS — HTTP 200, 327 UTF-8 bytes, pinned SHA-256 recorded |
| Custody review | PASS — no payable methods and no balance transfers |

## Studio Next live evidence

Every completed row below is backed by a real finalized Studio Next transaction or finalized state readback:

| Item | Address / transaction | Result |
|---|---|---|
| Source probe deployment | [`0xf864...53D9`](https://explorer-studio-dev.genlayer.com/address/0xf864b103902072014920bb02BF773D1AbDc153D9) | Exact fixture view confirmed |
| Source probe call | [`0x7606...d487`](https://explorer-studio-dev.genlayer.com/tx/0x7606cb2f98a4256d37e5244830b9f74ebc3a00f329d09a26abf552dd7294d487) | `FINALIZED / MAJORITY_AGREE`; 327 bytes; SHA-256 `5a437e9ac239b72a224ac07d9ad99668bb37de0a9b25111078eb687534cfb6db` |
| Main deployment v1 | [`0x1C1a...E689`](https://explorer-studio-dev.genlayer.com/address/0x1C1a1962342414948390705759294B3cA058E689) | SUPERSEDED: live advertising case exposed `ALLOWABLE` together with `requires_documentation=true`; invariant hardened before final deployment |
| v1 alcohol classification | [`0x4e60...f9c6`](https://explorer-studio-dev.genlayer.com/tx/0x4e60d5cb8d87e8b19674cc576f83bd0cfa79b34f891f8b8cf7a0f1967a0af9c6) | `DETERMINED / UNALLOWABLE / ALCOHOL_PROHIBITED`; correct |
| v1 audit-cost classification | [`0xb3a5...7a86`](https://explorer-studio-dev.genlayer.com/tx/0xb3a570eb8ccca1aaa322288602ced7abbc16918d171c3caf3cffa05969627a86) | `DETERMINED / ALLOWABLE / AUDIT_COST_ALLOWED`; correct |
| v1 advertising audit finding | [`0xd75b...ebb6`](https://explorer-studio-dev.genlayer.com/tx/0xd75b88c782ce8b9603fc77a647917caa6b5221addcba624e400c34e4826debb6) | Returned contradictory `ALLOWABLE + requires_documentation`; prompted invariant fix |
| v1 duplicate replay | [`0xe213...814b`](https://explorer-studio-dev.genlayer.com/tx/0xe213834cb62b2b31ca6f148af7955f14185aec4faa250e5cf3f304cfe5f4814b) | Total stayed `3`; no duplicate record |
| v1 unsupported section | [`0x2b25...202e`](https://explorer-studio-dev.genlayer.com/tx/0x2b253b933db627976540f84ed7b171c7f989ff10bd83b76f46365d63df3c202e) | Total stayed `3`; no record |
| Final main deployment | [`0x06c7...9a70`](https://explorer-studio-dev.genlayer.com/address/0x06c7afb39688C1FFF31318FFe1ceE202119a9a70) | Clean initial total `0`; exact hardened protocol views confirmed |
| Alcohol classification | [`0x8066...01e9`](https://explorer-studio-dev.genlayer.com/tx/0x80667d171eac21a800f443062425ca2acd7513460cef18a1f0583abd90c201e9) | `DETERMINED / UNALLOWABLE / ALCOHOL_PROHIBITED`, record `1` |
| Audit-cost classification | [`0x579f...a3d`](https://explorer-studio-dev.genlayer.com/tx/0x579f074969a1b220d14990999f8d5eb4c0378164b173d3bc9a53e529e34a3a3d) | `DETERMINED / ALLOWABLE / AUDIT_COST_ALLOWED`, record `2` |
| Advertising conflict | [`0xc8c9...6e5a`](https://explorer-studio-dev.genlayer.com/tx/0xc8c90820fe65b2ec4b3e44a3bcee2d6d0c0df8b34eaa6434ef219aa40c9c6e5a) | `MAJORITY_DISAGREE`; no state committed, total stayed `2` |
| Conditional travel classification | [`0x19c4...ac0a`](https://explorer-studio-dev.genlayer.com/tx/0x19c4b1dfb8c6c7e2b10e07efe697b43678960d84e344f19870b1f5cf1922ac0a) | `DETERMINED / CONDITIONAL / DOCUMENTATION_REQUIRED`, record `3` |
| Duplicate replay | [`0xa472...aa25`](https://explorer-studio-dev.genlayer.com/tx/0xa4723f1299d9aaaa4b9ba751e4a6ee1ae28dee2bc5b236a8b81f467a4002aa25) | `MAJORITY_AGREE`; total stayed `2` at time of replay |
| Unsupported section | [`0xe032...fc94`](https://explorer-studio-dev.genlayer.com/tx/0xe032a583886caef67b7129478447018462c94fa05e607cbc2ad432c279fdfc94) | `MAJORITY_AGREE`; total stayed `2`, no record |

Never claim live verification or insert invented hashes. Every completed row must link directly to the Studio Next explorer transaction and include finalized readback state.
