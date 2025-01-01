# Imports
import io

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from apps.account.factories import UserFactory


# Function to create users
@pytest.fixture
def users():
    # Create 10 users
    users = UserFactory.create_batch(10)

    # Return created users
    return users


# Function to create a test image
@pytest.fixture
def test_image():
    def _test_image(
        filename="test_avatar.jpg", size=(100, 100), image_format="JPEG"
    ) -> SimpleUploadedFile:
        """Create a test image

        Args:
            filename (str, optional): Defaults to "test_avatar.jpg".
            size (tuple, optional): Defaults to (100, 100).
            image_format (str, optional): Defaults to "JPEG".

        Returns:
            SimpleUploadedFile: Test image file
        """

        # Create a test image
        img = Image.new("RGB", size, color=(255, 0, 0))

        # Create a buffer
        buffer = io.BytesIO()

        # Save the image to the buffer
        img.save(buffer, format=image_format)

        # Seek to the beginning of the buffer
        buffer.seek(0)

        # Return the test image file
        return SimpleUploadedFile(
            name=filename,
            content=buffer.read(),
            content_type=f"image/{image_format.lower()}",
        )

    # Return the function
    return _test_image
