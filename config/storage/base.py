# Imports
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


# Custom storage backend for S3
class CustomS3Boto3Storage(S3Boto3Storage):
    """Custom S3 Boto3 Storage

    CustomS3Boto3Storage class is used to create a custom storage backend for S3.

    Extends:
        S3Boto3Storage

    Attributes:
        endpoint_url (str): The endpoint URL of the S3 bucket.
        custom_domain (str): The custom domain of the S3 bucket.

    Methods:
        url -> str: Returns the URL of the file.
    """

    # Constructor
    def __init__(self, *args, **kwargs) -> None:
        # Call the parent constructor
        super().__init__(*args, **kwargs)

        # Set the endpoint URL and custom domain
        self.endpoint_url = settings.AWS_S3_ENDPOINT_URL
        self.custom_domain = settings.AWS_S3_CUSTOM_DOMAIN

    # Method to return the URL of the file
    def url(self, name, parameters=None, expire=None):
        """Get the URL of the file.

        Args:
            name (str): The name of the file.
            parameters (dict): The parameters for the URL.
            expire (int): The expiration time for the URL.

        Returns:
            str: The URL of the file.
        """

        # Get the URL
        url = super().url(name, parameters, expire)

        # If the urls starts with https
        if url.startswith("https"):
            # Replace https with http
            url = "http" + url[5:]

        # Return the URL
        return url
