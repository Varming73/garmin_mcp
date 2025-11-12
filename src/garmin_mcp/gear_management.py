"""
Gear management functions for Garmin Connect MCP Server
"""
from typing import Optional

from mcp.server.fastmcp import FastMCP
from garminconnect import Garmin
from pydantic import ValidationError

from garmin_mcp.logging_config import get_logger
from garmin_mcp.response import success_response, error_response, not_found_response
from garmin_mcp.models import UserProfileIdInput, GearUuidInput

logger = get_logger(__name__)

# The garmin_client will be set by the main file
garmin_client: Optional[Garmin] = None


def configure(client: Garmin) -> None:
    """Configure the module with the Garmin client instance"""
    global garmin_client
    garmin_client = client
    logger.info("Gear management module configured")


def register_tools(app: FastMCP) -> FastMCP:
    """Register all gear management tools with the MCP server app"""

    @app.tool()
    async def get_gear(user_profile_id: str) -> str:
        """
        Get all gear registered with the user account

        Args:
            user_profile_id: User profile ID

        Returns:
            JSON string with gear list or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = UserProfileIdInput(user_profile_id=user_profile_id)

            logger.info(f"Fetching gear for profile {user_profile_id}")
            gear = garmin_client.get_gear(input_data.user_profile_id)

            if not gear:
                logger.info(f"No gear found for profile {user_profile_id}")
                return not_found_response("gear", f"user profile {user_profile_id}")

            logger.info(f"Retrieved gear for profile {user_profile_id}")
            return success_response(gear, message="Gear retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_gear: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving gear: {e}")
            return error_response("internal_error", f"Error retrieving gear: {str(e)}")

    @app.tool()
    async def get_gear_defaults(user_profile_id: str) -> str:
        """
        Get default gear settings

        Args:
            user_profile_id: User profile ID

        Returns:
            JSON string with gear defaults or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = UserProfileIdInput(user_profile_id=user_profile_id)

            logger.info(f"Fetching gear defaults for profile {user_profile_id}")
            defaults = garmin_client.get_gear_defaults(input_data.user_profile_id)

            if not defaults:
                logger.info(f"No gear defaults found for profile {user_profile_id}")
                return not_found_response("gear defaults", f"user profile {user_profile_id}")

            logger.info(f"Retrieved gear defaults for profile {user_profile_id}")
            return success_response(defaults, message="Gear defaults retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_gear_defaults: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving gear defaults: {e}")
            return error_response("internal_error", f"Error retrieving gear defaults: {str(e)}")

    @app.tool()
    async def get_gear_stats(gear_uuid: str) -> str:
        """
        Get statistics for specific gear

        Args:
            gear_uuid: UUID of the gear item

        Returns:
            JSON string with gear stats or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = GearUuidInput(gear_uuid=gear_uuid)

            logger.info(f"Fetching gear stats for UUID {gear_uuid}")
            stats = garmin_client.get_gear_stats(input_data.gear_uuid)

            if not stats:
                logger.info(f"No stats found for gear {gear_uuid}")
                return not_found_response("gear stats", f"UUID {gear_uuid}")

            logger.info(f"Retrieved gear stats for UUID {gear_uuid}")
            return success_response(stats, message="Gear stats retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_gear_stats: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving gear stats: {e}")
            return error_response("internal_error", f"Error retrieving gear stats: {str(e)}")

    return app
