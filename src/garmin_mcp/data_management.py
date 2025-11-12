"""
Data management functions for Garmin Connect MCP Server
"""
from typing import Optional

from mcp.server.fastmcp import FastMCP
from garminconnect import Garmin
from pydantic import ValidationError

from garmin_mcp.logging_config import get_logger
from garmin_mcp.response import success_response, error_response
from garmin_mcp.models import BodyCompositionInput, BloodPressureInput, HydrationInput

logger = get_logger(__name__)

# The garmin_client will be set by the main file
garmin_client: Optional[Garmin] = None


def configure(client: Garmin) -> None:
    """Configure the module with the Garmin client instance"""
    global garmin_client
    garmin_client = client
    logger.info("Data management module configured")


def register_tools(app: FastMCP) -> FastMCP:
    """Register all data management tools with the MCP server app"""

    @app.tool()
    async def add_body_composition(
        date: str,
        weight: float,
        percent_fat: Optional[float] = None,
        percent_hydration: Optional[float] = None,
        visceral_fat_mass: Optional[float] = None,
        bone_mass: Optional[float] = None,
        muscle_mass: Optional[float] = None,
        basal_met: Optional[float] = None,
        active_met: Optional[float] = None,
        physique_rating: Optional[int] = None,
        metabolic_age: Optional[float] = None,
        visceral_fat_rating: Optional[int] = None,
        bmi: Optional[float] = None
    ) -> str:
        """
        Add body composition data

        Args:
            date: Date in YYYY-MM-DD format
            weight: Weight in kg (must be positive, up to 500)
            percent_fat: Body fat percentage (0-100)
            percent_hydration: Hydration percentage (0-100)
            visceral_fat_mass: Visceral fat mass (0 or greater)
            bone_mass: Bone mass (0 or greater)
            muscle_mass: Muscle mass (0 or greater)
            basal_met: Basal metabolic rate (0 or greater)
            active_met: Active metabolic rate (0 or greater)
            physique_rating: Physique rating (1-9)
            metabolic_age: Metabolic age (0-150)
            visceral_fat_rating: Visceral fat rating (1-60)
            bmi: Body Mass Index (0-100)

        Returns:
            JSON string with result or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = BodyCompositionInput(
                date=date,
                weight=weight,
                percent_fat=percent_fat,
                percent_hydration=percent_hydration,
                visceral_fat_mass=visceral_fat_mass,
                bone_mass=bone_mass,
                muscle_mass=muscle_mass,
                basal_met=basal_met,
                active_met=active_met,
                physique_rating=physique_rating,
                metabolic_age=metabolic_age,
                visceral_fat_rating=visceral_fat_rating,
                bmi=bmi
            )

            logger.info(f"Adding body composition data for {date}")
            result = garmin_client.add_body_composition(
                input_data.date,
                weight=input_data.weight,
                percent_fat=input_data.percent_fat,
                percent_hydration=input_data.percent_hydration,
                visceral_fat_mass=input_data.visceral_fat_mass,
                bone_mass=input_data.bone_mass,
                muscle_mass=input_data.muscle_mass,
                basal_met=input_data.basal_met,
                active_met=input_data.active_met,
                physique_rating=input_data.physique_rating,
                metabolic_age=input_data.metabolic_age,
                visceral_fat_rating=input_data.visceral_fat_rating,
                bmi=input_data.bmi
            )

            logger.info(f"Successfully added body composition data for {date}")
            return success_response(result, message="Body composition data added")

        except ValidationError as e:
            logger.warning(f"Validation error in add_body_composition: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error adding body composition data: {e}")
            return error_response("internal_error", f"Error adding body composition data: {str(e)}")

    @app.tool()
    async def set_blood_pressure(
        systolic: int,
        diastolic: int,
        pulse: int,
        notes: Optional[str] = None
    ) -> str:
        """
        Set blood pressure values

        Args:
            systolic: Systolic pressure (top number, 50-300)
            diastolic: Diastolic pressure (bottom number, 30-200)
            pulse: Pulse rate (30-250)
            notes: Optional notes (max 500 characters)

        Returns:
            JSON string with result or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = BloodPressureInput(
                systolic=systolic,
                diastolic=diastolic,
                pulse=pulse,
                notes=notes
            )

            logger.info(f"Setting blood pressure: {systolic}/{diastolic}, pulse: {pulse}")
            result = garmin_client.set_blood_pressure(
                input_data.systolic,
                input_data.diastolic,
                input_data.pulse,
                notes=input_data.notes
            )

            logger.info("Successfully set blood pressure values")
            return success_response(result, message="Blood pressure values set")

        except ValidationError as e:
            logger.warning(f"Validation error in set_blood_pressure: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error setting blood pressure values: {e}")
            return error_response("internal_error", f"Error setting blood pressure values: {str(e)}")

    @app.tool()
    async def add_hydration_data(
        value_in_ml: int,
        cdate: str,
        timestamp: str
    ) -> str:
        """
        Add hydration data

        Args:
            value_in_ml: Amount of liquid in milliliters (1-10000)
            cdate: Date in YYYY-MM-DD format
            timestamp: Timestamp in ISO format (e.g., 2024-01-01T12:00:00.000Z)

        Returns:
            JSON string with result or error
        """
        try:
            if garmin_client is None:
                logger.error("Garmin client not initialized")
                return error_response("not_initialized", "Garmin client not initialized")

            # Validate input
            input_data = HydrationInput(
                value_in_ml=value_in_ml,
                cdate=cdate,
                timestamp=timestamp
            )

            logger.info(f"Adding hydration data: {value_in_ml}ml on {cdate}")
            result = garmin_client.add_hydration_data(
                value_in_ml=input_data.value_in_ml,
                cdate=input_data.cdate,
                timestamp=input_data.timestamp
            )

            logger.info("Successfully added hydration data")
            return success_response(result, message="Hydration data added")

        except ValidationError as e:
            logger.warning(f"Validation error in add_hydration_data: {e}")
            return error_response("validation_error", str(e))
        except Exception as e:
            logger.exception(f"Error adding hydration data: {e}")
            return error_response("internal_error", f"Error adding hydration data: {str(e)}")

    return app
