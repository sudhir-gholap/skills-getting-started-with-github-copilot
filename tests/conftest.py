"""
Pytest configuration and fixtures for the High School Management System API tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient for API testing."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Reset activities to a clean state before each test.
    This ensures test isolation and prevents test interference.
    """
    # Store original state
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Train for competitive matches and improve teamwork",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["nina@mergington.edu", "leo@mergington.edu"]
        },
        "Basketball Club": {
            "description": "Practice shooting, dribbling, and scrimmage games",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 14,
            "participants": ["alex@mergington.edu", "maya@mergington.edu"]
        },
        "Drama Club": {
            "description": "Explore acting, stagecraft, and dramatic performance",
            "schedule": "Wednesdays, 5:00 PM - 6:30 PM",
            "max_participants": 20,
            "participants": ["sara@mergington.edu", "ethan@mergington.edu"]
        },
        "Art Studio": {
            "description": "Create paintings, drawings, and mixed media projects",
            "schedule": "Tuesdays and Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["zoe@mergington.edu", "liam@mergington.edu"]
        },
        "Science Olympiad": {
            "description": "Prepare for science competitions with hands-on challenges",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["oliver@mergington.edu", "chloe@mergington.edu"]
        },
        "Debate Team": {
            "description": "Build public speaking and argumentation skills",
            "schedule": "Mondays and Wednesdays, 5:00 PM - 6:30 PM",
            "max_participants": 14,
            "participants": ["mia@mergington.edu", "noah@mergington.edu"]
        }
    }

    yield

    # Reset to original state after test
    activities.clear()
    activities.update(original_activities)
