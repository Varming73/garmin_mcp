"""
Women's health functions for Garmin Connect MCP Server
"""
from typing import Optional

from mcp.server.fastmcp import FastMCP
from garminconnect import Garmin
from pydantic import ValidationError

from garmin_mcp.logging_config import get_logger
from garmin_mcp.response import success_response, error_response, not_found_response
from garmin_mcp.models import DateInput, DateRangeInput

logger = get_logger(__name__)

# The garmin_client will be set by the main file
garmin_client: Optional[Garmin] = None


def configure(client: Garmin) -> None:
    """Configure the module with the Garmin client instance"""
    global garmin_client
    garmin_client = client
    logger.info("Women's health module configured")


def register_tools(app: FastMCP) -> FastMCP:
    """Register all women's health tools with the MCP server app"""

    @app.tool()
    async def get_pregnancy_summary() -> str:
        """
        Get pregnancy summary data

        Returns:
            JSON string with pregnancy summary or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            logger.info("Fetching pregnancy summary")
            summary = garmin_client.get_pregnancy_summary()

            if not summary:
                logger.info("No pregnancy summary data found")
                return not_found_response("pregnancy summary", "current user")

            logger.info("Retrieved pregnancy summary")
            return success_response(summary, message="Pregnancy summary retrieved")

        except Exception as e:
            logger.exception(f"Error retrieving pregnancy summary: {e}")
            return error_response("internal_error", f"Error retrieving pregnancy summary: {str(e)}")

    @app.tool()
    async def get_menstrual_data_for_date(date: str) -> str:
        """
        Get menstrual data for a specific date

        Args:
            date: Date in YYYY-MM-DD format

        Returns:
            JSON string with menstrual data or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DateInput(date=date)

            logger.info(f"Fetching menstrual data for {date}")
            data = garmin_client.get_menstrual_data_for_date(input_data.date)

            if not data:
                return not_found_response("menstrual data", f"date {date}")

            logger.info(f"Retrieved menstrual data for {date}")
            return success_response(data, message=f"Menstrual data for {date}")

        except ValidationError as e:
            logger.warning(f"Validation error in get_menstrual_data_for_date: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving menstrual data: {e}")
            return error_response("internal_error", f"Error retrieving menstrual data: {str(e)}")

    @app.tool()
    async def get_menstrual_calendar_data(start_date: str, end_date: str) -> str:
        """
        Get menstrual calendar data between specified dates

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format

        Returns:
            JSON string with menstrual calendar data or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DateRangeInput(start_date=start_date, end_date=end_date)

            logger.info(f"Fetching menstrual calendar data from {start_date} to {end_date}")
            data = garmin_client.get_menstrual_calendar_data(input_data.start_date, input_data.end_date)

            if not data:
                return not_found_response(
                    "menstrual calendar data",
                    f"date range {start_date} to {end_date}"
                )

            logger.info(f"Retrieved menstrual calendar data")
            return success_response(data, message="Menstrual calendar data retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_menstrual_calendar_data: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving menstrual calendar data: {e}")
            return error_response("internal_error", f"Error retrieving menstrual calendar data: {str(e)}")

    return app
