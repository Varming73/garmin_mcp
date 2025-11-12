"""
Weight management functions for Garmin Connect MCP Server
"""
import datetime
from typing import Optional

from mcp.server.fastmcp import FastMCP
from garminconnect import Garmin
from pydantic import ValidationError

from garmin_mcp.logging_config import get_logger
from garmin_mcp.response import success_response, error_response, not_found_response
from garmin_mcp.models import DateInput, DateRangeInput, WeightInput, WeightWithTimestampsInput, DeleteWeighInsInput

logger = get_logger(__name__)

# The garmin_client will be set by the main file
garmin_client: Optional[Garmin] = None


def configure(client: Garmin) -> None:
    """Configure the module with the Garmin client instance"""
    global garmin_client
    garmin_client = client
    logger.info("Weight management module configured")


def register_tools(app: FastMCP) -> FastMCP:
    """Register all weight management tools with the MCP server app"""

    @app.tool()
    async def get_weigh_ins(start_date: str, end_date: str) -> str:
        """
        Get weight measurements between specified dates

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format

        Returns:
            JSON string with weight measurements or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DateRangeInput(start_date=start_date, end_date=end_date)

            logger.info(f"Fetching weight measurements from {start_date} to {end_date}")
            weigh_ins = garmin_client.get_weigh_ins(input_data.start_date, input_data.end_date)

            if not weigh_ins:
                logger.info(f"No weight measurements found between {start_date} and {end_date}")
                return not_found_response(
                    "weight measurements",
                    f"date range {start_date} to {end_date}"
                )

            logger.info(f"Retrieved weight measurements for date range")
            return success_response(weigh_ins, message="Weight measurements retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_weigh_ins: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving weight measurements: {e}")
            return error_response("internal_error", f"Error retrieving weight measurements: {str(e)}")

    @app.tool()
    async def get_daily_weigh_ins(date: str) -> str:
        """
        Get weight measurements for a specific date

        Args:
            date: Date in YYYY-MM-DD format

        Returns:
            JSON string with weight measurements or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DateInput(date=date)

            logger.info(f"Fetching weight measurements for {date}")
            weigh_ins = garmin_client.get_daily_weigh_ins(input_data.date)

            if not weigh_ins:
                logger.info(f"No weight measurements found for {date}")
                return not_found_response("weight measurements", f"date {date}")

            logger.info(f"Retrieved weight measurements for {date}")
            return success_response(weigh_ins, message=f"Weight measurements for {date}")

        except ValidationError as e:
            logger.warning(f"Validation error in get_daily_weigh_ins: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving daily weight measurements: {e}")
            return error_response("internal_error", f"Error retrieving daily weight measurements: {str(e)}")

    @app.tool()
    async def delete_weigh_ins(date: str, delete_all: bool = False) -> str:
        """
        Delete weight measurements for a specific date

        Args:
            date: Date in YYYY-MM-DD format
            delete_all: Whether to delete all measurements for the day (default: False for safety)

        Returns:
            JSON string with deletion result or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DeleteWeighInsInput(date=date, delete_all=delete_all)

            logger.info(f"Deleting weight measurements for {date} (delete_all={delete_all})")
            result = garmin_client.delete_weigh_ins(input_data.date, delete_all=input_data.delete_all)

            logger.info(f"Successfully deleted weight measurements for {date}")
            return success_response(result, message=f"Weight measurements deleted for {date}")

        except ValidationError as e:
            logger.warning(f"Validation error in delete_weigh_ins: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error deleting weight measurements: {e}")
            return error_response("internal_error", f"Error deleting weight measurements: {str(e)}")

    @app.tool()
    async def add_weigh_in(weight: float, unit_key: str = "kg") -> str:
        """
        Add a new weight measurement

        Args:
            weight: Weight value (must be positive, up to 1000)
            unit_key: Unit of weight ('kg' or 'lb', default: 'kg')

        Returns:
            JSON string with result or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = WeightInput(weight=weight, unit_key=unit_key)

            logger.info(f"Adding weight measurement: {weight} {unit_key}")
            result = garmin_client.add_weigh_in(weight=input_data.weight, unitKey=input_data.unit_key)

            logger.info(f"Successfully added weight measurement")
            return success_response(result, message="Weight measurement added")

        except ValidationError as e:
            logger.warning(f"Validation error in add_weigh_in: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error adding weight measurement: {e}")
            return error_response("internal_error", f"Error adding weight measurement: {str(e)}")

    @app.tool()
    async def add_weigh_in_with_timestamps(
        weight: float,
        unit_key: str = "kg",
        date_timestamp: str = None,
        gmt_timestamp: str = None
    ) -> str:
        """
        Add a new weight measurement with specific timestamps

        Args:
            weight: Weight value (must be positive, up to 1000)
            unit_key: Unit of weight ('kg' or 'lb', default: 'kg')
            date_timestamp: Local timestamp in format YYYY-MM-DDThh:mm:ss (optional, auto-generated if not provided)
            gmt_timestamp: GMT timestamp in format YYYY-MM-DDThh:mm:ss (optional, auto-generated if not provided)

        Returns:
            JSON string with result or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Generate timestamps if not provided
            if date_timestamp is None or gmt_timestamp is None:
                now = datetime.datetime.now()
                date_timestamp = now.strftime('%Y-%m-%dT%H:%M:%S')
                gmt_timestamp = now.astimezone(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')

            # Validate input
            input_data = WeightWithTimestampsInput(
                weight=weight,
                unit_key=unit_key,
                date_timestamp=date_timestamp,
                gmt_timestamp=gmt_timestamp
            )

            logger.info(f"Adding weight measurement with timestamps: {weight} {unit_key}")
            result = garmin_client.add_weigh_in_with_timestamps(
                weight=input_data.weight,
                unitKey=input_data.unit_key,
                dateTimestamp=input_data.date_timestamp,
                gmtTimestamp=input_data.gmt_timestamp
            )

            logger.info(f"Successfully added weight measurement with timestamps")
            return success_response(result, message="Weight measurement with timestamps added")

        except ValidationError as e:
            logger.warning(f"Validation error in add_weigh_in_with_timestamps: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error adding weight measurement with timestamps: {e}")
            return error_response("internal_error", f"Error adding weight measurement with timestamps: {str(e)}")

    return app
