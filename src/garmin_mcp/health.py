"""
Health check functionality for Garmin MCP Server
"""
import json
from typing import Dict, Any
from datetime import datetime
from garminconnect import Garmin

from garmin_mcp.logging_config import get_logger

logger = get_logger(__name__)


def check_garmin_connection(client: Garmin) -> Dict[str, Any]:
    """
    Check if Garmin Connect connection is healthy

    Args:
        client: Garmin client instance

    Returns:
        Health check result dictionary
    """
    try:
        # Try a simple API call to verify connectivity
        # Using get_stats for today as a lightweight health check
        today = datetime.now().strftime("%Y-%m-%d")
        client.get_stats(today)

        return {
            "status": "healthy",
            "garmin_connection": "ok",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "garmin_connection": "failed",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


def get_server_info() -> Dict[str, Any]:
    """
    Get server information for health check

    Returns:
        Server info dictionary
    """
    return {
        "name": "Garmin Connect MCP Server",
        "version": "0.2.0",
        "timestamp": datetime.now().isoformat()
    }
