"""
Test script for MCP server functionality
This script tests the MCP server directly without needing Claude Desktop
"""

import asyncio
import sys
import json
import os
from pathlib import Path
from dotenv import load_dotenv

# Import MCP client for testing
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Load environment variables
load_dotenv()


async def test_mcp_server():
    """Test MCP server by simulating a client connection"""

    # Use uvx to run the server (same as production)
    server_command = "uv"
    server_args = ["run", "garmin-mcp"]

    print(f"Testing MCP server using: {server_command} {' '.join(server_args)}")
    print(f"Working directory: {Path.cwd()}")

    # Check if credentials are set
    if not os.environ.get("GARMIN_EMAIL") and not os.environ.get("GARMIN_EMAIL_FILE"):
        print("ERROR: GARMIN_EMAIL or GARMIN_EMAIL_FILE environment variable must be set")
        print("Please set up your credentials in a .env file")
        return

    # Create server parameters
    server_params = StdioServerParameters(
        command=server_command,
        args=server_args,
        env=None,  # Uses current environment which includes .env variables
    )

    try:
        # Connect to server
        print("Connecting to MCP server...")
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                print("Initializing connection...")
                await session.initialize()
                print("Connection initialized successfully!")

                # List available tools
                print("\nListing available tools:")
                tools_response = await session.list_tools()
                print(f"Found {len(tools_response.tools)} tools:")
                for tool in tools_response.tools[:10]:  # Show first 10
                    print(f"  - {tool.name}: {tool.description or 'No description'}")

                if len(tools_response.tools) > 10:
                    print(f"  ... and {len(tools_response.tools) - 10} more")

                # Test listing activities
                print("\nTesting list_activities tool...")
                try:
                    result = await session.call_tool(
                        "list_activities", arguments={"limit": 3}
                    )
                    print("Result received:")
                    response_text = result.content[0].text

                    # Try to parse as JSON for pretty printing
                    try:
                        response_json = json.loads(response_text)
                        print(json.dumps(response_json, indent=2)[:500] + "...")
                    except json.JSONDecodeError:
                        print(response_text[:500] + "...")

                except Exception as e:
                    print(f"ERROR calling list_activities: {str(e)}")

                print("\nMCP server test completed successfully!")

    except Exception as e:
        print(f"ERROR: Failed to connect to MCP server: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(test_mcp_server())
    sys.exit(exit_code or 0)
