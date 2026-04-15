"""
merkle_tree.py
==============
Bitcoin Merkle Tree construction and verification.
Assignment 6 — Task 2

Demonstrates:
  - Building a Merkle tree from 4 transaction IDs
  - Step-by-step hash computation using double SHA-256
  - Merkle proof (inclusion proof) generation and verification
  - Odd transaction count handling (last TXID duplicated)
"""

import hashlib
import json

# Core hash function

def double_sha256(data: bytes) -> bytes:
    """Bitcoin's standard hash function: SHA256(SHA256(data))"""
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


# Byte-order helpers

def display_to_internal(txid_hex: str) -> bytes:
    """
    Convert a TXID from display format (big-endian hex, as shown on explorers)
    to Bitcoin's internal byte order (little-endian / reversed bytes).
    """
    return bytes.fromhex(txid_hex)[::-1]


def internal_to_display(raw: bytes) -> str:
    """Convert internal bytes back to display hex (reversed)."""
    return raw[::-1].hex()


# Merkle tree builder

def build_merkle_tree(txids: list[str]) -> dict:
    """
    Build a complete Merkle tree from a list of transaction IDs.

    Args:
        txids: List of transaction IDs in display format (hex strings).

    Returns:
        A dictionary with:
          - levels: list of rows from leaves to root (each row = list of hex hashes)
          - root:   the Merkle root in display format
    """
    if not txids:
        raise ValueError("Cannot build a Merkle tree with no transactions")

    # Convert all TXIDs to internal byte order
    current_level = [display_to_internal(txid) for txid in txids]
    levels = [current_level[:]]   # store each level for display

    while len(current_level) > 1:

        # If odd count, duplicate the last item
        if len(current_level) % 2 == 1:
            current_level.append(current_level[-1])

        next_level = []
        for i in range(0, len(current_level), 2):
            combined = current_level[i] + current_level[i + 1]
            next_level.append(double_sha256(combined))

        current_level = next_level
        levels.append(current_level[:])

    root_internal = current_level[0]
    return {
        "levels": levels,
        "root": internal_to_display(root_internal),
        "root_internal": root_internal.hex(),
    }

# Merkle proof (inclusion proof)

def generate_merkle_proof(txids: list[str], target_txid: str) -> list[dict]:
    """
    Generate a Merkle proof — the minimal set of hashes needed to
    verify that target_txid is included in this block without
    downloading all transactions.

    Args:
        txids: All transaction IDs in the block (display format).
        target_txid: The TXID to prove inclusion for.

    Returns:
        List of {"hash": hex, "position": "left"|"right"} dicts.
    """
    current_level = [display_to_internal(t) for t in txids]
    target = display_to_internal(target_txid)
    proof = []

    while len(current_level) > 1:
        if len(current_level) % 2 == 1:
            current_level.append(current_level[-1])

        idx = current_level.index(target)
        if idx % 2 == 0:                      # target is left node
            sibling = current_level[idx + 1]
            proof.append({"hash": internal_to_display(sibling), "position": "right"})
            parent = double_sha256(target + sibling)
        else:                                  # target is right node
            sibling = current_level[idx - 1]
            proof.append({"hash": internal_to_display(sibling), "position": "left"})
            parent = double_sha256(sibling + target)

        # Rebuild next level and find parent
        next_level = []
        for i in range(0, len(current_level), 2):
            next_level.append(double_sha256(current_level[i] + current_level[i + 1]))

        current_level = next_level
        target = parent

    return proof


def verify_merkle_proof(
    txid: str,
    proof: list[dict],
    expected_root: str,
) -> bool:
    """
    Verify a Merkle proof.

    Args:
        txid:          The TXID to verify (display format).
        proof:         List of {"hash", "position"} dicts from generate_merkle_proof.
        expected_root: The Merkle root from the block header (display format).

    Returns:
        True if the proof is valid, False otherwise.
    """
    current = display_to_internal(txid)
    for step in proof:
        sibling = display_to_internal(step["hash"])
        if step["position"] == "right":
            current = double_sha256(current + sibling)
        else:
            current = double_sha256(sibling + current)
    return internal_to_display(current) == expected_root

# Pretty printer

def print_tree(tree: dict, txids: list[str]) -> None:
    labels = ["TxA", "TxB", "TxC", "TxD", "TxE", "TxF", "TxG", "TxH"]
    levels = tree["levels"]
    total = len(levels)

    print("=" * 70)
    print("MERKLE TREE — BOTTOM TO TOP")
    print("=" * 70)

    level_names = ["Leaf (TXID hashes)"] + \
                  [f"Level {i}" for i in range(1, total - 1)] + \
                  ["Merkle Root"]

    for depth, (level, name) in enumerate(zip(levels, level_names)):
        print(f"\n{name}:")
        for i, node in enumerate(level):
            display = internal_to_display(node)
            if depth == 0 and i < len(labels):
                label = f"  {labels[i]} ({txids[i][:16]}...)"
            elif depth == len(levels) - 1:
                label = "  ROOT"
            else:
                pair_label = f"Hash({''.join(labels[j] for j in range(i*2, min(i*2+2, len(txids))))})"
                label = f"  {pair_label}"
            print(f"{label}")
            print(f"    {display}")

    print(f"\nFinal Merkle Root: {tree['root']}")
    print("=" * 70)

# ASCII diagram

def print_ascii_diagram(txids: list[str], tree: dict) -> None:
    levels = tree["levels"]
    root  = tree["root"]
    hab   = internal_to_display(levels[1][0])
    hcd   = internal_to_display(levels[1][1])
    ha    = internal_to_display(levels[0][0])
    hb    = internal_to_display(levels[0][1])
    hc    = internal_to_display(levels[0][2])
    hd    = internal_to_display(levels[0][3])

    print("""
                         Merkle Root
                    ┌────────────────────┐
                    │ {root}... │
                    └──────────┬─────────┘
                               │
               ┌───────────────┴────────────────┐
               │                                │
        ┌──────┴──────┐                  ┌──────┴──────┐
        │  Hash(AB)   │                  │  Hash(CD)   │
        │ {hab}... │                  │ {hcd}... │
        └──────┬──────┘                  └──────┬──────┘
               │                                │
       ┌───────┴───────┐              ┌──────────┴──────────┐
       │               │              │                      │
   ┌───┴───┐       ┌───┴───┐      ┌───┴───┐             ┌────┴────┐
   │  TxA  │       │  TxB  │      │  TxC  │             │   TxD   │
   │{a}...│       │{b}...│      │{c}...│             │{d}...  │
   └───────┘       └───────┘      └───────┘             └─────────┘
""".format(
        root=root[:18],
        hab=hab[:18], hcd=hcd[:18],
        a=txids[0][:14], b=txids[1][:14],
        c=txids[2][:14], d=txids[3][:14],
    ))


# Main — run the demonstration

if __name__ == "__main__":
    # 4 example transaction IDs (demonstrate with well-known Bitcoin txids)
    # TxA = Genesis block coinbase tx
    # TxB–TxD = example transaction IDs
    txids = [
        "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b",
        "0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098",
        "9b0fc92260312ce44e74ef369f5c66bbb5b9b33d9a0d64dc8ba1c61c0b6b6b1c",
        "999e1c837c76a1b7fc76a102e5d5c7b2b3f7a9b6c5d4e3f2a1b0c9d8e7f6a5b4",
    ]

    print("\n[1] INPUT TRANSACTIONS")
    labels = ["TxA", "TxB", "TxC", "TxD"]
    for label, txid in zip(labels, txids):
        print(f"  {label}: {txid}")

    print("\n[2] BUILDING MERKLE TREE...")
    tree = build_merkle_tree(txids)

    print("\n[3] STEP-BY-STEP CALCULATION")
    levels = tree["levels"]
    print("\n  Leaf level (internal byte order):")
    leaf_labels = ["TxA", "TxB", "TxC", "TxD"]
    for label, node in zip(leaf_labels, levels[0]):
        print(f"    {label}: {node.hex()}")

    print("\n  Level 1 — pair hashes:")
    ha = levels[0][0]; hb = levels[0][1]
    hc = levels[0][2]; hd = levels[0][3]
    hab = double_sha256(ha + hb)
    hcd = double_sha256(hc + hd)
    print(f"    Hash_AB = dSHA256(TxA || TxB) = {hab[::-1].hex()}")
    print(f"    Hash_CD = dSHA256(TxC || TxD) = {hcd[::-1].hex()}")

    print("\n  Merkle Root:")
    root_bytes = double_sha256(hab + hcd)
    print(f"    Root = dSHA256(Hash_AB || Hash_CD) = {root_bytes[::-1].hex()}")

    print("\n[4] FULL TREE")
    print_tree(tree, txids)

    print("\n[5] ASCII DIAGRAM")
    print_ascii_diagram(txids, tree)

    print("\n[6] MERKLE PROOF — prove TxC is in the tree")
    proof = generate_merkle_proof(txids, txids[2])
    print(f"  Target: {txids[2]}")
    print("  Proof steps:")
    for step in proof:
        print(f"    {step['position'].upper()} sibling: {step['hash']}")
    valid = verify_merkle_proof(txids[2], proof, tree["root"])
    print(f"  Verification: {'PASS' if valid else 'FAIL'}")

    print("\n[7] JSON OUTPUT")
    output = {
        "transactions": {l: t for l, t in zip(labels, txids)},
        "hash_ab": internal_to_display(levels[1][0]),
        "hash_cd": internal_to_display(levels[1][1]),
        "merkle_root": tree["root"],
        "merkle_proof_for_TxC": proof,
        "proof_valid": valid,
    }
    print(json.dumps(output, indent=2))
