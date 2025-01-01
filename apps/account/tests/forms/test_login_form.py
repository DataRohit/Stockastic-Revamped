# Imports
import pytest
from django.contrib.auth import authenticate

from apps.account.factories import UserFactory
from apps.account.forms import UserLoginForm


# Function to test user login
@pytest.mark.django_db
def test_user_login_form():
    # Use UserFactory for creating test user
    user = UserFactory.create(
        username="test.user",
        email="test.user@example.com",
        first_name="Test",
        last_name="User",
        password="secure@password",
    )

    # Prepare login data
    login_data = {"email": user.email, "password": "secure@password"}

    # Create login form
    form = UserLoginForm(data=login_data)

    # Check if form is valid
    assert form.is_valid()

    # Authenticate user
    authenticated_user = authenticate(email=user.email, password="secure@password")

    # User authentication checks
    assert authenticated_user is not None, "User should be authenticated"
    assert authenticated_user == user, "Authenticated user should match created user"

    # Check the user attributes
    assert authenticated_user.email == user.email
    assert authenticated_user.username == user.username
    assert authenticated_user.is_active is True
    assert authenticated_user.is_staff is False
    assert authenticated_user.is_superuser is False


# Function to test login form empty email
@pytest.mark.django_db
def test_login_form_empty_email():
    # Prepare login data
    login_data = {"email": "", "password": "secure@password"}

    # Create login form
    form = UserLoginForm(data=login_data)

    # Check if form is valid
    assert not form.is_valid()

    # Check if email field is in errors
    assert "email" in form.errors

    # Check error message
    assert form.errors["email"][0] == "This field is required."


# Function to test login form empty password
@pytest.mark.django_db
def test_login_form_empty_password():
    # Prepare login data
    login_data = {"email": "test.user@example.com", "password": ""}

    # Create login form
    form = UserLoginForm(data=login_data)

    # Check if form is valid
    assert not form.is_valid()

    # Check if password field is in errors
    assert "password" in form.errors

    # Check error message
    assert form.errors["password"][0] == "This field is required."


# Function to test login form invalid email
@pytest.mark.django_db
def test_login_form_invalid_email():
    # Prepare login data
    login_data = {"email": "invalid.email", "password": "secure@password"}

    # Create login form
    form = UserLoginForm(data=login_data)

    # Check if form is valid
    assert not form.is_valid()

    # Check if email field is in errors
    assert "email" in form.errors

    # Check error message
    assert form.errors["email"][0] == "Enter a valid email address."


# Function to test login from invalid password
@pytest.mark.django_db
def test_login_form_invalid_password():
    # Use UserFactory for creating test user
    user = UserFactory.create(
        username="test.user",
        email="test.user@example.com",
        first_name="Test",
        last_name="User",
        password="secure@password",
    )

    # Prepare login data
    login_data = {"email": user.email, "password": "invalid@password"}

    # Create login form
    form = UserLoginForm(data=login_data)

    # Check if form is valid
    assert form.is_valid()

    # Authenticate user
    authenticated_user = authenticate(
        email=login_data["email"], password=login_data["password"]
    )

    # User authentication checks
    assert authenticated_user is None


# Function to test login form non-existent user
@pytest.mark.django_db
def test_login_form_non_existent_user():
    # Prepare login data
    login_data = {"email": "test.user@example.com", "password": "secure@password"}

    # Create login form
    form = UserLoginForm(data=login_data)

    # Check if form is valid
    assert form.is_valid()

    # Authenticate user
    authenticated_user = authenticate(
        email=login_data["email"], password=login_data["password"]
    )

    # User authentication checks
    assert authenticated_user is None


# Function to test login form inactive user
@pytest.mark.django_db
def test_login_form_inactive_user():
    # Use UserFactory for creating test user
    user = UserFactory.create(
        username="test.user",
        email="test.user@example.com",
        first_name="Test",
        last_name="User",
        password="secure@password",
        is_active=False,
    )

    # Prepare login data
    login_data = {"email": user.email, "password": "secure@password"}

    # Create login form
    form = UserLoginForm(data=login_data)

    # Check if form is valid
    assert form.is_valid()

    # Authenticate user
    authenticated_user = authenticate(email=user.email, password="secure@password")

    # User authentication checks
    assert authenticated_user is None
