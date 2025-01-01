# Imports
import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from apps.account.factories import UserFactory


# Function to test profile view
@pytest.mark.django_db
def test_profile_view(client):
    # Use UserFactory for creating test user
    user = UserFactory()

    # Log the user in
    client.force_login(user)

    # Get the profile page
    response = client.get(reverse("account:profile"))

    # Check if the status code is 200
    assert response.status_code == 200

    # Check if the correct template is used
    assertTemplateUsed(response, "account/profile.html")


# Function to test profile view when user is not logged in
@pytest.mark.django_db
def test_profile_view_not_logged_in(client):
    # Get the profile page
    response = client.get(reverse("account:profile"))

    # Assert the response status code
    assert response.status_code == 302

    # Follow the redirect url
    response = client.get(response.url)

    # Assert the response status code
    assert response.status_code == 200

    # Assert the correct template is used
    assertTemplateUsed(response, "account/login.html")

    # Assert that the user is authenticated and is the correct user
    assert not response.context["request"].user.is_authenticated

    # Assert that the context contains the user (should be anonymous)
    assert "user" in response.context
    assert response.context["user"].is_anonymous


# Function to test profile view with valid data
@pytest.mark.django_db
def test_profile_view_valid_data(client, test_image):
    # Use UserFactory for creating test user
    user = UserFactory()

    # Log the user in
    client.force_login(user)

    # Generate a test image using the fixture
    avatar_file = test_image()

    # Prepare update data
    update_data = {
        "username": "updated.user",
        "email": "updated.user@example.com",
        "first_name": "Updated",
        "last_name": "User",
    }

    # Get the profile page
    response = client.post(
        reverse("account:profile"), data=update_data, files={"avatar": avatar_file}
    )

    # Assert the response status code
    assert response.status_code == 302

    # Follow the redirect url
    response = client.get(response.url)

    # Assert the response status code
    assert response.status_code == 200

    # Assert the correct template is used
    assertTemplateUsed(response, "account/profile.html")

    # Assert success message response content
    assert b"Your profile has been updated!" in response.content


# Function to test profile view with empty username
@pytest.mark.django_db
def test_profile_view_empty_username(client):
    # Use UserFactory for creating test user
    user = UserFactory()

    # Log the user in
    client.force_login(user)

    # Prepare update data
    update_data = {
        "username": "",
    }

    # Get the profile page
    response = client.post(reverse("account:profile"), data=update_data)

    # Assert the response status code
    assert response.status_code == 200

    # Assert the correct template is used
    assertTemplateUsed(response, "account/profile.html")

    # Assert error message response content
    assert b"Username: This field is required." in response.content


# Function to test profile view with empty email
@pytest.mark.django_db
def test_profile_view_empty_email(client):
    # Use UserFactory for creating test user
    user = UserFactory()

    # Log the user in
    client.force_login(user)

    # Prepare update data
    update_data = {
        "email": "",
    }

    # Get the profile page
    response = client.post(reverse("account:profile"), data=update_data)

    # Assert the response status code
    assert response.status_code == 200

    # Assert the correct template is used
    assertTemplateUsed(response, "account/profile.html")

    # Assert error message response content
    assert b"Email: This field is required." in response.content


# Function to test profile view with empty first name
@pytest.mark.django_db
def test_profile_view_empty_first_name(client):
    # Use UserFactory for creating test user
    user = UserFactory()

    # Log the user in
    client.force_login(user)

    # Prepare update data
    update_data = {
        "first_name": "",
    }

    # Get the profile page
    response = client.post(reverse("account:profile"), data=update_data)

    # Assert the response status code
    assert response.status_code == 200

    # Assert the correct template is used
    assertTemplateUsed(response, "account/profile.html")

    # Assert error message response content
    assert b"FirstName: This field is required." in response.content


# Function to test profile view with empty last name
@pytest.mark.django_db
def test_profile_view_empty_last_name(client):
    # Use UserFactory for creating test user
    user = UserFactory()

    # Log the user in
    client.force_login(user)

    # Prepare update data
    update_data = {
        "last_name": "",
    }

    # Get the profile page
    response = client.post(reverse("account:profile"), data=update_data)

    # Assert the response status code
    assert response.status_code == 200

    # Assert the correct template is used
    assertTemplateUsed(response, "account/profile.html")

    # Assert error message response content
    assert b"LastName: This field is required." in response.content


# Function to test profile view with invalid username
@pytest.mark.django_db
def test_profile_view_invalid_username(client):
    # Use UserFactory for creating test user
    user = UserFactory()

    # Log the user in
    client.force_login(user)

    # Prepare update data
    update_data = {
        "username": "$invalid$user",
    }

    # Get the profile page
    response = client.post(reverse("account:profile"), data=update_data)

    # Assert the response status code
    assert response.status_code == 200

    # Assert the correct template is used
    assertTemplateUsed(response, "account/profile.html")

    # Assert error message response content
    assert (
        b"Username: Your username is not valid. A username can only contain letters, numbers, a dot, @ symbol, + symbol and a hyphen"
        in response.content
    )


# Function to test profile view with invalid email
@pytest.mark.django_db
def test_profile_view_invalid_email(client):
    # Use UserFactory for creating test user
    user = UserFactory()

    # Log the user in
    client.force_login(user)

    # Prepare update data
    update_data = {
        "email": "invalidemail",
    }

    # Get the profile page
    response = client.post(reverse("account:profile"), data=update_data)

    # Assert the response status code
    assert response.status_code == 200

    # Assert the correct template is used
    assertTemplateUsed(response, "account/profile.html")

    # Assert error message response content
    assert b"Email: Enter a valid email address." in response.content


# Function to test profile view with duplicate username
@pytest.mark.django_db
def test_profile_view_duplicate_username(client):
    # Use UserFactory for creating test users
    user1 = UserFactory()
    user2 = UserFactory()

    # Log the user in
    client.force_login(user1)

    # Prepare update data
    update_data = {
        "username": user2.username,
    }

    # Get the profile page
    response = client.post(reverse("account:profile"), data=update_data)

    # Assert the response status code
    assert response.status_code == 200

    # Assert the correct template is used
    assertTemplateUsed(response, "account/profile.html")

    # Assert error message response content
    assert b"Username: Username is already taken." in response.content


# Function to test profile view with duplicate email
@pytest.mark.django_db
def test_profile_view_duplicate_email(client):
    # Use UserFactory for creating test users
    user1 = UserFactory()
    user2 = UserFactory()

    # Log the user in
    client.force_login(user1)

    # Prepare update data
    update_data = {
        "email": user2.email,
    }

    # Get the profile page
    response = client.post(reverse("account:profile"), data=update_data)

    # Assert the response status code
    assert response.status_code == 200

    # Assert the correct template is used
    assertTemplateUsed(response, "account/profile.html")

    # Assert error message response content
    assert b"Email: Email is already taken." in response.content
