# Imports
import pytest

from apps.account.factories import UserFactory
from apps.account.forms import UserUpdateForm
from apps.account.models import User


# Function to test update form
@pytest.mark.django_db
def test_user_update_form(test_image):
    # Use UserFactory for creating test user
    user = UserFactory()

    # Generate a test image using the fixture
    avatar_file = test_image()

    # Get avatar file extension
    avatar_file_extension = avatar_file.name.split(".")[-1]

    # Prepare update data
    update_data = {
        "username": "updated.user",
        "email": "updated.user@example.com",
        "first_name": "Updated",
        "last_name": "User",
    }

    # Create update form
    form = UserUpdateForm(
        data=update_data, instance=user, files={"avatar": avatar_file}
    )

    # Check if form is valid
    assert form.is_valid()

    # Save the form
    form.save()

    # Get the updated user
    updated_user = User.objects.get(id=user.id)

    # User update checks
    assert updated_user.username == update_data["username"]
    assert updated_user.email == update_data["email"]
    assert updated_user.first_name == update_data["first_name"]
    assert updated_user.last_name == update_data["last_name"]
    assert (
        updated_user.avatar.name == f"avatars/{updated_user.id}.{avatar_file_extension}"
    )


# Function to test update form with empty username
@pytest.mark.django_db
def test_user_update_form_empty_username():
    # Use UserFactory for creating test user
    user = UserFactory()

    # Prepare update data
    update_data = {
        "username": "",
    }

    # Create update form
    form = UserUpdateForm(data=update_data, instance=user)

    # Check if form is invalid
    assert not form.is_valid()

    # Check if username field has error
    assert "username" in form.errors

    # Check error message
    assert form.errors["username"][0] == "This field is required."


# Function to test update form with empty email
@pytest.mark.django_db
def test_user_update_form_empty_email():
    # Use UserFactory for creating test user
    user = UserFactory()

    # Prepare update data
    update_data = {
        "email": "",
    }

    # Create update form
    form = UserUpdateForm(data=update_data, instance=user)

    # Check if form is invalid
    assert not form.is_valid()

    # Check if email field has error
    assert "email" in form.errors

    # Check error message
    assert form.errors["email"][0] == "This field is required."


# Function to test update form with empty first name
@pytest.mark.django_db
def test_user_update_form_empty_first_name():
    # Use UserFactory for creating test user
    user = UserFactory()

    # Prepare update data
    update_data = {
        "first_name": "",
    }

    # Create update form
    form = UserUpdateForm(data=update_data, instance=user)

    # Check if form is invalid
    assert not form.is_valid()

    # Check if first name field has error
    assert "first_name" in form.errors

    # Check error message
    assert form.errors["first_name"][0] == "This field is required."


# Function to test update form with empty last name
@pytest.mark.django_db
def test_user_update_form_empty_last_name():
    # Use UserFactory for creating test user
    user = UserFactory()

    # Prepare update data
    update_data = {
        "last_name": "",
    }

    # Create update form
    form = UserUpdateForm(data=update_data, instance=user)

    # Check if form is invalid
    assert not form.is_valid()

    # Check if last name field has error
    assert "last_name" in form.errors

    # Check error message
    assert form.errors["last_name"][0] == "This field is required."


# Function to test update form with invalid username
@pytest.mark.django_db
def test_user_update_form_invalid_username():
    # Use UserFactory for creating test user
    user = UserFactory()

    # Prepare update data
    update_data = {
        "username": "$invalid$user",
    }

    # Create update form
    form = UserUpdateForm(data=update_data, instance=user)

    # Check if form is invalid
    assert not form.is_valid()

    # Check if username field has error
    assert "username" in form.errors

    # Check error message
    assert (
        form.errors["username"][0]
        == "Your username is not valid. A username can only contain letters, numbers, a dot, @ symbol, + symbol and a hyphen"
    )


# Function to test update form with invalid email
@pytest.mark.django_db
def test_user_update_form_invalid_email():
    # Use UserFactory for creating test user
    user = UserFactory()

    # Prepare update data
    update_data = {
        "email": "invalid.email",
    }

    # Create update form
    form = UserUpdateForm(data=update_data, instance=user)

    # Check if form is invalid
    assert not form.is_valid()

    # Check if email field has error
    assert "email" in form.errors

    # Check error message
    assert form.errors["email"][0] == "Enter a valid email address."


# Function to test update form with duplicate username
@pytest.mark.django_db
def test_user_update_form_duplicate_username():
    # Use UserFactory for creating test users
    user1 = UserFactory()
    user2 = UserFactory()

    # Prepare update data
    update_data = {
        "username": user2.username,
    }

    # Create update form
    form = UserUpdateForm(data=update_data, instance=user1)

    # Check if form is invalid
    assert not form.is_valid()

    # Check if username field has error
    assert "username" in form.errors

    # Check error message
    assert form.errors["username"][0] == "Username is already taken."


# Function to test update form with duplicate email
@pytest.mark.django_db
def test_user_update_form_duplicate_email():
    # Use UserFactory for creating test users
    user1 = UserFactory()
    user2 = UserFactory()

    # Prepare update data
    update_data = {
        "email": user2.email,
    }

    # Create update form
    form = UserUpdateForm(data=update_data, instance=user1)

    # Check if form is invalid
    assert not form.is_valid()

    # Check if email field has error
    assert "email" in form.errors

    # Check error message
    assert form.errors["email"][0] == "Email is already taken."
