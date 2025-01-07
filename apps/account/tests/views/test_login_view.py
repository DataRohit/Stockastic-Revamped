# Imports
import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from apps.account.factories import UserFactory


# Function to test login view
@pytest.mark.django_db
def test_login_view(client):
    # Get the login page
    response = client.get(reverse("account:login"))

    # Assert the response status code
    assert response.status_code == 200

    # Check if the template is correct
    assertTemplateUsed(response, "account/login.html")


# Function to test login view valid data
@pytest.mark.django_db
def test_login_view_valid_data(client):
    # Create a user
    user = UserFactory(password="secure@password")

    # Post the login data
    response = client.post(
        reverse("account:login"), {"email": user.email, "password": "secure@password"}
    )

    # Assert the response status code
    assert response.status_code == 302

    # Check the response URL
    assert response.url == reverse("core:explore")

    # Follow the redirect url
    response = client.get(response.url)

    # Assert that the context contains the user (should be the authenticated user)
    assert "user" in response.context
    assert response.context["request"].user.is_authenticated
    assert response.context["user"] == user


# Function to test login view with empty email
@pytest.mark.django_db
def test_login_view_empty_email(client):
    # Post the login data
    response = client.post(
        reverse("account:login"), {"email": "", "password": "secure@password"}
    )

    # Assert the response status code
    assert response.status_code == 200

    # Check if the template is correct
    assertTemplateUsed(response, "account/login.html")

    # Assert error message response content
    assert b"Email: This field is required." in response.content


# Function to test login view with empty password
@pytest.mark.django_db
def test_login_view_empty_password(client):
    # Create a user
    user = UserFactory(password="secure@password")

    # Post the login data
    response = client.post(
        reverse("account:login"), {"email": user.email, "password": ""}
    )

    # Assert the response status code
    assert response.status_code == 200

    # Check if the template is correct
    assertTemplateUsed(response, "account/login.html")

    # Assert error message response content
    assert b"Password: This field is required." in response.content


# Function to test login view with invalid email
@pytest.mark.django_db
def test_login_view_invalid_email(client):
    # Post the login data
    response = client.post(
        reverse("account:login"),
        {"email": "invalid.email", "password": "secure@password"},
    )

    # Assert the response status code
    assert response.status_code == 200

    # Check if the template is correct
    assertTemplateUsed(response, "account/login.html")

    # Assert error message response content
    assert b"Email: Enter a valid email address." in response.content


# Function to test login view with invalid password
@pytest.mark.django_db
def test_login_view_invalid_password(client):
    # Create a user
    user = UserFactory(password="secure@password")

    # Post the login data
    response = client.post(
        reverse("account:login"), {"email": user.email, "password": "invalid@password"}
    )

    # Assert the response status code
    assert response.status_code == 200

    # Check if the template is correct
    assertTemplateUsed(response, "account/login.html")

    # Assert the error message
    assert b"Invalid email or password" in response.content


# Function to test login view with non-existent user
@pytest.mark.django_db
def test_login_view_non_existent_user(client):
    # Post the login data
    response = client.post(
        reverse("account:login"),
        {"email": "non.user@example.com", "password": "secure@password"},
    )

    # Assert the response status code
    assert response.status_code == 200

    # Check if the template is correct
    assertTemplateUsed(response, "account/login.html")

    # Assert the error message
    assert b"Invalid email or password" in response.content


# Function to test login view with inactive user
@pytest.mark.django_db
def test_login_view_inactive_user(client):
    # Create an inactive user
    user = UserFactory(is_active=False)

    # Post the login data
    response = client.post(
        reverse("account:login"), {"email": user.email, "password": "secure@password"}
    )

    # Assert the response status code
    assert response.status_code == 200

    # Check if the template is correct
    assertTemplateUsed(response, "account/login.html")

    # Assert the error message
    assert b"Invalid email or password" in response.content
