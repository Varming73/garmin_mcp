"""
Activity Management functions for Garmin Connect MCP Server
"""
from typing import Optional

from mcp.server.fastmcp import FastMCP
from garminconnect import Garmin
from pydantic import ValidationError

from garmin_mcp.logging_config import get_logger
from garmin_mcp.response import success_response, error_response, not_found_response
from garmin_mcp.models import (
    ActivityQueryInput,
    DateInput,
    ActivityIdInput
)

logger = get_logger(__name__)

# The garmin_client will be set by the main file
garmin_client: Optional[Garmin] = None


def configure(client: Garmin) -> None:
    """Configure the module with the Garmin client instance"""
    global garmin_client
    garmin_client = client
    logger.info("Activity management module configured")


def register_tools(app: FastMCP) -> FastMCP:
    """Register all activity management tools with the MCP server app"""

    @app.tool()
    async def get_activities_by_date(start_date: str, end_date: str, activity_type: str = "") -> str:
        """
        Get activities data between specified dates, optionally filtered by activity type

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            activity_type: Optional activity type filter (e.g., cycling, running, swimming)

        Returns:
            JSON string with activity data or error
        """
        try:
            # Validate input
            input_data = ActivityQueryInput(
                start_date=start_date,
                end_date=end_date,
                activity_type=activity_type
            )

            logger.info(f"Fetching activities from {start_date} to {end_date}, type: {activity_type or 'all'}")
            activities = garmin_client.get_activities_by_date(
                input_data.start_date,
                input_data.end_date,
                input_data.activity_type
            )

            if not activities:
                return not_found_response(
                    "activities",
                    f"date range {start_date} to {end_date}" +
                    (f" with type '{activity_type}'" if activity_type else "")
                )

            logger.info(f"Found {len(activities)} activities")
            return success_response(activities, message=f"Found {len(activities)} activities")

        except ValidationError as e:
            logger.warning(f"Validation error in get_activities_by_date: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving activities by date: {e}")
            return error_response("internal_error", f"Error retrieving activities: {str(e)}")

    @app.tool()
    async def get_activities_for_date(date: str) -> str:
        """
        Get activities for a specific date

        Args:
            date: Date in YYYY-MM-DD format

        Returns:
            JSON string with activity data or error
        """
        try:
            # Validate input
            input_data = DateInput(date=date)

            logger.info(f"Fetching activities for date {date}")
            activities = garmin_client.get_activities_fordate(input_data.date)

            if not activities:
                return not_found_response("activities", f"date {date}")

            logger.info(f"Found {len(activities)} activities for {date}")
            return success_response(activities, message=f"Found {len(activities)} activities")

        except ValidationError as e:
            logger.warning(f"Validation error in get_activities_for_date: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving activities for date: {e}")
            return error_response("internal_error", f"Error retrieving activities: {str(e)}")

    @app.tool()
    async def get_activity(activity_id: int) -> str:
        """
        Get basic activity information

        Args:
            activity_id: ID of the activity to retrieve

        Returns:
            JSON string with activity data or error
        """
        try:
            # Validate input
            input_data = ActivityIdInput(activity_id=activity_id)

            logger.info(f"Fetching activity {activity_id}")
            activity = garmin_client.get_activity(input_data.activity_id)

            if not activity:
                return not_found_response("activity", f"ID {activity_id}")

            logger.info(f"Retrieved activity {activity_id}")
            return success_response(activity)

        except ValidationError as e:
            logger.warning(f"Validation error in get_activity: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving activity {activity_id}: {e}")
            return error_response("internal_error", f"Error retrieving activity: {str(e)}")

    @app.tool()
    async def get_activity_splits(activity_id: int) -> str:
        """
        Get splits for an activity

        Args:
            activity_id: ID of the activity to retrieve splits for

        Returns:
            JSON string with splits data or error
        """
        try:
            # Validate input
            input_data = ActivityIdInput(activity_id=activity_id)

            logger.info(f"Fetching splits for activity {activity_id}")
            splits = garmin_client.get_activity_splits(input_data.activity_id)

            if not splits:
                return not_found_response("splits", f"activity ID {activity_id}")

            logger.info(f"Retrieved splits for activity {activity_id}")
            return success_response(splits)

        except ValidationError as e:
            logger.warning(f"Validation error in get_activity_splits: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving activity splits: {e}")
            return error_response("internal_error", f"Error retrieving splits: {str(e)}")

    @app.tool()
    async def get_activity_split_summaries(activity_id: int) -> str:
        """
        Get split summaries for an activity

        Args:
            activity_id: ID of the activity to retrieve split summaries for

        Returns:
            JSON string with split summaries or error
        """
        try:
            # Validate input
            input_data = ActivityIdInput(activity_id=activity_id)

            logger.info(f"Fetching split summaries for activity {activity_id}")
            split_summaries = garmin_client.get_activity_split_summaries(input_data.activity_id)

            if not split_summaries:
                return not_found_response("split summaries", f"activity ID {activity_id}")

            logger.info(f"Retrieved split summaries for activity {activity_id}")
            return success_response(split_summaries)

        except ValidationError as e:
            logger.warning(f"Validation error in get_activity_split_summaries: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving split summaries: {e}")
            return error_response("internal_error", f"Error retrieving split summaries: {str(e)}")

    @app.tool()
    async def get_activity_weather(activity_id: int) -> str:
        """
        Get weather data for an activity

        Args:
            activity_id: ID of the activity to retrieve weather data for

        Returns:
            JSON string with weather data or error
        """
        try:
            # Validate input
            input_data = ActivityIdInput(activity_id=activity_id)

            logger.info(f"Fetching weather data for activity {activity_id}")
            weather = garmin_client.get_activity_weather(input_data.activity_id)

            if not weather:
                return not_found_response("weather data", f"activity ID {activity_id}")

            logger.info(f"Retrieved weather data for activity {activity_id}")
            return success_response(weather)

        except ValidationError as e:
            logger.warning(f"Validation error in get_activity_weather: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving weather data: {e}")
            return error_response("internal_error", f"Error retrieving weather data: {str(e)}")

    @app.tool()
    async def get_activity_heart_rate_zones(activity_id: int) -> str:
        """
        Get heart rate zone data for an activity

        Args:
            activity_id: ID of the activity to retrieve heart rate zone data for

        Returns:
            JSON string with heart rate zone data or error
        """
        try:
            # Validate input
            input_data = ActivityIdInput(activity_id=activity_id)

            logger.info(f"Fetching heart rate zones for activity {activity_id}")
            hr_zones = garmin_client.get_activity_hr_in_timezones(input_data.activity_id)

            if not hr_zones:
                return not_found_response("heart rate zones", f"activity ID {activity_id}")

            logger.info(f"Retrieved heart rate zones for activity {activity_id}")
            return success_response(hr_zones)

        except ValidationError as e:
            logger.warning(f"Validation error in get_activity_heart_rate_zones: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving heart rate zones: {e}")
            return error_response("internal_error", f"Error retrieving heart rate zones: {str(e)}")

    @app.tool()
    async def get_activity_gear(activity_id: int) -> str:
        """
        Get gear data used for an activity

        Args:
            activity_id: ID of the activity to retrieve gear data for

        Returns:
            JSON string with gear data or error
        """
        try:
            # Validate input
            input_data = ActivityIdInput(activity_id=activity_id)

            logger.info(f"Fetching gear data for activity {activity_id}")
            gear = garmin_client.get_activity_gear(input_data.activity_id)

            if not gear:
                return not_found_response("gear data", f"activity ID {activity_id}")

            logger.info(f"Retrieved gear data for activity {activity_id}")
            return success_response(gear)

        except ValidationError as e:
            logger.warning(f"Validation error in get_activity_gear: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving gear data: {e}")
            return error_response("internal_error", f"Error retrieving gear data: {str(e)}")

    @app.tool()
    async def get_activity_exercise_sets(activity_id: int) -> str:
        """
        Get exercise sets for strength training activities

        Args:
            activity_id: ID of the activity to retrieve exercise sets for

        Returns:
            JSON string with exercise sets or error
        """
        try:
            # Validate input
            input_data = ActivityIdInput(activity_id=activity_id)

            logger.info(f"Fetching exercise sets for activity {activity_id}")
            exercise_sets = garmin_client.get_activity_exercise_sets(input_data.activity_id)

            if not exercise_sets:
                return not_found_response("exercise sets", f"activity ID {activity_id}")

            logger.info(f"Retrieved exercise sets for activity {activity_id}")
            return success_response(exercise_sets)

        except ValidationError as e:
            logger.warning(f"Validation error in get_activity_exercise_sets: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving exercise sets: {e}")
            return error_response("internal_error", f"Error retrieving exercise sets: {str(e)}")

    return app
