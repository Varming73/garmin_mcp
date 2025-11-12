"""
Device-related functions for Garmin Connect MCP Server
"""
from typing import Optional

from mcp.server.fastmcp import FastMCP
from garminconnect import Garmin
from pydantic import ValidationError

from garmin_mcp.logging_config import get_logger
from garmin_mcp.response import success_response, error_response, not_found_response
from garmin_mcp.models import DeviceIdInput, DeviceSolarInput

logger = get_logger(__name__)

# The garmin_client will be set by the main file
garmin_client: Optional[Garmin] = None


def configure(client: Garmin) -> None:
    """Configure the module with the Garmin client instance"""
    global garmin_client
    garmin_client = client
    logger.info("Devices module configured")


def register_tools(app: FastMCP) -> FastMCP:
    """Register all device-related tools with the MCP server app"""

    @app.tool()
    async def get_devices() -> str:
        """
        Get all Garmin devices associated with the user account

        Returns:
            JSON string with devices or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            logger.info("Fetching user devices")
            devices = garmin_client.get_devices()

            if not devices:
                logger.info("No devices found")
                return not_found_response("devices", "user account")

            logger.info(f"Retrieved {len(devices) if isinstance(devices, list) else 'unknown'} devices")
            return success_response(devices, message="Devices retrieved")

        except Exception as e:
            logger.exception(f"Error retrieving devices: {e}")
            return error_response("internal_error", f"Error retrieving devices: {str(e)}")

    @app.tool()
    async def get_device_last_used() -> str:
        """
        Get information about the last used Garmin device

        Returns:
            JSON string with device info or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            logger.info("Fetching last used device")
            device = garmin_client.get_device_last_used()

            if not device:
                logger.info("No last used device found")
                return not_found_response("last used device", "user account")

            logger.info("Retrieved last used device")
            return success_response(device, message="Last used device retrieved")

        except Exception as e:
            logger.exception(f"Error retrieving last used device: {e}")
            return error_response("internal_error", f"Error retrieving last used device: {str(e)}")

    @app.tool()
    async def get_device_settings(device_id: str) -> str:
        """
        Get settings for a specific Garmin device

        Args:
            device_id: Device ID

        Returns:
            JSON string with device settings or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DeviceIdInput(device_id=device_id)

            logger.info(f"Fetching device settings for device ID {device_id}")
            settings = garmin_client.get_device_settings(input_data.device_id)

            if not settings:
                logger.info(f"No settings found for device ID {device_id}")
                return not_found_response("device settings", f"device ID {device_id}")

            logger.info(f"Retrieved settings for device ID {device_id}")
            return success_response(settings, message="Device settings retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_device_settings: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving device settings: {e}")
            return error_response("internal_error", f"Error retrieving device settings: {str(e)}")

    @app.tool()
    async def get_primary_training_device() -> str:
        """
        Get information about the primary training device

        Returns:
            JSON string with device info or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            logger.info("Fetching primary training device")
            device = garmin_client.get_primary_training_device()

            if not device:
                logger.info("No primary training device found")
                return not_found_response("primary training device", "user account")

            logger.info("Retrieved primary training device")
            return success_response(device, message="Primary training device retrieved")

        except Exception as e:
            logger.exception(f"Error retrieving primary training device: {e}")
            return error_response("internal_error", f"Error retrieving primary training device: {str(e)}")

    @app.tool()
    async def get_device_solar_data(device_id: str, date: str) -> str:
        """
        Get solar data for a specific device

        Args:
            device_id: Device ID
            date: Date in YYYY-MM-DD format

        Returns:
            JSON string with solar data or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DeviceSolarInput(device_id=device_id, date=date)

            logger.info(f"Fetching solar data for device ID {device_id} on {date}")
            solar_data = garmin_client.get_device_solar_data(input_data.device_id, input_data.date)

            if not solar_data:
                logger.info(f"No solar data found for device ID {device_id} on {date}")
                return not_found_response(
                    "solar data",
                    f"device ID {device_id} on {date}"
                )

            logger.info(f"Retrieved solar data for device ID {device_id}")
            return success_response(solar_data, message="Device solar data retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_device_solar_data: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving solar data: {e}")
            return error_response("internal_error", f"Error retrieving solar data: {str(e)}")

    @app.tool()
    async def get_device_alarms() -> str:
        """
        Get alarms from all Garmin devices

        Returns:
            JSON string with device alarms or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            logger.info("Fetching device alarms")
            alarms = garmin_client.get_device_alarms()

            if not alarms:
                logger.info("No device alarms found")
                return not_found_response("device alarms", "user account")

            logger.info("Retrieved device alarms")
            return success_response(alarms, message="Device alarms retrieved")

        except Exception as e:
            logger.exception(f"Error retrieving device alarms: {e}")
            return error_response("internal_error", f"Error retrieving device alarms: {str(e)}")

    return app
