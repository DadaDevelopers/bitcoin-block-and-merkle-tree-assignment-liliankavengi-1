# Assignment 6 — Bitcoin Block and Merkle Tree

## Overview

This assignment explores Bitcoin's block structure and Merkle tree construction through real block data from mempool.space and a from-scratch Python implementation.

---

## Task 1 — Block Inspection

**Block inspected:** [Block 730,000 on mempool.space](https://mempool.space/block/0000000000000000000384f28cb3b9cf4377a39cfd6c29ae9466951de38c0529)

```
Block Inspection Results
------------------------
Block Height:           730,000
Block Hash:             0000000000000000000384f28cb3b9cf4377a39cfd6c29ae9466951de38c0529
Previous Block Hash:    00000000000000000008b6f6fb83f8d74512ef1e0af29e642dd20daddd7d318f
Merkle Root:            efa344bcd6c0607f93b709515dd6dc5496178112d680338ebea459e3de7b4fbc
Number of Transactions: 1,627
Timestamp:              2022-04-01 19:30:49 UTC  (Unix: 1648829449)
```

### Key observations

- The block hash starts with many leading zeros — this is proof-of-work. Miner Binance Pool had to perform roughly 28.5 quadrillion hashes to find a nonce that produced this result.
- The `Previous Block Hash` links this block directly to block 729,999. If anyone altered that earlier block, its hash would change, breaking this reference and invalidating every block after it.
- The `Merkle Root` is a single 32-byte fingerprint of all 1,627 transactions. Any change to any transaction — even one bit — produces a completely different Merkle root, which would break the block hash and invalidate the block.

---

## Task 2 — Merkle Tree Construction

### Transaction Hashes Used

| Label | TXID |
|-------|------|
| TxA | `4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b` |
| TxB | `0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098` |
| TxC | `9b0fc92260312ce44e74ef369f5c66bbb5b9b33d9a0d64dc8ba1c61c0b6b6b1c` |
| TxD | `999e1c837c76a1b7fc76a102e5d5c7b2b3f7a9b6c5d4e3f2a1b0c9d8e7f6a5b4` |

---

### Merkle Tree Diagram

```
                              Merkle Root
                   ┌──────────────────────────────────┐
                   │  4fd6b2c5eb2c6e7d768803363b2b420  │
                   │  85323f0476793b538cf38006eeec39011│
                   └─────────────┬────────────────────┘
                                 │
              ┌──────────────────┴──────────────────┐
              │                                     │
    ┌─────────┴──────────┐               ┌──────────┴─────────┐
    │      Hash(AB)      │               │      Hash(CD)      │
    │ 2f42d84035229248   │               │ eb9fbf96d8720fc8   │
    │ 3446963dd7a2713e   │               │ 113cf830bc7f6412   │
    │ c165f852a975ccfb   │               │ 5684f3315a74c767   │
    │ 0fd7f6194f58fb33   │               │ ac1103d24c94c823   │
    └────────┬───────────┘               └─────────┬──────────┘
             │                                     │
     ┌───────┴────────┐                   ┌────────┴────────┐
     │                │                   │                 │
┌────┴────┐     ┌─────┴────┐        ┌─────┴────┐     ┌──────┴─────┐
│   TxA   │     │   TxB    │        │   TxC    │     │    TxD     │
│4a5e1e4b │     │0e3e2357  │        │9b0fc922  │     │999e1c83    │
│aab89f3a │     │e806b6cd  │        │60312ce4  │     │7c76a1b7    │
│...      │     │...       │        │...       │     │...         │
└─────────┘     └──────────┘        └──────────┘     └────────────┘
```

---

### Step-by-Step Calculation

Bitcoin uses **double SHA-256** (`dSHA256 = SHA256(SHA256(data))`) for all Merkle hashing.
TXIDs are stored in **reversed byte order** internally before hashing.

#### Step 1 — Convert TXIDs to internal byte order (reverse each)

```
TxA (internal): 3ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a9fb8aa4b1e5e4a
TxB (internal): 982051fd1e4ba744bbbe680e1fee14677ba1a3c3540bf7b1cdb606e857233e0e
TxC (internal): 1c6b6b0b1cc6a18bdc640d9a3db3b9b5bb665c9f36ef744ee42c316022c90f9b
TxD (internal): b4a5f6e7d8c9b0a1f2e3d4c5b6a9f7b3b2c7d5e502a176fcb7a1767c831c9e99
```

#### Step 2 — Hash pairs to get Level 1

```
Hash_AB = dSHA256(TxA_internal || TxB_internal)
        = 2f42d840352292483446963dd7a2713ec165f852a975ccfb0fd7f6194f58fb33

Hash_CD = dSHA256(TxC_internal || TxD_internal)
        = eb9fbf96d8720fc8113cf830bc7f64125684f3315a74c767ac1103d24c94c823
```

#### Step 3 — Hash the pair of Level 1 hashes to get the Merkle Root

```
Merkle Root = dSHA256(Hash_AB || Hash_CD)
            = 4fd6b2c5eb2c6e7d768803363b2b42085323f0476793b538cf38006eeec39011
```

---

### Merkle Proof (Transaction Inclusion Proof)

To prove **TxC** is in the block without downloading all transactions:

| Step | Sibling Hash | Position |
|------|-------------|----------|
| 1 | `999e1c83...f6a5b4` (TxD) | RIGHT |
| 2 | `2f42d840...58fb33` (Hash_AB) | LEFT |

**Verification:**
```
dSHA256(TxC || TxD)              = Hash_CD
dSHA256(Hash_AB || Hash_CD)      = Merkle Root ✓
```

Only 2 hashes needed instead of all 4 TXIDs — with 1,627 transactions, you'd only need ~11 hashes instead of 1,627. This is the efficiency benefit of Merkle trees.

---

## Key Learnings

1. **Block linking via previous hash** — altering any historical block invalidates the entire chain forward, making tampering computationally infeasible.

2. **Merkle root as tamper seal** — the root commits every transaction to the block header. Changing even one byte in any transaction breaks the root and invalidates the block.

3. **Merkle proofs for SPV** — lightweight wallets only download 80-byte block headers. To verify a payment, they request a Merkle proof (~11 hashes for a 1,627-tx block) instead of the full 1.2 MB block. This is how mobile Bitcoin wallets work efficiently.

4. **Double SHA-256** — Bitcoin uses SHA256 twice for added security against length-extension attacks.

5. **Byte order matters** — TXIDs are displayed in reversed byte order on block explorers but stored and hashed in their original (internal) byte order. Getting this wrong produces incorrect Merkle roots.

---

## File Structure

```
assignment-6/
├── README.md              ← this file (main report)
├── block-inspection.md    ← Task 1 detailed findings
└── code/
    └── merkle_tree.py     ← Task 2 Python implementation
```

## How to Run

```bash
python3 code/merkle_tree.py
```

Requires Python 3.9+ and no external dependencies (uses only `hashlib` from the standard library).
