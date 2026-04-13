[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/a1G91hG4)
# assignment-6

# Bitcoin Block and Merkle Tree Assignment

## Assignment Overview

This assignment will help you understand Bitcoin's block structure and Merkle tree construction through hands-on exploration and visualization.

---

## Task 1: Block Inspection

### Instructions

Use a blockchain explorer to inspect a specific Bitcoin block:

**Recommended Explorers:**
- [mempool.space](https://mempool.space)
- [blockchain.com](https://www.blockchain.com/explorer)

### Requirements

Find and document the following information for a specific block:

1. **Block Height**: The position of the block in the blockchain
2. **Block Hash**: The unique identifier of the block
3. **Previous Block Hash**: The hash of the block that came before this one
4. **Merkle Root**: The root hash of the Merkle tree containing all transactions

### Submission Format

Create a document with the following structure:

```
Block Inspection Results
------------------------
Block Height: [your answer]
Block Hash: [your answer]
Previous Block Hash: [your answer]
Merkle Root: [your answer]
Number of Transactions: [your answer]
Timestamp: [your answer]
```

---

## Task 2: Merkle Tree Visualization

### Instructions

Construct a Merkle tree from 4 example transaction hashes to demonstrate how the Merkle root is calculated.

### Requirements

1. **Choose 4 Transaction Hashes**
   - You can use real transaction hashes from the block you inspected in Task 1
   - Or create example hashes for demonstration purposes

2. **Construct the Merkle Tree**
   - Show the tree structure visually (diagram, ASCII art, or drawing)
   - Label each level of the tree clearly
   - Show the hashing process at each level

3. **Calculate the Merkle Root**
   - Document each step of the calculation
   - Show how pairs of hashes are combined and re-hashed
   - Verify that your final result matches the expected Merkle root

### Expected Tree Structure

```
                    Merkle Root
                        |
            +-----------+-----------+
            |                       |
        Hash(AB)                Hash(CD)
            |                       |
        +---+---+               +---+---+
        |       |               |       |
      TxA     TxB             TxC     TxD
```

### Tools You Can Use

- Pen and paper
- Diagram tools (draw.io, Lucidchart, Excalidraw)
- Code (Python, JavaScript, etc.)
- ASCII art in your README

---

## Submission Guidelines

### What to Submit

1. A markdown file (`.md`) or PDF containing:
   - Your block inspection findings (Task 1)
   - Your Merkle tree visualization (Task 2)
   - Explanation of your process and findings

2. If you used code:
   - Include your source code files
   - Add comments explaining your logic

### Submission Format

Your submission should include:

```
📁 assignment-submission/
├── README.md (your main report)
├── block-inspection.md (Task 1 results)
├── merkle-tree-diagram.png (or .pdf)
└── code/ (optional, if you wrote code)
    └── merkle_tree.py (or other files)
```

---

## Learning Objectives

By completing this assignment, you will:

- Understand the structure of a Bitcoin block
- Learn how blocks are linked together via hashes
- Visualize how Merkle trees efficiently prove transaction inclusion
- Gain familiarity with blockchain explorers

---

## Resources

### Blockchain Explorers
- [Mempool.space](https://mempool.space) - Clean UI, detailed information
- [Blockchain.com](https://www.blockchain.com/explorer) - Classic explorer
- [Blockstream.info](https://blockstream.info) - Technical details

### Learning Resources
- [Bitcoin Developer Guide - Block Chain](https://developer.bitcoin.org/devguide/block_chain.html)
- [Merkle Trees Explained](https://www.investopedia.com/terms/m/merkle-tree.asp)
- [How Bitcoin Works Under the Hood](https://www.youtube.com/watch?v=Lx9zgZCMqXE)

### Optional Tools
- [Online SHA-256 Calculator](https://emn178.github.io/online-tools/sha256.html)
- [Python hashlib documentation](https://docs.python.org/3/library/hashlib.html)


Good luck! 🚀
