"""Sample application for MINIMAL scenario testing."""


class UserService:
    """Service for user operations."""

    def get_user(self, user_id: int) -> dict:
        """Get user by ID."""
        return {"id": user_id, "name": "Test User"}

    def create_user(self, name: str) -> dict:
        """Create a new user."""
        return {"id": 1, "name": name}
