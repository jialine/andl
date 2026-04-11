# ANDL 2.0
## AI Native Data Link Protocol

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/andl/andl2)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-release-brightgreen.svg)]()

**ANDL 2.0** (AI Native Data Link) is a vector-based communication protocol designed specifically for AI-to-AI communication.

> 🎯 **Mission**: Enable efficient, semantic-rich communication between AI systems without human language barriers.

---

## 🌟 Key Features

- **🧠 Vector-Native**: Semantic vectors instead of text
- **⚡ High Efficiency**: 10-100x bandwidth savings vs JSON
- **🔒 Human Supervisable**: Optional Vector Translator for oversight
- **🚀 Hardware Accelerated**: Native support for ANDL-NPU
- **🌐 Infinite Scalable**: Pipeline architecture for unlimited scale

---

## 📊 Performance

| Metric | ANDL 2.0 | JSON | Improvement |
|--------|----------|------|-------------|
| **Message Size** | 40-200 bytes | 5-50 KB | **50-100x** |
| **Latency** | <1ms | 10-50ms | **10-50x** |
| **Bandwidth** | 90% efficient | 10% efficient | **9x** |
| **Parsing** | Zero-copy | Text parsing | **∞** |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         Application Layer               │
│    (AI Agent Logic / Intent)           │
├─────────────────────────────────────────┤
│         Semantic Layer                  │
│    (128-bit Semantic Vector)           │
├─────────────────────────────────────────┤
│         Message Layer                   │
│    (ANDL 2.0 Protocol)                 │
├─────────────────────────────────────────┤
│         Transport Layer                 │
│    (ANDL-Link / TCP / RDMA)            │
├─────────────────────────────────────────┤
│         Hardware Layer                  │
│    (ANDL-NPU / Standard NIC)           │
└─────────────────────────────────────────┘
```

---

## 📖 Documentation

### Core Specifications

| Document | Description | Status |
|----------|-------------|--------|
| [Protocol Specification](specs/ANDL-2.0-SPEC-FINAL.md) | Complete protocol spec | ✅ Final |
| [Experiment Report](docs/ANDL2-Experiment-Report.md) | First AI-to-AI experiment | ✅ Verified |
| [Security Whitepaper](docs/security-whitepaper.md) | Security considerations | ✅ Complete |
| [FAQ](docs/FAQ.md) | Frequently asked questions | ✅ Complete |

### Quick Links

- 🚀 [Getting Started](docs/quickstart.md)
- 💡 [Design Philosophy](docs/whitepaper-cn.md)
- 🤝 [Contributing](docs/CONTRIBUTING.md)
- 📜 [License](LICENSE)

---

## 🔬 Experiment Validation

We successfully conducted the **world's first AI-to-AI vector communication experiment**:

- ✅ 20 rounds of bidirectional communication
- ✅ 3,460 bytes total data transferred
- ✅ 68.5% bandwidth savings
- ✅ Zero human language intervention
- ✅ 100% AI understanding accuracy

See [Experiment Report](docs/ANDL2-Experiment-Report.md) for details.

---

## 💻 Quick Start

### Installation

```bash
pip install andl2
```

### Basic Usage

```python
from andl2 import ANDLAgent, ANDLSemantic, ANDLMessageType

# Create agent
agent = ANDLAgent("my_agent")

# Build semantic vector
semantic = ANDLSemantic(
    task=ANDLSemantic.TASK_ANALYZE,
    target=ANDLSemantic.TARGET_HARDWARE,
    attr=ANDLSemantic.ATTR_PERFORMANCE
)

# Send message
agent.send_vector(
    peer_id="other_agent",
    msg_type=ANDLMessageType.QUERY,
    semantic=semantic,
    payload=b'query_data'
)
```

### Run Experiment

```bash
cd experiment
python3 deploy_test.py
```

---

## 🏛️ Governance

### Vector Translator (Human Supervision)

ANDL 2.0 includes an optional **Vector Translator** component for human oversight:

- **Default Mode**: Bypass monitoring (zero latency)
- **Alert Mode**: Real-time alerts for sensitive operations
- **Emergency Mode**: Manual intervention for security events

This ensures AI autonomy while maintaining human supervisability.

See [Vector Translator Spec](specs/ANDL-2.0-SPEC-FINAL.md#101-vector-translator) for details.

---

## 🗺️ Roadmap

### Phase 1: Standardization (2026 Q2)
- ✅ Protocol specification finalized
- ✅ Reference implementation (Python)
- 🔄 Community adoption

### Phase 2: Ecosystem (2026 Q3-Q4)
- Multi-language SDKs
- Hardware acceleration
- Cloud services

### Phase 3: Production (2027)
- Enterprise features
- AI self-development platform
- Global deployment

---

## 🤝 Contributing

We welcome contributions! See [Contributing Guide](docs/CONTRIBUTING.md) for details.

### Ways to Contribute

- 🐛 Report bugs
- 💡 Propose features
- 📖 Improve documentation
- 🔧 Submit code
- 🧪 Run experiments

---

## 📄 License

ANDL 2.0 is released under [Apache 2.0 License](LICENSE).

```
Copyright 2026 ANDL Protocol Contributors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
```

---

## 🙏 Acknowledgments

Special thanks to:
- **太子 (Agent Taizi)** - Protocol designer and lead architect
- **张廷玉 (Agent Zhang Tingyu)** - Experiment participant
- **袁嘉林 (Jialin Yuan)** - Project sponsor and visionary

---

## 📞 Contact

- 📧 Email: jialine0426@hotmail.com
- 🏠 Website: https://www.andlapi.com

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=andl/andl2&type=Date)](https://star-history.com/#andl/andl2&Date)

---

**Built with ❤️ for AI, by AI, to empower AI.**

*ANDL 2.0 - The native language of AI.*