"""
MCP Resources for Garmin Connect Data

Resources provide direct access to data streams that can be referenced by AI assistants.
"""
from typing import Optional
from mcp.server.fastmcp import FastMCP
from garminconnect import Garmin
from datetime import datetime

from garmin_mcp.logging_config import get_logger
from garmin_mcp.response import success_response, error_response

logger = get_logger(__name__)

garmin_client: Optional[Garmin] = None


def configure(client: Garmin) -> None:
    """Configure resources with Garmin client"""
    global garmin_client
    garmin_client = client
    logger.info("Resources module configured")


def register_resources(app: FastMCP) -> FastMCP:
    """
    Register MCP resources with the app

    Resources allow clients to access data without explicit tool calls
    """

    @app.resource("garmin://health/today")
    def get_today_health_summary() -> str:
        """
        Get a summary of today's health metrics

        Returns:
            JSON string with health summary
        """
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            stats = garmin_client.get_stats(today)

            summary = {
                "date": today,
                "steps": stats.get("totalSteps", 0),
                "distance": stats.get("totalDistanceMeters", 0),
                "calories": stats.get("activeKilocalories", 0),
                "floors": stats.get("floorsAscended", 0)
            }

            return success_response(summary, message="Today's health summary")
        except Exception as e:
            logger.exception(f"Error getting today's health summary: {e}")
            return error_response("internal_error", str(e))

    @app.resource("garmin://activities/recent")
    def get_recent_activities_resource() -> str:
        """
        Get recent activities as a resource

        Returns:
            JSON string with recent activities
        """
        try:
            activities = garmin_client.get_activities(0, 10)
            return success_response(activities, message="Recent activities")
        except Exception as e:
            logger.exception(f"Error getting recent activities: {e}")
            return error_response("internal_error", str(e))

    logger.info("MCP resources registered")
    return app
