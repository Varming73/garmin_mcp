"""
Pytest configuration and fixtures for Garmin MCP tests
"""
import pytest
from unittest.mock import Mock, MagicMock
from garminconnect import Garmin


@pytest.fixture
def mock_garmin_client():
    """
    Create a mock Garmin client for testing

    Returns:
        Mock Garmin client instance
    """
    client = Mock(spec=Garmin)

    # Mock common methods
    client.get_activities = MagicMock(return_value=[
        {
            "activityId": 12345,
            "activityName": "Morning Run",
            "activityType": {"typeKey": "running"},
            "startTimeLocal": "2024-01-15 07:00:00"
        }
    ])

    client.get_stats = MagicMock(return_value={
        "totalSteps": 10000,
        "totalDistanceMeters": 8000,
        "activeKilocalories": 500,
        "floorsAscended": 10
    })

    client.get_sleep_data = MagicMock(return_value={
        "dailySleepDTO": {
            "sleepScoreTotal": 85,
            "sleepTimeSeconds": 28800
        }
    })

    return client


@pytest.fixture
def sample_activity_data():
    """
    Sample activity data for testing

    Returns:
        Dict with sample activity data
    """
    return {
        "activityId": 12345,
        "activityName": "Morning Run",
        "activityType": {"typeKey": "running"},
        "startTimeLocal": "2024-01-15 07:00:00",
        "distance": 5000,
        "duration": 1800,
        "averageHR": 145
    }


@pytest.fixture
def sample_health_data():
    """
    Sample health data for testing

    Returns:
        Dict with sample health data
    """
    return {
        "totalSteps": 10000,
        "totalDistanceMeters": 8000,
        "activeKilocalories": 500,
        "floorsAscended": 10,
        "restingHeartRate": 58
    }
