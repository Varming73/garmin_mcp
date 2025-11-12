"""
Custom exceptions for Garmin MCP Server
"""


class GarminMCPError(Exception):
    """Base exception for all Garmin MCP errors"""

    def __init__(self, message: str, error_code: str = "internal_error") -> None:
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class AuthenticationError(GarminMCPError):
    """Raised when authentication with Garmin Connect fails"""

    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(message, error_code="authentication_error")


class GarminConnectionError(GarminMCPError):
    """Raised when connection to Garmin Connect fails"""

    def __init__(self, message: str = "Connection to Garmin Connect failed") -> None:
        super().__init__(message, error_code="connection_error")


class ValidationError(GarminMCPError):
    """Raised when input validation fails"""

    def __init__(self, message: str) -> None:
        super().__init__(message, error_code="validation_error")


class DataNotFoundError(GarminMCPError):
    """Raised when requested data is not found"""

    def __init__(self, message: str) -> None:
        super().__init__(message, error_code="data_not_found")


class RateLimitError(GarminMCPError):
    """Raised when rate limit is exceeded"""

    def __init__(self, message: str = "Rate limit exceeded") -> None:
        super().__init__(message, error_code="rate_limit_exceeded")


class ConfigurationError(GarminMCPError):
    """Raised when configuration is invalid"""

    def __init__(self, message: str) -> None:
        super().__init__(message, error_code="configuration_error")
