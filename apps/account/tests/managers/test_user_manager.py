# Imports
import pytest
from django.core.exceptions import ValidationError

from apps.account.factories import UserFactory
from apps.account.models import User


# Function to test create method - normal user creation
@pytest.mark.django_db
def test_create_method_normal_user_creation():
    # Get the initial count of users
    count = User.objects.count()

    # Create a new user
    user = User.objects.create(
        username="new.user",
        email="new.user@example.com",
        first_name="New",
        last_name="User",
        password="secure@password",
    )

    # Check the user count
    assert User.objects.count() == count + 1

    # Check the user attributes
    assert user.username == "new.user"
    assert user.email == "new.user@example.com"
    assert user.first_name == "New"
    assert user.last_name == "User"
    assert user.is_active is True
    assert user.is_staff is False
    assert user.is_superuser is False

    # Check the user password
    assert user.check_password("secure@password") is True


# Function to test create method - staff user creation
@pytest.mark.django_db
def test_create_method_staff_user_creation():
    # Get the initial count of users
    count = User.objects.count()

    # Create a new user
    user = User.objects.create(
        username="new.user",
        email="new.user@example.com",
        first_name="New",
        last_name="User",
        password="secure@password",
        is_staff=True,
    )

    # Check the user count
    assert User.objects.count() == count + 1

    # Check the user attributes
    assert user.username == "new.user"
    assert user.email == "new.user@example.com"
    assert user.first_name == "New"
    assert user.last_name == "User"
    assert user.is_active is True
    assert user.is_staff is True
    assert user.is_superuser is False

    # Check the user password
    assert user.check_password("secure@password") is True


# Function to test create method - superuser creation
@pytest.mark.django_db
def test_create_method_superuser_creation():
    # Get the initial count of users
    count = User.objects.count()

    # Create a new user
    user = User.objects.create(
        username="new.user",
        email="new.user@example.com",
        first_name="New",
        last_name="User",
        password="secure@password",
        is_staff=True,
        is_superuser=True,
    )

    # Check the user count
    assert User.objects.count() == count + 1

    # Check the user attributes
    assert user.username == "new.user"
    assert user.email == "new.user@example.com"
    assert user.first_name == "New"
    assert user.last_name == "User"
    assert user.is_active is True
    assert user.is_staff is True
    assert user.is_superuser is True

    # Check the user password
    assert user.check_password("secure@password") is True


# Function to test create_user method - normal user creation
@pytest.mark.django_db
def test_create_user_method_normal_user_creation():
    # Get the initial count of users
    count = User.objects.count()

    # Create a new user
    user = User.objects.create_user(
        username="new.user",
        email="new.user@example.com",
        first_name="New",
        last_name="User",
        password="secure@password",
    )

    # Check the user count
    assert User.objects.count() == count + 1

    # Check the user attributes
    assert user.username == "new.user"
    assert user.email == "new.user@example.com"
    assert user.first_name == "New"
    assert user.last_name == "User"
    assert user.is_active is True
    assert user.is_staff is False
    assert user.is_superuser is False

    # Check the user password
    assert user.check_password("secure@password") is True


# Function to test create_superuser method - superuser creation
@pytest.mark.django_db
def test_create_superuser_method_superuser_creation():
    # Get the initial count of users
    count = User.objects.count()

    # Create a new user
    user = User.objects.create_superuser(
        username="new.user",
        email="new.user@example.com",
        first_name="New",
        last_name="User",
        password="secure@password",
    )

    # Check the user count
    assert User.objects.count() == count + 1

    # Check the user attributes
    assert user.username == "new.user"
    assert user.email == "new.user@example.com"
    assert user.first_name == "New"
    assert user.last_name == "User"
    assert user.is_active is True
    assert user.is_staff is True
    assert user.is_superuser is True

    # Check the user password
    assert user.check_password("secure@password") is True


# Function to test user creation with invalid username
@pytest.mark.django_db
def test_user_creation_invalid_username():
    # Get the initial count of users
    count = User.objects.count()

    # Create a new user with invalid username
    with pytest.raises(ValidationError) as excinfo:
        # Create a new user
        User.objects.create(
            username="$invalid$user",
            email="invalid.user@example.com",
            first_name="Invalid",
            last_name="User",
            password="secure@password",
        )

    # Check that the exception contains 'username'
    exception_data = excinfo.value.message_dict
    assert "username" in exception_data

    # Check the specific error message for 'username'
    assert exception_data["username"] == [
        "Your username is not valid. A username can only contain letters, numbers, a dot, @ symbol, + symbol and a hyphen"
    ]

    # Check that no new user was created
    assert User.objects.count() == count


# Function to test user creation with invalid email
@pytest.mark.django_db
def test_user_creation_invalid_email():
    # Get the initial count of users
    count = User.objects.count()

    # Create a new user with invalid email
    with pytest.raises(ValidationError) as excinfo:
        # Create a new user
        User.objects.create(
            username="invalid.user",
            email="invalid.user@example",
            first_name="Invalid",
            last_name="User",
            password="secure@password",
        )

    # Check that the exception contains password error
    exception_value = excinfo.value
    assert any(
        "Enter a valid email address." in str(error)
        for error in exception_value.error_list
    )

    # Check that no new user was created
    assert User.objects.count() == count


# Function to test user creation with empty username
@pytest.mark.django_db
def test_user_creation_empty_username():
    # Get the initial count of users
    count = User.objects.count()

    # Create a new user with empty username
    with pytest.raises(ValueError, match="The username must be provided."):
        # Create a new user
        User.objects.create(
            username="",
            email="new.user@example.com",
            first_name="New",
            last_name="User",
            password="secure@password",
        )

    # Check that no new user was created
    assert User.objects.count() == count


# Function to test user creation with empty email
@pytest.mark.django_db
def test_user_creation_empty_email():
    # Get the initial count of users
    count = User.objects.count()

    # Create a new user with empty email
    with pytest.raises(ValueError, match="The email address must be provided."):
        # Create a new user
        User.objects.create(
            username="new.user",
            email="",
            first_name="New",
            last_name="User",
            password="secure@password",
        )

    # Check that no new user was created
    assert User.objects.count() == count


# Function to test user creation with empty first name
@pytest.mark.django_db
def test_user_creation_empty_first_name():
    # Get the initial count of users
    count = User.objects.count()

    # Create a new user with empty first name
    with pytest.raises(ValidationError) as excinfo:
        # Create a new user
        User.objects.create(
            username="new.user",
            email="new.user@example.com",
            first_name="",
            last_name="User",
            password="secure@password",
        )

    # Check that the exception contains 'first_name'
    exception_data = excinfo.value.message_dict
    assert "first_name" in exception_data

    # Check the specific error message for 'first_name'
    assert exception_data["first_name"] == ["This field cannot be blank."]

    # Check that no new user was created
    assert User.objects.count() == count


# Function to test user creation with empty last name
@pytest.mark.django_db
def test_user_creation_empty_last_name():
    # Get the initial count of users
    count = User.objects.count()

    # Create a new user with empty last name
    with pytest.raises(ValidationError) as excinfo:
        # Create a new user
        User.objects.create(
            username="new.user",
            email="new.user@example.com",
            first_name="New",
            last_name="",
            password="secure@password",
        )

    # Check that the exception contains 'last_name'
    exception_data = excinfo.value.message_dict
    assert "last_name" in exception_data

    # Check the specific error message for 'last_name'
    assert exception_data["last_name"] == ["This field cannot be blank."]

    # Check that no new user was created
    assert User.objects.count() == count


# Function to test user creation with duplicate username
@pytest.mark.django_db
def test_user_creation_duplicate_username():
    # Create a new user
    new_user = UserFactory()

    # Get the initial count of users
    count = User.objects.count()

    # Create a new user with duplicate username
    with pytest.raises(ValidationError) as excinfo:
        # Create a new user
        User.objects.create(
            username=new_user.username,
            email="new.user@example.com",
            first_name="New",
            last_name="User",
            password="secure@password",
        )

    # Check that the exception contains 'username'
    exception_data = excinfo.value.message_dict
    assert "username" in exception_data

    # Check the specific error message for 'username'
    assert exception_data["username"] == ["User with this Username already exists."]

    # Check that no new user was created
    assert User.objects.count() == count


# Function to test user creation with duplicate email
@pytest.mark.django_db
def test_user_creation_duplicate_email():
    # Create a new user
    user = UserFactory()

    # Get the initial count of users
    count = User.objects.count()

    # Create a new user with duplicate email
    with pytest.raises(ValidationError) as excinfo:
        # Create a new user
        User.objects.create(
            username="new.user",
            email=user.email,
            first_name="New",
            last_name="User",
            password="secure@password",
        )

    # Check that the exception contains 'email'
    exception_data = excinfo.value.message_dict
    assert "email" in exception_data

    # Check the specific error message for 'email'
    assert exception_data["email"] == ["User with this Email Address already exists."]

    # Check that no new user was created
    assert User.objects.count() == count


# Function to test user creation with empty password
@pytest.mark.django_db
def test_user_creation_empty_password():
    # Get the initial count of users
    count = User.objects.count()

    # Create a new user with empty password
    with pytest.raises(ValidationError) as excinfo:
        # Create a new user
        User.objects.create(
            username="new.user",
            email="new.user@example.com",
            first_name="New",
            last_name="User",
            password="",
        )

    # Check that the exception contains 'password'
    exception_data = excinfo.value.message_dict
    assert "password" in exception_data

    # Check the specific error message for 'password'
    assert exception_data["password"] == ["This field cannot be blank."]

    # Check that no new user was created
    assert User.objects.count() == count


# Function to test user creation with weak password
@pytest.mark.django_db
def test_user_creation_weak_password():
    # Get the initial count of users
    count = User.objects.count()

    # Create a new user with weak password
    with pytest.raises(ValidationError) as excinfo:
        # Create a new user
        user = User(
            username="new.user",
            email="new.user@example.com",
            first_name="New",
            last_name="User",
        )

        # Set weak password
        user.set_password("password")

        # Validate the data
        user.full_clean()

        # Save the user
        user.save()

    # Check that the exception contains password error
    exception_value = excinfo.value
    assert any(
        "This password is too common." in str(error)
        for error in exception_value.error_list
    )

    # Check that no new user was created
    assert User.objects.count() == count


# Function to test user creation with username similar password
@pytest.mark.django_db
def test_user_creation_username_similar_password():
    # Get the initial count of users
    count = User.objects.count()

    # Create a new user with username-similar password
    with pytest.raises(ValidationError) as excinfo:
        # Create a new user
        User.objects.create(
            username="new.user",
            email="new.user@example.com",
            first_name="New",
            last_name="User",
            password="new.user",
        )

    # Check that the exception contains password error
    exception_value = excinfo.value
    assert any(
        "The password is too similar to the Username." in str(error)
        for error in exception_value.error_list
    )

    # Check that no new user was created
    assert User.objects.count() == count


# Function to test user creation with numeric password
@pytest.mark.django_db
def test_user_creation_numeric_password():
    # Get the initial count of users
    count = User.objects.count()

    # Create a new user with numeric password
    with pytest.raises(ValidationError) as excinfo:
        # Create a new user
        User.objects.create(
            username="new.user",
            email="new.user@example.com",
            first_name="New",
            last_name="User",
            password="299782779",
        )

    # Check that the exception contains password error
    exception_value = excinfo.value
    assert any(
        "This password is entirely numeric." in str(error)
        for error in exception_value.error_list
    )

    # Check that no new user was created
    assert User.objects.count() == count
