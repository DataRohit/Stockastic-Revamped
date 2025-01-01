# Imports
from config.storage.base import CustomS3Boto3Storage


# Custom storage backend for media files
class MediaStorage(CustomS3Boto3Storage):
    """Custom Media Storage

    CustomMediaStorage class is used to create a custom storage backend for media files.

    Extends:
        CustomS3Boto3Storage

    Attributes:
        location (str): The location of the media files.
        default_acl (str): The default ACL for the media files.
        file_overwrite (bool): Whether to overwrite the file if it already exists.
    """

    # Attributes
    location = "media"
    default_acl = "private"
    file_overwrite = False
