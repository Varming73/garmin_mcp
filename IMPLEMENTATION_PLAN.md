# Implementation Plan: Critical Fixes for Garmin MCP Server

## Overview
This document outlines the comprehensive refactoring plan to address critical code quality, security, and MCP compliance issues.

## Architecture Changes

### 1. Remove Global State Pattern
**Current**: Each module uses `garmin_client = None` global variable
**New**: Use class-based managers with dependency injection

```python
# Old pattern
garmin_client = None
def configure(client):
    global garmin_client
    garmin_client = client

# New pattern
class ActivityManager:
    def __init__(self, client: Garmin):
        self.client = client
```

### 2. Structured Error Handling
**Components**:
- Custom exception hierarchy in `exceptions.py`
- Centralized logging configuration
- Structured error responses as JSON

### 3. Type Safety with Pydantic
**Add**:
- `models.py` with Pydantic models for request/response validation
- Full type hints throughout codebase
- Runtime validation for all inputs

### 4. Standardized Return Types
**All MCP tools return**:
```json
{
  "success": true,
  "data": {...},
  "error": null
}
```

## Implementation Order

### Phase 1: Foundation (P0 - Critical)
1. Create `exceptions.py` with custom exceptions
2. Create `logging_config.py` with structured logging
3. Create `models.py` with Pydantic validation models
4. Create `response.py` with standardized response builder

### Phase 2: Core Refactoring (P0 - Critical)
5. Refactor `__init__.py`:
   - Remove dead code
   - Fix variable shadowing
   - Move credential loading to function
   - Add type hints
6. Refactor all modules to class-based pattern
7. Add comprehensive error handling
8. Add input validation

### Phase 3: Testing Infrastructure (P0 - Critical)
9. Fix test file bug (reference to non-existent file)
10. Create `conftest.py` with pytest fixtures
11. Add unit tests for each module
12. Add GitHub Actions CI/CD workflow

### Phase 4: MCP Enhancements (P1 - Important)
13. Standardize all tool return types
14. Add MCP resources
15. Add MCP prompts
16. Add health check endpoint
17. Improve tool naming consistency

### Phase 5: Documentation (P1 - Important)
18. Complete security documentation
19. Add API reference documentation
20. Create CONTRIBUTING.md

### Phase 6: Dependencies & Polish (P2 - Medium)
21. Update dependency versions
22. Add dependabot configuration
23. Final testing and validation

## File Structure Changes

```
garmin_mcp/
├── src/garmin_mcp/
│   ├── __init__.py              # Refactored main entry
│   ├── exceptions.py            # NEW: Custom exceptions
│   ├── logging_config.py        # NEW: Logging setup
│   ├── models.py                # NEW: Pydantic models
│   ├── response.py              # NEW: Response builders
│   ├── health.py                # NEW: Health check
│   ├── managers/                # NEW: Manager classes
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── activity.py
│   │   ├── health_wellness.py
│   │   ├── ...
│   ├── resources/               # NEW: MCP resources
│   │   └── __init__.py
│   └── prompts/                 # NEW: MCP prompts
│       └── __init__.py
├── tests/
│   ├── conftest.py              # NEW: Pytest config
│   ├── unit/                    # NEW: Unit tests
│   │   ├── test_activity_manager.py
│   │   ├── ...
│   ├── integration/
│   │   └── test_garmin.py       # Moved
│   └── mcp/
│       └── test_mcp_server.py   # Fixed
├── .github/
│   └── workflows/
│       ├── ci.yml               # NEW: CI/CD
│       └── dependabot.yml       # NEW: Dependency updates
├── docs/
│   ├── SECURITY.md              # NEW: Security docs
│   └── API.md                   # NEW: API reference
└── CONTRIBUTING.md              # NEW: Contribution guide
```

## Key Design Decisions

1. **Manager Pattern**: Each domain gets a manager class injected with client
2. **Pydantic Validation**: All inputs validated before processing
3. **Structured Logging**: JSON logs with context for production
4. **Graceful Degradation**: MCP resources/prompts optional
5. **Backward Compatibility**: Keep existing tool names where sensible

## Success Criteria

- [ ] All files have type hints with mypy validation
- [ ] No global state variables
- [ ] All errors logged with context
- [ ] Input validation on all tools
- [ ] 80%+ test coverage
- [ ] CI/CD passing
- [ ] Security docs complete
- [ ] All MCP tools return consistent JSON
