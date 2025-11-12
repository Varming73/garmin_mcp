"""
Pydantic models for input validation and response serialization
"""
from datetime import date, datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, field_validator


class DateInput(BaseModel):
    """Model for single date input"""
    date: str = Field(..., description="Date in YYYY-MM-DD format")

    @field_validator('date')
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        """Validate date format"""
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')


class DateRangeInput(BaseModel):
    """Model for date range input"""
    start_date: str = Field(..., description="Start date in YYYY-MM-DD format")
    end_date: str = Field(..., description="End date in YYYY-MM-DD format")

    @field_validator('start_date', 'end_date')
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        """Validate date format"""
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')

    @field_validator('end_date')
    @classmethod
    def validate_date_order(cls, v: str, info) -> str:
        """Validate that end_date is after start_date"""
        data = info.data
        start_date_str = data.get('start_date')
        if start_date_str:
            start = datetime.strptime(start_date_str, '%Y-%m-%d')
            end = datetime.strptime(v, '%Y-%m-%d')
            if end < start:
                raise ValueError('end_date must be after or equal to start_date')
        return v


class ActivityQueryInput(BaseModel):
    """Model for activity query parameters"""
    start_date: str = Field(..., description="Start date in YYYY-MM-DD format")
    end_date: str = Field(..., description="End date in YYYY-MM-DD format")
    activity_type: str = Field(default="", description="Optional activity type filter")

    @field_validator('start_date', 'end_date')
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        """Validate date format"""
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')


class ActivityIdInput(BaseModel):
    """Model for activity ID input"""
    activity_id: int = Field(..., gt=0, description="Activity ID must be positive")


class ListActivitiesInput(BaseModel):
    """Model for listing activities"""
    limit: int = Field(default=5, gt=0, le=100, description="Number of activities to retrieve (1-100)")


class BloodPressureInput(BaseModel):
    """Model for blood pressure data"""
    systolic: int = Field(..., ge=50, le=300, description="Systolic pressure (50-300)")
    diastolic: int = Field(..., ge=30, le=200, description="Diastolic pressure (30-200)")
    pulse: int = Field(..., ge=30, le=250, description="Pulse rate (30-250)")
    notes: Optional[str] = Field(default=None, max_length=500, description="Optional notes")


class HydrationInput(BaseModel):
    """Model for hydration data"""
    value_in_ml: int = Field(..., gt=0, le=10000, description="Amount in milliliters (1-10000)")
    cdate: str = Field(..., description="Date in YYYY-MM-DD format")
    timestamp: str = Field(..., description="Timestamp in ISO format")

    @field_validator('cdate')
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        """Validate date format"""
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('cdate must be in YYYY-MM-DD format')

    @field_validator('timestamp')
    @classmethod
    def validate_timestamp_format(cls, v: str) -> str:
        """Validate timestamp format"""
        try:
            datetime.fromisoformat(v.replace('Z', '+00:00'))
            return v
        except ValueError:
            raise ValueError('timestamp must be in ISO format (e.g., 2024-01-01T12:00:00.000Z)')


class BodyCompositionInput(BaseModel):
    """Model for body composition data"""
    date: str = Field(..., description="Date in YYYY-MM-DD format")
    weight: float = Field(..., gt=0, le=500, description="Weight in kg (0-500)")
    percent_fat: Optional[float] = Field(default=None, ge=0, le=100)
    percent_hydration: Optional[float] = Field(default=None, ge=0, le=100)
    visceral_fat_mass: Optional[float] = Field(default=None, ge=0)
    bone_mass: Optional[float] = Field(default=None, ge=0)
    muscle_mass: Optional[float] = Field(default=None, ge=0)
    basal_met: Optional[float] = Field(default=None, ge=0)
    active_met: Optional[float] = Field(default=None, ge=0)
    physique_rating: Optional[int] = Field(default=None, ge=1, le=9)
    metabolic_age: Optional[float] = Field(default=None, ge=0, le=150)
    visceral_fat_rating: Optional[int] = Field(default=None, ge=1, le=60)
    bmi: Optional[float] = Field(default=None, ge=0, le=100)

    @field_validator('date')
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        """Validate date format"""
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')


class MCPResponse(BaseModel):
    """Standardized MCP tool response"""
    success: bool = Field(..., description="Whether the operation was successful")
    data: Optional[Any] = Field(default=None, description="Response data")
    error: Optional[Dict[str, str]] = Field(default=None, description="Error information")
    message: Optional[str] = Field(default=None, description="Optional message")
