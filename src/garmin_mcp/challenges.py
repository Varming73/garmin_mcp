"""
Challenges and badges functions for Garmin Connect MCP Server
"""
from typing import Optional

from mcp.server.fastmcp import FastMCP
from garminconnect import Garmin
from pydantic import ValidationError

from garmin_mcp.logging_config import get_logger
from garmin_mcp.response import success_response, error_response, not_found_response
from garmin_mcp.models import (
    DateRangeInput,
    GoalTypeInput,
    ChallengesPaginationInput,
    BadgeChallengesPaginationInput
)

logger = get_logger(__name__)

# The garmin_client will be set by the main file
garmin_client: Optional[Garmin] = None


def configure(client: Garmin) -> None:
    """Configure the module with the Garmin client instance"""
    global garmin_client
    garmin_client = client
    logger.info("Challenges module configured")


def register_tools(app: FastMCP) -> FastMCP:
    """Register all challenges-related tools with the MCP server app"""

    @app.tool()
    async def get_goals(goal_type: str = "active") -> str:
        """
        Get Garmin Connect goals (active, future, or past)

        Args:
            goal_type: Type of goals to retrieve ('active', 'future', or 'past', default: 'active')

        Returns:
            JSON string with goals or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = GoalTypeInput(goal_type=goal_type)

            logger.info(f"Fetching {goal_type} goals")
            goals = garmin_client.get_goals(input_data.goal_type)

            if not goals:
                logger.info(f"No {goal_type} goals found")
                return not_found_response(f"{goal_type} goals", "user account")

            logger.info(f"Retrieved {goal_type} goals")
            return success_response(goals, message=f"{goal_type.capitalize()} goals retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_goals: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving {goal_type} goals: {e}")
            return error_response("internal_error", f"Error retrieving {goal_type} goals: {str(e)}")

    @app.tool()
    async def get_personal_record() -> str:
        """
        Get personal records for user

        Returns:
            JSON string with personal records or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            logger.info("Fetching personal records")
            records = garmin_client.get_personal_record()

            if not records:
                logger.info("No personal records found")
                return not_found_response("personal records", "user account")

            logger.info("Retrieved personal records")
            return success_response(records, message="Personal records retrieved")

        except Exception as e:
            logger.exception(f"Error retrieving personal records: {e}")
            return error_response("internal_error", f"Error retrieving personal records: {str(e)}")

    @app.tool()
    async def get_earned_badges() -> str:
        """
        Get earned badges for user

        Returns:
            JSON string with earned badges or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            logger.info("Fetching earned badges")
            badges = garmin_client.get_earned_badges()

            if not badges:
                logger.info("No earned badges found")
                return not_found_response("earned badges", "user account")

            logger.info("Retrieved earned badges")
            return success_response(badges, message="Earned badges retrieved")

        except Exception as e:
            logger.exception(f"Error retrieving earned badges: {e}")
            return error_response("internal_error", f"Error retrieving earned badges: {str(e)}")

    @app.tool()
    async def get_adhoc_challenges(start: int = 0, limit: int = 100) -> str:
        """
        Get adhoc challenges data

        Args:
            start: Starting index for challenges retrieval (default: 0)
            limit: Maximum number of challenges to retrieve (1-100, default: 100)

        Returns:
            JSON string with adhoc challenges or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = ChallengesPaginationInput(start=start, limit=limit)

            logger.info(f"Fetching adhoc challenges (start={start}, limit={limit})")
            challenges = garmin_client.get_adhoc_challenges(input_data.start, input_data.limit)

            if not challenges:
                logger.info("No adhoc challenges found")
                return not_found_response("adhoc challenges", "user account")

            logger.info("Retrieved adhoc challenges")
            return success_response(challenges, message="Adhoc challenges retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_adhoc_challenges: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving adhoc challenges: {e}")
            return error_response("internal_error", f"Error retrieving adhoc challenges: {str(e)}")

    @app.tool()
    async def get_available_badge_challenges(start: int = 1, limit: int = 100) -> str:
        """
        Get available badge challenges data

        Args:
            start: Starting index for challenges retrieval (starts at 1, default: 1)
            limit: Maximum number of challenges to retrieve (1-100, default: 100)

        Returns:
            JSON string with available badge challenges or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = BadgeChallengesPaginationInput(start=start, limit=limit)

            logger.info(f"Fetching available badge challenges (start={start}, limit={limit})")
            challenges = garmin_client.get_available_badge_challenges(input_data.start, input_data.limit)

            if not challenges:
                logger.info("No available badge challenges found")
                return not_found_response("available badge challenges", "user account")

            logger.info("Retrieved available badge challenges")
            return success_response(challenges, message="Available badge challenges retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_available_badge_challenges: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving available badge challenges: {e}")
            return error_response("internal_error", f"Error retrieving available badge challenges: {str(e)}")

    @app.tool()
    async def get_badge_challenges(start: int = 1, limit: int = 100) -> str:
        """
        Get badge challenges data

        Args:
            start: Starting index for challenges retrieval (starts at 1, default: 1)
            limit: Maximum number of challenges to retrieve (1-100, default: 100)

        Returns:
            JSON string with badge challenges or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = BadgeChallengesPaginationInput(start=start, limit=limit)

            logger.info(f"Fetching badge challenges (start={start}, limit={limit})")
            challenges = garmin_client.get_badge_challenges(input_data.start, input_data.limit)

            if not challenges:
                logger.info("No badge challenges found")
                return not_found_response("badge challenges", "user account")

            logger.info("Retrieved badge challenges")
            return success_response(challenges, message="Badge challenges retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_badge_challenges: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving badge challenges: {e}")
            return error_response("internal_error", f"Error retrieving badge challenges: {str(e)}")

    @app.tool()
    async def get_non_completed_badge_challenges(start: int = 1, limit: int = 100) -> str:
        """
        Get non-completed badge challenges data

        Args:
            start: Starting index for challenges retrieval (starts at 1, default: 1)
            limit: Maximum number of challenges to retrieve (1-100, default: 100)

        Returns:
            JSON string with non-completed badge challenges or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = BadgeChallengesPaginationInput(start=start, limit=limit)

            logger.info(f"Fetching non-completed badge challenges (start={start}, limit={limit})")
            challenges = garmin_client.get_non_completed_badge_challenges(input_data.start, input_data.limit)

            if not challenges:
                logger.info("No non-completed badge challenges found")
                return not_found_response("non-completed badge challenges", "user account")

            logger.info("Retrieved non-completed badge challenges")
            return success_response(challenges, message="Non-completed badge challenges retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_non_completed_badge_challenges: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving non-completed badge challenges: {e}")
            return error_response("internal_error", f"Error retrieving non-completed badge challenges: {str(e)}")

    @app.tool()
    async def get_race_predictions() -> str:
        """
        Get race predictions for user

        Returns:
            JSON string with race predictions or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            logger.info("Fetching race predictions")
            predictions = garmin_client.get_race_predictions()

            if not predictions:
                logger.info("No race predictions found")
                return not_found_response("race predictions", "user account")

            logger.info("Retrieved race predictions")
            return success_response(predictions, message="Race predictions retrieved")

        except Exception as e:
            logger.exception(f"Error retrieving race predictions: {e}")
            return error_response("internal_error", f"Error retrieving race predictions: {str(e)}")

    @app.tool()
    async def get_inprogress_virtual_challenges(start_date: str, end_date: str) -> str:
        """
        Get in-progress virtual challenges/expeditions between dates

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format

        Returns:
            JSON string with in-progress virtual challenges or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = DateRangeInput(start_date=start_date, end_date=end_date)

            logger.info(f"Fetching in-progress virtual challenges from {start_date} to {end_date}")
            challenges = garmin_client.get_inprogress_virtual_challenges(
                input_data.start_date, input_data.end_date
            )

            if not challenges:
                logger.info(f"No in-progress virtual challenges found between {start_date} and {end_date}")
                return not_found_response(
                    "in-progress virtual challenges",
                    f"date range {start_date} to {end_date}"
                )

            logger.info("Retrieved in-progress virtual challenges")
            return success_response(challenges, message="In-progress virtual challenges retrieved")

        except ValidationError as e:
            logger.warning(f"Validation error in get_inprogress_virtual_challenges: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error retrieving in-progress virtual challenges: {e}")
            return error_response("internal_error", f"Error retrieving in-progress virtual challenges: {str(e)}")

    return app
