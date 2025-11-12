"""
Modular MCP Server for Garmin Connect Data
"""
import os
from typing import Optional, Tuple

import requests
from mcp.server.fastmcp import FastMCP

from garth.exc import GarthHTTPError
from garminconnect import Garmin, GarminConnectAuthenticationError

# Import new utilities
from garmin_mcp.logging_config import setup_logging, get_logger
from garmin_mcp.exceptions import AuthenticationError, ConfigurationError

# Import all modules
from garmin_mcp import activity_management
from garmin_mcp import health_wellness
from garmin_mcp import user_profile
from garmin_mcp import devices
from garmin_mcp import gear_management
from garmin_mcp import weight_management
from garmin_mcp import challenges
from garmin_mcp import training
from garmin_mcp import workouts
from garmin_mcp import data_management
from garmin_mcp import womens_health

# Setup logging
logger = get_logger(__name__)


def get_mfa() -> str:
    """Get MFA code from user input"""
    print("\nGarmin Connect MFA required. Please check your email/phone for the code.")
    return input("Enter MFA code: ")


def get_credentials() -> Tuple[Optional[str], Optional[str]]:
    """
    Get Garmin credentials from environment variables or files

    Returns:
        Tuple of (email, password)

    Raises:
        ConfigurationError: If configuration is invalid
    """
    # Get email from environment
    email = os.environ.get("GARMIN_EMAIL")
    email_file_path = os.environ.get("GARMIN_EMAIL_FILE")

    if email and email_file_path:
        raise ConfigurationError(
            "Must only provide one of GARMIN_EMAIL and GARMIN_EMAIL_FILE, got both"
        )
    elif email_file_path:
        try:
            with open(email_file_path, "r") as f:
                email = f.read().rstrip()
                if not email:
                    raise ConfigurationError(f"Email file {email_file_path} is empty")
        except FileNotFoundError:
            raise ConfigurationError(f"Email file not found: {email_file_path}")
        except Exception as e:
            raise ConfigurationError(f"Error reading email file: {e}")

    # Get password from environment
    password = os.environ.get("GARMIN_PASSWORD")
    password_file_path = os.environ.get("GARMIN_PASSWORD_FILE")

    if password and password_file_path:
        raise ConfigurationError(
            "Must only provide one of GARMIN_PASSWORD and GARMIN_PASSWORD_FILE, got both"
        )
    elif password_file_path:
        try:
            with open(password_file_path, "r") as f:
                password = f.read().rstrip()
                if not password:
                    raise ConfigurationError(f"Password file {password_file_path} is empty")
        except FileNotFoundError:
            raise ConfigurationError(f"Password file not found: {password_file_path}")
        except Exception as e:
            raise ConfigurationError(f"Error reading password file: {e}")

    # Validate credentials
    if not email:
        raise ConfigurationError(
            "GARMIN_EMAIL or GARMIN_EMAIL_FILE environment variable must be set"
        )
    if not password:
        raise ConfigurationError(
            "GARMIN_PASSWORD or GARMIN_PASSWORD_FILE environment variable must be set"
        )

    return email, password


def init_api(email: str, password: str) -> Optional[Garmin]:
    """
    Initialize Garmin API with credentials

    Args:
        email: Garmin Connect email
        password: Garmin Connect password

    Returns:
        Initialized Garmin client or None if initialization fails
    """
    tokenstore = os.getenv("GARMINTOKENS") or "~/.garminconnect"
    tokenstore_base64 = os.getenv("GARMINTOKENS_BASE64") or "~/.garminconnect_base64"

    try:
        # Using Oauth1 and OAuth2 token files from directory
        logger.info(f"Attempting to login using token data from '{tokenstore}'")

        garmin = Garmin()
        garmin.login(tokenstore)
        logger.info("Successfully logged in using stored tokens")

    except (FileNotFoundError, GarthHTTPError, GarminConnectAuthenticationError) as e:
        # Session is expired or tokens don't exist. Need fresh login
        logger.info(f"Stored tokens not valid ({type(e).__name__}), performing fresh login")
        logger.info(
            f"Tokens will be stored in '{tokenstore}' for future use"
        )

        try:
            garmin = Garmin(
                email=email, password=password, is_cn=False, prompt_mfa=get_mfa
            )
            garmin.login()

            # Save Oauth1 and Oauth2 token files to directory for next login
            garmin.garth.dump(tokenstore)
            logger.info(f"OAuth tokens stored in '{tokenstore}' directory")

            # Also save as base64 encoded string (alternative method)
            token_base64 = garmin.garth.dumps()
            dir_path = os.path.expanduser(tokenstore_base64)
            with open(dir_path, "w") as token_file:
                token_file.write(token_base64)
            logger.info(f"OAuth tokens also saved as base64 to '{dir_path}'")

        except (
            FileNotFoundError,
            GarthHTTPError,
            GarminConnectAuthenticationError,
            requests.exceptions.HTTPError,
        ) as err:
            logger.error(f"Authentication failed: {err}", exc_info=True)
            return None

    return garmin


def main() -> None:
    """Initialize the MCP server and register all tools"""
    # Setup logging
    log_level = os.getenv("LOG_LEVEL", "INFO")
    log_file = os.getenv("LOG_FILE")
    setup_logging(level=log_level, log_file=log_file)

    logger.info("Starting Garmin MCP Server")

    try:
        # Get credentials
        email, password = get_credentials()

        # Initialize Garmin client
        garmin_client = init_api(email, password)
        if not garmin_client:
            logger.error("Failed to initialize Garmin Connect client. Exiting.")
            return

        logger.info("Garmin Connect client initialized successfully")

        # Configure all modules with the Garmin client
        activity_management.configure(garmin_client)
        health_wellness.configure(garmin_client)
        user_profile.configure(garmin_client)
        devices.configure(garmin_client)
        gear_management.configure(garmin_client)
        weight_management.configure(garmin_client)
        challenges.configure(garmin_client)
        training.configure(garmin_client)
        workouts.configure(garmin_client)
        data_management.configure(garmin_client)
        womens_health.configure(garmin_client)

        # Create the MCP app
        app = FastMCP("Garmin Connect MCP Server")

        # Register tools from all modules
        app = activity_management.register_tools(app)
        app = health_wellness.register_tools(app)
        app = user_profile.register_tools(app)
        app = devices.register_tools(app)
        app = gear_management.register_tools(app)
        app = weight_management.register_tools(app)
        app = challenges.register_tools(app)
        app = training.register_tools(app)
        app = workouts.register_tools(app)
        app = data_management.register_tools(app)
        app = womens_health.register_tools(app)

        # Add activity listing tool directly to the app
        @app.tool()
        async def list_activities(limit: int = 5) -> str:
            """
            List recent Garmin activities

            Args:
                limit: Number of activities to retrieve (default: 5)

            Returns:
                JSON string with activity list
            """
            from garmin_mcp.response import success_response, error_response
            from garmin_mcp.models import ListActivitiesInput
            from pydantic import ValidationError

            try:
                # Validate input
                input_data = ListActivitiesInput(limit=limit)

                activities = garmin_client.get_activities(0, input_data.limit)

                if not activities:
                    return success_response([], message="No activities found")

                result_list = []
                for activity in activities:
                    result_list.append({
                        "name": activity.get('activityName', 'Unknown'),
                        "type": activity.get('activityType', {}).get('typeKey', 'Unknown'),
                        "date": activity.get('startTimeLocal', 'Unknown'),
                        "id": activity.get('activityId', 'Unknown')
                    })

                return success_response(
                    result_list,
                    message=f"Retrieved {len(result_list)} activities"
                )
            except ValidationError as e:
                logger.warning(f"Validation error in list_activities: {e}")
                return error_response("validation_error", str(e))
            except Exception as e:
                logger.exception(f"Error retrieving activities: {e}")
                return error_response("internal_error", f"Error retrieving activities: {str(e)}")

        logger.info("All tools registered successfully")

        # Run the MCP server
        logger.info("Starting MCP server...")
        app.run()

    except ConfigurationError as e:
        logger.error(f"Configuration error: {e}")
        print(f"Configuration error: {e}")
        return
    except Exception as e:
        logger.exception(f"Unexpected error during startup: {e}")
        print(f"Unexpected error: {e}")
        return


if __name__ == "__main__":
    main()
