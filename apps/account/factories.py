# Imports
import factory
from factory.django import DjangoModelFactory
from faker import Faker

from apps.account.models import User

# Initialize the Faker
fake = Faker()


# User Factory
class UserFactory(DjangoModelFactory):
    """User Factory

    Inherits:
        factory.django.DjangoModelFactory

    Meta:
        model (model): User

    Attributes:
        first_name (str): factory.Faker
        last_name (str): factory.Faker
        username (str): factory.LazyAttribute
        email (str): factory.LazyAttribute
        password (str): Random unencoded string of length 12
    """

    # Meta Class
    class Meta:
        # Attributes
        model = User
        django_get_or_create = (
            "username",
            "email",
            "first_name",
            "last_name",
        )

    # Attributes
    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    last_name = factory.LazyAttribute(lambda _: fake.last_name())
    username = factory.LazyAttribute(
        lambda obj: f"{obj.first_name}.{obj.last_name}".lower()
    )
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.LazyAttribute(
        lambda _: fake.password(
            length=12, special_chars=True, digits=True, upper_case=True, lower_case=True
        )
    )

    # Class method to create a user
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # Get the user manager
        manager = model_class.objects

        # Create the user
        return manager.create(*args, **kwargs)
