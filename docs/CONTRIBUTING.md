# Contributing to ANDL

Thank you for your interest in contributing to ANDL! This document provides guidelines and instructions for contributing.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [How to Contribute](#how-to-contribute)
4. [Development Setup](#development-setup)
5. [Coding Standards](#coding-standards)
6. [Testing](#testing)
7. [Documentation](#documentation)
8. [Community](#community)

---

## Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behavior:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community

**Unacceptable behavior:**
- Trolling, insulting/derogatory comments
- Public or private harassment
- Publishing others' private information
- Other conduct which could reasonably be considered inappropriate

---

## Getting Started

### Ways to Contribute

- **Report bugs**: Open an issue on GitHub
- **Suggest features**: Start a discussion
- **Write code**: Submit a pull request
- **Improve docs**: Fix typos, add examples
- **Help others**: Answer questions on Discord

### Before You Start

1. **Check existing issues**: Avoid duplicates
2. **Discuss major changes**: Open an issue first
3. **Read the whitepaper**: Understand the architecture
4. **Join Discord**: Real-time communication

---

## How to Contribute

### Reporting Bugs

Use GitHub Issues with this template:

```markdown
**Description**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What you expected to happen

**Environment**
- OS: [e.g., Ubuntu 22.04]
- Python: [e.g., 3.10]
- ANDL Version: [e.g., 2.0.0]

**Additional Context**
Screenshots, logs, etc.
```

### Suggesting Features

Use GitHub Discussions:

```markdown
**Feature Request**
Clear description of the feature

**Motivation**
Why is this feature needed?

**Proposed Solution**
How should it work?

**Alternatives**
What else was considered?
```

### Submitting Pull Requests

#### PR Process

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/andl.git
   cd andl
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

3. **Make changes**
   - Write code
   - Add tests
   - Update docs

4. **Commit**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

#### Commit Message Format

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Tests
- `chore`: Maintenance

**Examples:**
```
feat(transport): add RDMA support

fix(compression): handle edge case in sparsification

docs(api): add examples for consensus module
```

---

## Development Setup

### Prerequisites

- Python 3.8+
- Git
- Make (optional)

### Setup Steps

```bash
# 1. Clone repository
git clone https://github.com/andl/andl.git
cd andl

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. Install in development mode
pip install -e .

# 5. Run tests
pytest tests/ -v
```

### Project Structure

```
andl/
├── core/           # Core protocol implementation
├── docs/           # Documentation
├── tests/          # Test suite
├── examples/       # Example code
├── benchmarks/     # Performance benchmarks
└── scripts/        # Utility scripts
```

---

## Coding Standards

### Python Style Guide

Follow [PEP 8](https://pep8.org/) with these additions:

**Formatting:**
- Use `black` for code formatting
- Use `isort` for import sorting
- Max line length: 100 characters

**Type Hints:**
```python
def compress_vector(
    vector: np.ndarray,
    target_bits: int = 8
) -> CompressedVector:
    """Compress a semantic vector."""
    ...
```

**Docstrings:**
```python
def function_name(param: Type) -> ReturnType:
    """
    Short description.
    
    Longer description if needed.
    
    Args:
        param: Description of parameter
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When invalid input
    """
```

### Code Quality Tools

```bash
# Format code
black core/ tests/

# Sort imports
isort core/ tests/

# Lint
flake8 core/ tests/

# Type check
mypy core/

# Run all checks
make lint
```

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Classes | PascalCase | `SemanticGraph` |
| Functions | snake_case | `compress_vector` |
| Constants | UPPER_SNAKE | `DEFAULT_BUFFER_SIZE` |
| Private | _leading_underscore | `_internal_method` |

---

## Testing

### Test Structure

```
tests/
├── test_physical_layer.py
├── test_transport_layer.py
├── test_semantic_layer.py
├── test_application_layer.py
├── test_consensus.py
└── test_integration.py
```

### Writing Tests

```python
import pytest
import numpy as np
from andl import VectorCompressor

class TestVectorCompression:
    """Test vector compression functionality."""
    
    def test_compression_ratio(self):
        """Test that compression reduces size."""
        compressor = VectorCompressor(target_bits=8)
        original = np.random.randn(1024).astype(np.float32)
        
        compressed = compressor.compress(original)
        
        assert compressed.compression_ratio > 1.0
    
    def test_roundtrip(self):
        """Test compress-decompress roundtrip."""
        compressor = VectorCompressor(target_bits=8)
        original = np.random.randn(512).astype(np.float32)
        
        compressed = compressor.compress(original)
        restored = compressor.decompress(compressed)
        
        # Allow small numerical error
        np.testing.assert_allclose(original, restored, rtol=0.1)
```

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_compression.py -v

# Specific test
pytest tests/test_compression.py::TestVectorCompression::test_roundtrip -v

# With coverage
pytest tests/ --cov=andl --cov-report=html

# Parallel execution
pytest tests/ -n auto
```

### Test Coverage

Aim for:
- **L1 Protocol Layer**: 95%+ coverage
- **L2 Implementation**: 90%+ coverage
- **Integration tests**: Critical paths covered

---

## Documentation

### Documentation Types

1. **Code comments**: Explain "why", not "what"
2. **Docstrings**: API documentation
3. **Guides**: Tutorials and how-tos
4. **Whitepapers**: Architecture and design

### Building Docs

```bash
# Install docs dependencies
pip install -r requirements-docs.txt

# Build documentation
mkdocs build

# Serve locally
mkdocs serve
```

### Documentation Style

- Clear and concise
- Include examples
- Keep up-to-date with code
- Use diagrams where helpful

---

## Community

### Communication Channels

| Channel | Purpose | Link |
|---------|---------|------|
| GitHub Issues | Bugs, features | github.com/jialine/andl/issues |
| GitHub Discussions | Questions, ideas | github.com/jialine/andl/discussions |
| Discord | Real-time chat | discord.gg/andl |
| Twitter | Announcements | @andl_protocol |
| Email | Private | jialine0426@hotmail.com|

### Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Invited to contributor events

### Becoming a Maintainer

Long-term contributors may be invited to become maintainers:
- Consistent quality contributions
- Good communication
- Understanding of project values
- Community involvement

---

## License

By contributing, you agree that your contributions will be licensed under the Apache 2.0 License (for L1/L2) or as specified in the dual-licensing agreement.

---

## Questions?

- 📧 Email: jialine0426@hotmail.com

**Thank you for contributing to ANDL! 🚀**