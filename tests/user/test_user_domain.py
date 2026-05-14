import pytest


class TestUserDomain:
    def test_creates_valid_user(self, user_factory):
        user = user_factory()

        assert user.name == "Mario Rossi"
        assert user.email == "user@test.com"

    def test_rejects_invalid_values(self, user_factory):
        with pytest.raises(ValueError, match="Name cannot be empty"):
            user_factory(name="")

        with pytest.raises(ValueError, match="Email cannot be empty"):
            user_factory(email="")

        with pytest.raises(ValueError, match="Password cannot be empty"):
            user_factory(hashed_password="")
