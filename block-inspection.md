# Task 1 — Block Inspection Results

## Source
Block inspected using [mempool.space](https://mempool.space/block/0000000000000000000384f28cb3b9cf4377a39cfd6c29ae9466951de38c0529)

---

## Block Inspection Results

```
Block Inspection Results
------------------------
Block Height:        730,000
Block Hash:          0000000000000000000384f28cb3b9cf4377a39cfd6c29ae9466951de38c0529
Previous Block Hash: 00000000000000000008b6f6fb83f8d74512ef1e0af29e642dd20daddd7d318f
Merkle Root:         efa344bcd6c0607f93b709515dd6dc5496178112d680338ebea459e3de7b4fbc
Number of Transactions: 1,627
Timestamp:           2022-04-01 19:30:49 UTC  (Unix: 1648829449)
```

---

## Additional Block Header Fields

| Field | Value |
|-------|-------|
| Version | 536870912 (0x20000000) |
| Bits (nBits) | 386521239 |
| Nonce | 3,580,664,066 |
| Difficulty | 28,587,155,782,195.1 |
| Size | 1,210,916 bytes (~1.21 MB) |
| Weight | 3,993,515 WU |
| Median Time | 1648827418 |
| Mined by | Binance Pool |

---

## What Each Field Means

**Block Height (730,000)**  
The block's position in the blockchain, counting from block 0 (the Genesis Block). Block 730,000 is the 730,001st block ever mined.

**Block Hash (`000000...38c0529`)**  
A SHA-256d (double SHA-256) hash of the 80-byte block header. The leading zeros prove proof-of-work was performed — miners had to find a nonce such that the resulting hash fell below the difficulty target. This hash uniquely identifies the block.

**Previous Block Hash (`000000...d7d318f`)**  
The hash of the immediately preceding block (729,999). This is what chains blocks together — if any historical block were altered, its hash would change, breaking every subsequent block's `previousblockhash` reference and invalidating the entire chain forward.

**Merkle Root (`efa344...b4fbc`)**  
A 32-byte fingerprint of all 1,627 transactions in this block, computed by building a binary hash tree (Merkle tree) of all transaction IDs. Any change to any transaction in the block would produce a completely different Merkle root, making the block header — and therefore the block hash — invalid.

**Number of Transactions (1,627)**  
Includes the coinbase transaction (the miner's reward) plus 1,626 user transactions selected from the mempool based on fee rate.

**Timestamp (2022-04-01 19:30:49 UTC)**  
The Unix timestamp recorded by the miner when they constructed the block. Bitcoin consensus rules require this to be within 2 hours of network time and later than the median of the previous 11 blocks.

---

## Block Chain Link Visualisation

```
Block 729,999                    Block 730,000                    Block 730,001
┌─────────────────────┐          ┌─────────────────────┐          ┌─────────────────────┐
│ Hash:               │          │ Hash:               │          │ Hash:               │
│ 00000...d7d318f     │◄─────────│ 00000...38c0529     │◄─────────│ 00000...???????     │
│                     │          │                     │          │                     │
│ Merkle Root: ...    │          │ Merkle Root:        │          │ Prev Hash:          │
│ Transactions: ...   │          │ efa344...b4fbc      │          │ 00000...38c0529     │
│                     │          │ Transactions: 1,627 │          │                     │
└─────────────────────┘          └─────────────────────┘          └─────────────────────┘
```

Each block's `Previous Block Hash` field points to the hash of the block before it, forming an immutable chain.
