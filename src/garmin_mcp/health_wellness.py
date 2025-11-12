"""
Health & Wellness Data functions for Garmin Connect MCP Server
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
    logger.info("Health & Wellness module configured")


def register_tools(app: FastMCP) -> FastMCP:
    """Register all health and wellness tools with the MCP server app"""

    @app.tool()
    async def get_stats(date: str) -> str:
        """
        Get daily activity stats

        Args:
            date: Date in YYYY-MM-DD format

        Returns:
            JSON string with stats or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DateInput(date=date)

            logger.info(f"Fetching stats for {date}")
            stats = garmin_client.get_stats(input_data.date)

            if not stats:
                logger.info(f"No stats found for {date}")
                return not_found_response("stats", f"date {date}")

            logger.info(f"Retrieved stats for {date}")
            return success_response(stats, message="Stats retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_stats: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving stats: {e}")
            return error_response("internal_error", f"Error retrieving stats: {str(e)}")

    @app.tool()
    async def get_user_summary(date: str) -> str:
        """
        Get user summary data (compatible with garminconnect-ha)

        Args:
            date: Date in YYYY-MM-DD format

        Returns:
            JSON string with user summary or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DateInput(date=date)

            logger.info(f"Fetching user summary for {date}")
            summary = garmin_client.get_user_summary(input_data.date)

            if not summary:
                logger.info(f"No user summary found for {date}")
                return not_found_response("user summary", f"date {date}")

            logger.info(f"Retrieved user summary for {date}")
            return success_response(summary, message="User summary retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_user_summary: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving user summary: {e}")
            return error_response("internal_error", f"Error retrieving user summary: {str(e)}")

    @app.tool()
    async def get_body_composition(start_date: str, end_date: str = None) -> str:
        """
        Get body composition data for a single date or date range

        Args:
            start_date: Date in YYYY-MM-DD format or start date if end_date provided
            end_date: Optional end date in YYYY-MM-DD format for date range

        Returns:
            JSON string with body composition data or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input based on whether we have a date range or single date
            if end_date:
                # Validate date range
                input_data = DateRangeInput(start_date=start_date, end_date=end_date)
                logger.info(f"Fetching body composition from {start_date} to {end_date}")
                composition = garmin_client.get_body_composition(input_data.start_date, input_data.end_date)

                if not composition:
                    logger.info(f"No body composition data found between {start_date} and {end_date}")
                    return not_found_response(
                        "body composition data",
                        f"date range {start_date} to {end_date}"
                    )
            else:
                # Validate single date
                input_data = DateInput(date=start_date)
                logger.info(f"Fetching body composition for {start_date}")
                composition = garmin_client.get_body_composition(input_data.date)

                if not composition:
                    logger.info(f"No body composition data found for {start_date}")
                    return not_found_response("body composition data", f"date {start_date}")

            logger.info("Retrieved body composition data")
            return success_response(composition, message="Body composition data retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_body_composition: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving body composition data: {e}")
            return error_response("internal_error", f"Error retrieving body composition data: {str(e)}")

    @app.tool()
    async def get_stats_and_body(date: str) -> str:
        """
        Get stats and body composition data

        Args:
            date: Date in YYYY-MM-DD format

        Returns:
            JSON string with stats and body composition or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DateInput(date=date)

            logger.info(f"Fetching stats and body composition for {date}")
            data = garmin_client.get_stats_and_body(input_data.date)

            if not data:
                logger.info(f"No stats and body composition data found for {date}")
                return not_found_response("stats and body composition data", f"date {date}")

            logger.info(f"Retrieved stats and body composition for {date}")
            return success_response(data, message="Stats and body composition retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_stats_and_body: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving stats and body composition data: {e}")
            return error_response("internal_error", f"Error retrieving stats and body composition data: {str(e)}")

    @app.tool()
    async def get_steps_data(date: str) -> str:
        """
        Get steps data

        Args:
            date: Date in YYYY-MM-DD format

        Returns:
            JSON string with steps data or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DateInput(date=date)

            logger.info(f"Fetching steps data for {date}")
            steps_data = garmin_client.get_steps_data(input_data.date)

            if not steps_data:
                logger.info(f"No steps data found for {date}")
                return not_found_response("steps data", f"date {date}")

            logger.info(f"Retrieved steps data for {date}")
            return success_response(steps_data, message="Steps data retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_steps_data: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving steps data: {e}")
            return error_response("internal_error", f"Error retrieving steps data: {str(e)}")

    @app.tool()
    async def get_daily_steps(start_date: str, end_date: str) -> str:
        """
        Get steps data for a date range

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format

        Returns:
            JSON string with daily steps data or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DateRangeInput(start_date=start_date, end_date=end_date)

            logger.info(f"Fetching daily steps from {start_date} to {end_date}")
            steps_data = garmin_client.get_daily_steps(input_data.start_date, input_data.end_date)

            if not steps_data:
                logger.info(f"No daily steps data found between {start_date} and {end_date}")
                return not_found_response("daily steps data", f"date range {start_date} to {end_date}")

            logger.info("Retrieved daily steps data")
            return success_response(steps_data, message="Daily steps data retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_daily_steps: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving daily steps data: {e}")
            return error_response("internal_error", f"Error retrieving daily steps data: {str(e)}")

    @app.tool()
    async def get_training_readiness(date: str) -> str:
        """
        Get training readiness data

        Args:
            date: Date in YYYY-MM-DD format

        Returns:
            JSON string with training readiness or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DateInput(date=date)

            logger.info(f"Fetching training readiness for {date}")
            readiness = garmin_client.get_training_readiness(input_data.date)

            if not readiness:
                logger.info(f"No training readiness data found for {date}")
                return not_found_response("training readiness data", f"date {date}")

            logger.info(f"Retrieved training readiness for {date}")
            return success_response(readiness, message="Training readiness retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_training_readiness: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving training readiness data: {e}")
            return error_response("internal_error", f"Error retrieving training readiness data: {str(e)}")

    @app.tool()
    async def get_body_battery(start_date: str, end_date: str) -> str:
        """
        Get body battery data

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format

        Returns:
            JSON string with body battery data or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DateRangeInput(start_date=start_date, end_date=end_date)

            logger.info(f"Fetching body battery from {start_date} to {end_date}")
            battery_data = garmin_client.get_body_battery(input_data.start_date, input_data.end_date)

            if not battery_data:
                logger.info(f"No body battery data found between {start_date} and {end_date}")
                return not_found_response("body battery data", f"date range {start_date} to {end_date}")

            logger.info("Retrieved body battery data")
            return success_response(battery_data, message="Body battery data retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_body_battery: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving body battery data: {e}")
            return error_response("internal_error", f"Error retrieving body battery data: {str(e)}")

    @app.tool()
    async def get_body_battery_events(date: str) -> str:
        """
        Get body battery events data

        Args:
            date: Date in YYYY-MM-DD format

        Returns:
            JSON string with body battery events or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DateInput(date=date)

            logger.info(f"Fetching body battery events for {date}")
            events = garmin_client.get_body_battery_events(input_data.date)

            if not events:
                logger.info(f"No body battery events found for {date}")
                return not_found_response("body battery events", f"date {date}")

            logger.info(f"Retrieved body battery events for {date}")
            return success_response(events, message="Body battery events retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_body_battery_events: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving body battery events: {e}")
            return error_response("internal_error", f"Error retrieving body battery events: {str(e)}")

    @app.tool()
    async def get_blood_pressure(start_date: str, end_date: str) -> str:
        """
        Get blood pressure data

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format

        Returns:
            JSON string with blood pressure data or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DateRangeInput(start_date=start_date, end_date=end_date)

            logger.info(f"Fetching blood pressure from {start_date} to {end_date}")
            bp_data = garmin_client.get_blood_pressure(input_data.start_date, input_data.end_date)

            if not bp_data:
                logger.info(f"No blood pressure data found between {start_date} and {end_date}")
                return not_found_response("blood pressure data", f"date range {start_date} to {end_date}")

            logger.info("Retrieved blood pressure data")
            return success_response(bp_data, message="Blood pressure data retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_blood_pressure: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving blood pressure data: {e}")
            return error_response("internal_error", f"Error retrieving blood pressure data: {str(e)}")

    @app.tool()
    async def get_floors(date: str) -> str:
        """
        Get floors climbed data

        Args:
            date: Date in YYYY-MM-DD format

        Returns:
            JSON string with floors data or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DateInput(date=date)

            logger.info(f"Fetching floors data for {date}")
            floors_data = garmin_client.get_floors(input_data.date)

            if not floors_data:
                logger.info(f"No floors data found for {date}")
                return not_found_response("floors data", f"date {date}")

            logger.info(f"Retrieved floors data for {date}")
            return success_response(floors_data, message="Floors data retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_floors: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving floors data: {e}")
            return error_response("internal_error", f"Error retrieving floors data: {str(e)}")

    @app.tool()
    async def get_training_status(date: str) -> str:
        """
        Get training status data

        Args:
            date: Date in YYYY-MM-DD format

        Returns:
            JSON string with training status or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DateInput(date=date)

            logger.info(f"Fetching training status for {date}")
            status = garmin_client.get_training_status(input_data.date)

            if not status:
                logger.info(f"No training status data found for {date}")
                return not_found_response("training status data", f"date {date}")

            logger.info(f"Retrieved training status for {date}")
            return success_response(status, message="Training status retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_training_status: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving training status data: {e}")
            return error_response("internal_error", f"Error retrieving training status data: {str(e)}")

    @app.tool()
    async def get_rhr_day(date: str) -> str:
        """
        Get resting heart rate data

        Args:
            date: Date in YYYY-MM-DD format

        Returns:
            JSON string with resting heart rate or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DateInput(date=date)

            logger.info(f"Fetching resting heart rate for {date}")
            rhr_data = garmin_client.get_rhr_day(input_data.date)

            if not rhr_data:
                logger.info(f"No resting heart rate data found for {date}")
                return not_found_response("resting heart rate data", f"date {date}")

            logger.info(f"Retrieved resting heart rate for {date}")
            return success_response(rhr_data, message="Resting heart rate retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_rhr_day: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving resting heart rate data: {e}")
            return error_response("internal_error", f"Error retrieving resting heart rate data: {str(e)}")

    @app.tool()
    async def get_heart_rates(date: str) -> str:
        """
        Get heart rate data

        Args:
            date: Date in YYYY-MM-DD format

        Returns:
            JSON string with heart rate data or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DateInput(date=date)

            logger.info(f"Fetching heart rate data for {date}")
            hr_data = garmin_client.get_heart_rates(input_data.date)

            if not hr_data:
                logger.info(f"No heart rate data found for {date}")
                return not_found_response("heart rate data", f"date {date}")

            logger.info(f"Retrieved heart rate data for {date}")
            return success_response(hr_data, message="Heart rate data retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_heart_rates: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving heart rate data: {e}")
            return error_response("internal_error", f"Error retrieving heart rate data: {str(e)}")

    @app.tool()
    async def get_hydration_data(date: str) -> str:
        """
        Get hydration data

        Args:
            date: Date in YYYY-MM-DD format

        Returns:
            JSON string with hydration data or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DateInput(date=date)

            logger.info(f"Fetching hydration data for {date}")
            hydration_data = garmin_client.get_hydration_data(input_data.date)

            if not hydration_data:
                logger.info(f"No hydration data found for {date}")
                return not_found_response("hydration data", f"date {date}")

            logger.info(f"Retrieved hydration data for {date}")
            return success_response(hydration_data, message="Hydration data retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_hydration_data: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving hydration data: {e}")
            return error_response("internal_error", f"Error retrieving hydration data: {str(e)}")

    @app.tool()
    async def get_sleep_data(date: str) -> str:
        """
        Get sleep data

        Args:
            date: Date in YYYY-MM-DD format

        Returns:
            JSON string with sleep data or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DateInput(date=date)

            logger.info(f"Fetching sleep data for {date}")
            sleep_data = garmin_client.get_sleep_data(input_data.date)

            if not sleep_data:
                logger.info(f"No sleep data found for {date}")
                return not_found_response("sleep data", f"date {date}")

            logger.info(f"Retrieved sleep data for {date}")
            return success_response(sleep_data, message="Sleep data retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_sleep_data: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving sleep data: {e}")
            return error_response("internal_error", f"Error retrieving sleep data: {str(e)}")

    @app.tool()
    async def get_stress_data(date: str) -> str:
        """
        Get stress data

        Args:
            date: Date in YYYY-MM-DD format

        Returns:
            JSON string with stress data or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DateInput(date=date)

            logger.info(f"Fetching stress data for {date}")
            stress_data = garmin_client.get_stress_data(input_data.date)

            if not stress_data:
                logger.info(f"No stress data found for {date}")
                return not_found_response("stress data", f"date {date}")

            logger.info(f"Retrieved stress data for {date}")
            return success_response(stress_data, message="Stress data retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_stress_data: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving stress data: {e}")
            return error_response("internal_error", f"Error retrieving stress data: {str(e)}")

    @app.tool()
    async def get_respiration_data(date: str) -> str:
        """
        Get respiration data

        Args:
            date: Date in YYYY-MM-DD format

        Returns:
            JSON string with respiration data or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DateInput(date=date)

            logger.info(f"Fetching respiration data for {date}")
            respiration_data = garmin_client.get_respiration_data(input_data.date)

            if not respiration_data:
                logger.info(f"No respiration data found for {date}")
                return not_found_response("respiration data", f"date {date}")

            logger.info(f"Retrieved respiration data for {date}")
            return success_response(respiration_data, message="Respiration data retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_respiration_data: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving respiration data: {e}")
            return error_response("internal_error", f"Error retrieving respiration data: {str(e)}")

    @app.tool()
    async def get_spo2_data(date: str) -> str:
        """
        Get SpO2 (blood oxygen) data

        Args:
            date: Date in YYYY-MM-DD format

        Returns:
            JSON string with SpO2 data or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DateInput(date=date)

            logger.info(f"Fetching SpO2 data for {date}")
            spo2_data = garmin_client.get_spo2_data(input_data.date)

            if not spo2_data:
                logger.info(f"No SpO2 data found for {date}")
                return not_found_response("SpO2 data", f"date {date}")

            logger.info(f"Retrieved SpO2 data for {date}")
            return success_response(spo2_data, message="SpO2 data retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_spo2_data: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving SpO2 data: {e}")
            return error_response("internal_error", f"Error retrieving SpO2 data: {str(e)}")

    @app.tool()
    async def get_all_day_stress(date: str) -> str:
        """
        Get all-day stress data

        Args:
            date: Date in YYYY-MM-DD format

        Returns:
            JSON string with all-day stress data or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DateInput(date=date)

            logger.info(f"Fetching all-day stress data for {date}")
            stress_data = garmin_client.get_all_day_stress(input_data.date)

            if not stress_data:
                logger.info(f"No all-day stress data found for {date}")
                return not_found_response("all-day stress data", f"date {date}")

            logger.info(f"Retrieved all-day stress data for {date}")
            return success_response(stress_data, message="All-day stress data retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_all_day_stress: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving all-day stress data: {e}")
            return error_response("internal_error", f"Error retrieving all-day stress data: {str(e)}")

    @app.tool()
    async def get_all_day_events(date: str) -> str:
        """
        Get daily wellness events data

        Args:
            date: Date in YYYY-MM-DD format

        Returns:
            JSON string with daily wellness events or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DateInput(date=date)

            logger.info(f"Fetching daily wellness events for {date}")
            events = garmin_client.get_all_day_events(input_data.date)

            if not events:
                logger.info(f"No daily wellness events found for {date}")
                return not_found_response("daily wellness events", f"date {date}")

            logger.info(f"Retrieved daily wellness events for {date}")
            return success_response(events, message="Daily wellness events retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_all_day_events: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving daily wellness events: {e}")
            return error_response("internal_error", f"Error retrieving daily wellness events: {str(e)}")

    return app
