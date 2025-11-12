# Contributing to Garmin MCP Server

Thank you for your interest in contributing to the Garmin MCP Server! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Style](#code-style)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Architecture Guidelines](#architecture-guidelines)

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Follow the project's technical standards

## Getting Started

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Git
- Garmin Connect account (for testing)

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/garmin_mcp.git
   cd garmin_mcp
   ```

3. Add upstream remote:
   ```bash
   git remote add upstream https://github.com/Taxuspt/garmin_mcp.git
   ```

## Development Setup

### 1. Install Dependencies

```bash
# Install all dependencies including dev tools
uv sync --all-extras
```

### 2. Set Up Environment

Create a `.env` file in the project root:

```bash
GARMIN_EMAIL=your-email@example.com
GARMIN_PASSWORD=your-password
LOG_LEVEL=DEBUG
```

**Note**: Never commit `.env` files! They're in `.gitignore`.

### 3. Verify Installation

```bash
# Run tests
uv run pytest

# Check code style
uv run ruff check src/

# Run type checking
uv run mypy src/garmin_mcp --ignore-missing-imports
```

## Code Style

### Python Style Guide

We follow PEP 8 with some modifications:

- **Line length**: 100 characters (configured in `pyproject.toml`)
- **Formatter**: Ruff
- **Linter**: Ruff
- **Type checker**: mypy

### Required Patterns

#### 1. Type Hints

All functions must have type hints:

```python
from typing import Optional
from garminconnect import Garmin

def configure(client: Garmin) -> None:
    """Configure the module with the Garmin client"""
    global garmin_client
    garmin_client = client
```

#### 2. Docstrings

All functions and classes must have docstrings:

```python
async def get_activity(activity_id: int) -> str:
    """
    Get basic activity information

    Args:
        activity_id: ID of the activity to retrieve

    Returns:
        JSON string with activity data or error

    Raises:
        ValidationError: If activity_id is invalid
    """
```

#### 3. Input Validation

Use Pydantic models for all input validation:

```python
from garmin_mcp.models import ActivityIdInput
from pydantic import ValidationError

try:
    input_data = ActivityIdInput(activity_id=activity_id)
    # Use input_data.activity_id
except ValidationError as e:
    return error_response("validation_error", str(e))
```

#### 4. Error Handling

Use specific exception handling and logging:

```python
from garmin_mcp.logging_config import get_logger
from garmin_mcp.response import success_response, error_response

logger = get_logger(__name__)

try:
    result = garmin_client.get_activity(activity_id)
    logger.info(f"Retrieved activity {activity_id}")
    return success_response(result)
except ValidationError as e:
    logger.warning(f"Validation error: {e}")
    return error_response("validation_error", str(e))
except Exception as e:
    logger.exception(f"Unexpected error: {e}")
    return error_response("internal_error", str(e))
```

#### 5. Response Format

All MCP tools must return JSON strings:

```python
from garmin_mcp.response import success_response, error_response, not_found_response

# Success
return success_response(data, message="Operation successful")

# Not found
return not_found_response("activity", f"ID {activity_id}")

# Error
return error_response("error_code", "Error message")
```

### Code Formatting

Before committing, format your code:

```bash
# Format code
uv run ruff format src/

# Check for issues
uv run ruff check src/ --fix
```

## Testing

### Test Structure

```
tests/
├── conftest.py           # Shared fixtures
├── unit/                 # Unit tests (fast, no external deps)
│   ├── test_activity_management.py
│   └── test_models.py
└── integration/          # Integration tests (require credentials)
    └── test_garmin.py
```

### Writing Tests

#### Unit Tests

```python
import pytest
from unittest.mock import Mock
from garmin_mcp import activity_management

class TestActivityManagement:
    def setup_method(self):
        """Setup test fixtures"""
        self.mock_client = Mock()
        activity_management.configure(self.mock_client)

    @pytest.mark.asyncio
    async def test_get_activity_success(self):
        """Test successful activity retrieval"""
        self.mock_client.get_activity.return_value = {
            "activityId": 123,
            "activityName": "Test Run"
        }

        # Test implementation
        # ...
```

#### Integration Tests

Integration tests require real Garmin credentials:

```python
# tests/integration/test_garmin.py
def test_garmin_connection():
    """Test real connection to Garmin Connect"""
    # Only runs if credentials are provided
    # ...
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run only unit tests
uv run pytest tests/unit/

# Run with coverage
uv run pytest --cov=src/garmin_mcp --cov-report=html

# Run specific test
uv run pytest tests/unit/test_activity_management.py::TestActivityManagement::test_get_activity_success
```

## Pull Request Process

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions/modifications

### 2. Make Your Changes

- Write clean, well-documented code
- Add tests for new functionality
- Update documentation as needed
- Follow the code style guidelines

### 3. Commit Your Changes

Use conventional commits:

```bash
git add .
git commit -m "feat: add heart rate zone analysis tool"
git commit -m "fix: correct date validation in activity queries"
git commit -m "docs: update README with new features"
```

Commit message format:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `test:` - Test updates
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks

### 4. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear title and description
- Reference any related issues
- Explain what changed and why
- Include screenshots/examples if applicable

### 5. PR Requirements

Your PR must:
- ✅ Pass all CI checks (linting, tests, type checking)
- ✅ Include tests for new functionality
- ✅ Update documentation if needed
- ✅ Have descriptive commit messages
- ✅ Be based on the latest `main` branch

## Architecture Guidelines

### Module Structure

Each domain module should follow this pattern:

```python
"""
Module description
"""
from typing import Optional
from mcp.server.fastmcp import FastMCP
from garminconnect import Garmin
from pydantic import ValidationError

from garmin_mcp.logging_config import get_logger
from garmin_mcp.response import success_response, error_response
from garmin_mcp.models import YourInputModel

logger = get_logger(__name__)

garmin_client: Optional[Garmin] = None

def configure(client: Garmin) -> None:
    """Configure the module with the Garmin client"""
    global garmin_client
    garmin_client = client
    logger.info("Module configured")

def register_tools(app: FastMCP) -> FastMCP:
    """Register tools with the MCP server"""

    @app.tool()
    async def your_tool(param: str) -> str:
        """Tool description"""
        try:
            # Validate input
            input_data = YourInputModel(param=param)

            # Process
            result = garmin_client.your_method(input_data.param)

            # Return success
            return success_response(result)
        except ValidationError as e:
            logger.warning(f"Validation error: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error: {e}")
            return error_response("internal_error", str(e))

    return app
```

### Adding New Tools

1. Add input validation model to `models.py`
2. Implement tool in appropriate module
3. Add tests in `tests/unit/`
4. Update documentation

### Adding New Modules

1. Create module file in `src/garmin_mcp/`
2. Follow the module structure pattern above
3. Import and configure in `__init__.py`
4. Add comprehensive tests
5. Update README with new functionality

## Questions or Issues?

- Check existing issues and discussions
- Open a new issue for bugs or feature requests
- Join discussions for questions and ideas

Thank you for contributing! 🎉
