# Imports
import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


# Function to test the equity top gainers view when the user is unauthenticated
@pytest.mark.django_db
def test_equity_top_gainers_view_unauthenticated(client):
    # Get the equity top gainers page
    response = client.get(reverse("stock:equityTopGainers"))

    # Assert the response status code
    assert response.status_code == 302

    # Follow the redirect url
    response = client.get(response.url)

    # Assert the response status code
    assert response.status_code == 200

    # Assert the correct template is used
    assertTemplateUsed(response, "account/login.html")

    # Assert that the user is authenticated and is the correct user
    assert not response.context["user"].is_authenticated

    # Assert that the context contains the user (should be anonymous)
    assert "user" in response.context
    assert response.context["user"].is_anonymous


# Function to test the equity top gainers view when the user is authenticated
@pytest.mark.django_db
def test_equity_top_gainers_view_authenticated(client, user):
    # Authenticate the user
    client.force_login(user)

    # Get the equity top gainers page
    response = client.get(reverse("stock:equityTopGainers"))

    # Assert the response status code
    assert response.status_code == 200

    # Assert the correct template is used
    assertTemplateUsed(response, "stock/top_gainers.html")

    # Assert that the context contains the user (should be the authenticated user)
    assert "user" in response.context
    assert response.context["request"].user.is_authenticated
    assert response.context["user"] == user