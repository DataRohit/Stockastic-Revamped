# Imports
from config.storage.base import CustomS3Boto3Storage


# Custom storage backend for static files
class StaticStorage(CustomS3Boto3Storage):
    """Custom Static Storage

    CustomStaticStorage class is used to create a custom storage backend for static files.

    Extends:
        CustomS3Boto3Storage

    Attributes:
        location (str): The location of the static files.
        default_acl (str): The default ACL for the static files.
        file_overwrite (bool): Whether to overwrite the file if it already exists.
    """

    # Attributes
    location = "static"
    default_acl = "private"
    file_overwrite = False
