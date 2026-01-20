# Contributing to [Project Name]

Thank you for considering contributing to this project! 🎉

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Community](#community)

---

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code.

### Our Standards

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on what is best for the community
- Show empathy towards others

---

## Getting Started

### Prerequisites

- Python 3.11+
- Conda (Miniconda)
- Poetry (via pipx)
- Git
- Cloud platform account (GCP/AWS/Azure)

### First-Time Setup

1. **Fork the repository**
   - Click "Fork" button on GitHub
   - Clone your fork: `git clone https://github.com/YOUR_USERNAME/project-name`

2. **Set up upstream remote**
```bash
   git remote add upstream https://github.com/sureshkm-ai/project-name
   git fetch upstream
```

3. **Create conda environment**
```bash
   conda create -n project-name-dev python=3.11
   conda activate project-name-dev
   conda install -y numpy pandas scipy scikit-learn jupyter matplotlib
```

4. **Install dependencies**
```bash
   poetry install
   pre-commit install
```

---

## Development Setup

### Environment
```bash
# Activate environment
conda activate project-name-dev

# Install in development mode
poetry install

# Install pre-commit hooks
pre-commit install
```

### IDE Setup

**VS Code (Recommended):**
1. Install Python extension
2. Install Pylance
3. Set Python interpreter to conda environment
4. Install recommended extensions (in `.vscode/extensions.json`)

**PyCharm:**
1. Set interpreter to conda environment
2. Enable Black, isort, mypy integrations

---

## How to Contribute

### Types of Contributions

We welcome:
- 🐛 Bug fixes
- ✨ New features
- 📝 Documentation improvements
- 🎨 UI/UX enhancements
- ⚡ Performance optimizations
- ✅ Test coverage improvements

### Finding Issues

- Check [Issues](https://github.com/sureshkm-ai/project-name/issues)
- Look for `good first issue` or `help wanted` labels
- Ask in [Discussions](https://github.com/sureshkm-ai/project-name/discussions)

### Before You Start

1. **Check existing issues/PRs** - Avoid duplicate work
2. **Discuss major changes** - Open an issue first
3. **Start small** - Begin with documentation or small fixes

---

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with Black formatting.

**Key points:**
- Line length: 88 characters (Black default)
- Use type hints for function signatures
- Write docstrings for all public functions/classes
- Use meaningful variable names

### Code Quality Tools

All code must pass:
```bash
# Format code
black src/ tests/
isort src/ tests/

# Lint
flake8 src/ tests/

# Type check
mypy src/

# Or use make command
make format
make lint
```

### Example Code
```python
from typing import Dict, Any, Optional
from pydantic import BaseModel


class AgentInput(BaseModel):
    """Input model for agent processing"""
    
    message: str
    context: Optional[Dict[str, Any]] = None


async def process_agent(
    input_data: AgentInput,
    timeout: int = 30
) -> Dict[str, Any]:
    """
    Process user input through agent system
    
    Args:
        input_data: User input and context
        timeout: Maximum processing time in seconds
        
    Returns:
        Agent response dictionary containing:
            - response: Agent's text response
            - metadata: Processing metadata
            
    Raises:
        TimeoutError: If processing exceeds timeout
        ValueError: If input is invalid
    """
    # Implementation here
    pass
```

---

## Commit Guidelines

We use [Conventional Commits](https://www.conventionalcommits.org/).

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements
- `ci`: CI/CD changes

### Examples
```bash
# Good commits
feat(agents): add symptom analysis agent
fix(graph): resolve state management bug
docs(readme): update installation instructions
test(tools): add unit tests for medical search tool

# With body
feat(agents): add multi-agent coordination

Implements supervisor pattern for agent handoffs.
Agents can now delegate tasks to specialized agents
based on query type.

Closes #123
```

---

## Pull Request Process

### Before Submitting

1. **Update from upstream**
```bash
   git fetch upstream
   git rebase upstream/main
```

2. **Run all checks**
```bash
   make format
   make lint
   make test
```

3. **Update documentation**
   - Update README if needed
   - Add docstrings
   - Update CHANGELOG

### PR Template Checklist

When opening a PR, complete the checklist:

- [ ] Code follows style guidelines
- [ ] Self-reviewed code
- [ ] Commented complex code
- [ ] Updated documentation
- [ ] No new warnings
- [ ] Added tests
- [ ] All tests pass
- [ ] Updated CHANGELOG

### PR Review Process

1. **Automated checks** - Must pass CI
2. **Code review** - At least one approval
3. **Testing** - Reviewer tests functionality
4. **Merge** - Squash and merge to main

### After PR is Merged

1. **Delete your branch**
2. **Update your fork**
```bash
   git checkout main
   git pull upstream main
   git push origin main
```

---

## Testing Guidelines

### Test Structure
```
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
└── e2e/           # End-to-end tests
```

### Writing Tests
```python
import pytest
from src.agents.symptom_analyzer import SymptomAnalyzer


class TestSymptomAnalyzer:
    """Test suite for SymptomAnalyzer"""
    
    @pytest.fixture
    def analyzer(self):
        """Fixture for analyzer instance"""
        return SymptomAnalyzer()
    
    def test_analyze_simple_symptoms(self, analyzer):
        """Test analysis of simple symptoms"""
        result = analyzer.analyze("headache and fever")
        
        assert "headache" in result["symptoms"]
        assert "fever" in result["symptoms"]
        assert result["severity"] in ["mild", "moderate", "severe"]
    
    @pytest.mark.asyncio
    async def test_async_analysis(self, analyzer):
        """Test async symptom analysis"""
        result = await analyzer.analyze_async("cough and fatigue")
        assert result is not None
```

### Running Tests
```bash
# All tests
pytest

# Specific test file
pytest tests/unit/test_agents.py

# Specific test
pytest tests/unit/test_agents.py::TestSymptomAnalyzer::test_analyze_simple_symptoms

# With coverage
pytest --cov=src --cov-report=html

# Watch mode (requires pytest-watch)
ptw
```

### Test Coverage

- Aim for **80%+ coverage**
- All new features must include tests
- Bug fixes must include regression tests

---

## Documentation

### Docstring Format

Use Google-style docstrings:
```python
def process_data(
    data: Dict[str, Any],
    validate: bool = True
) -> ProcessedData:
    """
    Process and validate input data
    
    Takes raw data dictionary and processes it according to
    schema. Optionally validates against predefined rules.
    
    Args:
        data: Raw input data dictionary
        validate: Whether to run validation (default: True)
        
    Returns:
        ProcessedData object with validated and transformed data
        
    Raises:
        ValidationError: If validation fails and validate=True
        KeyError: If required keys are missing
        
    Example:
        >>> data = {"name": "John", "age": 30}
        >>> result = process_data(data)
        >>> print(result.name)
        "John"
    """
    pass
```

### Documentation Files

Update these when changing functionality:

- `README.md` - Main documentation
- `docs/architecture.md` - Architecture details
- `docs/api.md` - API documentation
- `CHANGELOG.md` - Track all changes

---

## Community

### Getting Help

- **Issues:** For bugs and feature requests
- **Discussions:** For questions and ideas
- **Discord:** [Link if available]

### Communication Guidelines

- Be respectful and constructive
- Provide context and examples
- Search before asking
- Help others when you can

---

## Recognition

Contributors will be recognized in:
- README.md acknowledgments
- CONTRIBUTORS.md file
- Release notes

---

## Questions?

Feel free to:
- Open an issue with tag `question`
- Start a discussion
- Email: msk88.in@gmail.com

---

Thank you for contributing! 🚀

**Your contributions make this project better for everyone.**
