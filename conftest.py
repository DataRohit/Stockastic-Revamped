# Imports
import pytest

from apps.account.factories import UserFactory


# Function to create user
@pytest.fixture
def user():
    # Create a user and return it
    return UserFactory()
