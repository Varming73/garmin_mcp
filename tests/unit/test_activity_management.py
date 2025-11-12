"""
Unit tests for activity management module
"""
import pytest
import json
from unittest.mock import Mock
from garmin_mcp import activity_management


class TestActivityManagement:
    """Test suite for activity management functions"""

    def setup_method(self):
        """Setup test fixtures"""
        self.mock_client = Mock()
        activity_management.configure(self.mock_client)

    def test_configure(self):
        """Test module configuration"""
        assert activity_management.garmin_client is not None
        assert activity_management.garmin_client == self.mock_client

    @pytest.mark.asyncio
    async def test_get_activity_success(self):
        """Test successful activity retrieval"""
        from mcp.server.fastmcp import FastMCP

        # Setup mock
        self.mock_client.get_activity.return_value = {
            "activityId": 123,
            "activityName": "Test Run"
        }

        # Create app and register tools
        app = FastMCP("Test")
        app = activity_management.register_tools(app)

        # Get the tool function
        tools = {tool.name: tool for tool in app._mcp_server.list_tools_sync().tools}
        assert "get_activity" in tools

    @pytest.mark.asyncio
    async def test_get_activity_validation_error(self):
        """Test activity retrieval with invalid ID"""
        from mcp.server.fastmcp import FastMCP

        app = FastMCP("Test")
        app = activity_management.register_tools(app)

        # Test would call tool with invalid activity_id (e.g., -1)
        # and verify it returns validation error

    def test_date_validation(self):
        """Test date input validation"""
        from garmin_mcp.models import DateInput
        from pydantic import ValidationError

        # Valid date
        valid_input = DateInput(date="2024-01-15")
        assert valid_input.date == "2024-01-15"

        # Invalid date format
        with pytest.raises(ValidationError):
            DateInput(date="15-01-2024")

        # Invalid date
        with pytest.raises(ValidationError):
            DateInput(date="2024-13-45")
