# Imports
import pytest
from django.urls import reverse

from apps.account.factories import UserFactory


# Function to test logout view with a logged in user
@pytest.mark.django_db
def test_logout_view(client):
    # Create a user
    user = UserFactory()

    # Log the user in
    client.force_login(user)

    # Get the response
    response = client.get(reverse("account:logout"))

    # Check the status code
    assert response.status_code == 302

    # Check the location
    assert response.url == reverse("account:login")

    # Follow the redirect url
    response = client.get(response.url)

    # Check the user is logged out
    assert not response.context["request"].user.is_authenticated

    # Assert the error message
    assert b"You have been logged out!" in response.content


# Function to test logout view with a logged out user
@pytest.mark.django_db
def test_logout_view_logged_out(client):
    # Get the response
    response = client.get(reverse("account:logout"))

    # Check the status code
    assert response.status_code == 302

    # Check the location
    assert response.url == reverse("account:login")

    # Follow the redirect url
    response = client.get(response.url)

    # Assert the error message
    assert b"You are not logged in!" in response.content
