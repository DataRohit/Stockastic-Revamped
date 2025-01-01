# Imports
import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from apps.account.factories import UserFactory


# Function to test register view
@pytest.mark.django_db
def test_register_view(client):
    # Get the register page
    response = client.get(reverse("account:register"))

    # Assert the response status code
    assert response.status_code == 200

    # Check if the template is correct
    assertTemplateUsed(response, "account/register.html")


# Function to test register view with valid data
@pytest.mark.django_db
def test_register_view_valid_data(client):
    # Post the register data
    response = client.post(
        reverse("account:register"),
        {
            "username": "new.user",
            "email": "new.user@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "secure@password",
            "confirm_password": "secure@password",
        },
    )

    # Assert the response status code
    assert response.status_code == 302

    # Check the response URL
    assert response.url == reverse("account:login")

    # Follow the redirect url
    response = client.get(response.url)

    # Assert success message in the content
    assert b"Your account has been created!" in response.content


# Function to test register view with empty username
@pytest.mark.django_db
def test_register_view_empty_username(client):
    # Post the register data
    response = client.post(
        reverse("account:register"),
        {
            "username": "",
            "email": "new.user@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "secure@password",
            "confirm_password": "secure@password",
        },
    )

    # Assert the response status code
    assert response.status_code == 200

    # Check if the template is correct
    assertTemplateUsed(response, "account/register.html")

    # Assert error message response content
    assert b"Username: This field is required." in response.content


# Function to test register view with empty email
@pytest.mark.django_db
def test_register_view_empty_email(client):
    # Post the register data
    response = client.post(
        reverse("account:register"),
        {
            "username": "new.user",
            "email": "",
            "first_name": "New",
            "last_name": "User",
            "password": "secure@password",
            "confirm_password": "secure@password",
        },
    )

    # Assert the response status code
    assert response.status_code == 200

    # Check if the template is correct
    assertTemplateUsed(response, "account/register.html")

    # Assert error message response content
    assert b"Email: This field is required." in response.content


# Function to test register view with empty first name
@pytest.mark.django_db
def test_register_view_empty_first_name(client):
    # Post the register data
    response = client.post(
        reverse("account:register"),
        {
            "username": "new.user",
            "email": "new.user@example.com",
            "first_name": "",
            "last_name": "User",
            "password": "secure@password",
            "confirm_password": "secure@password",
        },
    )

    # Assert the response status code
    assert response.status_code == 200

    # Check if the template is correct
    assertTemplateUsed(response, "account/register.html")

    # Assert error message response content
    assert b"FirstName: This field is required." in response.content


# Function to test register view with empty last name
@pytest.mark.django_db
def test_register_view_empty_last_name(client):
    # Post the register data
    response = client.post(
        reverse("account:register"),
        {
            "username": "new.user",
            "email": "new.user@example.com",
            "first_name": "New",
            "last_name": "",
            "password": "secure@password",
            "confirm_password": "secure@password",
        },
    )

    # Assert the response status code
    assert response.status_code == 200

    # Check if the template is correct
    assertTemplateUsed(response, "account/register.html")

    # Assert error message response content
    assert b"LastName: This field is required." in response.content


# Function to test register view with invalid username
@pytest.mark.django_db
def test_register_view_invalid_username(client):
    # Post the register data
    response = client.post(
        reverse("account:register"),
        {
            "username": "$new$user",
            "email": "new.user@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "secure@password",
            "confirm_password": "secure@password",
        },
    )

    # Assert the response status code
    assert response.status_code == 200

    # Check if the template is correct
    assertTemplateUsed(response, "account/register.html")

    # Assert error message response content
    assert (
        b"Your username is not valid. A username can only contain letters, numbers, a dot, @ symbol, + symbol and a hyphen"
        in response.content
    )


# Function to test register view with invalid email
@pytest.mark.django_db
def test_register_view_invalid_email(client):
    # Post the register data
    response = client.post(
        reverse("account:register"),
        {
            "username": "new.user",
            "email": "new.user",
            "first_name": "New",
            "last_name": "User",
            "password": "secure@password",
            "confirm_password": "secure@password",
        },
    )

    # Assert the response status code
    assert response.status_code == 200

    # Check if the template is correct
    assertTemplateUsed(response, "account/register.html")

    # Assert error message response content
    assert b"Email: Enter a valid email address." in response.content


# Function to test register view with duplicate username
@pytest.mark.django_db
def test_register_view_duplicate_username(client):
    # Create a user
    UserFactory(username="new.user")

    # Post the register data
    response = client.post(
        reverse("account:register"),
        {
            "username": "new.user",
            "email": "new.user@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "secure@password",
            "confirm_password": "secure@password",
        },
    )

    # Assert the response status code
    assert response.status_code == 200

    # Check if the template is correct
    assertTemplateUsed(response, "account/register.html")

    # Assert error message response content
    assert b"Username: User with this Username already exists." in response.content


# Function to test register view with duplicate email
@pytest.mark.django_db
def test_register_view_duplicate_email(client):
    # Create a user
    UserFactory(email="new.user@example.com")

    # Post the register data
    response = client.post(
        reverse("account:register"),
        {
            "username": "new.user",
            "email": "new.user@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "secure@password",
            "confirm_password": "secure@password",
        },
    )

    # Assert the response status code
    assert response.status_code == 200

    # Check if the template is correct
    assertTemplateUsed(response, "account/register.html")

    # Assert error message response content
    assert b"Email: User with this Email Address already exists." in response.content


# Function to test register view with empty password
@pytest.mark.django_db
def test_register_view_empty_password(client):
    # Post the register data
    response = client.post(
        reverse("account:register"),
        {
            "username": "new.user",
            "email": "new.user@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "",
            "confirm_password": "secure@password",
        },
    )

    # Assert the response status code
    assert response.status_code == 200

    # Check if the template is correct
    assertTemplateUsed(response, "account/register.html")

    # Assert error message response content
    assert b"Password: This field is required." in response.content


# Function to test register view with empty confirm password
@pytest.mark.django_db
def test_register_view_empty_confirm_password(client):
    # Post the register data
    response = client.post(
        reverse("account:register"),
        {
            "username": "new.user",
            "email": "new.user@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "secure@password",
            "confirm_password": "",
        },
    )

    # Assert the response status code
    assert response.status_code == 200

    # Check if the template is correct
    assertTemplateUsed(response, "account/register.html")

    # Assert error message response content
    assert b"ConfirmPassword: This field is required." in response.content


# Function to test register view with password do not match
@pytest.mark.django_db
def test_register_view_password_do_not_match(client):
    # Post the register data
    response = client.post(
        reverse("account:register"),
        {
            "username": "new.user",
            "email": "new.user@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "secure@password",
            "confirm_password": "password@secure",
        },
    )

    # Assert the response status code
    assert response.status_code == 200

    # Check if the template is correct
    assertTemplateUsed(response, "account/register.html")

    # Assert error message response content
    assert b"All: Passwords do not match" in response.content


# Function to test register view with weak password
@pytest.mark.django_db
def test_register_view_weak_password(client):
    # Post the register data
    response = client.post(
        reverse("account:register"),
        {
            "username": "new.user",
            "email": "new.user@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "password",
            "confirm_password": "password",
        },
    )

    # Assert the response status code
    assert response.status_code == 200

    # Check if the template is correct
    assertTemplateUsed(response, "account/register.html")

    # Assert error message response content
    assert b"Password: This password is too common." in response.content


# Function to test register view with similar password
@pytest.mark.django_db
def test_register_view_similar_password(client):
    # Post the register data
    response = client.post(
        reverse("account:register"),
        {
            "username": "new.user",
            "email": "new.user@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "new.user",
            "confirm_password": "new.user",
        },
    )

    # Assert the response status code
    assert response.status_code == 200

    # Check if the template is correct
    assertTemplateUsed(response, "account/register.html")

    # Assert error message response content
    assert b"All: The password is too similar to the Username." in response.content


# Function to test register view with numeric password
@pytest.mark.django_db
def test_register_view_numeric_password(client):
    # Post the register data
    response = client.post(
        reverse("account:register"),
        {
            "username": "new.user",
            "email": "new.user@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "299782779",
            "confirm_password": "299782779",
        },
    )

    # Assert the response status code
    assert response.status_code == 200

    # Check if the template is correct
    assertTemplateUsed(response, "account/register.html")

    # Assert error message response content
    assert b"Password: This password is entirely numeric." in response.content
