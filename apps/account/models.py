# Imports
import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.password_validation import validate_password
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """User

    User class is used to represent a user in the database

    Inherits:
        AbstractUser

    Attributes:
        pkid (BigAutoField): The primary key of the user
        id (UUIDField): The unique identifier of the user
        username (str): The username of the user
        email (EmailField): The email address of the user
        first_name (str): The first name of the user
        last_name (str): The last name of the user

    Constants:
        EMAIL_FIELD (str): The email field of the user
        USERNAME_FIELD (str): The username field of the user
        REQUIRED_FIELDS (List[str]): The required fields for the user

    Meta:
        verbose_name (str): The verbose name of the user
        verbose_name_plural (str): The verbose name of the user
        ordering (List[str]): The ordering of the user

    Properties:
        full_name (str): The full name of the user

    Methods:
        set_password -> None: Set the password of the user
        clean -> None: Clean the user data
        save -> User: Save the user
    """

    # Attributes
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(verbose_name=_("Username"), max_length=60, unique=True)
    email = models.EmailField(
        verbose_name=_("Email Address"), unique=True, db_index=True
    )
    first_name = models.CharField(verbose_name=_("First Name"), max_length=60)
    last_name = models.CharField(verbose_name=_("Last Name"), max_length=60)

    # Constants for email and username fields
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    # Constants for required fields
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    # Meta
    class Meta:
        # Attributes
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["-date_joined"]

    # Property to get the full name
    @property
    def full_name(self) -> str:
        """Get the full name of the user.

        Returns:
            str: The full name of the user.
        """

        # Get the full name
        full_name = f"{self.first_name} {self.last_name}"

        # Return the full name
        return full_name.strip()

    # Method to set the password
    def set_password(self, raw_password: str) -> None:
        """Set the password of the user.

        Args:
            raw_password (str): The raw password.
        """

        # Validate the password
        validate_password(raw_password, self)

        # Call the parent set_password method
        super().set_password(raw_password)

    # Method to clean the user
    def clean(self) -> None:
        """Clean the user data.

        Raises:
            ValidationError: If the user data is not valid.
        """

        # Call the parent clean method
        super().clean()

        # Validate the password
        validate_password(self.password, self)

    # Method to save the user
    def save(self, *args, **kwargs) -> None:
        """Save the user.

        Args:
            *args: The arguments.
            **kwargs: The keyword arguments.

        Raises:
            ValidationError: If the user data is not valid.
        """

        # Validate the user data
        self.full_clean()

        # Call the parent save method
        super().save(*args, **kwargs)