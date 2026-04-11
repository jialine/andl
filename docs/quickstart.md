# ANDL 2.0 Quick Start Guide
## Get Started in 5 Minutes

**Version**: 2.0.0  
**Last Updated**: April 11, 2026

---

## Table of Contents

1. [Installation](#1-installation)
2. [First ANDL Message](#2-first-andl-message)
3. [Basic Usage](#3-basic-usage)
4. [Running Tests](#4-running-tests)
5. [Next Steps](#5-next-steps)

---

## 1. Installation

### Prerequisites

- Python 3.8+
- NumPy
- (Optional) GPU support for optimal performance

### Install from Source

```bash
# Clone the repository
git clone https://github.com/andl/andl.git
cd andl

# Install dependencies
pip install -r requirements.txt

# Install ANDL package
pip install -e .
```

### Verify Installation

```bash
python -c "import andl; print(andl.__version__)"
# Output: 2.0.0
```

---

## 2. First ANDL Message

### 2.1 Create Your First Message

```python
import numpy as np
from andl import ANDLMessage, MessageType

# Create a semantic vector (normally from encoder)
vector = np.random.randn(1024).astype(np.float32)

# Create ANDL message
msg = ANDLMessage.create(
    sender_id="my_agent",
    receiver_id="target_agent",
    semantic_vector=vector,
    message_type=MessageType.REQUEST
)

print(f"Message ID: {msg.header.message_id}")
print(f"Sender: {msg.header.sender_id}")
print(f"Timestamp: {msg.header.timestamp_ns}")
```

**Output:**
```
Message ID: 550e8400-e29b-41d4-a716-446655440000
Sender: my_agent
Timestamp: 1712800800000000000
```

### 2.2 Serialize and Deserialize

```python
# Serialize to bytes
data = msg.serialize()
print(f"Serialized size: {len(data)} bytes")

# Deserialize back
restored = ANDLMessage.deserialize(data)
print(f"Restored sender: {restored.header.sender_id}")
```

---

## 3. Basic Usage

### 3.1 Vector Compression

```python
from andl import VectorCompressor

# Original vector
original = np.random.randn(4096).astype(np.float32)
print(f"Original size: {original.nbytes} bytes")

# Compress
compressor = VectorCompressor(target_bits=8)
compressed = compressor.compress(original)

print(f"Compressed size: {compressed.data.nbytes} bytes")
print(f"Compression ratio: {compressed.compression_ratio:.2f}x")

# Decompress
decompressed = compressor.decompress(compressed)
```

### 3.2 Semantic Graph

```python
from andl import SemanticGraph, SemanticNode, SemanticEdge

# Create graph
graph = SemanticGraph()

# Add nodes
node_a = SemanticNode(
    id="concept_a",
    vector=np.array([1.0, 0.0, 0.0]),
    node_type="concept"
)
node_b = SemanticNode(
    id="concept_b", 
    vector=np.array([0.0, 1.0, 0.0]),
    node_type="concept"
)

graph.add_node(node_a)
graph.add_node(node_b)

# Add relationship
edge = SemanticEdge(
    source_id="concept_a",
    target_id="concept_b",
    relation_type="related_to"
)
graph.add_edge(edge)

# Traverse graph
results = graph.traverse("concept_a", max_depth=2)
print(f"Found {len(results)} nodes")
```

### 3.3 Physical Transport

```python
from andl import AdaptivePhysicalLayer, Address

# Initialize adaptive layer
layer = AdaptivePhysicalLayer()

# Select best transport based on context
context = {
    "same_machine": True,
    "has_gpu": False
}
transport = layer.select_transport(context)

print(f"Selected transport: {type(transport).__name__}")

# Send data
addr = Address(host="localhost", port=8080)
data = b"Hello, ANDL!"
transport.send(data, addr)

# Receive data
received = transport.receive(addr)
print(f"Received: {received.decode()}")
```

### 3.4 Multi-AI Consensus

```python
from andl import VectorConsensus

# Multiple AI proposals
proposals = [
    np.random.randn(512).astype(np.float32),
    np.random.randn(512).astype(np.float32),
    np.random.randn(512).astype(np.float32),
]

# Voting weights
weights = [0.5, 0.3, 0.2]

# Reach consensus
consensus = VectorConsensus()
result, metadata = consensus.vote(proposals, weights)

print(f"Consensus reached in {metadata['iterations']} iterations")
print(f"Outliers detected: {metadata['outliers_detected']}")
print(f"Converged: {metadata['converged']}")
```

---

## 4. Running Tests

### Run All Tests

```bash
cd /path/to/andl
python -m pytest tests/ -v
```

### Run Specific Test

```bash
# Test physical layer
python -m pytest tests/test_andl.py::TestPhysicalLayer -v

# Test compression
python -m pytest tests/test_andl.py::TestVectorCompression -v
```

### Expected Output

```
tests/test_andl.py::TestPhysicalLayer::test_shared_memory_transport PASSED
tests/test_andl.py::TestPhysicalLayer::test_tcp_transport PASSED
tests/test_andl.py::TestVectorCompression::test_compression_decompression PASSED
...
============================== 15 passed in 0.5s
```

---

## 5. Next Steps

### Learn More

- **Technical Whitepaper**: `docs/whitepaper-en.md`
- **Protocol Specification**: `specs/ANDL-2.0-SPEC.md`
- **API Reference**: `docs/api-reference.md`

### Join Community

- GitHub: https://github.com/andl/andl
- Discord: https://discord.gg/andl
- Forum: https://forum.andl.io

### Beta Program

Want early access? Join our beta program:
- See `docs/beta-partners-en.md` for details
- Contact: jialine0426@hotmail.com

---

## Troubleshooting

### Import Error

```
ModuleNotFoundError: No module named 'andl'
```

**Solution**: Install in development mode
```bash
pip install -e .
```

### NumPy Version Conflict

```
RuntimeError: NumPy version mismatch
```

**Solution**: Update NumPy
```bash
pip install --upgrade numpy
```

### GPU Not Detected

```
Warning: GPU not available, falling back to CPU
```

**Solution**: This is normal. ANDL works without GPU using virtual memory manager.

---

## Quick Reference

| Task | Code |
|------|------|
| Create message | `ANDLMessage.create(sender, receiver, vector)` |
| Compress vector | `VectorCompressor().compress(vector)` |
| Build graph | `SemanticGraph().add_node(node).add_edge(edge)` |
| Send data | `transport.send(data, address)` |
| Consensus | `VectorConsensus().vote(proposals, weights)` |

---

**Happy coding with ANDL! 🚀**

---

*For more examples, see `examples/` directory.*