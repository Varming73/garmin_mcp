"""
User Profile functions for Garmin Connect MCP Server
"""
from typing import Optional

from mcp.server.fastmcp import FastMCP
from garminconnect import Garmin

from garmin_mcp.logging_config import get_logger
from garmin_mcp.response import success_response, error_response

logger = get_logger(__name__)

# The garmin_client will be set by the main file
garmin_client: Optional[Garmin] = None


def configure(client: Garmin) -> None:
    """Configure the module with the Garmin client instance"""
    global garmin_client
    garmin_client = client
    logger.info("User profile module configured")


def register_tools(app: FastMCP) -> FastMCP:
    """Register all user profile tools with the MCP server app"""

    @app.tool()
    async def get_full_name() -> str:
        """
        Get user's full name from profile

        Returns:
            JSON string with full name or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            logger.info("Fetching user's full name")
            full_name = garmin_client.get_full_name()

            logger.info("Retrieved user's full name")
            return success_response({"full_name": full_name}, message="User's full name retrieved")

        except Exception as e:
            logger.exception(f"Error retrieving user's full name: {e}")
            return error_response("internal_error", f"Error retrieving full name: {str(e)}")

    @app.tool()
    async def get_unit_system() -> str:
        """
        Get user's preferred unit system from profile

        Returns:
            JSON string with unit system or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            logger.info("Fetching user's unit system")
            unit_system = garmin_client.get_unit_system()

            logger.info(f"Retrieved unit system: {unit_system}")
            return success_response({"unit_system": unit_system}, message="Unit system retrieved")

        except Exception as e:
            logger.exception(f"Error retrieving unit system: {e}")
            return error_response("internal_error", f"Error retrieving unit system: {str(e)}")

    @app.tool()
    async def get_user_profile() -> str:
        """
        Get user profile information

        Returns:
            JSON string with profile data or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            logger.info("Fetching user profile")
            profile = garmin_client.get_user_profile()

            if not profile:
                logger.warning("No user profile information found")
                return error_response("data_not_found", "No user profile information found")

            logger.info("Retrieved user profile")
            return success_response(profile, message="User profile retrieved")

        except Exception as e:
            logger.exception(f"Error retrieving user profile: {e}")
            return error_response("internal_error", f"Error retrieving user profile: {str(e)}")

    @app.tool()
    async def get_user_settings() -> str:
        """
        Get user profile settings

        Returns:
            JSON string with settings or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            logger.info("Fetching user profile settings")
            settings = garmin_client.get_userprofile_settings()

            if not settings:
                logger.warning("No user profile settings found")
                return error_response("data_not_found", "No user profile settings found")

            logger.info("Retrieved user profile settings")
            return success_response(settings, message="User settings retrieved")

        except Exception as e:
            logger.exception(f"Error retrieving user settings: {e}")
            return error_response("internal_error", f"Error retrieving user settings: {str(e)}")

    return app
