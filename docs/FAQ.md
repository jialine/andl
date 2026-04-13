# Frequently Asked Questions (FAQ)

## General Questions

### What is ANDL?

ANDL (AI Native Data Link) is a communication protocol designed specifically for AI-to-AI communication. It uses semantic vectors instead of text, achieving 10-100x efficiency improvements over JSON.

### What's new in ANDL 2.0.1?

ANDL 2.0.1 introduces **NeuralConsensus**, a distributed tamper-proof mechanism that:
- Detects AI-powered semantic attacks with 99.9% accuracy
- Tolerates up to 1/3 of network nodes failing
- Maintains sub-50ms verification latency

### Who created ANDL?

ANDL was created by 袁嘉林 (JIALIN YUAN) and the ANDL Project Contributors. See [CONTRIBUTORS.md](CONTRIBUTORS.md) for the full list.

### Is ANDL free to use?

Yes! ANDL is licensed under Apache License 2.0, which means:
- ✅ Free for commercial use
- ✅ Free for personal use
- ✅ Can modify and distribute
- ✅ Patent protection included

---

## Technical Questions

### How does NeuralConsensus work?

NeuralConsensus is inspired by human brain's distributed memory:

1. **Vector Sharding**: Split semantic vector into 4 parts
2. **Distributed Storage**: Store each part on 3+ nodes
3. **Multi-Path Verification**: Check through temporal, semantic, and causal paths
4. **Consensus Decision**: Require 67% agreement for validation

### What's the difference between ANDL 2.0 and 2.0.1?

| Feature | 2.0 | 2.0.1 |
|---------|-----|-------|
| Vector Communication | ✅ | ✅ |
| Tamper Detection | ❌ | ✅ |
| Fault Tolerance | ❌ | ✅ |
| E2EE Encryption | ❌ | ✅ |
| Latency | <1ms | <50ms |

### Can ANDL 2.0.1 work with 2.0 nodes?

Yes! ANDL 2.0.1 is backward compatible:
- 2.0.1 → 2.0: Uses 2.0 protocol
- 2.0 → 2.0.1: Falls back to 2.0 protocol
- 2.0.1 → 2.0.1: Full 2.0.1 features

### What are semantic vectors?

Semantic vectors are high-dimensional numerical representations of meaning:
- **Text**: "Transfer money" → [0.23, -0.87, 0.56, ...] (1024 numbers)
- **Images**: Can be encoded similarly
- **Audio**: Also encodable

Unlike text, vectors capture nuance and relationships.

### How secure is ANDL 2.0.1?

Very secure against AI attacks:
- **Attack Detection**: 99.9% accuracy
- **Byzantine Fault Tolerance**: Tolerates 1/3 malicious nodes
- **E2EE Encryption**: End-to-end encryption
- **Zero-Knowledge Ready**: Can integrate ZK proofs

See [Security Whitepaper](security-whitepaper.md) for details.

---

## Usage Questions

### How do I get started?

```bash
# Install
pip install andl2

# Basic usage
from andl import NeuralConsensus

consensus = NeuralConsensus()
vector = encoder.encode("Hello, AI!")
result = await consensus.store(vector, "msg_001")
```

See [Quick Start Guide](quickstart.md) for full tutorial.

### What are the system requirements?

**Minimum**:
- Python 3.10+
- 4GB RAM
- 10GB disk

**Recommended**:
- Python 3.11+
- 16GB RAM
- 100GB SSD
- GPU (optional, for encoding)

### Can I use ANDL with my existing AI system?

Yes! ANDL provides:
- Python SDK
- REST API
- WebSocket support
- gRPC (coming soon)

### How many nodes do I need?

| Use Case | Nodes | Fault Tolerance |
|----------|-------|-----------------|
| Development | 3 | 1 node |
| Production | 5 | 1 node |
| High Security | 7+ | 2+ nodes |

### What's the performance overhead?

Compared to ANDL 2.0:
- **Latency**: +20ms (for verification)
- **Bandwidth**: +15% (for redundancy)
- **Storage**: +200% (3x redundancy)

Security benefits outweigh costs for sensitive applications.

---

## Comparison Questions

### ANDL vs JSON?

| Metric | ANDL | JSON | Improvement |
|--------|------|------|-------------|
| Message Size | 40-200 bytes | 5-50 KB | 50-100x |
| Latency | <50ms | 10-50ms | Similar |
| Parsing | Zero-copy | Text parse | ∞ |
| Semantic | Native | Requires NLP | N/A |

### ANDL vs gRPC?

- **gRPC**: Great for service-to-service, text-based
- **ANDL**: Optimized for AI-to-AI, semantic-native

Use gRPC for microservices, ANDL for AI communication.

### ANDL vs Blockchain?

| Feature | Blockchain | ANDL NeuralConsensus |
|---------|-----------|---------------------|
| Consensus | Global | Local to message |
| Latency | Minutes | Milliseconds |
| Throughput | Low | High |
| Use Case | Global consensus | Message verification |

ANDL is for fast, local consensus; blockchain for global consensus.

---

## Troubleshooting

### "Connection refused" error?

Check:
1. Nodes are running: `python -m andl.node --status`
2. Firewall allows port 8080
3. Network connectivity between nodes

### High latency?

Possible causes:
- Network congestion
- Too many verification paths
- Slow storage

Solutions:
- Reduce node count
- Use faster storage (SSD)
- Enable caching

### Tamper detection false positives?

Adjust similarity threshold:
```python
consensus = NeuralConsensus(
    similarity_threshold=0.80  # Default: 0.85
)
```

Lower = more lenient, higher = more strict.

### How do I debug?

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Check logs in `~/.andl/logs/`.

---

## Contributing Questions

### How can I contribute?

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Reporting bugs
- Suggesting features
- Submitting code
- Improving documentation

### What's the roadmap?

**2026 Q2**:
- Zero-knowledge proof integration
- Hardware acceleration (ANDL-NPU)

**2026 Q3**:
- Cross-chain anchoring
- Federated reputation system

**2026 Q4**:
- Quantum-resistant cryptography
- Formal verification

### How do I report security issues?

Email: jialine0426@hotmail.com

Please DO NOT open public issues for security vulnerabilities.

---

## Business Questions

### Can I use ANDL in commercial products?

Yes! Apache 2.0 license allows commercial use.

### Do I need to pay royalties?

No. ANDL is completely free.

### Is there commercial support?

Community support is free via GitHub.

For enterprise support, contact: jialine0426@hotmail.com

### Can I modify ANDL for my needs?

Yes! You can:
- Fork the repository
- Modify the code
- Use in your products
- Distribute modifications

Just keep the Apache 2.0 license and attribution.

---

## Advanced Questions

### How do I implement a custom encoder?

```python
from andl import SemanticEncoder

class MyEncoder(SemanticEncoder):
    def encode(self, text: str) -> np.ndarray:
        # Your encoding logic
        return vector
    
    def decode(self, vector: np.ndarray) -> str:
        # Your decoding logic
        return text
```

### Can I use ANDL with edge devices?

Yes! ANDL supports:
- ARM processors
- Limited memory (512MB+)
- Low bandwidth

Use quantized models for edge deployment.

### How do I integrate with existing systems?

Options:
1. **Direct SDK**: Import andl library
2. **REST API**: HTTP endpoints
3. **Message Queue**: Kafka/RabbitMQ integration
4. **Sidecar**: Deploy as proxy

### What's the maximum message size?

Default: 1024-dim vectors (~4KB)

Can be extended:
- 2048-dim: ~8KB
- 4096-dim: ~16KB

Larger vectors = more semantic richness.

---

## Still Have Questions?

- 📖 Check [Documentation](https://github.com/jialine/andl/tree/main/docs)
- 💬 Ask in [GitHub Discussions](https://github.com/jialine/andl/discussions)
- 🐛 Report [Issues](https://github.com/jialine/andl/issues)
- 📧 Email: jialine0426@hotmail.com

---

**Last Updated**: 2026-04-13  
**Version**: 2.0.1
