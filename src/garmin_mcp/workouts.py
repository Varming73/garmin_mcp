"""
Workout-related functions for Garmin Connect MCP Server
"""
from typing import Optional

from mcp.server.fastmcp import FastMCP
from garminconnect import Garmin
from pydantic import ValidationError

from garmin_mcp.logging_config import get_logger
from garmin_mcp.response import success_response, error_response, not_found_response
from garmin_mcp.models import WorkoutIdInput, WorkoutJsonInput

logger = get_logger(__name__)

# The garmin_client will be set by the main file
garmin_client: Optional[Garmin] = None


def configure(client: Garmin) -> None:
    """Configure the module with the Garmin client instance"""
    global garmin_client
    garmin_client = client
    logger.info("Workouts module configured")


def register_tools(app: FastMCP) -> FastMCP:
    """Register all workout-related tools with the MCP server app"""

    @app.tool()
    async def get_workouts() -> str:
        """
        Get all workouts

        Returns:
            JSON string with workouts or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            logger.info("Fetching all workouts")
            workouts = garmin_client.get_workouts()

            if not workouts:
                logger.info("No workouts found")
                return not_found_response("workouts", "user account")

            logger.info(f"Retrieved {len(workouts) if isinstance(workouts, list) else 'unknown'} workouts")
            return success_response(workouts, message="Workouts retrieved")

        except Exception as e:
            logger.exception(f"Error retrieving workouts: {e}")
            return error_response("internal_error", f"Error retrieving workouts: {str(e)}")

    @app.tool()
    async def get_workout_by_id(workout_id: int) -> str:
        """
        Get details for a specific workout

        Args:
            workout_id: ID of the workout to retrieve

        Returns:
            JSON string with workout details or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = WorkoutIdInput(workout_id=workout_id)

            logger.info(f"Fetching workout with ID {workout_id}")
            workout = garmin_client.get_workout_by_id(input_data.workout_id)

            if not workout:
                logger.info(f"No workout found with ID {workout_id}")
                return not_found_response("workout", f"ID {workout_id}")

            logger.info(f"Retrieved workout with ID {workout_id}")
            return success_response(workout, message="Workout retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_workout_by_id: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving workout: {e}")
            return error_response("internal_error", f"Error retrieving workout: {str(e)}")

    @app.tool()
    async def download_workout(workout_id: int) -> str:
        """
        Download a workout as a FIT file (returns workout data in FIT format)

        Args:
            workout_id: ID of the workout to download

        Returns:
            JSON string with workout data or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = WorkoutIdInput(workout_id=workout_id)

            logger.info(f"Downloading workout with ID {workout_id}")
            workout_data = garmin_client.download_workout(input_data.workout_id)

            if not workout_data:
                logger.info(f"No workout data found for workout ID {workout_id}")
                return not_found_response("workout data", f"ID {workout_id}")

            logger.info(f"Downloaded workout with ID {workout_id}")
            # Note: Since we can't return binary data directly in JSON,
            # we inform the user that the data is available
            return success_response(
                {"message": f"Workout data for ID {workout_id} is available in FIT format"},
                message="Workout data downloaded"
            )

        except ValidationError as e:
            logger.warning(f"Validation error in download_workout: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error downloading workout: {e}")
            return error_response("internal_error", f"Error downloading workout: {str(e)}")

    @app.tool()
    async def upload_workout(workout_json: str) -> str:
        """
        Upload a workout from JSON data

        Args:
            workout_json: JSON string containing workout data

        Returns:
            JSON string with upload result or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = WorkoutJsonInput(workout_json=workout_json)

            logger.info("Uploading workout from JSON data")
            result = garmin_client.upload_workout(input_data.workout_json)

            logger.info("Workout uploaded successfully")
            return success_response(result, message="Workout uploaded")

        except ValidationError as e:
            logger.warning(f"Validation error in upload_workout: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error uploading workout: {e}")
            return error_response("internal_error", f"Error uploading workout: {str(e)}")

    return app
