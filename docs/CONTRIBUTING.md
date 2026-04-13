# Contributing to ANDL

Thank you for your interest in contributing to ANDL (AI Native Data Link)! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code:

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Respect different viewpoints and experiences

## Getting Started

### Prerequisites

- Python 3.10+
- Git
- Node.js 18+ (for documentation)

### Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/andl.git
cd andl

# Add upstream remote
git remote add upstream https://github.com/jialine/andl.git
```

## How to Contribute

### Reporting Bugs

Before creating a bug report:

1. Check if the issue already exists
2. Use the latest version
3. Collect relevant information

When reporting:

```markdown
**Description**: Clear description of the bug

**Steps to Reproduce**:
1. Step one
2. Step two
3. ...

**Expected Behavior**: What should happen

**Actual Behavior**: What actually happens

**Environment**:
- OS: [e.g., Ubuntu 22.04]
- Python: [e.g., 3.10.4]
- ANDL Version: [e.g., 2.0.1]
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues:

- Use a clear title
- Provide detailed description
- Explain why this enhancement would be useful
- List possible alternatives

### Contributing Code

#### Types of Contributions

- **Bug fixes**: Fix existing issues
- **Features**: Add new functionality
- **Documentation**: Improve docs
- **Tests**: Add test coverage
- **Performance**: Optimize existing code

#### Good First Issues

Look for issues labeled:
- `good first issue`
- `help wanted`
- `documentation`

## Development Setup

### Python Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=andl --cov-report=html

# Run specific test file
pytest tests/test_neural_consensus.py

# Run with verbose output
pytest -v
```

### Building Documentation

```bash
cd docs
pip install -r requirements.txt
make html
```

## Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:

```python
# Maximum line length: 100 characters
# Use 4 spaces for indentation
# Use double quotes for strings

class NeuralConsensus:
    """
    Docstring style: Google style
    
    Args:
        node_count: Number of consensus nodes
        redundancy: Replication factor
        
    Returns:
        ConsensusResult with verification status
    """
    
    def __init__(self, node_count: int = 5, redundancy: int = 3):
        self.node_count = node_count
        self.redundancy = redundancy
```

### Type Hints

Use type hints for all function signatures:

```python
from typing import List, Dict, Optional

def verify_vector(
    vector: np.ndarray,
    threshold: float = 0.67
) -> ConsensusResult:
    ...
```

### Documentation Strings

All public functions must have docstrings:

```python
def store_shard(
    self,
    message_id: str,
    shard_id: int,
    data: np.ndarray
) -> bool:
    """
    Store a vector shard on this node.
    
    Stores the shard data with integrity hash for later
    verification. The shard is persisted to local storage.
    
    Args:
        message_id: Unique identifier for the message
        shard_id: Index of the shard (0-3)
        data: Vector data to store
        
    Returns:
        True if storage successful, False otherwise
        
    Raises:
        StorageError: If disk is full or write fails
        
    Example:
        >>> node = ConsensusNode("node_0")
        >>> success = node.store_shard("msg_001", 0, vector)
        >>> assert success
    """
```

## Testing

### Test Organization

```
tests/
├── unit/              # Unit tests
│   ├── test_encoder.py
│   ├── test_consensus.py
│   └── test_sharding.py
├── integration/       # Integration tests
│   ├── test_network.py
│   └── test_e2e.py
├── performance/       # Performance benchmarks
│   └── test_latency.py
└── fixtures/          # Test data
    └── sample_vectors.npy
```

### Writing Tests

```python
import pytest
import numpy as np
from andl import NeuralConsensus

class TestNeuralConsensus:
    """Test suite for NeuralConsensus"""
    
    @pytest.fixture
    def consensus(self):
        return NeuralConsensus(node_count=3)
    
    def test_store_and_verify(self, consensus):
        """Test basic store and verify flow"""
        vector = np.random.randn(1024)
        result = consensus.store(vector, "test_001")
        
        assert result["status"] == "stored"
        
        verification = consensus.verify("test_001", vector)
        assert verification.status == ConsensusStatus.VALID
    
    def test_tamper_detection(self, consensus):
        """Test detection of tampered vectors"""
        original = np.random.randn(1024)
        consensus.store(original, "test_002")
        
        tampered = np.random.randn(1024)  # Different vector
        verification = consensus.verify("test_002", tampered)
        
        assert verification.status == ConsensusStatus.TAMPERED
```

### Test Coverage

Aim for:
- Minimum 80% code coverage
- 100% coverage for critical paths
- All public APIs tested

## Documentation

### Types of Documentation

1. **Code Documentation**: Docstrings in code
2. **API Documentation**: Auto-generated from docstrings
3. **User Guides**: Markdown files in /docs
4. **Architecture Decision Records**: In /docs/adr

### Documentation Style

- Use clear, concise language
- Include code examples
- Add diagrams where helpful
- Keep examples runnable

### Building Docs

```bash
# Install docs dependencies
pip install -r docs/requirements.txt

# Build HTML docs
cd docs
make html

# Serve locally
python -m http.server 8000 -d _build/html
```

## Commit Message Guidelines

We follow conventional commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation only
- **style**: Code style (formatting)
- **refactor**: Code refactoring
- **test**: Adding tests
- **chore**: Maintenance tasks

### Examples

```
feat(consensus): add dynamic reputation adjustment

Implement automatic reputation scoring based on
verification success rate. Nodes with high success
rates get higher weight in consensus.

Closes #123
```

```
fix(sharding): correct shard boundary calculation

Previous implementation had off-by-one error in
shard decomposition, causing data corruption.

Fixes #456
```

## Pull Request Process

### Before Submitting

1. **Update documentation**: Reflect your changes
2. **Add tests**: Ensure coverage
3. **Run tests**: All tests must pass
4. **Update CHANGELOG**: Add entry for your changes
5. **Rebase**: Keep history clean

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Performance improvement

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
```

### Review Process

1. **Automated checks**: CI must pass
2. **Code review**: At least one approval
3. **Discussion**: Address feedback
4. **Merge**: Maintainers merge approved PRs

### After Merge

- Delete your branch
- Monitor for issues
- Update related documentation

## Release Process

Maintainers follow this process:

1. Update version in `__init__.py`
2. Update CHANGELOG.md
3. Create git tag: `git tag v2.0.2`
4. Push tag: `git push origin v2.0.2`
5. GitHub Actions creates release

## Community

### Communication Channels

- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: General questions
- **Email**: jialine0426@hotmail.com (security issues)

### Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Invited to organization (significant contributions)

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

## Questions?

- Check existing documentation
- Search closed issues
- Ask in GitHub Discussions

---

Thank you for contributing to ANDL! 🚀
