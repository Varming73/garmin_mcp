"""
Response builders for standardized MCP tool responses
"""
import json
from typing import Any, Dict, Optional
from garmin_mcp.exceptions import GarminMCPError


def success_response(data: Any, message: Optional[str] = None) -> str:
    """
    Build a successful response

    Args:
        data: Response data (will be JSON serialized)
        message: Optional success message

    Returns:
        JSON string of standardized response
    """
    response = {
        "success": True,
        "data": data,
        "error": None
    }
    if message:
        response["message"] = message

    return json.dumps(response, indent=2, default=str)


def error_response(
    error_code: str,
    message: str,
    details: Optional[Dict[str, Any]] = None
) -> str:
    """
    Build an error response

    Args:
        error_code: Error code identifier
        message: Human-readable error message
        details: Optional additional error details

    Returns:
        JSON string of standardized error response
    """
    error_data = {
        "code": error_code,
        "message": message
    }
    if details:
        error_data["details"] = details

    response = {
        "success": False,
        "data": None,
        "error": error_data
    }

    return json.dumps(response, indent=2, default=str)


def exception_to_response(exc: Exception) -> str:
    """
    Convert an exception to a standardized error response

    Args:
        exc: Exception instance

    Returns:
        JSON string of error response
    """
    if isinstance(exc, GarminMCPError):
        return error_response(
            error_code=exc.error_code,
            message=exc.message
        )
    else:
        # Generic exception
        return error_response(
            error_code="internal_error",
            message=str(exc)
        )


def not_found_response(resource: str, identifier: str) -> str:
    """
    Build a not found response

    Args:
        resource: Type of resource (e.g., "activity", "health data")
        identifier: Identifier that wasn't found

    Returns:
        JSON string of not found response
    """
    return error_response(
        error_code="data_not_found",
        message=f"No {resource} found for {identifier}"
    )
