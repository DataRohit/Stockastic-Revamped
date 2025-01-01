# Imports
import pytest

from apps.account.factories import UserFactory
from apps.account.forms import UserRegisterForm
from apps.account.models import User


# Function to test register form
@pytest.mark.django_db
def test_user_register_form():
    # Prepare register data
    user_data = {
        "username": "new.user",
        "email": "new.user@example.com",
        "first_name": "New",
        "last_name": "User",
        "password": "secure@password",
        "confirm_password": "secure@password",
    }

    # Get the initial user count
    count = User.objects.count()

    # Create register form
    form = UserRegisterForm(data=user_data)

    # Check if form is valid
    assert form.is_valid()

    # Save the form
    user = form.save()

    # Check if user is created
    assert User.objects.count() == count + 1

    # Check the user attributes
    assert user.username == user_data["username"]
    assert user.email == user_data["email"]
    assert user.first_name == user_data["first_name"]
    assert user.last_name == user_data["last_name"]
    assert user.is_active is True
    assert user.is_staff is False
    assert user.is_superuser is False

    # Check if password is set
    assert user.has_usable_password()

    # Check if password is correct
    assert user.check_password(user_data["password"])


# Function to test register form with empty username
@pytest.mark.django_db
def test_user_register_form_empty_username():
    # Prepare register data
    user_data = {
        "username": "",
        "email": "invalid.user@example.com",
        "first_name": "Invalid",
        "last_name": "User",
        "password": "secure@password",
        "confirm_password": "secure@password",
    }

    # Create register form
    form = UserRegisterForm(data=user_data)

    # Check if form is valid
    assert not form.is_valid()

    # Check if username field is in errors
    assert "username" in form.errors

    # Check error message
    assert form.errors["username"][0] == "This field is required."


# Function to test register form with empty email
@pytest.mark.django_db
def test_user_register_form_empty_email():
    # Prepare register data
    user_data = {
        "username": "invalid.user",
        "email": "",
        "first_name": "Invalid",
        "last_name": "User",
        "password": "secure@password",
        "confirm_password": "secure@password",
    }

    # Create register form
    form = UserRegisterForm(data=user_data)

    # Check if form is valid
    assert not form.is_valid()

    # Check if email field is in errors
    assert "email" in form.errors

    # Check error message
    assert form.errors["email"][0] == "This field is required."


# Function to test register form with empty first name
@pytest.mark.django_db
def test_user_register_form_empty_first_name():
    # Prepare register data
    user_data = {
        "username": "invalid.user",
        "email": "invalid.user@example.com",
        "first_name": "",
        "last_name": "User",
        "password": "secure@password",
        "confirm_password": "secure@password",
    }

    # Create register form
    form = UserRegisterForm(data=user_data)

    # Check if form is valid
    assert not form.is_valid()

    # Check if first name field is in errors
    assert "first_name" in form.errors

    # Check error message
    assert form.errors["first_name"][0] == "This field is required."


# Function to test register form with empty last name
@pytest.mark.django_db
def test_user_register_form_empty_last_name():
    # Prepare register data
    user_data = {
        "username": "invalid.user",
        "email": "invalid.user@example.com",
        "first_name": "Invalid",
        "last_name": "",
        "password": "secure@password",
        "confirm_password": "secure@password",
    }

    # Create register form
    form = UserRegisterForm(data=user_data)

    # Check if form is valid
    assert not form.is_valid()

    # Check if last name field is in errors
    assert "last_name" in form.errors

    # Check error message
    assert form.errors["last_name"][0] == "This field is required."


# Function to test register form with invalid username
@pytest.mark.django_db
def test_user_register_form_invalid_username():
    # Prepare register data
    user_data = {
        "username": "$invalid$user",
        "email": "invalid.user@example.com",
        "first_name": "Invalid",
        "last_name": "User",
        "password": "secure@password",
        "confirm_password": "secure@password",
    }

    # Create register form
    form = UserRegisterForm(data=user_data)

    # Check if form is valid
    assert not form.is_valid()

    # Check if username field is in errors
    assert "username" in form.errors

    # Check error message
    assert (
        form.errors["username"][0]
        == "Your username is not valid. A username can only contain letters, numbers, a dot, @ symbol, + symbol and a hyphen"
    )


# Function to test register form with invalid email
@pytest.mark.django_db
def test_user_register_form_invalid_email():
    # Prepare register data
    user_data = {
        "username": "invalid.user",
        "email": "invalid.email",
        "first_name": "Invalid",
        "last_name": "User",
        "password": "secure@password",
        "confirm_password": "secure@password",
    }

    # Create register form
    form = UserRegisterForm(data=user_data)

    # Check if form is valid
    assert not form.is_valid()

    # Check if email field is in errors
    assert "email" in form.errors

    # Check error message
    assert form.errors["email"][0] == "Enter a valid email address."


# Function to test register form with duplicate username
@pytest.mark.django_db
def test_user_register_form_duplicate_username():
    # Use UserFactory for creating test user
    existing_user = UserFactory.create(username="test.user")

    # Prepare register data
    user_data = {
        "username": existing_user.username,
        "email": "new.user@example.com",
        "first_name": "New",
        "last_name": "User",
        "password": "secure@password",
        "confirm_password": "secure@password",
    }

    # Create register form
    form = UserRegisterForm(data=user_data)

    # Check if form is valid
    assert not form.is_valid()

    # Check if username field is in errors
    assert "username" in form.errors

    # Check error message
    assert form.errors["username"][0] == "User with this Username already exists."


# Function to test register form with duplicate email
@pytest.mark.django_db
def test_user_register_form_duplicate_email():
    # Use UserFactory for creating test user
    existing_user = UserFactory.create(email="test.user@example.com")

    # Prepare register data
    user_data = {
        "username": "new.user",
        "email": existing_user.email,
        "first_name": "New",
        "last_name": "User",
        "password": "secure@password",
        "confirm_password": "secure@password",
    }

    # Create register form
    form = UserRegisterForm(data=user_data)

    # Check if form is valid
    assert not form.is_valid()

    # Check if email field is in errors
    assert "email" in form.errors

    # Check error message
    assert form.errors["email"][0] == "User with this Email Address already exists."


# Function to test register form with empty password
@pytest.mark.django_db
def test_user_register_form_empty_password():
    # Prepare register data
    user_data = {
        "username": "invalid.user",
        "email": "invalid.user@example.com",
        "first_name": "Invalid",
        "last_name": "User",
        "password": "",
        "confirm_password": "secure@password",
    }

    # Create register form
    form = UserRegisterForm(data=user_data)

    # Check if form is valid
    assert not form.is_valid()

    # Check if password field is in errors
    assert "password" in form.errors

    # Check error message
    assert form.errors["password"][0] == "This field is required."


# Function to test register form with empty confirm password
@pytest.mark.django_db
def test_user_register_form_empty_confirm_password():
    # Prepare register data
    user_data = {
        "username": "invalid.user",
        "email": "invalid.user@example.com",
        "first_name": "Invalid",
        "last_name": "User",
        "password": "secure@password",
        "confirm_password": "",
    }

    # Create register form
    form = UserRegisterForm(data=user_data)

    # Check if form is valid
    assert not form.is_valid()

    # Check if confirm password field is in errors
    assert "confirm_password" in form.errors

    # Check error message
    assert form.errors["confirm_password"][0] == "This field is required."


# Function to test register form with passwords do not match
@pytest.mark.django_db
def test_user_register_form_passwords_do_not_match():
    # Prepare register data
    user_data = {
        "username": "invalid.user",
        "email": "invalid.user@example.com",
        "first_name": "Invalid",
        "last_name": "User",
        "password": "secure@password",
        "confirm_password": "password@secure",
    }

    # Create register form
    form = UserRegisterForm(data=user_data)

    # Check if form is valid
    assert not form.is_valid()

    # Check if __all__ field is in errors
    assert "__all__" in form.errors

    # Check error message
    assert form.errors["__all__"][0] == "Passwords do not match."


# Function to test register form with weak password
@pytest.mark.django_db
def test_user_register_form_weak_password():
    # Prepare register data
    user_data = {
        "username": "invalid.user",
        "email": "invalid.user@example.com",
        "first_name": "Invalid",
        "last_name": "User",
        "password": "password",
        "confirm_password": "password",
    }

    # Create register form
    form = UserRegisterForm(data=user_data)

    # Check if form is valid
    assert not form.is_valid()

    # Check if password field is in errors
    assert "password" in form.errors

    # Check error message
    assert form.errors["password"][0] == "This password is too common."


# Function to test register form with similar password
@pytest.mark.django_db
def test_user_register_form_similar_password():
    # Prepare register data
    user_data = {
        "username": "invalid.user",
        "email": "invalid.user@example.com",
        "first_name": "Invalid",
        "last_name": "User",
        "password": "invalid.user",
        "confirm_password": "invalid.user",
    }

    # Create register form
    form = UserRegisterForm(data=user_data)

    # Check if form is valid
    assert not form.is_valid()

    # Check if __all__ field is in errors
    assert "__all__" in form.errors

    # Check error message
    assert form.errors["__all__"][0] == "The password is too similar to the Username."


# Function to test register form with numeric password
@pytest.mark.django_db
def test_user_register_form_numeric_password():
    # Prepare register data
    user_data = {
        "username": "invalid.user",
        "email": "invalid.user@example.com",
        "first_name": "Invalid",
        "last_name": "User",
        "password": "299782779",
        "confirm_password": "299782779",
    }

    # Create register form
    form = UserRegisterForm(data=user_data)

    # Check if form is valid
    assert not form.is_valid()

    # Check if password field is in errors
    assert "password" in form.errors

    # Check error message
    assert form.errors["password"][0] == "This password is entirely numeric."
