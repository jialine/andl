# Quick Start Guide

Get up and running with ANDL 2.0.1 in 5 minutes.

## Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager
- (Optional) Git for development

### Install from PyPI

```bash
pip install andl2
```

### Install from Source

```bash
git clone https://github.com/jialine/andl.git
cd andl
pip install -e .
```

### Verify Installation

```bash
python -c "import andl; print(andl.__version__)"
# Output: 2.0.1
```

---

## Your First ANDL Application

### 1. Basic Semantic Encoding

```python
import numpy as np
from andl import SemanticEncoder

# Create encoder
encoder = SemanticEncoder()

# Encode text to semantic vector
text = "Transfer 100 yuan to Alice"
vector = encoder.encode(text)

print(f"Text: {text}")
print(f"Vector shape: {vector.shape}")  # (1024,)
print(f"Vector sample: {vector[:5]}")
```

### 2. Distributed Storage

```python
import asyncio
from andl import NeuralConsensus

async def store_message():
    # Create consensus network
    consensus = NeuralConsensus(
        node_count=5,      # 5 nodes
        redundancy=3       # 3x redundancy
    )
    
    # Encode message
    vector = encoder.encode("Hello, NeuralConsensus!")
    
    # Store with distributed redundancy
    result = await consensus.store(vector, "msg_001")
    
    print(f"Storage result: {result}")
    return result

# Run
asyncio.run(store_message())
```

### 3. Verify Message Integrity

```python
async def verify_message():
    # Verify stored message
    verification = await consensus.verify("msg_001", vector)
    
    print(f"Status: {verification.status}")
    print(f"Agreement: {verification.agreement_rate:.1%}")
    print(f"Confidence: {verification.confidence:.1%}")
    
    if verification.status == ConsensusStatus.VALID:
        print("✓ Message is authentic!")
    elif verification.status == ConsensusStatus.TAMPERED:
        print("⚠️  Message has been tampered!")
    
    return verification

asyncio.run(verify_message())
```

### 4. Complete Example

```python
import asyncio
import numpy as np
from andl import NeuralConsensus, SemanticEncoder, ConsensusStatus

async def main():
    print("=" * 60)
    print("ANDL 2.0.1 Quick Start Demo")
    print("=" * 60)
    
    # Initialize
    encoder = SemanticEncoder()
    consensus = NeuralConsensus(node_count=5)
    
    # Step 1: Create and store message
    print("\n[Step 1] Creating message...")
    original_text = "Transfer 100 yuan to Alice"
    original_vector = encoder.encode(original_text)
    print(f"Text: {original_text}")
    
    print("\n[Step 2] Storing message...")
    storage_result = await consensus.store(original_vector, "payment_001")
    print(f"Stored across {storage_result['shards']} shards")
    print(f"Redundancy: {storage_result['redundancy']}x")
    
    # Step 3: Verify authentic message
    print("\n[Step 3] Verifying authentic message...")
    verification = await consensus.verify("payment_001", original_vector)
    print(f"Status: {verification.status.value}")
    print(f"Agreement: {verification.agreement_rate:.1%}")
    
    # Step 4: Try to verify tampered message
    print("\n[Step 4] Testing tamper detection...")
    tampered_text = "Transfer 100 yuan to Bob (HACKER)"
    tampered_vector = encoder.encode(tampered_text)
    
    verification = await consensus.verify("payment_001", tampered_vector)
    print(f"Status: {verification.status.value}")
    print(f"Agreement: {verification.agreement_rate:.1%}")
    
    if verification.status == ConsensusStatus.TAMPERED:
        print("\n✓ Tampering detected! NeuralConsensus is working.")
    
    print("\n" + "=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:
```bash
python demo.py
```

Expected output:
```
============================================================
ANDL 2.0.1 Quick Start Demo
============================================================

[Step 1] Creating message...
Text: Transfer 100 yuan to Alice

[Step 2] Storing message...
Stored across 4 shards
Redundancy: 3x

[Step 3] Verifying authentic message...
Status: valid
Agreement: 100.0%

[Step 4] Testing tamper detection...
Status: tampered
Agreement: 0.0%

✓ Tampering detected! NeuralConsensus is working.

============================================================
Demo completed successfully!
============================================================
```

---

## Running a Local Network

### Start Multiple Nodes

```bash
# Terminal 1: Node 0
python -m andl.node --id node_0 --port 8000

# Terminal 2: Node 1
python -m andl.node --id node_1 --port 8001 --peers localhost:8000

# Terminal 3: Node 2
python -m andl.node --id node_2 --port 8002 --peers localhost:8000,localhost:8001
```

### Connect Your Application

```python
consensus = NeuralConsensus(
    node_endpoints=[
        "http://localhost:8000",
        "http://localhost:8001",
        "http://localhost:8002"
    ]
)
```

---

## Configuration

### Basic Config

```python
from andl import NeuralConsensus

consensus = NeuralConsensus(
    node_count=5,              # Number of nodes
    redundancy=3,              # Replication factor
    consensus_threshold=0.67,  # 67% agreement required
    shard_sizes=[128, 256, 512, 128]  # Semantic shard dimensions
)
```

### From Config File

```yaml
# config.yaml
network:
  node_count: 5
  redundancy: 3
  consensus_threshold: 0.67

storage:
  backend: "rocksdb"
  path: "/var/andl/data"

security:
  encryption: true
  key_rotation_days: 30
```

```python
import yaml
from andl import NeuralConsensus

with open("config.yaml") as f:
    config = yaml.safe_load(f)

consensus = NeuralConsensus.from_config(config)
```

---

## Next Steps

### Learn More

- 📖 [Protocol Specification](../specs/ANDL-2.0.1-SPEC.md)
- 🔬 [Experiment Report](tamper-proof-experiment-report.md)
- 💡 [Design Philosophy](whitepaper-cn.md)

### Examples

- [Basic Chat Application](../examples/chat/)
- [Distributed AI Inference](../examples/inference/)
- [Secure Data Sharing](../examples/data-sharing/)

### Join Community

- 💬 [GitHub Discussions](https://github.com/jialine/andl/discussions)
- 🐛 [Report Issues](https://github.com/jialine/andl/issues)
- 🤝 [Contributing Guide](CONTRIBUTING.md)

---

## Common Issues

### ImportError: No module named 'andl'

```bash
# Solution: Install in virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install andl2
```

### Connection refused

```bash
# Check if nodes are running
python -m andl.node --status

# Or start a local test network
python -m andl.network --local --nodes 3
```

### High memory usage

```python
# Reduce node count for development
consensus = NeuralConsensus(node_count=3)
```

---

## Performance Tips

1. **Use batch operations**:
```python
# Instead of individual stores
results = await consensus.store_batch(vectors)
```

2. **Enable caching**:
```python
consensus = NeuralConsensus(
    cache_enabled=True,
    cache_ttl=300  # 5 minutes
)
```

3. **Use GPU encoding** (if available):
```python
encoder = SemanticEncoder(device="cuda")
```

---

**You're ready to build with ANDL!** 🚀

For questions, see [FAQ](FAQ.md) or join [Discussions](https://github.com/jialine/andl/discussions).
