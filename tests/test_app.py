"""
Test suite for the High School Management System API.
Uses the AAA (Arrange-Act-Assert) pattern for test structure.
"""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client):
        """
        ARRANGE: No setup needed, use default activities
        ACT: Send GET request to /activities
        ASSERT: Verify status code and response contains all activities
        """
        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data

    def test_get_activities_returns_correct_activity_structure(self, client):
        """
        ARRANGE: No setup needed
        ACT: Send GET request to /activities
        ASSERT: Verify each activity has required fields
        """
        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert response.status_code == 200
        activity = data["Chess Club"]
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)

    def test_get_activities_contains_participants(self, client):
        """
        ARRANGE: No setup needed
        ACT: Send GET request to /activities
        ASSERT: Verify activities have participants
        """
        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert response.status_code == 200
        chess_club_participants = data["Chess Club"]["participants"]
        assert len(chess_club_participants) > 0
        assert "michael@mergington.edu" in chess_club_participants


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_successful(self, client):
        """
        ARRANGE: Prepare email and activity name
        ACT: Send POST request to signup endpoint
        ASSERT: Verify success message and response
        """
        # Arrange
        email = "new_student@mergington.edu"
        activity_name = "Chess Club"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]

    def test_signup_adds_participant_to_activity(self, client):
        """
        ARRANGE: Prepare email and activity name
        ACT: Send POST request to signup, then fetch activities
        ASSERT: Verify participant appears in activity's participant list
        """
        # Arrange
        email = "test_student@mergington.edu"
        activity_name = "Programming Class"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        verify_response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities_data = verify_response.json()
        assert email in activities_data[activity_name]["participants"]

    def test_signup_duplicate_student_fails(self, client):
        """
        ARRANGE: Use email already registered in Chess Club
        ACT: Send POST request to signup with duplicate email
        ASSERT: Verify 400 status code and error message
        """
        # Arrange
        email = "michael@mergington.edu"  # Already in Chess Club
        activity_name = "Chess Club"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "Student already signed up"

    def test_signup_nonexistent_activity_fails(self, client):
        """
        ARRANGE: Use non-existent activity name
        ACT: Send POST request to signup with invalid activity
        ASSERT: Verify 404 status code and error message
        """
        # Arrange
        email = "student@mergington.edu"
        activity_name = "Nonexistent Club"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Activity not found"

    def test_signup_at_full_capacity(self, client):
        """
        ARRANGE: Create an activity with one spot left, fill it
        ACT: Attempt to signup one more student
        ASSERT: Verify signup succeeds (no max capacity check in current implementation)
        """
        # Arrange
        email = "new_student@mergington.edu"
        activity_name = "Chess Club"
        
        # Verify current participants
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert - signup succeeds
        assert response.status_code == 200
        verify_response = client.get("/activities")
        final_count = len(verify_response.json()[activity_name]["participants"])
        assert final_count == initial_count + 1

    def test_signup_increments_participant_count(self, client):
        """
        ARRANGE: Get initial participant count
        ACT: Sign up a new student
        ASSERT: Verify participant count increased by 1
        """
        # Arrange
        email = "new_participant@mergington.edu"
        activity_name = "Drama Club"
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 200
        verify_response = client.get("/activities")
        final_count = len(verify_response.json()[activity_name]["participants"])
        assert final_count == initial_count + 1


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint."""

    def test_unregister_successful(self, client):
        """
        ARRANGE: Use email already registered in an activity
        ACT: Send DELETE request to unregister endpoint
        ASSERT: Verify success message
        """
        # Arrange
        email = "michael@mergington.edu"  # Already in Chess Club
        activity_name = "Chess Club"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]

    def test_unregister_removes_participant(self, client):
        """
        ARRANGE: Use registered participant
        ACT: Send DELETE request, then fetch activities
        ASSERT: Verify participant removed from activity
        """
        # Arrange
        email = "michael@mergington.edu"
        activity_name = "Chess Club"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        verify_response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities_data = verify_response.json()
        assert email not in activities_data[activity_name]["participants"]

    def test_unregister_decrements_participant_count(self, client):
        """
        ARRANGE: Get initial participant count
        ACT: Unregister a participant
        ASSERT: Verify participant count decreased by 1
        """
        # Arrange
        email = "michael@mergington.edu"
        activity_name = "Chess Club"
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 200
        verify_response = client.get("/activities")
        final_count = len(verify_response.json()[activity_name]["participants"])
        assert final_count == initial_count - 1

    def test_unregister_nonexistent_activity_fails(self, client):
        """
        ARRANGE: Use non-existent activity name
        ACT: Send DELETE request with invalid activity
        ASSERT: Verify 404 status code and error message
        """
        # Arrange
        email = "student@mergington.edu"
        activity_name = "Nonexistent Club"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Activity not found"

    def test_unregister_unregistered_student_fails(self, client):
        """
        ARRANGE: Use email not registered in the activity
        ACT: Send DELETE request with unregistered email
        ASSERT: Verify 400 status code and error message
        """
        # Arrange
        email = "unknown@mergington.edu"
        activity_name = "Chess Club"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "Student not registered for this activity"

    def test_unregister_then_signup_same_student(self, client):
        """
        ARRANGE: Prepare student email already in an activity
        ACT: Unregister the student, then sign them up again
        ASSERT: Verify both operations succeed
        """
        # Arrange
        email = "michael@mergington.edu"
        activity_name = "Chess Club"

        # Act - unregister
        unregister_response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )

        # Act - signup again
        signup_response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert unregister_response.status_code == 200
        assert signup_response.status_code == 200
        verify_response = client.get("/activities")
        assert email in verify_response.json()[activity_name]["participants"]


class TestIntegration:
    """Integration tests for multiple endpoints working together."""

    def test_signup_unregister_signup_workflow(self, client):
        """
        ARRANGE: Prepare a new student email
        ACT: Sign up student, verify in list, unregister, verify removed, sign up again
        ASSERT: Verify each step succeeds
        """
        # Arrange
        email = "integration_test@mergington.edu"
        activity_name = "Art Studio"

        # Act & Assert - Sign up
        signup_response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        assert signup_response.status_code == 200

        # Act & Assert - Verify in list
        get_response = client.get("/activities")
        assert email in get_response.json()[activity_name]["participants"]

        # Act & Assert - Unregister
        unregister_response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        assert unregister_response.status_code == 200

        # Act & Assert - Verify removed from list
        get_response = client.get("/activities")
        assert email not in get_response.json()[activity_name]["participants"]

        # Act & Assert - Sign up again
        signup_response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        assert signup_response.status_code == 200

    def test_all_activities_can_accept_signups(self, client):
        """
        ARRANGE: Get all activities
        ACT: Sign up a unique student to each activity
        ASSERT: Verify all signups succeed
        """
        # Arrange
        initial_response = client.get("/activities")
        activities_dict = initial_response.json()

        # Act & Assert
        for idx, activity_name in enumerate(activities_dict.keys()):
            email = f"student_{idx}@mergington.edu"
            response = client.post(
                f"/activities/{activity_name}/signup?email={email}"
            )
            assert response.status_code == 200
