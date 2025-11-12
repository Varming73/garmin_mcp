# Module Refactoring Template

This document provides a template for refactoring the remaining modules to match the new standards implemented in v0.2.0.

## Modules to Refactor

- [ ] health_wellness.py
- [ ] user_profile.py
- [ ] devices.py
- [ ] gear_management.py
- [ ] weight_management.py
- [ ] challenges.py
- [ ] training.py
- [ ] workouts.py
- [ ] data_management.py (partially done)
- [ ] womens_health.py

## Refactoring Checklist

For each module:

- [ ] Add type hints to all functions
- [ ] Add proper imports for typing and validation
- [ ] Replace generic exception handling with specific handling
- [ ] Add logging statements
- [ ] Create Pydantic models for input validation
- [ ] Standardize return types to JSON strings
- [ ] Use response builders (success_response, error_response, not_found_response)
- [ ] Add comprehensive docstrings
- [ ] Create unit tests

## Template Code

### Module Structure

```python
"""
[Module Name] functions for Garmin Connect MCP Server
"""
from typing import Optional

from mcp.server.fastmcp import FastMCP
from garminconnect import Garmin
from pydantic import ValidationError

from garmin_mcp.logging_config import get_logger
from garmin_mcp.response import success_response, error_response, not_found_response
from garmin_mcp.models import (
    DateInput,
    DateRangeInput,
    # Add other relevant models
)

logger = get_logger(__name__)

# The garmin_client will be set by the main file
garmin_client: Optional[Garmin] = None


def configure(client: Garmin) -> None:
    """Configure the module with the Garmin client instance"""
    global garmin_client
    garmin_client = client
    logger.info("[Module name] module configured")


def register_tools(app: FastMCP) -> FastMCP:
    """Register all [module name] tools with the MCP server app"""

    @app.tool()
    async def tool_name(param1: str, param2: int = 0) -> str:
        """
        Tool description

        Args:
            param1: Description of param1
            param2: Description of param2 (default: 0)

        Returns:
            JSON string with data or error
        """
        try:
            # Validate input
            input_data = InputModel(param1=param1, param2=param2)

            logger.info(f"Fetching data with params: {input_data.param1}, {input_data.param2}")

            # Call Garmin API
            result = garmin_client.api_method(input_data.param1, input_data.param2)

            # Check if data exists
            if not result:
                return not_found_response("resource_type", f"params {param1}, {param2}")

            logger.info(f"Successfully retrieved data")
            return success_response(result, message="Data retrieved successfully")

        except ValidationError as e:
            logger.warning(f"Validation error in tool_name: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error in tool_name: {e}")
            return error_response("internal_error", f"Error retrieving data: {str(e)}")

    return app
```

### Input Models Template

Add to `src/garmin_mcp/models.py`:

```python
class YourInputModel(BaseModel):
    """Model for your input validation"""
    param1: str = Field(..., description="Parameter 1 description")
    param2: int = Field(default=0, ge=0, description="Parameter 2 (must be non-negative)")

    @field_validator('param1')
    @classmethod
    def validate_param1(cls, v: str) -> str:
        """Validate param1"""
        if not v:
            raise ValueError('param1 cannot be empty')
        return v
```

### Unit Test Template

Create in `tests/unit/test_[module_name].py`:

```python
"""
Unit tests for [module_name] module
"""
import pytest
import json
from unittest.mock import Mock
from garmin_mcp import [module_name]


class Test[ModuleName]:
    """Test suite for [module_name] functions"""

    def setup_method(self):
        """Setup test fixtures"""
        self.mock_client = Mock()
        [module_name].configure(self.mock_client)

    def test_configure(self):
        """Test module configuration"""
        assert [module_name].garmin_client is not None
        assert [module_name].garmin_client == self.mock_client

    @pytest.mark.asyncio
    async def test_tool_success(self):
        """Test successful tool execution"""
        from mcp.server.fastmcp import FastMCP

        # Setup mock
        self.mock_client.api_method.return_value = {
            "data": "test_value"
        }

        # Create app and register tools
        app = FastMCP("Test")
        app = [module_name].register_tools(app)

        # Verify tool is registered
        tools = {tool.name: tool for tool in app._mcp_server.list_tools_sync().tools}
        assert "tool_name" in tools

    def test_input_validation(self):
        """Test input validation"""
        from garmin_mcp.models import YourInputModel
        from pydantic import ValidationError

        # Valid input
        valid_input = YourInputModel(param1="test", param2=5)
        assert valid_input.param1 == "test"
        assert valid_input.param2 == 5

        # Invalid input
        with pytest.raises(ValidationError):
            YourInputModel(param1="", param2=-1)
```

## Step-by-Step Refactoring Guide

### Step 1: Add Imports

```python
from typing import Optional
from mcp.server.fastmcp import FastMCP
from garminconnect import Garmin
from pydantic import ValidationError

from garmin_mcp.logging_config import get_logger
from garmin_mcp.response import success_response, error_response, not_found_response
from garmin_mcp.models import DateInput, DateRangeInput
```

### Step 2: Add Type Hints

Change:
```python
garmin_client = None

def configure(client):
    global garmin_client
    garmin_client = client

def register_tools(app):
    # ...
```

To:
```python
garmin_client: Optional[Garmin] = None

def configure(client: Garmin) -> None:
    """Configure the module with the Garmin client instance"""
    global garmin_client
    garmin_client = client
    logger.info("Module configured")

def register_tools(app: FastMCP) -> FastMCP:
    """Register all tools with the MCP server app"""
    # ...
```

### Step 3: Add Input Validation

Change:
```python
@app.tool()
async def get_data(date: str) -> str:
    try:
        data = garmin_client.get_data(date)
        if not data:
            return f"No data found for {date}"
        return data
    except Exception as e:
        return f"Error: {str(e)}"
```

To:
```python
@app.tool()
async def get_data(date: str) -> str:
    """
    Get data for a specific date

    Args:
        date: Date in YYYY-MM-DD format

    Returns:
        JSON string with data or error
    """
    try:
        # Validate input
        input_data = DateInput(date=date)

        logger.info(f"Fetching data for date {date}")
        data = garmin_client.get_data(input_data.date)

        if not data:
            return not_found_response("data", f"date {date}")

        logger.info(f"Retrieved data for {date}")
        return success_response(data)

    except ValidationError as e:
        logger.warning(f"Validation error in get_data: {e}")
        return error_response("validation_error", str(e))
    except Exception as e:
        logger.exception(f"Error retrieving data: {e}")
        return error_response("internal_error", f"Error retrieving data: {str(e)}")
```

### Step 4: Add Logging

```python
logger = get_logger(__name__)

# In configure:
logger.info("Module configured")

# In tools:
logger.info(f"Fetching data for {param}")
logger.warning(f"Validation error: {e}")
logger.exception(f"Unexpected error: {e}")
```

### Step 5: Standardize Returns

All returns should use:
- `success_response(data, message=...)`
- `error_response(error_code, message)`
- `not_found_response(resource, identifier)`

### Step 6: Create Tests

Write unit tests following the template above.

## Example: health_wellness.py Refactoring

### Before:
```python
@app.tool()
async def get_stats(date: str) -> str:
    """Get daily activity stats"""
    try:
        stats = garmin_client.get_stats(date)
        if not stats:
            return f"No stats found for {date}"
        return stats
    except Exception as e:
        return f"Error retrieving stats: {str(e)}"
```

### After:
```python
@app.tool()
async def get_stats(date: str) -> str:
    """
    Get daily activity stats

    Args:
        date: Date in YYYY-MM-DD format

    Returns:
        JSON string with stats or error
    """
    try:
        # Validate input
        input_data = DateInput(date=date)

        logger.info(f"Fetching stats for date {date}")
        stats = garmin_client.get_stats(input_data.date)

        if not stats:
            return not_found_response("stats", f"date {date}")

        logger.info(f"Retrieved stats for {date}")
        return success_response(stats, message=f"Stats for {date}")

    except ValidationError as e:
        logger.warning(f"Validation error in get_stats: {e}")
        return error_response("validation_error", str(e))
    except Exception as e:
        logger.exception(f"Error retrieving stats: {e}")
        return error_response("internal_error", f"Error retrieving stats: {str(e)}")
```

## Common Patterns

### Date Validation
```python
from garmin_mcp.models import DateInput
input_data = DateInput(date=date)
# Use input_data.date
```

### Date Range Validation
```python
from garmin_mcp.models import DateRangeInput
input_data = DateRangeInput(start_date=start_date, end_date=end_date)
# Use input_data.start_date, input_data.end_date
```

### ID Validation
```python
from garmin_mcp.models import ActivityIdInput
input_data = ActivityIdInput(activity_id=activity_id)
# Use input_data.activity_id
```

## Notes

- The refactoring maintains backward compatibility for MCP tool names
- All validation happens before calling the Garmin API
- Logging provides traceability without exposing sensitive data
- Standardized responses make parsing easier for AI assistants
- Tests ensure refactoring doesn't break functionality

## Progress Tracking

Update the checklist at the top of this document as modules are refactored.
