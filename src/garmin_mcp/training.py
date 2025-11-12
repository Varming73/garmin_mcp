"""
Training and performance functions for Garmin Connect MCP Server
"""
from typing import Optional

from mcp.server.fastmcp import FastMCP
from garminconnect import Garmin
from pydantic import ValidationError

from garmin_mcp.logging_config import get_logger
from garmin_mcp.response import success_response, error_response, not_found_response
from garmin_mcp.models import DateInput, DateRangeInput, ActivityIdInput, ProgressSummaryInput

logger = get_logger(__name__)

# The garmin_client will be set by the main file
garmin_client: Optional[Garmin] = None


def configure(client: Garmin) -> None:
    """Configure the module with the Garmin client instance"""
    global garmin_client
    garmin_client = client
    logger.info("Training module configured")


def register_tools(app: FastMCP) -> FastMCP:
    """Register all training-related tools with the MCP server app"""

    @app.tool()
    async def get_progress_summary_between_dates(
        start_date: str, end_date: str, metric: str
    ) -> str:
        """
        Get progress summary for a metric between dates

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            metric: Metric to get progress for (e.g., 'elevationGain', 'duration', 'distance', 'movingDuration')

        Returns:
            JSON string with progress summary or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = ProgressSummaryInput(start_date=start_date, end_date=end_date, metric=metric)

            logger.info(f"Fetching progress summary for {metric} from {start_date} to {end_date}")
            summary = garmin_client.get_progress_summary_between_dates(
                input_data.start_date, input_data.end_date, input_data.metric
            )

            if not summary:
                logger.info(f"No progress summary found for {metric} between {start_date} and {end_date}")
                return not_found_response(
                    f"progress summary for {metric}",
                    f"date range {start_date} to {end_date}"
                )

            logger.info(f"Retrieved progress summary for {metric}")
            return success_response(summary, message=f"Progress summary for {metric} retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_progress_summary_between_dates: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving progress summary: {e}")
            return error_response("internal_error", f"Error retrieving progress summary: {str(e)}")

    @app.tool()
    async def get_hill_score(start_date: str, end_date: str) -> str:
        """
        Get hill score data between dates

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format

        Returns:
            JSON string with hill score data or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DateRangeInput(start_date=start_date, end_date=end_date)

            logger.info(f"Fetching hill score from {start_date} to {end_date}")
            hill_score = garmin_client.get_hill_score(input_data.start_date, input_data.end_date)

            if not hill_score:
                logger.info(f"No hill score data found between {start_date} and {end_date}")
                return not_found_response("hill score data", f"date range {start_date} to {end_date}")

            logger.info("Retrieved hill score data")
            return success_response(hill_score, message="Hill score data retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_hill_score: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving hill score data: {e}")
            return error_response("internal_error", f"Error retrieving hill score data: {str(e)}")

    @app.tool()
    async def get_endurance_score(start_date: str, end_date: str) -> str:
        """
        Get endurance score data between dates

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format

        Returns:
            JSON string with endurance score data or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DateRangeInput(start_date=start_date, end_date=end_date)

            logger.info(f"Fetching endurance score from {start_date} to {end_date}")
            endurance_score = garmin_client.get_endurance_score(input_data.start_date, input_data.end_date)

            if not endurance_score:
                logger.info(f"No endurance score data found between {start_date} and {end_date}")
                return not_found_response("endurance score data", f"date range {start_date} to {end_date}")

            logger.info("Retrieved endurance score data")
            return success_response(endurance_score, message="Endurance score data retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_endurance_score: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving endurance score data: {e}")
            return error_response("internal_error", f"Error retrieving endurance score data: {str(e)}")

    @app.tool()
    async def get_training_effect(activity_id: int) -> str:
        """
        Get training effect data for a specific activity

        Args:
            activity_id: ID of the activity to retrieve training effect for

        Returns:
            JSON string with training effect data or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = ActivityIdInput(activity_id=activity_id)

            logger.info(f"Fetching training effect for activity ID {activity_id}")
            effect = garmin_client.get_training_effect(input_data.activity_id)

            if not effect:
                logger.info(f"No training effect data found for activity ID {activity_id}")
                return not_found_response("training effect data", f"activity ID {activity_id}")

            logger.info(f"Retrieved training effect for activity ID {activity_id}")
            return success_response(effect, message="Training effect data retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_training_effect: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving training effect data: {e}")
            return error_response("internal_error", f"Error retrieving training effect data: {str(e)}")

    @app.tool()
    async def get_max_metrics(date: str) -> str:
        """
        Get max metrics data (like VO2 Max and fitness age)

        Args:
            date: Date in YYYY-MM-DD format

        Returns:
            JSON string with max metrics data or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DateInput(date=date)

            logger.info(f"Fetching max metrics for {date}")
            metrics = garmin_client.get_max_metrics(input_data.date)

            if not metrics:
                logger.info(f"No max metrics data found for {date}")
                return not_found_response("max metrics data", f"date {date}")

            logger.info(f"Retrieved max metrics for {date}")
            return success_response(metrics, message="Max metrics data retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_max_metrics: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving max metrics data: {e}")
            return error_response("internal_error", f"Error retrieving max metrics data: {str(e)}")

    @app.tool()
    async def get_hrv_data(date: str) -> str:
        """
        Get Heart Rate Variability (HRV) data

        Args:
            date: Date in YYYY-MM-DD format

        Returns:
            JSON string with HRV data or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DateInput(date=date)

            logger.info(f"Fetching HRV data for {date}")
            hrv_data = garmin_client.get_hrv_data(input_data.date)

            if not hrv_data:
                logger.info(f"No HRV data found for {date}")
                return not_found_response("HRV data", f"date {date}")

            logger.info(f"Retrieved HRV data for {date}")
            return success_response(hrv_data, message="HRV data retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_hrv_data: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving HRV data: {e}")
            return error_response("internal_error", f"Error retrieving HRV data: {str(e)}")

    @app.tool()
    async def get_fitnessage_data(date: str) -> str:
        """
        Get fitness age data

        Args:
            date: Date in YYYY-MM-DD format

        Returns:
            JSON string with fitness age data or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DateInput(date=date)

            logger.info(f"Fetching fitness age data for {date}")
            fitness_age = garmin_client.get_fitnessage_data(input_data.date)

            if not fitness_age:
                logger.info(f"No fitness age data found for {date}")
                return not_found_response("fitness age data", f"date {date}")

            logger.info(f"Retrieved fitness age data for {date}")
            return success_response(fitness_age, message="Fitness age data retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_fitnessage_data: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving fitness age data: {e}")
            return error_response("internal_error", f"Error retrieving fitness age data: {str(e)}")

    @app.tool()
    async def request_reload(date: str) -> str:
        """
        Request reload of epoch data

        Args:
            date: Date in YYYY-MM-DD format

        Returns:
            JSON string with reload result or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DateInput(date=date)

            logger.info(f"Requesting data reload for {date}")
            result = garmin_client.request_reload(input_data.date)

            logger.info(f"Data reload requested for {date}")
            return success_response(result, message="Data reload requested")

        except ValidationError as e:
            logger.warning(f"Validation error in request_reload: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error requesting data reload: {e}")
            return error_response("internal_error", f"Error requesting data reload: {str(e)}")

    return app
